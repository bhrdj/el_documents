#!/usr/bin/env python3
"""
Main PDF extraction script for chapter-by-chapter extraction.
Extracts chapters from the EL Caregiver Manual PDF.
"""

import sys
import json
import argparse
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.pdf_utils import (
    extract_chapter,
    extract_text_by_page,
    find_chapter_boundaries,
    preserve_unicode
)


def main():
    """Extract chapters from the PDF."""
    parser = argparse.ArgumentParser(
        description='Extract chapters from EL Caregiver Manual PDF'
    )
    parser.add_argument(
        'pdf_path',
        help='Path to the PDF file'
    )
    parser.add_argument(
        '--chapter',
        type=str,
        help='Chapter name/identifier'
    )
    parser.add_argument(
        '--start-page',
        type=int,
        help='Starting page number (0-indexed)'
    )
    parser.add_argument(
        '--end-page',
        type=int,
        help='Ending page number (0-indexed)'
    )
    parser.add_argument(
        '--find-chapters',
        action='store_true',
        help='Automatically detect chapter boundaries'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path (JSON format)'
    )
    parser.add_argument(
        '--output-text',
        type=str,
        help='Output file path (plain text format)'
    )

    args = parser.parse_args()

    # Validate PDF file exists
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}", file=sys.stderr)
        return 1

    try:
        # Find chapters mode
        if args.find_chapters:
            print(f"Detecting chapter boundaries in {pdf_path}...")
            chapters = find_chapter_boundaries(str(pdf_path))

            print(f"\nFound {len(chapters)} chapter markers:")
            for i, chapter in enumerate(chapters, 1):
                end = f"to page {chapter['end_page']}" if chapter['end_page'] else "to end"
                print(f"  {i}. {chapter['chapter_marker']} (page {chapter['page_number']} {end})")

            if args.output:
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(chapters, f, indent=2, ensure_ascii=False)
                print(f"\nChapter boundaries saved to {output_path}")

            return 0

        # Extract chapter mode
        if args.chapter:
            print(f"Extracting chapter '{args.chapter}' from {pdf_path}...")

            chapter_data = extract_chapter(
                str(pdf_path),
                args.chapter,
                args.start_page,
                args.end_page
            )

            print(f"Extracted {chapter_data['page_count']} pages")
            print(f"Found {len(chapter_data['headings'])} potential headings")

            # Save as JSON
            if args.output:
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(chapter_data, f, indent=2, ensure_ascii=False)
                print(f"Chapter data saved to {output_path}")

            # Save as text
            if args.output_text:
                output_path = Path(args.output_text)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(chapter_data['full_text'])
                print(f"Chapter text saved to {output_path}")

            return 0

        # Extract all pages mode
        if args.start_page is not None or args.end_page is not None:
            print(f"Extracting pages {args.start_page or 0} to {args.end_page or 'end'}...")

            pages = extract_text_by_page(str(pdf_path), args.start_page, args.end_page)

            print(f"Extracted {len(pages)} pages")

            # Combine pages into full text
            full_text = "\n\n".join(page['text'] for page in pages)
            full_text = preserve_unicode(full_text)

            # Save as text
            if args.output_text:
                output_path = Path(args.output_text)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(full_text)
                print(f"Text saved to {output_path}")

            # Save as JSON
            if args.output:
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(pages, f, indent=2, ensure_ascii=False)
                print(f"Page data saved to {output_path}")

            return 0

        # No action specified
        print("Error: Please specify --chapter, --start-page/--end-page, or --find-chapters", file=sys.stderr)
        parser.print_help()
        return 1

    except Exception as e:
        print(f"Error during extraction: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
