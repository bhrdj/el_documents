# PDF Generation Pipeline

**Location**: `scripts/pdf_generator.py`
**Last Updated**: 2025-11-06

## Overview

The PDF generation pipeline converts processed markdown chapters into PDFs using pandoc with comprehensive preprocessing to handle LaTeX compatibility issues.

## Quick Start

```bash
# Generate PDFs for all chapters
.venv/bin/python scripts/pdf_generator.py
```

Output PDFs are written to `output/pdfs/`.

## Preprocessing Pipeline

The `preprocess_markdown()` function automatically applies these fixes:

### 1. Deep List Nesting Limitation
- **Problem**: LaTeX has a maximum list nesting depth of ~5 levels
- **Solution**: Automatically limits nesting to 4 levels
- **Implementation**: `fix_deep_nesting()` reduces indent for items beyond max depth

### 2. Unicode Emoji and Symbol Stripping
- **Problem**: LaTeX doesn't support emoji and many Unicode symbols (📚, ⬅, ★, etc.)
- **Solution**: Comprehensive character-by-character filtering
- **Approach**:
  - Keeps basic ASCII (0x0000-0x007F)
  - Keeps Latin-1 Supplement (0x0080-0x00FF)
  - Replaces emoji and symbols with `[symbol]`
  - Smart quotes handled separately (see below)

### 3. Smart Quotes and Special Punctuation
- **Replacements**:
  - `–` (en dash) → `--`
  - `—` (em dash) → `---`
  - `"` `"` (smart quotes) → `"`
  - `'` `'` (smart apostrophes) → `'`
  - `…` (ellipsis) → `...`

### 4. Unicode Brackets
- **Replacements**:
  - `˹` → `[`
  - `˺` → `]`
- **Note**: These brackets are content markers preserved through earlier pipeline stages

### 5. YAML Metadata Parsing Issues
- **Problem**: Patterns like `**Purpose**: text` at file start cause YAML parse errors
- **Solution**: Two-pronged approach:
  1. Remove incomplete YAML delimiters (`---\n\n` at file start)
  2. Disable pandoc YAML parsing with `--from markdown-yaml_metadata_block`

## Input Source Configuration

Chapter files are sourced from different pipeline stages:

| Chapter | Source Directory | Notes |
|---------|------------------|-------|
| 0 | `03_edited/` | Manually edited |
| 1 | `05_repaired/` | Structure repairs applied |
| 2-3 | `02_removedbullets/` | Unicode bullets converted |
| 4-5 | `05_repaired/` | Structure repairs applied |
| 7-8 | `03_edited/` | Manually edited |
| 9 | `02_removedbullets/` | Unicode bullets converted |

To modify sources, edit the `chapters` list in `main()`.

## Pandoc Configuration

```bash
pandoc \
  --from markdown-yaml_metadata_block \  # Disable YAML metadata parsing
  input.md \
  -o output.pdf \
  -V geometry:margin=1in \               # 1 inch margins
  -V fontsize=11pt \                     # 11pt font
  --toc \                                # Generate table of contents
  --number-sections                      # Auto-number sections
```

## Temporary Files

During generation, preprocessed temporary files are created:
- Location: Same directory as input file
- Pattern: `{chapter_name}_temp.md`
- Cleanup: Automatic deletion after PDF generation

## Error Handling

The script reports:
- Success: `✓ Generated: chapter_XX.pdf`
- Failure: `Error generating PDF for ...` with pandoc error details
- Summary: Total success/failure counts

## Known Issues

### Chapter 1 Generation Failure
- **Status**: Process killed (exit code -9)
- **Likely Cause**: Memory/resource exhaustion during LaTeX compilation
- **Impact**: Low - older PDF exists from previous successful run
- **Investigation**: May need to split chapter or increase system resources

## Integration with Feature 005

This pipeline was enhanced during feature `005-document-structure-repair`:
- Consolidated fixes from separate `fix_pdf_issues.py` script
- Added comprehensive Unicode stripping
- Improved YAML parsing handling
- All fixes now automatic in main pipeline

## Related Documentation

- `output/markdown/README.md` - Chapter processing pipeline stages
- `specs/005-document-structure-repair/` - Structure repair feature
- `scripts/fix_unicode_bullets.py` - Unicode bullet conversion utility

## Troubleshooting

### "Unicode character X not set up for use with LaTeX"
- **Cause**: New emoji/symbol not caught by filter
- **Fix**: Update `strip_problematic_unicode()` function or add specific replacement

### "YAML parse exception"
- **Cause**: File starts with pattern that looks like YAML
- **Fix**: Verify `--from markdown-yaml_metadata_block` flag is present

### Memory issues (process killed)
- **Cause**: Large file or complex LaTeX rendering
- **Fix**: Split chapter or increase system memory

### Empty PDFs
- **Cause**: All content stripped by preprocessing
- **Fix**: Check preprocessing logic, ensure content preserved

## Future Enhancements

- [ ] Parallel PDF generation for faster processing
- [ ] Custom font configuration for better Unicode support
- [ ] Configurable preprocessing rules
- [ ] Better error reporting with line numbers
- [ ] Support for other output formats (HTML, EPUB)
