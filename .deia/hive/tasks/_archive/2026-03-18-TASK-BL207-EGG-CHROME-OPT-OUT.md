# TASK-BL207: EGG Chrome Opt-Out — Fix Hardcoded chrome:true

**Priority:** P0
**Assigned Model:** sonnet
**Re-queue:** 2 (previous attempts failed to modify source code)

---

## CRITICAL: You MUST Modify Source Code

**This task has FAILED TWICE because the bee did NOT change source code.**

**YOU MUST CHANGE `browser/src/shell/eggToShell.ts` lines 33 and 115.**

**If you only write tests, you have FAILED.**
**If you only write a briefing, you have FAILED.**
**If you do not change lines 33 and 115, you have FAILED.**

---

## Objective

Change `browser/src/shell/eggToShell.ts` to respect the `chrome` field from EGG config instead of hardcoding `chrome: true`.

When an EGG pane node sets `"chrome": false`, the shell AppNode must have `chrome: false`.

---

## Context

`browser/src/shell/eggToShell.ts` is the converter that transforms EGG layout JSON (from `.egg.md` files) into shell state nodes.

**Current problem:**
- Lines 33 and 115 hardcode `chrome: true`
- EGG configs that set `chrome: false` are IGNORED
- Example: `eggs/build-monitor.egg.md` line 37 sets `"chrome": false` on the build-service pane, but the title bar still shows

**Why this matters:**
- The build-service pane is a compact status bar (28px tall)
- Adding a title bar on top of it makes it 56px tall
- The EGG says `chrome: false` but it's ignored

**The types already support this:**
- `EggLayoutNode` (eggs/types.ts line 37) has: `chrome?: boolean`
- `AppNode` (shell/types.ts line 67) has: `chrome: boolean`
- The converter just needs to READ the field instead of hardcoding `true`

---

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts` — THE FILE YOU MUST CHANGE
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts` — AppNode type (chrome field)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\types.ts` — EggLayoutNode type (chrome field)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\build-monitor.egg.md` — test case (line 37: `"chrome": false`)
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\eggToShell.test.ts` — existing tests

---

## Exact Changes Required

### Change 1: Line 33 in browser/src/shell/eggToShell.ts

**BEFORE:**
```typescript
chrome: true,
```

**AFTER:**
```typescript
chrome: eggNode.chrome !== false,
```

### Change 2: Line 115 in browser/src/shell/eggToShell.ts

**BEFORE:**
```typescript
chrome: true,
```

**AFTER:**
```typescript
chrome: node.chrome !== false,
```

**That's it. Two lines. No other changes to eggToShell.ts.**

---

## Why This Logic?

`eggNode.chrome !== false` means:
- If `chrome` is `undefined` → defaults to `true` (backwards compatible)
- If `chrome` is `true` → `true`
- If `chrome` is `false` → `false`

This is the correct behavior. EGG panes without a `chrome` field should show the title bar (default ON). EGG panes with `"chrome": false` should hide it.

---

## Deliverables

- [ ] Line 33 changed from `chrome: true,` to `chrome: eggNode.chrome !== false,`
- [ ] Line 115 changed from `chrome: true,` to `chrome: node.chrome !== false,`
- [ ] No other lines in eggToShell.ts changed
- [ ] Tests written to verify the change
- [ ] All existing eggToShell tests still pass
- [ ] New tests verify chrome field is read from EGG config
- [ ] Response file written with all 8 sections

---

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] Test: EGG pane with `chrome: false` produces AppNode with `chrome: false`
- [ ] Test: EGG pane with `chrome: true` produces AppNode with `chrome: true`
- [ ] Test: EGG pane with NO chrome field produces AppNode with `chrome: true` (default)
- [ ] All existing eggToShell tests pass
- [ ] New tests added to `browser/src/shell/__tests__/eggToShell.test.ts`

**Test file location:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\eggToShell.test.ts`

---

## Acceptance Criteria

- [ ] `chrome: true` is NO LONGER hardcoded on line 33
- [ ] `chrome: true` is NO LONGER hardcoded on line 115
- [ ] EGG pane with `"chrome": false` produces shell node with `chrome: false`
- [ ] EGG pane without chrome field produces shell node with `chrome: true`
- [ ] EGG pane with `"chrome": true` produces shell node with `chrome: true`
- [ ] All eggToShell tests pass
- [ ] build-monitor.egg.md test case verified (build-service pane has chrome:false)

---

## Constraints

- No file over 500 lines (eggToShell.ts is currently 147 lines — safe)
- CSS: var(--sd-*) only (not applicable — this is TypeScript)
- No stubs
- **MUST modify eggToShell.ts source code**

---

## Smoke Test Commands

Run these after making changes:

```bash
# Test the specific file
cd browser && npx vitest run --reporter=verbose src/shell/__tests__/eggToShell.test.ts

# Test the entire shell module
cd browser && npx vitest run --reporter=verbose src/shell/

# Full test suite
cd browser && npx vitest run
```

All tests must pass.

---

## Expected Behavior After Fix

1. Open the build-monitor EGG in the app
2. The `build-service` pane (line 37 in build-monitor.egg.md) should have NO title bar
3. Other panes (without chrome field) should have title bars

This is currently broken because the `chrome: false` in the EGG is ignored.

After your fix, the `chrome: false` will be respected.

---

## Response Requirements — MANDATORY

When you finish, write:

`.deia/hive/responses/20260318-TASK-BL207-RESPONSE.md`

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

## WARNING: What NOT To Do

**DO NOT:**
- Only write tests without changing source code
- Only write a briefing without changing source code
- Change any other lines in eggToShell.ts besides 33 and 115
- Modify other files (except adding tests to eggToShell.test.ts)
- Ship stubs or `// TODO` comments
- Skip the response file

**IF YOU DO NOT CHANGE LINES 33 AND 115 IN eggToShell.ts, YOU HAVE FAILED THIS TASK.**

---

## Success Checklist

Before writing your response file, verify:

- [ ] I changed line 33 in eggToShell.ts
- [ ] I changed line 115 in eggToShell.ts
- [ ] I wrote tests to verify the change
- [ ] All existing tests pass
- [ ] All new tests pass
- [ ] No stubs or TODOs in my code
- [ ] I wrote a response file with all 8 sections

If any checkbox is unchecked, you have NOT completed this task.

---

**END OF TASK FILE**
