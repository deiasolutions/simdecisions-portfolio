# SPEC-HYG-007-ts-prop-renames: Fix 273 TS2339 property-does-not-exist errors in tests

## Priority
P1

## Depends On
SPEC-HYG-005

## Model Assignment
sonnet

## Objective

Fix 273 TS2339 "Property does not exist" errors in browser test files. The root cause is deprecated or renamed property names in test mocks that no longer match the current interfaces (e.g., `_paneId` was renamed to `paneId`, `conversation_id` was renamed to `conversationId`, snake_case properties migrated to camelCase). Update all test mocks, assertions, and helper functions to use the current property names as defined in the production type interfaces.

## Files to Read First

- .deia/reports/code-hygiene-2026-04-12.md
- .deia/reports/tsc.txt

## Acceptance Criteria

- [ ] `npx tsc --noEmit 2>&1 | grep -c "TS2339"` reports fewer than 30 errors (down from 273)
- [ ] All updated property names match the current interface definitions in production source
- [ ] No production source files are modified — only test files and test utilities
- [ ] All existing tests still pass after changes
- [ ] No new TypeScript errors introduced

## Smoke Test

- [ ] Run `cd browser && npx tsc --noEmit 2>&1 | grep -c "TS2339"` and confirm count is below 30
- [ ] Run `cd browser && npx vitest run --reporter=verbose 2>&1 | tail -5` and confirm tests pass

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- All existing tests must still pass after changes
- Run `npx tsc --noEmit` to verify fixes
- Only modify test files (files matching `__tests__/**` or `*.test.*` or `*.spec.*`)
- Do not rename production properties to match old test values — update tests to match production
- When uncertain about the correct current property name, check the source interface definition
