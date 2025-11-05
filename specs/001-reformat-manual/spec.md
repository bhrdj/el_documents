# Feature Specification: Reformat EL Caregiver Manual

**Feature**: `001-reformat-manual`
**Created**: 2025-11-05
**Status**: Draft
**Input**: Reformat EL Caregiver Manual chapters to match the formatting style established in Chapter 0 and Chapter 2, using vanilla markdown.

## User Scenarios & Testing

### User Story 1 - Establish Formatting Template (Priority: P1)

Analyze Chapter 0 and Chapter 2 of the EL Caregiver Manual to establish the target formatting style and create a formatting guide that can be applied to all other chapters.

**Why this priority**: Without a clear template, reformatting other chapters would be inconsistent. This establishes the baseline.

**Independent Test**: Can be fully tested by extracting and documenting the formatting patterns from Chapter 0 and Chapter 2, and validating that the documented patterns accurately represent the source chapters.

**Acceptance Scenarios**:

1. **Given** the PDF document EL_CgManual_CURRENT_v016.pdf, **When** Chapter 0 is analyzed, **Then** all formatting patterns (headings, lists, spacing, typography) are documented
2. **Given** the PDF document EL_CgManual_CURRENT_v016.pdf, **When** Chapter 2 is analyzed, **Then** formatting patterns are confirmed to match Chapter 0 or variations are documented
3. **Given** formatting patterns from both chapters, **When** a formatting guide is created, **Then** it provides clear rules for headings, lists, tables, spacing, and other markdown elements

---

### User Story 2 - Reformat Individual Chapters (Priority: P2)

Process each chapter (or section for larger chapters) systematically, applying the established formatting template to produce consistent vanilla markdown output.

**Why this priority**: This is the core reformatting work that depends on having the template established.

**Independent Test**: Can be tested by reformatting a single chapter and validating it against the formatting guide, checking content fidelity and format consistency.

**Acceptance Scenarios**:

1. **Given** a chapter from the manual and the formatting template, **When** the chapter is reformatted, **Then** output is valid vanilla markdown matching the template
2. **Given** original chapter content, **When** reformatted, **Then** all content is preserved with no additions, deletions, or modifications
3. **Given** a reformatted chapter, **When** checked against source, **Then** document structure (headings, lists, tables) is preserved accurately
4. **Given** unicode brackets around words in source, **When** reformatting, **Then** unicode brackets are preserved in output without modification

---

### User Story 3 - Validate Complete Manual (Priority: P3)

Verify that all reformatted chapters maintain consistent formatting and complete content fidelity across the entire manual.

**Why this priority**: Ensures quality and consistency across the full document after individual chapters are reformatted.

**Independent Test**: Can be tested by comparing all reformatted chapters against the formatting guide and source document for consistency and completeness.

**Acceptance Scenarios**:

1. **Given** all reformatted chapters, **When** formatting is checked, **Then** all chapters use consistent heading levels, list styles, and spacing
2. **Given** reformatted manual and source PDF, **When** content is compared, **Then** no content is missing, added, or altered
3. **Given** complete reformatted manual, **When** markdown is validated, **Then** all files are valid vanilla markdown with no extended features or HTML

---

### Edge Cases

- What happens when a chapter has complex tables that don't translate cleanly to markdown?
- How does the system handle special characters, mathematical notation, or unusual typography?
- What happens when heading levels in the source document are inconsistent?
- How are images, diagrams, or figures handled in the markdown output?
- What happens if unicode brackets appear in headings or special formatting contexts?
- **Unicode Bullets**: Raw extracted chapters contain three types of unicode bullets (`●` filled circle, `○` hollow circle, `■` filled square) that represent three levels of list hierarchy and must be converted to properly indented markdown bullets

## Requirements

### Functional Requirements

- **FR-001**: System MUST analyze Chapter 0 and Chapter 2 to extract formatting patterns (headings, lists, spacing, typography)
- **FR-002**: System MUST document the target formatting template based on Chapter 0 and Chapter 2 analysis
- **FR-003**: System MUST preserve all content from source chapters without additions, deletions, or modifications
- **FR-004**: System MUST preserve unicode brackets around words without modification or removal
- **FR-005**: System MUST output only vanilla markdown (no extended markdown, HTML, or special formatting)
- **FR-006**: System MUST preserve document structure including headings, lists, tables, and semantic elements
- **FR-007**: System MUST ensure consistent heading levels across all reformatted chapters
- **FR-008**: System MUST ensure consistent list formatting (bullet style, indentation) across all chapters
- **FR-011**: System MUST convert unicode bullet characters (`●` filled circle, `○` hollow circle, `■` filled square) to hierarchical markdown bullets with proper indentation (0, 2, and 4 spaces respectively)
- **FR-009**: System MUST process chapters systematically, either chapter-by-chapter or section-by-section for large chapters
- **FR-010**: System MUST maintain consistent spacing and typography throughout reformatted content

### Key Entities

- **Source Document**: EL_CgManual_CURRENT_v016.pdf - the input PDF containing all chapters
- **Chapter**: A section of the manual, either a numbered chapter or a major section
- **Formatting Template**: Documented formatting patterns extracted from Chapter 0 and Chapter 2
- **Reformatted Chapter**: Markdown output file for a single chapter following the template
- **Unicode Brackets**: Special bracket characters around certain words (especially in Chapter 0) that should be preserved

## Success Criteria

### Measurable Outcomes

- **SC-001**: Formatting template document completely captures all formatting patterns from Chapter 0 and Chapter 2
- **SC-002**: 100% of chapters are reformatted to valid vanilla markdown
- **SC-003**: 100% content fidelity - no content additions, deletions, or modifications in reformatted output
- **SC-004**: All reformatted chapters pass consistency validation against the formatting template
- **SC-005**: Unicode brackets are preserved in 100% of instances where they appear in source
- **SC-006**: All markdown files validate as vanilla markdown with no extended syntax or HTML

## Assumptions

- The source document (EL_CgManual_CURRENT_v016.pdf) is accessible in the repository
- Chapter 0 and Chapter 2 represent the desired formatting standard for the entire manual
- Unicode brackets will be addressed in a separate future effort, so preservation without modification is acceptable
- Vanilla markdown is sufficient to represent all content in the manual (tables, lists, headings, text)
- The reformatted output will be stored as separate .md files, one per chapter or major section

## Out of Scope

- Removing or modifying unicode brackets (deferred to future work)
- Content editing, rewriting, or improvement beyond formatting
- PDF generation from markdown output
- Automated validation of medical/educational content accuracy
- Translation or localization
- Addition of metadata, frontmatter, or navigation elements

## Dependencies

- Python environment (.venv) with PDF processing libraries
- Access to EL_CgManual_CURRENT_v016.pdf
- Markdown validation tools (optional for quality checking)

## Review & Acceptance Checklist

- [ ] All user stories are independently testable
- [ ] Functional requirements are complete and unambiguous
- [ ] Success criteria are measurable and technology-agnostic
- [ ] Edge cases are identified and documented
- [ ] Assumptions are clearly stated
- [ ] Out of scope items are defined
- [ ] No implementation details leak into specification
- [ ] Unicode bracket handling is clearly specified
