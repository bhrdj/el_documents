#!/usr/bin/env python3
"""
Validation utilities for document structure checks.
"""

import re
from typing import List, Tuple, Optional
from pathlib import Path


class ValidationIssue:
    """
    Represents a validation issue found in a document.

    Attributes:
        check_name: Name of the validation check
        severity: 'ERROR' or 'WARNING'
        line_number: Line where issue occurs (None if document-wide)
        message: Description of the issue
    """

    def __init__(
        self,
        check_name: str,
        severity: str,
        message: str,
        line_number: Optional[int] = None
    ):
        """
        Initialize a ValidationIssue.

        Args:
            check_name: Name of the check
            severity: 'ERROR' or 'WARNING'
            message: Issue description
            line_number: Line number (optional)
        """
        if severity not in ('ERROR', 'WARNING'):
            raise ValueError(f"Severity must be 'ERROR' or 'WARNING', got: {severity}")

        self.check_name = check_name
        self.severity = severity
        self.line_number = line_number
        self.message = message

    def __repr__(self) -> str:
        line_info = f" (line {self.line_number})" if self.line_number is not None else ""
        return f"{self.severity}: {self.check_name}{line_info} - {self.message}"


class ValidationResult:
    """
    Results of document structure validation.

    Attributes:
        document_path: Path to validated document
        checks_passed: Number of checks that passed
        checks_failed: Number of checks that failed
        issues: List of issues found
        overall_status: 'PASS' or 'FAIL'
    """

    def __init__(self, document_path: Path):
        """
        Initialize a ValidationResult.

        Args:
            document_path: Path to the document being validated
        """
        self.document_path = Path(document_path)
        self.checks_passed = 0
        self.checks_failed = 0
        self.issues: List[ValidationIssue] = []
        self.overall_status = 'PASS'

    def add_issue(self, issue: ValidationIssue) -> None:
        """Add a validation issue."""
        self.issues.append(issue)
        if issue.severity == 'ERROR':
            self.checks_failed += 1
            self.overall_status = 'FAIL'

    def add_pass(self) -> None:
        """Record a passed check."""
        self.checks_passed += 1

    def get_error_count(self) -> int:
        """Get count of ERROR-level issues."""
        return sum(1 for issue in self.issues if issue.severity == 'ERROR')

    def get_warning_count(self) -> int:
        """Get count of WARNING-level issues."""
        return sum(1 for issue in self.issues if issue.severity == 'WARNING')

    def __repr__(self) -> str:
        return f"ValidationResult({self.overall_status}: {self.checks_passed} passed, {self.checks_failed} failed)"


def validate_section_numbering(lines: List[str]) -> List[ValidationIssue]:
    """
    Validate that section numbering is consistent and hierarchical.

    Args:
        lines: Document lines to validate

    Returns:
        List of validation issues found
    """
    from .parser import is_header, get_header_level, extract_section_number

    issues = []
    prev_number_parts: List[int] = []

    for line_num, line in enumerate(lines, start=1):
        if not is_header(line):
            continue

        level = get_header_level(line)
        number, title = extract_section_number(line)

        if not number:
            # Header without number - could be intentional (title page, etc.)
            continue

        # Parse number into parts
        try:
            parts = [int(p) for p in number.split('.')]
        except ValueError:
            issues.append(ValidationIssue(
                'section_numbering',
                'ERROR',
                f"Invalid section number format: {number}",
                line_num
            ))
            continue

        # Check that number depth matches header level
        if len(parts) != level:
            issues.append(ValidationIssue(
                'section_numbering',
                'WARNING',
                f"Section number depth ({len(parts)}) doesn't match header level ({level}): {number}",
                line_num
            ))

        # Check sequential numbering
        if prev_number_parts:
            # Compare with previous number
            is_valid = False

            # Case 1: Same level, incremented by 1
            if len(parts) == len(prev_number_parts):
                if parts[:-1] == prev_number_parts[:-1] and parts[-1] == prev_number_parts[-1] + 1:
                    is_valid = True

            # Case 2: Deeper level (parent is previous number)
            elif len(parts) == len(prev_number_parts) + 1:
                if parts[:-1] == prev_number_parts and parts[-1] == 1:
                    is_valid = True

            # Case 3: Shallower level (going back up)
            elif len(parts) < len(prev_number_parts):
                # Check that we're continuing from the right ancestor
                common_depth = len(parts) - 1
                if parts[:common_depth] == prev_number_parts[:common_depth]:
                    is_valid = True

            if not is_valid:
                issues.append(ValidationIssue(
                    'section_numbering',
                    'ERROR',
                    f"Non-sequential section number: {prev_number_parts} -> {parts}",
                    line_num
                ))

        prev_number_parts = parts

    return issues


def validate_bullet_hierarchy(lines: List[str]) -> List[ValidationIssue]:
    """
    Validate bullet list indentation and hierarchy.

    Args:
        lines: Document lines to validate

    Returns:
        List of validation issues found
    """
    from .parser import is_list_item, count_leading_spaces

    issues = []
    in_list = False
    prev_indent = -1

    for line_num, line in enumerate(lines, start=1):
        if is_list_item(line):
            indent = count_leading_spaces(line)

            if not in_list:
                # Starting a new list
                in_list = True
                if indent != 0:
                    issues.append(ValidationIssue(
                        'bullet_hierarchy',
                        'WARNING',
                        f"List starts with non-zero indent: {indent} spaces",
                        line_num
                    ))
                prev_indent = indent
                continue

            # Check indent change is reasonable
            indent_change = indent - prev_indent
            if indent_change > 4:
                issues.append(ValidationIssue(
                    'bullet_hierarchy',
                    'WARNING',
                    f"Large indent jump: {prev_indent} -> {indent} spaces",
                    line_num
                ))

            prev_indent = indent
        else:
            # Not a list item - reset
            if in_list and not line.strip() == '':
                in_list = False
                prev_indent = -1

    return issues


def validate_content_completeness(source_lines: List[str], output_lines: List[str]) -> List[ValidationIssue]:
    """
    Validate that output contains all content from source.

    Args:
        source_lines: Source document lines
        output_lines: Output document lines

    Returns:
        List of validation issues found
    """
    issues = []

    # Simple check: output should have at least as many non-empty lines as source
    source_content = [line for line in source_lines if line.strip()]
    output_content = [line for line in output_lines if line.strip()]

    if len(output_content) < len(source_content) * 0.9:  # Allow 10% variation
        issues.append(ValidationIssue(
            'content_completeness',
            'ERROR',
            f"Output has significantly fewer lines ({len(output_content)}) than source ({len(source_content)})"
        ))

    return issues
