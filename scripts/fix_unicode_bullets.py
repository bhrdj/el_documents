#!/usr/bin/env python3
"""
Fix Unicode bullets in chapter files by converting them to markdown format.

This script uses the existing convert_document_bullets function from
markdown_utils to convert Unicode bullets (●, ○, ■) to proper markdown
bullets with correct indentation.
"""

import sys
from pathlib import Path

# Add reformat_manual/utils to path
sys.path.insert(0, str(Path(__file__).parent / "reformat_manual"))

from utils.markdown_utils import convert_document_bullets


def fix_unicode_bullets_in_file(input_file: Path, output_file: Path = None) -> None:
    """
    Fix Unicode bullets in a file.

    Args:
        input_file: Path to input file
        output_file: Path to output file (if None, overwrites input)
    """
    if not input_file.exists():
        raise FileNotFoundError(f"File not found: {input_file}")

    # Read content
    print(f"Reading: {input_file}")
    content = input_file.read_text(encoding='utf-8')

    # Convert Unicode bullets to markdown
    print("Converting Unicode bullets to markdown...")
    fixed_content = convert_document_bullets(content)

    # Write output
    if output_file is None:
        output_file = input_file

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(fixed_content, encoding='utf-8')
    print(f"✓ Fixed bullets written to: {output_file}")

    # Report statistics
    lines = fixed_content.split('\n')
    markdown_bullets = sum(1 for line in lines if line.lstrip().startswith('-'))
    unicode_bullets = sum(1 for line in lines if any(ub in line for ub in ['●', '○', '■']))

    print(f"  Markdown bullets: {markdown_bullets}")
    print(f"  Remaining Unicode bullets: {unicode_bullets}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: fix_unicode_bullets.py <input_file> [output_file]")
        print("Example: fix_unicode_bullets.py output/chapters/05_repaired/chapter_05.md")
        print("Example: fix_unicode_bullets.py input.md output.md")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    try:
        fix_unicode_bullets_in_file(input_file, output_file)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
