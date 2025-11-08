#!/usr/bin/env python3
"""
Parallel document reorganization using Gemini with token tracking and cost estimation.

This modular script can reorganize any chapter/document by:
1. Loading a reorganization plan with new section structure
2. Feeding the full original document to Gemini in parallel for each section
3. Combining sections in the correct order
4. Tracking token usage and estimating costs

Usage:
    .venv/bin/python scripts/gemini_reorganize_parallel.py \\
        --input output/markdown/05_repaired/ch05_older_stage02.md \\
        --plan output/markdown/05_repaired/ch05_macro_analysis.md \\
        --output output/markdown/05_repaired/ch05_final.md \\
        --sections "5.1:Introduction,5.2:Guiding Principles,5.3:Group Sizes,..."

Or use a config file:
    .venv/bin/python scripts/gemini_reorganize_parallel.py --config reorganize_config.json
"""

import sys
import argparse
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Dict, Optional

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from gemini_api import call_gemini


# Gemini 2.5 Pro Pricing (as of 2025-01-09)
# Source: https://ai.google.dev/gemini-api/docs/pricing
PRICING = {
    'gemini-2.5-pro': {
        'input': 1.25 / 1_000_000,   # $1.25 per million tokens (≤200K context)
        'output': 10.00 / 1_000_000,  # $10.00 per million tokens
    },
    'gemini-2.5-pro-exp': {
        'input': 4.00 / 1_000_000,   # $4.00 per million tokens (preview)
        'output': 20.00 / 1_000_000,  # $20.00 per million tokens
    }
}


def get_nairobi_time():
    """Get current time in Nairobi timezone (UTC+3)."""
    utc_now = datetime.utcnow()
    nairobi_time = utc_now + timedelta(hours=3)
    return nairobi_time.strftime('%Y-%m-%d %H:%M:%S EAT')


def calculate_cost(input_tokens: int, output_tokens: int, model: str = 'gemini-2.5-pro') -> float:
    """
    Calculate API cost for given token usage.

    Args:
        input_tokens: Number of input (prompt) tokens
        output_tokens: Number of output (completion) tokens
        model: Model name for pricing lookup

    Returns:
        Estimated cost in USD
    """
    pricing = PRICING.get(model, PRICING['gemini-2.5-pro'])
    cost = (input_tokens * pricing['input']) + (output_tokens * pricing['output'])
    return cost


def setup_logging(output_file: Path) -> logging.Logger:
    """
    Set up parallel logging to file and stdout.

    Args:
        output_file: Output markdown file path (log will be sibling with .log extension)

    Returns:
        Configured logger
    """
    log_file = output_file.parent / f"{output_file.stem}.log"

    # Create logger
    logger = logging.getLogger('reorganize')
    logger.setLevel(logging.INFO)

    # Remove existing handlers
    logger.handlers = []

    # File handler
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger


def log_and_print(logger: logging.Logger, message: str):
    """Log message to both file and stdout."""
    logger.info(message)


def parse_sections(sections_str: str) -> List[Tuple[str, str]]:
    """
    Parse section structure from string.

    Format: "5.1:Introduction,5.2:Principles,5.3:Activities"
    Returns: [("5.1", "Introduction"), ("5.2", "Principles"), ...]
    """
    sections = []
    for item in sections_str.split(','):
        item = item.strip()
        if ':' in item:
            num, title = item.split(':', 1)
            sections.append((num.strip(), title.strip()))
    return sections


