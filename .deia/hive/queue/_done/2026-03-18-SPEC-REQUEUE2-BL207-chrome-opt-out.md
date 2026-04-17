# BL-207 (RE-QUEUE 2): EGG chrome opt-out — MUST MODIFY eggToShell.ts

## Background — Why Re-Queued AGAIN
First re-queue bee wrote a "runtime verify briefing" instead of changing code. eggToShell.ts STILL hardcodes `chrome: true` on lines 33 and 115. Zero source changes landed. This is the second re-queue.

## THE PROBLEM
`browser/src/shell/eggToShell.ts` lines 33 and 115 hardcode `chrome: true`. EGG configs that set `chrome: false` on a pane node are IGNORED. The user cannot suppress title bars via EGG config.

## THE FIX (exact)
In `browser/src/shell/eggToShell.ts`:

Line 33 — change:
```typescript
chrome: true,
```
to:
```typescript
chrome: eggNode.chrome !== false,
```

Line 115 — change:
```typescript
chrome: true,
```
to:
```typescript
chrome: node.chrome !== false,
```

That's it. Two lines. The EGG pane config already has a `chrome` field — it's just being ignored.

## Files to Modify
- `browser/src/shell/eggToShell.ts` — lines 33 and 115, read `chrome` from EGG node config

## Files to Read First
- `browser/src/shell/eggToShell.ts` (THE file to change)
- `browser/src/shell/types.ts` (ShellNode type definition — verify chrome field exists)
- `eggs/build-monitor.egg.md` (has `"chrome": false` on build-service pane — use as test case)

## Deliverables
- [ ] eggToShell.ts reads `chrome` from EGG pane config (defaults true if not set)
- [ ] Panes with `"chrome": false` in EGG config hide their title bar
- [ ] Panes without chrome field still show title bar (backwards compatible)
- [ ] Tests: EGG with chrome:false produces shell node with chrome:false
- [ ] Tests: EGG without chrome field produces shell node with chrome:true
- [ ] Existing eggToShell tests still pass

## Acceptance Criteria
- [ ] `chrome: true` is NO LONGER hardcoded on lines 33 and 115
- [ ] EGG pane with `"chrome": false` hides title bar
- [ ] EGG pane without chrome field shows title bar (default ON)
- [ ] All eggToShell tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/shell/__tests__/eggToShell.test.ts`
- [ ] `cd browser && npx vitest run --reporter=verbose src/shell/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- YOU MUST CHANGE eggToShell.ts SOURCE CODE. If you only write tests or a briefing, you have FAILED.

## Model Assignment
sonnet

## Priority
P0

## Re-Queue Metadata
- Original spec: `_done/2026-03-17-SPEC-TASK-BL207-unified-title-bar.md`
- Re-queue 1: `_done/2026-03-18-SPEC-REQUEUE-BL207-unified-title-bar.md` (bee wrote briefing, not code)
- Failure reason: Bee treated it as verification instead of implementation. TWICE.
