# TASK-231: Seamless Pane Borders (W4 — 4.3)

## Objective
Verify seamless pane borders work correctly — adjacent panes with `seamlessEdges` in their EGG config should render without visible borders between them, creating a unified visual surface.

## Context
Wave 4 Product Polish (BL-002). PaneChrome.tsx already supports `node.meta.seamlessEdges` with per-edge boolean control (top/right/bottom/left). This removes border and border-radius on seamless edges. Need to verify it works end-to-end with real EGG layouts.

## Source Spec
`docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.3

## Files to Read First
- `browser/src/shell/components/PaneChrome.tsx` — Seamless edge logic (lines 73-88)
- `browser/src/shell/components/shell.css` — Shell layout styles
- `eggs/chat.egg.md` — Uses seamless split between chat output and terminal
- `eggs/canvas.egg.md` — Uses seamless borders between panes

## Deliverables
- [ ] Verify seamlessEdges config in EGG files produces borderless adjacent panes
- [ ] Verify non-seamless edges still show proper borders with focus color
- [ ] Verify border-radius is removed only on seamless edges (not all corners)
- [ ] Verify focused pane highlight (`--sd-border-focus`) still works on non-seamless edges
- [ ] Test with chat.egg.md: chat output and terminal should appear as one surface
- [ ] Fix any visual glitches (shadows leaking through seamless edges, gaps, etc.)
- [ ] Add test: seamless edges remove border/radius, non-seamless keep them
- [ ] Run: `cd browser && npx vitest run src/shell/`

## Priority
P1

## Model
haiku
