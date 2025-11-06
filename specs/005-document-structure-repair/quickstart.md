# Quickstart: Document Structure Repair

**Feature**: 005-document-structure-repair
**Created**: 2025-11-06
**Purpose**: Quick guide for running document structure repair scripts

## Prerequisites

1. **Python Environment**: Ensure `.venv` virtual environment is set up
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Input Files**: Processed chapters must exist in `output/chapters/04_merged/`
   - Verify: `ls output/chapters/04_merged/chapter_*.md`

3. **Working Directory**: Run all commands from repository root

---

## Quick Start (Run All Repairs)

The complete repair pipeline processes all chapters in sequence:

```bash
# Run the complete repair pipeline
.venv/bin/python scripts/repair_all.py

# Output will be in output/chapters/05_repaired/
# Reports generated:
#   - REPAIR_REPORT.md (what was fixed)
#   - VALIDATION_REPORT.md (verification results)
```

**What it does**:
1. Analyzes Chapter 5 content completeness
2. Restores any missing Chapter 5 content
3. Renumbers all sections with correct hierarchy
4. Repairs bullet list formatting
5. Validates all repairs
6. Generates comprehensive reports

**Expected Duration**: 2-5 minutes for all 10 chapters

---

## Individual Repair Scripts

### 1. Analyze Chapter 5 Content

Check if Chapter 5 is complete or has missing content:

```bash
.venv/bin/python scripts/analyze_chapter5.py
```

**Output**:
```
Analyzing Chapter 5 content...
✓ Source part 1: 1,234 lines, 45 sections
✓ Source part 2: 987 lines, 32 sections
✓ Merged file: 2,100 lines, 73 sections

Status: MISSING CONTENT
Missing sections: 4 sections from part 2
Details: output/chapters/05_repaired/CHAPTER_5_ANALYSIS.md
```

**Options**:
- `--restore`: Automatically restore missing content
- `--output-dir PATH`: Specify output directory (default: output/chapters/05_repaired)
- `--verbose`: Show detailed section comparison

---

### 2. Repair Section Numbering

Fix hierarchical section numbering across all chapters:

```bash
.venv/bin/python scripts/repair_section_numbering.py
```

**Output**:
```
Processing chapter_00.md...
  ✓ Renumbered 12 sections
Processing chapter_01.md...
  ✓ Renumbered 28 sections
...
Total: 156 sections renumbered across 10 chapters
```

**Options**:
- `--chapter N`: Process only specific chapter (0-9)
- `--input-dir PATH`: Input directory (default: output/chapters/04_merged)
- `--output-dir PATH`: Output directory (default: output/chapters/05_repaired)
- `--dry-run`: Show what would be changed without modifying files
- `--format STYLE`: Numbering style ('decimal' [default], 'outline')

**Example (single chapter)**:
```bash
.venv/bin/python scripts/repair_section_numbering.py --chapter 5 --verbose
```

---

### 3. Repair Bullet Hierarchy

Fix bullet list indentation and markers:

```bash
.venv/bin/python scripts/repair_bullet_hierarchy.py
```

**Output**:
```
Processing chapter_00.md...
  ✓ Repaired 3 bullet lists (18 items fixed)
Processing chapter_01.md...
  ✓ Repaired 12 bullet lists (87 items fixed)
...
Total: 215 bullet lists repaired across 10 chapters
```

**Options**:
- `--chapter N`: Process only specific chapter (0-9)
- `--input-dir PATH`: Input directory (default: output/chapters/04_merged)
- `--output-dir PATH`: Output directory (default: output/chapters/05_repaired)
- `--base-indent N`: Base indentation unit in spaces (default: auto-detect)
- `--max-depth N`: Maximum nesting depth (default: 4 for PDF compatibility)
- `--dry-run`: Preview changes without modifying files

**Example (specific chapter with custom indent)**:
```bash
.venv/bin/python scripts/repair_bullet_hierarchy.py --chapter 1 --base-indent 2
```

---

### 4. Validate Structure

Verify document structure correctness after repairs:

```bash
.venv/bin/python scripts/validate_structure.py
```

**Output**:
```
Validating chapter_00.md...
  ✓ Section hierarchy: PASS
  ✓ Bullet formatting: PASS
  ✓ Content completeness: PASS
...
Overall: 10/10 chapters PASSED validation

Details: output/chapters/05_repaired/VALIDATION_REPORT.md
```

**Validation Checks**:
- Section numbering is sequential and hierarchical
- No gaps or duplicates in numbering
- Bullet indentation matches hierarchy
- Bullet markers are consistent
- No content loss from source
- Cross-references are intact
- Maximum nesting depths respected

**Options**:
- `--input-dir PATH`: Directory to validate (default: output/chapters/05_repaired)
- `--strict`: Fail on warnings, not just errors
- `--output PATH`: Validation report file path

---

## Common Workflows

### Workflow 1: Full Repair Pipeline

Complete repair of all chapters:

