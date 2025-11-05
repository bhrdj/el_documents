#!/usr/bin/env python3
"""
Batch extract all chapters from the PDF using chapter boundaries.
"""

import json
import subprocess
import sys
from pathlib import Path


def main():
    """Extract all chapters based on chapter_boundaries.json"""

    # Load chapter boundaries
    boundaries_path = Path('output/chapter_boundaries.json')
    if not boundaries_path.exists():
        print(f"Error: {boundaries_path} not found", file=sys.stderr)
        print("Run with --find-chapters first to detect chapters", file=sys.stderr)
        return 1

    with open(boundaries_path, 'r', encoding='utf-8') as f:
        chapters = json.load(f)

    # Create output directory
    output_dir = Path('output/chapters/00_raw')
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = 'EL_CgManual_CURRENT_v016.pdf'

    print(f"Extracting {len(chapters)} chapters from {pdf_path}...")
    print()

    # Track Chapter 5 parts
    chapter_5_count = 0

    for chapter in chapters:
        chapter_num = chapter['chapter_number']
        chapter_marker = chapter['chapter_marker']
        start_page = chapter['page_number']
        end_page = chapter['end_page']

        # Handle duplicate Chapter 5
        if chapter_num == '5':
            chapter_5_count += 1
            safe_filename = f"chapter_{chapter_num}_part{chapter_5_count}.md"
            display_name = f"Chapter {chapter_num} Part {chapter_5_count}"
        else:
            safe_filename = f"chapter_{chapter_num}.md"
            display_name = f"Chapter {chapter_num}"

        output_path = output_dir / safe_filename

        print(f"Extracting {display_name}: {chapter_marker}")
        print(f"  Pages: {start_page} to {end_page or 'end'}")
        print(f"  Output: {output_path}")

        # Build command
        cmd = [
            '.venv/bin/python',
            'scripts/reformat_manual/extract_pdf.py',
            pdf_path,
            '--chapter', chapter_marker,
            '--start-page', str(start_page),
            '--output-text', str(output_path)
        ]

        if end_page:
            cmd.extend(['--end-page', str(end_page)])

        # Run extraction
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"  ERROR: {result.stderr}", file=sys.stderr)
            return 1

        print(f"  ✓ Extracted successfully")
        print()

    print(f"All chapters extracted to {output_dir}/")
    return 0


if __name__ == '__main__':
    sys.exit(main())
