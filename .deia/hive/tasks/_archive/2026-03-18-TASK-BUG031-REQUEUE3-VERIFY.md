# TASK-BUG031-REQUEUE3: Verify Code Explorer File Loading (Already Fixed)

## Objective

Verify that BUG-031 (Code explorer click error) has already been fixed in the source code and document the current state with comprehensive tests.

## Context

**This is a FALSE POSITIVE requeue.** The fix described in the briefing has already been applied to the source code:

- `treeBrowserAdapter.tsx` lines 189-211 already send `file:selected` events with:
  - `name: node.label` (line 204)
  - `uri` with protocol prefix `${protocol}${path}` (line 193)
  - Only for files, not directories (line 190: `!node.children` check)

Tests at `src/apps/__tests__/treeBrowserAdapter.test.tsx` are passing (6/6 tests).

## Root Cause of Requeue

Prior fix cycles likely failed due to infrastructure issues (missing task file paths in `_active/`, now resolved by separate spec). The actual bug fix was completed in an earlier attempt.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx` (lines 189-211)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\treeBrowserAdapter.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx` (lines 312-354)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\storage_routes.py` (lines 57-76)

## Deliverables

- [ ] Read source code and confirm fix is present
- [ ] Run existing tests and confirm all pass
- [ ] Add integration test for file:selected → SDEditor → /storage/read flow
- [ ] Document current implementation status
- [ ] Write response file with FALSE POSITIVE finding

## Test Requirements

### Test 1: Verify file:selected Event Structure (already exists)
File: `browser/src/apps/__tests__/treeBrowserAdapter.test.tsx`
- [x] Confirms `name` field is present
- [x] Confirms URI has protocol prefix
- [x] Confirms directories don't emit file:selected

### Test 2: Add Integration Test for File Load Flow
File: `browser/src/apps/__tests__/treeBrowserAdapter.integration.test.tsx` (NEW)
- [ ] Mount TreeBrowserAdapter with filesystem config
- [ ] Mock /storage/read endpoint
- [ ] Click a file node
- [ ] Verify file:selected event contains: uri (with protocol), name, path
- [ ] Verify SDEditor receives correct data structure
- [ ] Verify no "Bad Request URI" error

### Test 3: Verify SDEditor file:selected Handler
File: `browser/src/primitives/text-pane/__tests__/SDEditor.fileSelected.test.tsx` (NEW)
- [ ] Send file:selected event with correct structure
- [ ] Verify SDEditor calls `/storage/read?uri=home://path`
- [ ] Verify content loads and displays
- [ ] Send file:selected with missing `name` — verify fallback
- [ ] Send file:selected with URI without protocol — verify error handling

## Acceptance Criteria

- [ ] All existing treeBrowserAdapter tests pass (6 tests)
- [ ] New integration test passes (5+ assertions)
- [ ] SDEditor file:selected handler test passes (5+ tests)
- [ ] Source code inspection confirms fix is present (lines documented in response)
- [ ] Response file marks this as FALSE POSITIVE with evidence

## Smoke Test Commands

```bash
# Existing tests (must all pass)
cd browser && npx vitest run --reporter=verbose src/apps/__tests__/treeBrowserAdapter.test.tsx

# New integration test
cd browser && npx vitest run --reporter=verbose src/apps/__tests__/treeBrowserAdapter.integration.test.tsx

# SDEditor file:selected test
cd browser && npx vitest run --reporter=verbose src/primitives/text-pane/__tests__/SDEditor.fileSelected.test.tsx

# Full text-pane suite (no regressions)
cd browser && npx vitest run --reporter=verbose src/primitives/text-pane/
```

## Constraints (10 Hard Rules Apply)

- No file over 500 lines
- CSS: var(--sd-*) only (no hardcoded colors)
- No stubs or TODOs
- TDD: tests first, then implementation (integration tests only — implementation already exists)
- All file paths must be absolute
- This is a VERIFICATION task, not an implementation task

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-BUG031-REQUEUE3-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (FALSE_POSITIVE), model, date
2. **Files Modified** — list of NEW test files only (source code unchanged)
3. **What Was Done** — verification steps, evidence of existing fix
4. **Test Results** — all test pass counts (existing + new)
5. **Build Verification** — test suite output summary
6. **Acceptance Criteria** — copy from above, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — recommend closing BUG-031 as FIXED

**CRITICAL:** Mark status as "FALSE_POSITIVE — Fix Already Applied" and provide line numbers from source code as evidence.

## Model Assignment

Sonnet — This requires careful source code inspection and comprehensive test coverage.

## Priority

P0 (to close false positive quickly)
