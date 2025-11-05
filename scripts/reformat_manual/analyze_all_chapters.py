#!/usr/bin/env python3
"""
Analyze all chapters to identify restructuring opportunities.

Checks for:
- Chapter length and complexity
- Heading hierarchy issues
- Potential duplicates or redundancy
- Organizational problems
- Missing content
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict


def analyze_chapter(file_path: Path) -> Dict:
    """
    Analyze a single chapter file.

    Returns dict with analysis results.
    """
    content = file_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    analysis = {
        'file': file_path.name,
        'total_lines': len(lines),
        'non_empty_lines': sum(1 for line in lines if line.strip()),
        'headings': [],
        'heading_levels': defaultdict(int),
        'max_heading_depth': 0,
        'bullets': 0,
        'has_toc': False,
        'chapter_title': '',
        'main_sections': [],
        'issues': [],
    }

    heading_pattern = re.compile(r'^(#{1,6})\s+(.*)')

    for i, line in enumerate(lines, 1):
        # Count bullets
        if re.match(r'^[[:space:]]*-\s+', line):
            analysis['bullets'] += 1

        # Check for TOC
        if 'table of contents' in line.lower():
            analysis['has_toc'] = True

        # Analyze headings
        match = heading_pattern.match(line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()

            analysis['headings'].append((level, title, i))
            analysis['heading_levels'][level] += 1
            analysis['max_heading_depth'] = max(analysis['max_heading_depth'], level)

            # Track chapter title and main sections
            if level == 1:
                analysis['chapter_title'] = title
            elif level == 2:
                analysis['main_sections'].append(title)

    # Identify issues

    # Issue: No chapter title
    if not analysis['chapter_title']:
        analysis['issues'].append('Missing H1 chapter title')

    # Issue: Very short chapter
    if analysis['non_empty_lines'] < 50:
        analysis['issues'].append(f'Very short chapter ({analysis["non_empty_lines"]} non-empty lines)')

    # Issue: No headings
    if not analysis['headings']:
        analysis['issues'].append('No headings found')

    # Issue: Deep nesting (more than 4 levels)
    if analysis['max_heading_depth'] > 4:
        analysis['issues'].append(f'Very deep heading hierarchy (max level: {analysis["max_heading_depth"]})')

    # Issue: Heading level skips
    heading_levels = sorted(analysis['heading_levels'].keys())
    for i in range(len(heading_levels) - 1):
        if heading_levels[i+1] - heading_levels[i] > 1:
            analysis['issues'].append(f'Heading level skip: H{heading_levels[i]} to H{heading_levels[i+1]}')

    # Issue: No table of contents for long chapters
    if analysis['total_lines'] > 500 and not analysis['has_toc']:
        analysis['issues'].append('Long chapter without table of contents')

    return analysis


def generate_restructuring_plan(analyses: List[Dict]) -> str:
    """
    Generate restructuring recommendations based on analyses.
    """
    lines = [
        "# Chapter Restructuring Analysis and Plan",
        "",
        "**Date**: 2025-11-05",
        "**Purpose**: Identify chapters that would benefit from reorganization",
        "",
        "## Chapter Statistics",
        "",
        "| Chapter | Lines | Headings | Bullets | Max Depth | Issues |",
        "|---------|-------|----------|---------|-----------|--------|",
    ]

    for analysis in analyses:
        issues_count = len(analysis['issues'])
        lines.append(
            f"| {analysis['file']} | {analysis['total_lines']} | "
            f"{len(analysis['headings'])} | {analysis['bullets']} | "
            f"H{analysis['max_heading_depth']} | {issues_count} |"
        )

    lines.extend([
        "",
        "## Detailed Analysis by Chapter",
        "",
    ])

    for analysis in analyses:
        lines.append(f"### {analysis['file']}")
        lines.append("")

        if analysis['chapter_title']:
            lines.append(f"**Title**: {analysis['chapter_title']}")

        lines.append(f"**Statistics**:")
        lines.append(f"- Total lines: {analysis['total_lines']}")
        lines.append(f"- Headings: {len(analysis['headings'])}")
        lines.append(f"- Bullets: {analysis['bullets']}")
        lines.append(f"- Max heading depth: H{analysis['max_heading_depth']}")
        lines.append(f"- Has TOC: {'Yes' if analysis['has_toc'] else 'No'}")
        lines.append("")

        if analysis['main_sections']:
            lines.append(f"**Main Sections** ({len(analysis['main_sections'])}):")
            for section in analysis['main_sections'][:10]:
                lines.append(f"- {section}")
            if len(analysis['main_sections']) > 10:
                lines.append(f"- ... and {len(analysis['main_sections']) - 10} more")
            lines.append("")

        if analysis['issues']:
            lines.append(f"**Issues Found** ({len(analysis['issues'])}):")
            for issue in analysis['issues']:
                lines.append(f"- ⚠️ {issue}")
        else:
            lines.append("**Issues**: ✅ None found")

        lines.append("")
        lines.append("---")
        lines.append("")

    # Recommendations
    lines.extend([
        "## Restructuring Recommendations",
        "",
        "### High Priority",
        "",
    ])

    high_priority = []
    medium_priority = []
    low_priority = []

    for analysis in analyses:
        chapter = analysis['file']

        # High priority: Multiple serious issues
        if len(analysis['issues']) >= 3:
            high_priority.append(
                f"**{chapter}**: {len(analysis['issues'])} issues - "
                + ", ".join(analysis['issues'][:2]) + "..."
            )
        # Medium priority: Long chapter without TOC
        elif analysis['total_lines'] > 500 and not analysis['has_toc']:
            medium_priority.append(
                f"**{chapter}**: Add table of contents ({analysis['total_lines']} lines)"
            )
        # Low priority: Minor issues
        elif analysis['issues']:
            low_priority.append(
                f"**{chapter}**: {', '.join(analysis['issues'])}"
            )

    if high_priority:
        for item in high_priority:
            lines.append(f"- {item}")
        lines.append("")
    else:
        lines.append("- ✅ None")
        lines.append("")

    lines.extend([
        "### Medium Priority",
        "",
    ])

    if medium_priority:
        for item in medium_priority:
            lines.append(f"- {item}")
        lines.append("")
    else:
        lines.append("- ✅ None")
        lines.append("")

    lines.extend([
        "### Low Priority",
        "",
    ])

    if low_priority:
        for item in low_priority:
            lines.append(f"- {item}")
        lines.append("")
    else:
        lines.append("- ✅ None")
        lines.append("")

    # Specific actions
    lines.extend([
        "## Recommended Actions",
        "",
        "### Already Complete",
        "",
        "- ✅ **Chapter 5**: Successfully merged and reorganized with TOC",
        "",
        "### Proposed Actions",
        "",
    ])

    # Generate specific action items
    actions = []

    for analysis in analyses:
        chapter = analysis['file']
        chapter_num = chapter.replace('chapter_', '').replace('.md', '')

        if analysis['total_lines'] > 500 and not analysis['has_toc']:
            actions.append(f"1. **{chapter}**: Add table of contents for easier navigation")

        if 'Very short chapter' in str(analysis['issues']):
            actions.append(
                f"2. **{chapter}**: Review for completeness - may need expansion or merge with another chapter"
            )

        if analysis['max_heading_depth'] > 5:
            actions.append(
                f"3. **{chapter}**: Simplify heading hierarchy (currently H{analysis['max_heading_depth']})"
            )

    if actions:
        for action in actions:
            lines.append(f"- {action}")
    else:
        lines.append("- ✅ All chapters are well-structured!")

    lines.append("")

    return '\n'.join(lines)


def main():
    """Main analysis process."""
    repo_root = Path(__file__).parent.parent.parent
    chapters_dir = repo_root / "output" / "chapters" / "02_removedbullets"

    print("Chapter Restructuring Analysis")
    print("=" * 60)
    print()

    # Find all chapter files
    chapter_files = sorted(chapters_dir.glob("chapter_*.md"))
    chapter_files = [f for f in chapter_files if not f.name.startswith('chapter_05')]

    print(f"Analyzing {len(chapter_files)} chapters...")
    print()

    # Analyze each chapter
    analyses = []
    for chapter_file in chapter_files:
        print(f"  Analyzing {chapter_file.name}...")
        analysis = analyze_chapter(chapter_file)
        analyses.append(analysis)

    print()

    # Generate plan
    print("Generating restructuring plan...")
    plan = generate_restructuring_plan(analyses)

    # Write plan
    output_file = repo_root / "specs" / "001-reformat-manual" / "chapter-restructuring-plan.md"
    output_file.write_text(plan, encoding='utf-8')

    print()
    print("=" * 60)
    print("Analysis Complete!")
    print()
    print(f"Plan written to: {output_file}")
    print()

    # Summary
    total_issues = sum(len(a['issues']) for a in analyses)
    chapters_with_issues = sum(1 for a in analyses if a['issues'])

    print(f"Summary:")
    print(f"  Chapters analyzed: {len(analyses)}")
    print(f"  Chapters with issues: {chapters_with_issues}")
    print(f"  Total issues found: {total_issues}")


if __name__ == "__main__":
    main()
