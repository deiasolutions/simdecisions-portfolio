# WAVE0-08: Fix CloudAPIClient Mock Failures

## Priority
P0.025

## Model Assignment
haiku

## Objective
Fix 4 test failures in `browser/src/apps/sim/components/flow-designer/__tests__/FileOperations.test.tsx` where CloudAPIClient mock methods return undefined:
1. "mock saveFlow resolves with a flow record" - client.saveFlow is undefined
2. "mock listFlows resolves with empty array" - client.listFlows is undefined
3. "mock ping resolves to true" - client.ping is undefined
4. "mock validateFlow resolves with valid: true" - client.validateFlow is undefined

The test imports CloudAPIClient but the mock is returning undefined methods. The mock setup may be incorrect or the CloudAPIClient interface may have changed.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\FileOperations.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\adapters\api-client.ts` (or wherever CloudAPIClient is defined)

## Acceptance Criteria
- [ ] CloudAPIClient mock properly implements saveFlow, listFlows, ping, validateFlow methods
- [ ] All 4 failing tests pass
- [ ] Mock methods return the expected types (flow record, array, boolean, validation result)
- [ ] No new test failures introduced

## Constraints
- TDD: Tests must verify actual mock behavior
- No stubs in the mock — methods must return real test data
- Max 500 lines per file
- If CloudAPIClient interface changed, update mock to match current interface

## Smoke Test
- [ ] `cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/FileOperations.test.tsx` passes all API adapter tests
- [ ] No regressions in other flow-designer tests
