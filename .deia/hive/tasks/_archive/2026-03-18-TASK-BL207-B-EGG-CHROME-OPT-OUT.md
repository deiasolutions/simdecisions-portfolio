# TASK-BL207-B: EGG Chrome Opt-Out (SOURCE CODE FIX)

## Objective
Modify `eggToShell.ts` to read the `chrome` field from EGG pane config instead of hardcoding `chrome: true` on lines 33 and 115.

## Context

**CRITICAL:** This is a SOURCE CODE MODIFICATION task, NOT a verification or testing task. You MUST modify the file `eggToShell.ts`.

**The Problem:**
The file `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts` currently hardcodes `chrome: true` on two lines:
- Line 33: `chrome: true,` (in pane node conversion)
- Line 115: `chrome: true,` (in fallback/unknown node handling)

This ignores the `chrome` field in EGG pane configs. When an EGG pane sets `"chrome": false` (like build-monitor.egg.md line 37), the title bar is still shown.

**The Solution:**
Change both lines to read the `chrome` field from the EGG node config, defaulting to `true` if not specified.

**Why:**
EGG files like `build-monitor.egg.md` need to opt out of chrome on specific panes (e.g., the build-data-service pane which is 28px tall and shouldn't have a title bar).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts` — THE file to modify
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts` — AppNode type has `chrome: boolean` field
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\types.ts` — EggLayoutNode allows any fields via `[key: string]: unknown`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\build-monitor.egg.md` — test case with `"chrome": false` on line 37
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\eggToShell.test.ts` — existing tests (275 lines)

## Deliverables

### Source Code Changes (MANDATORY)

**YOU MUST MODIFY THIS FILE:**
`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts`

**Line 33 — Change FROM:**
```typescript
chrome: true,
```

**TO:**
```typescript
chrome: eggNode.chrome !== false,
```

**Line 115 — Change FROM:**
```typescript
chrome: true,
```

**TO:**
```typescript
chrome: true,
```

**Note:** Line 115 is in the fallback handler for unknown node types. Since there's no EGG node to read from in that branch (it's a warning case), leave it as hardcoded `true`. Only line 33 needs the dynamic read.

**Wait — correction after re-reading the code:**

Looking at line 115 more carefully, it's in the fallback/unknown handler which doesn't have access to a chrome field. The briefing was wrong to say both lines need changing. **ONLY line 33 needs to change.**

Let me re-examine the code... Line 115 is in the "unknown node type" fallback at the bottom of `eggLayoutToShellTree`. It creates a default empty pane. There's no `eggNode.chrome` to read because we're in the unknown case. So line 115 should stay `chrome: true` (default behavior for unknown nodes).

**CORRECTED DELIVERABLES:**

- [ ] Modify `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts` line 33 to read `chrome` from `eggNode.chrome` (defaults `true` if not set)
- [ ] Line 115 stays as-is (`chrome: true`) because it's the fallback handler with no EGG node to read from
- [ ] Add test case: EGG pane with `"chrome": false` → shell node with `chrome: false`
- [ ] Add test case: EGG pane without `chrome` field → shell node with `chrome: true` (default)
- [ ] Add test case: EGG pane with `"chrome": true` → shell node with `chrome: true`
- [ ] All existing `eggToShell.test.ts` tests still pass (should be 21 existing tests)

## Test Requirements

**Write tests FIRST (TDD)**

Add these test cases to `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\eggToShell.test.ts`:

1. **EGG pane with `chrome: false` produces shell node with `chrome: false`**
   ```typescript
   const eggLayout: EggLayoutNode = {
     type: 'pane',
     appType: 'terminal',
     chrome: false,
   }
   const result = eggLayoutToShellTree(eggLayout)
   expect((result as any).chrome).toBe(false)
   ```

2. **EGG pane without chrome field produces shell node with `chrome: true` (default)**
   ```typescript
   const eggLayout: EggLayoutNode = {
     type: 'pane',
     appType: 'terminal',
   }
   const result = eggLayoutToShellTree(eggLayout)
   expect((result as any).chrome).toBe(true)
   ```

3. **EGG pane with `chrome: true` produces shell node with `chrome: true`**
   ```typescript
   const eggLayout: EggLayoutNode = {
     type: 'pane',
     appType: 'terminal',
     chrome: true,
   }
   const result = eggLayoutToShellTree(eggLayout)
   expect((result as any).chrome).toBe(true)
   ```

**Test execution:**
```bash
cd browser && npx vitest run --reporter=verbose src/shell/__tests__/eggToShell.test.ts
```

**Expected result:**
- All 21 existing tests pass
- 3 new tests pass
- Total: 24 tests passing

## Constraints
- No file over 500 lines (eggToShell.ts is currently 147 lines, safe)
- CSS: var(--sd-*) only (NO CSS CHANGES NEEDED FOR THIS TASK)
- No stubs
- **YOU MUST MODIFY SOURCE CODE.** This is not a verification task. Change line 33 in eggToShell.ts.

## Acceptance Criteria

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts` line 33 changed from `chrome: true,` to `chrome: eggNode.chrome !== false,`
- [ ] Line 115 unchanged (it's the fallback handler, should stay `chrome: true`)
- [ ] Test: EGG pane with `chrome: false` → shell node with `chrome: false`
- [ ] Test: EGG pane without chrome field → shell node with `chrome: true` (default)
- [ ] Test: EGG pane with `chrome: true` → shell node with `chrome: true`
- [ ] All existing eggToShell tests pass (21 tests)
- [ ] New tests pass (3 tests)
- [ ] Smoke test: `cd browser && npx vitest run --reporter=verbose src/shell/__tests__/eggToShell.test.ts` shows 24 tests passing

## Build Verification

After making changes, run:
```bash
cd browser && npx vitest run --reporter=verbose src/shell/__tests__/eggToShell.test.ts
```

Confirm:
- 24 tests pass
- 0 tests fail
- No errors about chrome being undefined or null

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260318-TASK-BL207-B-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes (e.g., "Changed line 33 from `chrome: true` to `chrome: eggNode.chrome !== false`")
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test output summary (last 10 lines)
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Why This Is Re-Queue #2

**First attempt:** Bee delivered BL-207 but left `chrome: true` hardcoded on lines 33 and 115.

**Re-queue 1:** Bee wrote `.deia/hive/coordination/2026-03-17-BRIEFING-BL207-REQUEUE-runtime-verify.md` and thought it was done. NO SOURCE CODE WAS MODIFIED.

**Re-queue 2 (THIS TASK):** We are being EXPLICIT. The bee MUST modify `eggToShell.ts` line 33. This is not a verification task. This is a SOURCE CODE FIX.

---

**Model:** sonnet
**Role:** bee
**Inject boot:** yes
