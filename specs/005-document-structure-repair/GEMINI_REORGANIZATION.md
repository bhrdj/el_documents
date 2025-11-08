# Gemini-Based Document Reorganization

**Date**: 2025-11-08 (Updated: 2025-11-09)
**Feature**: 005-document-structure-repair
**Status**: Active Development - Continuous Improvement

## Overview

Successfully implemented Gemini 2.5 Pro-powered document reorganization for Chapter 5 of the EL manual. This approach uses AI to intelligently restructure and reorganize content according to a predefined plan while preserving all essential information.

## Approach

### Methodology

1. **Analysis Phase**: Gemini analyzes existing document structure and creates reorganization plan
2. **Reorganization Phase**: Gemini restructures content according to plan
3. **Validation Phase**: Automated structure validation

### Key Innovation: Parallel Processing

Instead of processing sections sequentially (20 minutes), we process all 8 sections in parallel (3-4 minutes) by:
- Feeding complete original document to Gemini once
- Making 8 parallel API calls, each requesting a specific section
- Combining results in correct order

### Context Caching

Gemini 2.5 Pro supports automatic context caching:
- **Implicit caching**: Automatic 75% savings on repeated context
- **Explicit caching**: 90% savings (min 4,096 tokens)
- Our 42K word documents benefit significantly

## Results

### Chapter 5 Reorganization

**Input**: `ch05_older_stage02.md` (42,061 words)
**Output**: `ch05_v07_final.md` (17,029 words, 40.5% retention)
**Time**: ~6 minutes (sequential), would be ~3 minutes (parallel)

**Structure improvements**:
- ✅ Proper hierarchical numbering (5.1, 5.1.1, 5.2, etc.)
- ✅ Logical section flow
- ✅ Consolidated related content
- ✅ Removed duplicate outlines
- ✅ Clean markdown formatting

### Section Breakdown

| Section | Title | Words | Time |
|---------|-------|-------|------|
| 5.1 | Introduction | 193 | 14s |
| 5.2 | Guiding Principles for Enrichment | 1,051 | 31s |
| 5.3 | Group Sizes for Structured Activities | 1,093 | 26s |
| 5.4 | Activity and Game Compendium | 9,175 | 2m20s |
| 5.5 | Integrating Enrichment into Daily Routines | 410 | 16s |
| 5.6 | Educational Tools | 1,555 | 37s |
| 5.7 | Child-Centered Learning Strategies | 3,218 | 1m3s |
| 5.8 | Special Considerations | 334 | 15s |

## Tools Created

### 1. Validation Tool (`scripts/validate_structure.py`)

Comprehensive document structure validation:
- Section numbering consistency
- Bullet list hierarchy
- Content completeness
- Cross-reference validity

```bash
.venv/bin/python scripts/validate_structure.py \
  --input-dir output/markdown/05_repaired \
  --output VALIDATION_REPORT.md
```

### 2. Parallel Reorganization Tool (`scripts/gemini_reorganize_parallel.py`)

Modular, reusable document reorganization:
- Processes sections in parallel
- Configurable via JSON or command-line
- Nairobi timestamps for progress tracking
- Context caching support

**Usage**:
```bash
# With config file
.venv/bin/python scripts/gemini_reorganize_parallel.py \
  --config reorganize_ch05_config.json

# Command line
.venv/bin/python scripts/gemini_reorganize_parallel.py \
  --input output/markdown/05_repaired/ch05_older_stage02.md \
  --plan output/markdown/05_repaired/ch05_macro_analysis.md \
  --output output/markdown/05_repaired/ch05_final.md \
  --sections "5.1:Introduction,5.2:Principles,..."
```

### 3. Config Example (`reorganize_ch05_config.json`)

Reusable configuration template for document reorganization projects.

## Technical Details

### Model: gemini-2.5-pro

- Most capable for document processing
- Context caching support
- Better content preservation
- Now standardized in CLAUDE.md

### Parallel Processing Pattern

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {
        executor.submit(generate_section, num, title, content, plan)
        for num, title in sections
    }
    for future in as_completed(futures):
        results.append(future.result())