def generate_section_parallel(
    section_num: str,
    section_title: str,
    full_original_content: str,
    analysis_plan: str,
    is_first: bool,
    logger: logging.Logger,
    model: str = "gemini-2.5-pro",
    temperature: float = 0.2
) -> Dict:
    """
    Generate a section - designed to run in parallel.

    Returns:
        Dict with section_num, section_title, content, words, and usage stats
    """
    start_time = get_nairobi_time()
    log_and_print(logger, f"[{start_time}] Starting {section_num}: {section_title}")

    if is_first:
        prompt = f"""You are reorganizing a document according to a reorganization plan.

YOUR COMPLETE REORGANIZATION PLAN:
{analysis_plan}

---

COMPLETE ORIGINAL DOCUMENT (extract content from here):
{full_original_content}

---

TASK:
Generate Section {section_num}: {section_title}

This is the FIRST section, so:
1. Start with the main chapter/document title
2. Then create the complete section {section_num} with all subsections
3. Extract ALL relevant content from the original document
4. Follow your reorganization plan's structure exactly
5. Use proper hierarchical numbering ({section_num}.1, {section_num}.2, etc.)
6. Include ALL details, examples, and instructions - do NOT summarize
7. Use proper markdown headers (##, ###, ####, etc.)

OUTPUT: Return ONLY the reorganized markdown starting with the main title."""

    else:
        prompt = f"""You are reorganizing a document according to a reorganization plan.

YOUR COMPLETE REORGANIZATION PLAN:
{analysis_plan}

---

COMPLETE ORIGINAL DOCUMENT (extract content from here):
{full_original_content}

---

TASK:
Generate Section {section_num}: {section_title}

Requirements:
1. Extract ALL relevant content from the original document for this section
2. Follow your reorganization plan's structure exactly
3. Use proper hierarchical numbering ({section_num}.1, {section_num}.2, etc.)
4. Include ALL details, examples, and instructions - do NOT summarize
5. Use proper markdown headers (##, ###, ####, etc.)

OUTPUT: Return ONLY the reorganized markdown for section {section_num}. Do NOT include the main title."""

    # Call Gemini with usage tracking
    try:
        response = call_gemini(
            prompt,
            model=model,
            temperature=temperature,
            max_output_tokens=50000,
            return_usage=True
        )

        content = response['text']
        usage = response['usage']
        words = len(content.split())

        # Calculate cost
        cost = calculate_cost(
            usage['prompt_tokens'],
            usage['completion_tokens'],
            model
        )

        end_time = get_nairobi_time()
        log_and_print(
            logger,
            f"[{end_time}] ✓ {section_num}: {words:,} words | "
            f"Tokens: {usage['prompt_tokens']:,}in + {usage['completion_tokens']:,}out = {usage['total_tokens']:,} | "
            f"Cost: ${cost:.4f}"
        )

        return {
            'section_num': section_num,
            'section_title': section_title,
            'content': content,
            'words': words,
            'usage': usage,
            'cost': cost,
            'success': True
        }

    except Exception as e:
        end_time = get_nairobi_time()
        log_and_print(logger, f"[{end_time}] ✗ Failed {section_num}: {e}")
        return {
            'section_num': section_num,
            'section_title': section_title,
            'content': "",
            'words': 0,
            'usage': {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0},
            'cost': 0.0,
            'success': False
        }


def reorganize_document(
    input_file: Path,
    plan_file: Path,
    output_file: Path,
    sections: List[Tuple[str, str]],
    model: str = "gemini-2.5-pro",
    temperature: float = 0.2,
    max_workers: int = 8
) -> bool:
    """
    Reorganize a document by processing sections in parallel.

    Args:
        input_file: Path to original document
        plan_file: Path to reorganization plan
        output_file: Path for output
        sections: List of (section_num, section_title) tuples
        model: Gemini model to use
        temperature: Sampling temperature
        max_workers: Maximum parallel API calls

    Returns:
        True if successful, False otherwise
    """
    # Set up logging
    logger = setup_logging(output_file)

    log_and_print(logger, "="*80)
    log_and_print(logger, "Parallel Document Reorganization with Token Tracking")
    log_and_print(logger, "="*80)
    log_and_print(logger, f"Started: {get_nairobi_time()}")
    log_and_print(logger, f"Input: {input_file}")
    log_and_print(logger, f"Plan: {plan_file}")
    log_and_print(logger, f"Output: {output_file}")
    log_and_print(logger, f"Log: {output_file.parent / f'{output_file.stem}.log'}")
    log_and_print(logger, f"Sections: {len(sections)}")
    log_and_print(logger, f"Model: {model}")
    log_and_print(logger, f"Max parallel workers: {max_workers}")
    log_and_print(logger, "")

    # Read files
    with open(input_file, 'r', encoding='utf-8') as f:
        original_content = f.read()

    with open(plan_file, 'r', encoding='utf-8') as f:
        analysis_plan = f.read()

    total_words = len(original_content.split())
    log_and_print(logger, f"Input words: {total_words:,}")
    log_and_print(logger, "")

    # Process sections in parallel
    log_and_print(logger, f"{'='*80}")
    log_and_print(logger, f"Processing {len(sections)} sections in parallel...")
    log_and_print(logger, f"{'='*80}\n")

    results = {}
    total_input_tokens = 0
    total_output_tokens = 0
    total_cost = 0.0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_section = {}
        for i, (section_num, section_title) in enumerate(sections):
            future = executor.submit(
                generate_section_parallel,
                section_num,
                section_title,
                original_content,
                analysis_plan,
                is_first=(i == 0),
                logger=logger,
                model=model,
                temperature=temperature
            )
            future_to_section[future] = (section_num, section_title)

        # Collect results as they complete
        for future in as_completed(future_to_section):
            result = future.result()
            section_num = result['section_num']
            results[section_num] = result

            # Accumulate totals
            if result['success']:
                total_input_tokens += result['usage']['prompt_tokens']
                total_output_tokens += result['usage']['completion_tokens']
                total_cost += result['cost']

    log_and_print(logger, "")
    log_and_print(logger, f"{'='*80}")
    log_and_print(logger, "All sections completed - combining...")
    log_and_print(logger, f"{'='*80}\n")

    # Combine sections in order
    combined_parts = []
    total_output_words = 0

    for section_num, section_title in sections:
        if section_num in results and results[section_num]['success']:
            content = results[section_num]['content'].strip()
            words = results[section_num]['words']

            # Remove markdown code fences if present
            if content.startswith("```markdown"):
                content = content[len("```markdown"):].strip()
            if content.endswith("```"):
                content = content[:-3].strip()

            combined_parts.append(content)
            total_output_words += words

            log_and_print(logger, f"  ✓ {section_num}: {section_title} ({words:,} words)")
        else:
            log_and_print(logger, f"  ✗ {section_num}: {section_title} (MISSING)")

    # Join all parts
    combined = "\n\n".join(combined_parts)

    # Clean up any remaining code fences
    if combined.startswith("```markdown"):
        combined = combined[len("```markdown"):].strip()
    if combined.endswith("```"):
        combined = combined[:-3].strip()

    # Write output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(combined)

    # Final report
    size_kb = output_file.stat().st_size / 1024

    log_and_print(logger, "")
    log_and_print(logger, "="*80)
    log_and_print(logger, "✓ REORGANIZATION COMPLETE!")
    log_and_print(logger, "="*80)
    log_and_print(logger, f"Completed: {get_nairobi_time()}")
    log_and_print(logger, "")
    log_and_print(logger, "Output Metrics:")
    log_and_print(logger, f"  File: {output_file}")
    log_and_print(logger, f"  Size: {size_kb:.1f} KB")
    log_and_print(logger, f"  Words: {total_output_words:,}")
    log_and_print(logger, f"  Word retention: {total_output_words / total_words * 100:.1f}%")
    log_and_print(logger, "")
    log_and_print(logger, "Token Usage:")
    log_and_print(logger, f"  Input tokens: {total_input_tokens:,}")
    log_and_print(logger, f"  Output tokens: {total_output_tokens:,}")
    log_and_print(logger, f"  Total tokens: {total_input_tokens + total_output_tokens:,}")
    log_and_print(logger, "")
    log_and_print(logger, f"Estimated Cost: ${total_cost:.4f}")
    log_and_print(logger, f"  ({model} @ ${PRICING[model]['input']*1_000_000:.2f}/M in, ${PRICING[model]['output']*1_000_000:.2f}/M out)")
    log_and_print(logger, "="*80)

    return True


