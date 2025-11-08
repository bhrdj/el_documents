#!/usr/bin/env python3
"""
Validate document structure after repair operations.

This script performs comprehensive validation on repaired markdown documents:
- Section numbering: sequential, hierarchical, no gaps/duplicates
- Bullet hierarchy: consistent indentation, appropriate markers
- Content completeness: verify no content loss from source
- Cross-references: verify internal links still work

Usage:
    .venv/bin/python scripts/validate_structure.py --input-dir output/chapters/05_repaired
    .venv/bin/python scripts/validate_structure.py --input-dir output/chapters/05_repaired --strict
    .venv/bin/python scripts/validate_structure.py --input-dir output/chapters/05_repaired --output VALIDATION_REPORT.md
"""

import argparse
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple
import sys

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.validation import (
    ValidationIssue,
    ValidationResult,
    validate_section_numbering,
    validate_bullet_hierarchy,
    validate_content_completeness
)
from lib.parser import is_header, extract_section_number


def validate_cross_references(lines: List[str], available_sections: Set[str]) -> List[ValidationIssue]:
    """
    Validate that internal cross-references point to existing sections.

    Args:
        lines: Document lines to validate
        available_sections: Set of valid section numbers/identifiers

    Returns:
        List of validation issues found
    """
    issues = []

    # Pattern for internal links: [text](#section-id) or [text](section-number)
    link_pattern = re.compile(r'\[([^\]]+)\]\(#?([^\)]+)\)')

    for line_num, line in enumerate(lines, start=1):
        matches = link_pattern.findall(line)
        for link_text, link_target in matches:
            # Check if it's a section reference (starts with # or looks like a number)
            if link_target.startswith('#') or re.match(r'^\d+(\.\d+)*$', link_target):
                # Clean up the target
                clean_target = link_target.lstrip('#').strip()

                # Check if target exists in available sections
                # This is a simple check - could be enhanced to check anchor IDs too
                if clean_target and clean_target not in available_sections:
                    issues.append(ValidationIssue(
                        'cross_references',
                        'WARNING',
                        f"Potentially broken internal link: [{link_text}]({link_target})",
                        line_num
                    ))

    return issues


def extract_section_identifiers(lines: List[str]) -> Set[str]:
    """
    Extract all section numbers and potential anchor IDs from document.

    Args:
        lines: Document lines

    Returns:
        Set of section identifiers (numbers, IDs, etc.)
    """
    identifiers = set()

    for line in lines:
        if is_header(line):
            number, title = extract_section_number(line)
            if number:
                identifiers.add(number)

            # Also add potential anchor ID (lowercase title with hyphens)
            if title:
                anchor = title.lower().replace(' ', '-').replace('_', '-')
                # Remove non-alphanumeric characters except hyphens
                anchor = re.sub(r'[^a-z0-9-]', '', anchor)
                identifiers.add(anchor)

    return identifiers


def validate_document(
    doc_path: Path,
    source_path: Path = None,
    strict: bool = False
) -> ValidationResult:
    """
    Perform all validation checks on a document.

    Args:
        doc_path: Path to document to validate
        source_path: Optional path to source document for content comparison
        strict: If True, treat warnings as errors

    Returns:
        ValidationResult with all issues found
    """
    result = ValidationResult(doc_path)

    # Read document
    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        result.add_issue(ValidationIssue(
            'file_read',
            'ERROR',
            f"Failed to read document: {e}"
        ))
        return result

    # Section numbering validation
    section_issues = validate_section_numbering(lines)
    for issue in section_issues:
        if strict and issue.severity == 'WARNING':
            issue.severity = 'ERROR'
        result.add_issue(issue)

    if not section_issues:
        result.add_pass()

    # Bullet hierarchy validation
    bullet_issues = validate_bullet_hierarchy(lines)
    for issue in bullet_issues:
        if strict and issue.severity == 'WARNING':
            issue.severity = 'ERROR'
        result.add_issue(issue)

    if not bullet_issues:
        result.add_pass()

    # Cross-reference validation
    available_sections = extract_section_identifiers(lines)
    xref_issues = validate_cross_references(lines, available_sections)
    for issue in xref_issues:
        if strict and issue.severity == 'WARNING':
            issue.severity = 'ERROR'
        result.add_issue(issue)

    if not xref_issues:
        result.add_pass()

    # Content completeness validation (if source provided)
    if source_path and source_path.exists():
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                source_lines = f.readlines()

            content_issues = validate_content_completeness(source_lines, lines)
            for issue in content_issues:
                result.add_issue(issue)

            if not content_issues:
                result.add_pass()
        except Exception as e:
            result.add_issue(ValidationIssue(
                'content_comparison',
                'WARNING',
                f"Failed to compare with source: {e}"
            ))

    return result


