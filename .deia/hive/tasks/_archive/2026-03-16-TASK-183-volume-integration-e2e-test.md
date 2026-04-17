# TASK-183: E2E test for volume storage integration

## Objective
Write end-to-end integration test that verifies the complete flow: tree-browser lists files → user clicks file → text-pane loads content. Use real backend with test volume.

## Context
This is the integration verification task. All prior tasks (TASK-180, TASK-181, TASK-182) must be complete before this task can run. This test verifies the complete user flow works end-to-end.

Test pattern follows existing E2E tests (see `tests/hivenode/test_e2e.py` for backend, and browser integration tests for frontend patterns).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\treeBrowserAdapter.test.tsx` (if exists, for adapter test patterns)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\__tests__\SDEditor.test.tsx` (for text-pane test patterns)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_storage_routes.py` (if exists, for backend storage test patterns)

## Deliverables
- [ ] Backend test: Create test volume, write test files, verify `/storage/list` and `/storage/read` work
- [ ] Frontend integration test: Mock backend responses, render TreeBrowserAdapter with filesystem adapter, click file node, verify bus event emitted
- [ ] Frontend text-pane test: Mock `/storage/read` endpoint, emit `file:selected` bus event, verify content loads
- [ ] Full integration test (optional, depends on test infrastructure): Render tree-browser + text-pane together, click file, verify content appears
- [ ] All tests pass

## Test Requirements
- [ ] Backend: test `/storage/list` returns entries for home://test/
- [ ] Backend: test `/storage/read` returns file content
- [ ] Backend: test `/storage/stat` returns metadata
- [ ] Frontend: test TreeBrowserAdapter emits `file:selected` on file click
- [ ] Frontend: test SDEditor loads content when `file:selected` received
- [ ] Frontend: test error handling (404, network error)
- [ ] Minimum 6 integration tests total
- [ ] All tests pass

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (not applicable)
- No stubs in implementation (tests can use mocks)
- Use existing E2E test patterns from codebase
- Tests should be fast (<5s total)
- Use vitest for frontend, pytest for backend

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-183-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
