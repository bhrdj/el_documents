#!/usr/bin/env python3
"""
Reformat a raw chapter to match the established formatting template.

This script takes a raw chapter extracted from the PDF and applies
the formatting rules documented in formatting-guide.md to produce
clean vanilla markdown output.

Key transformations:
- Convert unicode bullets (●○■) to hierarchical markdown bullets
- Apply consistent heading formatting
- Clean up page markers and footers
- Apply spacing rules
- Preserve unicode brackets ˹˺

Pipeline Integration:
- Input: output/chapters/00_raw/ (raw PDF extraction)
- Output: output/chapters/02_removedbullets/ (default) or specified stage

Usage:
    .venv/bin/python scripts/reformat_manual/reformat_chapter.py <chapter_number>
    .venv/bin/python scripts/reformat_manual/reformat_chapter.py 0
    .venv/bin/python scripts/reformat_manual/reformat_chapter.py 2
    .venv/bin/python scripts/reformat_manual/reformat_chapter.py 5 03_nextstage
"""

import sys
import re
from pathlib import Path
from typing import Optional

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.markdown_utils import (
    convert_document_bullets,
    apply_spacing_rules,
    apply_heading_format,
)


def remove_page_markers(content: str) -> str:
    """
    Remove PDF page markers and footers.

    Removes:
    - "Page X of XX" markers
    - "EL_CgManual_CURRENT_v016 November 5, 2025" footers
    - Duplicate chapter headings on pages

    Args:
        content: Raw chapter text

    Returns:
        Content with page markers removed
    """
    lines = content.split('\n')
    cleaned = []

    for line in lines:
        # Skip page markers
        if re.match(r'.*Page \d+ of [X\d]+', line):
            continue

        # Skip footer lines with manual version
        if 'EL_CgManual_CURRENT_v' in line:
            continue

        cleaned.append(line)

    return '\n'.join(cleaned)


def remove_duplicate_chapter_headings(content: str, chapter_num: int) -> str:
    """
    Remove duplicate chapter headings that appear on multiple pages.

    Keeps only the first occurrence of the chapter heading.

    Args:
        content: Chapter text
        chapter_num: Chapter number

    Returns:
        Content with duplicate headings removed
    """
    lines = content.split('\n')

    # Pattern to match chapter headings
    chapter_patterns = [
        rf'^CHAPTER {chapter_num}[:\.].*',
        rf'^{chapter_num}\.\s+[A-Z\s]+',
    ]

    seen_main_heading = False
    cleaned = []

    for line in lines:
        # Check if this is a chapter heading
        is_chapter_heading = any(re.match(pattern, line.strip(), re.IGNORECASE)
                                  for pattern in chapter_patterns)

        if is_chapter_heading:
            if not seen_main_heading:
                # Keep the first occurrence
                cleaned.append(line)
                seen_main_heading = True
            # else: skip duplicate heading
        else:
            cleaned.append(line)

    return '\n'.join(cleaned)


def normalize_headings(content: str) -> str:
    """
    Normalize heading format to match the template.

    Ensures headings have:
    - Proper markdown # prefix based on numbering depth
    - Single blank line before and after
    - Consistent formatting

    Args:
        content: Chapter text

    Returns:
        Content with normalized headings
    """
    lines = content.split('\n')
    result = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Detect numbered headings (e.g., "2.1.3 Title" or "2.1.3.4 Title")
        heading_match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+)', stripped)

        if heading_match:
            numbering = heading_match.group(1)
            title = heading_match.group(2)

            # Count depth: "2" = 1, "2.1" = 2, "2.1.3" = 3
            depth = numbering.count('.') + 1

            # Clamp to valid heading levels (1-6)
            level = min(depth, 6)

            # Format as markdown heading
            formatted = apply_heading_format(f"{numbering} {title}", level)

            # Ensure blank line before heading (if not first line)
            if i > 0 and result and result[-1].strip():
                result.append('')

            result.append(formatted.rstrip())

            # Add blank line after heading
            if i < len(lines) - 1:
                result.append('')
        else:
            result.append(line)

    return '\n'.join(result)


