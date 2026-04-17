# TASK-139: Fix CloudAPIClient Mock Failures in FileOperations.test.tsx

## Objective
Fix 4 failing tests in FileOperations.test.tsx where CloudAPIClient mock methods (saveFlow, listFlows, ping, validateFlow) return undefined instead of their expected mock values.

## Context

The test file `browser/src/apps/sim/components/flow-designer/__tests__/FileOperations.test.tsx` mocks CloudAPIClient at lines 37-57:

```typescript
vi.mock("../../../adapters/api-client", () => ({
  CloudAPIClient: vi.fn().mockImplementation(() => ({
    saveFlow: vi.fn().mockResolvedValue({ id: "rec-1", flow_id: "flow-1" }),
    listFlows: vi.fn().mockResolvedValue([]),
    ping: vi.fn().mockResolvedValue(true),
    validateFlow: vi.fn().mockResolvedValue({ valid: true, issues: [] }),
    // ... other methods
  })),
  APIError: class APIError extends Error { /* ... */ }
}));
```

The mock creates `vi.fn().mockImplementation(...)`, which means:
- CloudAPIClient is a mock function (the outer `vi.fn()`)
- When called, it returns an object with mock methods
- But when called without being invoked, it returns `undefined`

The tests (lines 605, 611, 619, 626, 633) call it like this:

```typescript
const client = (CloudAPIClient as unknown as () => Record<string, unknown>)();
```

**Root cause:** The tests are calling the outer `vi.fn()`, which needs to be invoked to return the inner object. The current mock setup is correct, but the call pattern is fragile.

**Solution:** Update the mock to return the mock implementation directly when called, ensuring the mock methods are accessible.

The actual CloudAPIClient is a class (api-client.ts:278) with a constructor that takes `baseUrl: string = "/api/phase"`.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\FileOperations.test.tsx` (lines 30-57, 600-638)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\adapters\api-client.ts` (lines 278-350 — CloudAPIClient class)

## Deliverables

- [ ] Update CloudAPIClient mock in FileOperations.test.tsx to ensure methods are defined when the mock is called
- [ ] Verify mock returns expected values: `{ id: "rec-1", flow_id: "flow-1" }`, `[]`, `true`, `{ valid: true, issues: [] }`
- [ ] All 4 failing tests pass:
  - "mock saveFlow resolves with a flow record"
  - "mock listFlows resolves with empty array"
  - "mock ping resolves to true"
  - "mock validateFlow resolves with valid: true"
- [ ] No changes to test assertions — only fix the mock setup
- [ ] No new test failures introduced

## Test Requirements

- [ ] TDD: Fix the mock, then verify tests pass
- [ ] All 4 failing tests pass
- [ ] Run full FileOperations.test.tsx suite — verify no regressions
- [ ] Edge cases:
  - Mock can be instantiated multiple times (each call returns fresh mock)
  - Mock methods are spies (can use `.toHaveBeenCalled()` if needed in future tests)

## Constraints

- No file over 500 lines
- CSS: var(--sd-*) only (not applicable, no CSS in this task)
- No stubs — mock methods must return actual test data
- Only modify the mock setup (lines 37-57) — do NOT modify test assertions (lines 600-638)
- Do NOT modify api-client.ts — this is a test-only fix

## Acceptance Criteria

- [ ] CloudAPIClient mock properly implements saveFlow, listFlows, ping, validateFlow methods
- [ ] All 4 failing tests pass
- [ ] Mock methods return the expected types (flow record, array, boolean, validation result)
- [ ] No new test failures introduced

## Smoke Test

```bash
cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/FileOperations.test.tsx
```

Expected output:
- All tests in "API adapter mock" suite pass (4 tests)
- No regressions in other test suites in the file

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-139-RESPONSE.md`

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
