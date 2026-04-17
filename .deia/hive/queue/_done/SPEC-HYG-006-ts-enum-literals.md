# SPEC-HYG-006-ts-enum-literals: Fix 638 TS2322 type mismatch errors in test files

## Priority
P1

## Depends On
SPEC-HYG-005

## Model Assignment
sonnet

## Objective

Fix 638 TS2322 type mismatch errors across browser test files. The root cause is stale enum string literals in test mocks and assertions that no longer match current type definitions (e.g., `"home"` should be `"home-only"`, old variant names that were renamed). Update all test mocks, factory functions, and assertions to use the current type values as defined in the production source files.

## Files to Read First

- .deia/reports/code-hygiene-2026-04-12.md
- .deia/reports/tsc.txt
- browser/tsconfig.json

## Acceptance Criteria

- [ ] `npx tsc --noEmit 2>&1 | grep -c "TS2322"` reports fewer than 50 errors (down from 638)
- [ ] All updated string literals match the current type/enum definitions in production source
- [ ] No production source files are modified — only test files and test utilities
- [ ] All existing tests still pass after changes
- [ ] No new TypeScript errors introduced

## Smoke Test

- [ ] Run `cd browser && npx tsc --noEmit 2>&1 | grep -c "TS2322"` and confirm count is below 50
- [ ] Run `cd browser && npx vitest run --reporter=verbose 2>&1 | tail -5` and confirm tests pass

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- All existing tests must still pass after changes
- Run `npx tsc --noEmit` to verify fixes
- Only modify test files (files matching `__tests__/**` or `*.test.*` or `*.spec.*`)
- Do not change production type definitions to match old test values — update tests to match production
- When uncertain about the correct current value, check the source type definition file
