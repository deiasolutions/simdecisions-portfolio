# TASK-BUG-021-B: Canvas Minimap CSS Fix (REQUEUE)

## Objective
Add 3 missing CSS properties to `.react-flow__minimap-mask` in `canvas.css` to fix minimap visibility on dark themes.

## Context

**This is a REQUEUE.** The previous bee (2026-03-17) claimed to fix this bug but NEVER actually edited the file. The CSS properties were never added. This is a false positive that must be corrected.

**Current state:**
```css
.react-flow__minimap-mask {
  stroke-dasharray: 4 4;
}
```

**Required state:**
```css
.react-flow__minimap-mask {
  stroke: var(--sd-purple) !important;
  stroke-width: 2;
  stroke-dasharray: 4 4;
  fill: none !important;
}
```

**Why these properties:**
- `stroke: var(--sd-purple) !important` — Makes viewport indicator visible using theme-aware color. `!important` overrides ReactFlow inline styles.
- `stroke-width: 2` — Makes the outline visible and crisp.
- `stroke-dasharray: 4 4` — Already present. Dashed pattern for visual distinction.
- `fill: none !important` — Prevents white background fill on dark themes. `!important` overrides ReactFlow defaults.

**Test file already exists and is correct:** `browser/src/primitives/canvas/__tests__/minimap.styles.test.tsx`

Currently **3 tests are FAILING** because the CSS properties are missing:
- CSS: minimap mask stroke uses var(--sd-purple) ❌
- CSS: minimap mask fill is set to none ❌
- CSS: minimap mask stroke-width is set ❌

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\canvas.css` (lines 102-104)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\minimap.styles.test.tsx` (understand what tests expect)

## Deliverables
- [ ] Edit `canvas.css` to add `stroke`, `stroke-width`, and `fill` properties to `.react-flow__minimap-mask`
- [ ] All 8 tests in `minimap.styles.test.tsx` pass
- [ ] No regressions in other canvas tests

## Test Requirements
- [ ] Run: `cd browser && npx vitest run src/primitives/canvas/__tests__/minimap.styles.test.tsx --reporter=verbose`
- [ ] Expected: **8 tests passing** (currently 5 passing, 3 failing)
- [ ] No canvas test regressions: `cd browser && npx vitest run src/primitives/canvas/__tests__/ --reporter=verbose`

## Constraints
- **This is a pure CSS fix.** Do NOT modify `CanvasApp.tsx`. The MiniMap component is already correct.
- **Do NOT create new files.** Only edit `canvas.css`.
- **Do NOT modify test files.** They are already correct and failing for the right reason.
- **Use CSS variables only.** No hardcoded colors (already specified in required code).
- **Keep existing `stroke-dasharray: 4 4` property.** Only add the 3 missing properties.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260319-TASK-BUG-021-B-RESPONSE.md`

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

## Critical: Response File Accuracy

**The previous bee wrote a response file claiming completion but NEVER actually edited the file.**

You MUST:
1. **Actually edit the file** using the Edit tool
2. **Run the tests** and include REAL output
3. **Only claim COMPLETE** if tests actually pass

If tests fail, the response status must be FAILED with explanation.

---

**This is a 5-minute fix. Add 3 CSS properties to one CSS rule. Run tests. Verify. Report.**
