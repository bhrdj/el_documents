#!/usr/bin/env python3
"""
Markdown parsing utilities for document structure analysis.
"""

import re
from typing import Optional, Tuple


def is_header(line: str) -> bool:
    """
    Check if a line is a markdown header.

    Args:
        line: Line of text to check

    Returns:
        True if line is a header (starts with #), False otherwise
    """
    stripped = line.strip()
    return bool(re.match(r'^#{1,6}\s+', stripped))


def get_header_level(line: str) -> Optional[int]:
    """
    Extract header level from a markdown header line.

    Args:
        line: Header line to analyze

    Returns:
        Header level (1-6) or None if not a header
    """
    stripped = line.strip()
    match = re.match(r'^(#{1,6})\s+', stripped)
    if match:
        return len(match.group(1))
    return None


def extract_section_number(line: str) -> Tuple[Optional[str], str]:
    """
    Extract section number and title from a header line.

    Supports patterns like:
    - "## 1.2 Title"
    - "## 1.2.3 Title"
    - "## Title" (no number)

    Args:
        line: Header line to parse

    Returns:
        Tuple of (section_number, title)
        section_number is None if no number found
    """
    stripped = line.strip()

    # Remove leading # symbols
    match = re.match(r'^#{1,6}\s+(.*)$', stripped)
    if not match:
        return (None, stripped)

    rest = match.group(1).strip()

    # Try to extract section number
    # Pattern: optional number(s) with dots, followed by space and title
    num_match = re.match(r'^([\d.]+)\s+(.*)$', rest)
    if num_match:
        number = num_match.group(1).rstrip('.')
        title = num_match.group(2).strip()
        return (number, title)

    # No section number found
    return (None, rest)


def is_list_item(line: str) -> bool:
    """
    Check if a line is a list item (bullet or numbered).

    Args:
        line: Line to check

    Returns:
        True if line is a list item, False otherwise
    """
    stripped = line.lstrip(' ')

    # Bullet list: starts with -, *, or +
    if re.match(r'^[-*+]\s+', stripped):
        return True

    # Numbered list: starts with digit(s) followed by . or )
    if re.match(r'^\d+[.)]\s+', stripped):
        return True

    return False


def get_list_marker(line: str) -> Optional[str]:
    """
    Extract the list marker from a list item line.

    Args:
        line: List item line

    Returns:
        The marker character(s) or None if not a list item
    """
    stripped = line.lstrip(' ')

    # Bullet list marker
    match = re.match(r'^([-*+])\s+', stripped)
    if match:
        return match.group(1)

    # Numbered list marker
    match = re.match(r'^(\d+[.)])\s+', stripped)
    if match:
        return match.group(1)

    return None


def count_leading_spaces(line: str) -> int:
    """
    Count leading spaces in a line.

    Args:
        line: Line to analyze

    Returns:
        Number of leading spaces
    """
    return len(line) - len(line.lstrip(' '))


def extract_list_content(line: str) -> Optional[str]:
    """
    Extract content from a list item (without marker and leading spaces).

    Args:
        line: List item line

    Returns:
        Content text or None if not a list item
    """
    stripped = line.lstrip(' ')

    # Bullet list
    match = re.match(r'^[-*+]\s+(.*)$', stripped)
    if match:
        return match.group(1)

    # Numbered list
    match = re.match(r'^\d+[.)]\s+(.*)$', stripped)
    if match:
        return match.group(1)

    return None


def is_empty_line(line: str) -> bool:
    """
    Check if a line is empty or contains only whitespace.

    Args:
        line: Line to check

    Returns:
        True if empty or whitespace only, False otherwise
    """
    return len(line.strip()) == 0


def is_code_fence(line: str) -> bool:
    """
    Check if a line is a code fence (``` or ~~~).

    Args:
        line: Line to check

    Returns:
        True if code fence, False otherwise
    """
    stripped = line.strip()
    return bool(re.match(r'^[`~]{3,}', stripped))
