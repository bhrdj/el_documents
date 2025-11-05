# Unicode Bullet Conversion Implementation Plan

**Feature**: `001-reformat-manual` | **Date**: 2025-11-05
**Related Docs**: [spec.md](./spec.md), [plan.md](./plan.md), [formatting-guide.md](./formatting-guide.md)

## Problem Statement

The raw PDF extraction produces list items with three types of unicode bullet characters representing hierarchical levels:
- `●` (U+25CF) - Filled circle - Level 1
- `○` (U+25CB) - Hollow circle - Level 2
- `■` (U+25A0) - Filled square - Level 3

These must be converted to standard markdown bullets with proper indentation to create valid, hierarchical markdown lists.

## Critical Distinction

**Unicode Bullets** `●○■` → **CONVERT** to markdown bullets `-`
**Unicode Brackets** `˹˺` → **PRESERVE** as content markers

## Conversion Specification

### Mapping Table

| Input | Level | Output | Indentation | Notes |
|-------|-------|--------|-------------|-------|
| `●` | 1 | `- ` | 0 spaces | Top-level item |
| `○` | 2 | `  - ` | 2 spaces | Nested under level 1 |
| `■` | 3 | `    - ` | 4 spaces | Nested under level 2 |

### Pattern Recognition

**Input patterns**:
```
● First level item
○ Second level item
■ Third level item
```

**Output patterns**:
```markdown
- First level item
  - Second level item
    - Third level item
```

## Implementation Strategy

### Step 1: Detection Function

**Function**: `detect_unicode_bullets(text: str) -> bool`

**Purpose**: Identify if a line contains a unicode bullet marker

**Logic**:
```python
def detect_unicode_bullets(line: str) -> tuple[bool, str, int]:
    """
    Detect unicode bullet and return bullet info.

    Returns:
        (has_bullet, bullet_char, level)
        - has_bullet: True if line starts with unicode bullet
        - bullet_char: The unicode character found ('●', '○', '■')
        - level: Indentation level (1, 2, or 3)
    """
    stripped = line.lstrip()

    if stripped.startswith('●'):
        return (True, '●', 1)
    elif stripped.startswith('○'):
        return (True, '○', 2)
    elif stripped.startswith('■'):
        return (True, '■', 3)
    else:
        return (False, '', 0)
```

### Step 2: Conversion Function

**Function**: `convert_unicode_bullet_to_markdown(line: str) -> str`

**Purpose**: Convert a single line with unicode bullet to markdown bullet with proper indentation

**Logic**:
```python
def convert_unicode_bullet_to_markdown(line: str) -> str:
    """
    Convert unicode bullet line to markdown format.

    Examples:
        '● Item' -> '- Item'
        '○ Nested item' -> '  - Nested item'
        '■ Deep nested' -> '    - Deep nested'
    """
    has_bullet, bullet_char, level = detect_unicode_bullets(line)

    if not has_bullet:
        return line  # No bullet, return as-is

    # Remove the unicode bullet and any following space
    content = line.lstrip().lstrip('●○■').lstrip()

    # Build markdown bullet with appropriate indentation
    indent = '  ' * (level - 1)  # 0, 2, or 4 spaces
    return f"{indent}- {content}"
```

### Step 3: List Block Processing

**Function**: `process_list_block(lines: list[str]) -> list[str]`

**Purpose**: Process a contiguous block of list items, maintaining hierarchy

**Logic**:
```python
def process_list_block(lines: list[str]) -> list[str]:
    """
    Process a block of consecutive list items.

    Handles:
    - Converting all unicode bullets to markdown
    - Maintaining hierarchy
    - Preserving content including unicode brackets
    """
    result = []

    for line in lines:
        has_bullet, _, _ = detect_unicode_bullets(line)

        if has_bullet:
            converted = convert_unicode_bullet_to_markdown(line)
            result.append(converted)
        else:
            # Non-bullet line (continuation of previous item)
            result.append(line)

    return result
```

### Step 4: Full Document Processing

**Function**: `convert_document_bullets(content: str) -> str`

**Purpose**: Process entire document, converting all unicode bullets while preserving structure

**Logic**:
```python
def convert_document_bullets(content: str) -> str:
    """
    Convert all unicode bullets in document to markdown format.

    Preserves:
    - Unicode brackets ˹˺ (content markers)
    - Heading structure
    - Non-list content
    - Blank lines and spacing
    """
    lines = content.split('\n')
    result = []

    for line in lines:
        has_bullet, _, _ = detect_unicode_bullets(line)

        if has_bullet:
            converted = convert_unicode_bullet_to_markdown(line)
            result.append(converted)
        else:
            # Not a bullet line - preserve as-is
            result.append(line)

    return '\n'.join(result)
```

## Edge Cases and Handling

### 1. Multi-line List Items

**Input**:
```
● This is a long list item that wraps
to a second line
```

**Expected Output**:
```markdown
- This is a long list item that wraps
to a second line
```

**Handling**: The continuation line (without bullet) should remain at the same indentation level as the list item content.

### 2. Mixed Lists and Paragraphs

