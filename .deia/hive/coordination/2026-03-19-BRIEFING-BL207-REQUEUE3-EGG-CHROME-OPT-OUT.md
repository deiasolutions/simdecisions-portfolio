# BRIEFING: BL-207 (RE-QUEUE 3) — EGG chrome opt-out

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-19
**Model Assignment:** sonnet
**Priority:** P0

---

## Background

This is the **THIRD attempt** at BL-207. Both previous attempts FAILED because bees wrote verification briefings instead of changing source code.

**The problem is simple:** `browser/src/shell/eggToShell.ts` hardcodes `chrome: true` on lines 33 and 115. EGG files that set `"chrome": false` on a pane node are completely IGNORED.

**Root cause of previous failures:** Bees treated this as a verification task instead of an implementation task. They wrote tests or briefings but never modified the source file.

---

## What Q33N Must Do

Write ONE task file for ONE bee. The task must:

1. **Require the bee to modify `browser/src/shell/eggToShell.ts`** — specifically lines 33 and 115
2. **Make it crystal clear this is a CODE CHANGE task**, not a verification task
3. **Specify the exact changes** (see "The Fix" below)
4. **Include TDD requirements** (tests first, then implementation)
5. **Warn the bee explicitly:** "If you do not modify eggToShell.ts source code, you have FAILED."

---

## The Fix (Exact)

In `browser/src/shell/eggToShell.ts`:

**Line 33** — change from:
```typescript
chrome: true,
```
to:
```typescript
chrome: eggNode.chrome !== false,
```

**Line 115** — change from:
```typescript
chrome: true,
```
to:
```typescript
chrome: node.chrome !== false,
```

That's it. Two lines. The logic: default to `true` (backwards compatible), but respect `chrome: false` when present in EGG config.

---

## Files to Reference

- `browser/src/shell/eggToShell.ts` — THE file to modify (lines 33, 115)
- `browser/src/shell/types.ts` — ShellNode type definition (chrome field should already exist)
- `eggs/build-monitor.egg.md` — has `"chrome": false` on build-service pane, use as test case
- `browser/src/shell/__tests__/eggToShell.test.ts` — existing tests, add new tests for chrome field

---

## Deliverables (Task File Must Specify)

- [ ] `eggToShell.ts` modified — lines 33 and 115 now read `chrome` from EGG node config
- [ ] Default behavior: `chrome: true` when field is absent or `undefined` (backwards compatible)
- [ ] Explicit opt-out: `chrome: false` in EGG config produces shell node with `chrome: false`
- [ ] Tests written FIRST (TDD):
  - Test: EGG pane with `"chrome": false` → shell node has `chrome: false`
  - Test: EGG pane without chrome field → shell node has `chrome: true`
  - Test: EGG pane with `"chrome": true` → shell node has `chrome: true`
- [ ] All existing `eggToShell` tests still pass
- [ ] Full browser test suite passes

---

## Acceptance Criteria (Task File Must Include)

- [ ] Lines 33 and 115 in `eggToShell.ts` NO LONGER hardcode `chrome: true`
- [ ] EGG pane with `"chrome": false` hides title bar when rendered
- [ ] EGG pane without `chrome` field shows title bar (default ON)
- [ ] At least 3 new tests added to `eggToShell.test.ts`
- [ ] All tests pass: `cd browser && npx vitest run src/shell/__tests__/eggToShell.test.ts`
- [ ] Full test suite passes: `cd browser && npx vitest run`

---

## Constraints

- No file over 500 lines
- CSS: var(--sd-*) only (though this task is TypeScript, not CSS)
- No stubs
- **CRITICAL:** The bee MUST modify `eggToShell.ts`. If the bee does not modify this file, the task has FAILED.

---

## Smoke Test

After implementation:
```bash
cd browser && npx vitest run --reporter=verbose src/shell/__tests__/eggToShell.test.ts
cd browser && npx vitest run --reporter=verbose src/shell/
cd browser && npx vitest run
```

---

## Why This Failed Twice Before

- **First failure:** Bee wrote a "runtime verify briefing" instead of changing code
- **Second failure:** Bee treated it as verification task again, wrote tests but didn't modify source

Both times the bee misunderstood the task as "verify the feature works" instead of "implement the feature."

---

## Q33N Instructions

1. Read `browser/src/shell/eggToShell.ts` (THE file to change)
2. Read `browser/src/shell/types.ts` (type definitions)
3. Read `browser/src/shell/__tests__/eggToShell.test.ts` (existing tests)
4. Read `eggs/build-monitor.egg.md` (example EGG with chrome: false)
5. Write ONE task file with clear, explicit instructions to modify eggToShell.ts
6. Include exact line numbers and exact code changes in the task
7. Emphasize TDD: tests first, then implementation
8. Add explicit warning: "If you do not modify eggToShell.ts source code, you have FAILED."
9. Return to Q33NR for review BEFORE dispatching

---

## Model Assignment

**Bee model:** haiku (this is a 2-line change with tests, straightforward)

---

## Expected Timeline

- Q33N writes task: 5-10 minutes
- Q33NR reviews task: 2-5 minutes
- Bee implementation: 15-25 minutes (TDD + tests + verification)
- Total: ~45 minutes

---

## Success Criteria for Q33N

Your task file is successful if:
- It explicitly states "modify eggToShell.ts lines 33 and 115"
- It includes the exact code change (from `chrome: true` to `chrome: eggNode.chrome !== false`)
- It requires tests FIRST (TDD)
- It warns the bee that failing to modify source = FAILURE
- Q33NR approves it on first review

---

## Questions for Q33N

None. This is fully specified. Execute.

---

**End of briefing.**
