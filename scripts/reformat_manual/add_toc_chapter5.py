#!/usr/bin/env python3
"""
Add table of contents to Chapter 5.

Generates TOC from all headings in the chapter.
"""

import re
from pathlib import Path
from typing import List, Tuple


def extract_headings(content: str) -> List[Tuple[int, str, str]]:
    """
    Extract all headings from content.

    Returns:
        List of (level, number, title) tuples
    """
    headings = []
    heading_pattern = re.compile(r'^(#{2,6})\s+(\d+(?:\.\d+)*)\s*(.*)', re.MULTILINE)

    for match in heading_pattern.finditer(content):
        level = len(match.group(1))
        number = match.group(2)
        title = match.group(3).strip()
        headings.append((level, number, title))

    return headings


def generate_toc(headings: List[Tuple[int, str, str]]) -> str:
    """
    Generate table of contents from headings.
    """
    toc_lines = [
        "## Table of Contents",
        "",
    ]

    for level, number, title in headings:
        # Calculate indent (H2 = 0, H3 = 2, H4 = 4, etc.)
        indent = "  " * (level - 2)

        # Create anchor link (GitHub-style)
        anchor = number.replace(".", "")

        # Format TOC entry
        if title:
            entry = f"{indent}- [{number} {title}](#{number}-{title.lower().replace(' ', '-')})"
        else:
            entry = f"{indent}- [{number}](#{number})"

        toc_lines.append(entry)

    toc_lines.append("")
    toc_lines.append("---")
    toc_lines.append("")

    return "\n".join(toc_lines)


def add_toc_to_chapter(content: str) -> str:
    """
    Add table of contents after the chapter header.
    """
    lines = content.split('\n')

    # Find where to insert TOC (after the --- separator following the header)
    insert_index = 0
    found_separator = False

    for i, line in enumerate(lines):
        if line.strip() == '---':
            found_separator = True
            insert_index = i + 1
            break

    if not found_separator:
        # No separator found, insert after header
        insert_index = 15  # After the header block

    # Extract headings
    headings = extract_headings(content)

    # Generate TOC
    toc = generate_toc(headings)

    # Insert TOC
    lines.insert(insert_index, toc)

    return '\n'.join(lines)


def main():
    """Main TOC generation process."""
    # Paths
    repo_root = Path(__file__).parent.parent.parent
    input_file = repo_root / "output" / "chapters" / "03_merged" / "chapter_05_deduplicated.md"
    output_file = repo_root / "output" / "chapters" / "03_merged" / "chapter_05_with_toc.md"

    print("Chapter 5 Table of Contents Generation")
    print("=" * 60)
    print()

    # Read chapter
    print(f"Reading: {input_file}")
    content = input_file.read_text(encoding='utf-8')

    # Add TOC
    print("Generating table of contents...")
    content_with_toc = add_toc_to_chapter(content)

    # Count headings
    headings = extract_headings(content)
    print(f"  Generated TOC with {len(headings)} entries")

    # Write output
    print(f"Writing: {output_file}")
    output_file.write_text(content_with_toc, encoding='utf-8')

    print()
    print("=" * 60)
    print("TOC Generation Complete!")
    print()
    print(f"Output: {output_file}")


if __name__ == "__main__":
    main()
