"""Bullet list repair module for fixing hierarchy and formatting.

This module provides functions for repairing bullet list indentation,
applying consistent markers, and enforcing maximum depth limits.
"""

from typing import List, Tuple, Optional
from .bullet_detection import (
    is_list_item,
    count_leading_spaces,
    get_bullet_marker,
    get_list_item_content,
    detect_base_indent
)


# Default marker sequence by hierarchy level
DEFAULT_MARKERS = ['-', '*', '+', '-', '*', '+']


def standardize_indentation(
    list_block: List[str],
    spaces_per_level: int = 2,
    base_indent: Optional[int] = None
) -> List[str]:
    """Standardize indentation in a list block.

    Args:
        list_block: Lines in the list block
        spaces_per_level: Target spaces per indentation level
        base_indent: Current base indentation (auto-detect if None)

    Returns:
        List block with standardized indentation
    """
    if base_indent is None:
        base_indent = detect_base_indent(list_block)

    result = []

    for line in list_block:
        if is_list_item(line):
            # Get current level
            current_indent = count_leading_spaces(line)
            current_level = current_indent // base_indent if base_indent > 0 else 0

            # Calculate new indent
            new_indent = current_level * spaces_per_level

            # Get content
            content = get_list_item_content(line)
            marker = get_bullet_marker(line)

            # Reconstruct line
            new_line = ' ' * new_indent + marker + ' ' + content + '\n'
            result.append(new_line)
        else:
            # Preserve non-list lines
            result.append(line)

    return result


def apply_marker_sequence(
    list_block: List[str],
    marker_sequence: Optional[List[str]] = None,
    base_indent: Optional[int] = None
) -> List[str]:
    """Apply consistent marker sequence by hierarchy level.

    Args:
        list_block: Lines in the list block
        marker_sequence: Marker sequence for levels (defaults to ['-', '*', '+', ...])
        base_indent: Base indentation unit (auto-detect if None)

    Returns:
        List block with consistent markers
    """
    if marker_sequence is None:
        marker_sequence = DEFAULT_MARKERS

    if base_indent is None:
        base_indent = detect_base_indent(list_block)

    result = []

    for line in list_block:
        if is_list_item(line):
            # Determine level
            indent = count_leading_spaces(line)
            level = indent // base_indent if base_indent > 0 else 0

            # Get appropriate marker for level
            marker_idx = level % len(marker_sequence)
            new_marker = marker_sequence[marker_idx]

            # Get content
            content = get_list_item_content(line)

            # Preserve indentation, update marker
            indent_str = ' ' * indent
            new_line = indent_str + new_marker + ' ' + content + '\n'
            result.append(new_line)
        else:
            # Preserve non-list lines
            result.append(line)

    return result


def limit_nesting_depth(
    list_block: List[str],
    max_depth: int = 4,
    base_indent: Optional[int] = None
) -> Tuple[List[str], int]:
    """Limit nesting depth of bullet lists.

    Args:
        list_block: Lines in the list block
        max_depth: Maximum nesting levels allowed (default: 4)
        base_indent: Base indentation unit (auto-detect if None)

    Returns:
        Tuple of (repaired list block, number of items flattened)
    """
    if base_indent is None:
        base_indent = detect_base_indent(list_block)

    result = []
    flattened_count = 0

    for line in list_block:
        if is_list_item(line):
            # Determine current level
            indent = count_leading_spaces(line)
            level = indent // base_indent if base_indent > 0 else 0

            # Cap level at max_depth
            if level >= max_depth:
                new_level = max_depth - 1
                new_indent = new_level * base_indent
                flattened_count += 1
            else:
                new_indent = indent

            # Get content and marker
            content = get_list_item_content(line)
            marker = get_bullet_marker(line)

            # Reconstruct line
            new_line = ' ' * new_indent + marker + ' ' + content + '\n'
            result.append(new_line)
        else:
            # Preserve non-list lines
            result.append(line)

    return result, flattened_count


