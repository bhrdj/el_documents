#!/usr/bin/env python3
"""
Fix markdown issues that prevent PDF generation.
"""

import re
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

def preprocess_for_pdf(content):
    """
    Apply all preprocessing needed for PDF generation.
    """
    # Replace unicode brackets (˹˺) with regular brackets
    content = content.replace('˹', '[')
    content = content.replace('˺', ']')

    # Replace emoji and other problematic Unicode
    content = content.replace('🙏', '{prayer hands}')
    content = content.replace('📚', '[stack]')
    content = content.replace('⬅', '<-')
    content = content.replace('➡', '->')
    content = content.replace('⬆', '^')
    content = content.replace('⬇', 'v')

    # Handle other common problematic characters
    replacements = {
        '–': '--',
        '—': '---',
        '"': '"',
        '"': '"',
        ''': "'",
        ''': "'",
        '…': '...',
    }

    for old, new in replacements.items():
        content = content.replace(old, new)

    # Fix YAML parsing issues - add --- YAML delimiter at start to prevent interpretation
    # If content starts with a heading, add YAML front matter delimiter
    if not content.startswith('---'):
        content = '---\n\n' + content

    # Fix deeply nested lists
    content = fix_deep_nesting(content, max_depth=4)

    return content

def main():
    # Process problematic chapters - fix in place for 05_repaired
    problematic = [
        ('output/markdown/05_repaired/chapter_01_fixed.md', 'output/markdown/05_repaired/chapter_01_fixed.md'),
        ('output/markdown/05_repaired/chapter_04_fixed.md', 'output/markdown/05_repaired/chapter_04_fixed.md'),
        ('output/markdown/05_repaired/chapter_05.md', 'output/markdown/05_repaired/chapter_05.md'),
    ]

    for input_file, output_file in problematic:
        input_path = Path(input_file)
        output_path = Path(output_file)

        if not input_path.exists():
            print(f"Skipping {input_file} - not found")
            continue

        content = input_path.read_text(encoding='utf-8')
        fixed_content = preprocess_for_pdf(content)

        output_path.write_text(fixed_content, encoding='utf-8')
        print(f"✓ Fixed: {output_file}")

if __name__ == '__main__':
    main()
