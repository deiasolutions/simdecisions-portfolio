# TASK-150: Port Canvas Test Files from Platform

## Objective
Port 12 canvas test files from platform/simdecisions-2 (~1,859 lines) to shiftcenter. Update imports, skip tests for missing components, ensure all portable tests pass.

## Context

Platform repo (`C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\`) has 12 canvas-related test files that need to be ported to shiftcenter.

**Key structural differences:**
- Platform has `Canvas.tsx` — ShiftCenter has `FlowCanvas.tsx` (similar but different props/API)
- Platform has `BPMNNode.tsx` — ShiftCenter does NOT (skip BPMN tests)
- Platform has annotation nodes (AnnotationImageNode, AnnotationLineNode) — ShiftCenter does NOT (skip annotation tests)
- Both have animation modules (similar structure)
- Both have GroupNode (can port GroupNode tests)

**Test setup:**
- ShiftCenter uses: `browser/src/infrastructure/relay_bus/__tests__/setup.ts` (has p5 mock already)
- Platform uses: `src/test/setup.ts` (same p5 mock structure)

**Component mapping:**
```
Platform                          → ShiftCenter
─────────────────────────────────────────────────
Canvas                            → FlowCanvas (DIFFERENT API)
BPMNNode                          → (NONE — skip tests)
AnnotationImageNode               → (NONE — skip tests)
AnnotationLineNode                → (NONE — skip tests)
GroupNode                         → GroupNode (EXISTS)
animation/CheckpointFlash         → animation/CheckpointFlash (EXISTS)
animation/NodePulse               → animation/NodePulse (EXISTS)
animation/QueueBadge              → animation/QueueBadge (EXISTS)
animation/ResourceBar             → animation/ResourceBar (EXISTS)
animation/SimClock                → animation/SimClock (EXISTS)
animation/TokenAnimation          → animation/TokenAnimation (EXISTS)
```

## Files to Read First

### ShiftCenter (target structure)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowCanvas.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\GroupNode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\index.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\FlowToolbar.test.tsx` (reference for test structure)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\__tests__\setup.ts`

### Platform (source files)
All in: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\`

1. `__tests__/BPMNNode.test.tsx` (234 lines) — **SKIP: no BPMN in shiftcenter**
2. `__tests__/Canvas.drop.test.tsx` (226 lines) — **ADAPT: FlowCanvas has different drop API**
3. `__tests__/Canvas.lasso.test.tsx` (126 lines) — **ADAPT: check if lasso exists**
4. `__tests__/Canvas.minimap.test.tsx` (79 lines) — **ADAPT: check if minimap exists**
5. `__tests__/Canvas.pan.test.tsx` (111 lines) — **ADAPT: check if pan exists**
6. `__tests__/canvas.test.tsx` (293 lines) — **ADAPT: FlowCanvas core tests**
7. `Canvas.broadcast.test.tsx` (213 lines) — **ADAPT: check if broadcast exists**
8. `animation/__tests__/animation.test.tsx` (227 lines) — **PORT: animation module exists**
9. `nodes/__tests__/nodes.test.tsx` (84 lines) — **SKIP: tests BPMN nodes**
10. `nodes/AnnotationImageNode.test.tsx` (122 lines) — **SKIP: no annotation nodes**
11. `nodes/AnnotationLineNode.test.tsx` (106 lines) — **SKIP: no annotation nodes**
12. `nodes/GroupNode.test.tsx` (38 lines) — **PORT: GroupNode exists**

## Deliverables

- [ ] Create 12 test files in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\`
- [ ] For each file:
  - [ ] Update all import paths to shiftcenter structure
  - [ ] Replace `Canvas` with `FlowCanvas` where applicable
  - [ ] Add skip comments for missing components (BPMN, annotations)
  - [ ] Adapt ReactFlow mocking to match shiftcenter usage
- [ ] GroupNode.test.tsx: Full port, all tests passing
- [ ] animation.test.tsx: Full port, all tests passing
- [ ] Canvas tests (drop, lasso, minimap, pan, core, broadcast): Skip tests for features not in FlowCanvas, mark clearly
- [ ] BPMNNode.test.tsx, nodes.test.tsx, AnnotationImageNode.test.tsx, AnnotationLineNode.test.tsx: All tests skipped with clear comments

## Test Requirements

**TDD constraint:** These ARE tests, so implement them fully. No stubs.

- [ ] Tests written for all 12 files
- [ ] Portable tests (GroupNode, animation) MUST pass
- [ ] Tests for missing components MUST be explicitly skipped with `it.skip()` and clear comments
- [ ] No new failures in existing flow-designer tests
- [ ] All test file names match platform source:
  ```
  BPMNNode.test.tsx
  Canvas.drop.test.tsx
  Canvas.lasso.test.tsx
  Canvas.minimap.test.tsx
  Canvas.pan.test.tsx
  canvas.test.tsx
  Canvas.broadcast.test.tsx
  animation.test.tsx
  nodes.test.tsx
  AnnotationImageNode.test.tsx
  AnnotationLineNode.test.tsx
  GroupNode.test.tsx
  ```

**Edge cases:**
- [ ] p5 mock: Verify existing setup.ts is sufficient (no additional mocking needed)
- [ ] ReactFlow instance mocking: FlowCanvas uses ReactFlowInstance differently than Canvas
- [ ] Missing components: Every skipped test must have a comment: `// SKIP: [Component] does not exist in shiftcenter`

## Constraints

- Max 500 lines per file (all source files < 300, so safe)
- No file modifications outside `browser/src/apps/sim/components/flow-designer/__tests__/`
- CSS: var(--sd-*) only (tests shouldn't have inline styles)
- No stubs — if a component is missing, skip the test with a clear comment
- Import paths must use shiftcenter structure:
  ```typescript
  // Platform (old):
  import { Canvas } from '../Canvas'
  import { BPMNNode } from '../nodes/BPMNNode'

  // ShiftCenter (new):
  import { FlowCanvas } from '../FlowCanvas'
  import { GroupNode } from '../nodes/GroupNode'
  import { CheckpointFlash } from '../animation/CheckpointFlash'
  ```

## Smoke Test

```bash
cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/
```

**Expected outcome:**
- GroupNode.test.tsx: All tests pass
- animation.test.tsx: All tests pass
- Canvas tests: Some tests pass, some explicitly skipped
- BPMN/annotation tests: All tests explicitly skipped

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-150-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths (all 12 test files)
3. **What Was Done** — bullet list of concrete changes:
   - Import path updates
   - Component mapping (Canvas → FlowCanvas)
   - Which tests were skipped and why
   - Which tests were fully ported
4. **Test Results** — test files run, pass/fail/skip counts:
   - Total tests: X
   - Passing: Y
   - Skipped: Z (with reason)
   - Failing: 0 (or list failures with explanation)
5. **Build Verification** — test/build output summary:
   - Vitest output showing all test results
   - No new failures in existing flow-designer tests
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any:
   - Clock: wall time (e.g., "24 minutes")
   - Cost: estimated USD (e.g., "$0.12")
   - Carbon: estimated CO2e (e.g., "2.3g CO2e")
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks:
   - List all skipped components
   - Recommendations for future porting (if BPMN/annotations are added later)

DO NOT skip any section.

## Notes

- This is a mechanical port with architectural adaptation
- If a component doesn't exist in shiftcenter, skip it — do NOT stub it
- The spec says "10 files" but there are 12 — port all 12
- Priority P0.45
- Model: haiku (efficient for porting tasks)
- Many tests will be skipped due to missing components — this is expected and correct
