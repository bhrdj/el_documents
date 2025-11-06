# Research: Document Structure Repair

**Feature**: 005-document-structure-repair
**Created**: 2025-11-06
**Purpose**: Technical research and decisions for document structure repair implementation

## Research Areas

### 1. Markdown Structure Analysis

**Question**: What's the best approach for analyzing markdown document structure and detecting hierarchy?

**Research Findings**:

**Approach A: Regex-based Header Parsing**
- Use regex patterns to identify markdown headers (`#`, `##`, `###`, etc.)
- Extract section numbering from header text
- Build hierarchy tree from nesting levels
- **Pros**: Simple, no external dependencies, direct control
- **Cons**: May miss malformed headers, requires careful regex crafting

**Approach B: Markdown AST Parsing**
- Use `markdown` or `mistletoe` library to parse into Abstract Syntax Tree
- Traverse AST to identify headers, lists, and structure
- **Pros**: More robust, handles edge cases, standard approach
- **Cons**: Additional dependency, may be overkill for simple structure

**Approach C: Hybrid Approach**
- Use regex for quick header identification
- Use string analysis for content context
- Build custom hierarchy representation
- **Pros**: Balanced complexity, tailored to our needs
- **Cons**: More custom code to maintain

**Decision**: **Approach C - Hybrid Approach**

**Rationale**:
- Our documents have known structure patterns from the PDF extraction pipeline
- Regex provides sufficient accuracy for header detection in our controlled format
- Custom hierarchy building gives us precise control over numbering logic
- No need for heavy AST parsing when simple pattern matching works
- Keeps dependencies minimal (already have `re` module)

**Alternatives Considered**: AST parsing was considered but rejected due to added complexity without clear benefit for our specific use case.

---

### 2. Hierarchical Section Numbering Algorithm

**Question**: How should we implement context-aware section numbering that maintains hierarchy?

**Research Findings**:

**Approach A: Tree-Based Numbering**
- Build complete section tree first
- Traverse tree depth-first to assign numbers
- Maintain stack of current position at each level
- **Pros**: Mathematically sound, handles complex hierarchies
- **Cons**: Two-pass algorithm (build + number)

**Approach B: Stream-Based Numbering**
- Process document line-by-line
- Maintain counter stack for each hierarchy level
- Update counters as headers are encountered
- **Pros**: Single-pass, memory efficient, simple state
- **Cons**: Requires careful state management

**Approach C: Template-Based Numbering**
- Use predefined numbering templates (1.0, 1.1, 1.1.1)
- Match existing patterns and extend
- **Pros**: Respects existing conventions
- **Cons**: Less flexible, may not handle all cases

**Decision**: **Approach B - Stream-Based Numbering**

**Rationale**:
- Single-pass efficiency important for processing multiple large documents
- State management is straightforward with simple counter stack
- Easy to test incrementally line-by-line
- Handles dynamic hierarchy changes gracefully
- Memory efficient for large documents

**Implementation Pattern**:
```python
counters = [0] * 7  # Support up to 6 levels (0 is unused)
current_level = 0

for line in document:
    if is_header(line):
        level = get_header_level(line)  # 1-6
        counters[level] += 1
        # Reset deeper levels
        for i in range(level + 1, 7):
            counters[i] = 0
        # Build number: "1.2.3"
        number = '.'.join(str(counters[i]) for i in range(1, level + 1))
```

**Alternatives Considered**: Tree-based was considered but rejected for being unnecessarily complex for linear document processing.

---

### 3. Bullet List Hierarchy Detection

**Question**: How do we detect and repair incorrect bullet list hierarchy?

**Research Findings**:

**Pattern Analysis from Existing Documents**:
- Indentation typically 2-4 spaces per level
- Inconsistent bullet markers: `-`, `*`, `+`
- Some lists have broken indentation (0, 4, 4, 4 instead of 0, 2, 4, 6)
- Maximum observed depth: 6 levels (from fix_pdf_issues.py limiting to 4)

**Approach A: Indentation-Only Detection**
- Count leading spaces
- Assume fixed spacing (e.g., 2 spaces = 1 level)
- **Pros**: Simple, works for consistent docs
- **Cons**: Fails with mixed spacing

**Approach B: Context-Aware Detection**
- Analyze surrounding list items
- Detect indentation patterns dynamically
- Use most common spacing as base unit
- **Pros**: Handles inconsistent documents
- **Cons**: More complex logic

**Approach C: Semantic Content Analysis**
- Analyze list item content for parent-child relationships
- Use sentence structure and keywords
- **Pros**: Most accurate for meaning
- **Cons**: Requires NLP, over-engineered

