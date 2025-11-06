# Feature 005: Document Structure Repair

## Overview

This feature repairs structural issues in processed markdown documents from the EL manual PDF extraction pipeline:

1. **Restore Missing Chapter 5 Content** - Ensures all content from source files is present
2. **Section Hierarchy Numbering** - Applies consistent hierarchical numbering (1.0, 1.1, 1.1.1, etc.)
3. **Bullet List Formatting** - Fixes indentation and markers to match semantic hierarchy

## Status

**Branch**: `005-document-structure-repair`
**Status**: In Implementation
**Priority**: P1 (User Stories 1 & 2), P2 (User Story 3)

## Implementation

### Scripts

- `scripts/analyze_chapter5.py` - Analyze and restore Chapter 5 content
- `scripts/repair_section_numbering.py` - Fix hierarchical section numbering
- `scripts/repair_bullet_hierarchy.py` - Repair bullet list formatting
- `scripts/validate_structure.py` - Validate document structure
- `scripts/repair_all.py` - Run complete repair pipeline

### Library Modules

- `scripts/lib/document.py` - Document entity class
- `scripts/lib/section.py` - Section entity class
- `scripts/lib/hierarchy.py` - Hierarchy level state management
- `scripts/lib/bullet.py` - Bullet list entities
- `scripts/lib/parser.py` - Markdown parsing utilities
- `scripts/lib/validation.py` - Validation utilities
- `scripts/lib/reporting.py` - Report generation utilities
- `scripts/lib/content_comparison.py` - Content comparison for Chapter 5
- `scripts/lib/section_numbering.py` - Section numbering algorithm
- `scripts/lib/bullet_detection.py` - Bullet hierarchy detection
- `scripts/lib/bullet_repair.py` - Bullet hierarchy repair logic

### Output

All repaired documents are written to: `output/chapters/05_repaired/`

Reports generated:
- `CHAPTER_5_ANALYSIS.md` - Chapter 5 content analysis
- `REPAIR_REPORT.md` - Summary of all repairs
- `VALIDATION_REPORT.md` - Structure validation results

## Usage

See [quickstart.md](quickstart.md) for detailed usage instructions.

### Quick Start

```bash
# Run complete repair pipeline
.venv/bin/python scripts/repair_all.py

# Individual repairs
.venv/bin/python scripts/analyze_chapter5.py --restore
.venv/bin/python scripts/repair_section_numbering.py
.venv/bin/python scripts/repair_bullet_hierarchy.py
.venv/bin/python scripts/validate_structure.py
```

## Technical Details

- **Language**: Python 3.11
- **Dependencies**: Standard library only (no new packages required)
- **Architecture**: Single project with standalone processing scripts
- **Processing Model**: Stream-based single-pass algorithms for efficiency

## Documentation

- [spec.md](spec.md) - Feature specification with user stories
- [plan.md](plan.md) - Technical implementation plan
- [research.md](research.md) - Technical research and decisions
- [data-model.md](data-model.md) - Entity definitions and relationships
- [quickstart.md](quickstart.md) - User guide
- [tasks.md](tasks.md) - Implementation task breakdown

## Success Criteria

- ✓ All processed documents contain 100% of source content
- ✓ Section numbering follows consistent hierarchical pattern with zero errors
- ✓ Bullet lists display correct visual hierarchy
- ✓ Processing completes without manual intervention
- ✓ Automated validation passes with zero errors

## Related Features

- Feature 001: Reformat Manual
- Feature 002: Semantic Coherence Analysis
