#!/usr/bin/env python3
"""
Analyze Chapter 5 to identify logical sections between 5-9% of total word count.
"""

import re
from pathlib import Path
from typing import List, Tuple


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def extract_sections(file_path: Path) -> List[Tuple[str, str, int, int]]:
    """
    Extract sections from markdown with hierarchy.

    Returns:
        List of (level, heading, start_pos, word_count)
    """
    content = file_path.read_text()

    # Find all markdown headings with their positions
    heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)

    matches = list(heading_pattern.finditer(content))
    sections = []

    for i, match in enumerate(matches):
        level = len(match.group(1))  # Number of # symbols
        heading = match.group(2).strip()
        start_pos = match.start()

        # Find end position (next heading or end of file)
        if i < len(matches) - 1:
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(content)

        section_text = content[start_pos:end_pos]
        word_count = count_words(section_text)

        sections.append((level, heading, start_pos, end_pos, word_count))

    return content, sections


def find_logical_divisions(sections: List[Tuple], total_words: int,
                           min_pct: float = 0.05, max_pct: float = 0.09):
    """
    Find logical section groupings between min_pct and max_pct of total.
    """
    min_words = int(total_words * min_pct)
    max_words = int(total_words * max_pct)

    print(f"Total words: {total_words:,}")
    print(f"Target section size: {min_words:,} - {max_words:,} words ({min_pct*100}% - {max_pct*100}%)")
    print(f"\n{'='*80}")
    print("Section Analysis:")
    print(f"{'='*80}\n")

    divisions = []
    current_group = []
    current_words = 0
    current_start = 0

    for i, (level, heading, start_pos, end_pos, word_count) in enumerate(sections):
        # Print section info
        indent = "  " * (level - 1)
        print(f"{indent}{'#'*level} {heading}")
        print(f"{indent}   Words: {word_count:,} | Cumulative: {sum(s[4] for s in sections[:i+1]):,}")

        # Track top-level sections for grouping
        if level <= 2:  # Main sections (# or ##)
            if current_words > 0:
                # Check if adding this section would exceed max
                if current_words + word_count > max_words:
                    # Save current group if it meets minimum
                    if current_words >= min_words:
                        divisions.append({
                            'sections': current_group.copy(),
                            'start': current_start,
                            'end': start_pos,
                            'words': current_words
                        })
                        current_group = []
                        current_words = 0
                        current_start = start_pos

            if current_words == 0:
                current_start = start_pos

            current_group.append((level, heading, start_pos, end_pos, word_count))
            current_words += word_count

    # Add final group
    if current_words >= min_words:
        divisions.append({
            'sections': current_group,
            'start': current_start,
            'end': sections[-1][3] if sections else 0,
            'words': current_words
        })

    return divisions


def main():
    """Main execution."""
    file_path = Path("/home/steven/git/el_documents/output/markdown/05_repaired/ch05_v01.md")

    print("Analyzing Chapter 5 structure...\n")

    content, sections = extract_sections(file_path)
    total_words = count_words(content)

    # Find logical divisions
    divisions = find_logical_divisions(sections, total_words)

    print(f"\n{'='*80}")
    print(f"Proposed Division into {len(divisions)} sections:")
    print(f"{'='*80}\n")

    for i, div in enumerate(divisions, 1):
        pct = (div['words'] / total_words) * 100
        print(f"Section {i}: {div['words']:,} words ({pct:.1f}%)")
        for level, heading, _, _, wc in div['sections'][:3]:  # Show first 3 headings
            indent = "  " * level
            print(f"{indent}- {heading} ({wc:,} words)")
        if len(div['sections']) > 3:
            print(f"    ... and {len(div['sections']) - 3} more subsections")
        print()

    # Save division map
    output_path = Path("/home/steven/git/el_documents/output/markdown/05_repaired/section_divisions.txt")

    with output_path.open('w') as f:
        f.write(f"Chapter 5 Section Divisions\n")
        f.write(f"Total words: {total_words:,}\n")
        f.write(f"Target per section: 5-9% = {int(total_words*0.05):,} - {int(total_words*0.09):,} words\n\n")

        for i, div in enumerate(divisions, 1):
            pct = (div['words'] / total_words) * 100
            f.write(f"\n{'='*60}\n")
            f.write(f"SECTION {i}: {div['words']:,} words ({pct:.1f}%)\n")
            f.write(f"Character range: {div['start']:,} - {div['end']:,}\n")
            f.write(f"{'='*60}\n")

            for level, heading, start, end, wc in div['sections']:
                indent = "  " * (level - 1)
                f.write(f"{indent}{'#'*level} {heading} ({wc:,} words)\n")

    print(f"\nDivision map saved to: {output_path}")

    # Create section extraction info
    print(f"\n{'='*80}")
    print("Character Ranges for Extraction:")
    print(f"{'='*80}\n")

    for i, div in enumerate(divisions, 1):
        print(f"Section {i}: chars {div['start']:,} to {div['end']:,}")


if __name__ == "__main__":
    main()
