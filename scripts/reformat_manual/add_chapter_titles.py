#!/usr/bin/env python3
"""
Add H1 chapter titles to chapters that are missing them.

Based on the first H2 section or chapter number.
"""

import re
from pathlib import Path
from typing import Optional


CHAPTER_TITLES = {
    '00': 'CHAPTER 0: FRONT MATTER',
    '01': 'CHAPTER 1: CHILD ADMISSION',
    '04': 'CHAPTER 4: CHILD INTERACTION STRATEGIES',
    '07': 'CHAPTER 7: STAFF STAYING IN DAYCARE',
}


def detect_chapter_number(filename: str) -> Optional[str]:
    """Extract chapter number from filename."""
    match = re.match(r'chapter_(\d+)', filename)
    if match:
        return match.group(1)
    return None


def has_h1_title(content: str) -> bool:
    """Check if content already has an H1 title."""
    return bool(re.match(r'^#\s+', content, re.MULTILINE))


def add_h1_title(content: str, title: str) -> str:
    """Add H1 title at the beginning of content."""
    # Add title at the very beginning
    return f"# {title}\n\n{content}"


def main():
    """Main process to add H1 titles."""
    repo_root = Path(__file__).parent.parent.parent
    chapters_dir = repo_root / "output" / "chapters" / "02_removedbullets"

    print("Adding H1 Chapter Titles")
    print("=" * 60)
    print()

    chapters_to_fix = ['00', '01', '04', '07']

    for chapter_num in chapters_to_fix:
        chapter_file = chapters_dir / f"chapter_{chapter_num}.md"

        if not chapter_file.exists():
            print(f"⚠️  Chapter {chapter_num}: File not found")
            continue

        print(f"Processing Chapter {chapter_num}...")

        # Read content
        content = chapter_file.read_text(encoding='utf-8')

        # Check if already has H1
        if has_h1_title(content):
            print(f"  ✓ Already has H1 title, skipping")
            continue

        # Get title
        if chapter_num in CHAPTER_TITLES:
            title = CHAPTER_TITLES[chapter_num]
        else:
            print(f"  ⚠️  No title defined for chapter {chapter_num}")
            continue

        # Add title
        new_content = add_h1_title(content, title)

        # Write back
        chapter_file.write_text(new_content, encoding='utf-8')
        print(f"  ✓ Added H1 title: {title}")

    print()
    print("=" * 60)
    print("H1 Titles Added Successfully!")


if __name__ == "__main__":
    main()
