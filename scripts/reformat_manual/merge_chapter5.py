#!/usr/bin/env python3
"""
Intelligent merge of Chapter 5 parts 1 and 2.

Strategy:
- Use Part 1 as primary structure (more recent, more detailed)
- Enrich sparse sections with Part 2's explanatory content
- Remove duplicates (Part 1 takes precedence)
- Clean up structure and organization

Usage:
    .venv/bin/python scripts/reformat_manual/merge_chapter5.py
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Section:
    """Represents a section with heading and content."""
    heading: str
    level: int
    number: str
    title: str
    content: List[str]

    @property
    def is_sparse(self) -> bool:
        """Check if section has minimal content (just heading, no real content)."""
        # Count non-empty, non-heading lines
        content_lines = [
            line for line in self.content
            if line.strip() and not line.strip().startswith('#')
        ]
        return len(content_lines) < 3  # Less than 3 lines of actual content


def parse_markdown_sections(content: str) -> List[Section]:
    """
    Parse markdown into structured sections.

    Returns list of Section objects with heading hierarchy.
    """
    lines = content.split('\n')
    sections = []
    current_section = None

    heading_pattern = re.compile(r'^(#{1,6})\s+(.*)')

    for line in lines:
        match = heading_pattern.match(line)

        if match:
            # Save previous section if exists
            if current_section:
                sections.append(current_section)

            # Parse new section
            level = len(match.group(1))
            full_title = match.group(2).strip()

            # Extract section number and title
            number_match = re.match(r'^(\d+(?:\.\d+)*)\s*(.*)', full_title)
            if number_match:
                number = number_match.group(1)
                title = number_match.group(2).strip()
            else:
                number = ""
                title = full_title

            current_section = Section(
                heading=line,
                level=level,
                number=number,
                title=title,
                content=[]
            )
        elif current_section:
            current_section.content.append(line)

    # Add last section
    if current_section:
        sections.append(current_section)

    return sections


def build_section_map(sections: List[Section]) -> Dict[str, Section]:
    """
    Build a map of section number to Section object.
    """
    section_map = {}
    for section in sections:
        if section.number:
            section_map[section.number] = section
    return section_map


def merge_sections(part1_sections: List[Section], part2_sections: List[Section]) -> List[Section]:
    """
    Intelligently merge sections from both parts.

    Strategy:
    - Use Part 1 structure as base
    - For sparse sections in Part 1, check Part 2 for content
    - If Part 2 has richer content, use it
    - Always prefer Part 1 if both have substantial content
    """
    part2_map = build_section_map(part2_sections)
    merged = []

    for section in part1_sections:
        if section.number and section.is_sparse:
            # Part 1 section is sparse, check Part 2
            if section.number in part2_map:
                part2_section = part2_map[section.number]
                if not part2_section.is_sparse:
                    # Part 2 has better content, use it
                    print(f"  Enriching {section.number} with Part 2 content")
                    merged.append(part2_section)
                    continue

        # Use Part 1 section (default)
        merged.append(section)

    return merged


def reconstruct_markdown(sections: List[Section]) -> str:
    """
    Reconstruct markdown from sections.
    """
    lines = []

    for section in sections:
        # Add heading
        lines.append(section.heading)

        # Add content
        lines.extend(section.content)

    return '\n'.join(lines)


def clean_structure(content: str) -> str:
    """
    Clean up structural issues in the merged content.

    - Remove excessive blank lines
    - Ensure consistent spacing around headings
    - Fix any obvious formatting issues
    """
    lines = content.split('\n')
    cleaned = []
    prev_blank = False

    for i, line in enumerate(lines):
        is_blank = not line.strip()
        is_heading = line.strip().startswith('#')

        # Skip excessive blank lines (more than 2 consecutive)
        if is_blank:
            if prev_blank:
                # Skip if we already have a blank line
                continue
            prev_blank = True
        else:
            prev_blank = False

        cleaned.append(line)

    return '\n'.join(cleaned)


def add_chapter_header(content: str) -> str:
    """
    Add a professional chapter header with overview.
    """
    header = """# CHAPTER 5: STRUCTURED ENRICHMENT

**Purpose**: This chapter provides comprehensive guidance on structured enrichment activities for children aged 6-36 months in EL daycares.

**Key Activity Types**:
- Big-Group Activities: Mixed-age group activities for social development
- Small-Group Activities: Focused pre-school preparation sessions
- Free-Choice Activities: Child-led exploration and play
- One-on-One Sessions: Individual attention and skill building

**Note**: This chapter has been professionally reorganized from the original source material to improve clarity and reduce redundancy.

---

