# Data Model: Document Structure Repair

**Feature**: 005-document-structure-repair
**Created**: 2025-11-06
**Purpose**: Define entities, relationships, and data structures for document structure repair

## Overview

This document defines the core data entities and their relationships used in the document structure repair system. Since this is a document processing pipeline (not a database application), these entities represent in-memory data structures during processing.

---

## Core Entities

### 1. Document

**Purpose**: Represents a single markdown chapter file being processed

**Attributes**:
- `file_path` (Path): Absolute path to the markdown file
- `chapter_number` (int): Chapter number (0-9)
- `content` (str): Full markdown content as text
- `lines` (List[str]): Content split into lines for line-by-line processing
- `sections` (List[Section]): Hierarchical sections detected in document
- `metadata` (Dict[str, Any]): Document metadata (title, stage, etc.)

**Relationships**:
- Contains many `Section` entities
- Contains many `BulletList` entities
- Belongs to one `ProcessingStage`

**Validation Rules**:
- `file_path` must exist and be readable
- `content` must be valid UTF-8 text
- `chapter_number` must be 0-9
- `lines` count must match content line count

**State Transitions**:
```
Raw → Analyzed → Numbered → Repaired → Validated
```

---

### 2. Section

**Purpose**: Represents a hierarchical section within a document (identified by markdown headers)