**Decision**: **Approach B - Context-Aware Detection**

**Rationale**:
- Our documents have inconsistent indentation from PDF extraction
- Need to handle mixed spacing patterns
- Can detect most common pattern in a list block
- No NLP overhead while still handling real-world messiness
- Balances accuracy and complexity

**Implementation Pattern**:
```python
def detect_list_spacing(list_block):
    """Detect the base indentation unit for a list block."""
    indents = [count_leading_spaces(line) for line in list_block if is_list_item(line)]
    # Find GCD of all non-zero indents
    from math import gcd
    base_unit = reduce(gcd, [i for i in indents if i > 0])
    return base_unit or 2  # Default to 2 if can't detect

def repair_bullet_hierarchy(list_block):
    base_unit = detect_list_spacing(list_block)
    for line in list_block:
        if is_list_item(line):
            current_indent = count_leading_spaces(line)
            level = current_indent // base_unit
            # Apply consistent markers by level
            markers = ['-', '*', '+', '-', '*', '+']
            new_indent = ' ' * (level * 2)  # Standardize to 2 spaces
            new_marker = markers[min(level, len(markers) - 1)]
            # Reconstruct line
```

**Alternatives Considered**: Simple indentation-only would fail on our real documents; semantic analysis is overkill.

---

### 4. Chapter 5 Content Restoration Strategy

**Question**: What's the best way to ensure complete Chapter 5 content restoration?

**Research Findings**:

**Current State Analysis**:
- Raw extraction: `chapter_5_part1.md` + `chapter_5_part2.md` (stage 00_raw)
- Merged file exists: `chapter_05.md` (stage 04_merged)
- Need to verify: Is merged file complete or missing content?

**Approach A: Content Comparison**
- Compare merged file against both source parts
- Identify missing paragraphs, sections, or elements
- **Pros**: Precise identification of gaps
- **Cons**: Requires content diffing logic

**Approach B: Re-merge from Source**
- Discard current merge, rebuild from part1 + part2
- Apply deduplication logic during merge
- **Pros**: Clean rebuild, ensures completeness
- **Cons**: May lose any manual edits in current merge

**Approach C: Hybrid Validation + Selective Restoration**
- Validate current merge completeness
- Only restore missing sections
- Preserve existing quality improvements
- **Pros**: Best of both worlds
- **Cons**: Most complex logic

**Decision**: **Approach A - Content Comparison**

**Rationale**:
- Need to understand exactly what's missing before fixing
- Content comparison reveals specific gaps
- Can then make informed decision about restore vs. re-merge
- Provides diagnostic information for validation report
- Lower risk than discarding current work

**Implementation Strategy**:
1. Parse all three files (part1, part2, merged)
2. Extract section headers and content blocks
3. Create content fingerprints (hash or first 50 chars)
4. Identify which content from parts is missing in merged
5. Report findings for manual review or auto-restore
6. Apply restoration preserving existing structure

**Alternatives Considered**: Re-merge would be simpler but risks losing quality improvements from stage 04.

---

## Technology Decisions

### Dependencies

**No New Dependencies Required**
- All required functionality available in existing stack:
  - `re`: Regex for pattern matching
  - `pathlib`: File operations
  - Standard library only for core logic

**Existing Dependencies to Use**:
- `markdown`: If AST parsing needed (currently not required)
- `pytest`: For testing framework

**Decision**: Keep dependencies minimal, use standard library.

---

### Testing Strategy

**Test-Driven Development Approach**:
1. **Unit Tests**: Test individual functions (numbering logic, indent detection, content comparison)
2. **Integration Tests**: Test full document processing pipeline
3. **Validation Tests**: Verify output meets success criteria
4. **Regression Tests**: Ensure existing chapters not broken by repairs

**Test Data**:
- Use actual chapter excerpts as test fixtures
- Create minimal examples for edge cases
- Include malformed examples from real extraction issues

**Coverage Goals**:
- 80% code coverage minimum
- 100% coverage for critical numbering and restoration logic

---

## Summary

| Decision Area | Chosen Approach | Key Rationale |
|--------------|-----------------|---------------|
| Structure Analysis | Hybrid Regex + Custom | Simple, sufficient, minimal dependencies |
| Section Numbering | Stream-Based | Single-pass, efficient, easy state management |
| Bullet Hierarchy | Context-Aware Detection | Handles real-world inconsistencies |
| Chapter 5 Restoration | Content Comparison | Precise gap identification, preserves existing work |
| Dependencies | Standard Library | Minimize complexity, use what's available |
| Testing | TDD with Pytest | Ensure correctness, prevent regressions |

All NEEDS CLARIFICATION items from Technical Context have been resolved.
