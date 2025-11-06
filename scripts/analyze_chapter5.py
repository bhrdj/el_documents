#!/usr/bin/env python3
"""
Analyze and restore missing Chapter 5 content.

This script compares the merged Chapter 5 file against the source parts
(chapter_5_part1.md and chapter_5_part2.md) to identify and optionally
restore any missing content.
"""

import argparse
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.content_comparison import (
    parse_content_blocks,
    find_missing_content,
    merge_source_blocks,
    create_analysis_report
)
from lib.document import Document


def load_source_files(input_dir: Path) -> tuple:
    """
    Load Chapter 5 source files (part1, part2, and merged).

    Args:
        input_dir: Input directory containing merged file

    Returns:
        Tuple of (part1_doc, part2_doc, merged_doc) or (None, None, None) if not found
    """
    # Source parts are in 00_raw
    raw_dir = input_dir.parent / "00_raw"
    part1_path = raw_dir / "chapter_5_part1.md"
    part2_path = raw_dir / "chapter_5_part2.md"

    # Merged file is in the input directory (04_merged)
    merged_path = input_dir / "chapter_05.md"

    # Check files exist
    if not part1_path.exists():
        print(f"❌ Error: Source file not found: {part1_path}")
        return (None, None, None)

    if not part2_path.exists():
        print(f"❌ Error: Source file not found: {part2_path}")
        return (None, None, None)

    if not merged_path.exists():
        print(f"❌ Error: Merged file not found: {merged_path}")
        return (None, None, None)

    try:
        part1_doc = Document(part1_path, chapter_number=5)
        part2_doc = Document(part2_path, chapter_number=5)
        merged_doc = Document(merged_path, chapter_number=5)
        return (part1_doc, part2_doc, merged_doc)
    except Exception as e:
        print(f"❌ Error loading documents: {e}")
        return (None, None, None)


def analyze_chapter5(
    part1_doc: Document,
    part2_doc: Document,
    merged_doc: Document,
    verbose: bool = False
) -> tuple:
    """
    Analyze Chapter 5 content completeness.

    Args:
        part1_doc: Part 1 source document
        part2_doc: Part 2 source document
        merged_doc: Current merged document
        verbose: Whether to print verbose output

    Returns:
        Tuple of (missing_blocks, all_source_blocks, merged_blocks, analysis_report)
    """
    if verbose:
        print(f"📊 Analyzing Chapter 5 content...")
        print(f"  Part 1: {len(part1_doc.lines)} lines")
        print(f"  Part 2: {len(part2_doc.lines)} lines")
        print(f"  Merged: {len(merged_doc.lines)} lines")

    # Parse content blocks
    part1_blocks = parse_content_blocks(part1_doc.lines)
    part2_blocks = parse_content_blocks(part2_doc.lines)
    merged_blocks = parse_content_blocks(merged_doc.lines)

    if verbose:
        print(f"\n📦 Content blocks detected:")
        print(f"  Part 1: {len(part1_blocks)} blocks")
        print(f"  Part 2: {len(part2_blocks)} blocks")
        print(f"  Merged: {len(merged_blocks)} blocks")

    # Merge source blocks (deduplicate)
    all_source_blocks = merge_source_blocks(part1_blocks, part2_blocks)

    if verbose:
        print(f"  Combined unique source blocks: {len(all_source_blocks)}")

    # Find missing content
    missing_blocks, _ = find_missing_content(all_source_blocks, merged_blocks)

    if verbose:
        print(f"\n🔍 Missing content: {len(missing_blocks)} blocks")

    # Generate analysis report
    analysis_report = create_analysis_report(
        part1_blocks,
        part2_blocks,
        merged_blocks,
        missing_blocks
    )

    return (missing_blocks, all_source_blocks, merged_blocks, analysis_report)


def restore_missing_content(
    merged_doc: Document,
    missing_blocks: list,
    output_path: Path,
    verbose: bool = False
) -> bool:
    """
    Restore missing content to the merged document.

    Args:
        merged_doc: Current merged document
        missing_blocks: List of missing content blocks
        output_path: Path to save restored document
        verbose: Whether to print verbose output

    Returns:
        True if restoration successful, False otherwise
    """
    if not missing_blocks:
        if verbose:
            print("✓ No missing content to restore")
        return True

    if verbose:
        print(f"\n🔧 Restoring {len(missing_blocks)} missing blocks...")

    # Simple append strategy: add missing blocks at end
    # More sophisticated logic could try to insert in correct positions
    restored_lines = merged_doc.lines.copy()

    restored_lines.append("\n")
    restored_lines.append("---")
    restored_lines.append("\n")
    restored_lines.append("## Restored Content")
    restored_lines.append("\n")
    restored_lines.append("*The following content was automatically restored from source files.*")
    restored_lines.append("\n")

    for block in missing_blocks:
        restored_lines.append("\n")
        restored_lines.append(block.content)
        restored_lines.append("\n")

    # Save restored document
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_content = '\n'.join(restored_lines)
        output_path.write_text(output_content, encoding='utf-8')

        if verbose:
            print(f"✓ Restored content saved to: {output_path}")

        return True

    except Exception as e:
        print(f"❌ Error saving restored content: {e}")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze and restore missing Chapter 5 content"
    )
    parser.add_argument(
        '--restore',
        action='store_true',
        help="Automatically restore missing content"
    )
    parser.add_argument(
        '--input-dir',
        type=Path,
        default=Path("output/chapters/04_merged"),
        help="Input directory with source files (default: output/chapters/04_merged)"
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path("output/chapters/05_repaired"),
        help="Output directory for repaired files (default: output/chapters/05_repaired)"
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help="Enable verbose output"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Chapter 5 Content Analysis")
    print("=" * 60)

    # Load source files
    part1_doc, part2_doc, merged_doc = load_source_files(args.input_dir)
    if not all([part1_doc, part2_doc, merged_doc]):
        sys.exit(1)

    # Analyze content
    missing_blocks, all_source_blocks, merged_blocks, analysis_report = analyze_chapter5(
        part1_doc,
        part2_doc,
        merged_doc,
        verbose=args.verbose
    )

    # Save analysis report
    report_path = args.output_dir / "CHAPTER_5_ANALYSIS.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(analysis_report, encoding='utf-8')

    if args.verbose:
        print(f"\n📄 Analysis report saved to: {report_path}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"Analysis Summary:")
    print(f"{'='*60}")
    print(f"  Source blocks (part1 + part2): {len(all_source_blocks)}")
    print(f"  Merged file blocks: {len(merged_blocks)}")
    print(f"  Missing blocks: {len(missing_blocks)}")

    if len(missing_blocks) == 0:
        print(f"\n✓ STATUS: Chapter 5 is COMPLETE")
        print(f"  All source content is present in the merged file.")
        return 0
    else:
        print(f"\n⚠ STATUS: Chapter 5 is INCOMPLETE")
        print(f"  {len(missing_blocks)} content blocks are missing.")

        if args.restore:
            print(f"\n🔧 Restoring missing content...")
            output_path = args.output_dir / "chapter_05.md"

            success = restore_missing_content(
                merged_doc,
                missing_blocks,
                output_path,
                verbose=args.verbose
            )

            if success:
                print(f"\n✓ Restoration complete: {output_path}")
                print(f"  Review the restored content and adjust placement if needed.")
                return 0
            else:
                print(f"\n❌ Restoration failed")
                return 1
        else:
            print(f"\n  Run with --restore flag to automatically restore missing content.")
            return 1


if __name__ == '__main__':
    sys.exit(main())
