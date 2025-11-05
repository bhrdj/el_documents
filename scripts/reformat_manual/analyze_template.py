#!/usr/bin/env python3
"""
Template analysis script for analyzing Chapter 0 and Chapter 2 formatting.
Extracts formatting patterns to document in the formatting guide.
"""

import sys
import json
import argparse
from pathlib import Path
from collections import Counter

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.pdf_utils import extract_chapter, detect_headings


def analyze_heading_patterns(text: str) -> dict:
    """
    Analyze heading patterns in the text.

    Returns dictionary with heading analysis.
    """
    lines = text.split('\n')
    heading_patterns = {
        'all_caps': [],
        'numbered': [],
        'bracketed': [],
        'short_lines': []
    }

    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if not line_stripped:
            continue

        # All caps (potential heading)
        if line_stripped.isupper() and len(line_stripped) > 2:
            heading_patterns['all_caps'].append({
                'text': line_stripped,
                'line_num': i
            })

        # Numbered headings (e.g., "1.2 Title")
        import re
        if re.match(r'^(\d+\.)+\d*\s+', line_stripped):
            heading_patterns['numbered'].append({
                'text': line_stripped,
                'line_num': i
            })

        # Bracketed headings (e.g., "[1.2 Title")
        if re.match(r'^\[.*\d+\.', line_stripped):
            heading_patterns['bracketed'].append({
                'text': line_stripped,
                'line_num': i
            })

        # Short lines followed by blank (potential heading)
        if (len(line_stripped) < 80 and
            i + 1 < len(lines) and
            not lines[i + 1].strip()):
            heading_patterns['short_lines'].append({
                'text': line_stripped,
                'line_num': i
            })

    return heading_patterns


def analyze_list_patterns(text: str) -> dict:
    """
    Analyze list formatting patterns.

    Returns dictionary with list analysis.
    """
    lines = text.split('\n')
    list_patterns = {
        'bullet_markers': Counter(),
        'numbered_lists': [],
        'indentation_levels': []
    }

    import re

    for line in lines:
        # Count bullet markers
        if re.match(r'^\s*[●•\-\*]\s+', line):
            marker = re.match(r'^\s*([●•\-\*])', line).group(1)
            list_patterns['bullet_markers'][marker] += 1

            # Track indentation
            indent = len(line) - len(line.lstrip())
            list_patterns['indentation_levels'].append(indent)

        # Numbered lists
        if re.match(r'^\s*\d+[\.\)]\s+', line):
            list_patterns['numbered_lists'].append(line.strip())

    return list_patterns


def analyze_unicode_brackets(text: str) -> dict:
    """
    Analyze unicode bracket usage patterns.

    Returns dictionary with unicode bracket analysis.
    """
    import re

    # Common unicode brackets
    unicode_brackets = {
        '˹': 'LEFT TORTOISE SHELL BRACKET (U+02F9)',
        '˺': 'RIGHT TORTOISE SHELL BRACKET (U+02FA)',
        '〔': 'LEFT TORTOISE SHELL BRACKET (U+3014)',
        '〕': 'RIGHT TORTOISE SHELL BRACKET (U+3015)',
        '【': 'LEFT BLACK LENTICULAR BRACKET (U+3010)',
        '】': 'RIGHT BLACK LENTICULAR BRACKET (U+3011)',
        '「': 'LEFT CORNER BRACKET (U+300C)',
        '」': 'RIGHT CORNER BRACKET (U+300D)'
    }

    bracket_usage = {}
    examples = {}

    for bracket, description in unicode_brackets.items():
        count = text.count(bracket)
        if count > 0:
            bracket_usage[bracket] = {
                'count': count,
                'description': description
            }

            # Find examples
            pattern = f'[^{bracket}]*{bracket}[^{bracket}]*'
            matches = re.findall(f'.{{0,40}}{re.escape(bracket)}.{{0,40}}', text)
            examples[bracket] = matches[:5]  # First 5 examples

    return {
        'bracket_usage': bracket_usage,
        'examples': examples
    }


