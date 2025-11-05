# Editorial Review Strategy

**Feature**: `001-reformat-manual`
**Stage**: 03_edited (to be created)
**Date**: 2025-11-05

## Objective

Review and improve chapter content for clarity, consistency, and quality while maintaining the original meaning and structure.

## Scope

**In Scope:**
- Grammar and clarity improvements
- Identifying redundancies
- Fixing unclear or ambiguous language
- Balancing bullet point hierarchies
- Structural improvements within sections

**Out of Scope:**
- Changing content meaning or intent
- Adding new information not in source
- Removing substantive content
- Major reorganization of chapters

## Processing Order

Process chapters from smallest to largest to develop editing patterns before tackling larger chapters:

1. Chapter 8 (2.9K) - smallest
2. Chapter 7 (3.1K)
3. Chapter 0 (6.7K)
4. Chapter 3 (22K)
5. Chapter 2 (28K)
6. Chapter 4 (47K)
7. Chapter 1 (52K)
8. **[SKIP]** Chapter 9 (30K) - deferred
9. **[LATER]** Chapter 5 Part 1 (130K) - needs special handling
10. **[LATER]** Chapter 5 Part 2 (121K) - needs special handling

## Workflow per Chapter

### 1. Initial Review
- Read chapter completely for overall understanding
- Note themes, structure, and purpose
- Identify major sections

### 2. Issue Identification
Scan for:
- **Grammar issues**: Subject-verb agreement, tense consistency, punctuation
- **Clarity problems**: Ambiguous pronouns, unclear references, confusing phrasing
- **Redundancies**: Repeated information, duplicate points
- **Hierarchy issues**:
  - Over-nested bullets (too many levels)
  - Under-nested bullets (missing structure)
  - Mixed nesting patterns
- **Consistency**: Terminology, formatting, style

### 3. Generate Improvement List
For each issue, document:
- **Location**: Section/heading where issue appears
- **Type**: Grammar, clarity, redundancy, hierarchy, etc.
- **Excerpt**: Relevant text showing the issue (20-50 words)
- **Problem**: What's wrong
- **Proposed fix**: How to improve it
- **Impact**: Minor/Medium/Major
- **Confidence**: High/Medium-High/Medium/Low - how confident in the proposed fix

### 4. User Review
Present improvements as a numbered list for user approval:
```
1. [GRAMMAR] Section 2.1.3 - Subject-verb disagreement
   Current: "The caregivers is responsible..."
   Fix: "The caregivers are responsible..."
   Impact: Minor
   Confidence: High - clear grammatical error

2. [CLARITY] Section 2.4 - Ambiguous pronoun
   Current: "Remove the item and clean it. Store it properly."
   Fix: "Remove the item and clean it. Store the item properly."
   Impact: Minor
   Confidence: Medium - could be interpreted either way
```

User responds with which items to fix (e.g., "Fix all", "Fix 1, 2, 5, 7", or requests discussion for low-confidence items)

### 5. Apply Approved Changes
- Make only approved edits
- Preserve original intent
- Maintain markdown formatting
- Keep unicode brackets if present

### 6. Save to Next Stage
- Output to `output/chapters/03_edited/`
- Generate diff/change summary
- Update chapter completion tracking

## Issue Type Definitions

### Grammar
- Subject-verb agreement
- Tense consistency
- Punctuation errors
- Capitalization issues
- Article usage (a/an/the)

### Clarity
- Ambiguous pronouns (it, they, this, that)
- Unclear references
- Confusing sentence structure
- Missing context
- Overly complex phrasing

### Redundancy
- Repeated information in same section
- Duplicate bullet points
- Redundant modifiers
- Unnecessary repetition

### Hierarchy
- Bullets that should be nested deeper
- Bullets that should be promoted to higher level
- Inconsistent nesting patterns
- Missing parent items for nested bullets
- Over-nested lists (4+ levels)

### Consistency
- Terminology variations (pick one term and use consistently)
- Formatting inconsistencies
- Style variations
- Numbering pattern inconsistencies

## Special Considerations

### Unicode Brackets (˹˺)
**Preserve exactly** - these mark terms for future Anki card generation.
Do not remove, modify, or add brackets.

### Chapter 5 (Large Chapters)
Due to context window constraints:
- Process in smaller sections
- May need multiple passes
- Use separate strategy document if needed

### Chapter 9 (Deferred)
Skip for now - will process later with different approach.

## Output Structure

```
output/chapters/03_edited/
├── chapter_08.md           # Edited chapters
├── chapter_07.md
├── [...]
└── EDITORIAL_REPORT.md     # Summary of all changes
```

Each chapter edit generates:
- Edited chapter file
- Individual change log (optional)
- Contribution to overall editorial report

## Quality Checks

Before marking chapter complete:
- [ ] All approved changes applied
- [ ] No unapproved changes made
- [ ] Markdown formatting valid
- [ ] Unicode brackets preserved (if present)
- [ ] Headings and structure intact
- [ ] No content meaning changed

## Progress Tracking

Track completion in todo list:
- Chapter reviewed
- Improvements identified
- User approved changes
- Changes applied
- Output saved to 03_edited/
- Move to next chapter

---

**Status**: In Progress (3 of 10 chapters completed)
**Completed**: Chapters 0, 7, 8
**Current Chapter**: Chapter 3 (22K) - next to process

## Actual Experience Notes

### Confidence Ratings Proved Valuable
Adding confidence ratings helped identify items that needed user discussion:
- High confidence items (~80%): Usually approved immediately
- Medium confidence items (~15%): Sometimes needed clarification
- Low confidence items (~5%): Always required user input

### Common Patterns Identified
- Story/section headings often have placeholder text ("STORY_TITLE")
- Table of contents sections need labeling
- Unicode brackets require careful preservation
- Signature blocks often need reformatting
- Editorial notes should be flagged, not removed immediately

### Flagged Issues Strategy
For content decisions beyond grammar/clarity:
- Flag issue clearly in change log
- Mark location in edited document
- Document alternatives/questions
- Defer resolution to future pass
- Example: Duplicate content sections requiring reconciliation