def generate_report(
    results: Dict[str, ValidationResult],
    output_path: Path = None
) -> str:
    """
    Generate a validation report from results.

    Args:
        results: Dictionary mapping document paths to ValidationResults
        output_path: Optional path to write report to

    Returns:
        Report text
    """
    lines = [
        "# Document Structure Validation Report",
        "",
        f"**Generated**: {Path.cwd()}",
        f"**Documents Validated**: {len(results)}",
        ""
    ]

    # Overall summary
    total_passed = sum(r.checks_passed for r in results.values())
    total_failed = sum(r.checks_failed for r in results.values())
    total_errors = sum(r.get_error_count() for r in results.values())
    total_warnings = sum(r.get_warning_count() for r in results.values())

    overall_status = "PASS" if total_errors == 0 else "FAIL"

    lines.extend([
        "## Summary",
        "",
        f"**Overall Status**: {overall_status}",
        f"- Total checks passed: {total_passed}",
        f"- Total checks failed: {total_failed}",
        f"- Total errors: {total_errors}",
        f"- Total warnings: {total_warnings}",
        ""
    ])

    # Per-document results
    lines.extend([
        "## Document Results",
        ""
    ])

    for doc_name, result in sorted(results.items()):
        status_icon = "✓" if result.overall_status == "PASS" else "✗"
        lines.append(f"### {status_icon} {doc_name}")
        lines.append("")
        lines.append(f"**Status**: {result.overall_status}")
        lines.append(f"- Checks passed: {result.checks_passed}")
        lines.append(f"- Checks failed: {result.checks_failed}")
        lines.append(f"- Errors: {result.get_error_count()}")
        lines.append(f"- Warnings: {result.get_warning_count()}")
        lines.append("")

        if result.issues:
            lines.append("**Issues:**")
            lines.append("")

            # Group issues by check name
            issues_by_check = {}
            for issue in result.issues:
                if issue.check_name not in issues_by_check:
                    issues_by_check[issue.check_name] = []
                issues_by_check[issue.check_name].append(issue)

            for check_name, issues in sorted(issues_by_check.items()):
                lines.append(f"#### {check_name} ({len(issues)} issues)")
                lines.append("")
                for issue in issues:
                    line_info = f" (line {issue.line_number})" if issue.line_number else ""
                    lines.append(f"- **{issue.severity}**{line_info}: {issue.message}")
                lines.append("")
        else:
            lines.append("**No issues found.**")
            lines.append("")

    report_text = "\n".join(lines)

    # Write to file if requested
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"Report written to: {output_path}")

    return report_text


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate document structure after repair operations"
    )
    parser.add_argument(
        '--input-dir',
        type=Path,
        required=True,
        help="Directory containing repaired documents to validate"
    )
    parser.add_argument(
        '--source-dir',
        type=Path,
        help="Optional directory containing source documents for content comparison"
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help="Treat warnings as errors"
    )
    parser.add_argument(
        '--output',
        type=Path,
        help="Path to write validation report (default: print to stdout)"
    )
    parser.add_argument(
        '--pattern',
        default='*.md',
        help="File pattern to match (default: *.md)"
    )

    args = parser.parse_args()

    # Validate input directory
    if not args.input_dir.exists():
        print(f"Error: Input directory does not exist: {args.input_dir}", file=sys.stderr)
        sys.exit(1)

    # Find documents to validate
    documents = sorted(args.input_dir.glob(args.pattern))
    if not documents:
        print(f"Error: No documents found matching pattern: {args.pattern}", file=sys.stderr)
        sys.exit(1)

    print(f"Validating {len(documents)} documents...")
    print()

    # Validate each document
    results = {}
    for doc_path in documents:
        doc_name = doc_path.name

        # Find corresponding source document if source_dir provided
        source_path = None
        if args.source_dir:
            source_path = args.source_dir / doc_name
            if not source_path.exists():
                source_path = None

        print(f"Validating {doc_name}...", end=' ')
        result = validate_document(doc_path, source_path, args.strict)
        results[doc_name] = result

        status_icon = "✓" if result.overall_status == "PASS" else "✗"
        print(f"{status_icon} {result.overall_status}")

    print()

    # Generate and display report
    report = generate_report(results, args.output)

    if not args.output:
        print(report)

    # Exit with error code if any document failed
    if any(r.overall_status == "FAIL" for r in results.values()):
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
