# BRIEFING: BUG-022-B Palette Click-to-Place Implementation

**Date:** 2026-03-18
**From:** Q33NR (Regent)
**To:** Q33N (Queen Coordinator)
**Spec:** `2026-03-18-SPEC-REQUEUE-BUG022B-canvas-click-to-place.md`

---

## Objective

Wire the palette adapter so clicking a component in the components panel places it on the canvas. Currently clicking does nothing. This is a re-queue because previous attempts only wrote tests without implementing the actual feature.

---

## Background

- **BUG-022-A (icons):** Fixed by BUG-035 (isTextIcon function). Icons now render correctly.
- **BUG-022-B (click-to-place):** Previous bee wrote tests only, no source code changes.
- **FIX-BUG022B:** Only fixed test infrastructure (_dispatch mock), not the actual feature.
- **This re-queue:** Get the actual source code written to make tests pass.

---

## What Needs to Happen

1. **paletteAdapter click handler** must emit a bus event (e.g., `canvas:place-component`)
2. **CanvasApp or canvas hook** must listen for placement event and add node to canvas
3. **Existing tests must pass** (10 tests in paletteClickToPlace.test.tsx)
4. **No regressions** in TreeNodeRow icon tests (15 tests)

---

## Files to Read

### Core Implementation Files
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\paletteAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\messageBus.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md`

### Test Files
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\paletteClickToPlace.test.tsx` (10 tests — make these pass)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\TreeNodeRow.icon.test.tsx` (15 tests — no regressions)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\TreeNodeRow.palette-icons.integration.test.tsx` (no regressions)

### Previous Attempts (for context)
- `.deia/hive/queue/_done/2026-03-17-SPEC-TASK-BUG022-canvas-components-panel-plain.md`
- `.deia/hive/queue/_done/2026-03-18-SPEC-TASK-FIX-BUG022B-palette-click-dispatch.md`
- `.deia/hive/responses/20260318-TASK-BUG022B-FIX-PALETTE-CLICK-TESTS-RESPONSE.md` (if exists)

---

## Deliverables

- [ ] **paletteAdapter.ts:** Add click handler that emits bus event `canvas:place-component` (or similar)
- [ ] **CanvasApp.tsx or canvas hook:** Add listener for placement event and implement node addition logic
- [ ] **All paletteClickToPlace tests pass** (10 tests)
- [ ] **No regressions:** TreeNodeRow icon tests still pass (15 tests)
- [ ] **No new test failures** in canvas/ or tree-browser/

---

## Acceptance Criteria (from spec)

- [ ] Click a palette item → component appears on canvas
- [ ] All paletteClickToPlace tests pass
- [ ] All TreeNodeRow icon/palette tests pass
- [ ] No new test failures in canvas/ or tree-browser/

---

## Smoke Test Commands

```bash
cd browser && npx vitest run src/primitives/canvas/__tests__/paletteClickToPlace.test.tsx
cd browser && npx vitest run src/primitives/tree-browser/__tests__/TreeNodeRow.icon.test.tsx
cd browser && npx vitest run src/primitives/tree-browser/__tests__/TreeNodeRow.palette-icons.integration.test.tsx
```

---

## Constraints

- **No file over 500 lines** (modularize at 500, hard limit 1,000)
- **CSS: var(--sd-*) only** (no hex, no rgb(), no named colors)
- **No stubs** (real implementation required)
- **Do NOT modify messageBus.ts core** (only add listeners/emitters in adapter and canvas code)
- **TDD:** Tests already exist — implement code to pass them

---

## Model Assignment

**Sonnet** (as specified in spec)

---

## Priority

**P0** (as specified in spec)

---

## Q33N Instructions

1. Read the test file first to understand what behavior is expected
2. Read paletteAdapter.ts to understand current structure
3. Read CanvasApp.tsx to understand how canvas manages nodes
4. Write task file(s) for bee(s) to implement the feature
5. Return task files to Q33NR for review BEFORE dispatching

---

## Notes

This is a **re-queue** because previous attempts failed to implement the actual feature. The tests exist. The infrastructure exists. The bee must write the IMPLEMENTATION CODE, not just tests.

Make it VERY clear in the task file that the bee must:
- Modify paletteAdapter.ts to emit bus event on click
- Modify CanvasApp.tsx (or canvas hook) to listen and add node
- NOT just write more tests

---

**END BRIEFING**