**Input**:
```
This is a paragraph.

● First bullet
○ Nested bullet

Another paragraph.
```

**Expected Output**:
```markdown
This is a paragraph.

- First bullet
  - Nested bullet

Another paragraph.
```

**Handling**: Preserve blank lines before and after list blocks.

### 3. Unicode Brackets in List Items

**Input**:
```
● ˹Guide˺ day-to-day daycare ˹operations˺
```

**Expected Output**:
```markdown
- ˹Guide˺ day-to-day daycare ˹operations˺
```

**Handling**: Unicode brackets `˹˺` must be preserved exactly. Only the bullet marker `●` is converted.

### 4. Level Transitions

**Input**:
```
● Level 1
○ Level 2
■ Level 3
○ Back to level 2
● Back to level 1
```

**Expected Output**:
```markdown
- Level 1
  - Level 2
    - Level 3
  - Back to level 2
- Back to level 1
```

**Handling**: Each bullet's indentation is determined solely by its bullet character, not by context.

### 5. Empty or Whitespace-Only Lines

**Input**:
```
● First item

○ Second item (with blank line before)
```

**Expected Output**:
```markdown
- First item

  - Second item (with blank line before)
```

**Handling**: Preserve blank lines within list blocks (though this may need cleanup based on markdown best practices).

## Validation Strategy

### Unit Tests

1. **Test single bullet conversion**:
   - Input: `"● Test item"`
   - Expected: `"- Test item"`

2. **Test each level**:
   - Level 1: `"● Item"` → `"- Item"`
   - Level 2: `"○ Item"` → `"  - Item"`
   - Level 3: `"■ Item"` → `"    - Item"`

3. **Test unicode bracket preservation**:
   - Input: `"● ˹Test˺ item"`
   - Expected: `"- ˹Test˺ item"`

4. **Test hierarchical list**:
   - Input: Multi-line with all three levels
   - Expected: Properly indented markdown

### Integration Tests

1. **Process Chapter 2 raw file**: Convert all bullets and verify output
2. **Compare line counts**: Input and output should have same number of list items
3. **Verify unicode brackets**: Count of `˹` and `˺` should be unchanged
4. **Validate markdown**: Output should pass markdown linter

## Implementation Sequence

### Phase 1: Core Functions (T018-T019)
1. Implement `detect_unicode_bullets()` in `markdown_utils.py`
2. Implement `convert_unicode_bullet_to_markdown()` in `markdown_utils.py`
3. Write unit tests for both functions

### Phase 2: Document Processing (T020-T021)
1. Implement `convert_document_bullets()` in `markdown_utils.py`
2. Add to `reformat_chapter.py` pipeline
3. Test on sample chapter

### Phase 3: Integration (T022-T024)
1. Integrate into full chapter reformatting workflow
2. Test on Chapter 2 (heavy bullet usage)
3. Test on Chapter 0 (ensure brackets preserved)

### Phase 4: Validation (T025-T028)
1. Add validation checks to `validate_output.py`
2. Verify no unicode bullets `●○■` remain in output
3. Verify unicode brackets `˹˺` are preserved
4. Process all chapters and validate

## Success Criteria

### Conversion Completeness
- **Zero** unicode bullet characters (`●○■`) in final markdown output
- All list items properly converted to markdown bullets (`-`)

### Content Preservation
- **100%** of unicode brackets (`˹˺`) preserved from input
- No text content lost or modified during conversion
- Line breaks and spacing preserved appropriately

### Markdown Validity
- All output is valid markdown
- List hierarchy properly represented with indentation
- Linters report no issues with list formatting

### Visual Consistency
- Rendered markdown shows proper nested list structure
- Indentation creates clear visual hierarchy
- Lists render correctly in markdown viewers

## Testing Checklist

- [ ] Unit test: Detect filled circle bullet `●`
- [ ] Unit test: Detect hollow circle bullet `○`
- [ ] Unit test: Detect filled square bullet `■`
- [ ] Unit test: Convert level 1 bullet (0 spaces)
- [ ] Unit test: Convert level 2 bullet (2 spaces)
- [ ] Unit test: Convert level 3 bullet (4 spaces)
- [ ] Unit test: Preserve unicode brackets in list items
- [ ] Integration test: Process Chapter 2 (many bullets)
- [ ] Integration test: Process Chapter 0 (brackets + bullets)
- [ ] Validation: No unicode bullets in output
- [ ] Validation: All unicode brackets preserved
- [ ] Validation: Markdown linter passes
- [ ] Manual review: Visual inspection of rendered markdown

## Notes

- Unicode bullets are **list structure markers** → convert
- Unicode brackets are **semantic content markers** → preserve
- Indentation must be exactly 2 spaces per level for standard markdown
- Consider adding a `--dry-run` mode to preview conversions
- Log all conversions for debugging and verification

## References

- [Formatting Guide](./formatting-guide.md) - Section 2.1 "Unicode Bullet Conversion"
- [Spec](./spec.md) - FR-011: Unicode bullet conversion requirement
- [Tasks](./tasks.md) - Tasks T018-T028 (User Story 2 and 3)