**Attributes**:
- `level` (int): Header level (1-6, corresponding to #, ##, ###, etc.)
- `title` (str): Section title text (without header markers or numbering)
- `number` (str): Assigned section number (e.g., "1.2.3")
- `original_number` (str | None): Original section number from source (if present)
- `line_index` (int): Line number where section header appears
- `content_lines` (List[str]): Lines belonging to this section (until next header)
- `parent` (Section | None): Reference to parent section (one level up)
- `children` (List[Section]): Child sections (one level down)

**Relationships**:
- Belongs to one `Document`
- Has zero or one parent `Section`
- Has zero or more child `Section` entities
- Contains zero or more `BulletList` entities
- Contains zero or more `ContentElement` entities

**Validation Rules**:
- `level` must be 1-6
- `number` format must match pattern `\d+(\.\d+)*` (e.g., "1", "1.2", "1.2.3")
- `line_index` must be valid index within document
- Parent section (if exists) must have level = current level - 1
- Children sections must have level = current level + 1

**Invariants**:
- Sections form a proper tree hierarchy (no orphans, no cycles)
- Section numbers must be sequential within same parent
- Deeper sections cannot appear before their parents

---

### 3. HierarchyLevel

**Purpose**: Represents a level in the document hierarchy with numbering state

**Attributes**:
- `depth` (int): Nesting depth (1-6)
- `counter` (int): Current counter value at this level
- `number_format` (str): Format template (e.g., "arabic", "roman", "alpha")
- `separator` (str): Separator character (typically ".")

**Relationships**:
- Used by numbering algorithm to maintain state
- Associated with one or more `Section` entities at the same level

**Validation Rules**:
- `depth` must be 1-6
- `counter` must be >= 0
- `separator` typically one of: ".", "-", ""

**Usage Pattern**:
```python
levels = [HierarchyLevel(depth=i, counter=0) for i in range(1, 7)]

def process_section(section):
    level_idx = section.level - 1
    levels[level_idx].counter += 1
    # Reset deeper levels
    for i in range(level_idx + 1, 6):
        levels[i].counter = 0
    # Build number
    section.number = '.'.join(str(levels[i].counter) for i in range(0, level_idx + 1))
```

---

### 4. BulletList

**Purpose**: Represents a contiguous block of bullet list items with hierarchy

**Attributes**:
- `start_line` (int): Line index where list starts
- `end_line` (int): Line index where list ends
- `items` (List[BulletItem]): Individual list items
- `max_depth` (int): Maximum nesting depth in this list
- `base_indent` (int): Base indentation unit (detected or 2)
- `is_ordered` (bool): True if numbered list, False if bullet list

**Relationships**:
- Belongs to one `Section`
- Contains many `BulletItem` entities
- Part of one `Document`

**Validation Rules**:
- `start_line` < `end_line`
- `max_depth` <= 6 (pandoc limit for PDF generation)
- `base_indent` typically 2 or 4 spaces
- All items must have `line_index` between `start_line` and `end_line`

**State Transitions**:
```
Detected → Analyzed → Repaired → Validated
```

---

### 5. BulletItem

**Purpose**: Represents a single item in a bullet list

**Attributes**:
- `line_index` (int): Line number of this item
- `level` (int): Nesting level (0-based: 0 = top level)
- `indent` (int): Actual leading spaces
- `marker` (str): Bullet marker character ('-', '*', '+', or number)
- `content` (str): Item text (without marker and spaces)
- `parent` (BulletItem | None): Parent item (one level up)
- `children` (List[BulletItem]): Child items (one level down)

**Relationships**:
- Belongs to one `BulletList`
- Has zero or one parent `BulletItem`
- Has zero or more child `BulletItem` entities

**Validation Rules**:
- `level` must be >= 0 and <= 6
- `indent` should be consistent with level (indent = level * base_indent)
- `marker` must be valid ('-', '*', '+', or '\d+\.')
- Parent item (if exists) must have level = current level - 1

**Repair Logic**:
```python
def repair_bullet_item(item, base_indent=2):
    correct_indent = item.level * base_indent
    markers = ['-', '*', '+', '-', '*', '+']
    correct_marker = markers[item.level % len(markers)]
    return f"{' ' * correct_indent}{correct_marker} {item.content}"
```

---

### 6. ContentElement

**Purpose**: Represents other content types (paragraphs, tables, code blocks)

**Attributes**:
- `element_type` (str): Type of element ('paragraph', 'table', 'code', 'image', 'reference')
- `line_start` (int): Starting line index
- `line_end` (int): Ending line index
- `content` (str): Raw content text
- `metadata` (Dict[str, Any]): Element-specific metadata

**Relationships**:
- Belongs to one `Section`
- Part of one `Document`

**Validation Rules**:
- `element_type` must be one of: 'paragraph', 'table', 'code', 'image', 'reference', 'other'
- `line_start` <= `line_end`
- `content` must be non-empty for most types

**Usage**: Used primarily for validation and content preservation checks, not actively transformed.

---

## Derived Structures

### ProcessingReport

**Purpose**: Summary of all repairs performed on a document

**Attributes**:
- `document_path` (Path): Path to processed document
- `chapter_number` (int): Chapter number
- `repairs_applied` (List[str]): Descriptions of repairs
- `sections_renumbered` (int): Count of sections renumbered
- `bullets_repaired` (int): Count of bullet items fixed
- `content_restored` (bool): Whether missing content was restored
- `validation_passed` (bool): Whether post-repair validation passed
- `errors` (List[str]): Any errors encountered

**Output Format**: Markdown report file

---

### ValidationResult

**Purpose**: Results of structure validation checks

**Attributes**:
- `document_path` (Path): Path to validated document
- `checks_passed` (int): Number of validation checks passed
- `checks_failed` (int): Number of validation checks failed
- `issues` (List[ValidationIssue]): Specific issues found
- `overall_status` (str): 'PASS' or 'FAIL'

**ValidationIssue Structure**:
- `check_name` (str): Name of validation check
- `severity` (str): 'ERROR' or 'WARNING'
- `line_number` (int | None): Line where issue occurs
- `message` (str): Description of issue

**Output Format**: Markdown validation report

---

## Entity Relationships Diagram

```
Document (1) ──contains──> (*) Section
    │                          │
    │                          ├── (1) parent ──> (0..1) Section
    │                          └── (*) children ──> (*) Section
    │
    └──contains──> (*) BulletList
                       │
                       └──contains──> (*) BulletItem
                                          │
                                          ├── (1) parent ──> (0..1) BulletItem
                                          └── (*) children ──> (*) BulletItem

Section (1) ──contains──> (*) ContentElement
Section (1) ──contains──> (*) BulletList

Document ──generates──> (1) ProcessingReport
Document ──validates──> (1) ValidationResult
```

---

## Data Flow

### Input Processing Flow

```
1. Raw Markdown File (stage 04_merged)
   ↓
2. Document Entity (parse into memory)
   ↓
3. Section Entities (extract hierarchy)
   ↓
4. BulletList Entities (detect lists)
   ↓
5. HierarchyLevel State (numbering algorithm)
   ↓
6. Repaired Document (apply transformations)
   ↓
7. ValidationResult (verify correctness)
   ↓
8. Output Markdown File (stage 05_repaired)
   ↓
9. ProcessingReport (document changes)
```

### State Management

The processing pipeline maintains state in memory:

1. **Parse Phase**: File → Document → Sections + BulletLists
2. **Analysis Phase**: Detect hierarchy, numbering issues, bullet problems
3. **Repair Phase**: Apply numbering, fix bullets, restore content
4. **Validation Phase**: Verify repairs, check constraints
5. **Output Phase**: Write repaired document + reports

No persistent database - all state is transient during processing.

---

## Summary

The data model supports three main operations:

1. **Section Numbering**: `Document` → `Section` hierarchy → `HierarchyLevel` state → Numbered `Section`
2. **Bullet Repair**: `Document` → `BulletList` → `BulletItem` hierarchy → Repaired `BulletList`
3. **Content Restoration**: Source `Document` entities → Content comparison → Merged `Document`

All entities are in-memory Python objects with clear validation rules and state transitions.
