#!/usr/bin/env python3
"""
Markdown parser for extracting section hierarchy and content.
"""

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class Section:
    """Represents a markdown section with metadata."""
    id: str
    heading: str
    level: int
    line_start: int
    line_end: int
    content: str
    parent_id: Optional[str] = None
    subsections: List[str] = None

    def __post_init__(self):
        if self.subsections is None:
            self.subsections = []

    @property
    def line_count(self) -> int:
        """Number of lines in this section."""
        return self.line_end - self.line_start + 1

    @property
    def token_estimate(self) -> int:
        """Rough token estimate (4 chars per token average)."""
        return len(self.content) // 4


class MarkdownParser:
    """Parse markdown files and extract section hierarchy."""

    HEADING_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$')

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lines = []
        self.sections = []

    def parse(self) -> List[Section]:
        """Parse markdown file and return list of sections."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

        # Find all headings
        headings = []
        for i, line in enumerate(self.lines):
            match = self.HEADING_PATTERN.match(line.strip())
            if match:
                level = len(match.group(1))
                heading_text = match.group(2).strip()
                headings.append((i, level, heading_text))

        # Build sections
        for idx, (line_num, level, heading_text) in enumerate(headings):
            # Determine section end (next heading of same or higher level, or EOF)
            end_line = len(self.lines) - 1
            for next_line, next_level, _ in headings[idx + 1:]:
                if next_level <= level:
                    end_line = next_line - 1
                    break

            # Extract content
            content_lines = self.lines[line_num:end_line + 1]
            content = ''.join(content_lines)

            # Generate section ID
            section_id = self._generate_section_id(idx, level, headings[:idx + 1])

            # Find parent
            parent_id = self._find_parent_id(idx, level, headings[:idx])

            section = Section(
                id=section_id,
                heading=heading_text,
                level=level,
                line_start=line_num + 1,  # 1-indexed
                line_end=end_line + 1,     # 1-indexed
                content=content,
                parent_id=parent_id
            )

            self.sections.append(section)

        # Build subsection relationships
        self._build_subsection_tree()

        return self.sections

    def _generate_section_id(self, idx: int, level: int,
                            prev_headings: List[Tuple[int, int, str]]) -> str:
        """Generate hierarchical section ID (e.g., '1.2.3')."""
        # Count sections at each level up to this point
        level_counts = {i: 0 for i in range(1, 7)}

        for _, prev_level, _ in prev_headings:
            if prev_level <= level:
                level_counts[prev_level] += 1
                # Reset deeper levels when we encounter a higher-level heading
                if prev_level < level:
                    for deeper in range(prev_level + 1, 7):
                        level_counts[deeper] = 0

        # Build ID from level counts
        id_parts = []
        for lvl in range(1, level + 1):
            id_parts.append(str(level_counts[lvl]))

        return '.'.join(id_parts)

    def _find_parent_id(self, idx: int, level: int,
                        prev_headings: List[Tuple[int, int, str]]) -> Optional[str]:
        """Find parent section ID (previous heading of lower level)."""
        if level == 1:
            return None

        # Search backwards for first heading with level < current level
        for i in range(len(prev_headings) - 1, -1, -1):
            _, prev_level, _ = prev_headings[i]
            if prev_level < level:
                # Found parent, return its ID
                return self._generate_section_id(i, prev_level, prev_headings[:i + 1])

        return None

    def _build_subsection_tree(self):
        """Populate subsections lists for each section."""
        for section in self.sections:
            # Find all sections with this section as parent
            children = [s.id for s in self.sections if s.parent_id == section.id]
            section.subsections = children

    def get_section_by_id(self, section_id: str) -> Optional[Section]:
        """Retrieve section by ID."""
        for section in self.sections:
            if section.id == section_id:
                return section
        return None

    def get_major_sections(self, max_level: int = 2) -> List[Section]:
        """Get top-level sections up to max_level."""
        return [s for s in self.sections if s.level <= max_level]

    def get_subsections(self, section_id: str) -> List[Section]:
        """Get all subsections of a given section."""
        parent = self.get_section_by_id(section_id)
        if not parent:
            return []

        return [self.get_section_by_id(sid) for sid in parent.subsections]
