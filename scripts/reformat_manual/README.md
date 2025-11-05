# EL Caregiver Manual Reformatting Scripts

Scripts for extracting and reformatting the EL Caregiver Manual from PDF to vanilla markdown.

## Current Status

**Phase Completed**: PDF Extraction (Phase 1)

- Chapter boundary detection implemented and tested
- All 10 chapters successfully extracted from `EL_CgManual_CURRENT_v016.pdf`
- Raw extractions stored in pipeline structure for multi-phase processing
- Batch extraction script created for reproducibility
- Chapter 8 split into separate chapters (8: Stories, 9: Relocations/Additions)

**Next Phase**: Basic Reformatting (Phase 2) - Apply formatting guide rules

## Pipeline Structure

```
output/chapters/
├── 00_raw/           # Raw PDF extractions (current)
│   ├── chapter_0.md
│   ├── chapter_1.md
│   ├── chapter_2.md
│   ├── chapter_3.md
│   ├── chapter_4.md
│   ├── chapter_5_part1.md
│   ├── chapter_5_part2.md
│   ├── chapter_7.md
│   ├── chapter_8.md
│   └── chapter_9.md
└── 01_basicreformat/ # Formatted chapters (planned)
```

## Scripts

### extract_pdf.py

Main PDF extraction script with multiple modes.

**Usage**:
```bash
# Detect chapter boundaries
.venv/bin/python scripts/reformat_manual/extract_pdf.py \
  EL_CgManual_CURRENT_v016.pdf \
  --find-chapters \
  --output output/chapter_boundaries.json

# Extract single chapter
.venv/bin/python scripts/reformat_manual/extract_pdf.py \
  EL_CgManual_CURRENT_v016.pdf \
  --chapter "CHAPTER 2 : CHILD CARE" \
  --start-page 9 \
  --end-page 30 \
  --output-text output/chapter_2.md

# Extract page range
.venv/bin/python scripts/reformat_manual/extract_pdf.py \
  EL_CgManual_CURRENT_v016.pdf \
  --start-page 0 \
  --end-page 10 \
  --output-text output/pages_0-10.txt
```

**Arguments**:
- `pdf_path`: Path to source PDF (required)
- `--find-chapters`: Detect chapter boundaries automatically
- `--chapter NAME`: Extract specific chapter by name
- `--start-page N`: Starting page (0-indexed)
- `--end-page N`: Ending page (0-indexed)
- `--output PATH`: Output path for JSON data
- `--output-text PATH`: Output path for text/markdown

### extract_all_chapters.py

Batch extraction script that processes all chapters based on detected boundaries.

**Usage**:
```bash
# Extract all chapters (requires chapter_boundaries.json)
.venv/bin/python scripts/reformat_manual/extract_all_chapters.py
```

**Behavior**:
- Reads `output/chapter_boundaries.json`
- Extracts all chapters to `output/chapters/00_raw/`
- Handles duplicate Chapter 5 as part1 and part2
- Reports progress for each chapter

### utils/pdf_utils.py

Core PDF extraction utilities.

**Functions**:
- `extract_chapter()`: Extract single chapter with metadata
- `extract_text_by_page()`: Extract text from page range
- `find_chapter_boundaries()`: Detect chapter markers in PDF (includes special handling for "RELOCATIONS, ADDITIONS" section)
- `preserve_unicode()`: Ensure unicode character preservation

**Chapter Detection**:
- Standard pattern: `CHAPTER N` or `Chapter N` (where N is a number or Roman numeral)
- Special case: `RELOCATIONS, ADDITIONS` detected as Chapter 9

## Chapter Structure

The manual contains **10 chapter sections** (out of order):

| File | Chapter | Title | Pages | Size | Lines |
|------|---------|-------|-------|------|-------|
| chapter_0.md | 0 | Front Matter | 2-8 | 7.1K | 125 |
| chapter_2.md | 2 | Child Care | 9-30 | 29K | 549 |
| chapter_3.md | 3 | Safety and Hygiene | 31-48 | 23K | 453 |
| chapter_4.md | 4 | Child Interaction Strategies | 49-89 | 50K | 987 |
| chapter_5_part1.md | 5.1 | Structured Enrichment (Part 1) | 90-198 | 136K | 2954 |
| chapter_5_part2.md | 5.2 | Structured Enrichment (Part 2) | 199-305 | 129K | 2705 |
| chapter_1.md | 1 | Child Admission | 306-346 | 53K | 1019 |
| chapter_7.md | 7 | Staff Staying in Daycare | 347-351 | 3.4K | 75 |
| chapter_8.md | 8 | Caregiver Challenge Stories | 352-353 | 3.1K | 41 |
| chapter_9.md | 9 | Relocations, Additions | 354-end | 32K | 605 |

**Notes**:
- Chapters appear out of numerical order in the source PDF. This is preserved in extraction.
- Chapter 8 was split from original extraction: Stories remain in ch8, Relocations/Additions moved to ch9.

## Dependencies

See `requirements.txt` for complete dependencies. Key libraries:

- `pdfplumber`: PDF text extraction with layout preservation
- `pypdf`: PDF metadata and structure handling

## Development Standards

All scripts follow project standards defined in `CLAUDE.md`:

- Virtual environment: `.venv/bin/python` for all execution
- Documentation-first: README and specs updated before commits
- Version control: All scripts and outputs tracked in git

## Related Documentation

- **Specification**: `specs/001-reformat-manual/spec.md`
- **Implementation Plan**: `specs/001-reformat-manual/plan.md`
- **Formatting Guide**: `specs/001-reformat-manual/formatting-guide.md`
- **Task List**: `specs/001-reformat-manual/tasks.md`

## Troubleshooting

**FontBBox warnings**: The PDF extraction generates warnings about font descriptors. These are non-fatal and do not affect text extraction quality.

**Chapter 6 missing**: The source PDF does not contain Chapter 6. This is not an extraction error.

**Chapter 5 split**: Chapter 5 is unusually large (265K total) and appears twice in the PDF. It's extracted as two parts for easier processing.
