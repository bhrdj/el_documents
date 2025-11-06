#!/usr/bin/env python3
"""
Document entity class for document structure repair.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional


class Document:
    """
    Represents a single markdown chapter file being processed.

    Attributes:
        file_path: Absolute path to the markdown file
        chapter_number: Chapter number (0-9)
        content: Full markdown content as text
        lines: Content split into lines for line-by-line processing
        sections: Hierarchical sections detected in document
        metadata: Document metadata (title, stage, etc.)
    """

    def __init__(self, file_path: Path, chapter_number: Optional[int] = None):
        """
        Initialize a Document from a file path.

        Args:
            file_path: Path to the markdown file
            chapter_number: Optional chapter number (0-9), auto-detected if not provided

        Raises:
            FileNotFoundError: If file_path does not exist
            ValueError: If file is not readable or chapter_number invalid
        """
        self.file_path = Path(file_path).resolve()

        if not self.file_path.exists():
            raise FileNotFoundError(f"Document file not found: {self.file_path}")

        if not self.file_path.is_file():
            raise ValueError(f"Path is not a file: {self.file_path}")

        # Auto-detect chapter number from filename if not provided
        if chapter_number is None:
            chapter_number = self._extract_chapter_number()

        if chapter_number is not None and not (0 <= chapter_number <= 9):
            raise ValueError(f"Chapter number must be 0-9, got: {chapter_number}")

        self.chapter_number = chapter_number

        # Load content
        try:
            self.content = self.file_path.read_text(encoding='utf-8')
        except Exception as e:
            raise ValueError(f"Failed to read file {self.file_path}: {e}")

        self.lines = self.content.split('\n')
        self.sections = []
        self.metadata = {}

    def _extract_chapter_number(self) -> Optional[int]:
        """
        Extract chapter number from filename like 'chapter_05.md' or 'chapter_5.md'.

        Returns:
            Chapter number (0-9) or None if not found
        """
        import re
        filename = self.file_path.name
        match = re.search(r'chapter[_\s]?(\d+)', filename, re.IGNORECASE)
        if match:
            num = int(match.group(1))
            if 0 <= num <= 9:
                return num
        return None

    def save(self, output_path: Path) -> None:
        """
        Save the document to a new location.

        Args:
            output_path: Path where to save the document
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Reconstruct content from lines
        output_content = '\n'.join(self.lines)
        output_path.write_text(output_content, encoding='utf-8')

    def __repr__(self) -> str:
        return f"Document(chapter={self.chapter_number}, path={self.file_path.name}, lines={len(self.lines)})"

    def __str__(self) -> str:
        return f"Chapter {self.chapter_number}: {self.file_path.name} ({len(self.lines)} lines, {len(self.sections)} sections)"
