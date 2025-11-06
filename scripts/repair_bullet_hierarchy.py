#!/usr/bin/env python3
"""Repair bullet list hierarchy in markdown documents.

This script fixes bullet list indentation and markers to match
semantic hierarchy, using context-aware detection for inconsistent spacing.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.bullet_detection import (
    detect_list_blocks,
    analyze_hierarchy,
    validate_hierarchy
)
from lib.bullet_repair import (
    repair_bullet_list,
    preview_bullet_repair,
    format_repair_summary
)


class BulletRepairReport:
    """Report for bullet list repair operations."""

    def __init__(self, input_file: str):
        self.input_file = input_file
        self.output_file = None
        self.success = False
        self.blocks_found = 0
        self.blocks_repaired = 0
        self.total_items = 0
        self.items_changed = 0
        self.messages = []

    def add_info(self, message: str):
        """Add an info message."""
        self.messages.append(('INFO', message))

    def add_warning(self, message: str):
        """Add a warning message."""
        self.messages.append(('WARN', message))

    def add_error(self, message: str):
        """Add an error message."""
        self.messages.append(('ERROR', message))

    def format(self) -> str:
        """Format report for display."""
        lines = [f"\nBullet Repair Report: {Path(self.input_file).name}"]
        lines.append(f"Status: {'SUCCESS' if self.success else 'FAILED'}")

        if self.output_file:
            lines.append(f"Output: {self.output_file}")

        lines.append(f"\nStatistics:")
        lines.append(f"  List blocks found: {self.blocks_found}")
        lines.append(f"  Blocks repaired: {self.blocks_repaired}")
        lines.append(f"  Total items: {self.total_items}")
        lines.append(f"  Items changed: {self.items_changed}")

        if self.messages:
            lines.append(f"\nMessages:")
            for level, msg in self.messages:
                prefix = f"  [{level}]"
                lines.append(f"{prefix} {msg}")

        return '\n'.join(lines)


def load_document(file_path: Path) -> List[str]:
    """Load document lines from file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()


