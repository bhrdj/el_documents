---
description: "Task list for document structure repair feature implementation"
---

# Tasks: Document Structure Repair

**Input**: Design documents from `/specs/005-document-structure-repair/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Not explicitly requested in specification - tests are optional for this feature

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project structure**: `scripts/` for Python scripts, `output/markdown/05_repaired/` for output
- **Tests**: `tests/` at repository root
- Paths follow existing el_documents repository structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create project structure and prepare output directories

- [X] T001 Create output directory structure: `output/markdown/05_repaired/`
- [X] T002 [P] Create tests directory structure: `tests/` with subdirectories for unit and integration tests
- [X] T003 [P] Create feature README at `specs/005-document-structure-repair/README.md` documenting the feature

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core shared utilities and data structures that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create shared Document class in `scripts/lib/document.py` with properties: file_path, chapter_number, content, lines, sections, metadata
- [X] T005 [P] Create Section class in `scripts/lib/section.py` with properties: level, title, number, original_number, line_index, content_lines, parent, children
- [X] T006 [P] Create HierarchyLevel class in `scripts/lib/hierarchy.py` for numbering state management
- [X] T007 [P] Create BulletList and BulletItem classes in `scripts/lib/bullet.py` for list hierarchy
- [X] T008 Create markdown parsing utilities in `scripts/lib/parser.py` with functions: is_header(), get_header_level(), extract_section_number(), is_list_item()
- [X] T009 [P] Create validation utilities in `scripts/lib/validation.py` for structure validation checks
- [X] T010 [P] Create reporting utilities in `scripts/lib/reporting.py` for generating ProcessingReport and ValidationResult

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Restore Missing Chapter 5 Content (Priority: P1) 🎯 MVP

**Goal**: Analyze and restore all missing content from Chapter 5 to ensure document completeness

**Independent Test**: Compare output Chapter 5 against source PDF (chapter_5_part1.md + chapter_5_part2.md) to verify all content sections, paragraphs, and elements are present with no content loss

### Implementation for User Story 1

- [X] T011 [US1] Create content comparison module in `scripts/lib/content_comparison.py` with functions: parse_content_blocks(), create_content_fingerprint(), find_missing_content()
- [X] T012 [US1] Implement Chapter 5 analysis script in `scripts/analyze_chapter5.py` that loads part1, part2, and merged files
- [X] T013 [US1] Add section extraction logic to analyze_chapter5.py to identify all sections from source parts
- [X] T014 [US1] Add content fingerprinting logic to analyze_chapter5.py using first 50 chars or hash for comparison
- [X] T015 [US1] Add missing content detection logic to analyze_chapter5.py to identify which content blocks are missing from merged file
- [X] T016 [US1] Add content restoration logic to analyze_chapter5.py to insert missing content while preserving existing structure
- [X] T017 [US1] Add report generation to analyze_chapter5.py to create CHAPTER_5_ANALYSIS.md with findings
- [X] T018 [US1] Add CLI interface to analyze_chapter5.py with flags: --restore, --output-dir, --verbose
- [X] T019 [US1] Test analyze_chapter5.py script with dry-run to verify detection accuracy
- [X] T020 [US1] Run analyze_chapter5.py with --restore flag to restore missing Chapter 5 content to output/markdown/05_repaired/chapter_05.md

**Checkpoint**: At this point, Chapter 5 should be complete with all content restored and verified

---

## Phase 4: User Story 2 - Section Hierarchy Numbering Correction (Priority: P1)

**Goal**: Apply consistent, correct hierarchical section numbering across all documents

**Independent Test**: Examine any processed document and verify section numbers follow consistent hierarchical pattern (1.0, 1.1, 1.1.1, 1.2, 2.0) with no gaps, duplicates, or sequence breaks

### Implementation for User Story 2

- [X] T021 [US2] Create section numbering module in `scripts/lib/section_numbering.py` with stream-based numbering algorithm
- [X] T022 [US2] Implement counter stack management in section_numbering.py to track hierarchy levels (1-6)
- [X] T023 [US2] Add section number formatting logic in section_numbering.py to generate numbers like "1.2.3"
- [X] T024 [US2] Add header rewriting logic in section_numbering.py to update markdown headers with new numbers
- [X] T025 [US2] Create main repair script in `scripts/repair_section_numbering.py` with document processing loop
- [X] T026 [US2] Add document parsing to repair_section_numbering.py using shared Document and Section classes
- [X] T027 [US2] Add section detection to repair_section_numbering.py to identify all headers (# through ######)
- [X] T028 [US2] Add numbering application to repair_section_numbering.py by traversing document line-by-line
- [X] T029 [US2] Add cross-reference preservation logic to repair_section_numbering.py to maintain internal links
- [X] T030 [US2] Add CLI interface to repair_section_numbering.py with flags: --chapter, --input-dir, --output-dir, --dry-run, --format
- [X] T031 [US2] Test repair_section_numbering.py with --dry-run on chapter_01.md to verify numbering logic
- [X] T032 [US2] Run repair_section_numbering.py on all chapters to apply consistent numbering to output/markdown/05_repaired/

**Checkpoint**: At this point, all documents should have correct hierarchical section numbering

---

## Phase 5: User Story 3 - Bullet Hierarchy Repair (Priority: P2)

**Goal**: Fix bullet list indentation and markers to match semantic hierarchy

**Independent Test**: Examine bullet lists in processed documents and verify indentation levels match semantic hierarchy, markers are consistent at each level, and nested items appear correctly under parents

### Implementation for User Story 3

- [X] T033 [US3] Create bullet detection module in `scripts/lib/bullet_detection.py` with functions: detect_list_blocks(), count_leading_spaces(), detect_base_indent()
- [X] T034 [US3] Implement GCD-based indent detection in bullet_detection.py to find base indentation unit from mixed spacing
- [X] T035 [US3] Add hierarchy analysis in bullet_detection.py to determine nesting levels from indentation
- [X] T036 [US3] Create bullet repair module in `scripts/lib/bullet_repair.py` with repair logic
- [X] T037 [US3] Implement standardized marker assignment in bullet_repair.py using marker sequence ['-', '*', '+', '-', '*', '+']
- [X] T038 [US3] Add consistent indentation application in bullet_repair.py (2 spaces per level)
- [X] T039 [US3] Add max depth limiting in bullet_repair.py (default: 4 levels for PDF compatibility)
- [X] T040 [US3] Create main repair script in `scripts/repair_bullet_hierarchy.py` with document processing loop
- [X] T041 [US3] Add bullet list detection to repair_bullet_hierarchy.py to identify contiguous list blocks
- [X] T042 [US3] Add hierarchy repair application to repair_bullet_hierarchy.py for each list block
- [X] T043 [US3] Add CLI interface to repair_bullet_hierarchy.py with flags: --chapter, --input-dir, --output-dir, --base-indent, --max-depth, --dry-run
- [X] T044 [US3] Test repair_bullet_hierarchy.py with --dry-run on chapter_01.md to verify bullet formatting
- [X] T045 [US3] Run repair_bullet_hierarchy.py on all chapters to fix bullet hierarchy in output/markdown/05_repaired/

**Checkpoint**: At this point, all bullet lists should have correct indentation and markers

---

## Phase 6: Validation & Reporting

**Purpose**: Validate all repairs and generate comprehensive reports

- [ ] T046 Create validation script in `scripts/validate_structure.py` with all validation checks
- [ ] T047 Add section numbering validation to validate_structure.py: check sequential numbering, no gaps, no duplicates
- [ ] T048 Add bullet hierarchy validation to validate_structure.py: check consistent indentation, appropriate markers
- [ ] T049 Add content completeness validation to validate_structure.py: verify no content loss from source files
- [ ] T050 Add cross-reference validation to validate_structure.py: verify internal links still work
- [ ] T051 Add CLI interface to validate_structure.py with flags: --input-dir, --strict, --output
- [ ] T052 Run validate_structure.py on output/markdown/05_repaired/ to generate VALIDATION_REPORT.md
- [ ] T053 Create master repair script in `scripts/repair_all.py` that orchestrates all three repair operations
- [ ] T054 Add sequential processing to repair_all.py: analyze_chapter5 → repair_section_numbering → repair_bullet_hierarchy → validate_structure
- [ ] T055 Add comprehensive reporting to repair_all.py to generate REPAIR_REPORT.md with summary of all changes
- [ ] T056 Test repair_all.py on a single chapter to verify end-to-end pipeline
- [ ] T057 Run repair_all.py on all chapters to complete full repair pipeline

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation

- [X] T058 [P] Create feature README.md in specs/005-document-structure-repair/ documenting implementation decisions and usage
- [X] T059 [P] Update requirements.txt if any new dependencies were added (should be none per research.md)
- [X] T060 [P] Add .gitignore entries for output/markdown/05_repaired/ if needed
- [X] T061 [P] Create usage examples in quickstart.md showing common workflows
- [X] T062 Review all generated reports (CHAPTER_5_ANALYSIS.md, REPAIR_REPORT.md, VALIDATION_REPORT.md) for completeness
- [X] T063 Verify all repaired chapters in output/markdown/05_repaired/ are ready for PDF generation
- [X] T064 Run PDF generation test using repaired chapters to ensure compatibility
- [X] T065 Create implementation summary documenting: sections renumbered count, bullets fixed count, content restored status

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User Story 1 (Chapter 5 Restoration): Can start after Foundational - No dependencies on other stories
  - User Story 2 (Section Numbering): Can start after Foundational - No dependencies on other stories (but logically benefits from US1)
  - User Story 3 (Bullet Repair): Can start after Foundational - No dependencies on other stories (but logically benefits from US1 & US2)
- **Validation (Phase 6)**: Depends on desired user stories being complete
- **Polish (Phase 7)**: Depends on Validation completion

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - Fully independent
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Fully independent (recommended after US1 for completeness)
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Fully independent (recommended after US1 & US2 for best results)

**Note**: While user stories are technically independent, sequential execution (US1 → US2 → US3) is recommended to ensure Chapter 5 content is complete before applying formatting fixes.

### Within Each User Story

- User Story 1: Sequential tasks (analysis → restoration → verification)
- User Story 2: Sequential tasks (numbering logic → application → testing)
- User Story 3: Sequential tasks (detection → repair → application)

### Parallel Opportunities

- **Phase 1**: T002, T003 can run in parallel with T001
- **Phase 2**: T005, T006, T007, T009, T010 can all run in parallel after T004 completes
- **Phase 7**: T058, T059, T060, T061 can all run in parallel

**Limited parallelization within user stories**: Most tasks within each story are sequential due to logical dependencies (must detect before fixing, must fix before validating).

---

## Parallel Example: Foundational Phase

```bash
# After T004 completes, launch these in parallel:
Task: "Create Section class in scripts/lib/section.py"
Task: "Create HierarchyLevel class in scripts/lib/hierarchy.py"
Task: "Create BulletList and BulletItem classes in scripts/lib/bullet.py"
Task: "Create validation utilities in scripts/lib/validation.py"
Task: "Create reporting utilities in scripts/lib/reporting.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

