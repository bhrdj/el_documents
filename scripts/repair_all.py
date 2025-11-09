#!/usr/bin/env python3
"""
Master orchestration script for complete document structure repair.

This script runs the entire document repair pipeline in the correct sequence:
1. Analyze and restore Chapter 5 missing content
2. Repair hierarchical section numbering across all documents
3. Repair bullet list hierarchy and formatting
4. Validate all repairs
5. Generate comprehensive repair report

Usage:
    .venv/bin/python scripts/repair_all.py [options]

Examples:
    # Process all chapters with default settings
    .venv/bin/python scripts/repair_all.py

    # Process a single chapter only
    .venv/bin/python scripts/repair_all.py --chapter 5

    # Dry-run mode (preview changes only)
    .venv/bin/python scripts/repair_all.py --dry-run

    # Verbose output with custom output directory
    .venv/bin/python scripts/repair_all.py --output-dir output/markdown/05_test --verbose
"""

import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from reporting import AggregateReport, ProcessingReport


def run_command(command: List[str], description: str, verbose: bool = False) -> bool:
    """
    Run a subprocess command and handle output.

    Args:
        command: Command to run as list of arguments
        description: Human-readable description of the command
        verbose: If True, show all output; otherwise show only errors

    Returns:
        True if command succeeded, False otherwise
    """
    print(f"\n{'='*80}")
    print(f"STEP: {description}")
    print(f"{'='*80}")

    if verbose:
        print(f"Running: {' '.join(str(c) for c in command)}")
        print()

    try:
        if verbose:
            # Show real-time output
            result = subprocess.run(command, check=True, text=True)
            return True
        else:
            # Capture output, only show on error
            result = subprocess.run(
                command,
                check=True,
                text=True,
                capture_output=True
            )
            print(f"✓ {description} - COMPLETED")
            return True

    except subprocess.CalledProcessError as e:
        print(f"\n✗ {description} - FAILED")
        print(f"Error code: {e.returncode}")
        if e.stdout:
            print(f"\nStdout:\n{e.stdout}")
        if e.stderr:
            print(f"\nStderr:\n{e.stderr}")
        return False
    except Exception as e:
        print(f"\n✗ {description} - FAILED")
        print(f"Exception: {e}")
        return False