def save_document(file_path: Path, lines: List[str]):
    """Save document lines to file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def repair_document_bullets(
    input_path: Path,
    output_path: Optional[Path] = None,
    spaces_per_level: int = 2,
    max_depth: Optional[int] = 4,
    dry_run: bool = False
) -> BulletRepairReport:
    """Repair bullet list hierarchy in a document.

    Args:
        input_path: Input markdown file
        output_path: Output file (None = overwrite input)
        spaces_per_level: Spaces per indentation level
        max_depth: Maximum nesting depth (None = no limit)
        dry_run: If True, preview only

    Returns:
        BulletRepairReport with results
    """
    report = BulletRepairReport(input_file=str(input_path))

    try:
        # Load document
        lines = load_document(input_path)
        report.add_info(f"Loaded {len(lines)} lines")

        # Detect list blocks
        blocks = detect_list_blocks(lines)
        report.blocks_found = len(blocks)
        report.add_info(f"Found {len(blocks)} bullet list blocks")

        if len(blocks) == 0:
            report.add_info("No bullet lists found - nothing to repair")
            report.success = True
            return report

        # Process each block
        result_lines = lines.copy()
        total_items = 0
        total_changed = 0

        for block_idx, (start, end) in enumerate(blocks):
            # Extract block
            block_lines = lines[start:end + 1]

            # Analyze hierarchy
            hierarchy = analyze_hierarchy(block_lines)
            warnings = validate_hierarchy(hierarchy)

            if warnings:
                report.add_warning(f"Block {block_idx + 1} (lines {start}-{end}):")
                for warning in warnings:
                    report.add_warning(f"  {warning}")

            # Repair block
            repaired_block, stats = repair_bullet_list(
                block_lines,
                spaces_per_level=spaces_per_level,
                max_depth=max_depth
            )

            total_items += stats.get('original_items', 0)
            total_changed += stats.get('indents_changed', 0) + stats.get('markers_changed', 0)

            # Show sample of changes
            if block_idx < 3:  # Show first 3 blocks
                changes = preview_bullet_repair(block_lines, spaces_per_level, max_depth)
                if changes:
                    report.add_info(f"Block {block_idx + 1} repairs (showing first 3):")
                    for i, (line_idx, old, new) in enumerate(changes[:3]):
                        report.add_info(f"  Line {start + line_idx}: {old[:50]} -> {new[:50]}")
                    if len(changes) > 3:
                        report.add_info(f"  ... and {len(changes) - 3} more changes")

            # Update result
            result_lines[start:end + 1] = repaired_block

        report.blocks_repaired = len(blocks)
        report.total_items = total_items
        report.items_changed = total_changed

        if dry_run:
            report.add_info("DRY RUN: No changes written")
            report.success = True
            return report

        # Save output
        if output_path is None:
            output_path = input_path

        save_document(output_path, result_lines)
        report.output_file = str(output_path)
        report.add_info(f"Saved repaired document to {output_path}")

        report.success = True

    except Exception as e:
        report.add_error(f"Failed to repair bullets: {e}")
        report.success = False

    return report


def process_directory(
    input_dir: Path,
    output_dir: Path,
    pattern: str = "chapter_*.md",
    spaces_per_level: int = 2,
    max_depth: Optional[int] = 4,
    dry_run: bool = False,
    verbose: bool = False
) -> List[BulletRepairReport]:
    """Process all matching files in a directory."""
    reports = []

    # Find all matching files
    files = sorted(input_dir.glob(pattern))

    if not files:
        print(f"No files matching '{pattern}' found in {input_dir}")
        return reports

    print(f"Processing {len(files)} files from {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Spacing: {spaces_per_level} spaces per level")
    if max_depth:
        print(f"Max depth: {max_depth} levels")

    if dry_run:
        print("DRY RUN MODE - No changes will be written\n")

    for file_path in files:
        output_path = output_dir / file_path.name

        print(f"\nProcessing: {file_path.name}")

        report = repair_document_bullets(
            file_path,
            output_path,
            spaces_per_level=spaces_per_level,
            max_depth=max_depth,
            dry_run=dry_run
        )

        reports.append(report)

        if verbose or not report.success:
            print(report.format())

    return reports


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Repair bullet list hierarchy in markdown documents"
    )

    parser.add_argument(
        '--chapter',
        type=str,
        help='Process a single chapter file (e.g., chapter_01.md)'
    )

    parser.add_argument(
        '--input-dir',
        type=Path,
        default=Path('output/chapters/05_repaired'),
        help='Input directory (default: output/chapters/05_repaired)'
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('output/chapters/05_repaired'),
        help='Output directory (default: output/chapters/05_repaired)'
    )

    parser.add_argument(
        '--pattern',
        type=str,
        default='chapter_*.md',
        help='File pattern to match (default: chapter_*.md)'
    )

    parser.add_argument(
        '--base-indent',
        type=int,
        default=2,
        help='Base indentation in spaces (default: 2)'
    )

    parser.add_argument(
        '--max-depth',
        type=int,
        default=4,
        help='Maximum nesting depth (default: 4, 0=unlimited)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without writing files'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed processing information'
    )

    args = parser.parse_args()

    # Handle max-depth=0 as unlimited
    max_depth = None if args.max_depth == 0 else args.max_depth

    # Process single chapter or directory
    if args.chapter:
        input_path = args.input_dir / args.chapter
        output_path = args.output_dir / args.chapter

        if not input_path.exists():
            print(f"Error: File not found: {input_path}")
            sys.exit(1)

        print(f"Processing: {input_path}")

        report = repair_document_bullets(
            input_path,
            output_path,
            spaces_per_level=args.base_indent,
            max_depth=max_depth,
            dry_run=args.dry_run
        )

        print(report.format())
        sys.exit(0 if report.success else 1)

    else:
        # Process directory
        reports = process_directory(
            args.input_dir,
            args.output_dir,
            pattern=args.pattern,
            spaces_per_level=args.base_indent,
            max_depth=max_depth,
            dry_run=args.dry_run,
            verbose=args.verbose
        )

        # Summary
        success_count = sum(1 for r in reports if r.success)
        total_blocks = sum(r.blocks_found for r in reports)
        total_items = sum(r.total_items for r in reports)
        total_changed = sum(r.items_changed for r in reports)

        print(f"\n{'='*60}")
        print(f"Summary:")
        print(f"  Files processed: {success_count}/{len(reports)}")
        print(f"  Total list blocks: {total_blocks}")
        print(f"  Total list items: {total_items}")
        print(f"  Items changed: {total_changed}")

        if success_count < len(reports):
            print("\nFailed files:")
            for report in reports:
                if not report.success:
                    print(f"  - {Path(report.input_file).name}")

        sys.exit(0 if success_count == len(reports) else 1)


if __name__ == '__main__':
    main()
