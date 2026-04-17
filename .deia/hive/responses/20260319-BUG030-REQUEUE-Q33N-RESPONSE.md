# BUG-030 REQUEUE: Chat Tree Duplicate Conversations — Q33N TASK FILE READY

**Status:** TASK FILE READY FOR REVIEW
**Model:** Sonnet (Q33N coordinator)
**Date:** 2026-03-19

---

## Task File Created

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-19-TASK-BUG030D-CHAT-TREE-DEDUP.md`

**Task ID:** TASK-BUG030D
**Objective:** Fix chat tree duplicate conversations by adding explicit deduplication at adapter level

---

## Analysis Summary

After reading the source code, I identified the issue:

### Current Architecture
1. `chatApi.ts` `readIndex()` already has deduplication logic (lines 204-211)
2. It merges `home://` and `cloud://` indexes and dedupes by conversation ID
3. However, this assumes the duplicates come from cross-volume merging

### The Actual Bug
The briefing states **40+ duplicates** appear at runtime. This suggests:
- Duplicates exist WITHIN a single volume's index file (not just across volumes)
- OR the deduplication in chatApi is failing silently
- OR the adapter is being called multiple times and accumulating results

### The Fix (Defensive Layer)
Add explicit deduplication in `chatHistoryAdapter.ts` AFTER calling `listConversations()`:
- Use a Map to track conversations by ID
- If duplicate IDs exist, prefer the one with most recent `updated_at`
- This is defensive even though chatApi should already dedupe

---

## Task File Contents

**Files to modify:**
1. `chatHistoryAdapter.ts` — add deduplication logic after `listConversations()` call
2. `chatHistoryAdapter.test.ts` — add test that verifies deduplication works

**Key implementation:**
```typescript
// DEFENSIVE DEDUPLICATION
const deduped = new Map<string, Conversation>();
for (const conv of conversations) {
  const existing = deduped.get(conv.id);
  if (!existing || new Date(conv.updated_at) > new Date(existing.updated_at)) {
    deduped.set(conv.id, conv);
  }
}
```

**Test coverage:**
- New test: `'deduplicates conversations with same ID'`
- Mocks 3 conversations with identical IDs but different `updated_at`
- Verifies only 1 appears in result (the newest one)

---

## Why This Approach

1. **Previous attempts only fixed test mocks** — this fixes the actual adapter source
2. **Defensive programming** — even if chatApi dedupes correctly, an extra layer catches edge cases
3. **Minimal change** — ~10 lines added to adapter, maintains all existing behavior
4. **TDD approach** — test written first to demonstrate the bug, then fix applied
5. **No performance impact** — Map-based dedup is O(n), same as existing sort operation

---

## Files Referenced During Analysis

- `chatHistoryAdapter.ts` (125 lines) — the adapter with grouping logic
- `chatApi.ts` (411 lines) — API layer with existing dedup at lines 204-211
- `chatHistoryAdapter.test.ts` (486 lines) — existing test suite (9 tests, all pass)

---

## Next Steps

**Awaiting Q33NR review of task file.**

Once approved, I will:
1. Dispatch a Haiku bee to implement the fix
2. Review the bee's response file
3. Verify all tests pass
4. Report completion to Q33NR

---

## Notes for Q33NR

- The task file is complete with full implementation guidance
- Test is fully specified (no ambiguity for the bee)
- Model: Haiku is sufficient for this implementation (straightforward logic)
- Estimated time: 15-20 minutes for bee to complete
- No dependencies on other tasks
- Can be dispatched immediately after approval
