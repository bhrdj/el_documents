#!/usr/bin/env python3
"""
Bullet list entity classes for hierarchical list structure.
"""

from typing import List, Optional


class BulletItem:
    """
    Represents a single item in a bullet list.

    Attributes:
        line_index: Line number of this item
        level: Nesting level (0-based: 0 = top level)
        indent: Actual leading spaces
        marker: Bullet marker character ('-', '*', '+', or number)
        content: Item text (without marker and spaces)
        parent: Parent item (one level up)
        children: Child items (one level down)
    """

    def __init__(
        self,
        line_index: int,
        level: int,
        indent: int,
        marker: str,
        content: str
    ):
        """
        Initialize a BulletItem.

        Args:
            line_index: Line number of this item
            level: Nesting level (0-based)
            indent: Actual leading spaces
            marker: Bullet marker
            content: Item text

        Raises:
            ValueError: If level is negative or > 6
        """
        if level < 0 or level > 6:
            raise ValueError(f"Bullet level must be 0-6, got: {level}")

        self.line_index = line_index
        self.level = level
        self.indent = indent
        self.marker = marker
        self.content = content
        self.parent: Optional[BulletItem] = None
        self.children: List[BulletItem] = []

    def add_child(self, child: 'BulletItem') -> None:
        """Add a child item."""
        child.parent = self
        self.children.append(child)

    def __repr__(self) -> str:
        return f"BulletItem(level={self.level}, marker={self.marker}, content={self.content[:30]}...)"


class BulletList:
    """
    Represents a contiguous block of bullet list items with hierarchy.

    Attributes:
        start_line: Line index where list starts
        end_line: Line index where list ends
        items: Individual list items
        max_depth: Maximum nesting depth in this list
        base_indent: Base indentation unit (detected or 2)
        is_ordered: True if numbered list, False if bullet list
    """

    def __init__(
        self,
        start_line: int,
        end_line: int = -1,
        base_indent: int = 2,
        is_ordered: bool = False
    ):
        """
        Initialize a BulletList.

        Args:
            start_line: Starting line number
            end_line: Ending line number (set later if not known)
            base_indent: Base indentation unit in spaces
            is_ordered: Whether this is a numbered list

        Raises:
            ValueError: If start_line < 0 or end_line < start_line (when end_line >= 0)
        """
        if start_line < 0:
            raise ValueError(f"start_line must be >= 0, got: {start_line}")

        if end_line >= 0 and end_line < start_line:
            raise ValueError(f"end_line must be >= start_line, got: {end_line} < {start_line}")

        self.start_line = start_line
        self.end_line = end_line
        self.items: List[BulletItem] = []
        self.max_depth = 0
        self.base_indent = base_indent
        self.is_ordered = is_ordered

    def add_item(self, item: BulletItem) -> None:
        """
        Add a bullet item to the list.

        Args:
            item: BulletItem to add
        """
        self.items.append(item)
        if item.level > self.max_depth:
            self.max_depth = item.level

    def validate(self) -> bool:
        """
        Validate list structure.

        Returns:
            True if valid, False otherwise

        Validation checks:
        - All items have line_index between start_line and end_line
        - Max depth <= 6 (pandoc limit)
        """
        if self.end_line < 0:
            return False

        for item in self.items:
            if not (self.start_line <= item.line_index <= self.end_line):
                return False

        if self.max_depth > 6:
            return False

        return True

    def __repr__(self) -> str:
        return f"BulletList(lines={self.start_line}-{self.end_line}, items={len(self.items)}, max_depth={self.max_depth})"

    def __str__(self) -> str:
        return f"Bullet List [{self.start_line}-{self.end_line}]: {len(self.items)} items, depth {self.max_depth}"