def clean_list_spacing(content: str) -> str:
    """
    Clean up spacing around lists.

    Ensures:
    - Single blank line before list blocks
    - Single blank line after list blocks
    - No blank lines between list items

    Args:
        content: Chapter text

    Returns:
        Content with cleaned list spacing
    """
    lines = content.split('\n')
    result = []
    in_list = False
    prev_was_blank = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        is_list_item = stripped.startswith('-') or stripped.startswith('  -') or stripped.startswith('    -')
        is_blank = not stripped

        if is_list_item:
            if not in_list and result and not prev_was_blank:
                # Add blank line before list starts
                result.append('')
            in_list = True
            result.append(line)
            prev_was_blank = False
        elif in_list and is_blank:
            # Blank line within or after list
            # Peek ahead to see if list continues
            next_is_list = False
            if i + 1 < len(lines):
                next_stripped = lines[i + 1].strip()
                next_is_list = next_stripped.startswith('-') or next_stripped.startswith('  -') or next_stripped.startswith('    -')

            if next_is_list:
                # Skip blank line within list
                pass
            else:
                # End of list - add blank line after
                result.append('')
                in_list = False
                prev_was_blank = True
        else:
            in_list = False
            result.append(line)
            prev_was_blank = is_blank

    return '\n'.join(result)


def reformat_chapter(raw_file: Path, output_file: Path) -> None:
    """
    Reformat a raw chapter to match the formatting template.

    Args:
        raw_file: Path to raw chapter file
        output_file: Path to output reformatted chapter

    Raises:
        FileNotFoundError: If raw_file doesn't exist
    """
    if not raw_file.exists():
        raise FileNotFoundError(f"Raw chapter file not found: {raw_file}")

    # Read raw content
    print(f"Reading raw chapter: {raw_file}")
    content = raw_file.read_text(encoding='utf-8')

    # Extract chapter number from filename (e.g., "chapter_2.md" -> 2)
    chapter_num_match = re.search(r'chapter_(\d+)', raw_file.name)
    chapter_num = int(chapter_num_match.group(1)) if chapter_num_match else 0

    print(f"Processing chapter {chapter_num}...")

    # Step 1: Remove PDF artifacts
    print("  - Removing page markers and footers")
    content = remove_page_markers(content)
    content = remove_duplicate_chapter_headings(content, chapter_num)

    # Step 2: Convert unicode bullets to markdown
    print("  - Converting unicode bullets to hierarchical markdown")
    content = convert_document_bullets(content)

    # Step 3: Normalize headings
    print("  - Normalizing heading format")
    content = normalize_headings(content)

    # Step 4: Clean up list spacing
    print("  - Cleaning list spacing")
    content = clean_list_spacing(content)

    # Step 5: Apply general spacing rules
    print("  - Applying spacing rules")
    content = apply_spacing_rules(content)

    # Write output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(content, encoding='utf-8')
    print(f"✓ Reformatted chapter written to: {output_file}")

    # Report statistics
    lines = content.split('\n')
    bullet_count = sum(1 for line in lines if line.strip().startswith('-'))
    heading_count = sum(1 for line in lines if line.strip().startswith('#'))

    print(f"  Statistics: {heading_count} headings, {bullet_count} list items")


def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: reformat_chapter.py <chapter_number> [output_stage]")
        print("Example: reformat_chapter.py 2")
        print("Example: reformat_chapter.py 2 03_nextprocess")
        sys.exit(1)

    chapter_arg = sys.argv[1]
    output_stage = sys.argv[2] if len(sys.argv) > 2 else "02_removedbullets"

    # Determine paths - using versioned pipeline structure
    repo_root = Path(__file__).parent.parent.parent
    raw_dir = repo_root / "output" / "chapters" / "00_raw"
    output_dir = repo_root / "output" / "chapters" / output_stage

    # Handle chapter naming variations
    # Try different naming patterns: chapter_N.md, chapter_N_partM.md
    raw_files = list(raw_dir.glob(f"chapter_{chapter_arg}*.md"))

    if not raw_files:
        print(f"Error: No raw chapter file found for chapter {chapter_arg}")
        print(f"Looked in: {raw_dir}")
        sys.exit(1)

    # Process each matching file
    for raw_file in raw_files:
        # Generate output filename
        if "part" in raw_file.name:
            # Keep part designation: chapter_5_part1.md -> chapter_05_part1.md
            output_name = raw_file.name.replace(f"chapter_{chapter_arg}", f"chapter_{chapter_arg.zfill(2)}")
        else:
            # Simple chapter: chapter_2.md -> chapter_02.md
            output_name = f"chapter_{chapter_arg.zfill(2)}.md"

        output_file = output_dir / output_name

        try:
            reformat_chapter(raw_file, output_file)
        except Exception as e:
            print(f"Error processing {raw_file}: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
