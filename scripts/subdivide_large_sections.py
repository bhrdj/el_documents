#!/usr/bin/env python3
"""
Subdivide sections 2 and 6 which are too large.
"""

import re
from pathlib import Path


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def subdivide_section(content: str, section_num: int, target_words: int = 1500):
    """
    Subdivide a section into smaller chunks based on level 4 and 5 headings.
    """
    # Find all headings (level 4 and deeper)
    heading_pattern = re.compile(r'^(#{4,6})\s+(.+)$', re.MULTILINE)
    matches = list(heading_pattern.finditer(content))

    if not matches:
        # No subheadings, split by word count
        words = content.split()
        chunks = []
        for i in range(0, len(words), target_words):
            chunk = ' '.join(words[i:i + target_words])
            chunks.append(chunk)
        return chunks

    # Split by headings
    subsections = []
    current_content = content[:matches[0].start()]  # Preamble
    current_start = 0

    for i, match in enumerate(matches):
        level = len(match.group(1))
        heading = match.group(2).strip()
        start_pos = match.start()

        # Get content until next heading
        if i < len(matches) - 1:
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(content)

        section_text = content[start_pos:end_pos]
        section_words = count_words(section_text)

        # Check if we should save current subsection
        current_words = count_words(current_content)

        if current_words + section_words > target_words * 1.2 and current_words > target_words * 0.5:
            # Save current subsection
            if current_content.strip():
                subsections.append(current_content)
            current_content = section_text
        else:
            # Add to current subsection
            current_content += section_text

    # Add final subsection
    if current_content.strip():
        subsections.append(current_content)

    return subsections


def main():
    """Main execution."""
    sections_dir = Path("/home/steven/git/el_documents/output/chapters/05_repaired/sections")

    # Read sections that need subdivision
    section_2 = (sections_dir / "section_02.md").read_text()
    section_6 = (sections_dir / "section_06.md").read_text()

    print("Subdividing large sections...")
    print(f"Section 2: {count_words(section_2):,} words")
    print(f"Section 6: {count_words(section_6):,} words")
    print()

    # Subdivide section 2
    sub2 = subdivide_section(section_2, 2, target_words=1500)
    print(f"Section 2 split into {len(sub2)} subsections:")
    for i, sub in enumerate(sub2, 1):
        print(f"  2.{i}: {count_words(sub):,} words")

    # Subdivide section 6
    sub6 = subdivide_section(section_6, 6, target_words=1500)
    print(f"\nSection 6 split into {len(sub6)} subsections:")
    for i, sub in enumerate(sub6, 1):
        print(f"  6.{i}: {count_words(sub):,} words")

    # Now rebuild the complete section list
    final_sections = []

    # Section 1
    final_sections.append((sections_dir / "section_01.md").read_text())

    # Section 2 subdivisions
    for sub in sub2:
        final_sections.append(sub)

    # Sections 3, 4, 5
    final_sections.append((sections_dir / "section_03.md").read_text())
    final_sections.append((sections_dir / "section_04.md").read_text())
    final_sections.append((sections_dir / "section_05.md").read_text())

    # Section 6 subdivisions
    for sub in sub6:
        final_sections.append(sub)

    # Save final sections
    final_dir = sections_dir / "final"
    final_dir.mkdir(exist_ok=True)

    print(f"\n{'='*80}")
    print(f"Final section breakdown ({len(final_sections)} sections):")
    print(f"{'='*80}\n")

    total_words = 0
    for i, section in enumerate(final_sections, 1):
        words = count_words(section)
        total_words += words
        pct = (words / 18269) * 100  # Total useful content words
        section_file = final_dir / f"section_{i:02d}.md"
        section_file.write_text(section)
        print(f"Section {i:02d}: {words:,} words ({pct:.1f}%) -> {section_file.name}")

    print(f"\nTotal: {total_words:,} words")
    print(f"\nAll sections saved to: {final_dir}")


if __name__ == "__main__":
    main()
