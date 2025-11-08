#!/usr/bin/env python3
"""
Generate PDF for the reorganized Chapter 5 (ch05_v07_final.md)
"""

import subprocess
import sys
from pathlib import Path

def generate_pdf(input_file: str, output_file: str):
    """Generate PDF from markdown using pandoc."""

    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generating PDF from: {input_file}")
    print(f"Output: {output_file}")
    print()

    # Use pandoc to generate PDF
    cmd = [
        'pandoc',
        str(input_path),
        '-o', str(output_path),
        '--from', 'markdown-yaml_metadata_block',
        '--pdf-engine', 'pdflatex',
        '-V', 'geometry:margin=1in',
        '-V', 'fontsize=11pt'
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        print("✓ PDF generated successfully!")
        print(f"File size: {output_path.stat().st_size / 1024:.1f} KB")
        return True

    except subprocess.CalledProcessError as e:
        print(f"✗ Error generating PDF:", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        return False
    except FileNotFoundError:
        print("✗ Error: pandoc not found. Please install pandoc.", file=sys.stderr)
        return False


if __name__ == '__main__':
    input_file = 'output/markdown/05_repaired/ch05_v07_final.md'
    output_file = 'output/pdfs/ch05_v07_final.pdf'

    success = generate_pdf(input_file, output_file)
    sys.exit(0 if success else 1)
