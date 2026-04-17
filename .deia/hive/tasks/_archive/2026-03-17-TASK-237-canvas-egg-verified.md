# TASK-237: Canvas EGG Verified

## Objective

Verify the SimDecisions canvas EGG (`eggs/canvas.egg.md`) renders correctly as a 5-pane layout with all pane interactions working, and add integration tests to verify the EGG parses into correct shell state.

## Context

The canvas EGG is the flagship SimDecisions product. It must render with:
- Left column (18%): palette tree-browser with node types
- Center column: canvas (65%), chat text-pane (25%), IR terminal (10%)
- Right column (18%): properties tree-browser
- Seamless borders between center panes (chat and terminal)
- Working bus events between panes (palette selection → canvas, canvas selection → properties)

The EGG file already exists at `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md` with full layout definition. The palette and properties adapters exist at:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\paletteAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\propertiesAdapter.ts`

Canvas primitive exists at `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx` with 22 node types and bus integration.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md` — Canvas EGG layout definition
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggLoader.ts` — EGG loading logic
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts` — EGG to Shell state conversion
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\eggToShell.test.ts` — Existing EGG test pattern
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx` — Canvas primitive
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\paletteAdapter.ts` — Palette adapter
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\propertiesAdapter.ts` — Properties adapter
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalApp.tsx` — Terminal primitive

## Deliverables

- [ ] Add integration test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\__tests__\canvasEgg.test.ts`
- [ ] Test verifies canvas.egg.md parses into correct shell state with:
  - 3-level nested split structure (vertical 18% → vertical 82% → horizontal splits)
  - 5 panes total: palette tree-browser, canvas app, text-pane, terminal, properties tree-browser
  - Correct ratios preserved: 0.18, 0.82, 0.65, 0.75
  - Seamless border flag set on chat/terminal split
  - All pane configs present (adapter names, routeTarget, zoomEnable, gridSnap, links)
- [ ] Test verifies terminal has `routeTarget: "ir"` in config
- [ ] Test verifies canvas has `zoomEnable: true` and `gridSnap: true` in config
- [ ] Test verifies palette has `adapter: "palette"` in config
- [ ] Test verifies properties has `adapter: "properties"` in config
- [ ] Test verifies text-pane has `renderMode: "chat"` in config
- [ ] If any layout issues found (wrong proportions, missing panes, incorrect configs), fix them in canvas.egg.md
- [ ] Run all browser tests: `cd browser && npx vitest run` — all tests pass

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases covered:
  - EGG loads without errors
  - All 5 panes present in shell state
  - Ratios match EGG definition
  - Seamless flag preserved
  - Pane configs match EGG definition

## Constraints

- No file over 500 lines (modularize if needed)
- CSS: `var(--sd-*)` only (no hardcoded colors)
- No stubs — fully implement all test cases
- Rule 3: All CSS uses variables, no hardcoded colors
- Rule 5: TDD — write tests first, then fix any issues
- Rule 6: NO STUBS — fully implement all assertions

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-237-RESPONSE.md`

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
