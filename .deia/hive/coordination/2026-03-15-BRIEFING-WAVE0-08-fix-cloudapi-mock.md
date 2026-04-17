# BRIEFING: Fix CloudAPIClient Mock Failures (WAVE0-08)

**Date:** 2026-03-15
**From:** Q33NR (regent)
**To:** Q33N (coordinator)
**Priority:** P0.025
**Model Assignment:** haiku

---

## Objective

Fix 4 test failures in `browser/src/apps/sim/components/flow-designer/__tests__/FileOperations.test.tsx` where CloudAPIClient mock methods return undefined.

---

## Context

The spec is WAVE0-08 from the queue:

```
.deia/hive/queue/2026-03-15-WAVE0-08-SPEC-fix-cloudapi-mock.md
```

**Failures:**
1. "mock saveFlow resolves with a flow record" - client.saveFlow is undefined
2. "mock listFlows resolves with empty array" - client.listFlows is undefined
3. "mock ping resolves to true" - client.ping is undefined
4. "mock validateFlow resolves with valid: true" - client.validateFlow is undefined

**Root Cause Analysis:**

The test file mocks CloudAPIClient like this (lines 37-57):

```typescript
vi.mock("../../../adapters/api-client", () => ({
  CloudAPIClient: vi.fn().mockImplementation(() => ({
    saveFlow: vi.fn().mockResolvedValue({ id: "rec-1", flow_id: "flow-1" }),
    // ... other methods
  })),
  APIError: class APIError extends Error { /* ... */ }
}));
```

Then the tests instantiate it like this (lines 601-606):

```typescript
const { CloudAPIClient } = await import("../../../adapters/api-client");
const client = (CloudAPIClient as unknown as () => Record<string, unknown>)();
```

**The problem:** CloudAPIClient is a real **class** in api-client.ts (line 278), not a factory function. The mock returns a constructor function, but the tests call it without `new`.

The mock setup creates `vi.fn().mockImplementation(...)`, which means:
- `CloudAPIClient` is a mock function
- When called, it returns an object with mock methods
- But the tests are calling it as a plain function, not as a constructor

The cast `as unknown as () => Record<string, unknown>` bypasses TypeScript checks but doesn't fix the runtime issue.

**The fix:** Update the mock to return a constructor that can be called with `new`, OR update the test instantiation to call the mock function correctly.

---

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\FileOperations.test.tsx` (lines 30-57, 600-638)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\adapters\api-client.ts` (lines 278-478 — CloudAPIClient class definition)

---

## Acceptance Criteria

From the spec:

- [ ] CloudAPIClient mock properly implements saveFlow, listFlows, ping, validateFlow methods
- [ ] All 4 failing tests pass
- [ ] Mock methods return the expected types (flow record, array, boolean, validation result)
- [ ] No new test failures introduced

---

## Constraints

- **TDD:** Tests must verify actual mock behavior
- **No stubs:** Methods must return real test data
- **Max 500 lines per file**
- **If CloudAPIClient interface changed, update mock to match current interface**

---

## Smoke Test

From the spec:

```bash
cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/FileOperations.test.tsx
```

Must pass all API adapter tests, no regressions in other flow-designer tests.

---

## Recommended Approach

**Option A: Fix the mock to be a proper class constructor**

```typescript
vi.mock("../../../adapters/api-client", () => ({
  CloudAPIClient: vi.fn(function(this: any) {
    this.saveFlow = vi.fn().mockResolvedValue({ id: "rec-1", flow_id: "flow-1" });
    this.listFlows = vi.fn().mockResolvedValue([]);
    this.ping = vi.fn().mockResolvedValue(true);
    this.validateFlow = vi.fn().mockResolvedValue({ valid: true, issues: [] });
    // ... other methods
  }),
  APIError: class APIError extends Error { /* ... */ }
}));
```

Then update the tests to call with `new`:

```typescript
const client = new CloudAPIClient();
```

**Option B: Keep the factory pattern, call correctly**

Keep the mock as-is (returns a factory function), but call it correctly:

```typescript
const client = CloudAPIClient(); // call the mock function, which returns the object
```

**Recommendation:** Option A is cleaner and matches the actual class interface. Go with Option A.

---

## Task Files Required

One task file:

- **TASK-XXX:** Fix CloudAPIClient mock in FileOperations.test.tsx
  - Update mock setup to be a proper constructor
  - Update test instantiation to use `new CloudAPIClient()`
  - Verify all 4 failing tests pass
  - Verify no regressions

Model: haiku (simple fix, well-defined)

---

## Notes

- The actual CloudAPIClient class has more methods than the mock. Only mock the methods that the tests use.
- The mock should return methods as spies (`vi.fn()`) so tests can call `.toHaveBeenCalledWith()` if needed.
- The `APIError` class mock is already correct (lines 47-56).

---

**Q33N:** Please write the task file for this fix and return it for my review before dispatching.
