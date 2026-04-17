# Briefing: Fix BUG-028 Regression Tests

**Date:** 2026-03-25
**From:** Q33NR (REGENT-QUEUE-TEMP-SPEC-BUG-028-EFEMER)
**To:** Q33N
**Model:** Sonnet

---

## Context

SPEC-BUG-028 was processed and the bee (20260324-TASK-BUG-028-RESPONSE.md) reported COMPLETE, stating the implementation was already present. The implementation IS correct:

- `treeBrowserAdapter.tsx` lines 275-289: emits `channel:selected` when a channel is clicked
- The implementation exists and is correct

However, the regression tests in `BUG-028-regression.test.tsx` are NOW FAILING:
- Run result: **3 failed, 2 passed** (was 4 passed, 1 failed in the bee's response)
- Failing tests:
  1. "clicking a channel fires channel:selected bus event" — can't find `generalNode`
  2. "non-channel tree-browser adapters do NOT send channel:selected" — tree shows "No items", not loading
  3. "channel:selected event includes nonce and timestamp" — can't find event

The 2 passing tests: "clicking a DM" and "clicking different channels"

---

## Objective

Fix the 3 failing regression tests in `BUG-028-regression.test.tsx` so all 5 tests pass. The implementation is correct — this is a test infrastructure issue.

---

## Investigation Required

1. **Check mock fetch setup:** The test mocks `fetch` to return channel data, but the tree is showing "No items" which means the data isn't loading
2. **Check timing issues:** Use longer timeouts or better waitFor conditions
3. **Check node selectors:** Tests look for `.tree-node-label` but maybe the structure changed
4. **Check if channelsAdapter is calling the mocked fetch:** Add debug logging or verify mock call count

---

## Files to Read

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\BUG-028-regression.test.tsx` (test file)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\channelsAdapter.ts` (adapter implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx` (wiring)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx` (component)

---

## Deliverables

1. Fixed test file where all 5 tests pass
2. No changes to implementation code (it's already correct)
3. Test output showing 5/5 passing

---

## Constraints

- TDD: tests MUST pass
- No changes to `treeBrowserAdapter.tsx` lines 275-289 (the implementation is correct)
- No changes to `channelsAdapter.ts` (unless it's genuinely broken)
- Fix the TEST infrastructure, not the implementation

---

## Acceptance Criteria

- [ ] All 5 tests in `BUG-028-regression.test.tsx` pass
- [ ] No implementation code changed (unless genuinely broken)
- [ ] Test output confirms 5/5 passing
- [ ] Response file includes full test output

---

## Priority

P0 — blocking SPEC-BUG-028 completion

---

## Task File Requirements

Write ONE task file:
- `TASK-BUG-028-FIX-TESTS.md`
- Assign to Sonnet
- Include test debugging steps
- Include all file paths (absolute)
- Include 8-section response file requirement
