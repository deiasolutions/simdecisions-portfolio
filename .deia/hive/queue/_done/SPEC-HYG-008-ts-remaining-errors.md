# SPEC-HYG-008-ts-remaining-errors: Fix remaining TypeScript errors across browser tests

## Priority
P2

## Depends On
SPEC-HYG-005, SPEC-HYG-006, SPEC-HYG-007

## Model Assignment
sonnet

## Objective

Fix the remaining TypeScript errors in browser test and source files after HYG-005/006/007 are complete. This covers: TS2345 (108 argument type errors), TS2741 (82 missing required property errors), TS2353 (70 object literal errors), TS2739 (48 missing properties on type), TS2683 (48 unsafe 'this' context errors), TS2591 (32 module reference errors), and TS2740 (29 type missing properties). Address each category systematically by fixing test mocks, adding missing required properties, and correcting argument types.

## Files to Read First

- .deia/reports/tsc.txt
- .deia/reports/code-hygiene-2026-04-12.md

## Acceptance Criteria

- [ ] `npx tsc --noEmit 2>&1 | grep -c "TS2345"` reports fewer than 20 errors (down from 108)
- [ ] `npx tsc --noEmit 2>&1 | grep -c "TS2741"` reports fewer than 15 errors (down from 82)
- [ ] `npx tsc --noEmit 2>&1 | grep -c "TS2353"` reports fewer than 15 errors (down from 70)
- [ ] `npx tsc --noEmit 2>&1 | grep -c "TS2739"` reports fewer than 10 errors (down from 48)
- [ ] `npx tsc --noEmit 2>&1 | grep -c "TS2683"` reports fewer than 10 errors (down from 48)
- [ ] `npx tsc --noEmit 2>&1 | grep -c "TS2591"` reports zero errors (down from 32)
- [ ] `npx tsc --noEmit 2>&1 | grep -c "TS2740"` reports fewer than 10 errors (down from 29)
- [ ] All existing tests still pass after changes
- [ ] No new TypeScript errors introduced

## Smoke Test

- [ ] Run `cd browser && npx tsc --noEmit 2>&1 | grep -cE "TS(2345|2741|2353|2739|2683|2591|2740)"` and confirm total count is below 80
- [ ] Run `cd browser && npx vitest run --reporter=verbose 2>&1 | tail -5` and confirm tests pass

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- All existing tests must still pass after changes
- Run `npx tsc --noEmit` to verify fixes
- Prefer fixing test mocks to match production types over changing production types
- For TS2683 'this' context errors, use arrow functions or explicit this-parameter typing
- For TS2591 module errors, add proper import statements instead of global references
- Do not suppress errors with `@ts-ignore` or `as any` — fix the root cause
