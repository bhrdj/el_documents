#!/usr/bin/env python3
"""
Iteratively reorganize Chapter 5 section by section using Gemini 2.5 Pro.
Each section builds on the previous reorganized output.
"""

import sys
from pathlib import Path
import time

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from gemini_api import call_gemini


def reorganize_section(
    section_num: int,
    section_content: str,
    previous_output: str,
    is_first: bool = False
) -> str:
    """
    Reorganize a single section with context from previous sections.

    Args:
        section_num: Section number
        section_content: Content to reorganize
        previous_output: Previously reorganized content
        is_first: Whether this is the first section

    Returns:
        Reorganized content for this section
    """
    print(f"\nProcessing Section {section_num:02d}...")
    print(f"  Input: {len(section_content.split())} words")

    if is_first:
        prompt = f"""You are an expert editor and technical writer. This is Section 1 of a multi-section educational manual chapter on structured enrichment for children aged 6-36 months in EL daycares.

TASK: Reorganize this section to improve organization and clarity while keeping ALL content.

IMPORTANT:
- Keep ALL the same ideas and information
- Improve structural organization and flow
- Fix any formatting issues
- Use consistent markdown formatting
- DO NOT remove content
- DO NOT add new content beyond what's implied
- This is SECTION 1, so include appropriate chapter header and introduction

Here is Section 1:

{section_content}

Please output the reorganized version of Section 1."""

    else:
        preview_words = 500
        previous_preview = ' '.join(previous_output.split()[-preview_words:])

        prompt = f"""You are an expert editor and technical writer. You are reorganizing a multi-section educational manual chapter section by section.

CONTEXT - Here is the END of what you've reorganized so far (last {preview_words} words):
---
...{previous_preview}
---

TASK: Now reorganize Section {section_num} to improve organization and flow, maintaining consistency with the style and structure you've established.

IMPORTANT:
- Keep ALL content from Section {section_num}
- Maintain consistency with previous sections
- Improve organization and clarity
- Use the same markdown formatting style
- DO NOT remove content
- DO NOT add new content
- Continue section numbering logically

Here is Section {section_num}:

{section_content}

Please output ONLY the reorganized content for Section {section_num}. Do NOT repeat previous sections."""

    try:
        response = call_gemini(
            prompt,
            model="gemini-2.5-pro",
            temperature=0.3,
            max_output_tokens=10000
        )

        # Clean up the response
        response = response.strip()

        # Remove any meta-commentary
        if response.startswith("Of course") or response.startswith("Certainly"):
            lines = response.split('\n')
            # Find where actual content starts
            for i, line in enumerate(lines):
                if line.strip().startswith('#') or line.strip().startswith('---'):
                    response = '\n'.join(lines[i:])
                    break

        print(f"  Output: {len(response.split())} words")

        return response

    except Exception as e:
        print(f"  ERROR: {e}")
        raise


def main():
    """Main execution."""
    sections_dir = Path("/home/steven/git/el_documents/output/markdown/05_repaired/sections/reorganize_input")
    output_dir = Path("/home/steven/git/el_documents/output/markdown/05_repaired")

    # Get all section files
    section_files = sorted(sections_dir.glob("section_*.md"))

    if not section_files:
        print(f"No section files found in {sections_dir}")
        sys.exit(1)

    print(f"{'='*80}")
    print(f"Iterative Chapter 5 Reorganization")
    print(f"{'='*80}")
    print(f"Found {len(section_files)} sections to process\n")

    # Initialize output
    reorganized_output = ""
    total_input_words = 0
    total_output_words = 0

    # Process each section
    for i, section_file in enumerate(section_files, 1):
        section_content = section_file.read_text()
        input_words = len(section_content.split())
        total_input_words += input_words

        try:
            reorganized_section = reorganize_section(
                section_num=i,
                section_content=section_content,
                previous_output=reorganized_output,
                is_first=(i == 1)
            )

            output_words = len(reorganized_section.split())
            total_output_words += output_words

            # Append to output
            if reorganized_output:
                reorganized_output += "\n\n" + reorganized_section
            else:
                reorganized_output = reorganized_section

            # Save progress after each section
            progress_file = output_dir / "ch05_v03_progress.md"
            progress_file.write_text(reorganized_output)

            print(f"  ✓ Section {i:02d} complete")
            print(f"  Progress: {i}/{len(section_files)} sections ({i/len(section_files)*100:.1f}%)")
            print(f"  Total output so far: {total_output_words:,} words")

            # Rate limit
            if i < len(section_files):
                time.sleep(2)

        except Exception as e:
            print(f"\n✗ Failed on section {i}: {e}")
            print(f"Progress saved to: {output_dir}/ch05_v03_progress.md")
            sys.exit(1)

    # Save final output
    final_file = output_dir / "ch05_v03.md"
    final_file.write_text(reorganized_output)

    print(f"\n{'='*80}")
    print("Reorganization Complete!")
    print(f"{'='*80}")
    print(f"Input: {total_input_words:,} words")
    print(f"Output: {total_output_words:,} words")
    print(f"Sections processed: {len(section_files)}")
    print(f"\nFinal output saved to: {final_file}")


if __name__ == "__main__":
    main()
