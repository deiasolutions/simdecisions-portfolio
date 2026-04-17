# BRIEFING: BL-121 — Properties Panel Canvas Selection Wiring

**Date:** 2026-03-19
**From:** Q33NR (REGENT-QUEUE-TEMP-SPEC-REQUEUE-BL121-)
**To:** Q33N
**Model Assignment:** Sonnet

---

## Objective

Fix the broken wiring between canvas node selection and the properties panel. When a user selects a canvas node, the properties pane should display the node's properties. Currently this does not work.

---

## Context

### What Exists
- `browser/src/primitives/tree-browser/adapters/propertiesAdapter.ts` — properties adapter
- `browser/src/apps/sim/components/flow-designer/properties/PropertyPanel.tsx` — properties panel UI
- `eggs/canvas.egg.md` — EGG config with properties pane
- `browser/src/primitives/canvas/CanvasApp.tsx` — canvas app that handles selection

### What's Broken
The bus event flow from canvas selection → properties adapter → properties pane is incomplete or misconfigured.

### What Needs to Happen
1. When a canvas node is selected, CanvasApp.tsx must send a bus event (likely `node:selected`) with the node data
2. The properties adapter must listen for this event
3. The adapter must transform the node data into tree-browser items
4. The properties pane must display the transformed data
5. Deselecting must clear the properties pane

---

## Files to Read First

**Canvas:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md`

**Properties:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\propertiesAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\simPropertiesAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\properties\PropertyPanel.tsx`

**Bus:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\busTypes.ts`

---

## Deliverables

Your task is to write task files for bees to:

1. **Investigate the current state:**
   - What bus events does CanvasApp.tsx send on node selection?
   - What events does propertiesAdapter listen for?
   - What's the gap?

2. **Wire the selection event:**
   - CanvasApp.tsx sends `node:selected` (or equivalent) with node data
   - propertiesAdapter subscribes to the event
   - Adapter transforms node data into tree-browser items
   - Properties pane renders the items

3. **Handle deselection:**
   - Deselecting clears the properties pane

4. **Write tests:**
   - Tests for selection → properties flow
   - Tests for deselection → clear
   - Tests for multi-selection (if applicable)
   - No regressions in canvas or tree-browser tests

---

## Constraints

- **No file over 500 lines.** Modularize if needed.
- **CSS: var(--sd-*) only.** No hardcoded colors.
- **No stubs.** Every function fully implemented.
- **TDD.** Tests first, then implementation.
- **Absolute paths** in all task files.
- **All 8 sections** in bee response files.

---

## Acceptance Criteria

- [ ] Selecting a canvas node displays its properties in the properties pane
- [ ] Deselecting clears the properties pane
- [ ] Tests pass for selection → properties flow
- [ ] Tests pass for deselection → clear
- [ ] No regressions in canvas tests (`browser/src/primitives/canvas/`)
- [ ] No regressions in tree-browser tests (`browser/src/primitives/tree-browser/`)
- [ ] All browser tests pass (`cd browser && npx vitest run`)

---

## Smoke Test

```bash
cd browser && npx vitest run --reporter=verbose src/primitives/canvas/
cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/
cd browser && npx vitest run
```

---

## Notes

- The spec mentions `simPropertiesAdapter.ts` — check if this is the right adapter or if we need to wire propertiesAdapter instead
- Check if the canvas.egg.md properties pane config points to the right adapter
- Bus event naming must follow existing patterns (check busTypes.ts)
- Multi-selection may be out of scope — focus on single node selection first

---

## Q33N: Your Next Steps

1. Read the files listed above
2. Write task files (one per logical unit of work)
3. Break down into testable, bee-sized chunks
4. Return the task files to me for review
5. **DO NOT dispatch bees yet** — wait for my approval

---

**End of briefing.**
