"""Section numbering module for document structure repair.

This module implements stream-based hierarchical section numbering
using a counter stack approach for efficient single-pass processing.
"""

from typing import List, Tuple, Optional
import re


class SectionNumberer:
    """Stream-based section numbering with counter stack management.

    Processes documents line-by-line, maintaining hierarchical numbering
    state through a counter stack. Supports up to 6 levels of hierarchy.
    """

    def __init__(self, max_levels: int = 6):
        """Initialize the section numberer.

        Args:
            max_levels: Maximum hierarchy depth to support (default: 6)
        """
        self.max_levels = max_levels
        # Counter stack: index 0 unused, 1-6 for header levels #-######
        self.counters = [0] * (max_levels + 1)
        self.current_level = 0

    def reset(self):
        """Reset all counters to initial state."""
        self.counters = [0] * (self.max_levels + 1)
        self.current_level = 0

    def process_header(self, level: int) -> str:
        """Process a header at the given level and return its number.

        Args:
            level: Header level (1-6 for # through ######)

        Returns:
            Formatted section number (e.g., "1.2.3")
        """
        if level < 1 or level > self.max_levels:
            raise ValueError(f"Header level must be between 1 and {self.max_levels}")

        # Increment counter at this level
        self.counters[level] += 1

        # Reset all deeper levels
        for i in range(level + 1, self.max_levels + 1):
            self.counters[i] = 0

        # Update current level
        self.current_level = level

        # Build section number from counter stack
        return self.format_number(level)

    def format_number(self, level: int) -> str:
        """Format section number from counter stack.

        Args:
            level: Header level to format up to

        Returns:
            Formatted section number (e.g., "1.2.3")
        """
        parts = [str(self.counters[i]) for i in range(1, level + 1)]
        return '.'.join(parts)

    def get_current_number(self) -> str:
        """Get the current section number.

        Returns:
            Current section number or empty string if no section processed yet
        """
        if self.current_level == 0:
            return ""
        return self.format_number(self.current_level)


def get_header_level(line: str) -> Optional[int]:
    """Extract header level from a markdown line.

    Args:
        line: Markdown line to check

    Returns:
        Header level (1-6) or None if not a header
    """
    stripped = line.lstrip()
    if not stripped.startswith('#'):
        return None

    # Count leading # characters
    level = 0
    for char in stripped:
        if char == '#':
            level += 1
        else:
            break

    # Must have space after # and be valid level
    if level > 0 and level <= 6 and len(stripped) > level and stripped[level] == ' ':
        return level

    return None


def extract_header_text(line: str) -> str:
    """Extract the text content from a header line, removing # and section numbers.

    Args:
        line: Header line to process

    Returns:
        Header text without leading # and existing section numbers
    """
    stripped = line.lstrip()
    if not stripped.startswith('#'):
        return line.strip()

    # Remove leading #'s and space
    level = get_header_level(line)
    if level is None:
        return line.strip()

    text = stripped[level:].strip()

    # Remove existing section number if present (e.g., "1.2.3 Title" -> "Title")
    # Pattern: optional number at start followed by space
    text = re.sub(r'^\d+(\.\d+)*\s+', '', text)

    return text


def format_header_line(level: int, number: str, text: str, preserve_indent: bool = True,
                       original_line: str = "") -> str:
    """Format a header line with proper numbering.

    Args:
        level: Header level (1-6)
        number: Section number to insert
        text: Header text
        preserve_indent: Whether to preserve original indentation
        original_line: Original line (for preserving indentation)

    Returns:
        Formatted header line
    """
    # Get original indentation if preserving
    indent = ""
    if preserve_indent and original_line:
        indent = original_line[:len(original_line) - len(original_line.lstrip())]

    # Build header
    hashes = '#' * level
    return f"{indent}{hashes} {number} {text}"


def renumber_document_headers(lines: List[str], numberer: Optional[SectionNumberer] = None) -> List[str]:
    """Renumber all headers in a document.

    Args:
        lines: Document lines
        numberer: SectionNumberer instance (creates new one if None)

    Returns:
        Document lines with renumbered headers
    """
    if numberer is None:
        numberer = SectionNumberer()
    else:
        numberer.reset()

    result = []

    for line in lines:
        level = get_header_level(line)

        if level is not None:
            # This is a header - renumber it
            number = numberer.process_header(level)
            text = extract_header_text(line)
            new_line = format_header_line(level, number, text,
                                         preserve_indent=True,
                                         original_line=line)
            result.append(new_line)
        else:
            # Not a header - preserve as-is
            result.append(line)

    return result


def preview_renumbering(lines: List[str]) -> List[Tuple[int, str, str]]:
    """Preview what renumbering would do without modifying the document.

    Args:
        lines: Document lines

    Returns:
        List of (line_number, old_header, new_header) tuples
    """
    numberer = SectionNumberer()
    changes = []

    for i, line in enumerate(lines, 1):
        level = get_header_level(line)

        if level is not None:
            number = numberer.process_header(level)
            text = extract_header_text(line)
            new_line = format_header_line(level, number, text,
                                         preserve_indent=True,
                                         original_line=line)

            if line.strip() != new_line.strip():
                changes.append((i, line.strip(), new_line.strip()))

    return changes
