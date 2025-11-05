#!/usr/bin/env python3
"""
Add table of contents to any chapter.

Usage:
    .venv/bin/python scripts/reformat_manual/add_toc_to_chapter.py <chapter_number>
    .venv/bin/python scripts/reformat_manual/add_toc_to_chapter.py 2
"""

import sys
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
    if not headings:
        return ""

    toc_lines = [
        "## Table of Contents",
        "",
    ]

    for level, number, title in headings:
        # Calculate indent (H2 = 0, H3 = 2, H4 = 4, etc.)
        indent = "  " * (level - 2)

        # Format TOC entry
        if title:
            # Create simplified anchor (just the number and title)
            anchor = f"{number}-{title.lower().replace(' ', '-').replace('/', '').replace('(', '').replace(')', '').replace(',', '').replace(':', '').replace('.', '')}"
            entry = f"{indent}- [{number} {title}](#{anchor})"
        else:
            entry = f"{indent}- [{number}](#{number})"

        toc_lines.append(entry)

    toc_lines.append("")
    toc_lines.append("---")
    toc_lines.append("")

    return "\n".join(toc_lines)


def has_toc(content: str) -> bool:
    """Check if content already has a table of contents."""
    return bool(re.search(r'^##\s+Table of Contents', content, re.MULTILINE | re.IGNORECASE))


def add_toc_to_chapter(content: str) -> str:
    """
    Add table of contents after the H1 title.
    """
    lines = content.split('\n')

    # Find insertion point (after H1 title + blank line)
    insert_index = 0
    found_h1 = False

    for i, line in enumerate(lines):
        if line.startswith('# '):
            found_h1 = True
            # Insert after H1 and any following blank lines
            insert_index = i + 1
            # Skip blank lines after H1
            while insert_index < len(lines) and not lines[insert_index].strip():
                insert_index += 1
            break

    if not found_h1:
        # No H1 found, insert at beginning
        insert_index = 0

    # Extract headings
    headings = extract_headings(content)

    if not headings:
        print("  ⚠️  No headings found to create TOC")
        return content

    # Generate TOC
    toc = generate_toc(headings)

    # Insert TOC
    lines.insert(insert_index, toc)

    return '\n'.join(lines)


def main():
    """Main TOC generation process."""
    if len(sys.argv) < 2:
        print("Usage: add_toc_to_chapter.py <chapter_number>")
        print("Example: add_toc_to_chapter.py 2")
        sys.exit(1)

    chapter_num = sys.argv[1].zfill(2)

    # Paths
    repo_root = Path(__file__).parent.parent.parent
    input_file = repo_root / "output" / "chapters" / "02_removedbullets" / f"chapter_{chapter_num}.md"

    if not input_file.exists():
        print(f"Error: Chapter file not found: {input_file}")
        sys.exit(1)

    print(f"Adding Table of Contents to Chapter {chapter_num}")
    print("=" * 60)
    print()

    # Read chapter
    print(f"Reading: {input_file}")
    content = input_file.read_text(encoding='utf-8')

    # Check if TOC already exists
    if has_toc(content):
        print("  ⚠️  Chapter already has a table of contents")
        print()
        response = input("Overwrite existing TOC? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            sys.exit(0)
        # Remove existing TOC
        content = re.sub(r'^##\s+Table of Contents\n.*?^---\n', '', content, flags=re.MULTILINE | re.DOTALL)

    # Add TOC
    print("Generating table of contents...")
    content_with_toc = add_toc_to_chapter(content)

    # Count headings
    headings = extract_headings(content)
    print(f"  Generated TOC with {len(headings)} entries")

    # Write output (back to same file)
    print(f"Writing: {input_file}")
    input_file.write_text(content_with_toc, encoding='utf-8')

    print()
    print("=" * 60)
    print("TOC Added Successfully!")
    print()
    print(f"Chapter: {input_file}")
    print(f"TOC entries: {len(headings)}")


if __name__ == "__main__":
    main()
