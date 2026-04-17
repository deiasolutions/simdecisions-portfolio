# TASK-237: canvas.egg.md Verified (W4 — 4.9)

## Objective
Verify the SimDecisions canvas EGG renders correctly as a 5-pane layout: palette (left), canvas (center-top), chat (center-middle), IR terminal (center-bottom), properties (right).

## Context
Wave 4 Product Polish. The canvas EGG is the SimDecisions product — the flagship app. It must render correctly with all panes visible, proper proportions, and seamless borders where configured.

## Source Spec
`docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.9

## Files to Read First
- `eggs/canvas.egg.md` — Canvas EGG layout definition (290 lines)
- `browser/src/shell/eggLoader.ts` — EGG parsing and loading
- `browser/src/primitives/canvas/` — Canvas primitive
- `browser/src/primitives/tree-browser/` — Tree browser (palette + properties)

## Deliverables
- [ ] Load `?egg=canvas` in browser and verify:
  - Left column (18%): palette tree-browser with node types
  - Center column: canvas (65%), chat text-pane (25%), IR terminal (10%)
  - Right column (18%): properties tree-browser
  - Seamless borders between center panes
- [ ] Verify canvas renders with grid snap and zoom controls
- [ ] Verify terminal has `routeTarget: "ir"` working
- [ ] Verify bus events flow between panes (palette selection → canvas, canvas selection → properties)
- [ ] Fix any layout issues (wrong proportions, missing panes, broken seamless edges)
- [ ] Add at least 1 integration test verifying the EGG parses into correct shell state
- [ ] Run: `cd browser && npx vitest run`

## Priority
P1

## Model
haiku
