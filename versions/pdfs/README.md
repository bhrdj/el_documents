# PDF Chapter Exports

**Generated**: 2025-11-06
**Source**: Latest versions from processing pipeline

## Successfully Generated PDFs

| Chapter | File | Size | Source |
|---------|------|------|--------|
| 00 | `chapter_00.pdf` | 106K | `03_edited/chapter_00.md` |
| 02 | `chapter_02.pdf` | 153K | `02_removedbullets/chapter_02.md` |
| 03 | `chapter_03.pdf` | 165K | `02_removedbullets/chapter_03.md` |
| 05 | `chapter_05.pdf` | 220K | `04_merged/chapter_05_deduplicated.md` |
| 07 | `chapter_07.pdf` | 110K | `03_edited/chapter_07.md` |
| 08 | `chapter_08.pdf` | 89K | `03_edited/chapter_08.md` |
| 09 | `chapter_09.pdf` | 139K | `02_removedbullets/chapter_09.md` |

**Total: 7 PDFs generated successfully**

## Alternative Formats

| Chapter | File | Size | Format | Source |
|---------|------|------|--------|--------|
| 04 | `chapter_04.html` | 79K | HTML | `04_merged/chapter_04.md` |

**Note**: Chapter 4 was generated as HTML due to deeply nested list structures that exceed LaTeX's nesting limits.

## Known Issues

### Chapter 01: Child Admission
**Status**: Not converted
**Source**: `output/chapters/02_removedbullets/chapter_01.md`
**Issue**: File complexity (283 headings, 52K) causes pandoc to exceed memory limits in the current environment.
**Workaround**: Use the source markdown file directly, or view in a markdown viewer.

### Chapter 04: Child Interaction Strategies
**Status**: HTML only
**Source**: `output/chapters/04_merged/chapter_04.md`
**Issue**: List structures nested beyond LaTeX's maximum depth (6 levels).
**Solution**: Generated as HTML (`chapter_04.html`) which handles unlimited nesting.

## Conversion Settings

PDFs were generated using pandoc with the following settings:
- **PDF Engine**: pdflatex (default)
- **Margins**: 1 inch on all sides
- **Font size**: 11pt
- **Table of Contents**: Included
- **Section numbering**: Enabled

## Source Files

### Latest Versions Used
Based on the processing pipeline, these are the most recent/processed versions:

- **Edited chapters** (Stage 03): Chapters 00, 07, 08
- **Merged chapters** (Stage 04): Chapters 04, 05
- **Formatted chapters** (Stage 02): Chapters 01, 02, 03, 09

### Pipeline Stages
1. **00_raw** - Raw PDF extraction
2. **02_removedbullets** - Unicode bullets → markdown
3. **03_edited** - Editorial improvements
4. **04_merged** - Chapter merging and deduplication

## Recommendations

### For Chapter 01
Consider one of these alternatives:
1. View the markdown file directly in a markdown viewer
2. Split into smaller sections and convert separately
3. Export to HTML with a simpler tool
4. Use on a system with more available memory

### For Chapter 04
- The HTML version (`chapter_04.html`) is fully functional and can be:
  - Viewed in any web browser
  - Printed to PDF from browser (File → Print → Save as PDF)
  - Converted with browser-based tools

## Regenerating PDFs

To regenerate these PDFs:

```bash
# Run the PDF generator script
.venv/bin/python scripts/pdf_generator.py

# Or manually for individual chapters
pandoc output/chapters/XX_stage/chapter_NN.md \
  -o output/pdfs/chapter_NN.pdf \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  --toc \
  --number-sections
```

## Scripts Used

- `scripts/pdf_generator.py` - Main PDF generation with Unicode preprocessing
- `scripts/fix_pdf_issues.py` - Fix deep nesting and Unicode issues

---

**Success Rate**: 7/9 PDFs (78%) + 1 HTML
**Total Coverage**: 8/9 chapters (89%)
