#!/usr/bin/env python3
"""
Content comparison module for detecting missing content in Chapter 5.
"""

import hashlib
import re
from typing import List, Dict, Tuple, Set
from .parser import is_header, extract_section_number


class ContentBlock:
    """
    Represents a block of content for comparison.

    Attributes:
        type: Block type ('section', 'paragraph', 'list', 'other')
        line_start: Starting line number
        line_end: Ending line number
        content: Actual content text
        fingerprint: Unique fingerprint for comparison
        section_number: Section number if applicable
    """

    def __init__(
        self,
        block_type: str,
        line_start: int,
        line_end: int,
        content: str,
        section_number: str = ""
    ):
        """
        Initialize a ContentBlock.

        Args:
            block_type: Type of content block
            line_start: Starting line number
            line_end: Ending line number
            content: Content text
            section_number: Section number if this is a section header
        """
        self.type = block_type
        self.line_start = line_start
        self.line_end = line_end
        self.content = content
        self.section_number = section_number
        self.fingerprint = self.create_content_fingerprint(content)

    @staticmethod
    def create_content_fingerprint(content: str) -> str:
        """
        Create a unique fingerprint for content comparison.

        Uses first 50 chars + hash of full content.

        Args:
            content: Content to fingerprint

        Returns:
            Fingerprint string
        """
        # Normalize: strip whitespace, lowercase, remove extra spaces
        normalized = ' '.join(content.strip().lower().split())

        # Use first 50 chars as preview
        preview = normalized[:50]

        # Hash full content for uniqueness
        content_hash = hashlib.md5(normalized.encode()).hexdigest()[:8]

        return f"{preview}|{content_hash}"

    def matches(self, other: 'ContentBlock') -> bool:
        """
        Check if this block matches another block.

        Args:
            other: Another ContentBlock to compare

        Returns:
            True if blocks match, False otherwise
        """
        return self.fingerprint == other.fingerprint

    def __repr__(self) -> str:
        return f"ContentBlock({self.type}, lines={self.line_start}-{self.line_end}, preview={self.content[:30]}...)"


def parse_content_blocks(lines: List[str]) -> List[ContentBlock]:
    """
    Parse document lines into content blocks.

    Args:
        lines: Document lines

    Returns:
        List of ContentBlock objects
    """
    blocks = []
    current_block_lines = []
    current_block_start = 0
    current_block_type = 'other'

    for i, line in enumerate(lines):
        # Check if this is a section header
        if is_header(line):
            # Save previous block if exists
            if current_block_lines:
                content = '\n'.join(current_block_lines)
                blocks.append(ContentBlock(
                    current_block_type,
                    current_block_start,
                    i - 1,
                    content
                ))

            # Start new section block
            section_num, title = extract_section_number(line)
            blocks.append(ContentBlock(
                'section',
                i,
                i,
                line.strip(),
                section_num or ""
            ))

            current_block_lines = []
            current_block_start = i + 1
            current_block_type = 'other'

        elif line.strip() == '':
            # Empty line - potential block boundary
            if current_block_lines:
                content = '\n'.join(current_block_lines)
                blocks.append(ContentBlock(
                    current_block_type,
                    current_block_start,
                    i - 1,
                    content
                ))
                current_block_lines = []
                current_block_start = i + 1

        else:
            # Content line - add to current block
            current_block_lines.append(line)

    # Add final block
    if current_block_lines:
        content = '\n'.join(current_block_lines)
        blocks.append(ContentBlock(
            current_block_type,
            current_block_start,
            len(lines) - 1,
            content
        ))

    return blocks


def find_missing_content(
    source_blocks: List[ContentBlock],
    target_blocks: List[ContentBlock]
) -> Tuple[List[ContentBlock], Set[str]]:
    """
    Find content blocks from source that are missing in target.

    Args:
        source_blocks: Blocks from source document(s)
        target_blocks: Blocks from target document

    Returns:
        Tuple of (missing_blocks, target_fingerprints)
    """
    # Create fingerprint set for target blocks
    target_fingerprints = {block.fingerprint for block in target_blocks}

    # Find source blocks not in target
    missing_blocks = [
        block for block in source_blocks
        if block.fingerprint not in target_fingerprints
    ]

    return (missing_blocks, target_fingerprints)


def merge_source_blocks(
    part1_blocks: List[ContentBlock],
    part2_blocks: List[ContentBlock]
) -> List[ContentBlock]:
    """
    Merge blocks from two source parts, removing duplicates.

    Args:
        part1_blocks: Blocks from part 1
        part2_blocks: Blocks from part 2

    Returns:
        Merged list of unique blocks
    """
    # Use fingerprints to detect duplicates
    seen_fingerprints = set()
    merged_blocks = []

    for block in part1_blocks + part2_blocks:
        if block.fingerprint not in seen_fingerprints:
            seen_fingerprints.add(block.fingerprint)
            merged_blocks.append(block)

    return merged_blocks


def create_analysis_report(
    part1_blocks: List[ContentBlock],
    part2_blocks: List[ContentBlock],
    merged_blocks: List[ContentBlock],
    missing_blocks: List[ContentBlock]
) -> str:
    """
    Create a markdown analysis report.

    Args:
        part1_blocks: Blocks from part 1
        part2_blocks: Blocks from part 2
        merged_blocks: Blocks from current merged file
        missing_blocks: Missing blocks detected

    Returns:
        Markdown formatted report
    """
    lines = []
    lines.append("# Chapter 5 Content Analysis")
    lines.append("\n## Source Analysis\n")
    lines.append(f"- **Part 1 Blocks**: {len(part1_blocks)}")
    lines.append(f"- **Part 2 Blocks**: {len(part2_blocks)}")
    lines.append(f"- **Total Source Blocks**: {len(part1_blocks) + len(part2_blocks)}")
    lines.append(f"\n- **Current Merged Blocks**: {len(merged_blocks)}")
    lines.append(f"\n- **Missing Blocks**: {len(missing_blocks)}")

    # Status
    if len(missing_blocks) == 0:
        lines.append(f"\n**Status**: ✓ COMPLETE - All source content present in merged file")
    else:
        lines.append(f"\n**Status**: ⚠ INCOMPLETE - {len(missing_blocks)} blocks missing from merged file")

    # List missing content if any
    if missing_blocks:
        lines.append(f"\n## Missing Content Details\n")
        for i, block in enumerate(missing_blocks, 1):
            lines.append(f"\n### Missing Block {i}")
            lines.append(f"- **Type**: {block.type}")
            lines.append(f"- **Section**: {block.section_number or 'N/A'}")
            lines.append(f"- **Preview**: {block.content[:100]}...")

    lines.append(f"\n## Recommendations\n")
    if missing_blocks:
        lines.append("- Run with `--restore` flag to automatically restore missing content")
        lines.append("- Review restored content to ensure proper placement")
    else:
        lines.append("- No action needed - Chapter 5 is complete")

    return '\n'.join(lines)
