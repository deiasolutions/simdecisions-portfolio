# BUG-030 (RE-QUEUE): Chat tree-browser test failures — 30 tests failing

## Background — Why Re-Queued
Previous bee (Haiku) claimed COMPLETE but only ran 2 configuration tests. Full test suite shows **30 tests failing** in `chatHistoryAdapter.test.ts`. The adapter fix (adding 'chat-history' to AUTO_EXPAND_ADAPTERS) was correct, but existing tests are broken due to mock setup issues.

## Problem Analysis
Q88NR-bot investigation (2026-03-18 20:02) found:
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

## Objective
Fix the test mocks in `chatHistoryAdapter.test.ts` so all 30 failing tests pass. **DO NOT modify adapter source code** — it is correct.

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

## Re-Queue Metadata
- Original spec: `.deia/hive/queue/_done/2026-03-17-SPEC-TASK-BUG030-chat-tree-browser-empty.md`
- Previous response: `.deia/hive/responses/20260317-BUG-030-RESPONSE.md`
- Failure reason: 30 tests failing — mock setup broken, real chatApi being called
- Test file: `browser/src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts`
- Investigation by: Q88NR-bot (REGENT-QUEUE-TEMP-2026-03-18-SPEC-REQ)
