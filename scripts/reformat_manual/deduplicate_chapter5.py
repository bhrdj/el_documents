#!/usr/bin/env python3
"""
Remove duplicate sections from merged Chapter 5.

Keeps the first occurrence of each unique heading (section number).
"""

import re
from pathlib import Path
from typing import List, Tuple


def deduplicate_chapter(content: str) -> Tuple[str, int]:
    """
    Remove duplicate sections, keeping the first occurrence.

    Returns:
        Tuple of (deduplicated_content, number_of_duplicates_removed)
    """
    lines = content.split('\n')
    seen_headings = set()
    output_lines = []
    current_section_heading = None
    current_section_lines = []
    duplicates_removed = 0

    heading_pattern = re.compile(r'^(#{1,6})\s+(\d+(?:\.\d+)*)\s*(.*)')

    for line in lines:
        match = heading_pattern.match(line)

        if match:
            # Save previous section if it wasn't a duplicate
            if current_section_heading:
                if current_section_heading not in seen_headings:
                    output_lines.extend(current_section_lines)
                    seen_headings.add(current_section_heading)
                else:
                    duplicates_removed += 1
                    print(f"  Removing duplicate: {current_section_heading}")

            # Start new section
            section_number = match.group(2)
            current_section_heading = section_number
            current_section_lines = [line]
        else:
            # Add line to current section
            if current_section_heading is None:
                # Header content before first section
                output_lines.append(line)
            else:
                current_section_lines.append(line)

    # Don't forget the last section
    if current_section_heading:
        if current_section_heading not in seen_headings:
            output_lines.extend(current_section_lines)
        else:
            duplicates_removed += 1
            print(f"  Removing duplicate: {current_section_heading}")

    return '\n'.join(output_lines), duplicates_removed


def main():
    """Main deduplication process."""
    # Paths
    repo_root = Path(__file__).parent.parent.parent
    input_file = repo_root / "output" / "chapters" / "03_merged" / "chapter_05.md"
    output_file = repo_root / "output" / "chapters" / "03_merged" / "chapter_05_deduplicated.md"

    print("Chapter 5 Deduplication")
    print("=" * 60)
    print()

    # Read merged chapter
    print(f"Reading: {input_file}")
    content = input_file.read_text(encoding='utf-8')

    # Count original sections
    original_headings = len(re.findall(r'^#{1,6}\s+\d+(?:\.\d+)*', content, re.MULTILINE))
    print(f"Original sections: {original_headings}")
    print()

    # Deduplicate
    print("Removing duplicates...")
    deduplicated_content, duplicates_removed = deduplicate_chapter(content)
    print()

    # Count final sections
    final_headings = len(re.findall(r'^#{1,6}\s+\d+(?:\.\d+)*', deduplicated_content, re.MULTILINE))

    # Write output
    print(f"Writing: {output_file}")
    output_file.write_text(deduplicated_content, encoding='utf-8')

    # Summary
    print()
    print("=" * 60)
    print("Deduplication Complete!")
    print()
    print(f"Original sections: {original_headings}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Final sections: {final_headings}")
    print()
    print(f"Output: {output_file}")


if __name__ == "__main__":
    main()
