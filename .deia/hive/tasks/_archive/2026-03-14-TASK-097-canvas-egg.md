# TASK-097: Build Canvas EGG Definition

## Objective
Create the canvas.egg.md product definition file that wires up a 5-pane layout for the SimDecisions canvas experience.

## Context
EGG files define product configurations in ShiftCenter. See `eggs/efemera.egg.md` for the pattern. The canvas EGG creates a layout with: palette sidebar | canvas main + terminal below | properties sidebar.

## Dependencies
- **TASK-093** (canvas primitive), **TASK-094** (canvas adapter), **TASK-095** (palette adapter), **TASK-096** (properties adapter) should all be complete

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\efemera.egg.md` (pattern reference)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts` (EGG resolver logic)

## Deliverables
- [ ] Create `eggs/canvas.egg.md` with:
  - **Product name**: SimDecisions Canvas
  - **Layout**: 3-column split
    - Left (20%): tree-browser with palette adapter
    - Center: vertical split
      - Top (70%): canvas app
      - Bottom (30%): terminal (for LLM chat that generates IR)
    - Right (20%): tree-browser with properties adapter
  - **Pane configs**:
    - Palette pane: `app: tree-browser`, `adapter: palette`, `chrome: true`
    - Canvas pane: `app: canvas`, `chrome: true`
    - Terminal pane: `app: terminal`, `routeTarget: to_ir`, `chrome: true`
    - Properties pane: `app: tree-browser`, `adapter: properties`, `chrome: true`
  - **Links** (bus wiring):
    - terminal → canvas (via `terminal:ir-deposit`)
    - canvas → properties (via `canvas:node-selected`)
    - palette → canvas (via `palette:node-drag-start`)
  - **Prompt block**: System prompt teaching the LLM to generate PHASE-IR mutations
- [ ] No tests needed (pure YAML/markdown config)

## Constraints
- Follow the exact format of `efemera.egg.md`
- No file over 500 lines
- All pane app references must match registered app names

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260314-TASK-097-RESPONSE.md`

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
