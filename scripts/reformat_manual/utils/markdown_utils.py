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

    # Check for bullet list markers (including unicode bullets from PDF)
    if re.match(r'^[●○•\-\*]\s+', text):
        return 'bullet'

    # Check for numbered list markers
    if re.match(r'^\d+[\.\)]\s+', text):
        return 'numbered'

    return None


def detect_unicode_bullets(line: str) -> tuple[bool, str, int]:
    """
    Detect unicode bullet and return bullet info.

    The PDF extraction produces three types of unicode bullets representing hierarchy:
    - ● (U+25CF) - Filled circle - Level 1
    - ○ (U+25CB) - Hollow circle - Level 2
    - ■ (U+25A0) - Filled square - Level 3

    Args:
        line: Text line to analyze

    Returns:
        Tuple of (has_bullet, bullet_char, level):
        - has_bullet: True if line starts with unicode bullet
        - bullet_char: The unicode character found ('●', '○', '■', or '')
        - level: Indentation level (1, 2, 3, or 0 if no bullet)
    """
    stripped = line.lstrip()

    if stripped.startswith('●'):
        return (True, '●', 1)
    elif stripped.startswith('○'):
        return (True, '○', 2)
    elif stripped.startswith('■'):
        return (True, '■', 3)
    else:
        return (False, '', 0)


def convert_unicode_bullet_to_markdown(line: str) -> str:
    """
    Convert a single line with unicode bullet to markdown bullet with proper indentation.

    Conversion rules:
    - ● (filled circle) → - (no indent, level 1)
    - ○ (hollow circle) →   - (2 space indent, level 2)
    - ■ (filled square) →     - (4 space indent, level 3)

    Unicode brackets ˹˺ are preserved as they are content markers, not list markers.

    Args:
        line: Text line that may contain unicode bullet

    Returns:
        Line converted to markdown format with proper indentation

    Examples:
        '● Item' -> '- Item'
        '○ Nested item' -> '  - Nested item'
        '■ Deep nested' -> '    - Deep nested'
        '● ˹Guide˺ operations' -> '- ˹Guide˺ operations'
    """
    has_bullet, bullet_char, level = detect_unicode_bullets(line)

    if not has_bullet:
        return line  # No bullet, return as-is

    # Remove the unicode bullet and any following space
    content = line.lstrip().lstrip('●○■').lstrip()

    # Build markdown bullet with appropriate indentation
    # Level 1: 0 spaces, Level 2: 2 spaces, Level 3: 4 spaces
    indent = '  ' * (level - 1)
    return f"{indent}- {content}"


def convert_document_bullets(content: str) -> str:
    """
    Convert all unicode bullets in document to markdown format.

    Processes entire document, converting unicode bullet characters to standard
    markdown bullets with proper hierarchical indentation while preserving all
    other content including unicode brackets.

    Preserves:
    - Unicode brackets ˹˺ (content markers)
    - Heading structure
    - Non-list content
    - Blank lines and spacing

    Args:
        content: Full document text with unicode bullets

    Returns:
        Document with all unicode bullets converted to markdown format
    """
    lines = content.split('\n')
    result = []

    for line in lines:
        has_bullet, _, _ = detect_unicode_bullets(line)

        if has_bullet:
            converted = convert_unicode_bullet_to_markdown(line)
            result.append(converted)
        else:
            # Not a bullet line - preserve as-is
            result.append(line)

    return '\n'.join(result)


def convert_bullet_to_markdown(text: str) -> str:
    """
    Convert unicode bullet characters to standard markdown bullets.

    DEPRECATED: Use convert_document_bullets() instead for proper hierarchical conversion.

    Args:
        text: Text that may contain unicode bullets

    Returns:
        Text with standard markdown bullets
    """
    # Replace common unicode bullets with markdown hyphen
    text = re.sub(r'^(\s*)[●○•]\s+', r'\1- ', text, flags=re.MULTILINE)

    return text
