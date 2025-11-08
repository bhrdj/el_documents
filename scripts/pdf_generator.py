#!/usr/bin/env python3
"""
Generate PDFs from markdown files with comprehensive preprocessing for LaTeX compatibility.

This is the consolidated PDF generation pipeline that automatically handles:
- Unicode emoji and symbols (comprehensive stripping of problematic characters)
- Smart quotes and special punctuation (en/em dashes, ellipsis, etc.)
- Deep list nesting (limits to 4 levels for LaTeX compatibility)
- YAML metadata parsing issues (disables pandoc YAML block parsing)
- Unicode brackets (˹˺ → [])

All preprocessing is automatic - no separate fix scripts needed.

Usage:
    .venv/bin/python scripts/pdf_generator.py

Output:
    PDFs written to output/pdfs/ directory

Input Sources (configured in main()):
    - chapter_00: output/markdown/03_edited/
    - chapter_01: output/markdown/05_repaired/
    - chapter_02-03: output/markdown/02_removedbullets/
    - chapter_04-05: output/markdown/05_repaired/
    - chapter_07-08: output/markdown/03_edited/
    - chapter_09: output/markdown/02_removedbullets/

Technical Details:
    - Uses pandoc with --from markdown-yaml_metadata_block
    - Temporary preprocessed files created during generation
    - Automatic cleanup of temp files
    - Reports success/failure for each chapter
"""

import re
import subprocess
import sys
import unicodedata
from pathlib import Path

def count_indent(line):
    """Count the indentation level of a list item."""
    if not line.strip().startswith('-'):
        return None
    spaces = len(line) - len(line.lstrip(' '))
    return spaces // 2  # Each level is 2 spaces

def fix_deep_nesting(content, max_depth=4):
    """
    Limit list nesting to max_depth levels to prevent LaTeX errors.
    """
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        depth = count_indent(line)
        if depth is not None and depth > max_depth:
            # Reduce to max depth
            new_indent = ' ' * (max_depth * 2)
            text = line.lstrip(' ')
            line = new_indent + text
        fixed_lines.append(line)

    return '\n'.join(fixed_lines)

def preprocess_markdown(content):
    """
    Replace problematic Unicode characters with LaTeX-safe alternatives.
    Consolidates all PDF preprocessing fixes into one pipeline.
    """
    # Replace unicode brackets (˹˺) with regular brackets
    content = content.replace('˹', '[')
    content = content.replace('˺', ']')

    # Strip all emoji and problematic Unicode (comprehensive approach)
    # Remove characters in emoji ranges and other problematic Unicode blocks
    def strip_problematic_unicode(text):
        result = []
        for char in text:
            # Keep basic Latin, common punctuation, and specific safe Unicode
            code = ord(char)
            # Allow: Basic Latin (0x0000-0x007F), Latin-1 Supplement (0x0080-0x00FF),
            #        newlines, tabs, and specific safe ranges
            if (code < 0x0080 or  # Basic ASCII
                (0x0080 <= code <= 0x00FF) or  # Latin-1 Supplement
                char in ['\n', '\t', '\r']):  # Whitespace
                result.append(char)
            else:
                # Replace with description or simple placeholder
                if unicodedata.category(char) == 'So':  # Symbol, other (emoji, etc.)
                    result.append('[symbol]')
                elif code >= 0x2B00:  # High Unicode (arrows, symbols, emoji)
                    result.append('[symbol]')
                else:
                    # Keep other characters like smart quotes (will be replaced below)
                    result.append(char)
        return ''.join(result)

    content = strip_problematic_unicode(content)

    # Handle other common problematic characters
    replacements = {
        '–': '--',  # en dash
        '—': '---',  # em dash
        '"': '"',
        '"': '"',
        ''': "'",
        ''': "'",
        '…': '...',
    }

    for old, new in replacements.items():
        content = content.replace(old, new)

    # Fix YAML parsing issues - remove incomplete YAML delimiters
    # This prevents pandoc from treating lines like "**Purpose**: text" as YAML
    if content.startswith('---\n\n'):
        # File has incomplete YAML delimiter - remove it entirely
        content = content[4:]  # Remove "---\n\n"

    # Remove leading blank lines
    content = content.lstrip('\n')

    # Escape colons after bold text to prevent YAML interpretation
    # Pattern: **Text**: -> **Text**\:
    content = re.sub(r'(\*\*[^*]+\*\*):', r'\1\\:', content)

    # Fix deeply nested lists (limit to 4 levels for LaTeX compatibility)
    content = fix_deep_nesting(content, max_depth=4)

    return content

def generate_pdf(input_file, output_file):
    """
    Generate PDF from markdown file with preprocessing.
    """
    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():
        print(f"Error: Input file not found: {input_file}")
        return False

    # Read and preprocess the markdown
    content = input_path.read_text(encoding='utf-8')
    processed_content = preprocess_markdown(content)

    # Create temporary file
    temp_file = input_path.parent / f"{input_path.stem}_temp.md"
    temp_file.write_text(processed_content, encoding='utf-8')

    try:
        # Generate PDF using pandoc
        # Disable YAML metadata parsing to prevent issues with **bold**: patterns
        cmd = [
            'pandoc',
            '--from', 'markdown-yaml_metadata_block',
            str(temp_file),
            '-o', str(output_path),
            '-V', 'geometry:margin=1in',
            '-V', 'fontsize=11pt',
            '--toc',
            '--number-sections'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error generating PDF for {input_file}:")
            print(result.stderr)
            return False

        print(f"✓ Generated: {output_path.name}")
        return True

    finally:
        # Clean up temporary file
        if temp_file.exists():
            temp_file.unlink()

def main():
    # Define latest version of each chapter
    # Using repaired chapters (05_repaired) for chapters 1, 4, 5
    chapters = [
        ('output/markdown/03_edited/chapter_00.md', 'output/pdfs/chapter_00.pdf'),
        ('output/markdown/05_repaired/chapter_01_fixed.md', 'output/pdfs/chapter_01.pdf'),
        ('output/markdown/02_removedbullets/chapter_02.md', 'output/pdfs/chapter_02.pdf'),
        ('output/markdown/02_removedbullets/chapter_03.md', 'output/pdfs/chapter_03.pdf'),
        ('output/markdown/05_repaired/chapter_04_fixed.md', 'output/pdfs/chapter_04.pdf'),
        ('output/markdown/05_repaired/chapter_05.md', 'output/pdfs/chapter_05.pdf'),
        ('output/markdown/03_edited/chapter_07.md', 'output/pdfs/chapter_07.pdf'),
        ('output/markdown/03_edited/chapter_08.md', 'output/pdfs/chapter_08.pdf'),
        ('output/markdown/02_removedbullets/chapter_09.md', 'output/pdfs/chapter_09.pdf'),
    ]

    print("Generating PDFs for all chapters...\n")

    success_count = 0
    fail_count = 0

    for input_file, output_file in chapters:
        if generate_pdf(input_file, output_file):
            success_count += 1
        else:
            fail_count += 1

    print(f"\n{'='*50}")
    print(f"PDF Generation Complete")
    print(f"{'='*50}")
    print(f"Successfully generated: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"\nPDFs are in: output/pdfs/")

if __name__ == '__main__':
    main()