def main():
    """Main orchestration function."""
    parser = argparse.ArgumentParser(
        description='Master script to run complete document structure repair pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--input-dir',
        type=Path,
        default=Path('output/markdown/04_merged'),
        help='Input directory with source documents (default: output/markdown/04_merged)'
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('output/markdown/05_repaired'),
        help='Output directory for repaired documents (default: output/markdown/05_repaired)'
    )

    parser.add_argument(
        '--chapter',
        type=int,
        help='Process only a specific chapter number (e.g., 5)'
    )

    parser.add_argument(
        '--pattern',
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
        '--skip-chapter5',
        action='store_true',
        help='Skip Chapter 5 analysis and restoration (useful if already done)'
    )

    parser.add_argument(
        '--skip-validation',
        action='store_true',
        help='Skip final validation step'
    )

    args = parser.parse_args()

    # Determine Python interpreter
    python = '.venv/bin/python'

    # Build base paths
    scripts_dir = Path(__file__).parent
    input_dir = args.input_dir
    output_dir = args.output_dir

    print("="*80)
    print("DOCUMENT STRUCTURE REPAIR - MASTER PIPELINE")
    print("="*80)
    print(f"\nInput directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Dry-run mode: {args.dry_run}")
    print(f"Verbose mode: {args.verbose}")
    if args.chapter:
        print(f"Processing chapter: {args.chapter}")
    print()

    # Ensure output directory exists
    if not args.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Output directory ready: {output_dir}\n")

    # Track which steps succeeded
    steps_status = {}
    start_time = datetime.now()

    # =========================================================================
    # STEP 1: Analyze and Restore Chapter 5 Content
    # =========================================================================
    if not args.skip_chapter5 and (args.chapter is None or args.chapter == 5):
        step1_cmd = [
            python,
            str(scripts_dir / 'analyze_chapter5.py'),
            '--input-dir', str(input_dir),
            '--output-dir', str(output_dir),
        ]

        if not args.dry_run:
            step1_cmd.append('--restore')

        if args.verbose:
            step1_cmd.append('--verbose')

        steps_status['chapter5_restore'] = run_command(
            step1_cmd,
            "Step 1: Analyze and Restore Chapter 5 Content",
            args.verbose
        )
    else:
        if args.skip_chapter5:
            print(f"\n{'='*80}")
            print("Step 1: SKIPPED (--skip-chapter5 flag)")
            print(f"{'='*80}")
            steps_status['chapter5_restore'] = True  # Don't fail the pipeline
        else:
            print(f"\n{'='*80}")
            print(f"Step 1: SKIPPED (processing chapter {args.chapter}, not Chapter 5)")
            print(f"{'='*80}")
            steps_status['chapter5_restore'] = True  # Don't fail the pipeline

    # =========================================================================
    # STEP 2: Repair Section Numbering
    # =========================================================================
    step2_cmd = [
        python,
        str(scripts_dir / 'repair_section_numbering.py'),
        '--input-dir', str(input_dir),
        '--output-dir', str(output_dir),
        '--pattern', args.pattern,
    ]

    if args.chapter is not None:
        step2_cmd.extend(['--chapter', f'chapter_{args.chapter:02d}.md'])

    if args.dry_run:
        step2_cmd.append('--dry-run')

    if args.verbose:
        step2_cmd.append('--verbose')

    steps_status['section_numbering'] = run_command(
        step2_cmd,
        "Step 2: Repair Hierarchical Section Numbering",
        args.verbose
    )

    # Only continue if previous step succeeded
    if not steps_status['section_numbering']:
        print("\n✗ Pipeline failed at Step 2. Stopping.")
        sys.exit(1)

    # =========================================================================
    # STEP 3: Repair Bullet List Hierarchy
    # =========================================================================
    step3_cmd = [
        python,
        str(scripts_dir / 'repair_bullet_hierarchy.py'),
        '--input-dir', str(output_dir),  # Read from output of step 2
        '--output-dir', str(output_dir),  # Write back to same directory
        '--pattern', args.pattern,
    ]

    if args.chapter is not None:
        step3_cmd.extend(['--chapter', f'chapter_{args.chapter:02d}.md'])

    if args.dry_run:
        step3_cmd.append('--dry-run')

    if args.verbose:
        step3_cmd.append('--verbose')

    steps_status['bullet_hierarchy'] = run_command(
        step3_cmd,
        "Step 3: Repair Bullet List Hierarchy",
        args.verbose
    )

    # Only continue if previous step succeeded
    if not steps_status['bullet_hierarchy']:
        print("\n✗ Pipeline failed at Step 3. Stopping.")
        sys.exit(1)

    # =========================================================================
    # STEP 4: Validate Structure
    # =========================================================================
    if not args.skip_validation and not args.dry_run:
        validation_pattern = f'chapter_{args.chapter:02d}.md' if args.chapter is not None else '*.md'

        step4_cmd = [
            python,
            str(scripts_dir / 'validate_structure.py'),
            '--input-dir', str(output_dir),
            '--source-dir', str(input_dir),
            '--pattern', validation_pattern,
            '--output', str(output_dir / 'VALIDATION_REPORT.md'),
        ]

        # Note: validation script doesn't have --verbose flag, it always shows output
        steps_status['validation'] = run_command(
            step4_cmd,
            "Step 4: Validate Document Structure",
            args.verbose
        )

        # Validation failure is not fatal - we still report success if repairs completed
        if not steps_status['validation']:
            print("\n⚠ Validation detected issues (see VALIDATION_REPORT.md)")
    else:
        if args.skip_validation:
            print(f"\n{'='*80}")
            print("Step 4: SKIPPED (--skip-validation flag)")
            print(f"{'='*80}")
        else:
            print(f"\n{'='*80}")
            print("Step 4: SKIPPED (dry-run mode)")
            print(f"{'='*80}")
        steps_status['validation'] = True

    # =========================================================================
    # STEP 5: Generate Comprehensive Report
    # =========================================================================
    end_time = datetime.now()
    duration = end_time - start_time

    print(f"\n{'='*80}")
    print("PIPELINE SUMMARY")
    print(f"{'='*80}\n")

    print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {duration}\n")

    print("Steps completed:")
    for step_name, status in steps_status.items():
        status_icon = "✓" if status else "✗"
        status_text = "SUCCESS" if status else "FAILED"
        print(f"  {status_icon} {step_name}: {status_text}")

    # Generate final summary report
    if not args.dry_run:
        report_path = output_dir / 'REPAIR_REPORT.md'

        report_lines = []
        report_lines.append("# Document Structure Repair - Pipeline Report")
        report_lines.append(f"\n**Generated**: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"**Duration**: {duration}")
        report_lines.append(f"**Mode**: {'Dry-run' if args.dry_run else 'Production'}")
        report_lines.append(f"\n## Configuration\n")
        report_lines.append(f"- **Input Directory**: `{input_dir}`")
        report_lines.append(f"- **Output Directory**: `{output_dir}`")
        report_lines.append(f"- **File Pattern**: `{args.pattern}`")
        if args.chapter:
            report_lines.append(f"- **Chapter Filter**: Chapter {args.chapter}")

        report_lines.append(f"\n## Pipeline Steps\n")
        report_lines.append("| Step | Description | Status |")
        report_lines.append("|------|-------------|--------|")

        step_descriptions = {
            'chapter5_restore': 'Analyze and Restore Chapter 5 Content',
            'section_numbering': 'Repair Hierarchical Section Numbering',
            'bullet_hierarchy': 'Repair Bullet List Hierarchy',
            'validation': 'Validate Document Structure'
        }

        for step_name, description in step_descriptions.items():
            if step_name in steps_status:
                status_icon = "✓" if steps_status[step_name] else "✗"
                status_text = "SUCCESS" if steps_status[step_name] else "FAILED"
                report_lines.append(f"| {step_name} | {description} | {status_icon} {status_text} |")

        all_succeeded = all(steps_status.values())
        report_lines.append(f"\n## Overall Status\n")
        if all_succeeded:
            report_lines.append("**Result**: ✓ ALL STEPS COMPLETED SUCCESSFULLY")
        else:
            failed_steps = [name for name, status in steps_status.items() if not status]
            report_lines.append(f"**Result**: ✗ PIPELINE FAILED")
            report_lines.append(f"\n**Failed Steps**: {', '.join(failed_steps)}")

        report_lines.append(f"\n## Next Steps\n")
        report_lines.append("- Review `VALIDATION_REPORT.md` for structural issues")
        report_lines.append("- Check individual chapter files in output directory")
        report_lines.append("- Run PDF generation if all validations pass")

        report_content = '\n'.join(report_lines)
        report_path.write_text(report_content, encoding='utf-8')

        print(f"\n✓ Pipeline report saved to: {report_path}")

    # Final exit status
    print()
    if all(steps_status.values()):
        print("="*80)
        print("✓ PIPELINE COMPLETED SUCCESSFULLY")
        print("="*80)
        sys.exit(0)
    else:
        print("="*80)
        print("✗ PIPELINE COMPLETED WITH ERRORS")
        print("="*80)
        sys.exit(1)


if __name__ == '__main__':
    main()
