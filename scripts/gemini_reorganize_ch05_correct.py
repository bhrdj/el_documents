#!/usr/bin/env python3
"""
Correct approach: Give Gemini the WHOLE original chapter,
ask it to generate each NEW section from the reorganization plan.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from gemini_api import call_gemini


# Gemini's proposed 8 major sections from the reorganization plan
SECTION_STRUCTURE = [
    ("5.1", "Introduction"),
    ("5.2", "Guiding Principles for Enrichment"),
    ("5.3", "Group Sizes for Structured Activities"),
    ("5.4", "Activity and Game Compendium"),
    ("5.5", "Integrating Enrichment into Daily Routines"),
    ("5.6", "Educational Tools"),
    ("5.7", "Child-Centered Learning Strategies"),
    ("5.8", "Special Considerations"),
]


def get_nairobi_time():
    """Get current time in Nairobi timezone (UTC+3)."""
    utc_now = datetime.utcnow()
    nairobi_time = utc_now + timedelta(hours=3)
    return nairobi_time.strftime('%Y-%m-%d %H:%M:%S EAT')


def generate_section(
    section_num: str,
    section_title: str,
    full_original_content: str,
    analysis_plan: str,
    is_first: bool = False,
    subsection_spec: str = None
) -> str:
    """
    Generate a complete section from the new outline by analyzing the full original content.

    Args:
        section_num: New section number (e.g., "5.1", "5.4.1")
        section_title: New section title
        full_original_content: The COMPLETE original chapter
        analysis_plan: Gemini's reorganization plan
        is_first: True if this is section 5.1 (include chapter title)
        subsection_spec: If splitting a large section, specify which subsection to generate
    """

    if subsection_spec:
        print(f"  Subsection: {subsection_spec}")
        task_description = f"Generate subsection {subsection_spec} of section {section_num}"
    else:
        task_description = f"Generate complete section {section_num}"

    if is_first and not subsection_spec:
        prompt = f"""You are reorganizing Chapter 5 of an EL daycare manual according to your reorganization plan.

YOUR COMPLETE REORGANIZATION PLAN:
{analysis_plan}

---

COMPLETE ORIGINAL CHAPTER (for reference - extract content from here):
{full_original_content}

---

TASK:
Generate Section {section_num}: {section_title}