def load_config(config_file: Path) -> Dict:
    """Load configuration from JSON file."""
    with open(config_file, 'r') as f:
        return json.load(f)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Reorganize documents in parallel using Gemini with token tracking",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Config file option
    parser.add_argument(
        '--config',
        type=Path,
        help="JSON config file with all parameters"
    )

    # Individual parameters
    parser.add_argument(
        '--input',
        type=Path,
        help="Input document file"
    )
    parser.add_argument(
        '--plan',
        type=Path,
        help="Reorganization plan file"
    )
    parser.add_argument(
        '--output',
        type=Path,
        help="Output file path"
    )
    parser.add_argument(
        '--sections',
        type=str,
        help='Section structure: "5.1:Intro,5.2:Principles,5.3:Activities"'
    )
    parser.add_argument(
        '--model',
        default="gemini-2.5-pro",
        help="Gemini model to use (default: gemini-2.5-pro)"
    )
    parser.add_argument(
        '--temperature',
        type=float,
        default=0.2,
        help="Sampling temperature (default: 0.2)"
    )
    parser.add_argument(
        '--max-workers',
        type=int,
        default=8,
        help="Maximum parallel API calls (default: 8)"
    )

    args = parser.parse_args()

    # Load from config if provided
    if args.config:
        config = load_config(args.config)
        input_file = Path(config['input'])
        plan_file = Path(config['plan'])
        output_file = Path(config['output'])
        sections = parse_sections(config['sections'])
        model = config.get('model', 'gemini-2.5-pro')
        temperature = config.get('temperature', 0.2)
        max_workers = config.get('max_workers', 8)
    else:
        # Use command line args
        if not all([args.input, args.plan, args.output, args.sections]):
            parser.error("--input, --plan, --output, and --sections are required (or use --config)")

        input_file = args.input
        plan_file = args.plan
        output_file = args.output
        sections = parse_sections(args.sections)
        model = args.model
        temperature = args.temperature
        max_workers = args.max_workers

    # Validate files exist
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    if not plan_file.exists():
        print(f"Error: Plan file not found: {plan_file}", file=sys.stderr)
        sys.exit(1)

    if not sections:
        print("Error: No sections defined", file=sys.stderr)
        sys.exit(1)

    # Run reorganization
    try:
        success = reorganize_document(
            input_file=input_file,
            plan_file=plan_file,
            output_file=output_file,
            sections=sections,
            model=model,
            temperature=temperature,
            max_workers=max_workers
        )
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print(f"\n\nInterrupted by user at {get_nairobi_time()}. Exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"\nError at {get_nairobi_time()}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
