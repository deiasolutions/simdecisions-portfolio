# TASK-092: Port PHASE-IR TypeScript Types

## Objective
Port the PHASE-IR v1.0 type definitions from the old repo (`platform/simdecisions-2/src/types/ir.ts`) into ShiftCenter's browser as TypeScript types.

## Context
The Python PHASE-IR primitives were ported in TASK-071 to `engine/phase_ir/primitives.py`. The browser side needs equivalent TypeScript types for the canvas primitive to render and manipulate IR graphs.

The old repo has `src/types/ir.ts` (~500 lines) with: NodeType enum, IRNode, IREdge, IRGraph, OperatorConfig, TimingConfig, GuardConfig, Action, etc.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\primitives.py` (Python version — use as reference)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\irRouting.ts` (existing basic IR routing)

## Deliverables
- [ ] Create `browser/src/types/ir.ts` with full PHASE-IR v1.0 TypeScript types
- [ ] Types must include at minimum:
  - `NodeType` enum (start, end, task, decision, checkpoint, parallel_split, parallel_join, queue, group)
  - `IRNode` interface (id, type, label, position, data, timing?, operator?, guard?)
  - `IREdge` interface (id, source, target, label?, guard?, probability?)
  - `IRGraph` interface (nodes, edges, metadata?)
  - `TimingConfig` interface (distribution, params)
  - `OperatorConfig` interface (type, count, skills?)
  - `GuardConfig` interface (expression, type)
  - `Action` interface (type, target, payload)
- [ ] Types must align with Python `engine/phase_ir/primitives.py`
- [ ] Export all types from the file
- [ ] Create `browser/src/types/__tests__/ir.test.ts` with 15+ tests:
  - Type guard functions for each node type
  - IRGraph validation (nodes array, edges array)
  - Edge source/target reference validation
  - Serialization roundtrip (JSON parse/stringify preserves types)

## Constraints
- No file over 500 lines
- Do NOT modify `irRouting.ts` — that file handles terminal envelope routing, separate concern
- Types should be pure (no React, no DOM, no side effects)
- CSS: N/A (types only)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260314-TASK-092-RESPONSE.md`

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