This is the FIRST section, so:
1. Start with the chapter title: # 5. Foundations of Structured Enrichment (6-36 Months)
2. Then create the complete section {section_num} with all subsections
3. Extract ALL relevant content from the original chapter
4. Follow your reorganization plan's structure exactly
5. Use proper hierarchical numbering ({section_num}.1, {section_num}.2, etc.)
6. Include ALL details, examples, and instructions - do NOT summarize
7. Use proper markdown headers (##, ###, ####, etc.)

OUTPUT: Return ONLY the reorganized markdown starting with the chapter title."""

    elif subsection_spec:
        prompt = f"""You are reorganizing Chapter 5 of an EL daycare manual according to your reorganization plan.

YOUR COMPLETE REORGANIZATION PLAN:
{analysis_plan}

---

COMPLETE ORIGINAL CHAPTER (for reference - extract content from here):
{full_original_content}

---

TASK:
Generate {subsection_spec} of Section {section_num}: {section_title}

Requirements:
1. Extract content from the original chapter relevant to this subsection
2. Follow your reorganization plan's structure
3. Use proper hierarchical numbering
4. Include ALL details, examples, and instructions - do NOT summarize
5. This is a PART of section {section_num}, so start with the appropriate subsection header
6. Use proper markdown headers (###, ####, etc.)

OUTPUT: Return ONLY the reorganized markdown for this subsection."""

    else:
        prompt = f"""You are reorganizing Chapter 5 of an EL daycare manual according to your reorganization plan.

YOUR COMPLETE REORGANIZATION PLAN:
{analysis_plan}

---

COMPLETE ORIGINAL CHAPTER (for reference - extract content from here):
{full_original_content}

---

TASK:
Generate Section {section_num}: {section_title}

Requirements:
1. Extract ALL relevant content from the original chapter for this section
2. Follow your reorganization plan's structure exactly
3. Use proper hierarchical numbering ({section_num}.1, {section_num}.2, etc.)
4. Include ALL details, examples, and instructions - do NOT summarize
5. Use proper markdown headers (##, ###, ####, etc.)

OUTPUT: Return ONLY the reorganized markdown for section {section_num}. Do NOT include the chapter title."""

    # Call Gemini
    print(f"  Calling Gemini... [{get_nairobi_time()}]")
    reorganized = call_gemini(
        prompt,
        model="gemini-2.5-pro",
        temperature=0.2,
        max_output_tokens=50000
    )

    words = len(reorganized.split())
    completion_time = get_nairobi_time()
    print(f"  ✓ Generated {words:,} words [{completion_time}]")

    return reorganized


def main():
    """Main entry point."""

    # File paths - using ch05_older_stage02.md as requested
    original_file = 'output/markdown/05_repaired/ch05_older_stage02.md'
    analysis_file = 'output/markdown/05_repaired/ch05_macro_analysis.md'
    output_file = 'output/markdown/05_repaired/ch05_v07_final.md'

    print("="*70)
    print("Chapter 5 Reorganization (Correct Approach)")
    print("="*70)
    print(f"Started: {get_nairobi_time()}")
    print()

    # Read files
    with open(original_file, 'r', encoding='utf-8') as f:
        original_content = f.read()

    with open(analysis_file, 'r', encoding='utf-8') as f:
        analysis_plan = f.read()

    total_words = len(original_content.split())
    print(f"Input file: {original_file}")
    print(f"Total input words: {total_words:,}")
    print(f"Output file: {output_file}")
    print()

    # Process each section from the NEW outline
    all_sections = []

    for i, (section_num, section_title) in enumerate(SECTION_STRUCTURE):
        print(f"{'='*70}")
        print(f"Section {section_num}: {section_title}")
        print(f"{'='*70}")

        # For section 5.4 (Activity Compendium), check if we need to split
        # Otherwise, generate the complete section
        if section_num == "5.4":
            # This is likely the largest section - check if we should split it
            print("Note: Large section - may need multiple API calls")
            print()

            # For now, try generating it as one piece
            # If it times out or truncates, we'll split it into subsections
            result = generate_section(
                section_num=section_num,
                section_title=section_title,
                full_original_content=original_content,
                analysis_plan=analysis_plan,
                is_first=(i == 0)
            )
            all_sections.append(result)
        else:
            # Normal section - generate in one go
            result = generate_section(
                section_num=section_num,
                section_title=section_title,
                full_original_content=original_content,
                analysis_plan=analysis_plan,
                is_first=(i == 0)
            )
            all_sections.append(result)

        print()

    # Combine all sections
    print(f"{'='*70}")
    print("Combining all sections...")
    print(f"{'='*70}\n")

    combined = all_sections[0]
    for section in all_sections[1:]:
        section = section.strip()
        # Remove markdown code fences if present
        if section.startswith("```markdown"):
            section = section[len("```markdown"):].strip()
        if section.endswith("```"):
            section = section[:-3].strip()
        combined += "\n\n" + section

    # Clean up any remaining code fences
    if combined.startswith("```markdown"):
        combined = combined[len("```markdown"):].strip()
    if combined.endswith("```"):
        combined = combined[:-3].strip()

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(combined)

    # Report
    output_path = Path(output_file)
    size_kb = output_path.stat().st_size / 1024
    output_words = len(combined.split())

    print("="*70)
    print("✓ REORGANIZATION COMPLETE!")
    print("="*70)
    print(f"Completed: {get_nairobi_time()}")
    print(f"Output file: {output_file}")
    print(f"File size: {size_kb:.1f} KB")
    print(f"Output words: {output_words:,}")
    print(f"Input words: {total_words:,}")
    print(f"Word retention: {output_words / total_words * 100:.1f}%")
    print("="*70)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\nInterrupted by user at {get_nairobi_time()}. Exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"\nError at {get_nairobi_time()}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
