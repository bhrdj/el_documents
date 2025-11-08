#!/usr/bin/env python3
"""
Compare Chapter 5 v01 (original) with v03 (reorganized).
"""

import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from gemini_api import call_gemini


def main():
    """Main execution."""
    base_dir = Path("/home/steven/git/el_documents/output/chapters/05_repaired")
    v01_path = base_dir / "ch05_v01.md"
    v03_path = base_dir / "ch05_v03.md"
    comparison_path = base_dir / "ch05_compare_v01v03.md"

    print("Reading versions...")
    v01_content = v01_path.read_text()
    v03_content = v03_path.read_text()

    print(f"v01: {len(v01_content.split())} words")
    print(f"v03: {len(v03_content.split())} words")

    print("\nSending to Gemini 2.5 Pro for comparison...")

    # Due to size, we'll sample sections for comparison
    v01_sample = ' '.join(v01_content.split()[:5000])  # First 5000 words
    v03_sample = ' '.join(v03_content.split()[:5000])  # First 5000 words

    prompt = f"""You are an expert editor and reading comprehension specialist. Please compare these two versions of an educational manual chapter and analyze which one reads better.

NOTE: These are SAMPLES (first ~5000 words) of much larger documents.

VERSION 1 (Original - Sample):
---
{v01_sample}
---

VERSION 3 (Iteratively Reorganized - Sample):
---
{v03_sample}
---

Please provide a detailed comparison that addresses:

1. **Overall Readability**: Which version is easier to read and understand?
2. **Organization**: Which version has better structural organization?
3. **Flow**: Which version flows more naturally from section to section?
4. **Clarity**: Which version presents information more clearly?
5. **Section Numbering**: Which version has better section numbering and hierarchy?
6. **Specific Improvements**: What specific improvements does the better version have?
7. **Recommendation**: Which version would you recommend for publication and why?

Please be thorough and specific in your analysis."""

    response = call_gemini(
        prompt,
        model="gemini-2.5-pro",
        temperature=0.5,
        max_output_tokens=10000
    )

    print(f"\nSaving comparison to: {comparison_path}")
    comparison_path.write_text(response)

    print("✓ Comparison complete!")
    print(f"\nComparison saved to: {comparison_path}")


if __name__ == "__main__":
    main()
