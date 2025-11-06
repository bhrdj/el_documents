#!/usr/bin/env python3
"""
Section entity class for hierarchical document sections.
"""

from typing import List, Optional


class Section:
    """
    Represents a hierarchical section within a document.

    Attributes:
        level: Header level (1-6, corresponding to #, ##, ###, etc.)
        title: Section title text (without header markers or numbering)
        number: Assigned section number (e.g., "1.2.3")
        original_number: Original section number from source (if present)
        line_index: Line number where section header appears
        content_lines: Lines belonging to this section (until next header)
        parent: Reference to parent section (one level up)
        children: Child sections (one level down)
    """

    def __init__(
        self,
        level: int,
        title: str,
        line_index: int,
        number: str = "",
        original_number: Optional[str] = None
    ):
        """
        Initialize a Section.

        Args:
            level: Header level (1-6)
            title: Section title text
            line_index: Line number where section appears
            number: Assigned section number (default: empty, set later)
            original_number: Original section number if present

        Raises:
            ValueError: If level is not 1-6
        """
        if not (1 <= level <= 6):
            raise ValueError(f"Section level must be 1-6, got: {level}")

        self.level = level
        self.title = title
        self.number = number
        self.original_number = original_number
        self.line_index = line_index
        self.content_lines: List[str] = []
        self.parent: Optional[Section] = None
        self.children: List[Section] = []

    def add_child(self, child: 'Section') -> None:
        """
        Add a child section.

        Args:
            child: Child section to add

        Raises:
            ValueError: If child level is not exactly one level deeper
        """
        if child.level != self.level + 1:
            raise ValueError(
                f"Child section level must be {self.level + 1}, got {child.level}"
            )
        child.parent = self
        self.children.append(child)

    def get_full_number(self) -> str:
        """
        Get the complete hierarchical number for this section.

        Returns:
            Full section number like "1.2.3"
        """
        return self.number

    def __repr__(self) -> str:
        return f"Section(level={self.level}, number={self.number}, title={self.title[:30]}...)"

    def __str__(self) -> str:
        indent = "  " * (self.level - 1)
        return f"{indent}{self.number} {self.title}"
