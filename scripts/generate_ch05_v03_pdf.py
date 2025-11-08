#!/usr/bin/env python3
"""
Generate PDF for ch05_v03.md using the existing PDF generation pipeline.
"""

import sys
from pathlib import Path

# Import the generate_pdf function from pdf_generator
sys.path.insert(0, str(Path(__file__).parent))
from pdf_generator import generate_pdf

def main():
    """Generate PDF for ch05_v03.md"""
    input_file = Path('output/markdown/05_repaired/ch05_v03.md')
    output_file = Path('output/pdfs/ch05_v03.pdf')

    print(f"Generating PDF for ch05_v03.md...")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}\n")

    if generate_pdf(str(input_file), str(output_file)):
        print(f"\n✓ PDF generated successfully: {output_file}")
    else:
        print(f"\n✗ PDF generation failed")
        sys.exit(1)

if __name__ == '__main__':
    main()
