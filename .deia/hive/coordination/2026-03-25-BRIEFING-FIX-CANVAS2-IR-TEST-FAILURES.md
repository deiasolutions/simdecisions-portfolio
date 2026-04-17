# BRIEFING: Fix Canvas2 IR Test Failures (Fix Cycle 1)

**Date:** 2026-03-25
**Priority:** P0 (Fix Cycle)
**Model:** sonnet
**Parent Spec:** SPEC-BUG-canvas2-ir-not-reaching-canvas

## Context

The previous queen (watchdog timeout) completed most of the canvas2 IR pipeline work:

1. ✅ Root cause identified: EGG prompts told LLM to return bare JSON instead of envelope format `{to_user: "...", to_ir: [...]}`
2. ✅ Fix applied: Updated `eggs/canvas2.egg.md` and `eggs/canvas.egg.md` prompt blocks to instruct envelope format
3. ✅ Regression test created: `browser/src/apps/sim/components/flow-designer/__tests__/FlowDesigner.envelope-ir-deposit.test.tsx`
4. ✅ Existing tests pass: `terminalResponseRouter.test.ts` passes (exit code 0)
5. ❌ **NEW test FAILS**: FlowDesigner.envelope-ir-deposit.test.tsx has 7 test failures

## Your Job

Fix the FlowDesigner.envelope-ir-deposit.test.tsx so all tests pass. Do NOT change the EGG files unless absolutely necessary — the fix should be in the test file or the FlowDesigner component itself.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\FlowDesigner.envelope-ir-deposit.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\terminalResponseRouter.ts`
- Test output from previous run (in `.deia/hive/responses/` directory)

## Expected Test Command

```bash
cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/FlowDesigner.envelope-ir-deposit.test.tsx
```

## Deliverables

- [ ] All 7 tests in FlowDesigner.envelope-ir-deposit.test.tsx pass
- [ ] No regressions on other FlowDesigner tests
- [ ] terminalResponseRouter.test.ts still passes
- [ ] canvas-ir-deposit.test.tsx still passes

## Acceptance Criteria

- [ ] FlowDesigner.envelope-ir-deposit.test.tsx: 7/7 tests pass
- [ ] No changes to EGG files (unless root cause requires it)
- [ ] No regressions on existing tests
- [ ] Response file documents what was wrong and how it was fixed

## Constraints

- No file over 500 lines
- CSS: `var(--sd-*)` only
- No stubs
- TDD approach: understand failures, fix them, verify all pass

## Model Assignment

sonnet

## Budget Note

This is Fix Cycle 1 of 2 allowed. If this fix cycle fails, we get one more attempt before flagging NEEDS_DAVE.
