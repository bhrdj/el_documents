# Implementation Plan: Reformat EL Caregiver Manual

**Feature**: `001-reformat-manual` | **Date**: 2025-11-05 | **Spec**: [spec.md](./spec.md)

## Summary

Systematically reformat all chapters of the EL Caregiver Manual (EL_CgManual_CURRENT_v016.pdf) to match the formatting style established in Chapter 0 and Chapter 2, using vanilla markdown output. The process involves: (1) analyzing template chapters to document formatting patterns, (2) extracting content from PDF, (3) applying formatting template chapter-by-chapter or section-by-section, (4) validating output for consistency and content fidelity.

## Technical Context

**Language/Version**: Python 3.11 (using .venv/bin/python)
**Primary Dependencies**: PyPDF2 or pdfplumber (PDF extraction), markdown validation tools
**Storage**: Filesystem - input PDF, output markdown files per chapter
**Testing**: Manual validation against source PDF and formatting template
**Target Platform**: Linux development environment
**Project Type**: Single - document processing scripts
**Performance Goals**: Process entire manual in < 30 minutes
**Constraints**: Must preserve 100% content fidelity, vanilla markdown only
**Scale/Scope**: ~10-15 chapters, varying sizes from a few pages to 20+ pages

## Constitution Check

✅ **Documentation-First**: This plan document and spec created before implementation
✅ **Virtual Environment**: All Python execution via `.venv/bin/python`
✅ **Spec-Driven Development**: Following spec-kit workflow
✅ **Version Control**: All scripts and output markdown will be version controlled
❌ **Not Applicable**: No libraries being created (one-off processing task)

## Project Structure

### Documentation (this feature)

```text
specs/001-reformat-manual/
├── spec.md              # Feature specification
├── plan.md              # This file - implementation plan
├── formatting-guide.md  # Extracted from Chapter 0 and Chapter 2 analysis
└── tasks.md             # Task breakdown (to be created)
```

### Source Code (repository root)

```text
scripts/
└── reformat_manual/
    ├── extract_pdf.py           # Extract text/structure from PDF
    ├── analyze_template.py      # Analyze Chapter 0 and 2, output formatting guide
    ├── reformat_chapter.py      # Apply formatting template to single chapter
    ├── validate_output.py       # Validate markdown output
    └── utils/
        ├── pdf_utils.py         # PDF extraction utilities
        └── markdown_utils.py    # Markdown formatting utilities

output/
└── reformatted_manual/
    ├── chapter_00.md
    ├── chapter_01.md
    ├── chapter_02.md
    └── [... additional chapters]

requirements.txt             # Updated with PDF processing dependencies
```

**Structure Decision**: Simple script-based approach with utilities. No complex framework needed for one-time document processing. Scripts can be run individually or orchestrated manually.

## Implementation Approach

### Phase 0: Analysis & Template Extraction

**Objective**: Analyze Chapter 0 and Chapter 2 to document the target formatting template.

**Tasks**:
1. Extract Chapter 0 and Chapter 2 from PDF
2. Analyze formatting patterns:
   - Heading hierarchy (H1, H2, H3 levels)
   - List styles (bullet, numbered, indentation)
   - Table formatting
   - Spacing between elements
   - Typography (bold, italic, emphasis patterns)
3. Document findings in `specs/001-reformat-manual/formatting-guide.md`
4. Note unicode bracket occurrences and preservation strategy
5. Validate template against both chapters for consistency

**Deliverables**:
- `formatting-guide.md` - Complete formatting template documentation
- `scripts/reformat_manual/analyze_template.py` - Script to extract and document patterns

---

### Phase 1: PDF Extraction Infrastructure

**Objective**: Build reliable PDF content extraction that preserves structure.

**Tasks**:
1. Research PDF extraction libraries (PyPDF2, pdfplumber, pdfminer)
2. Implement `pdf_utils.py` with functions:
   - Extract text by chapter/page
   - Detect headings, lists, tables
   - Preserve unicode characters (including brackets)
3. Implement `extract_pdf.py` to extract full manual by chapter
4. Validate extraction preserves all content including unicode brackets
5. Test extraction on Chapter 0 and Chapter 2 specifically

