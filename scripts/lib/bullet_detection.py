"""Bullet list detection and hierarchy analysis module.

This module provides functions for detecting bullet list blocks,
analyzing indentation patterns, and determining semantic hierarchy.
"""

import re
from typing import List, Tuple, Optional
from math import gcd
from functools import reduce


def is_list_item(line: str) -> bool:
    """Check if a line is a bullet list item.

    Args:
        line: Line to check

    Returns:
        True if line is a bullet list item
    """
    stripped = line.lstrip()
    if not stripped:
        return False

    # Check for bullet markers: -, *, +
    return stripped[0] in ['-', '*', '+'] and (len(stripped) == 1 or stripped[1] == ' ')


def count_leading_spaces(line: str) -> int:
    """Count leading spaces in a line.

    Args:
        line: Line to analyze

    Returns:
        Number of leading spaces
    """
    if not line:
        return 0

    count = 0
    for char in line:
        if char == ' ':
            count += 1
        elif char == '\t':
            # Convert tabs to 4 spaces
            count += 4
        else:
            break

    return count


def get_bullet_marker(line: str) -> Optional[str]:
    """Extract the bullet marker from a list item.

    Args:
        line: Line to analyze

    Returns:
        Bullet marker (-, *, +) or None
    """
    if not is_list_item(line):
        return None

    stripped = line.lstrip()
    return stripped[0]


def detect_list_blocks(lines: List[str]) -> List[Tuple[int, int]]:
    """Detect contiguous bullet list blocks in document.

    Args:
        lines: Document lines

    Returns:
        List of (start_index, end_index) tuples for each list block
    """
    blocks = []
    in_block = False
    start_idx = 0

    for i, line in enumerate(lines):
        if is_list_item(line):
            if not in_block:
                # Start new block
                in_block = True
                start_idx = i
        else:
            # Check if this is blank line within block (allowed)
            if in_block and line.strip() == '':
                # Check next non-blank line
                next_idx = i + 1
                while next_idx < len(lines) and lines[next_idx].strip() == '':
                    next_idx += 1

                if next_idx < len(lines) and is_list_item(lines[next_idx]):
                    # Blank line within block - continue
                    continue
                else:
                    # End of block
                    blocks.append((start_idx, i - 1))
                    in_block = False
            elif in_block:
                # Non-list-item, non-blank line - end block
                blocks.append((start_idx, i - 1))
                in_block = False

    # Handle block that extends to end of document
    if in_block:
        blocks.append((start_idx, len(lines) - 1))

    return blocks


def detect_base_indent(list_block: List[str]) -> int:
    """Detect the base indentation unit from a list block using GCD approach.

    Args:
        list_block: Lines in the list block

    Returns:
        Base indentation unit in spaces (defaults to 2 if can't detect)
    """
    indents = []

    for line in list_block:
        if is_list_item(line):
            indent = count_leading_spaces(line)
            indents.append(indent)

    if not indents:
        return 2  # Default

    # Remove duplicates and sort
    unique_indents = sorted(set(indents))

    if len(unique_indents) == 1:
        # All items at same level
        return 2  # Default spacing

    # Calculate differences between consecutive levels
    differences = []
    for i in range(len(unique_indents) - 1):
        diff = unique_indents[i + 1] - unique_indents[i]
        if diff > 0:
            differences.append(diff)

    if not differences:
        return 2

    # Find GCD of all differences
    base_unit = reduce(gcd, differences)

    # Sanity check: base unit should be reasonable (1-8 spaces)
    if base_unit < 1 or base_unit > 8:
        return 2

    return base_unit


def analyze_hierarchy(list_block: List[str], base_indent: Optional[int] = None) -> List[Tuple[str, int, str, int]]:
    """Analyze hierarchy levels in a list block.

    Args:
        list_block: Lines in the list block
        base_indent: Base indentation unit (auto-detect if None)

    Returns:
        List of (original_line, indent_spaces, marker, hierarchy_level) tuples
    """
    if base_indent is None:
        base_indent = detect_base_indent(list_block)

    result = []

    for line in list_block:
        if is_list_item(line):
            indent = count_leading_spaces(line)
            marker = get_bullet_marker(line)
            level = indent // base_indent if base_indent > 0 else 0

            result.append((line, indent, marker, level))

    return result


def validate_hierarchy(hierarchy: List[Tuple[str, int, str, int]]) -> List[str]:
    """Validate hierarchy and identify issues.

    Args:
        hierarchy: Output from analyze_hierarchy

    Returns:
        List of validation warning messages
    """
    warnings = []

    if not hierarchy:
        return warnings

    # Check for gaps in hierarchy levels
    levels = [item[3] for item in hierarchy]
    max_level = max(levels)

    for i in range(1, len(hierarchy)):
        prev_level = hierarchy[i - 1][3]
        curr_level = hierarchy[i][3]

        # Check for level jumps > 1
        if curr_level > prev_level + 1:
            warnings.append(
                f"Hierarchy gap: level {prev_level} -> {curr_level} "
                f"(line: {hierarchy[i][0][:50]}...)"
            )

    # Check for inconsistent markers at same level
    level_markers = {}
    for line, indent, marker, level in hierarchy:
        if level not in level_markers:
            level_markers[level] = set()
        level_markers[level].add(marker)

    for level, markers in level_markers.items():
        if len(markers) > 1:
            warnings.append(
                f"Inconsistent markers at level {level}: {markers}"
            )

    # Check for unusual indentation patterns
    indents = [item[1] for item in hierarchy]
    unique_indents = sorted(set(indents))

    if len(unique_indents) > 6:
        warnings.append(
            f"Excessive indentation levels ({len(unique_indents)} unique indents)"
        )

    return warnings


def get_list_item_content(line: str) -> str:
    """Extract content from a bullet list item (without marker).

    Args:
        line: List item line

    Returns:
        Content without bullet marker and leading spaces
    """
    if not is_list_item(line):
        return line.strip()

    stripped = line.lstrip()

    # Remove marker and following space
    if len(stripped) > 1 and stripped[1] == ' ':
        return stripped[2:]
    else:
        return stripped[1:]


def detect_continuation_lines(lines: List[str], list_start: int, list_end: int) -> List[Tuple[int, bool]]:
    """Detect which lines in a list block are continuation lines vs. new items.

    Args:
        lines: All document lines
        list_start: Start index of list block
        list_end: End index of list block

    Returns:
        List of (line_index, is_continuation) tuples
    """
    result = []

    for i in range(list_start, list_end + 1):
        line = lines[i]

        if is_list_item(line):
            # This is a list item
            result.append((i, False))
        elif line.strip() == '':
            # Blank line - could be within or between items
            result.append((i, False))
        else:
            # Non-blank, non-list-item line - likely continuation
            # Check indentation relative to previous list item
            prev_item_indent = None
            for j in range(i - 1, list_start - 1, -1):
                if is_list_item(lines[j]):
                    prev_item_indent = count_leading_spaces(lines[j])
                    break

            is_continuation = False
            if prev_item_indent is not None:
                current_indent = count_leading_spaces(line)
                # Continuation if indented more than the list item
                is_continuation = current_indent > prev_item_indent

            result.append((i, is_continuation))

    return result
