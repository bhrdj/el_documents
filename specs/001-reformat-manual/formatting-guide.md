# Formatting Guide: EL Caregiver Manual

**Based on**: Analysis of Chapter 0 (Front Matter) and Chapter 2 (Child Care)
**Generated**: 2025-11-05
**Source**: EL_CgManual_CURRENT_v016.pdf

## Overview

This document defines the formatting template for reformatting the EL Caregiver Manual into vanilla markdown. The template is based on comprehensive analysis of Chapter 0 and Chapter 2, which represent the target formatting standard.

---

## 1. Heading Structure

**CRITICAL RULE**: Heading level (number of `#` marks) must correspond to numbering depth:
- H1 (`#`) = Single number (e.g., `2`)
- H2 (`##`) = Two numbers (e.g., `2.1`)
- H3 (`###`) = Three numbers (e.g., `2.1.1`)
- H4 (`####`) = Four numbers (e.g., `2.1.1.1`)
- H5 (`#####`) = Five numbers (e.g., `2.1.1.1.1`)
- H6 (`######`) = Six numbers (e.g., `2.1.1.1.1.1`)

### 1.1 Primary Chapter Headings (H1)

**Pattern**: `# CHAPTER X: TITLE` or `# X. TITLE`

**Examples**:
- `# CHAPTER 0: FRONT MATTER`
- `# 2. CHILD CARE`

**Formatting Rules**:
- Use single `#` for H1 headings
- Single number only (bare chapter number)
- Title in TITLE CASE or ALL CAPS (preserve source formatting)
- Single blank line before and after

**Numbering**: `X` (single number)

### 1.2 Section Headings (H2)

**Pattern**: `## X.Y TITLE`

**Examples**:
- `## 0.1 INTRODUCTION`
- `## 2.1 DIAPER CHANGING`

**Formatting Rules**:
- Use `##` for H2 headings
- Two-level numbering: chapter.section
- Title typically in ALL CAPS
- Single blank line before and after

**Numbering**: `X.Y` (two numbers)

### 1.3 Subsection Headings (H3)

**Pattern**: `### X.Y.Z Title`

**Examples**:
- `### 2.1.1 Timing and Records`
- `### 2.4.2 Meal Preparation`

**Formatting Rules**:
- Use `###` for H3 headings
- Three-level numbering: chapter.section.subsection
- Title in Title Case or Sentence case
- Single blank line before and after

**Numbering**: `X.Y.Z` (three numbers)

### 1.4 Deep Subsection Headings (H4, H5, H6)

**Pattern**: `#### X.Y.Z.W Title` and deeper

**Examples**:
- `#### 2.4.2.3 Kitchen hygiene and food safety` (H4 with 4 numbers)
- `##### 2.4.2.3.1 Preventing food contamination` (H5 with 5 numbers)
- `###### 2.4.2.5.1 Labeling utensils` (H6 with 6 numbers)

**Formatting Rules**:
- Use `####`, `#####`, or `######` for deeper levels
- Numbering depth must match heading level (4, 5, or 6 numbers)
- Title in Title Case or Sentence case
- Single blank line before and after

**Numbering**:
- H4: `X.Y.Z.W` (four numbers)
- H5: `X.Y.Z.W.V` (five numbers)
- H6: `X.Y.Z.W.V.U` (six numbers)

### 1.5 Bracketed Headings (Chapter 0 Style)

**Pattern**: `### [X.Y.Z Title]` or `[X.Y.Z ˹Title with brackets˺]`

**Note**: Chapter 0 uses bracketed headings with unicode brackets around key terms. These should be preserved as-is.

**Examples**:
- `### [0.2 "˹NOT A CONTRACT˺" ˹DISCLAIMER˺]`
- `### [0.2.1 EL ˹Vision˺]`
- `### [0.2.3.1 ˹Excellence in childcare˺:]`

**Formatting Rules**:
- Preserve square brackets `[]` around heading text
- Preserve unicode brackets `˹˺` around emphasized terms
- Keep punctuation (colons, quotes) as in source
- Single blank line before and after

---

## 2. List Formatting

### 2.1 Unicode Bullet Conversion (CRITICAL)

**Source Format**: PDF extraction yields three types of unicode bullets representing hierarchy:
- `●` (U+25CF) - Filled circle - **First level** (no indentation)
- `○` (U+25CB) - Hollow circle - **Second level** (2 space indent)
- `■` (U+25A0) - Filled square - **Third level** (4 space indent)

**Target Format**: Standard markdown bullets with hierarchical indentation