**Deliverables**:
- `scripts/reformat_manual/utils/pdf_utils.py` - PDF extraction utilities
- `scripts/reformat_manual/extract_pdf.py` - Main extraction script
- Extracted chapter text files (intermediate format)

---

### Phase 2: Formatting Application

**Objective**: Apply formatting template to produce vanilla markdown output.

**Tasks**:
1. Implement `markdown_utils.py` with functions:
   - Apply heading formatting based on template
   - Format lists (bullets, numbering, indentation)
   - Format tables in markdown
   - Apply spacing rules
   - Preserve unicode brackets
2. Implement `reformat_chapter.py`:
   - Read extracted chapter content
   - Apply formatting template rules
   - Output vanilla markdown
   - Log any formatting decisions or warnings
3. Test on Chapter 0 and Chapter 2 first (should match source closely)
4. Process remaining chapters systematically

**Deliverables**:
- `scripts/reformat_manual/utils/markdown_utils.py` - Markdown formatting utilities
- `scripts/reformat_manual/reformat_chapter.py` - Chapter reformatting script
- `output/reformatted_manual/` directory with all chapters as .md files

---

### Phase 3: Validation & Quality Assurance

**Objective**: Ensure 100% content fidelity and formatting consistency.

**Tasks**:
1. Implement `validate_output.py`:
   - Check vanilla markdown validity (no HTML, no extended syntax)
   - Validate heading hierarchy consistency
   - Check list formatting consistency
   - Validate unicode bracket preservation
2. Manual review:
   - Compare each chapter against source PDF
   - Verify no content additions/deletions/modifications
   - Check formatting matches template
3. Document any edge cases or manual adjustments needed
4. Fix any validation failures

**Deliverables**:
- `scripts/reformat_manual/validate_output.py` - Validation script
- Validation report documenting any issues and resolutions
- Final, validated markdown chapters in `output/reformatted_manual/`

---

## Execution Pattern

All Python scripts must be executed using the virtual environment:

```bash
.venv/bin/python scripts/reformat_manual/analyze_template.py
.venv/bin/python scripts/reformat_manual/extract_pdf.py
.venv/bin/python scripts/reformat_manual/reformat_chapter.py --chapter 0
.venv/bin/python scripts/reformat_manual/validate_output.py
```

## Dependencies to Install

Add to `requirements.txt`:
```
pdfplumber>=0.10.0      # PDF text extraction with layout
PyPDF2>=3.0.0           # PDF manipulation
markdown>=3.5           # Markdown validation
```

Install via:
```bash
source .venv/bin/activate
pip install pdfplumber PyPDF2 markdown
pip freeze > requirements.txt
```

## Success Validation

**Phase 0 Complete When**:
- Formatting guide document exists and is comprehensive
- Both Chapter 0 and Chapter 2 patterns are documented
- Unicode bracket handling strategy is documented

**Phase 1 Complete When**:
- PDF extraction successfully extracts all chapters
- Extracted content includes all text, structure, and unicode characters
- Test extraction on Chapter 0 and 2 shows 100% content fidelity

**Phase 2 Complete When**:
- All chapters are reformatted to markdown
- Chapter 0 and 2 markdown closely matches source formatting
- All output is valid vanilla markdown

**Phase 3 Complete When**:
- All validation checks pass
- Manual review confirms content fidelity
- Formatting consistency validated across all chapters
- Unicode brackets preserved in all instances

## Risk Mitigation

**Risk**: PDF extraction loses formatting information
- **Mitigation**: Test multiple libraries (pdfplumber, PyPDF2), choose best
- **Fallback**: Manual formatting rules based on template analysis

**Risk**: Complex tables don't translate well to markdown
- **Mitigation**: Document table patterns in template, use markdown table syntax
- **Fallback**: Simplify table layout to work within markdown constraints

**Risk**: Unicode brackets or special characters get corrupted
- **Mitigation**: Use UTF-8 encoding throughout, test preservation early
- **Fallback**: Manual review and correction of special characters

**Risk**: Inconsistent source formatting makes template application difficult
- **Mitigation**: Document variations, create rules for each pattern
- **Fallback**: Manual review and adjustment of problematic sections

## Out of Scope (Per Specification)

- Removing or modifying unicode brackets
- Content editing or improvement
- PDF generation from markdown
- Automated content accuracy validation
- Translation or localization
