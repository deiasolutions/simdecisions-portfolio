# TASK-BUG-028-FIX-TESTS: Fix BUG-028 Regression Tests

**Assigned to:** Sonnet
**Date:** 2026-03-25
**Priority:** P0 (blocking SPEC-BUG-028 completion)

---

## Objective

Fix the 3 failing regression tests in `BUG-028-regression.test.tsx` so all 5 tests pass. The implementation code is already correct — this is purely a test infrastructure issue.

---

## Context

The previous bee (20260324-TASK-BUG-028-RESPONSE.md) reported COMPLETE with 4/5 tests passing. Now we have 2/5 failing (tests degraded):

**Current state:** 2 failed, 3 passed
- ❌ "clicking a channel fires channel:selected bus event" — can't find `generalNode`
- ✅ "clicking a DM fires channel:selected with type=dm" — PASSING
- ✅ "clicking different channels sends separate events" — PASSING
- ❌ "non-channel tree-browser adapters do NOT send channel:selected" — tree shows "No items"
- ❌ "channel:selected event includes nonce and timestamp" — can't find event

**Root cause:** The mock `fetch` implementation doesn't match the real `fetch` interface. The channelsAdapter calls `res.json()` which expects an async method, but the test's mock returns a plain object with `async` keyword without actually being a proper Promise.

**Implementation is CORRECT:** `treeBrowserAdapter.tsx` lines 275-289 correctly emit `channel:selected` bus events. Do NOT modify implementation code.

---

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\BUG-028-regression.test.tsx` (test file to fix)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\channelsAdapter.ts` (how data is loaded)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx` (how adapter is wired)

---

## Deliverables

- [ ] Fix mock `fetch` implementation to properly match `Response` interface
- [ ] Fix test 1: "clicking a channel fires channel:selected bus event"
- [ ] Fix test 2: "non-channel tree-browser adapters do NOT send channel:selected"
- [ ] Fix test 3: "channel:selected event includes nonce and timestamp"
- [ ] All 5 tests in `BUG-028-regression.test.tsx` pass
- [ ] No changes to implementation code (treeBrowserAdapter.tsx, channelsAdapter.ts)
- [ ] Test output shows 5/5 passing

---

## Test Requirements

- [ ] Tests written FIRST (TDD) — tests already exist, fixing them
- [ ] All 5 tests pass
- [ ] Edge cases covered:
  - [ ] Channels load from mocked fetch
  - [ ] Tree nodes render with correct labels
  - [ ] Click events fire on tree nodes
  - [ ] Bus events are captured by MockMessageBus
  - [ ] Non-channel adapters don't emit channel:selected

---

## Investigation Checklist

Before fixing, verify these issues:

1. **Mock fetch structure:**
   - Current mock: `mockFetch.mockResolvedValueOnce({ ok: true, json: async () => channels })`
   - Problem: `json` needs to return a real Promise
   - Fix: `mockFetch.mockResolvedValueOnce({ ok: true, json: () => Promise.resolve(channels) })`

2. **Timing issues:**
   - The `waitFor` timeout is 3000ms — should be sufficient
   - Check if nodes actually render before clicking
   - Add debug logs if needed to see what's rendering

3. **DOM structure:**
   - Tests look for `.tree-node-row` and `.tree-node-label`
   - Verify these classes exist in TreeBrowser component
   - Check if nodes are nested under group nodes (Pinned, Channels, DMs)

4. **Adapter loading:**
   - channelsAdapter groups channels into sections: Pinned, Channels, DMs
   - Test data has `pinned: true` for 'general' — it will be under "Pinned" group
   - Tree nodes might be nested: group > channel
   - Search needs to expand groups first or search within children

---

## Constraints

- **No file over 500 lines** — test file is 285 lines, well under limit
- **CSS: var(--sd-\*) only** — not applicable (test file)
- **No stubs** — all test logic must be complete
- **TDD** — tests already exist, just fixing them
- **NO CHANGES TO IMPLEMENTATION CODE** — treeBrowserAdapter.tsx lines 275-289 are correct

---

## Acceptance Criteria

- [ ] All 5 tests in `BUG-028-regression.test.tsx` pass
- [ ] Test output shows: `Test Files  1 passed (1)` and `Tests  5 passed (5)`
- [ ] No implementation files modified (only test file modified)
- [ ] Mock fetch properly implements Response interface
- [ ] Tests account for grouped channel structure (Pinned/Channels/DMs)
- [ ] Response file includes full test output showing 5/5 passing

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260325-TASK-BUG-028-FIX-TESTS-RESPONSE.md`

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

---

## Test Command

```bash
cd browser && npx vitest run src/primitives/tree-browser/__tests__/BUG-028-regression.test.tsx
```

Expected output:
```
Test Files  1 passed (1)
Tests  5 passed (5)
```
