#!/usr/bin/env python3
"""
Hierarchy level class for section numbering state management.
"""

from typing import List


class HierarchyLevel:
    """
    Represents a level in the document hierarchy with numbering state.

    Attributes:
        depth: Nesting depth (1-6)
        counter: Current counter value at this level
        separator: Separator character (typically ".")
    """

    def __init__(self, depth: int, counter: int = 0, separator: str = "."):
        """
        Initialize a HierarchyLevel.

        Args:
            depth: Nesting depth (1-6)
            counter: Initial counter value (default: 0)
            separator: Separator character (default: ".")

        Raises:
            ValueError: If depth is not 1-6
        """
        if not (1 <= depth <= 6):
            raise ValueError(f"Hierarchy depth must be 1-6, got: {depth}")

        self.depth = depth
        self.counter = counter
        self.separator = separator

    def increment(self) -> int:
        """
        Increment the counter and return the new value.

        Returns:
            The new counter value
        """
        self.counter += 1
        return self.counter

    def reset(self) -> None:
        """Reset the counter to 0."""
        self.counter = 0

    def __repr__(self) -> str:
        return f"HierarchyLevel(depth={self.depth}, counter={self.counter})"


class HierarchyState:
    """
    Manages numbering state across all hierarchy levels.

    This class maintains a stack of counters for each hierarchy level
    and provides methods to generate section numbers.
    """

    def __init__(self, max_depth: int = 6):
        """
        Initialize hierarchy state.

        Args:
            max_depth: Maximum hierarchy depth (default: 6)
        """
        self.max_depth = max_depth
        # Create level counters for each depth (1-6)
        self.levels = [HierarchyLevel(i) for i in range(1, max_depth + 1)]

    def process_header(self, level: int) -> str:
        """
        Process a header at the given level and generate its number.

        This implements the stream-based numbering algorithm:
        1. Increment counter at current level
        2. Reset all deeper level counters
        3. Generate number from all active levels

        Args:
            level: Header level (1-6)

        Returns:
            Generated section number (e.g., "1.2.3")

        Raises:
            ValueError: If level is not 1-6
        """
        if not (1 <= level <= self.max_depth):
            raise ValueError(f"Level must be 1-{self.max_depth}, got: {level}")

        # Increment counter at this level
        level_idx = level - 1
        self.levels[level_idx].increment()

        # Reset all deeper levels
        for i in range(level_idx + 1, self.max_depth):
            self.levels[i].reset()

        # Build number from all active levels
        number_parts = [str(self.levels[i].counter) for i in range(0, level_idx + 1)]
        return ".".join(number_parts)

    def reset(self) -> None:
        """Reset all level counters to 0."""
        for level in self.levels:
            level.reset()

    def get_current_number(self, level: int) -> str:
        """
        Get the current number at a given level without incrementing.

        Args:
            level: Header level (1-6)

        Returns:
            Current section number at that level
        """
        if not (1 <= level <= self.max_depth):
            raise ValueError(f"Level must be 1-{self.max_depth}, got: {level}")

        level_idx = level - 1
        number_parts = [str(self.levels[i].counter) for i in range(0, level_idx + 1)]
        return ".".join(number_parts)

    def __repr__(self) -> str:
        counters = [level.counter for level in self.levels]
        return f"HierarchyState(counters={counters})"
