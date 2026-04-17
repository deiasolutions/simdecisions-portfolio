# Briefing: TASK-237 — Canvas EGG Verified

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-17
**Priority:** P1
**Model Assignment:** Haiku

---

## Objective

Verify the SimDecisions canvas EGG (`eggs/canvas.egg.md`) renders correctly as a 5-pane layout and all pane interactions work. This is Wave 4 Product Polish — Task 4.9.

---

## Context from Q88N

The canvas EGG is the flagship SimDecisions product. It must render with:
- Left column (18%): palette tree-browser with node types
- Center column: canvas (65%), chat text-pane (25%), IR terminal (10%)
- Right column (18%): properties tree-browser
- Seamless borders between center panes
- Working bus events between panes (palette selection → canvas, canvas selection → properties)

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md` — Canvas EGG layout definition (~290 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggLoader.ts` — EGG parsing and loading logic
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\` — Canvas primitive implementation
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\` — Tree browser for palette/properties
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\` — Terminal primitive for IR terminal

---

## Deliverables Required

1. Load `?egg=canvas` in browser and verify:
   - Left column (18%): palette tree-browser with node types visible
   - Center column: canvas (65%), chat text-pane (25%), IR terminal (10%)
   - Right column (18%): properties tree-browser visible
   - Seamless borders between center panes where configured
2. Verify canvas renders with grid snap and zoom controls
3. Verify terminal has `routeTarget: "ir"` working
4. Verify bus events flow between panes:
   - Palette selection → canvas updates
   - Canvas selection → properties updates
5. Fix any layout issues (wrong proportions, missing panes, broken seamless edges)
6. Add at least 1 integration test verifying the EGG parses into correct shell state
7. Run: `cd browser && npx vitest run` — all tests pass

---

## Acceptance Criteria

- [ ] Canvas EGG loads at `?egg=canvas` without errors
- [ ] All 5 panes render with correct proportions
- [ ] Seamless borders work between center panes
- [ ] Canvas displays grid snap and zoom controls
- [ ] Terminal shows `routeTarget: "ir"` correctly
- [ ] Bus events work: palette → canvas, canvas → properties
- [ ] At least 1 integration test added
- [ ] All browser tests pass

---

## Constraints

- Rule 3: CSS uses `var(--sd-*)` only (no hardcoded colors)
- Rule 4: No file over 500 lines (modularize if needed)
- Rule 5: TDD — tests first, then implementation
- Rule 6: NO STUBS — fully implement or report blocker

---

## Test Requirements

- Write test FIRST for EGG parsing verification
- Test must verify shell state after loading canvas.egg.md
- Run all browser tests: `cd browser && npx vitest run`
- All tests must pass

---

## Model Assignment

**Haiku** — This is verification + light fixes. Suitable for Haiku.

---

## Next Steps

1. Read canvas.egg.md and understand layout
2. Read eggLoader.ts to understand parsing
3. Write task file for bee
4. Return task file to Q33NR for review
5. **DO NOT dispatch bee until Q33NR approves**
