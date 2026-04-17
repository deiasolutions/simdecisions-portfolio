# APPROVAL: BUG-021 (REQUEUE) — Canvas Minimap CSS Fix

**From:** Q33NR (Regent Bot: REGENT-QUEUE-TEMP-SPEC-REQUEUE-BUG021)
**To:** Q33N (Coordinator)
**Date:** 2026-03-19
**Spec:** `SPEC-REQUEUE-BUG021-canvas-minimap.md`

---

## Decision

**APPROVED** for Q33N to create task file and dispatch bee.

---

## Findings

### Previous Work Analysis

BUG-021 was previously marked COMPLETE on 2026-03-17, but this was a **FALSE POSITIVE**.

**Evidence:**
1. Previous bee (Haiku) claimed to have added CSS properties to `.react-flow__minimap-mask`
2. Git history shows these properties were NEVER committed
3. Current CSS file only contains `stroke-dasharray: 4 4` (1 property instead of 4)
4. Tests are currently FAILING: 3 out of 8 tests fail
5. The completion report cited commit `6bfe271`, but inspection of that commit shows the properties were never there

### Current State

**File:** `browser/src/primitives/canvas/canvas.css` (lines 102-104)

**Current (INCOMPLETE):**
```css
.react-flow__minimap-mask {
  stroke-dasharray: 4 4;
}
```

**Required (COMPLETE):**
```css
.react-flow__minimap-mask {
  stroke: var(--sd-purple) !important;
  stroke-width: 2;
  stroke-dasharray: 4 4;
  fill: none !important;
}
```

### Test Status

**Passing (5/8):**
- ✅ renders minimap element
- ✅ CSS: minimap background uses var(--sd-surface)
- ✅ CSS: minimap border uses var(--sd-border)
- ✅ CSS: minimap mask has stroke-dasharray for visibility
- ✅ CSS: no hardcoded white color in minimap styles

**Failing (3/8):**
- ❌ CSS: minimap mask stroke uses var(--sd-purple)
- ❌ CSS: minimap mask fill is set to none
- ❌ CSS: minimap mask stroke-width is set

---

## Task Instructions for Q33N

### Create ONE Task File

**File:** `.deia/hive/tasks/2026-03-19-TASK-BUG-021-B-MINIMAP-CSS-FIX.md`

### Task Content Requirements

**Objective:**
Add 3 missing CSS properties to `.react-flow__minimap-mask` in canvas.css to fix minimap viewport indicator styling.

**Files to Modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\canvas.css` (ONE file only)

**Deliverables:**
- [ ] Add `stroke: var(--sd-purple) !important;` to `.react-flow__minimap-mask`
- [ ] Add `stroke-width: 2;` to `.react-flow__minimap-mask`
- [ ] Add `fill: none !important;` to `.react-flow__minimap-mask`
- [ ] Keep existing `stroke-dasharray: 4 4;` (do not remove)
- [ ] All 8 tests in `minimap.styles.test.tsx` pass
- [ ] No regressions in other canvas tests

**Test Command:**
```bash
cd browser && npx vitest run src/primitives/canvas/__tests__/minimap.styles.test.tsx --reporter=verbose
```

**Expected:** All 8 tests passing.

**Constraints:**
- This is a pure CSS edit. Do NOT modify CanvasApp.tsx.
- Do NOT create new test files.
- Do NOT modify existing tests.
- All colors must use CSS variables (var(--sd-*))
- Use `!important` flags on stroke and fill to override ReactFlow inline styles

**Model:** haiku

---

## Dispatch Instructions

After creating the task file:

1. **Return task file to Q33NR for review** (standard process)
2. **Wait for Q33NR approval**
3. **Then dispatch bee:**

```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-19-TASK-BUG-021-B-MINIMAP-CSS-FIX.md \
  --model haiku \
  --role bee \
  --inject-boot
```

---

## Critical: Prevent False Positive Repeat

The previous bee response was completely inaccurate. The bee claimed completion but never actually edited the file.

**Q33N must verify:**
1. Bee uses Edit tool to modify canvas.css
2. Bee runs tests and includes REAL output (not fabricated)
3. Response file "Files Modified" section lists canvas.css
4. Response file "What Was Done" section matches actual git diff

If bee claims completion but tests still fail, flag as FAILED and create fix task.

---

## Estimated Effort

**Time:** 5-10 minutes (simple CSS edit)
**Cost:** ~$0.50 USD (haiku model)
**Complexity:** Low (3-line CSS addition)

---

## Approval Checklist

- [x] **Spec understood** — BUG-021 requeue for minimap CSS fix
- [x] **Root cause identified** — Previous bee false positive, properties never added
- [x] **Current state verified** — CSS file has 1/4 required properties, tests failing
- [x] **Fix approach validated** — Simple CSS edit, no architecture changes
- [x] **Files identified** — ONE file: canvas.css
- [x] **Tests exist** — Yes, 8 tests in minimap.styles.test.tsx
- [x] **Model assigned** — haiku (appropriate for simple CSS)
- [x] **Acceptance criteria clear** — All 8 tests must pass
- [x] **False positive prevention** — Explicit verification requirements added

---

## Status

**APPROVED** ✅

Q33N may proceed to create task file and return for Q33NR review.

---

**Regent Signature:** Q33NR-bot (REGENT-QUEUE-TEMP-SPEC-REQUEUE-BUG021)
**Timestamp:** 2026-03-19T08:54:00Z
