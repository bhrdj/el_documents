#!/usr/bin/env python3
"""
Phase 1: Extract section hierarchy from markdown files.

Usage:
    .venv/bin/python scripts/04_analysis/01_extract_sections.py <input_file> [output_file]

Example:
    .venv/bin/python scripts/04_analysis/01_extract_sections.py \
        output/chapters/04_merged/chapter_05_deduplicated.md \
        output/chapters/04_merged/chapter_05_sections.yaml
"""

import sys
import os
from pathlib import Path
import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.markdown_parser import MarkdownParser


def assess_completeness(section) -> str:
    """Assess section completeness based on content patterns."""
    content = section.content.strip()

    # Check for orphaned heading (no content)
    lines = content.split('\n')
    non_heading_lines = [l for l in lines if not l.strip().startswith('#')]
    content_text = '\n'.join(non_heading_lines).strip()

    if len(content_text) < 50:
        return "orphaned"

    # Check for incomplete markers
    incomplete_markers = [
        "TODO", "[incomplete]", "[pending]", "...",
        "to be continued", "see below"
    ]

    if any(marker.lower() in content.lower() for marker in incomplete_markers):
        return "partial"

    # Check if section ends abruptly (no punctuation)
    if content_text and not content_text[-1] in '.!?':
        return "partial"

    return "complete"


def extract_age_groups(content: str) -> list:
    """Extract mentioned age groups from content."""
    age_patterns = [
        "infant", "toddler", "preschool", "school-age",
        "0-18 months", "18-36 months", "3-5 years", "5-12 years",
        "babies", "young children", "older children"
    ]

    found = []
    content_lower = content.lower()

    for pattern in age_patterns:
        if pattern in content_lower:
            found.append(pattern)

    return list(set(found))


def classify_content_type(heading: str, content: str) -> list:
    """Classify content type based on heading and content."""
    types = []

    # Keyword patterns
    activity_keywords = ["activity", "activities", "game", "exercise"]
    example_keywords = ["example", "examples", "sample"]
    theory_keywords = ["introduction", "overview", "theory", "concept", "principle"]
    guideline_keywords = ["guideline", "tip", "recommendation", "best practice"]

    heading_lower = heading.lower()
    content_lower = content.lower()

    if any(kw in heading_lower for kw in activity_keywords):
        types.append("activities")

    if any(kw in heading_lower for kw in example_keywords):
        types.append("examples")

    if any(kw in heading_lower for kw in theory_keywords):
        types.append("theory")

    if any(kw in heading_lower for kw in guideline_keywords):
        types.append("guidelines")

    # Content-based detection
    if "step" in content_lower or "procedure" in content_lower:
        types.append("procedures")

    if not types:
        types.append("general")

    return list(set(types))


def extract_sections(input_file: str, output_file: str = None):
    """Extract sections from markdown file and save to YAML."""

    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)

    # Parse markdown
    print(f"Parsing: {input_file}")
    parser = MarkdownParser(input_file)
    sections = parser.parse()

    print(f"Found {len(sections)} sections")

    # Convert to structured format
    section_data = []

    for section in sections:
        data = {
            'section_id': section.id,
            'heading': section.heading,
            'level': section.level,
            'line_range': [section.line_start, section.line_end],
            'line_count': section.line_count,
            'token_estimate': section.token_estimate,
            'parent_id': section.parent_id,
            'subsections': section.subsections,
            'age_groups_mentioned': extract_age_groups(section.content),
            'content_type': classify_content_type(section.heading, section.content),
            'completeness': assess_completeness(section),
        }

        section_data.append(data)

    # Generate output filename if not provided
    if not output_file:
        input_path = Path(input_file)
        output_file = str(input_path.parent / f"{input_path.stem}_sections.yaml")

    # Save to YAML
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump({
            'source_file': input_file,
            'total_sections': len(sections),
            'sections': section_data
        }, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"Saved section data to: {output_file}")

    # Print summary statistics
    print("\n--- Summary Statistics ---")
    print(f"Total sections: {len(sections)}")

    by_level = {}
    for section in section_data:
        level = section['level']
        by_level[level] = by_level.get(level, 0) + 1

    print("\nSections by level:")
    for level in sorted(by_level.keys()):
        print(f"  Level {level} ({'#' * level}): {by_level[level]}")

    # Completeness summary
    completeness_counts = {}
    for section in section_data:
        comp = section['completeness']
        completeness_counts[comp] = completeness_counts.get(comp, 0) + 1

    print("\nCompleteness status:")
    for status, count in sorted(completeness_counts.items()):
        print(f"  {status}: {count}")

    # Major sections (level 2)
    major_sections = [s for s in section_data if s['level'] == 2]
    print(f"\nMajor sections (##): {len(major_sections)}")
    for s in major_sections[:10]:  # Show first 10
        print(f"  {s['section_id']}: {s['heading']} ({s['line_count']} lines)")

    if len(major_sections) > 10:
        print(f"  ... and {len(major_sections) - 10} more")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    extract_sections(input_file, output_file)
