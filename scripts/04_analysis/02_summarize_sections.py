#!/usr/bin/env python3
"""
Phase 1: Generate summaries for extracted sections using Claude API.

Usage:
    .venv/bin/python scripts/04_analysis/02_summarize_sections.py <sections_yaml> <markdown_file> [output_file]

Example:
    .venv/bin/python scripts/04_analysis/02_summarize_sections.py \
        output/chapters/04_merged/chapter_05_sections.yaml \
        output/chapters/04_merged/chapter_05_deduplicated.md \
        output/chapters/04_merged/chapter_05_summaries.yaml

Note: Requires ANTHROPIC_API_KEY environment variable to be set.
"""

import sys
import os
from pathlib import Path
import yaml
import time
from typing import Dict, List

# Check for API key
API_KEY = os.environ.get('ANTHROPIC_API_KEY')
if not API_KEY:
    print("Warning: ANTHROPIC_API_KEY not set. Will use local summarization fallback.")

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    print("Warning: anthropic package not installed. Using fallback summarization.")
    HAS_ANTHROPIC = False


def load_section_content(markdown_file: str, line_start: int, line_end: int) -> str:
    """Load section content from markdown file."""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Convert from 1-indexed to 0-indexed
    content_lines = lines[line_start - 1:line_end]
    return ''.join(content_lines)


def summarize_with_claude(section_data: Dict, content: str) -> str:
    """Generate summary using Claude API."""
    if not HAS_ANTHROPIC or not API_KEY:
        return summarize_fallback(content)

    client = anthropic.Anthropic(api_key=API_KEY)

    prompt = f"""Analyze this section from an Early Learning manual and provide a concise summary.

Section: {section_data['heading']} (Level {section_data['level']})

Content:
{content}

Provide a structured summary covering:
1. Main topic/purpose (1-2 sentences)
2. Key activities or concepts described
3. Target age groups mentioned (if any)
4. Notable features or important details

Keep the summary concise but informative (3-5 sentences total)."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text.strip()

    except Exception as e:
        print(f"  Error calling Claude API: {e}")
        print("  Falling back to local summarization")
        return summarize_fallback(content)


def summarize_fallback(content: str) -> str:
    """Fallback summarization using simple text analysis."""
    lines = content.split('\n')

    # Remove heading line
    content_lines = [l for l in lines if not l.strip().startswith('#')]
    text = '\n'.join(content_lines).strip()

    if not text:
        return "Empty section - no content to summarize."

    # Extract first few non-empty lines as summary
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    if not paragraphs:
        return "Section contains only whitespace or formatting."

    # Use first paragraph, truncate if too long
    summary = paragraphs[0]

    if len(summary) > 400:
        summary = summary[:400] + "..."

    return f"[Fallback summary] {summary}"


def summarize_sections(sections_yaml: str, markdown_file: str, output_file: str = None):
    """Generate summaries for all sections."""

    # Load sections data
    if not os.path.exists(sections_yaml):
        print(f"Error: Sections file not found: {sections_yaml}")
        sys.exit(1)

    if not os.path.exists(markdown_file):
        print(f"Error: Markdown file not found: {markdown_file}")
        sys.exit(1)

    with open(sections_yaml, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    sections = data['sections']
    print(f"Loaded {len(sections)} sections from {sections_yaml}")

    # Focus on major sections (level 2-3) for summarization
    # Level 1 is typically chapter title, too broad
    # Level 4+ are usually too granular
    major_sections = [s for s in sections if 2 <= s['level'] <= 3]

    print(f"Summarizing {len(major_sections)} major sections (levels 2-3)")

    # Generate summaries
    summaries = []
    total = len(major_sections)

    for idx, section in enumerate(major_sections, 1):
        print(f"[{idx}/{total}] Summarizing: {section['section_id']} - {section['heading']}")

        # Load content
        content = load_section_content(
            markdown_file,
            section['line_range'][0],
            section['line_range'][1]
        )

        # Generate summary
        summary = summarize_with_claude(section, content)

        summaries.append({
            'section_id': section['section_id'],
            'heading': section['heading'],
            'level': section['level'],
            'line_range': section['line_range'],
            'summary': summary,
            'age_groups_mentioned': section.get('age_groups_mentioned', []),
            'content_type': section.get('content_type', []),
            'completeness': section.get('completeness', 'unknown')
        })

        # Rate limiting - be nice to the API
        if HAS_ANTHROPIC and API_KEY and idx < total:
            time.sleep(1)

    # Generate output filename if not provided
    if not output_file:
        input_path = Path(sections_yaml)
        output_file = str(input_path.parent / f"{input_path.stem.replace('_sections', '')}_summaries.yaml")

    # Save summaries
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump({
            'source_sections': sections_yaml,
            'source_markdown': markdown_file,
            'total_summaries': len(summaries),
            'summaries': summaries
        }, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"\nSaved {len(summaries)} summaries to: {output_file}")

    # Print sample
    print("\n--- Sample Summaries ---")
    for summary in summaries[:3]:
        print(f"\n{summary['section_id']}: {summary['heading']}")
        print(f"  {summary['summary'][:200]}...")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    sections_yaml = sys.argv[1]
    markdown_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    summarize_sections(sections_yaml, markdown_file, output_file)
