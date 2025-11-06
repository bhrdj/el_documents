#!/usr/bin/env python3
"""Repair section numbering in markdown documents.

This script applies consistent hierarchical section numbering across
markdown documents, fixing gaps, duplicates, and sequence breaks.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Optional
import re

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.section_numbering import (
    SectionNumberer,
    renumber_document_headers,
    preview_renumbering,
    get_header_level
)
from lib.document import Document


class SimpleReport:
    """Simple processing report for section numbering repairs."""

    def __init__(self, input_file: str):
        self.input_file = input_file
        self.output_file = None
        self.success = False
        self.messages = []

    def add_info(self, message: str):
        """Add an info message."""
        self.messages.append(('INFO', message))

    def add_error(self, message: str):
        """Add an error message."""
        self.messages.append(('ERROR', message))

    def format(self) -> str:
        """Format report for display."""
        lines = [f"\nReport for: {self.input_file}"]
        lines.append(f"Status: {'SUCCESS' if self.success else 'FAILED'}")
        if self.output_file:
            lines.append(f"Output: {self.output_file}")
        lines.append("\nMessages:")
        for level, msg in self.messages:
            prefix = "  [INFO] " if level == 'INFO' else "  [ERROR]"
            lines.append(f"{prefix} {msg}")
        return '\n'.join(lines)


class CrossReferenceManager:
    """Manage cross-references during section renumbering.

    Detects internal links and updates them when section numbers change.
    """

    def __init__(self):
        self.section_map: Dict[str, str] = {}  # old_number -> new_number
        self.title_map: Dict[str, str] = {}    # section_title -> new_number

    def record_renumbering(self, old_header: str, new_header: str, section_title: str):
        """Record a section renumbering for cross-reference updates.

        Args:
            old_header: Original header line
            new_header: New header line
            section_title: Section title (without number)
        """
        # Extract old number
        old_number = self._extract_number(old_header)
        new_number = self._extract_number(new_header)

        if old_number:
            self.section_map[old_number] = new_number

        self.title_map[section_title.lower().strip()] = new_number

    def _extract_number(self, header: str) -> str:
        """Extract section number from header line."""
        # Remove leading # and whitespace
        stripped = header.lstrip('#').strip()

        # Match section number at start
        match = re.match(r'^(\d+(?:\.\d+)*)', stripped)
        if match:
            return match.group(1)
        return ""

    def update_references(self, lines: List[str]) -> List[str]:
        """Update cross-references in document lines.

        Args:
            lines: Document lines

        Returns:
            Lines with updated references
        """
        result = []

        for line in lines:
            updated_line = line

            # Update markdown links: [text](#section-123)
            # Pattern: [text](#section-X.Y.Z) or [text](#X.Y.Z)
            for old_num, new_num in self.section_map.items():
                # Try various anchor formats
                old_formats = [
                    f"#section-{old_num}",
                    f"#{old_num}",
                    f"#section{old_num.replace('.', '')}",
                ]
                new_anchor = f"#section-{new_num}"

                for old_fmt in old_formats:
                    updated_line = updated_line.replace(old_fmt, new_anchor)

            # Update text references: "see section 1.2.3"
            for old_num, new_num in self.section_map.items():
                # Case-insensitive replacement
                pattern = re.compile(re.escape(old_num), re.IGNORECASE)
                # Only replace if surrounded by section-like context
                if 'section' in updated_line.lower() or 'see' in updated_line.lower():
                    updated_line = pattern.sub(new_num, updated_line)

            result.append(updated_line)

        return result


def load_document(file_path: Path) -> List[str]:
    """Load document lines from file.

    Args:
        file_path: Path to markdown file

    Returns:
        List of lines (with newlines preserved)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()


