# TASK-BUG-VERIFY-WAVE-0: Verify Canvas Port Fixes (BUG-018, BUG-019 ONLY)

## Objective

**IMPORTANT:** BUG-028 is handled by separate task (TASK-BUG-028-CHANNELS-CLICK). Focus ONLY on BUG-018 and BUG-019.

Verify whether BUG-018 and BUG-019 were fixed by the Canvas Full Port (commit 0336f49). For each bug, investigate the implementation, write verification tests if missing, and determine status: FIXED (close it) or OPEN (write fix spec for Wave 1).

## Context — WORK ALREADY DONE

✅ **Partial work exists:**
- BUG-018 regression test partially created at `browser/src/apps/sim/components/flow-designer/__tests__/BUG-018-regression.test.tsx`
- BUG-019 spec written to `.deia/hive/queue/_needs_review/SPEC-BUG-019.md`

**Canvas Full Port (commit 0336f49) included:**

1. **BUG-018:** Canvas IR generation shows error, response appears in Code egg instead
   - **Port work:** TASK-CANVAS-001 added IR pipeline (`irConverter.ts`), bus subscription for `terminal:ir-deposit`, and 16 integration tests
   - **Check:** Is the terminal → IR → canvas wiring complete? Does canvas receive and render IR deposits?

2. **BUG-019:** Canvas component drag captured by Stage instead of dropping on canvas
   - **Port work:** TASK-CANVAS-009A/009B added lasso overlay, smart edge handles, drag isolation tests
   - **Check:** Can components be dragged from palette to canvas? Is drag event propagation stopped correctly?

## Files to Read First

### BUG-018 (IR wiring)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\irConverter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx` (line 520-577, bus subscription)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\ir-deposit.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260323-TASK-CANVAS-001-RESPONSE.md`

### BUG-019 (drag isolation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\paletteAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\canvasDragIsolation.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\LassoOverlay.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260323-TASK-CANVAS-009A-RESPONSE.md`


## Deliverables

For each bug, produce:

- [ ] Investigation report (200-300 words per bug):
  - What was implemented by the Canvas port?
  - What tests currently exist?
  - Does the implementation cover the bug's root cause?
  - Status: FIXED or OPEN

- [ ] Verification test (if status = FIXED and no test exists):
  - Write a focused regression test that would have caught the bug originally
  - Test must pass after implementation
  - Test file naming: `browser/src/primitives/<component>/__tests__/<bug-id>-regression.test.tsx`
  - Minimum 3 test cases per bug

- [ ] Fix spec (if status = OPEN):
  - Write spec file to `.deia/hive/queue/_needs_review/SPEC-<BUG-ID>.md`
  - Spec must include: root cause, acceptance criteria, test requirements, file paths

- [ ] Inventory update:
  - If FIXED: `python _tools/inventory.py bug update --id <BUG-ID> --status FIXED`
  - If OPEN: leave status unchanged, spec will be reviewed by Q33NR

## Test Requirements

- [ ] Tests written FIRST (TDD) for any new verification tests
- [ ] All new tests pass
- [ ] No existing tests broken by investigation
- [ ] Edge cases covered:
  - **BUG-018:** Empty IR, malformed IR, IR with missing node types, broadcast vs targeted deposits
  - **BUG-019:** Drag from palette to empty canvas, drag over existing nodes, drag with Stage zoom/pan

## Constraints

- No file over 500 lines
- CSS: `var(--sd-*)` only — no hardcoded colors
- No stubs — fully implement all functions
- Do NOT refactor existing code — investigation only
- Do NOT fix bugs directly — write specs if bugs are OPEN

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260324-TASK-BUG-VERIFY-WAVE-0-RESPONSE.md`

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

## Bug Details (from inventory)

### BUG-018
- **ID:** BUG-018
- **Severity:** P0
- **Component:** canvas
- **Title:** Canvas IR generation shows error, response appears in Code egg instead
- **Status:** OPEN

### BUG-019
- **ID:** BUG-019
- **Severity:** P0
- **Component:** canvas
- **Title:** Canvas component drag captured by Stage instead of dropping on canvas
- **Status:** OPEN

### BUG-028
- **ID:** BUG-028
- **Severity:** P0
- **Component:** efemera
- **Title:** Efemera channels not wired: clicking channels does nothing
- **Status:** OPEN
