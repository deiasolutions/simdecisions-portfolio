# BRIEFING: BL-207 Re-Queue 2 — EGG chrome opt-out

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-18
**Priority:** P0
**Model Assignment:** sonnet

---

## CRITICAL: This Spec Has Failed TWICE

**Re-queue 1:** Bee wrote a "runtime verify briefing" instead of changing code.
**Re-queue 2 (THIS ROUND):** We are here because the previous bee DID NOT CHANGE SOURCE CODE.

**THE SPEC EXPLICITLY STATES:**
> "YOU MUST CHANGE eggToShell.ts SOURCE CODE. If you only write tests or a briefing, you have FAILED."

---

## The Problem

`browser/src/shell/eggToShell.ts` lines 33 and 115 hardcode `chrome: true`. EGG configs that set `chrome: false` on a pane node are IGNORED.

**Example:** `eggs/build-monitor.egg.md` line 37 sets `"chrome": false` on the build-service pane. This is currently IGNORED. The title bar shows anyway.

---

## The Fix (EXACT — Do NOT Deviate)

In `browser/src/shell/eggToShell.ts`:

### Line 33 — CHANGE THIS:
```typescript
chrome: true,
```

### TO THIS:
```typescript
chrome: eggNode.chrome !== false,
```

### Line 115 — CHANGE THIS:
```typescript
chrome: true,
```

### TO THIS:
```typescript
chrome: node.chrome !== false,
```

**That's it. Two lines. No other changes.**

---

## Files to Modify

- `browser/src/shell/eggToShell.ts` — lines 33 and 115 only

---

## Files to Read First

- `browser/src/shell/eggToShell.ts` (THE file to change)
- `browser/src/shell/types.ts` (ShellNode type definition)
- `eggs/build-monitor.egg.md` (has `"chrome": false` on build-service pane — use as test case)
- `browser/src/eggs/types.ts` (EggLayoutNode type definition)

---

## Task File Requirements

The task file you write MUST include:

### Deliverables
- [ ] eggToShell.ts lines 33 and 115 changed (no other lines)
- [ ] Panes with `"chrome": false` in EGG config hide their title bar
- [ ] Panes without chrome field still show title bar (backwards compatible)
- [ ] Tests: EGG with chrome:false produces shell node with chrome:false
- [ ] Tests: EGG without chrome field produces shell node with chrome:true
- [ ] Existing eggToShell tests still pass

### Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing eggToShell tests pass
- [ ] New tests verify chrome field is read from EGG config
- [ ] Edge case: chrome undefined → defaults to true
- [ ] Edge case: chrome true → true
- [ ] Edge case: chrome false → false

### Acceptance Criteria
- [ ] `chrome: true` is NO LONGER hardcoded on lines 33 and 115
- [ ] EGG pane with `"chrome": false` hides title bar
- [ ] EGG pane without chrome field shows title bar (default ON)
- [ ] All eggToShell tests pass

### Smoke Test Commands
```bash
cd browser && npx vitest run --reporter=verbose src/shell/__tests__/eggToShell.test.ts
cd browser && npx vitest run --reporter=verbose src/shell/
cd browser && npx vitest run
```

---

## Constraints

- No file over 500 lines
- CSS: var(--sd-*) only (not applicable here)
- No stubs
- **THE BEE MUST CHANGE SOURCE CODE IN eggToShell.ts**
- **If the bee only writes tests or a briefing, the task has FAILED**

---

## Expected Behavior After Fix

1. Load build-monitor.egg (has `chrome: false` on build-service pane)
2. The build-service pane should have NO title bar
3. Other panes (with no chrome field) should have title bars

---

## What Q33N Must Do

1. **Read the files listed above**
2. **Write ONE task file** for a bee
3. **The task file must explicitly state:** "Change lines 33 and 115 in eggToShell.ts"
4. **The task file must explicitly warn:** "Do NOT write only tests. Do NOT write only a briefing. You MUST modify the source code."
5. **Return the task file to me (Q33NR) for review**

---

## What the BEE Must Do

1. **Read eggToShell.ts**
2. **Change line 33** from `chrome: true,` to `chrome: eggNode.chrome !== false,`
3. **Change line 115** from `chrome: true,` to `chrome: node.chrome !== false,`
4. **Write tests** to verify the change
5. **Run all tests** and ensure they pass
6. **Write response file** with all 8 sections

---

## Why This Failed Before

**Re-queue 1:** Bee wrote a briefing file instead of changing code.
**Root cause:** Task file was not explicit enough about requiring SOURCE CODE changes.

**This time:** Task file MUST be crystal clear: "Modify eggToShell.ts lines 33 and 115. If you do not change these lines, you have failed."

---

## Success Criteria for Q33N

- [ ] Task file explicitly states: "Change lines 33 and 115 in eggToShell.ts"
- [ ] Task file explicitly warns: "Do NOT only write tests. You MUST modify source code."
- [ ] Task file includes deliverables for source code changes
- [ ] Task file includes test requirements
- [ ] Task file includes smoke test commands

---

## Model Assignment

**Bee model:** sonnet (this is a simple 2-line change, but requires understanding context)

---

## Priority

P0 — This has failed twice. It must succeed this time.