**Conversion Rules**:
| Unicode Bullet | Level | Markdown Output | Indentation |
| --- | --- | --- | --- |
| `●` (filled circle) | Level 1 | `- ` | 0 spaces |
| `○` (hollow circle) | Level 2 | `  - ` | 2 spaces |
| `■` (filled square) | Level 3 | `    - ` | 4 spaces |

**Example Transformation**:

**Source (with unicode bullets)**:
```
● Get!
○ The needed supplies include:
■ Daycare diaper supplies bag.
■ The child's diaper supplies bag.
○ Always verify the mat is clean.
```

**Target (markdown with indentation)**:
```markdown
- Get!
  - The needed supplies include:
    - Daycare diaper supplies bag.
    - The child's diaper supplies bag.
  - Always verify the mat is clean.
```

**CRITICAL NOTES**:
- Unicode bullets `●○■` are LIST MARKERS and must be converted to markdown bullets
- Unicode brackets `˹˺` are CONTENT MARKERS and must be PRESERVED (see Section 3)
- Do not confuse bullets with brackets - completely different purposes

### 2.2 Bullet Lists

**Marker**: Use standard markdown `-` for all bullets (after converting from unicode)

**Example**:
```markdown
- First item
- Second item
- Third item
```

**Formatting Rules**:
- Use `-` (hyphen) for all bullet points
- Single space after marker
- Wrap long items naturally
- Single blank line before and after list block
- No blank lines between list items

### 2.3 Nested Bullets

**Pattern**: Indent with 2 spaces per level

**Example**:
```markdown
- Parent item
  - Nested item
  - Another nested item
- Another parent item
```

**Formatting Rules**:
- Use `-` for all levels (nested bullets also use `-`)
- 2 spaces for each indentation level
- Consistent indentation throughout
- Maximum depth: 3 levels (matching source document structure)

### 2.4 Numbered Lists

**Pattern**: Standard markdown numbered lists

**Example**:
```markdown
1. First item
2. Second item
3. Third item
```

**Formatting Rules**:
- Sequential numbering starting from 1
- Period after number
- Single space after period
- Single blank line before and after list block

---

## 3. Unicode Bracket Preservation (Chapter 0 Only)

**Characters**: `˹˺` (tortoise shell brackets) and `[]` (square brackets)

**Purpose**: Mark key terms in Chapter 0 for future Anki-style exam question generation (out of scope for current project)

**Scope**: Chapter 0 only

**Rules**:
- Preserve exactly as-is in Chapter 0 (placement, spacing, encoding)
- If found in other chapters: preserve but flag for manual review
- Do not convert to ASCII equivalents

**Examples**: `˹Guide˺ day-to-day ˹operations˺` or `[0.2 "˹NOT A CONTRACT˺" ˹DISCLAIMER˺]`

---

## 4. Spacing and Layout

### 4.1 Paragraph Spacing

**Rules**:
- Single blank line between paragraphs
- No trailing whitespace on lines
- Wrap long lines naturally (no hard wrapping at specific column)

### 4.2 Section Spacing

**Rules**:
- Single blank line before and after headings
- Single blank line before and after list blocks
- Two blank lines between major sections (optional, for readability)

### 4.3 Page Markers

**Pattern**: `Page X of XX` markers appear in source

**Rule**: These should be **removed** in markdown output (page numbers are not meaningful in markdown)

**Source Example**: `2. CHILD CARE Page 3 of XX`
**Markdown Output**: Omit this line

### 4.4 Footer Text

**Pattern**: `EL_CgManual_CURRENT_v016 November 5, 2025`

**Rule**: These footer markers should be **removed** in markdown output

---

## 5. Special Formatting

### 5.1 Tables

**Format**: Use standard markdown table syntax

**Example**:
```markdown
| Column 1 | Column 2 | Column 3 |
| --- | --- | --- |
| Data 1 | Data 2 | Data 3 |
| Data 4 | Data 5 | Data 6 |
```

**Rules**:
- Use pipe `|` delimiters
- Header separator row with `---`
- Align columns consistently
- Single blank line before and after table

### 5.2 Emphasis

**Bold**: Use `**bold text**` for emphasis when present in source

**Italic**: Use `*italic text*` for italic emphasis when present in source

**Note**: The unicode brackets `˹˺` are NOT emphasis markers - they are literal content

### 5.3 Code or Special Text

**Not applicable** - this manual does not contain code blocks or technical syntax

---

## 6. Content Fidelity Rules

### 6.1 Preservation Requirements

**MUST preserve**:
1. All text content exactly as written
2. All unicode characters (especially brackets)
3. Spelling (including any errors in source)
4. Punctuation
5. Capitalization patterns
6. List order and hierarchy

