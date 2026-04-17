# TASK-BUG030B: Fix chatHistoryAdapter tests to match API contract -- FAILED

**Status:** FAILED (infrastructure issue)
**Model:** Sonnet
**Date:** 2026-03-18

## Files Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\chatHistoryAdapter.test.ts` — modified multiple times, attempting different mock approaches

## What Was Done
- Analyzed the failing chatHistoryAdapter.test.ts (7 failures, 2 passing)
- Identified root cause: Vitest module mocks (`vi.mock()`) are NOT being applied to chatApi and volumeStatus imports
- Attempted 6 different mocking approaches:
  1. vi.hoisted() with mocked functions
  2. Removing unused imports that might trigger real module loading
  3. Enhanced localStorage clearing in beforeEach()
  4. Arrow function factory pattern in vi.mock()
  5. Clean cache + isolated test execution
  6. Manual localStorage key removal by prefix
- All attempts failed — the real `listConversations()` and `getVolumeStatus()` functions are being called instead of mocks
- Confirmed localStorage data persists across test runs (`conv-1773884255499-9pb83y`, `conv-1773502144864-yxfkmh`, etc.)
- Discovered this test file is UNTRACKED in git (created by previous bee BUG-030, never committed)
- Discovered parallel test file `src/primitives/tree-browser/__tests__/chatHistoryAdapter.test.ts` also fails all 9 tests with same mocking issue

## Test Results
**File:** `src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts`
- **7 failed** (returns empty array, groups by date, sorts, badge, truncates, error handling, metadata)
- **2 passed** (uses ID for null title, handles zero messages)
- **Failure pattern:** All tests expecting empty/mocked data receive real localStorage conversations instead

**Root cause:** Vitest `vi.mock()` does not intercept module imports in chatHistoryAdapter.ts. The adapter imports the REAL chatApi and volumeStatus modules at evaluation time, before mocks are applied.

**Evidence:**
```
Error: /node/discover returned 401
  at getNodeList (volumeStatus.ts:51:11)
```
Real volumeStatus function called, attempting HTTP fetch to hivenode.

```
expected [ { id: 'group-Today', …(2) }, …(2) ] to deeply equal []
```
Real listConversations returned localStorage data (3 groups: Today, This Week, Older), not mocked empty array.

## Build Verification
- Test run: `npx vitest run src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts`
- Result: 7 failed, 2 passed (9 total)
- Duration: ~10s per run
- No compilation errors
- Mocks confirmed non-functional via error stack traces showing real function calls

## Acceptance Criteria
- [ ] Chat tree-browser shows conversation entries when they exist — **BLOCKED**
- [ ] Date headers group conversations correctly — **BLOCKED**
- [ ] Empty state shows placeholder text — **BLOCKED**
- [ ] Tests pass — **FAILED (7/9 failing)**
- [ ] No regressions in tree-browser tests — **NOT TESTED (blocked by mock failure)**

## Clock / Cost / Carbon
- **Clock:** 1.5 hours
- **Cost:** $1.20 (estimated, 79K tokens @ Sonnet rates)
- **Carbon:** 16g CO2e (estimated)

## Issues / Follow-ups

### Critical Blocker: Vitest Module Mocking Non-Functional
**Symptom:** `vi.mock()` does not prevent real module imports in chatHistoryAdapter.ts
**Impact:** Cannot test adapter in isolation — all tests call real chatApi → localStorage → real conversations
**Tried:**
- vi.hoisted() pattern (recommended Vitest approach)
- Factory functions in vi.mock()
- Removing imports that might trigger module loading
- Clean cache + isolated execution
- Manual localStorage clearing

**None worked.**

### Possible Root Causes
1. **Vitest version/config issue:** vitest.config.ts may be missing required settings for ESM module mocking
2. **Import timing:** chatHistoryAdapter.ts imports chatApi at top level, BEFORE test setup runs
3. **localStorage persistence:** jsdom localStorage persists across test runs in same process
4. **Module caching:** node_modules/.vite cache may be serving stale modules

### Recommended Fix Approaches (for Q33N or next bee)

**Option A: Refactor adapter for dependency injection**
```typescript
// chatHistoryAdapter.ts
export async function loadChatHistory(
  deps = { listConversations, getVolumeStatus }
): Promise<TreeNodeData[]> {
  const conversations = await deps.listConversations();
  // ...
}
```
Then tests can pass mock dependencies directly without relying on vi.mock().

**Option B: Mock at fetch/localStorage level**
Instead of mocking chatApi functions, mock the underlying APIs:
```typescript
vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 404 }));
vi.stubGlobal('localStorage', { /* mock implementation */ });
```
This ensures chatApi uses mocked storage, but requires mocking localStorage API surface.

**Option C: Fix Vitest config**
Check platform repo for working Vitest config with ESM mocking. May need:
```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    clearMocks: true,
    mockReset: true,
    restoreMocks: true,
  }
})
```

**Option D: Delete this test file, write integration tests instead**
If unit tests with mocks are fundamentally broken, write integration tests that:
- Use real localStorage with controlled data
- Clear storage before each test
- Accept that adapter tests are integration, not unit

### Other Findings
- The previous bee (BUG-030) added AUTO_EXPAND_ADAPTERS to treeBrowserAdapter.tsx (correct fix)
- The test file was created but never added to git (untracked)
- There's a duplicate test file at `src/primitives/tree-browser/__tests__/chatHistoryAdapter.test.ts` (also failing all 9 tests)
- chatHistoryAdapter.ts source code appears correct (no changes needed)

### Next Steps
1. **Escalate to Q33N:** This is a test infrastructure issue, not a test expectation issue
2. **Choose fix approach:** A, B, C, or D above
3. **If Option A:** Refactor adapter + tests together (larger task, but cleanest)
4. **If Option B:** Mock fetch + localStorage globally in test setup
5. **If Option C:** Review platform repo vitest.config, apply fixes
6. **If Option D:** Delete unit test, write integration test with real storage

### Files to Review
- `browser/vitest.config.ts` — may need clearMocks/mockReset settings
- `browser/src/infrastructure/relay_bus/__tests__/setup.ts` — global test setup
- `platform/simdecisions-2/vitest.config.ts` — reference config (if exists)
- `browser/src/primitives/tree-browser/__tests__/chatHistoryAdapter.test.ts` — duplicate test file, also failing

## Summary
Task FAILED due to Vitest module mocking infrastructure issue. The test expectations in the file are actually CORRECT (home://, both, offline, 🔴), but the mocks don't apply, so the adapter calls real chatApi functions that read localStorage. This is NOT a test expectation problem — it's a test framework problem. Fixing this requires either refactoring the adapter for DI, mocking at a lower level (fetch/localStorage), fixing Vitest config, or abandoning unit tests in favor of integration tests.

**Recommendation:** Escalate to Q33N for architectural decision on fix approach.
