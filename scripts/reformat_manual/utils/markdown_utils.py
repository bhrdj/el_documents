"""
Markdown utilities for formatting text according to the established template.
Produces vanilla markdown output without extended features.
"""

import re
from typing import List, Dict, Optional


def apply_heading_format(text: str, level: int = 1) -> str:
    """
    Format text as a markdown heading at the specified level.

    Args:
        text: Heading text
        level: Heading level (1-6, where 1 is H1)

    Returns:
        Formatted markdown heading
    """
    level = max(1, min(6, level))  # Clamp to valid range
    prefix = '#' * level
    return f"{prefix} {text.strip()}\n"


def format_bullet_list(items: List[str], indent_level: int = 0) -> str:
    """
    Format a list of items as markdown bullet list.

    Args:
        items: List of text items
        indent_level: Indentation level (0 = top level, 1 = nested, etc.)

    Returns:
        Formatted markdown bullet list
    """
    indent = '  ' * indent_level
    formatted_items = []

    for item in items:
        item_text = item.strip()
        if item_text:
            formatted_items.append(f"{indent}- {item_text}")

    return '\n'.join(formatted_items) + '\n'


def format_numbered_list(items: List[str], start: int = 1, indent_level: int = 0) -> str:
    """
    Format a list of items as markdown numbered list.

    Args:
        items: List of text items
        start: Starting number
        indent_level: Indentation level (0 = top level, 1 = nested, etc.)

    Returns:
        Formatted markdown numbered list
    """
    indent = '  ' * indent_level
    formatted_items = []

    for i, item in enumerate(items, start=start):
        item_text = item.strip()
        if item_text:
            formatted_items.append(f"{indent}{i}. {item_text}")

    return '\n'.join(formatted_items) + '\n'


def format_table(headers: List[str], rows: List[List[str]]) -> str:
    """
    Format data as a markdown table.

    Args:
        headers: Column headers
        rows: Table data rows

    Returns:
        Formatted markdown table
    """
    if not headers or not rows:
        return ""

    # Build header row
    header_row = "| " + " | ".join(headers) + " |"

    # Build separator row
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"

    # Build data rows
    data_rows = []
    for row in rows:
        # Pad row if it has fewer columns than headers
        padded_row = row + [""] * (len(headers) - len(row))
        data_rows.append("| " + " | ".join(padded_row[:len(headers)]) + " |")

    return "\n".join([header_row, separator] + data_rows) + "\n"


def apply_spacing_rules(text: str) -> str:
    """
    Apply consistent spacing rules to markdown text.

    Rules:
    - Single blank line between paragraphs
    - Single blank line before and after headings
    - Single blank line before and after lists
    - No trailing whitespace on lines
    - Single newline at end of file

    Args:
        text: Markdown text to format

    Returns:
        Text with consistent spacing
    """
    # Remove trailing whitespace from each line
    lines = [line.rstrip() for line in text.split('\n')]

    # Remove excessive blank lines (more than 2 consecutive)
    cleaned_lines = []
    blank_count = 0

    for line in lines:
        if not line.strip():
            blank_count += 1
            if blank_count <= 2:
                cleaned_lines.append(line)
        else:
            blank_count = 0
            cleaned_lines.append(line)

    # Join and ensure single newline at end
    result = '\n'.join(cleaned_lines)
    result = result.rstrip() + '\n'

    return result


def clean_text(text: str) -> str:
    """
    Clean text while preserving unicode characters.

    Args:
        text: Text to clean

    Returns:
        Cleaned text
    """
    # Remove excessive whitespace but preserve intentional spacing
    # Do NOT remove unicode characters

    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Remove multiple spaces (but preserve single spaces)
    text = re.sub(r' {2,}', ' ', text)

    return text


def escape_markdown_special_chars(text: str, preserve_formatting: bool = False) -> str:
    """
    Escape markdown special characters that should be treated as literal.

    Args:
        text: Text that may contain special characters
        preserve_formatting: If True, preserve intentional markdown formatting

    Returns:
        Text with special characters escaped
    """
    if preserve_formatting:
        # Only escape characters that are clearly not intentional formatting
        # This is conservative to avoid breaking actual formatting
        return text

    # Characters that need escaping: \ ` * _ { } [ ] ( ) # + - . ! |
    special_chars = ['\\', '`', '*', '_', '{', '}', '[', ']', '(', ')', '#', '+', '-', '.', '!', '|']

    for char in special_chars:
        text = text.replace(char, '\\' + char)

    return text


def create_section_separator() -> str:
    """
    Create a section separator (horizontal rule in markdown).

    Returns:
        Markdown horizontal rule
    """
    return "---\n"


def format_paragraph(text: str) -> str:
    """
    Format text as a paragraph with proper spacing.

    Args:
        text: Paragraph text

    Returns:
        Formatted paragraph
    """
    # Clean the text
    text = clean_text(text.strip())

    # Ensure paragraph ends with newline
    if text and not text.endswith('\n'):
        text += '\n'

    return text


def detect_list_type(text: str) -> Optional[str]:
    """
    Detect if text represents a list item and what type.

    Args:
        text: Text line to analyze

    Returns:
        'bullet', 'numbered', or None
    """
    text = text.strip()

    # Check for bullet list markers
    if re.match(r'^[•\-\*]\s+', text):
        return 'bullet'

    # Check for numbered list markers
    if re.match(r'^\d+[\.\)]\s+', text):
        return 'numbered'

    return None
