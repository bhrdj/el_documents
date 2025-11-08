#!/usr/bin/env python3
"""
Finalize section division by recursively subdividing any section > 1,644 words.
"""

import re
from pathlib import Path
from typing import List


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def split_by_headings(content: str, max_words: int = 1644, depth: int = 0) -> List[str]:
    """
    Split content by headings, ensuring no section exceeds max_words.
    """
    # Prevent infinite recursion
    if depth > 5:
        # Force split by word count
        words = content.split()
        sections = []
        for i in range(0, len(words), max_words):
            chunk = ' '.join(words[i:i + max_words])
            sections.append(chunk)
        return sections

    # Find all headings at any level
    heading_pattern = re.compile(r'^(#{3,6})\s+(.+)$', re.MULTILINE)
    matches = list(heading_pattern.finditer(content))

    if not matches or len(matches) < 2:
        # No headings or too few, split by word count
        words = content.split()
        if len(words) <= max_words:
            return [content]

        sections = []
        for i in range(0, len(words), max_words):
            chunk = ' '.join(words[i:i + max_words])
            sections.append(chunk)
        return sections

    # Split by headings
    sections = []
    current_content = content[:matches[0].start()]  # Preamble

    for i, match in enumerate(matches):
        start_pos = match.start()

        # Get content until next heading
        if i < len(matches) - 1:
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(content)

        section_text = content[start_pos:end_pos]
        section_words = count_words(section_text)

        # Check if adding this would exceed limit
        current_words = count_words(current_content)

        if current_words + section_words > max_words and current_content.strip():
            # Save current and start new
            sections.append(current_content)
            current_content = section_text
        else:
            # Add to current
            current_content += section_text

    # Add final section
    if current_content.strip():
        sections.append(current_content)

    # Recursively split any section that's still too large
    final_sections = []
    for section in sections:
        if count_words(section) > max_words:
            # Need to split further
            subsections = split_by_headings(section, max_words, depth + 1)
            final_sections.extend(subsections)
        else:
            final_sections.append(section)

    return final_sections


def main():
    """Main execution."""
    sections_dir = Path("/home/steven/git/el_documents/output/chapters/05_repaired/sections/final")

    # Read all current sections
    section_files = sorted(sections_dir.glob("section_*.md"))
    all_sections = []

    print("Reading current sections...")
    for f in section_files:
        content = f.read_text()
        words = count_words(content)
        print(f"  {f.name}: {words:,} words")

        if words > 1644:
            print(f"    -> Too large, subdividing...")
            subsections = split_by_headings(content, max_words=1644)
            print(f"    -> Split into {len(subsections)} parts")
            for j, sub in enumerate(subsections, 1):
                print(f"       Part {j}: {count_words(sub):,} words")
            all_sections.extend(subsections)
        else:
            all_sections.append(content)

    # Save final sections
    output_dir = sections_dir.parent / "reorganize_input"
    output_dir.mkdir(exist_ok=True)

    print(f"\n{'='*80}")
    print(f"Final section breakdown ({len(all_sections)} sections):")
    print(f"{'='*80}\n")

    total_words = 0
    for i, section in enumerate(all_sections, 1):
        words = count_words(section)
        total_words += words
        pct = (words / 18269) * 100  # Total useful content
        section_file = output_dir / f"section_{i:02d}.md"
        section_file.write_text(section)

        status = "✓" if 913 <= words <= 1644 else ("!" if words > 1644 else "~")
        print(f"{status} Section {i:02d}: {words:,} words ({pct:.1f}%)")

    print(f"\nTotal: {total_words:,} words")
    print(f"Sections in target range (913-1,644): {sum(1 for s in all_sections if 913 <= count_words(s) <= 1644)}/{len(all_sections)}")
    print(f"\nAll sections saved to: {output_dir}")


if __name__ == "__main__":
    main()