def analyze_spacing_patterns(text: str) -> dict:
    """
    Analyze spacing patterns in the text.

    Returns dictionary with spacing analysis.
    """
    lines = text.split('\n')

    spacing_patterns = {
        'consecutive_blank_lines': [],
        'paragraph_spacing': [],
        'section_spacing': []
    }

    blank_count = 0
    for i, line in enumerate(lines):
        if not line.strip():
            blank_count += 1
        else:
            if blank_count > 0:
                spacing_patterns['consecutive_blank_lines'].append(blank_count)
            blank_count = 0

    return spacing_patterns


def analyze_chapter(chapter_data: dict) -> dict:
    """
    Perform comprehensive analysis of a chapter.

    Args:
        chapter_data: Chapter data from extract_chapter

    Returns:
        Dictionary with complete analysis
    """
    text = chapter_data['full_text']

    analysis = {
        'chapter_name': chapter_data['chapter_name'],
        'page_count': chapter_data['page_count'],
        'heading_patterns': analyze_heading_patterns(text),
        'list_patterns': analyze_list_patterns(text),
        'unicode_brackets': analyze_unicode_brackets(text),
        'spacing_patterns': analyze_spacing_patterns(text),
        'detected_headings': chapter_data['headings']
    }

    return analysis


def main():
    """Analyze formatting patterns in template chapters."""
    parser = argparse.ArgumentParser(
        description='Analyze formatting patterns in Chapter 0 and Chapter 2'
    )
    parser.add_argument(
        'pdf_path',
        help='Path to the PDF file'
    )
    parser.add_argument(
        '--chapter-0-start',
        type=int,
        default=2,
        help='Chapter 0 start page (default: 2)'
    )
    parser.add_argument(
        '--chapter-0-end',
        type=int,
        default=8,
        help='Chapter 0 end page (default: 8)'
    )
    parser.add_argument(
        '--chapter-2-start',
        type=int,
        default=9,
        help='Chapter 2 start page (default: 9)'
    )
    parser.add_argument(
        '--chapter-2-end',
        type=int,
        default=30,
        help='Chapter 2 end page (default: 30)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='output/template_analysis.json',
        help='Output file path (JSON format)'
    )

    args = parser.parse_args()

    # Validate PDF file exists
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}", file=sys.stderr)
        return 1

    try:
        print("Analyzing Chapter 0...")
        chapter_0 = extract_chapter(
            str(pdf_path),
            "Chapter 0",
            args.chapter_0_start,
            args.chapter_0_end
        )
        analysis_0 = analyze_chapter(chapter_0)

        print("Analyzing Chapter 2...")
        chapter_2 = extract_chapter(
            str(pdf_path),
            "Chapter 2",
            args.chapter_2_start,
            args.chapter_2_end
        )
        analysis_2 = analyze_chapter(chapter_2)

        # Compare patterns
        print("\n=== ANALYSIS SUMMARY ===")
        print(f"\nChapter 0:")
        print(f"  Pages: {analysis_0['page_count']}")
        print(f"  All-caps headings: {len(analysis_0['heading_patterns']['all_caps'])}")
        print(f"  Numbered headings: {len(analysis_0['heading_patterns']['numbered'])}")
        print(f"  Bracketed headings: {len(analysis_0['heading_patterns']['bracketed'])}")
        print(f"  Unicode bracket types: {len(analysis_0['unicode_brackets']['bracket_usage'])}")

        print(f"\nChapter 2:")
        print(f"  Pages: {analysis_2['page_count']}")
        print(f"  All-caps headings: {len(analysis_2['heading_patterns']['all_caps'])}")
        print(f"  Numbered headings: {len(analysis_2['heading_patterns']['numbered'])}")
        print(f"  Bracketed headings: {len(analysis_2['heading_patterns']['bracketed'])}")
        print(f"  Unicode bracket types: {len(analysis_2['unicode_brackets']['bracket_usage'])}")

        # Save analysis
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        full_analysis = {
            'chapter_0': analysis_0,
            'chapter_2': analysis_2
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(full_analysis, f, indent=2, ensure_ascii=False)

        print(f"\nAnalysis saved to {output_path}")
        print("\nNext step: Review the analysis and document patterns in formatting-guide.md")

        return 0

    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