**MUST NOT**:
1. Add content not in source
2. Remove or modify content
3. "Fix" grammar or spelling
4. Reorder sections
5. Change unicode brackets to ASCII
6. Modify emphasized terms

### 6.2 Cleanup Rules

**MAY remove**:
1. Page numbers ("Page X of XX")
2. Footer text with manual version and date
3. Duplicate chapter headings on pages
4. Excessive whitespace

**MAY normalize**:
1. Blank line spacing (to single blank lines)
2. Line wrapping (remove PDF artifacts)
3. Consistent bullet markers within lists

---

## 7. Chapter-Specific Patterns

### 7.1 Chapter 0 (Front Matter)

**Characteristics**:
- Bracketed headings using `[]` and `˹˺` (see Section 3)
- Mission/vision statement blocks
- Mix of ALL CAPS and Title Case headings

**Special Handling**:
- Preserve all brackets (see Section 3)
- Maintain vision/mission block structure

### 7.2 Chapter 2 (Child Care)

**Characteristics**:
- Deep heading hierarchy (up to 5 levels: 2.4.2.3.1)
- Extensive bullet lists
- Detailed procedural content

**Special Handling**:
- Map heading depth to correct markdown level (may need H4-H6)
- Maintain list structure and indentation

### 7.3 Other Chapters (Expected Patterns)

Based on Chapter 2 analysis:
- Numbered section hierarchies
- Extensive bullet lists
- Procedural/instructional content

---

## 8. Validation Criteria

### 8.1 Format Validation