```bash
# Option A: Use the all-in-one script
.venv/bin/python scripts/repair_all.py

# Option B: Run steps manually
.venv/bin/python scripts/analyze_chapter5.py --restore
.venv/bin/python scripts/repair_section_numbering.py
.venv/bin/python scripts/repair_bullet_hierarchy.py
.venv/bin/python scripts/validate_structure.py
```

---

### Workflow 2: Test on Single Chapter

Test repairs on one chapter before processing all:

```bash
# Repair just chapter 5
.venv/bin/python scripts/repair_section_numbering.py --chapter 5
.venv/bin/python scripts/repair_bullet_hierarchy.py --chapter 5
.venv/bin/python scripts/validate_structure.py

# Review output
cat output/chapters/05_repaired/chapter_05.md | less
```

---

### Workflow 3: Dry Run (Preview Changes)

See what would be changed without modifying files:

```bash
# Preview numbering changes
.venv/bin/python scripts/repair_section_numbering.py --dry-run --verbose

# Preview bullet fixes
.venv/bin/python scripts/repair_bullet_hierarchy.py --dry-run --verbose
```

---

### Workflow 4: Investigate Chapter 5 Issues

Detailed analysis of Chapter 5 content:

```bash
# Generate detailed analysis
.venv/bin/python scripts/analyze_chapter5.py --verbose

# Review analysis report
cat output/chapters/05_repaired/CHAPTER_5_ANALYSIS.md

# Restore missing content if needed
.venv/bin/python scripts/analyze_chapter5.py --restore
```

---

## Output Structure

After running repairs, the output directory contains:

```
output/chapters/05_repaired/
├── chapter_00.md              # Repaired chapters
├── chapter_01.md
├── chapter_02.md
├── chapter_03.md
├── chapter_04.md
├── chapter_05.md              # Complete restored content
├── chapter_07.md
├── chapter_08.md
├── chapter_09.md
├── REPAIR_REPORT.md           # Summary of all repairs
├── VALIDATION_REPORT.md       # Validation results
└── CHAPTER_5_ANALYSIS.md      # Chapter 5 content analysis
```

---

## Verification Steps

After running repairs, verify the results:

### 1. Check Repair Report
```bash
cat output/chapters/05_repaired/REPAIR_REPORT.md
```

Look for:
- Number of sections renumbered
- Number of bullets fixed
- Content restoration status
- Any errors or warnings

### 2. Check Validation Report
```bash
cat output/chapters/05_repaired/VALIDATION_REPORT.md
```

Look for:
- All chapters show "PASS" status
- No ERROR-level issues
- Minimal or zero WARNING-level issues

### 3. Spot-Check Content
```bash
# Check chapter 5 completeness
wc -l output/chapters/04_merged/chapter_05.md output/chapters/05_repaired/chapter_05.md

# Should show similar or higher line count in repaired version
```

### 4. Visual Inspection
```bash
# Compare before/after for a chapter
diff output/chapters/04_merged/chapter_01.md output/chapters/05_repaired/chapter_01.md | less
```

---

## Troubleshooting

### Issue: "No such file or directory: output/chapters/04_merged"

**Solution**: Ensure previous processing stages are complete:
```bash
ls output/chapters/04_merged/
# Should show chapter_*.md files
```

If missing, run earlier processing stages first.

---

### Issue: "Chapter 5 analysis shows missing content"

**Solution**: This is expected! Use the restore flag:
```bash
.venv/bin/python scripts/analyze_chapter5.py --restore
```

---

### Issue: "Validation failed with errors"

**Solution**: Check validation report for specific issues:
```bash
cat output/chapters/05_repaired/VALIDATION_REPORT.md
# Look for ERROR entries and line numbers
```

Common causes:
- Malformed markdown in source files
- Inconsistent header levels (e.g., ## followed by ####)
- Lists with unusual indentation patterns

Fix source files if needed, or adjust repair script parameters.

---

### Issue: "Script hangs or runs very slowly"

**Solution**: Process chapters individually to isolate issue:
```bash
for i in {0..9}; do
    echo "Processing chapter $i..."
    .venv/bin/python scripts/repair_section_numbering.py --chapter $i
done
```

---

## Integration with PDF Generation

After structure repair, the repaired chapters can be used for PDF generation:

```bash
# Update PDF generator to use stage 05_repaired
.venv/bin/python scripts/pdf_generator.py --input-dir output/chapters/05_repaired

# Output: PDFs in output/pdfs/
```

The repaired structure ensures:
- Consistent section numbering in PDF bookmarks
- Proper bullet list rendering (max depth 4)
- Complete Chapter 5 content included

---

## Next Steps

After successful repair:

1. **Review Reports**: Check `REPAIR_REPORT.md` and `VALIDATION_REPORT.md`
2. **Spot-Check Content**: Visually inspect a few chapters for correctness
3. **Generate PDFs**: Use repaired chapters for PDF generation
4. **Commit Changes**: Commit repaired files to git (stage 05_repaired)
5. **Update Documentation**: Note any specific issues or patterns discovered

---

## Support

For issues or questions:
- Check validation report for specific error details
- Review individual script help: `script_name.py --help`
- Check specs: `specs/005-document-structure-repair/`