def repair_bullet_list(
    list_block: List[str],
    spaces_per_level: int = 2,
    marker_sequence: Optional[List[str]] = None,
    max_depth: Optional[int] = 4
) -> Tuple[List[str], dict]:
    """Comprehensively repair a bullet list block.

    Applies all repairs:
    1. Detects base indentation
    2. Standardizes spacing
    3. Applies consistent markers
    4. Limits nesting depth

    Args:
        list_block: Lines in the list block
        spaces_per_level: Target spaces per indentation level
        marker_sequence: Marker sequence by level
        max_depth: Maximum nesting depth (None = no limit)

    Returns:
        Tuple of (repaired list block, statistics dict)
    """
    if not list_block:
        return list_block, {}

    stats = {
        'original_items': sum(1 for line in list_block if is_list_item(line)),
        'base_indent_detected': None,
        'items_flattened': 0,
        'markers_changed': 0,
        'indents_changed': 0
    }

    # Detect base indentation
    base_indent = detect_base_indent(list_block)
    stats['base_indent_detected'] = base_indent

    # Track original state for statistics
    original_state = []
    for line in list_block:
        if is_list_item(line):
            original_state.append((
                count_leading_spaces(line),
                get_bullet_marker(line)
            ))

    # Step 1: Standardize indentation
    repaired = standardize_indentation(
        list_block,
        spaces_per_level=spaces_per_level,
        base_indent=base_indent
    )

    # Step 2: Apply marker sequence
    repaired = apply_marker_sequence(
        repaired,
        marker_sequence=marker_sequence,
        base_indent=spaces_per_level  # Use new spacing
    )

    # Step 3: Limit depth if specified
    if max_depth is not None:
        repaired, flattened = limit_nesting_depth(
            repaired,
            max_depth=max_depth,
            base_indent=spaces_per_level  # Use new spacing
        )
        stats['items_flattened'] = flattened

    # Calculate statistics
    new_state = []
    for line in repaired:
        if is_list_item(line):
            new_state.append((
                count_leading_spaces(line),
                get_bullet_marker(line)
            ))

    for (old_indent, old_marker), (new_indent, new_marker) in zip(original_state, new_state):
        if old_indent != new_indent:
            stats['indents_changed'] += 1
        if old_marker != new_marker:
            stats['markers_changed'] += 1

    return repaired, stats


def preview_bullet_repair(
    list_block: List[str],
    spaces_per_level: int = 2,
    max_depth: Optional[int] = 4
) -> List[Tuple[int, str, str]]:
    """Preview bullet list repairs without applying them.

    Args:
        list_block: Lines in the list block
        spaces_per_level: Target spaces per indentation level
        max_depth: Maximum nesting depth

    Returns:
        List of (line_index, old_line, new_line) tuples showing changes
    """
    repaired, _ = repair_bullet_list(
        list_block,
        spaces_per_level=spaces_per_level,
        max_depth=max_depth
    )

    changes = []
    for i, (old, new) in enumerate(zip(list_block, repaired)):
        if old.strip() != new.strip():
            changes.append((i, old.rstrip(), new.rstrip()))

    return changes


def format_repair_summary(stats: dict) -> str:
    """Format repair statistics as a readable summary.

    Args:
        stats: Statistics dictionary from repair_bullet_list

    Returns:
        Formatted summary string
    """
    lines = [
        f"Bullet List Repair Summary:",
        f"  Items processed: {stats.get('original_items', 0)}",
        f"  Base indent detected: {stats.get('base_indent_detected', 'N/A')} spaces",
        f"  Indents changed: {stats.get('indents_changed', 0)}",
        f"  Markers changed: {stats.get('markers_changed', 0)}",
        f"  Items flattened (depth limit): {stats.get('items_flattened', 0)}"
    ]

    return '\n'.join(lines)
