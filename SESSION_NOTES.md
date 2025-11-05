# Session Notes - Chapter Reorganization

**Date**: 2025-11-05
**Status**: In progress - context limit approaching, need to reset

## Completed Work

### ✅ Chapter 5 Reorganization (COMPLETE & COMMITTED)
- **Commit**: `19b7be8` - "reorganize chapter 5: merge parts, deduplicate, add TOC"
- Merged chapter_05_part1.md + part2.md
- Removed 394 duplicate sections
- Final: 2,727 lines with 172 unique sections (62% reduction)
- Added professional TOC with 172 entries
- **Location**: `output/chapters/03_merged/chapter_05.md`

### ✅ Chapter Analysis (COMPLETE)
- Analyzed all 8 remaining chapters
- Created: `specs/001-reformat-manual/chapter-restructuring-plan.md`
- Found 15 total issues across chapters

### ✅ H1 Chapter Titles Added (COMPLETE)
- Chapter 0: CHAPTER 0: FRONT MATTER
- Chapter 1: CHAPTER 1: CHILD ADMISSION
- Chapter 4: CHAPTER 4: CHILD INTERACTION STRATEGIES
- Chapter 7: CHAPTER 7: STAFF STAYING IN DAYCARE

### ✅ TOCs Added to Long Chapters (COMPLETE)
- Chapter 2: 111 entries ✓
- Chapter 3: 82 entries ✓
- Chapter 9: 47 entries ✓

## Current Issue - TOC Placement

**Problem**: TOC was added at line ~101 in Chapter 2 instead of after H1 title.

**Cause**: Chapter 2 had duplicate plain text titles that confused the script.

**Status**:
- Chapter 2 title fixed to proper H1 markdown
- TOCs exist but may not be in ideal position (after content started instead of after H1)
- Chapters 3 and 9 may have same issue

**Solution needed**:
Move TOCs to appear right after H1 title + blank line for all three chapters (2, 3, 9).

## Files Modified (Not Yet Committed)

```
output/chapters/02_removedbullets/chapter_00.md  # Added H1 title
output/chapters/02_removedbullets/chapter_01.md  # Added H1 title
output/chapters/02_removedbullets/chapter_02.md  # Added H1 title + TOC
output/chapters/02_removedbullets/chapter_03.md  # Added TOC
output/chapters/02_removedbullets/chapter_04.md  # Added H1 title
output/chapters/02_removedbullets/chapter_07.md  # Added H1 title
output/chapters/02_removedbullets/chapter_09.md  # Added TOC
```

New scripts created:
```
scripts/reformat_manual/add_chapter_titles.py
scripts/reformat_manual/add_toc_to_chapter.py
```

## Next Steps (In Order)

1. **Fix TOC placement** in Chapters 2, 3, 9:
   - Move TOC to appear right after H1 title
   - Format: `# TITLE\n\n## Table of Contents\n...`

2. **Verify all changes**:
   ```bash
   # Check H1 titles present
   grep -n "^# CHAPTER" output/chapters/02_removedbullets/chapter_{00,01,04,07}.md

   # Check TOC placement
   head -30 output/chapters/02_removedbullets/chapter_{02,03,09}.md
   ```

3. **Commit changes**:
   ```bash
   git add output/chapters/02_removedbullets/chapter_{00,01,02,03,04,07,09}.md
   git add scripts/reformat_manual/add_chapter_titles.py
   git add scripts/reformat_manual/add_toc_to_chapter.py
   git commit -m "add H1 titles and TOCs to chapters 0,1,2,3,4,7,9"
   ```

4. **Optional future work**:
   - Chapter 8 left as-is per user request (very short, no changes needed)
   - No heading hierarchy simplification (kept as-is per user request)

## Scripts Available

### Chapter Processing
- `merge_chapter5.py` - Intelligent merge with precedence
- `deduplicate_chapter5.py` - Remove duplicate sections
- `add_toc_chapter5.py` - Generate TOC (Chapter 5 specific)
- `add_toc_to_chapter.py` - Generate TOC (any chapter) ⭐ USE THIS
- `add_chapter_titles.py` - Add H1 titles
- `analyze_all_chapters.py` - Cross-chapter analysis
- `validate_output.py` - Chapter validation

### How to Use
```bash
# Add TOC to any chapter
.venv/bin/python scripts/reformat_manual/add_toc_to_chapter.py <chapter_num>

# Add H1 titles (specific chapters hardcoded)
.venv/bin/python scripts/reformat_manual/add_chapter_titles.py

# Validate chapters
.venv/bin/python scripts/reformat_manual/validate_output.py
```

## User Decisions Made

1. **Chapter 8**: Leave as-is (don't expand or merge)
2. **Heading hierarchy**: Don't simplify for uniformity - keep deep nesting if it adds clarity
3. **H1 titles**: Add to all chapters missing them ✓
4. **TOCs**: Add to long chapters (2, 3, 9) ✓

## Project Structure

```
output/chapters/
├── 00_raw/                    # Raw PDF extraction
├── 02_removedbullets/         # Reformatted with markdown bullets
│   ├── chapter_00.md          # Modified: +H1 title
│   ├── chapter_01.md          # Modified: +H1 title
│   ├── chapter_02.md          # Modified: +H1 title, +TOC
│   ├── chapter_03.md          # Modified: +TOC
│   ├── chapter_04.md          # Modified: +H1 title
│   ├── chapter_05_part1.md    # Original Part 1 (for reference)
│   ├── chapter_05_part2.md    # Original Part 2 (for reference)
│   ├── chapter_07.md          # Modified: +H1 title
│   ├── chapter_08.md          # Unchanged (per user request)
│   ├── chapter_09.md          # Modified: +TOC
│   └── VALIDATION_REPORT.md
└── 03_merged/
    ├── chapter_05.md          # ⭐ OFFICIAL merged Chapter 5 with TOC
    ├── chapter_05_deduplicated.md  # Backup before TOC added
    ├── CHAPTER_5_MERGE_REPORT.md
    └── README.md
```

## Git Status

**Last commit**: `19b7be8` - Chapter 5 reorganization
**Uncommitted changes**: H1 titles + TOCs for chapters 0,1,2,3,4,7,9

## Quick Recovery Commands

```bash
# If TOC placement is wrong, fix it manually:
# 1. Find the TOC section (starts with "## Table of Contents")
# 2. Cut it (delete those lines)
# 3. Paste it right after the H1 title + blank line

# Or use sed to move TOC to after H1:
# (This is complex, better to do manually or write a proper script)

# Check if changes look good:
git diff output/chapters/02_removedbullets/chapter_02.md | head -100

# If all good, commit:
git add output/chapters/02_removedbullets/ scripts/reformat_manual/
git commit -m "add H1 titles and TOCs to remaining chapters"
```

## Key Files to Review After Reset

1. This file: `SESSION_NOTES.md`
2. Restructuring plan: `specs/001-reformat-manual/chapter-restructuring-plan.md`
3. Chapter 5 output: `output/chapters/03_merged/chapter_05.md`
4. Modified chapters: `output/chapters/02_removedbullets/chapter_{00,01,02,03,04,07,09}.md`

## Context Recovery

To pick up where we left off:
1. Read this file (SESSION_NOTES.md)
2. Check git status to see uncommitted changes
3. Verify TOC placement in chapters 2, 3, 9 (should be right after H1)
4. If TOC placement wrong, manually move or write script to fix
5. Commit all changes once verified
6. Continue with any additional chapter improvements if needed
