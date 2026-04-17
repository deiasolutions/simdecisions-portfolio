# TASK-235-REQUEUE: Wire PaneLoader into AppFrame

## Objective
Modify AppFrame.tsx to import and use the existing PaneLoader component so panes show a loading spinner while their applet content is mounting.

## Context

### What Already Works
- `browser/src/shell/components/PaneLoader.tsx` — 57-line working spinner component (/, -, \, |)
- `browser/src/shell/components/__tests__/PaneLoader.test.tsx` — 8 passing tests
- `browser/src/shell/components/__tests__/AppFrame.loading.test.tsx` — 8 tests written but currently FAILING

### What's Missing
AppFrame.tsx currently has ZERO loading state logic. It renders apps immediately or shows "Unknown app type" error.

The tests in AppFrame.loading.test.tsx expect:
1. **100ms delay before showing loader** — prevents flash on fast loads
2. **Loader shows when appType is set but component hasn't mounted**
3. **Loader hides when component renders** (at 150ms mark)
4. **Loader never shows for 'empty' appType**
5. **Loading state resets when appType changes**

### Why This Was Re-Queued
Original bee (Sonnet) created PaneLoader.tsx and wrote tests in TASK-235, but claimed to modify AppFrame.tsx to 86 lines with loading logic. Git history shows AppFrame.tsx is still 59 lines with NO loading logic. The changes never landed.

PaneLoader exists in the codebase but is never imported or used.

## Files to Read First

**Read these in order:**
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\AppFrame.tsx` — current state (NO loading logic, 59 lines)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneLoader.tsx` — existing component (works, don't recreate)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\AppFrame.loading.test.tsx` — tests that must pass

## Files to Modify

**ONLY modify this file:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\AppFrame.tsx`

**DO NOT modify these files (they already work):**
- PaneLoader.tsx — already exists and works
- PaneLoader.test.tsx — 8 tests already passing
- AppFrame.loading.test.tsx — tests already written, just need AppFrame changes to make them pass

## Technical Requirements

### Loading State Logic
Add the following loading state behavior to AppFrame.tsx:

1. **Import PaneLoader** at the top of the file
2. **Add loading state tracking** with these states:
   - `mounting` — component is loading
   - `showLoader` — 100ms has passed, show loader
   - `ready` — 150ms has passed, component is ready
3. **Timing logic:**
   - Start timer when appType changes
   - After 100ms: set `showLoader = true` (if still mounting)
   - After 150ms: set `ready = true`, hide loader
   - If appType is 'empty': never show loader
4. **Render logic:**
   - If `showLoader && !ready`: show PaneLoader
   - If `ready && Renderer exists`: show Renderer
   - If `ready && no Renderer`: show "Unknown app type" error
   - If appType is 'empty': show nothing (no loader, no error)
5. **Reset on appType change:** Clear all timers and reset state when node.appType changes

### Implementation Pattern
Use React `useState` and `useEffect` hooks:
- `useState` for loading state (showLoader, ready)
- `useEffect` with cleanup for timers
- `useEffect` dependency on `node.appType` to reset state

### Code Style
- All styles inline (no external CSS)
- Only CSS variables: `var(--sd-*)`
- Keep AppFrame.tsx under 150 lines (currently 59 lines)
- No hardcoded colors anywhere
- No stubs or TODOs

## Deliverables

- [ ] AppFrame.tsx imports PaneLoader from './PaneLoader'
- [ ] Loading state logic added with useState/useEffect
- [ ] 100ms delay before showing loader (prevents flash)
- [ ] 150ms timer to mark component ready
- [ ] Loader shown between 100-150ms if still mounting
- [ ] Loader never shown for 'empty' appType
- [ ] Loading state resets when appType changes
- [ ] All timers cleaned up on unmount and appType change
- [ ] All 8 tests in AppFrame.loading.test.tsx pass
- [ ] All 8 tests in PaneLoader.test.tsx still pass
- [ ] No regressions in other shell/ tests

## Test Requirements

### Target Tests (must pass)
```bash
cd browser && npx vitest run --reporter=verbose src/shell/components/__tests__/AppFrame.loading.test.tsx
```
**Expected:** 8/8 pass

### Existing Tests (must not regress)
```bash
cd browser && npx vitest run --reporter=verbose src/shell/components/__tests__/PaneLoader.test.tsx
```
**Expected:** 8/8 pass (already passing)

### Full Shell Suite (smoke test)
```bash
cd browser && npx vitest run --reporter=verbose src/shell/
```
**Expected:** No regressions from baseline

## Constraints

- **No file over 500 lines** (AppFrame.tsx currently 59 lines, keep under 150)
- **CSS: var(--sd-*) only** (PaneLoader already compliant, maintain in AppFrame)
- **No stubs** — full implementation required
- **MUST modify AppFrame.tsx** — that's the entire point of this re-queue
- **Do NOT recreate PaneLoader.tsx** — it already exists and works
- **Do NOT modify PaneLoader.tsx** — it's already correct
- **Do NOT modify the test files** — they're already correct

## Acceptance Criteria

- [ ] AppFrame.tsx imports PaneLoader
- [ ] Loading spinner shows when pane is mounting (after 100ms delay)
- [ ] No flash on fast loads (<100ms)
- [ ] Loading hidden for 'empty' appType
- [ ] Loading resets when appType changes
- [ ] AppFrame.loading.test.tsx: 8/8 pass
- [ ] PaneLoader.test.tsx: 8/8 pass (no regression)
- [ ] No new test failures in shell/ suite
- [ ] No hardcoded colors in AppFrame.tsx
- [ ] AppFrame.tsx stays under 150 lines

## Model Assignment

**sonnet** — Frontend logic with timing behavior requires careful state management.

## Priority

**P1** — Re-queue to fix incomplete work from previous task.

## Re-Queue Metadata

- **Original spec:** `.deia/hive/queue/_done/2026-03-16-SPEC-TASK-235-loading-states.md`
- **Previous response:** `.deia/hive/responses/20260317-TASK-235-RESPONSE.md`
- **Failure reason:** AppFrame.tsx changes never landed despite bee claiming to modify it
- **What exists:** PaneLoader.tsx (57 lines, works), PaneLoader.test.tsx (8 tests pass), AppFrame.loading.test.tsx (8 tests fail)
- **What's missing:** AppFrame.tsx modifications to import and use PaneLoader

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260318-TASK-235-REQUEUE-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes (what code was added to AppFrame.tsx)
4. **Test Results** — test files run, pass/fail counts for all three test commands
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
