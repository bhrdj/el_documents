#!/usr/bin/env python3
"""
Generate PDFs from markdown files, handling Unicode characters that cause LaTeX issues.
"""

import re
import subprocess
import sys
from pathlib import Path

def preprocess_markdown(content):
    """
    Replace problematic Unicode characters with LaTeX-safe alternatives.
    """
    # Replace unicode brackets (˹˺) with regular brackets
    content = content.replace('˹', '[')
    content = content.replace('˺', ']')

    # Replace emoji and other problematic Unicode
    content = content.replace('🙏', '{prayer hands}')

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
        cmd = [
            'pandoc',
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
    chapters = [
        ('output/chapters/03_edited/chapter_00.md', 'output/pdfs/chapter_00.pdf'),
        ('output/chapters/02_removedbullets/chapter_01.md', 'output/pdfs/chapter_01.pdf'),
        ('output/chapters/02_removedbullets/chapter_02.md', 'output/pdfs/chapter_02.pdf'),
        ('output/chapters/02_removedbullets/chapter_03.md', 'output/pdfs/chapter_03.pdf'),
        ('output/chapters/04_merged/chapter_04.md', 'output/pdfs/chapter_04.pdf'),
        ('output/chapters/04_merged/chapter_05_deduplicated.md', 'output/pdfs/chapter_05.pdf'),
        ('output/chapters/03_edited/chapter_07.md', 'output/pdfs/chapter_07.pdf'),
        ('output/chapters/03_edited/chapter_08.md', 'output/pdfs/chapter_08.pdf'),
        ('output/chapters/02_removedbullets/chapter_09.md', 'output/pdfs/chapter_09.pdf'),
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
