#!/usr/bin/env python3
"""
Divide Chapter 5 into logical sections of 5-9% word count each.
Excludes the "Restored Content" section which is redundant.
"""

import re
from pathlib import Path
from typing import List, Tuple, Dict


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def main():
    """Main execution."""
    file_path = Path("/home/steven/git/el_documents/output/chapters/05_repaired/ch05_v01.md")
    content = file_path.read_text()

    # Find and exclude the "Restored Content" section
    restored_match = re.search(r'^## 1\.7 Restored Content', content, re.MULTILINE)

    if restored_match:
        useful_content = content[:restored_match.start()].strip()
        restored_content = content[restored_match.start():]
        print(f"Found 'Restored Content' section at position {restored_match.start():,}")
        print(f"Restored Content word count: {count_words(restored_content):,}")
    else:
        useful_content = content
        print("No 'Restored Content' section found")

    total_words = count_words(useful_content)
    print(f"\nUseful content word count: {total_words:,}")

    # Calculate target section sizes
    min_words = int(total_words * 0.05)
    max_words = int(total_words * 0.09)

    print(f"Target section size: {min_words:,} - {max_words:,} words (5-9%)")
    print(f"Expected number of sections: {total_words // max_words} - {total_words // min_words}")

    # Find all level 2 and 3 headings (## and ###)
    heading_pattern = re.compile(r'^(#{2,3})\s+(.+)$', re.MULTILINE)
    matches = list(heading_pattern.finditer(useful_content))

    print(f"\nFound {len(matches)} potential section boundaries\n")

    # Create sections by grouping headings
    sections = []
    current_section_content = ""
    current_section_start = 0
    current_section_headings = []

    for i, match in enumerate(matches):
        level = len(match.group(1))
        heading = match.group(2).strip()
        start_pos = match.start()

        # Determine content for this heading
        if i < len(matches) - 1:
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(useful_content)

        section_text = useful_content[start_pos:end_pos]
        section_words = count_words(section_text)

        # Should we start a new section?
        current_words = count_words(current_section_content)

        if current_words == 0:
            # First section
            current_section_start = start_pos
            current_section_content = section_text
            current_section_headings = [(level, heading, section_words)]

        elif current_words + section_words > max_words:
            # Current section is full enough, save it
            if current_words >= min_words:
                sections.append({
                    'number': len(sections) + 1,
                    'start': current_section_start,
                    'end': start_pos,
                    'content': current_section_content,
                    'words': current_words,
                    'headings': current_section_headings
                })

            # Start new section
            current_section_start = start_pos
            current_section_content = section_text
            current_section_headings = [(level, heading, section_words)]

        else:
            # Add to current section
            current_section_content += section_text
            current_section_headings.append((level, heading, section_words))

    # Add final section
    if current_section_content:
        current_words = count_words(current_section_content)
        if current_words >= min_words:
            sections.append({
                'number': len(sections) + 1,
                'start': current_section_start,
                'end': len(useful_content),
                'content': current_section_content,
                'words': current_words,
                'headings': current_section_headings
            })

    # Print results
    print(f"{'='*80}")
    print(f"Created {len(sections)} sections")
    print(f"{'='*80}\n")

    for sec in sections:
        pct = (sec['words'] / total_words) * 100
        print(f"Section {sec['number']}: {sec['words']:,} words ({pct:.1f}%)")
        print(f"  Character range: {sec['start']:,} - {sec['end']:,}")
        print(f"  Main topics:")
        for i, (level, heading, words) in enumerate(sec['headings'][:5]):
            indent = "    " if level == 3 else "  "
            print(f"{indent}- {heading} ({words:,} words)")
        if len(sec['headings']) > 5:
            print(f"    ... and {len(sec['headings']) - 5} more topics")
        print()

    # Save sections to disk
    output_dir = Path("/home/steven/git/el_documents/output/chapters/05_repaired/sections")
    output_dir.mkdir(exist_ok=True)

    for sec in sections:
        section_file = output_dir / f"section_{sec['number']:02d}.md"
        section_file.write_text(sec['content'])
        print(f"Saved: {section_file}")

    # Save section map
    map_file = output_dir / "section_map.txt"
    with map_file.open('w') as f:
        f.write(f"Chapter 5 Section Division Map\n")
        f.write(f"{'='*80}\n\n")
        f.write(f"Total useful content: {total_words:,} words\n")
        f.write(f"Target per section: {min_words:,} - {max_words:,} words (5-9%)\n")
        f.write(f"Number of sections: {len(sections)}\n\n")

        for sec in sections:
            pct = (sec['words'] / total_words) * 100
            f.write(f"\n{'='*80}\n")
            f.write(f"SECTION {sec['number']}: {sec['words']:,} words ({pct:.1f}%)\n")
            f.write(f"{'='*80}\n")
            f.write(f"Character range: {sec['start']:,} - {sec['end']:,}\n")
            f.write(f"File: section_{sec['number']:02d}.md\n\n")
            f.write(f"Topics:\n")
            for level, heading, words in sec['headings']:
                indent = "  " * (level - 2)
                f.write(f"{indent}{'#'*level} {heading} ({words:,} words)\n")

    print(f"\nSection map saved to: {map_file}")

    print(f"\n{'='*80}")
    print("Section division complete!")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
