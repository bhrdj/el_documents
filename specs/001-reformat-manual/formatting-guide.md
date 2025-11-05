# Formatting Guide: EL Caregiver Manual

**Based on**: Analysis of Chapter 0 (Front Matter) and Chapter 2 (Child Care)
**Generated**: 2025-11-05
**Source**: EL_CgManual_CURRENT_v016.pdf

## Overview

This document defines the formatting template for reformatting the EL Caregiver Manual into vanilla markdown. The template is based on comprehensive analysis of Chapter 0 and Chapter 2, which represent the target formatting standard.

---

## 1. Heading Structure

### 1.1 Primary Chapter Headings (H1)

**Pattern**: `# CHAPTER X: TITLE` or `# X. TITLE`

**Examples**:
- `# CHAPTER 0: FRONT MATTER`
- `# 2. CHILD CARE`

**Formatting Rules**:
- Use single `#` for H1 headings
- Chapter number followed by period or "CHAPTER" prefix
- Title in TITLE CASE or ALL CAPS (preserve source formatting)
- Single blank line before and after

### 1.2 Section Headings (H2)

**Pattern**: `## X.Y TITLE`

**Examples**:
- `## 0.1 INTRODUCTION`
- `## 2.1 DIAPER CHANGING`

**Formatting Rules**:
- Use `##` for H2 headings
- Numbered with chapter.section format
- Title typically in ALL CAPS
- Single blank line before and after

### 1.3 Subsection Headings (H3)

**Pattern**: `### X.Y.Z Title`

**Examples**:
- `### 2.1.1 Timing and Records`
- `### 2.4.2.3.1 Preventing food contamination`

**Formatting Rules**:
- Use `###` for H3 headings
- Numbered with full hierarchy (can extend to 4-5 levels)
- Title in Title Case or Sentence case
- Single blank line before and after

### 1.4 Bracketed Headings (Chapter 0 Style)

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

### 2.1 Bullet Lists

**Marker**: Use `●` (U+25CF BLACK CIRCLE) or `-` for bullets

**Examples**:
```markdown
● First item
● Second item
● Third item
```

Or:

```markdown
- First item
- Second item
- Third item
```

**Formatting Rules**:
- Use bullet character from source (typically `●` in this manual)
- Single space after marker
- Wrap long items naturally
- Single blank line before and after list block
- No blank lines between list items

### 2.2 Nested Bullets

**Pattern**: Indent with 2 spaces per level

**Example**:
```markdown
● Parent item
  ○ Nested item
  ○ Another nested item
● Another parent item
```

**Formatting Rules**:
- Use `○` (U+25CB WHITE CIRCLE) or indented `-` for nested bullets
- 2 spaces for each indentation level
- Consistent marker within same level

### 2.3 Numbered Lists

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

## 3. Unicode Bracket Preservation

### 3.1 Unicode Bracket Characters

**Characters Used**:
- `˹` (U+02F9) - LEFT TORTOISE SHELL BRACKET
- `˺` (U+02FA) - RIGHT TORTOISE SHELL BRACKET

**Usage Pattern**: These brackets surround emphasized or key terms throughout the manual, especially in Chapter 0.

**Examples**:
- `˹Guide˺ day-to-day daycare ˹operations˺`
- `˹Neither˺ the ˹provisions˺ of this document`
- `˹Excellence in childcare˺:`
- `˹NOT A CONTRACT˺`

### 3.2 Preservation Rules (CRITICAL)

1. **NEVER remove or modify unicode brackets**
2. **ALWAYS preserve exact placement around terms**
3. **Maintain UTF-8 encoding throughout processing**
4. **Do not replace with ASCII equivalents** (e.g., don't convert to `[` or `{`)
5. **Preserve spacing** - no space between bracket and enclosed text

### 3.3 Formatting Context

Unicode brackets appear in:
- Headings (especially Chapter 0)
- List items
- Inline text emphasizing key concepts
- Section titles

**Important**: These are not markdown formatting - they are content that must be preserved literally.

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
- Heavy use of unicode brackets
- Bracketed section headings
- Mix of formal and informal headings
- Mission/vision statement blocks
- Bullet lists with emphasized terms

**Special Handling**:
- Preserve ALL brackets meticulously
- Maintain bracketed heading format
- Keep vision/mission block structure

### 7.2 Chapter 2 (Child Care)

**Characteristics**:
- Deep heading hierarchy (up to 5 levels deep: 2.4.2.3.1)
- Extensive bullet lists
- Detailed procedural content
- NO unicode brackets (Chapter 2 doesn't use them)

**Special Handling**:
- Careful heading level mapping (may need up to H6 for 5-level nesting)
- Maintain list structure and indentation
- Preserve procedural step order

### 7.3 Expected Patterns in Other Chapters

Based on Chapter 2 pattern, most chapters likely:
- Use numbered section hierarchies
- Contain extensive bullet lists
- Have procedural/instructional content
- May or may not use unicode brackets

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

### 9.2 List Transformation

**Source (PDF text)**:
```
● Diapered children are checked at least hourly for the need of diaper change. Children under 12
months are checked more frequently.
● After every diaper change, a mark should be put on the Diaper data collection Sheet.
```

**Markdown Output**:
```markdown
● Diapered children are checked at least hourly for the need of diaper change. Children under 12 months are checked more frequently.
● After every diaper change, a mark should be put on the Diaper data collection Sheet.
```

**Changes**:
- Joined wrapped lines into single lines
- Maintained bullet marker
- Preserved exact text

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

● ˹Guide˺ day-to-day daycare ˹operations˺
● Ensure ˹EL standards˺ are ˹met˺ in every EL daycare]
```

**Changes**:
- Added blank line after intro sentence (before list)
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

## Revision History

- **v1.0** (2025-11-05): Initial template based on Chapter 0 and Chapter 2 analysis
