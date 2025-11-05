"""
PDF utilities for extracting text and structure from PDF documents.
Preserves unicode characters and detects document structure.
"""

import pdfplumber
from typing import List, Dict, Tuple, Optional
import re


def extract_text_by_page(pdf_path: str, start_page: Optional[int] = None,
                         end_page: Optional[int] = None) -> List[Dict[str, any]]:
    """
    Extract text from PDF pages with metadata.

    Args:
        pdf_path: Path to the PDF file
        start_page: Starting page number (0-indexed), None for first page
        end_page: Ending page number (0-indexed), None for last page

    Returns:
        List of dictionaries containing page number and extracted text
    """
    pages_data = []

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        start = start_page if start_page is not None else 0
        end = end_page if end_page is not None else total_pages - 1

        for page_num in range(start, min(end + 1, total_pages)):
            page = pdf.pages[page_num]
            text = page.extract_text()

            if text:
                pages_data.append({
                    'page_number': page_num,
                    'text': text,
                    'width': page.width,
                    'height': page.height
                })

    return pages_data


def detect_headings(text: str, page_num: int = 0) -> List[Dict[str, any]]:
    """
    Detect potential headings in text based on common patterns.

    Args:
        text: Text content to analyze
        page_num: Page number for context

    Returns:
        List of detected headings with metadata
    """
    headings = []
    lines = text.split('\n')

    for i, line in enumerate(lines):
        line_stripped = line.strip()

        # Skip empty lines
        if not line_stripped:
            continue

        # Pattern 1: All caps (potential heading)
        if line_stripped.isupper() and len(line_stripped) > 2:
            headings.append({
                'text': line_stripped,
                'line_number': i,
                'page_number': page_num,
                'type': 'all_caps',
                'confidence': 0.8
            })
            continue

        # Pattern 2: Numbered sections (e.g., "1. Introduction", "1.1 Overview")
        numbered_pattern = r'^(\d+\.)+\s+(.+)$'
        match = re.match(numbered_pattern, line_stripped)
        if match:
            headings.append({
                'text': line_stripped,
                'line_number': i,
                'page_number': page_num,
                'type': 'numbered',
                'confidence': 0.9,
                'number': match.group(1)
            })
            continue

        # Pattern 3: Short lines followed by blank line (potential heading)
        if (len(line_stripped) < 80 and
            len(line_stripped) > 2 and
            i + 1 < len(lines) and
            not lines[i + 1].strip()):
            headings.append({
                'text': line_stripped,
                'line_number': i,
                'page_number': page_num,
                'type': 'short_line',
                'confidence': 0.6
            })

    return headings


def preserve_unicode(text: str) -> str:
    """
    Ensure unicode characters (especially brackets) are preserved.

    Args:
        text: Text that may contain unicode characters

    Returns:
        Text with unicode characters preserved
    """
    # Ensure text is properly encoded as UTF-8
    # This function primarily serves as a validation/passthrough
    # to ensure unicode characters are not corrupted during processing

    if not isinstance(text, str):
        text = str(text)

    # Common unicode brackets that need preservation:
    # 〔 (U+3014) LEFT TORTOISE SHELL BRACKET
    # 〕 (U+3015) RIGHT TORTOISE SHELL BRACKET
    # 【 (U+3010) LEFT BLACK LENTICULAR BRACKET
    # 】 (U+3011) RIGHT BLACK LENTICULAR BRACKET
    # 「 (U+300C) LEFT CORNER BRACKET
    # 」 (U+300D) RIGHT CORNER BRACKET

    return text


def extract_chapter(pdf_path: str, chapter_name: str,
                    start_page: Optional[int] = None,
                    end_page: Optional[int] = None) -> Dict[str, any]:
    """
    Extract a specific chapter from the PDF.

    Args:
        pdf_path: Path to the PDF file
        chapter_name: Name/identifier of the chapter
        start_page: Starting page number (0-indexed)
        end_page: Ending page number (0-indexed)

    Returns:
        Dictionary with chapter metadata and content
    """
    pages = extract_text_by_page(pdf_path, start_page, end_page)

    # Combine all page texts with page separators
    full_text = ""
    for page in pages:
        full_text += page['text'] + "\n\n"

    # Preserve unicode characters
    full_text = preserve_unicode(full_text)

    # Detect headings across all pages
    all_headings = []
    for page in pages:
        headings = detect_headings(page['text'], page['page_number'])
        all_headings.extend(headings)

    return {
        'chapter_name': chapter_name,
        'start_page': start_page,
        'end_page': end_page,
        'pages': pages,
        'full_text': full_text,
        'headings': all_headings,
        'page_count': len(pages)
    }


def find_chapter_boundaries(pdf_path: str) -> List[Dict[str, any]]:
    """
    Attempt to automatically detect chapter boundaries in the PDF.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        List of detected chapters with start/end page numbers
    """
    chapters = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue

            # Look for chapter markers
            # Common patterns: "Chapter N", "CHAPTER N", "Section N"
            chapter_pattern = r'^(CHAPTER|Chapter|SECTION|Section)\s+(\d+|[IVXLCDM]+)'

            lines = text.split('\n')
            for line in lines[:5]:  # Check first 5 lines of page
                match = re.search(chapter_pattern, line.strip())
                if match:
                    chapters.append({
                        'chapter_marker': line.strip(),
                        'page_number': page_num,
                        'chapter_type': match.group(1),
                        'chapter_number': match.group(2)
                    })
                    break

    # Add end page numbers
    for i, chapter in enumerate(chapters):
        if i + 1 < len(chapters):
            chapter['end_page'] = chapters[i + 1]['page_number'] - 1
        else:
            chapter['end_page'] = None  # Last chapter goes to end

    return chapters
