# BL-208: Task File Ready for Q33NR Review

**Status:** TASK FILE WRITTEN
**Model:** Sonnet 4.5
**Date:** 2026-03-17
**Role:** Q33N (Queen Coordinator)

## Task File Created
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-17-TASK-BL-208-app-directory-sort-order.md`

## What Was Included

### Objective
Clear one-sentence objective: Update AppsHome to sort EGGs by status (BUILT first, STUB second) within each section, with visual divider.

### Context (Comprehensive)
- Current behavior documented (no status-based sorting exists)
- What needs to change (3 main points)
- Architecture overview (4 key files explained)
- Exact sort logic provided (code snippet with comments)
- Divider implementation approach (when to show, how to render)
- CSS snippet for divider (var(--sd-*) only)

### Files to Read First (4 files, all absolute paths)
- AppsHome.tsx (main component)
- AppsHome.css (styling)
- AppsHome.test.tsx (existing tests)
- types.ts (EggMeta interface, read-only)

### Deliverables (6 items, all checkboxed)
- Sort logic in groupedEggs useMemo
- Render status divider
- Add CSS class for divider
- Update existing tests
- Add 4-6 new tests (specific scenarios listed)

### Test Requirements (TDD)
- Tests first approach
- 10 existing tests + 4-6 new tests = 14-16 total expected
- 5 edge cases explicitly listed

### Acceptance Criteria (6 items, all checkboxed)
- BUILT before STUB within sections
- Visual divider between groups
- Divider uses var(--sd-*) only
- All tests pass (specific count: 14-16)
- No file over 500 lines (current AppsHome.tsx: 98 lines)
- No stubs

### Constraints (4 items)
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- TDD approach

### Test Commands (2 commands)
- AppsHome tests only (specific file path)
- All browser tests

### Response Requirements
- Full 8-section template included
- Specific output path given
- Reminder: DO NOT skip any section

## Model Assignment
haiku (per spec and briefing)

## Checklist for Q33NR Review

### Structure ✓
- [x] Objective: one sentence, concrete deliverable
- [x] Context: includes current state, what changes, why
- [x] Files to Read First: absolute paths
- [x] Deliverables: concrete outputs, checkboxed
- [x] Test Requirements: TDD, edge cases listed
- [x] Acceptance Criteria: specific, measurable, checkboxed
- [x] Constraints: all 4 hard rules present
- [x] Test commands: both provided with paths
- [x] Response requirements: 8-section template
- [x] Model assignment: haiku (correct per spec)

### Content Quality ✓
- [x] No vague language ("improve", "enhance", "optimize")
- [x] Specific implementation approach given (sort logic code snippet)
- [x] CSS pattern documented (var(--sd-*) only)
- [x] Test count expectation: 14-16 total (10 existing + 4-6 new)
- [x] Edge cases enumerated (5 scenarios)
- [x] File size check included (AppsHome.tsx currently 98 lines)

### No Gaps ✓
- [x] Sort logic provided (BUILT=0, STUB=1, ascending)
- [x] Divider render logic explained (insert between last BUILT and first STUB)
- [x] CSS snippet given (grid-column, height, background, margin)
- [x] Test scenarios specific (not generic "test sorting")
- [x] No stubs allowed (constraint explicitly stated)

### Adherence to Rules ✓
- [x] TDD required (tests first)
- [x] CSS variables only (no hardcoded colors)
- [x] No file over 500 lines
- [x] All paths absolute (4 files listed)
- [x] Response template: 8 sections mandatory

## Ready for Q33NR Review
This task file is complete and ready for Q33NR to review. It includes:
- Clear objective and context
- Specific implementation guidance (sort logic + divider approach)
- TDD test requirements with edge cases
- All constraints from BOOT.md
- Absolute file paths
- Model assignment: haiku

No corrections anticipated. Task is bee-ready after Q33NR approval.

## Next Steps for Q33NR
1. Review task file against checklist above
2. Verify all 8 response file sections are documented
3. Approve dispatch OR request corrections (max 2 cycles)
4. After approval: Q33N dispatches bee with haiku model
5. Q33N monitors for completion and reviews response file
6. Q33N reports results to Q33NR