"""

    # Remove old chapter heading if exists
    content_lines = content.split('\n')
    if content_lines[0].startswith('CHAPTER 5'):
        content_lines = content_lines[1:]

    return header + '\n'.join(content_lines)


def generate_merge_report(part1_sections: List[Section], part2_sections: List[Section],
                         merged_sections: List[Section]) -> str:
    """
    Generate a report documenting the merge process.
    """
    report_lines = [
        "# Chapter 5 Merge Report",
        "",
        f"**Date**: 2025-11-05",
        "",
        "## Summary",
        "",
        f"- Part 1 sections: {len(part1_sections)}",
        f"- Part 2 sections: {len(part2_sections)}",
        f"- Merged sections: {len(merged_sections)}",
        "",
        "## Merge Strategy",
        "",
        "1. Used Part 1 as primary structure (more recent)",
        "2. Identified sparse sections in Part 1 (< 3 lines of content)",
        "3. Enriched sparse sections with Part 2's explanatory content where available",
        "4. Removed duplicates (Part 1 takes precedence)",
        "5. Cleaned structure and formatting",
        "",
        "## Sections Enriched from Part 2",
        "",
    ]

    # Track which sections were enriched
    enriched_count = 0
    part2_map = build_section_map(part2_sections)

    for i, section in enumerate(part1_sections):
        if section.number and section.is_sparse:
            if section.number in part2_map:
                part2_section = part2_map[section.number]
                if not part2_section.is_sparse:
                    enriched_count += 1
                    report_lines.append(f"- {section.number} {section.title}")

    report_lines.extend([
        "",
        f"**Total sections enriched**: {enriched_count}",
        "",
        "## Statistics",
        "",
    ])

    # Count content
    total_headings = len(merged_sections)
    sparse_sections = sum(1 for s in merged_sections if s.is_sparse)

    report_lines.extend([
        f"- Total headings: {total_headings}",
        f"- Sections with substantial content: {total_headings - sparse_sections}",
        f"- Sections still sparse: {sparse_sections}",
        "",
    ])

    return '\n'.join(report_lines)


def main():
    """Main merge process."""
    # Paths
    repo_root = Path(__file__).parent.parent.parent
    part1_file = repo_root / "output" / "chapters" / "02_removedbullets" / "chapter_05_part1.md"
    part2_file = repo_root / "output" / "chapters" / "02_removedbullets" / "chapter_05_part2.md"
    output_dir = repo_root / "output" / "chapters" / "03_merged"
    output_file = output_dir / "chapter_05.md"
    report_file = output_dir / "CHAPTER_5_MERGE_REPORT.md"

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Chapter 5 Intelligent Merge")
    print("=" * 60)
    print()

    # Read both parts
    print("Reading source files...")
    part1_content = part1_file.read_text(encoding='utf-8')
    part2_content = part2_file.read_text(encoding='utf-8')

    # Parse into sections
    print("Parsing Part 1 sections...")
    part1_sections = parse_markdown_sections(part1_content)
    print(f"  Found {len(part1_sections)} sections")

    print("Parsing Part 2 sections...")
    part2_sections = parse_markdown_sections(part2_content)
    print(f"  Found {len(part2_sections)} sections")
    print()

    # Identify sparse sections
    part1_sparse = sum(1 for s in part1_sections if s.is_sparse)
    print(f"Part 1 sparse sections: {part1_sparse}")
    print()

    # Merge
    print("Merging sections...")
    merged_sections = merge_sections(part1_sections, part2_sections)
    print(f"  Created {len(merged_sections)} merged sections")
    print()

    # Reconstruct markdown
    print("Reconstructing markdown...")
    merged_content = reconstruct_markdown(merged_sections)

    # Clean structure
    print("Cleaning structure...")
    merged_content = clean_structure(merged_content)

    # Add professional header
    print("Adding chapter header...")
    merged_content = add_chapter_header(merged_content)

    # Write output
    print(f"Writing merged chapter to: {output_file}")
    output_file.write_text(merged_content, encoding='utf-8')

    # Generate report
    print(f"Generating merge report: {report_file}")
    report = generate_merge_report(part1_sections, part2_sections, merged_sections)
    report_file.write_text(report, encoding='utf-8')

    # Summary
    print()
    print("=" * 60)
    print("Merge Complete!")
    print()
    print(f"Output: {output_file}")
    print(f"Report: {report_file}")
    print()

    # Statistics
    merged_sparse = sum(1 for s in merged_sections if s.is_sparse)
    print(f"Final chapter statistics:")
    print(f"  Total sections: {len(merged_sections)}")
    print(f"  Sections with content: {len(merged_sections) - merged_sparse}")
    print(f"  Sections still sparse: {merged_sparse}")


if __name__ == "__main__":
    main()