Both User Stories 1 and 2 are P1 priority and form the core MVP:

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Chapter 5 Restoration)
4. **CHECKPOINT**: Verify Chapter 5 is complete
5. Complete Phase 4: User Story 2 (Section Numbering)
6. **CHECKPOINT**: Verify all documents have correct numbering
7. Complete Phase 6: Validation (basic validation)
8. **STOP and VALIDATE**: Test that Chapter 5 is complete and all documents have correct numbering

### Full Feature (All User Stories)

1. Complete Setup + Foundational → Foundation ready
2. Complete User Story 1 → Verify Chapter 5 complete → Checkpoint
3. Complete User Story 2 → Verify numbering correct → Checkpoint
4. Complete User Story 3 → Verify bullets formatted → Checkpoint
5. Complete Validation & Reporting → Full validation → Reports generated
6. Complete Polish → Documentation → Feature complete

### Sequential Execution (Recommended)

Given logical dependencies and single-developer context:

1. Complete phases 1-2 (Setup + Foundational)
2. Complete User Story 1 (ensures content complete)
3. Complete User Story 2 (numbering works on complete content)
4. Complete User Story 3 (bullet formatting works on correctly numbered content)
5. Complete Validation (verify everything)
6. Complete Polish (finalize)

### Validation Strategy

After each user story:
- Run the story's independent test
- Verify output matches acceptance scenarios
- Generate intermediate report
- Only proceed if validation passes

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently testable per specification
- No TDD approach specified - tests are optional
- Focus on correct implementation verified by validation scripts
- All scripts use `.venv/bin/python` per CLAUDE.md standards
- Commit after each logical group of tasks
- Stop at checkpoints to validate story independently
- Generate reports at each major phase for documentation
