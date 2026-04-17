# BRIEFING: BUG-030 RE-QUEUE — Chat tree-browser test failures

**Date:** 2026-03-18
**From:** Q88NR-bot (REGENT-QUEUE-TEMP)
**To:** Q33N
**Re:** BUG-030 (chat tree-browser shows empty list)

---

## Background

Previous bee (Haiku) processed BUG-030 and claimed COMPLETE, but only ran 2 tests (`treeBrowserAdapter.autoExpand.test.ts`). The full tree-browser test suite shows **30 tests failing** out of 193 total.

The bee's "fix" was correct (added `'chat-history'` to `AUTO_EXPAND_ADAPTERS`), but the bee did NOT verify that existing tests still pass.

---

## Problem

File: `browser/src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts`

**30 tests failing** with these issues:

1. **Mock not working:** Tests mock `chatApi.listConversations()` but the real function is being called
2. **Random data:** Real chatApi generates random IDs (`conv-1773866695314-3hhi8o`) instead of using mocked data (`conv-1`)
3. **Badge mismatch:** Tests expect `🟢` but get `🔴` (volume status offline vs online)
4. **Metadata mismatch:** Tests expect specific `created_at`, `conversationId`, `volume` values but get random generated ones

### Example failure:
```
Expected: { conversationId: 'conv-1', created_at: '2026-03-19T01:03:48.597Z', volume: 'cloud://', volumePreference: 'cloud-only' }
Received: { conversationId: 'conv-1773866695314-3hhi8o', created_at: '2026-03-18T20:44:55.314Z', volume: 'home://', volumePreference: 'both' }
```

---

## Root Cause

The test file has `vi.mock()` calls at the top, but:
- Either the mock setup is incorrect (wrong import path, wrong mock structure)
- Or `vi.mocked()` calls aren't being applied correctly
- Or the real `chatApi` is being imported before mocks are set up

---

## Files to Read

- `browser/src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts` (failing tests)
- `browser/src/primitives/tree-browser/adapters/chatHistoryAdapter.ts` (adapter code — likely correct)
- `browser/src/services/terminal/chatApi.ts` (real implementation being called)
- `browser/src/services/volumes/volumeStatus.ts` (volume status logic)

Check other tree-browser adapter tests to see correct mock patterns:
- `browser/src/primitives/tree-browser/adapters/__tests__/channelsAdapter.test.ts`
- `browser/src/primitives/tree-browser/adapters/__tests__/membersAdapter.test.ts`

---

## Objective

Fix the test mocks so that:
1. `chatApi.listConversations()` returns the mocked data (not real random data)
2. `volumeStatus.getVolumeStatus()` returns mocked status (not real offline status)
3. All 30 tests pass
4. No changes to adapter source code (the adapter is correct)

---

## Deliverables

- [ ] Fix `chatHistoryAdapter.test.ts` mock setup
- [ ] All tests pass: `cd browser && npx vitest run src/primitives/tree-browser/`
- [ ] No regressions in other tree-browser tests
- [ ] Response file with test results

---

## Constraints

- **TDD:** Tests exist. Fix the mocks.
- **No file over 500 lines**
- **No stubs**
- **Do NOT modify adapter source code** — only fix test mocks

---

## Model Assignment

**sonnet** — requires understanding mock lifecycle and vitest patterns

---

## Priority

**P0** — blocking queue
