# WAVE0-08: Fix CloudAPIClient Mock Failures — Task File Ready for Review

**Status:** TASK FILE COMPLETE — AWAITING Q33NR APPROVAL
**Coordinator:** Q33N
**Date:** 2026-03-15

---

## Summary

I have written **1 task file** for WAVE0-08 (Fix CloudAPIClient Mock Failures).

**Task file created:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-15-TASK-139-fix-cloudapi-mock.md`

---

## Root Cause Analysis

After reading the test file and the actual CloudAPIClient class, I identified the issue:

**The mock is correct, but the call pattern exposes a quirk:**

The mock setup (lines 37-57) creates:
```typescript
CloudAPIClient: vi.fn().mockImplementation(() => ({
  saveFlow: vi.fn().mockResolvedValue({ id: "rec-1", flow_id: "flow-1" }),
  listFlows: vi.fn().mockResolvedValue([]),
  ping: vi.fn().mockResolvedValue(true),
  validateFlow: vi.fn().mockResolvedValue({ valid: true, issues: [] }),
}))
```

This creates an **outer mock function** (`vi.fn()`) that, when called, returns the **inner object** with mock methods.

The tests call it like this:
```typescript
const client = (CloudAPIClient as unknown as () => Record<string, unknown>)();
```

**The problem:** When vitest hoists the mock, the outer `vi.fn()` may not be properly initialized, causing it to return `undefined` instead of calling the `mockImplementation`.

**The fix:** Ensure the mock returns the implementation object directly when called, or use a pattern that vitest handles more reliably.

---

## Task File: TASK-139

**Objective:** Fix 4 failing tests where CloudAPIClient mock methods return undefined.

**Assigned model:** haiku (simple mock fix, well-scoped)

**Key deliverables:**
- Update CloudAPIClient mock to ensure methods are defined when called
- All 4 failing tests pass
- No new regressions

**Files modified (by bee):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\FileOperations.test.tsx` (mock setup only, lines 37-57)

**Test command:**
```bash
cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/FileOperations.test.tsx
```

**Constraints:**
- Only modify mock setup — do NOT modify test assertions
- No stubs — mock methods must return real test data
- Max 500 lines per file (current file is ~650 lines, no new content added)

---

## Recommended Fix Pattern (for bee)

The task file does not prescribe the exact fix, but suggests the bee ensure the mock returns methods when called. Two viable approaches:

**Option A: Add default return value to outer vi.fn()**
```typescript
vi.mock("../../../adapters/api-client", () => {
  const mockInstance = {
    saveFlow: vi.fn().mockResolvedValue({ id: "rec-1", flow_id: "flow-1" }),
    listFlows: vi.fn().mockResolvedValue([]),
    ping: vi.fn().mockResolvedValue(true),
    validateFlow: vi.fn().mockResolvedValue({ valid: true, issues: [] }),
    // ... other methods
  };
  return {
    CloudAPIClient: vi.fn(() => mockInstance),
    APIError: class APIError extends Error { /* ... */ }
  };
});
```

**Option B: Use mockReturnValue**
```typescript
const mockImplementation = () => ({
  saveFlow: vi.fn().mockResolvedValue({ id: "rec-1", flow_id: "flow-1" }),
  // ... other methods
});

vi.mock("../../../adapters/api-client", () => ({
  CloudAPIClient: vi.fn().mockReturnValue(mockImplementation()),
  APIError: class APIError extends Error { /* ... */ }
}));
```

I have intentionally NOT prescribed the exact fix in the task file — the bee should diagnose and fix based on vitest behavior. Both options are valid.

---

## Next Steps

**Q33NR:** Please review the task file at:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-15-TASK-139-fix-cloudapi-mock.md`

If approved, I will dispatch the bee (haiku model) to execute the fix.

**Approval required before dispatch.**

---

## Notes

- This is a test-only fix — no changes to production code (api-client.ts)
- The actual CloudAPIClient is a proper class with a constructor — the mock just needs to return mock methods consistently
- The test assertions are correct — they just need the mock to work properly
- No new tests needed — we're fixing existing tests

---

**Q33N standing by for Q33NR approval.**