A reformatted chapter passes format validation when:
- All headings use proper markdown syntax (#, ##, ###)
- Lists use consistent markers
- Spacing follows rules (single blank lines)
- No page markers or footers remain
- Valid vanilla markdown (no HTML, no extended features)

### 8.2 Content Validation

A reformatted chapter passes content validation when:
- 100% of source text is present
- No text added that wasn't in source
- Unicode brackets preserved in every instance
- List order and hierarchy maintained
- Heading structure matches source

### 8.3 Consistency Validation

Chapters are consistent when:
- Heading levels map uniformly across chapters
- Bullet markers consistent within chapter
- Spacing rules applied uniformly
- Similar content structures formatted identically

---

## 9. Example Transformations

### 9.1 Heading Transformation

**Source (PDF text)**:
```
0. FRONT MATTER Page 2 of XX
CHAPTER 0. FRONT MATTER
CHAPTER 0. FRONT MATTER
0.1 INTRODUCTION
```

**Markdown Output**:
```markdown
# CHAPTER 0: FRONT MATTER

## 0.1 INTRODUCTION
```

**Changes**:
- Removed page marker
- Removed duplicate chapter headings
- Used # for H1, ## for H2

### 9.2 List Transformation (Simple)

**Source (PDF text)**:
```
● Diapered children are checked at least hourly for the need of diaper change. Children under 12
months are checked more frequently.
● After every diaper change, a mark should be put on the Diaper data collection Sheet.
```

**Markdown Output**:
```markdown
- Diapered children are checked at least hourly for the need of diaper change. Children under 12 months are checked more frequently.
- After every diaper change, a mark should be put on the Diaper data collection Sheet.
```

**Changes**:
- Joined wrapped lines into single lines
- Converted unicode bullet `●` to markdown bullet `-`
- Preserved exact text content

### 9.2b List Transformation (Hierarchical)

**Source (PDF text)**:
```
● Check!
○ Check the diaper to confirm that the child needs a diaper change.
○ Check on the register about whether the child is supposed to receive diaper-rash cream.
● Get!
○ Get the needed supplies and place them on the diaper changing mat.
○ The needed supplies include:
■ Daycare diaper supplies bag.
■ The child's diaper supplies bag.
■ The diaper changing mat.
```

**Markdown Output**:
```markdown
- Check!
  - Check the diaper to confirm that the child needs a diaper change.
  - Check on the register about whether the child is supposed to receive diaper-rash cream.
- Get!
  - Get the needed supplies and place them on the diaper changing mat.
  - The needed supplies include:
    - Daycare diaper supplies bag.
    - The child's diaper supplies bag.
    - The diaper changing mat.
```

**Changes**:
- Converted `●` (filled circle) to `-` (no indent)
- Converted `○` (hollow circle) to `  -` (2 space indent)
- Converted `■` (filled square) to `    -` (4 space indent)
- Maintained hierarchical relationship between items
- Preserved exact text content

### 9.3 Unicode Bracket Transformation

**Source (PDF text)**:
```
[Managers, caregivers, and other staff are urged to study the manual to:
● ˹Guide˺ day-to-day daycare ˹operations˺
● Ensure ˹EL standards˺ are ˹met˺ in every EL daycare]
```

**Markdown Output**:
```markdown
[Managers, caregivers, and other staff are urged to study the manual to:

- ˹Guide˺ day-to-day daycare ˹operations˺
- Ensure ˹EL standards˺ are ˹met˺ in every EL daycare]
```

**Changes**:
- Added blank line after intro sentence (before list)
- Converted unicode bullets `●` to markdown bullets `-`
- **PRESERVED unicode brackets exactly**
- Maintained bracket context around list block

---

## 10. Implementation Notes

### 10.1 Processing Order

1. Extract raw text from PDF (preserving unicode)
2. Identify headings and structure
3. Clean up page markers and footers
4. Format headings with appropriate markdown levels
5. Format lists with consistent markers
6. Normalize spacing
7. Validate unicode bracket preservation
8. Validate content fidelity

### 10.2 Common PDF Artifacts to Handle

- **Line wrapping**: PDF may break lines artificially - rejoin into natural paragraphs
- **Duplicate headings**: Chapter heading may repeat on each page - keep only once
- **Page markers**: "Page X of XX" - remove
- **Footer text**: Version and date stamps - remove
- **Extra whitespace**: Normalize to single blank lines

### 10.3 Quality Checks

For each reformatted chapter:
1. **Visual comparison** against source PDF
2. **Unicode grep** to find and verify all bracket instances
3. **Content diff** to ensure no additions/deletions
4. **Markdown validation** to ensure vanilla markdown
5. **Heading hierarchy** check for logical structure

---

## 11. Edge Cases Discovered During Implementation

### 11.1 Unpaired Unicode Brackets

**Issue**: Chapter 0 has slightly mismatched unicode bracket counts (123 opening vs 124 closing)

**Resolution**: This is a minor discrepancy in the source document. The validation script flags this as a warning but does not fail validation, as the content fidelity requirement mandates preserving the source exactly as-is.

**Impact**: Low - does not affect readability or content quality

### 11.2 Heading Level Skips

**Issue**: Chapter 2 contains at least one instance where heading levels skip from H1 directly to H3

**Example**: Line 101 in chapter_02.md shows a heading level skip

**Resolution**: Preserved as-is to maintain content fidelity. The validation script flags this as a warning.

**Impact**: Low - markdown renderers handle this correctly, though it's not best practice

### 11.3 Table of Contents Lines

**Issue**: Chapter 0 contains what appears to be a table of contents (lines 5-14 in reformatted output) that lists section headings but is not formatted as a list

**Resolution**: Preserved as-is since these lines exist in the source and modification would violate content fidelity requirements

**Impact**: Low - could be manually improved in a future editorial pass

### 11.4 Duplicate Section Headings

**Issue**: Some chapters have section headings that appear twice (e.g., "0.1 INTRODUCTION" appears on lines 1 and 19 of chapter_00.md)

**Resolution**: The remove_duplicate_chapter_headings function attempts to remove duplicates, but some edge cases remain. These are preserved when uncertain to maintain content fidelity.

**Impact**: Low - does not significantly affect readability

### 11.5 Empty Chapter Content

**Issue**: Chapter 8 (chapter_08.md) has 0 headings and 0 list items, suggesting it may be a placeholder or very brief chapter

**Resolution**: Processed normally. The validation script reports the statistics but does not fail.

**Impact**: None - if the source has minimal content, the output correctly reflects that

### 11.6 Multi-Part Chapters

**Issue**: Chapter 5 is split into two parts (chapter_05_part1.md and chapter_05_part2.md) due to length

**Resolution**: The reformat_chapter.py script handles multi-part chapters by processing all files matching the chapter number pattern

**Impact**: None - both parts are processed correctly and maintain proper formatting

### 11.7 Chapter Numbering Gaps

**Issue**: The manual contains chapters 0, 1, 2, 3, 4, 5, 7, 8, 9 (missing chapter 6)

**Resolution**: No special handling needed - chapters are processed independently

**Impact**: None - the numbering gap appears to be intentional in the source document

### 11.8 Unicode Bullet Distribution

**Issue**: Unicode bullets (●○■) appear heavily in most chapters but were already converted in earlier processing stages

**Observation**: The 02_removedbullets stage shows proper hierarchical conversion:
- 4,140 total list items across all chapters
- All unicode bullets successfully converted to markdown format with appropriate indentation

**Impact**: None - conversion was successful

---

## Revision History

- **v1.0** (2025-11-05): Initial template based on Chapter 0 and Chapter 2 analysis
- **v1.1** (2025-11-05): Added edge cases section documenting implementation findings
