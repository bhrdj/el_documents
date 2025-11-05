# Tasks: Reformat EL Caregiver Manual

**Input**: Design documents from `/specs/001-reformat-manual/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Not explicitly requested in specification - focusing on validation tasks instead

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Repository root structure with `scripts/`, `output/`, `specs/`
- Python execution via `.venv/bin/python`
- All scripts in `scripts/reformat_manual/` directory

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure: scripts/reformat_manual/, scripts/reformat_manual/utils/, output/reformatted_manual/
- [X] T002 Install PDF processing dependencies: pdfplumber>=0.10.0, PyPDF2>=3.0.0, markdown>=3.5
- [X] T003 Update requirements.txt with installed dependencies using pip freeze

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core PDF extraction utilities that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Create PDF utilities module in scripts/reformat_manual/utils/pdf_utils.py with extract_text_by_page function
- [X] T005 [P] Add detect_headings function to scripts/reformat_manual/utils/pdf_utils.py for structure detection
- [X] T006 [P] Add preserve_unicode function to scripts/reformat_manual/utils/pdf_utils.py for unicode bracket preservation
- [X] T007 [P] Create markdown utilities module in scripts/reformat_manual/utils/markdown_utils.py with basic formatting functions
- [X] T008 Create main PDF extraction script in scripts/reformat_manual/extract_pdf.py for chapter-by-chapter extraction
- [X] T009 Test PDF extraction on sample page to verify unicode bracket preservation and content fidelity

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Establish Formatting Template (Priority: P1) 🎯 MVP

**Goal**: Analyze Chapter 0 and Chapter 2 to establish target formatting style and create a formatting guide

**Independent Test**: Extract and validate Chapter 0 and Chapter 2, document formatting patterns, verify documented patterns match source chapters

### Implementation for User Story 1

- [X] T010 [US1] Create template analysis script in scripts/reformat_manual/analyze_template.py
- [X] T011 [US1] Extract Chapter 0 from EL_CgManual_CURRENT_v016.pdf using extract_pdf.py
- [X] T012 [US1] Extract Chapter 2 from EL_CgManual_CURRENT_v016.pdf using extract_pdf.py
- [X] T013 [US1] Analyze Chapter 0 formatting patterns: headings, lists, spacing, typography, unicode brackets
- [X] T014 [US1] Analyze Chapter 2 formatting patterns and compare with Chapter 0 for consistency
- [X] T015 [US1] Document formatting template in specs/001-reformat-manual/formatting-guide.md
- [X] T016 [US1] Add unicode bracket preservation rules to formatting-guide.md
- [X] T017 [US1] Validate formatting guide completeness against both source chapters

**Checkpoint**: At this point, User Story 1 should be complete with a comprehensive formatting template documented

---

## Phase 4: User Story 2 - Reformat Individual Chapters (Priority: P2)

**Goal**: Process each chapter systematically, applying the established formatting template to produce consistent vanilla markdown output

**Independent Test**: Reformat a single chapter and validate against formatting guide, checking content fidelity and format consistency

### Implementation for User Story 2

- [ ] T018 [US2] Implement apply_heading_format function in scripts/reformat_manual/utils/markdown_utils.py
- [ ] T019 [P] [US2] Implement format_lists function in scripts/reformat_manual/utils/markdown_utils.py
- [ ] T020 [P] [US2] Implement format_tables function in scripts/reformat_manual/utils/markdown_utils.py
- [ ] T021 [P] [US2] Implement apply_spacing_rules function in scripts/reformat_manual/utils/markdown_utils.py
- [ ] T022 [US2] Create chapter reformatting script in scripts/reformat_manual/reformat_chapter.py
- [ ] T023 [US2] Add command-line interface to reformat_chapter.py for specifying chapter number
- [ ] T024 [US2] Test reformat_chapter.py on Chapter 0, output to output/reformatted_manual/chapter_00.md
- [ ] T025 [US2] Validate Chapter 0 output matches source formatting and preserves all content
- [ ] T026 [US2] Test reformat_chapter.py on Chapter 2, output to output/reformatted_manual/chapter_02.md
- [ ] T027 [US2] Process remaining chapters systematically using reformat_chapter.py
- [ ] T028 [US2] Verify unicode brackets preserved in all reformatted chapter outputs

**Checkpoint**: At this point, all chapters should be reformatted to vanilla markdown with consistent formatting

---

## Phase 5: User Story 3 - Validate Complete Manual (Priority: P3)

**Goal**: Verify that all reformatted chapters maintain consistent formatting and complete content fidelity across the entire manual

**Independent Test**: Compare all reformatted chapters against formatting guide and source document for consistency and completeness

### Implementation for User Story 3

- [ ] T029 [P] [US3] Create validation script in scripts/reformat_manual/validate_output.py
- [ ] T030 [P] [US3] Implement check_markdown_validity function in validate_output.py to ensure vanilla markdown
- [ ] T031 [P] [US3] Implement check_heading_consistency function in validate_output.py
- [ ] T032 [P] [US3] Implement check_list_formatting function in validate_output.py
- [ ] T033 [P] [US3] Implement validate_unicode_brackets function in validate_output.py
- [ ] T034 [US3] Run validate_output.py on all chapters in output/reformatted_manual/
- [ ] T035 [US3] Generate validation report documenting any issues found
- [ ] T036 [US3] Manually review each chapter against source PDF for content fidelity
- [ ] T037 [US3] Fix any validation failures identified in validation report
- [ ] T038 [US3] Document edge cases encountered in specs/001-reformat-manual/formatting-guide.md
- [ ] T039 [US3] Final validation pass on complete reformatted manual

**Checkpoint**: All user stories complete - manual fully reformatted with validated consistency and fidelity

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation

- [ ] T040 [P] Update specs/001-reformat-manual/formatting-guide.md with lessons learned
- [ ] T041 [P] Add usage documentation to scripts/reformat_manual/README.md
- [ ] T042 Code cleanup and refactoring of utility functions
- [ ] T043 Add inline documentation to all Python scripts

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P2): Depends on User Story 1 (needs formatting template)
  - User Story 3 (P3): Depends on User Story 2 (needs reformatted chapters to validate)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on User Story 1 (requires formatting-guide.md)
- **User Story 3 (P3)**: Depends on User Story 2 (requires all reformatted chapters)

### Within Each User Story

**User Story 1**:
- Extraction tasks (T011, T012) can run in parallel
- Analysis tasks (T013, T014) must run sequentially
- Documentation tasks (T015, T016, T017) build on analysis

**User Story 2**:
- Utility function tasks (T018-T021) can run in parallel where marked [P]
- Testing tasks (T024, T026) must run after script creation (T022, T023)
- Chapter processing (T027) is sequential but can be batched

**User Story 3**:
- Validation function tasks (T029-T033) can run in parallel where marked [P]
- Validation execution (T034-T039) mostly sequential

### Parallel Opportunities

- **Phase 1 Setup**: All 3 tasks can run sequentially (directory creation, install, update requirements)
- **Phase 2 Foundational**: Tasks T004, T005, T006, T007 marked [P] can run in parallel
- **Within User Story 2**: Tasks T019, T020, T021 marked [P] can run in parallel
- **Within User Story 3**: Tasks T029-T033 marked [P] can run in parallel
- **Polish Phase**: Tasks T040, T041 marked [P] can run in parallel

---

## Parallel Example: User Story 2

```bash
# Launch markdown utility functions together:
Task: "Implement format_lists function in scripts/reformat_manual/utils/markdown_utils.py"
Task: "Implement format_tables function in scripts/reformat_manual/utils/markdown_utils.py"
Task: "Implement apply_spacing_rules function in scripts/reformat_manual/utils/markdown_utils.py"
```

---

## Parallel Example: User Story 3

```bash
# Launch validation functions together:
Task: "Implement check_markdown_validity function in validate_output.py"
Task: "Implement check_heading_consistency function in validate_output.py"
Task: "Implement check_list_formatting function in validate_output.py"
Task: "Implement validate_unicode_brackets function in validate_output.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Verify formatting template is comprehensive
5. Review formatting-guide.md for completeness

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Formatting template established → Review formatting guide
3. Add User Story 2 → Chapters reformatted → Manual spot-check
4. Add User Story 3 → Validation complete → Final review
5. Each story adds value and moves toward complete reformatted manual

### Sequential Execution (Single Developer)

This project requires sequential execution due to dependencies:

1. Complete Setup + Foundational together
2. Complete User Story 1 (establishes formatting template)
3. Complete User Story 2 (uses template to reformat chapters)
4. Complete User Story 3 (validates reformatted output)
5. Stories must complete in priority order due to dependencies

---

## Notes

- [P] tasks = different files or independent functions, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently testable with its acceptance criteria
- Use `.venv/bin/python` for all script execution
- Commit after completing each user story phase
- Stop at checkpoints to validate story completion
- Unicode bracket preservation is critical - test early and often
- Content fidelity is non-negotiable - validate against source PDF
