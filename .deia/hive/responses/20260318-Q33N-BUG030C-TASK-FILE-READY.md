# Q33N Report: BUG-030-C Task File Ready for Review

**From:** Q33N (Coordinator)
**To:** Q33NR (Regent)
**Date:** 2026-03-18
**Re:** BUG-030 (Re-Queue 3) — Fix Chat History Adapter Test Mocks

---

## Summary

I have analyzed the briefing and created a task file for BUG-030-C. The task is ready for your review before dispatch.

**Task file location:**
```
C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-18-TASK-BUG030C-fix-chat-history-test-mocks.md
```

---

## Key Findings from Analysis

### Root Cause Confirmed

The test mocks are defined but NOT being applied. Evidence:

1. **401 errors in test output:**
   ```
   [volumeStatus] Failed to check volume status: Error: /node/discover returned 401
   ```
   This proves the **real** `getVolumeStatus()` is being called.

2. **Random conversation IDs:**
   Tests expect `conv-1773866695314-abc123` but get `conv-1773884945157-6xp0x0` (random).
   This proves the **real** `listConversations()` is being called, creating new random conversations instead of using mock data.

3. **Test results:** 7 failed / 2 passed (only 2 passing tests don't fully exercise the adapter)

### Why Current Mocks Don't Work

The test file uses this pattern:

```typescript
vi.mock('../../../../services/terminal/chatApi', async () => {
  return {
    listConversations: vi.fn(),
    // ...
  };
});

// Later in beforeEach:
mockListConversations.mockResolvedValue([]);
```

**Problem:** The `vi.fn()` in the factory creates mock functions at hoist time, but the `mockResolvedValue()` calls in `beforeEach` are trying to configure DIFFERENT instances. The mocks never intercept the real calls.

### Proven Solution

Use the **global fetch mock pattern** from `volumeStatus.test.ts`:

```typescript
const mockFetch = vi.fn();
global.fetch = mockFetch;
```

Both `chatApi.ts` and `volumeStatus.ts` use `fetch()` internally. Mocking fetch globally intercepts all HTTP calls and gives full control.

---

## Task File Overview

### Objective
Fix test mocks in `chatHistoryAdapter.test.ts` so all 8 tests pass. **DO NOT modify adapter source code** (it's correct).

### Approach
1. Remove current `vi.mock()` calls
2. Add global fetch mock (proven pattern)
3. Configure fetch responses in `beforeEach`
4. Import real functions (fetch intercepts them)

### Deliverables
- Remove broken vi.mock() calls
- Add global fetch mock
- Configure fetch for 3 endpoints: `/health`, `/node/discover`, `/storage/read`
- All 8 tests pass (0 failed)
- No changes to adapter source
- No 401 errors
- No random IDs

### Acceptance Criteria
- All tests pass: `cd browser && npx vitest run src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts`
- No 401 errors in output
- No random conversation IDs
- No changes to `chatHistoryAdapter.ts`
- No regressions in other tree-browser tests

---

## Files to Be Modified

**Only 1 file will be changed:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\chatHistoryAdapter.test.ts`

**No changes to:**
- `chatHistoryAdapter.ts` (adapter source — correct)
- Any other source files

---

## Test Status

### Current (Before Fix)
```
Test Files  1 failed (1)
Tests       7 failed | 2 passed (9)
```

### Target (After Fix)
```
Test Files  1 passed (1)
Tests       0 failed | 9 passed (9)
```

---

## Model Assignment

**Recommended:** sonnet

**Reasoning:**
- Requires understanding vitest mock patterns
- Needs to analyze why current mocks fail
- Must implement correct pattern from reference file
- Moderate complexity (test infrastructure, not business logic)

---

## Risk Assessment

**Risk Level:** Low

**Why:**
- Only test file changes (no source code)
- Proven solution pattern exists (volumeStatus.test.ts)
- Adapter source is confirmed correct
- Clear acceptance criteria (all tests pass)

**Potential Issues:**
- Fetch mock might need fine-tuning for chatApi's storage/read format
- May need to mock additional endpoints if chatApi makes other calls
- Backend detection caching might interfere (solution: call `resetBackendCache()` in beforeEach)

---

## Dependencies

**Blocked By:** None

**Blocks:** None (standalone test fix)

**Related Tasks:**
- BUG-030 (original issue — this is 3rd re-queue)
- Previous fix attempts failed due to:
  1. Modifying adapter source (wrong approach)
  2. _active/ path bug (now fixed)

---

## Ready for Dispatch?

**Status:** Ready for your review

**Next Steps:**
1. You (Q33NR) review the task file
2. If approved, I (Q33N) dispatch the bee
3. Bee fixes test mocks
4. I review response file
5. I report results to you

---

## Questions for Q33NR

None. The task file is complete and ready for review. The approach is proven (global fetch mock pattern from volumeStatus.test.ts), the scope is clear (test file only), and acceptance criteria are measurable (all tests pass).

---

**Q33NR: Please review the task file and approve dispatch.**
