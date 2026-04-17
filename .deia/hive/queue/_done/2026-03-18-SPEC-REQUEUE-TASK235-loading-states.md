# TASK-235 (RE-QUEUE): Pane loading states — wire PaneLoader into AppFrame

## Background — Why Re-Queued
Original bee (Sonnet) created PaneLoader.tsx (57 lines, working component) and wrote 16 tests. But the AppFrame.tsx modifications never landed. PaneLoader exists but is never imported or used. This re-queue wires it in.

## Objective
Wire PaneLoader into AppFrame.tsx so panes show a loading spinner while their applet content is mounting.

## What Already Exists (DO NOT recreate)
- `browser/src/shell/components/PaneLoader.tsx` — 57 lines, working spinner component (/, -, \, |)
- `browser/src/shell/components/__tests__/PaneLoader.test.tsx` — 8 passing tests
- `browser/src/shell/components/__tests__/AppFrame.loading.test.tsx` — 8 tests (some may need fixes)

## What Is Missing
AppFrame.tsx has NO loading state logic. It needs:
1. Import PaneLoader
2. Add loading state with 100ms delay before showing (prevents flash on fast loads)
3. Show PaneLoader when appType is set but component hasn't mounted
4. Hide PaneLoader when component renders or when appType is 'empty'
5. Reset loading state when appType changes

## Files to Read First
- `browser/src/shell/components/AppFrame.tsx` (current state — no loading logic)
- `browser/src/shell/components/PaneLoader.tsx` (already exists and works)
- `browser/src/shell/components/__tests__/AppFrame.loading.test.tsx` (target: make these pass)

## Files to Modify
- `browser/src/shell/components/AppFrame.tsx` — add loading state + PaneLoader import

## Deliverables
- [ ] AppFrame.tsx imports and uses PaneLoader
- [ ] Loading spinner shows when pane is mounting (after 100ms delay)
- [ ] No flash on fast loads (<100ms)
- [ ] Loading hidden for 'empty' appType
- [ ] Loading resets when appType changes
- [ ] AppFrame.loading.test.tsx tests pass (8 tests)
- [ ] PaneLoader.test.tsx still passes (8 tests)
- [ ] No regressions in shell/ tests

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/shell/components/__tests__/PaneLoader.test.tsx`
- [ ] `cd browser && npx vitest run --reporter=verbose src/shell/components/__tests__/AppFrame.loading.test.tsx`
- [ ] `cd browser && npx vitest run --reporter=verbose src/shell/`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- MUST modify AppFrame.tsx (that's the whole point)
- Do NOT recreate PaneLoader.tsx — it already exists and works

## Model Assignment
sonnet

## Priority
P1

## Re-Queue Metadata
- Original spec: `_done/2026-03-16-SPEC-TASK-235-loading-states.md`
- Previous response: `20260317-TASK-235-RESPONSE.md`
- Failure reason: AppFrame.tsx changes never landed, PaneLoader created but never wired in
