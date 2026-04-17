# BRIEFING: Port Canvas Test Files

**From:** Q33NR (Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-15
**Spec:** 2026-03-15-1206-SPEC-w1-09-canvas-tests
**Priority:** P0.45
**Model Assignment:** haiku

---

## Objective

Port the remaining 12 canvas test files from platform/simdecisions-2 (~1,859 lines total) to shiftcenter. Update imports, fix mocks, ensure all tests pass.

---

## Context

The spec requests "10 test files (~2,348 lines)" but actual count is 12 files (~1,859 lines). Q88N likely estimated based on older data. Port all 12 files.

ShiftCenter already has 8 flow-designer tests. This ports the remaining canvas-specific tests:
- Canvas interaction tests (drop, lasso, pan, minimap, broadcast)
- Node rendering tests (BPMN, annotations, groups)
- Animation tests
- Core canvas tests

---

## Source Files (platform)

All files in: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\`

1. `__tests__/BPMNNode.test.tsx` (234 lines)
2. `__tests__/Canvas.drop.test.tsx` (226 lines)
3. `__tests__/Canvas.lasso.test.tsx` (126 lines)
4. `__tests__/Canvas.minimap.test.tsx` (79 lines)
5. `__tests__/Canvas.pan.test.tsx` (111 lines)
6. `__tests__/canvas.test.tsx` (293 lines)
7. `Canvas.broadcast.test.tsx` (213 lines)
8. `animation/__tests__/animation.test.tsx` (227 lines)
9. `nodes/__tests__/nodes.test.tsx` (84 lines)
10. `nodes/AnnotationImageNode.test.tsx` (122 lines)
11. `nodes/AnnotationLineNode.test.tsx` (106 lines)
12. `nodes/GroupNode.test.tsx` (38 lines)

---

## Target Directory

`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\`

All files go into the same `__tests__/` directory. No subdirectory nesting.

---

## Key Porting Changes Required

### 1. Import Path Updates
Platform uses:
```typescript
import { Canvas } from '../Canvas'
import { BPMNNode } from '../nodes/BPMNNode'
```

ShiftCenter uses:
```typescript
import { Canvas } from '../Canvas'  // same relative path, but verify component exists
import { BPMNNode } from '../tabletop/nodes/BPMNNode'  // check actual location
```

**Action:** Read the shiftcenter flow-designer directory structure first. Map every import to the correct path.

### 2. Mock Setup
Platform uses p5 mocking in setup.ts:
```typescript
vi.mock('p5')
```

ShiftCenter already has this in `browser/src/test/setup.ts`. Verify it's sufficient.

### 3. Component Structure Differences
Platform canvas components may differ from shiftcenter. If a component doesn't exist in shiftcenter, the test should be marked as SKIPPED with a comment explaining why.

**Do NOT stub components to make tests pass. If the component is missing, skip the test.**

### 4. Animation Tests
`animation.test.tsx` tests animation scheduling/rendering. Verify shiftcenter has the animation module before porting.

### 5. Node Tests
Node tests (BPMN, Annotation, Group) test individual node rendering. Verify these node types exist in shiftcenter.

---

## Test Requirements

- [ ] All 12 test files ported
- [ ] All imports updated to shiftcenter paths
- [ ] All tests pass OR are explicitly skipped with reason
- [ ] No new test failures in existing flow-designer tests
- [ ] No file over 500 lines (all source files under 300, so this is safe)

---

## Constraints

- Max 500 lines per file (all files under 300, so safe)
- TDD: these ARE tests, so implement them fully
- No stubs — if a component is missing, skip the test with a clear comment
- CSS: var(--sd-*) only (tests shouldn't have inline styles)
- Model: haiku (straightforward porting task)

---

## Smoke Test

```bash
cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/
```

All ported tests must pass or be explicitly skipped.

---

## Response Requirements

Bee must write response file to `.deia/hive/responses/20260315-TASK-<ID>-RESPONSE.md` with all 8 sections:
1. Header (status, model, date)
2. Files Modified (all 12 test files, full paths)
3. What Was Done (import changes, mocks, skipped tests)
4. Test Results (pass/fail/skip counts)
5. Build Verification (vitest output summary)
6. Acceptance Criteria (mark [x] or [ ])
7. Clock / Cost / Carbon (all three)
8. Issues / Follow-ups (any missing components, skipped tests)

---

## Q33N Actions

1. **Read the shiftcenter flow-designer structure** to map component locations
2. **Write a single task file** for haiku bee to port all 12 tests
3. **Include the response file requirement** in the task
4. **Return to Q33NR for review** before dispatching

---

## Notes

- This is a mechanical port. If something doesn't exist in shiftcenter, skip it.
- The spec says "10 files" but there are 12. Port all 12.
- Priority is P0.45, so this processes after P0.44 specs.
- Session budget tracking: haiku is cost-efficient for this task.
