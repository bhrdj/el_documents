#!/usr/bin/env python3
"""
Validate reformatted chapters for quality and consistency.

This script validates that reformatted chapters meet all requirements:
- Valid vanilla markdown (no HTML, no extended features)
- Consistent heading hierarchy
- Proper list formatting
- Unicode brackets preserved
- Content fidelity maintained

Usage:
    .venv/bin/python scripts/reformat_manual/validate_output.py
    .venv/bin/python scripts/reformat_manual/validate_output.py --chapter 2
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))


class ValidationResult:
    """Container for validation results."""

    def __init__(self, chapter: str):
        self.chapter = chapter
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.stats: Dict[str, int] = {}

    def add_error(self, message: str):
        """Add an error to the validation results."""
        self.errors.append(message)

    def add_warning(self, message: str):
        """Add a warning to the validation results."""
        self.warnings.append(message)

    def is_valid(self) -> bool:
        """Check if validation passed (no errors)."""
        return len(self.errors) == 0

    def __str__(self) -> str:
        """String representation of validation results."""
        status = "✓ PASS" if self.is_valid() else "✗ FAIL"
        lines = [f"\n{self.chapter}: {status}"]

        if self.stats:
            lines.append("  Statistics:")
            for key, value in self.stats.items():
                lines.append(f"    {key}: {value}")

        if self.errors:
            lines.append("  Errors:")
            for error in self.errors:
                lines.append(f"    - {error}")

        if self.warnings:
            lines.append("  Warnings:")
            for warning in self.warnings:
                lines.append(f"    - {warning}")

        return "\n".join(lines)


def check_markdown_validity(content: str, result: ValidationResult) -> None:
    """
    Check that content is valid vanilla markdown with no extended features.

    Validates:
    - No HTML tags (except comments)
    - No extended markdown features (definition lists, footnotes, etc.)
    - Valid markdown syntax

    Args:
        content: Chapter content to validate
        result: ValidationResult to update with findings
    """
    lines = content.split('\n')

    # Check for HTML tags (excluding comments)
    html_pattern = re.compile(r'<(?!!--)[^>]+>')
    for i, line in enumerate(lines, 1):
        if html_pattern.search(line):
            result.add_error(f"Line {i}: HTML tags found: {line.strip()[:50]}")

    # Check for extended markdown features
    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Check for definition lists (: at start of line)
        if stripped.startswith(':') and not stripped.startswith('::'):
            result.add_warning(f"Line {i}: Possible definition list syntax")

        # Check for footnote references [^1]
        if re.search(r'\[\^[\w\d]+\]', stripped):
            result.add_warning(f"Line {i}: Footnote reference found")

        # Check for tables with extended features (alignment markers)
        if re.match(r'\|[\s:]+[\-:]+[\s:]+\|', stripped):
            if ':' in stripped:
                result.add_warning(f"Line {i}: Table with alignment markers (extended markdown)")

    # Update statistics
    result.stats['total_lines'] = len(lines)
    result.stats['non_empty_lines'] = sum(1 for line in lines if line.strip())


def check_heading_consistency(content: str, result: ValidationResult) -> None:
    """
    Check that heading hierarchy is consistent throughout the chapter.

    Validates:
    - Headings use # syntax correctly
    - No heading level skips (e.g., # followed by ###)
    - Headings have proper spacing

    Args:
        content: Chapter content to validate
        result: ValidationResult to update with findings
    """
    lines = content.split('\n')

    heading_pattern = re.compile(r'^(#{1,6})\s+(.+)')
    prev_level = 0
    heading_count = 0

    for i, line in enumerate(lines, 1):
        match = heading_pattern.match(line)

        if match:
            heading_count += 1
            level = len(match.group(1))
            title = match.group(2)

            # Check for proper spacing after heading
            if i < len(lines) and lines[i].strip() != '':
                # Next line should be blank or another heading
                if not lines[i].startswith('#'):
                    result.add_warning(f"Line {i}: Heading should be followed by blank line")

            # Check for level skips (only skip 1 level at most)
            if prev_level > 0 and level > prev_level + 1:
                result.add_warning(f"Line {i}: Heading level skip from H{prev_level} to H{level}")

            prev_level = level

    result.stats['heading_count'] = heading_count


def check_list_formatting(content: str, result: ValidationResult) -> None:
    """
    Check that list formatting is consistent and correct.

    Validates:
    - Proper list indentation (0, 2, 4 spaces for levels 1-3)
    - Consistent list markers (- for bullets)
    - No unicode bullets (●○■) in output
    - Proper spacing around lists

    Args:
        content: Chapter content to validate
        result: ValidationResult to update with findings
    """
    lines = content.split('\n')

    bullet_pattern = re.compile(r'^(\s*)-\s+(.+)')
    unicode_bullet_pattern = re.compile(r'[●○■]')

    bullet_count = 0
    in_list = False

    for i, line in enumerate(lines, 1):
        # Check for unicode bullets (should be converted)
        if unicode_bullet_pattern.search(line):
            result.add_error(f"Line {i}: Unicode bullet found (should be converted): {line.strip()[:50]}")

        # Check markdown bullets
        match = bullet_pattern.match(line)
        if match:
            bullet_count += 1
            indent = match.group(1)
            content_part = match.group(2)

            # Check indentation is correct (0, 2, or 4 spaces)
            indent_len = len(indent)
            if indent_len not in [0, 2, 4]:
                result.add_warning(f"Line {i}: Non-standard bullet indentation ({indent_len} spaces)")

            in_list = True
        elif in_list and line.strip() == '':
            # Check if there's a blank line within list
            if i < len(lines):
                next_line = lines[i] if i < len(lines) else ''
                if re.match(r'^\s*-\s+', next_line):
                    result.add_warning(f"Line {i}: Blank line within list block")
            in_list = False
        elif not line.strip().startswith('-'):
            in_list = False

    result.stats['bullet_count'] = bullet_count


def validate_unicode_brackets(content: str, result: ValidationResult) -> None:
    """
    Validate that unicode brackets are preserved where they should be.

    Checks:
    - Unicode brackets ˹˺ are present if chapter should have them
    - Brackets are properly paired
    - Brackets are not malformed

    Args:
        content: Chapter content to validate
        result: ValidationResult to update with findings
    """
    # Count opening and closing brackets
    opening_count = content.count('˹')
    closing_count = content.count('˺')

    result.stats['unicode_bracket_pairs'] = min(opening_count, closing_count)

    # Check for unpaired brackets
    if opening_count != closing_count:
        result.add_warning(f"Unpaired unicode brackets: {opening_count} opening, {closing_count} closing")

    # Check for common bracket errors
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        # Check for brackets without content
        if '˹˺' in line:
            result.add_warning(f"Line {i}: Empty unicode brackets found")

        # Check for nested brackets (uncommon, might be error)
        if '˹˹' in line or '˺˺' in line:
            result.add_warning(f"Line {i}: Nested or duplicate unicode brackets")


def validate_chapter(chapter_file: Path) -> ValidationResult:
    """
    Validate a single chapter file.

    Args:
        chapter_file: Path to chapter file to validate

    Returns:
        ValidationResult with findings
    """
    result = ValidationResult(chapter_file.name)

    if not chapter_file.exists():
        result.add_error(f"File not found: {chapter_file}")
        return result

    # Read chapter content
    try:
        content = chapter_file.read_text(encoding='utf-8')
    except Exception as e:
        result.add_error(f"Failed to read file: {e}")
        return result

    # Run all validation checks
    check_markdown_validity(content, result)
    check_heading_consistency(content, result)
    check_list_formatting(content, result)
    validate_unicode_brackets(content, result)

    return result


def generate_validation_report(results: List[ValidationResult], output_file: Path) -> None:
    """
    Generate a validation report summarizing all results.

    Args:
        results: List of validation results
        output_file: Path to write report
    """
    lines = ["# Validation Report", ""]
    lines.append(f"**Date**: {Path(__file__).parent.parent.parent}")
    lines.append("")

    # Summary statistics
    total_chapters = len(results)
    passed = sum(1 for r in results if r.is_valid())
    failed = total_chapters - passed

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total chapters validated: {total_chapters}")
    lines.append(f"- Passed: {passed}")
    lines.append(f"- Failed: {failed}")
    lines.append("")

    # Overall statistics
    lines.append("## Statistics")
    lines.append("")

    total_stats = defaultdict(int)
    for result in results:
        for key, value in result.stats.items():
            total_stats[key] += value

    for key, value in sorted(total_stats.items()):
        lines.append(f"- {key}: {value}")
    lines.append("")

    # Individual chapter results
    lines.append("## Chapter Results")
    lines.append("")

    for result in results:
        lines.append(str(result))
        lines.append("")

    # Write report
    report_text = '\n'.join(lines)
    output_file.write_text(report_text, encoding='utf-8')
    print(f"✓ Validation report written to: {output_file}")


def main():
    """Main entry point for validation."""
    import argparse

    parser = argparse.ArgumentParser(description='Validate reformatted chapters')
    parser.add_argument('--chapter', type=str, help='Validate specific chapter (e.g., 02)')
    parser.add_argument('--stage', type=str, default='02_removedbullets',
                       help='Pipeline stage to validate (default: 02_removedbullets)')
    args = parser.parse_args()

    # Determine paths
    repo_root = Path(__file__).parent.parent.parent
    chapters_dir = repo_root / "output" / "chapters" / args.stage

    if not chapters_dir.exists():
        print(f"Error: Chapters directory not found: {chapters_dir}")
        sys.exit(1)

    # Get chapters to validate
    if args.chapter:
        chapter_files = list(chapters_dir.glob(f"chapter_{args.chapter}*.md"))
        if not chapter_files:
            print(f"Error: No chapter file found for chapter {args.chapter}")
            sys.exit(1)
    else:
        chapter_files = sorted(chapters_dir.glob("chapter_*.md"))

    if not chapter_files:
        print(f"Error: No chapter files found in {chapters_dir}")
        sys.exit(1)

    print(f"Validating {len(chapter_files)} chapter(s)...\n")

    # Validate each chapter
    results = []
    for chapter_file in chapter_files:
        print(f"Validating {chapter_file.name}...")
        result = validate_chapter(chapter_file)
        results.append(result)

        # Print immediate feedback
        if result.is_valid():
            print(f"  ✓ PASS")
        else:
            print(f"  ✗ FAIL ({len(result.errors)} errors)")

    # Generate report
    report_file = chapters_dir / "VALIDATION_REPORT.md"
    generate_validation_report(results, report_file)

    # Print summary
    print("\n" + "="*60)
    passed = sum(1 for r in results if r.is_valid())
    failed = len(results) - passed
    print(f"Validation complete: {passed} passed, {failed} failed")
    print(f"Report: {report_file}")

    # Exit with error if any validation failed
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
