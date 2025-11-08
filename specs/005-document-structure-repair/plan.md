# Implementation Plan: Document Structure Repair

**Branch**: `005-document-structure-repair` | **Date**: 2025-11-06 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/005-document-structure-repair/spec.md`

## Summary

This feature repairs structural issues in processed markdown documents from the EL manual PDF extraction pipeline. The system will:
1. Restore missing Chapter 5 content by analyzing and merging source files
2. Apply context-aware hierarchical section numbering throughout all documents
3. Repair bullet list formatting to reflect proper semantic hierarchy

The technical approach uses Python-based markdown analysis and transformation, building on existing document processing infrastructure.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: markdown, pdfplumber, PyPDF2, sentence-transformers, regex, python-docx
**Storage**: File-based markdown documents in `output/markdown/` with staged processing directories
**Testing**: pytest for unit and integration tests
**Target Platform**: Linux server (development and production)
**Project Type**: Single project with standalone processing scripts
**Performance Goals**: Process all 10 chapters in under 5 minutes, maintain 100% content fidelity
**Constraints**: Must preserve all original content, cross-references, and formatting; no content loss allowed
**Scale/Scope**: 10 chapters (~500KB total markdown), hierarchical sections up to 6 levels deep, ~200 bullet lists

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Research Gates

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| I. Documentation-First | Feature README and spec updates | ✓ PASS | Spec created, will add feature README during implementation |
| II. Virtual Environment | Use `.venv/bin/python` for all scripts | ✓ PASS | Following existing project standard |
| III. Spec-Driven Development | Spec exists and validated | ✓ PASS | Spec validated with all checklists passed |
| IV. Document Processing Standards | Output clearly versioned, scripts organized | ✓ PASS | Will use stage 05 directory for output |

### Design Complexity Assessment

**Complexity Level**: Low-Medium
- Builds on existing document processing pipeline (stages 00-04)
- Uses standard markdown parsing and transformation patterns
- No new external dependencies required
- Straightforward file-based processing workflow

**Justification**: Feature aligns with existing architecture and adds no unnecessary complexity.

## Project Structure

### Documentation (this feature)

```text
specs/005-document-structure-repair/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── checklists/          # Quality validation checklists
│   └── requirements.md  # Spec quality checklist (completed)
└── spec.md              # Feature specification
```

### Source Code (repository root)

```text
scripts/
├── fix_pdf_issues.py           # Existing: Fix markdown for PDF generation
├── pdf_generator.py            # Existing: Generate PDFs from markdown
├── analyze_chapter5.py         # NEW: Analyze Chapter 5 content completeness
├── repair_section_numbering.py # NEW: Fix hierarchical section numbering
├── repair_bullet_hierarchy.py  # NEW: Fix bullet list formatting
└── validate_structure.py       # NEW: Validate document structure post-repair

output/markdown/
├── 00_raw/                     # Existing: Raw extracted chapters
├── 02_removedbullets/          # Existing: Bullets removed
├── 03_edited/                  # Existing: Edited content
├── 04_merged/                  # Existing: Merged chapters
└── 05_repaired/                # NEW: Structure-repaired chapters
    ├── chapter_00.md
    ├── chapter_01.md
    ├── chapter_02.md
    ├── chapter_03.md
    ├── chapter_04.md
    ├── chapter_05.md           # Restored complete content
    ├── chapter_07.md
    ├── chapter_08.md
    ├── chapter_09.md
    ├── REPAIR_REPORT.md        # Detailed repair actions taken
    └── VALIDATION_REPORT.md    # Structure validation results

tests/
├── test_chapter5_restore.py    # NEW: Test Chapter 5 content restoration
├── test_section_numbering.py   # NEW: Test section numbering logic
├── test_bullet_repair.py       # NEW: Test bullet hierarchy repair
└── test_validation.py          # NEW: Test structure validation
```

**Structure Decision**: Single project structure is appropriate for this document processing pipeline. Scripts are standalone utilities that process markdown files through staged directories. Each stage builds on the previous, maintaining a clear data lineage.

## Complexity Tracking

> No constitution violations - table not needed

---

## Post-Design Constitution Check

*Re-evaluated after Phase 1 design completion*

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| I. Documentation-First | Spec, plan, research, data-model, quickstart complete | ✓ PASS | All design docs generated |
| II. Virtual Environment | Scripts will use `.venv/bin/python` | ✓ PASS | Consistent with existing scripts |
| III. Spec-Driven Development | Following spec-kit workflow | ✓ PASS | Using /speckit.plan → /speckit.tasks → /speckit.implement |
| IV. Document Processing Standards | Output in stage 05_repaired/ | ✓ PASS | Follows existing stage pattern |

**Design Complexity Re-Assessment**: Still Low-Medium
- Design confirms simple, focused approach
- No architectural surprises
- Standard Python processing scripts
- Clean separation of concerns (analyze, repair, validate)

**No new concerns identified in design phase.**

---

## Phase 0 & 1 Completion Summary

### Phase 0: Research (✓ Complete)
- **File**: `research.md`
- **Decisions Made**:
  - Structure analysis: Hybrid regex + custom approach
  - Section numbering: Stream-based single-pass algorithm
  - Bullet hierarchy: Context-aware detection
  - Chapter 5 restoration: Content comparison approach
  - Dependencies: Standard library only (no new deps)

### Phase 1: Design (✓ Complete)
- **File**: `data-model.md` - Entities and relationships defined
- **File**: `quickstart.md` - User guide for running scripts
- **Agent Context**: Updated with Python 3.11 and document processing details

**All NEEDS CLARIFICATION items resolved.**

**Ready for Phase 2**: `/speckit.tasks` to generate task breakdown