def save_document(file_path: Path, lines: List[str]):
    """Save document lines to file.

    Args:
        file_path: Path to save to
        lines: Lines to write
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def repair_document_numbering(
    input_path: Path,
    output_path: Optional[Path] = None,
    preserve_references: bool = True,
    dry_run: bool = False
) -> SimpleReport:
    """Repair section numbering in a document.

    Args:
        input_path: Input markdown file
        output_path: Output file (None = overwrite input)
        preserve_references: Whether to update cross-references
        dry_run: If True, don't write output, just report changes

    Returns:
        SimpleReport with results
    """
    report = SimpleReport(input_file=str(input_path))

    try:
        # Load document
        lines = load_document(input_path)
        report.add_info(f"Loaded {len(lines)} lines from {input_path.name}")

        # Preview changes
        changes = preview_renumbering(lines)
        report.add_info(f"Found {len(changes)} headers to renumber")

        if len(changes) == 0:
            report.add_info("No changes needed - document already correctly numbered")
            report.success = True
            return report

        # Show preview
        for line_num, old, new in changes[:10]:  # Show first 10
            report.add_info(f"  Line {line_num}: {old[:60]} -> {new[:60]}")

        if len(changes) > 10:
            report.add_info(f"  ... and {len(changes) - 10} more changes")

        if dry_run:
            report.add_info("DRY RUN: No changes written")
            report.success = True
            return report

        # Apply renumbering
        numberer = SectionNumberer()
        renumbered_lines = renumber_document_headers(lines, numberer)

        # Handle cross-references
        if preserve_references:
            xref_manager = CrossReferenceManager()

            # Record all renumberings
            for line_num, old, new in changes:
                # Extract section title
                old_text = old.lstrip('#').strip()
                title = re.sub(r'^\d+(\.\d+)*\s+', '', old_text)
                xref_manager.record_renumbering(old, new, title)

            # Update references
            renumbered_lines = xref_manager.update_references(renumbered_lines)
            report.add_info(f"Updated cross-references ({len(xref_manager.section_map)} mappings)")

        # Save output
        if output_path is None:
            output_path = input_path

        save_document(output_path, renumbered_lines)
        report.add_info(f"Saved repaired document to {output_path}")

        report.success = True
        report.output_file = str(output_path)

    except Exception as e:
        report.add_error(f"Failed to repair numbering: {e}")
        report.success = False

    return report


def process_directory(
    input_dir: Path,
    output_dir: Path,
    pattern: str = "chapter_*.md",
    dry_run: bool = False,
    verbose: bool = False
) -> List[SimpleReport]:
    """Process all matching files in a directory.

    Args:
        input_dir: Input directory
        output_dir: Output directory
        pattern: File glob pattern
        dry_run: If True, preview only
        verbose: Show detailed output

    Returns:
        List of processing reports
    """
    reports = []

    # Find all matching files
    files = sorted(input_dir.glob(pattern))

    if not files:
        print(f"No files matching '{pattern}' found in {input_dir}")
        return reports

    print(f"Processing {len(files)} files from {input_dir}")
    print(f"Output directory: {output_dir}")

    if dry_run:
        print("DRY RUN MODE - No changes will be written\n")

    for file_path in files:
        output_path = output_dir / file_path.name

        print(f"\nProcessing: {file_path.name}")

        report = repair_document_numbering(
            file_path,
            output_path,
            preserve_references=True,
            dry_run=dry_run
        )

        reports.append(report)

        if verbose or not report.success:
            print(report.format())

    return reports


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Repair hierarchical section numbering in markdown documents"
    )

    parser.add_argument(
        '--chapter',
        type=str,
        help='Process a single chapter file (e.g., chapter_01.md)'
    )

    parser.add_argument(
        '--input-dir',
        type=Path,
        default=Path('output/chapters/04_merged'),
        help='Input directory (default: output/chapters/04_merged)'
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
        '--dry-run',
        action='store_true',
        help='Preview changes without writing files'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed processing information'
    )

    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    args = parser.parse_args()

    # Process single chapter or directory
    if args.chapter:
        input_path = args.input_dir / args.chapter
        output_path = args.output_dir / args.chapter

        if not input_path.exists():
            print(f"Error: File not found: {input_path}")
            sys.exit(1)

        print(f"Processing: {input_path}")

        report = repair_document_numbering(
            input_path,
            output_path,
            preserve_references=True,
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
            dry_run=args.dry_run,
            verbose=args.verbose
        )

        # Summary
        success_count = sum(1 for r in reports if r.success)
        print(f"\n{'='*60}")
        print(f"Summary: {success_count}/{len(reports)} files processed successfully")

        if success_count < len(reports):
            print("\nFailed files:")
            for report in reports:
                if not report.success:
                    print(f"  - {Path(report.input_file).name}")

        sys.exit(0 if success_count == len(reports) else 1)


if __name__ == '__main__':
    main()
