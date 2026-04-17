# BUG-030 (RE-QUEUE 3): Chat tree-browser test failures — 30 tests failing

## Background — Why Re-Queued
Previous re-queue (attempt 2) was dispatched but all 4 fix cycles failed due to _active/ path reference bug (now fixed). Root issue: adapter source code is CORRECT, but test mocks are broken — real chatApi being called instead of mocked version.

## Objective
Fix the test mocks in `chatHistoryAdapter.test.ts` so all 30 failing tests pass. **DO NOT modify adapter source code** — it is correct.

## Problem Analysis
- Adapter source code is CORRECT (no changes needed)
- AUTO_EXPAND fix was CORRECT (groups auto-expand now)
- **Test mocks are BROKEN** — real chatApi being called instead of mocked version
- Real chatApi generates random IDs, causing test assertions to fail

### Test Failures
```bash
cd browser && npx vitest run src/primitives/tree-browser/
# Result: 30 failed | 163 passed (193 total)
```

Example failure:
```
Expected: { conversationId: 'conv-1', volume: 'cloud://', volumePreference: 'cloud-only' }
Received: { conversationId: 'conv-1773866695314-3hhi8o', volume: 'home://', volumePreference: 'both' }
```

## Files to Read First
- `browser/src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts` (failing tests — FIX THIS)
- `browser/src/primitives/tree-browser/adapters/chatHistoryAdapter.ts` (adapter — DO NOT MODIFY, it's correct)
- `browser/src/primitives/tree-browser/adapters/__tests__/channelsAdapter.test.ts` (reference for correct mock pattern)

## Root Cause
The test file has `vi.mock()` calls at lines 10-25, but:
- Mock setup is incorrect (wrong import path, wrong structure, or timing issue)
- `vi.mocked()` calls (lines 38, 72, etc.) aren't being applied correctly
- Real `chatApi` is imported before mocks are established

## Deliverables
- [ ] Fix mock setup in `chatHistoryAdapter.test.ts`
- [ ] Verify `vi.mock()` paths match actual import paths
- [ ] Ensure mocked functions return expected data
- [ ] All 30 tests pass in tree-browser suite
- [ ] No regressions in other adapter tests

## Acceptance Criteria
- [ ] `cd browser && npx vitest run src/primitives/tree-browser/` — all tests pass (0 failed)
- [ ] No changes to adapter source files (only test file changes)
- [ ] Mock functions properly intercept real API calls
- [ ] Test data matches expected conversation format (no random IDs)

## Smoke Test
```bash
cd browser && npx vitest run src/primitives/tree-browser/ --reporter=verbose
cd browser && npx vitest run
```

## Constraints
- **TDD:** Tests exist. Fix mocks, not source code.
- No file over 500 lines
- No stubs
- **DO NOT modify adapter source code** — only fix test mocks
- CSS: var(--sd-*) only (N/A — no CSS changes)

## Model Assignment
sonnet

## Priority
P0