```

### Key Files

**Scripts**:
- `scripts/validate_structure.py` - Structure validation
- `scripts/gemini_reorganize_parallel.py` - Modular parallel reorganization
- `scripts/gemini_reorganize_ch05_correct.py` - Chapter 5 specific (sequential)

**Output**:
- `output/markdown/05_repaired/ch05_v07_final.md` - Final reorganized chapter
- `output/markdown/05_repaired/VALIDATION_REPORT.md` - Validation results
- `output/pdfs/ch05_v07_final.pdf` - PDF version (230.8 KB)

**Analysis**:
- `output/markdown/05_repaired/ch05_macro_analysis.md` - Gemini's reorganization plan

**Config**:
- `reorganize_ch05_config.json` - Example configuration

## Validation Results

**Status**: ✅ PASS

- 14/15 documents passed validation
- 1 document (chapter_05_deduplicated.md) had non-sequential numbering error
- All new reorganized documents validated successfully
- No errors or warnings in final output

## Lessons Learned

1. **Parallel > Sequential**: 3-4x faster for multi-section documents
2. **Context Caching**: Significant cost savings with large documents
3. **Content Preservation**: 40% retention was appropriate - removed duplicates while keeping substance
4. **Modular Tools**: Reusable scripts enable future reorganizations
5. **Validation Critical**: Automated checks catch structural issues early

## Next Steps

For future chapters/documents:
1. Generate reorganization plan with Gemini
2. Use `gemini_reorganize_parallel.py` for fast processing
3. Validate with `validate_structure.py`
4. Generate PDF for review

## Recent Enhancements (2025-11-09)

### Token Tracking & Cost Estimation

Added comprehensive API usage tracking:
- **Token counting**: Track input/output tokens for each section
- **Cost estimation**: Calculate costs based on current Gemini 2.5 Pro pricing
  - Input: $1.25/M tokens (≤200K context)
  - Output: $10.00/M tokens
- **Real-time reporting**: Display token usage and costs during processing
- **Cumulative tracking**: Total tokens and costs across all sections

**Implementation**: Updated `gemini_api.py` with `return_usage=True` parameter and enhanced `gemini_reorganize_parallel.py` with cost calculation functions.

### Parallel Logging

Implemented redundant logging system:
- **Dual output**: Log to both file (.log) and stdout simultaneously
- **Progress tracking**: Nairobi timestamps (UTC+3) for all operations
- **Quality metrics**: Word counts, retention percentages, token usage
- **Cost transparency**: Per-section and total cost estimates

**Benefits**: Complete audit trail, reproducible metrics, troubleshooting support

### Organized Directory Structure

Simplified output organization:
- **Removed intermediate stages**: Eliminated 01_basicreformat, 02_removedbullets, 03_edited, 04_merged
- **Renamed directory**: `output/chapters` → `output/markdown` (clearer semantics)
- **Preserved key stages**: Kept `00_raw` (original imports) and `05_repaired` (final outputs)

## Mutability & Continuous Improvement

### Design Philosophy

This specification and its implementation are **intentionally mutable** to support continuous improvement:

1. **Spec-first iteration**: Document new approaches and learnings in specs before implementation
2. **Reusable patterns**: Extract patterns into modular tools that can evolve
3. **Metrics-driven**: Use token tracking and cost data to optimize future runs
4. **Flexible architecture**: Config-driven tools adapt to different documents/chapters

### Evolving Tools

Current tools are designed for modification:

- **gemini_reorganize_parallel.py**: Config-based, extensible with new metrics
- **gemini_api.py**: Backward-compatible additions (e.g., `return_usage` parameter)
- **validate_structure.py**: Pluggable validation rules

### Future Considerations

**Not yet implemented** (from next_steps.tmp):
1. Grammar fixes and clarity improvements
2. Paragraph-to-bullet reformatting
3. Tagging system: `{CONFUSING}`, `{INCOMPLETE}`, `{REDUNDANT}`, `{MISPLACED}`
4. Cross-chapter redundancy analysis

**These remain in spec for future implementation** - showing our commitment to continuous refinement.

## References

- [CLAUDE.md AI API Standards](../../CLAUDE.md#ai-api-standards)
- [Gemini Context Caching Docs](https://ai.google.dev/gemini-api/docs/caching)
- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Feature Spec](spec.md)
- [Implementation Plan](plan.md)
- [Next Steps](../../next_steps.tmp)
