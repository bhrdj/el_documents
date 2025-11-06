#!/usr/bin/env python3
"""
Reporting utilities for generating processing and validation reports.
"""

from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class ProcessingReport:
    """
    Summary of repairs performed on a document.

    Attributes:
        document_path: Path to processed document
        chapter_number: Chapter number
        repairs_applied: Descriptions of repairs
        sections_renumbered: Count of sections renumbered
        bullets_repaired: Count of bullet items fixed
        content_restored: Whether missing content was restored
        validation_passed: Whether post-repair validation passed
        errors: Any errors encountered
    """

    def __init__(self, document_path: Path, chapter_number: int):
        """
        Initialize a ProcessingReport.

        Args:
            document_path: Path to the document
            chapter_number: Chapter number
        """
        self.document_path = Path(document_path)
        self.chapter_number = chapter_number
        self.repairs_applied: List[str] = []
        self.sections_renumbered = 0
        self.bullets_repaired = 0
        self.content_restored = False
        self.validation_passed = False
        self.errors: List[str] = []
        self.timestamp = datetime.now()

    def add_repair(self, description: str) -> None:
        """Add a repair description."""
        self.repairs_applied.append(description)

    def add_error(self, error: str) -> None:
        """Add an error message."""
        self.errors.append(error)

    def to_markdown(self) -> str:
        """
        Generate markdown report.

        Returns:
            Markdown formatted report
        """
        lines = []
        lines.append(f"# Processing Report: Chapter {self.chapter_number}")
        lines.append(f"\n**Document**: `{self.document_path.name}`")
        lines.append(f"**Generated**: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"\n## Summary\n")
        lines.append(f"- **Sections Renumbered**: {self.sections_renumbered}")
        lines.append(f"- **Bullets Repaired**: {self.bullets_repaired}")
        lines.append(f"- **Content Restored**: {'Yes' if self.content_restored else 'No'}")
        lines.append(f"- **Validation Status**: {'✓ PASSED' if self.validation_passed else '✗ FAILED'}")

        if self.repairs_applied:
            lines.append(f"\n## Repairs Applied\n")
            for repair in self.repairs_applied:
                lines.append(f"- {repair}")

        if self.errors:
            lines.append(f"\n## Errors\n")
            for error in self.errors:
                lines.append(f"- ❌ {error}")

        return '\n'.join(lines)

    def save(self, output_path: Path) -> None:
        """
        Save report to file.

        Args:
            output_path: Path where to save the report
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        content = self.to_markdown()
        output_path.write_text(content, encoding='utf-8')


class AggregateReport:
    """
    Aggregates multiple processing reports into a summary.
    """

    def __init__(self, title: str = "Document Structure Repair Report"):
        """
        Initialize an AggregateReport.

        Args:
            title: Report title
        """
        self.title = title
        self.reports: List[ProcessingReport] = []
        self.timestamp = datetime.now()

    def add_report(self, report: ProcessingReport) -> None:
        """Add a processing report."""
        self.reports.append(report)

    def get_totals(self) -> Dict[str, Any]:
        """
        Calculate aggregate totals.

        Returns:
            Dictionary of totals
        """
        return {
            'total_chapters': len(self.reports),
            'total_sections_renumbered': sum(r.sections_renumbered for r in self.reports),
            'total_bullets_repaired': sum(r.bullets_repaired for r in self.reports),
            'content_restored_count': sum(1 for r in self.reports if r.content_restored),
            'validation_passed_count': sum(1 for r in self.reports if r.validation_passed),
            'total_errors': sum(len(r.errors) for r in self.reports)
        }

    def to_markdown(self) -> str:
        """
        Generate aggregate markdown report.

        Returns:
            Markdown formatted aggregate report
        """
        lines = []
        lines.append(f"# {self.title}")
        lines.append(f"\n**Generated**: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

        totals = self.get_totals()

        lines.append(f"\n## Overall Summary\n")
        lines.append(f"- **Total Chapters Processed**: {totals['total_chapters']}")
        lines.append(f"- **Total Sections Renumbered**: {totals['total_sections_renumbered']}")
        lines.append(f"- **Total Bullets Repaired**: {totals['total_bullets_repaired']}")
        lines.append(f"- **Chapters with Content Restored**: {totals['content_restored_count']}")
        lines.append(f"- **Chapters Passing Validation**: {totals['validation_passed_count']}/{totals['total_chapters']}")
        lines.append(f"- **Total Errors**: {totals['total_errors']}")

        # Status indicator
        if totals['validation_passed_count'] == totals['total_chapters'] and totals['total_errors'] == 0:
            lines.append(f"\n**Overall Status**: ✓ SUCCESS")
        else:
            lines.append(f"\n**Overall Status**: ⚠ WARNINGS OR ERRORS")

        lines.append(f"\n## Chapter Details\n")
        lines.append(f"| Chapter | Sections | Bullets | Content | Validation | Errors |")
        lines.append(f"|---------|----------|---------|---------|------------|--------|")

        for report in sorted(self.reports, key=lambda r: r.chapter_number):
            content_icon = "✓" if report.content_restored else "-"
            validation_icon = "✓" if report.validation_passed else "✗"
            error_count = len(report.errors)
            error_display = "0" if error_count == 0 else f"⚠ {error_count}"

            lines.append(
                f"| {report.chapter_number} | "
                f"{report.sections_renumbered} | "
                f"{report.bullets_repaired} | "
                f"{content_icon} | "
                f"{validation_icon} | "
                f"{error_display} |"
            )

        # Add individual reports if there are errors
        reports_with_errors = [r for r in self.reports if r.errors]
        if reports_with_errors:
            lines.append(f"\n## Error Details\n")
            for report in reports_with_errors:
                lines.append(f"\n### Chapter {report.chapter_number}\n")
                for error in report.errors:
                    lines.append(f"- {error}")

        return '\n'.join(lines)

    def save(self, output_path: Path) -> None:
        """
        Save aggregate report to file.

        Args:
            output_path: Path where to save the report
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        content = self.to_markdown()
        output_path.write_text(content, encoding='utf-8')
