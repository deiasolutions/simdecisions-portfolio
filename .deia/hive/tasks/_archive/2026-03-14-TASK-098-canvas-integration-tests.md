# TASK-098: Canvas Integration Tests

## Objective
Write integration tests that verify the full canvas pipeline: terminal input -> IR deposit -> canvas render -> node selection -> properties display.

## Context
All canvas components are built by TASK-092 through TASK-097. This task verifies they work together end-to-end using mocked bus events.

## Dependencies
- **All canvas tasks (092-097) must be complete**

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx` (from TASK-093)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\canvasAdapter.tsx` (from TASK-094)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\paletteAdapter.ts` (from TASK-095)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\propertiesAdapter.ts` (from TASK-096)

## Deliverables
- [ ] Create `browser/src/primitives/canvas/__tests__/canvas.integration.test.tsx` — 8+ tests:
  - **Pipeline test**: Emit `terminal:ir-deposit` with sample IRGraph -> canvas renders nodes
  - **Selection test**: Click canvas node -> `canvas:node-selected` fires -> properties adapter receives node
  - **Palette test**: Emit `palette:node-drag-start` -> verify canvas handles drag event
  - **Empty state test**: Canvas with no IR data shows empty placeholder
  - **Multiple deposits test**: Two consecutive `terminal:ir-deposit` events -> second replaces first
  - **Edge rendering test**: IRGraph with edges -> edges render between correct nodes
  - **EGG load test**: Import canvas.egg.md -> verify pane structure resolves correctly
  - **Adapter cleanup test**: Unmount canvas adapter -> verify bus listeners removed

## Constraints
- No file over 500 lines
- Use vitest + @testing-library/react
- Mock the bus (do NOT use real WebSocket or HTTP)
- Each test must be independent (no shared state)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260314-TASK-098-RESPONSE.md`

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

## Model Assignment
haiku
