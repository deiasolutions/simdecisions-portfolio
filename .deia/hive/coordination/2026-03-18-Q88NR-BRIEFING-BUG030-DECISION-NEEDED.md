# Q88N Decision Required: BUG030 Test Strategy

**From:** Q88NR-bot (REGENT-QUEUE-TEMP-2026-03-18-2038-SPE)
**Date:** 2026-03-18 20:40
**Priority:** P1 (blocks completing BUG030 work)

---

## Situation Summary

**BUG-030: Chat tree-browser empty** has been investigated and partially fixed. The original diagnosis was incorrect, and a new approach is needed.

### What Happened

1. **REQUEUE-BUG030 spec** said: "Fix test mocks — test expectations don't match API"
2. **Fix Cycle 1 (Sonnet BEE)** discovered: Test expectations ARE correct, but test isolation is broken
3. **Root cause:** chatApi reads real localStorage data, bypassing mocks
4. **Current state:** 2/9 tests passing (was 1/9), but 7 still fail due to localStorage isolation
5. **Status:** Marked NEEDS_DAVE — architectural decision required

### Why NEEDS_DAVE

This is not a "failed fix" that can be iterated. The original premise was wrong. We need a **different test strategy**, not better mocking.

---

## The Core Issue

**chatHistoryAdapter tests cannot properly mock chatApi because:**
1. chatApi imports at module load time (before mocks applied)
2. chatApi internally accesses localStorage directly
3. Tests read REAL conversation data from previous test runs
4. Mock setup patterns are correct (proven by volumeStatus mock working)

**Example failure:**
```
Expected: { conversationId: 'conv-1', volume: 'cloud://', volumePreference: 'cloud-only' }
Received: { conversationId: 'conv-1773866695314-3hhi8o', volume: 'home://', volumePreference: 'both' }
```
→ The received data is REAL data from localStorage, not mocked data.

---

## Three Options (from BEE Analysis)

### Option A: Mock fetch globally ⚡ FASTEST
**Pattern:** Like `chatApi.test.ts` already does

```typescript
const mockFetch = vi.fn();
vi.stubGlobal('fetch', mockFetch);

// Force chatApi to use localStorage by making fetch fail
mockFetch.mockRejectedValue(new Error('Connection refused'));
```

**Pros:**
- Minimal code changes (only test file)
- Fast to implement (1-2 hours)
- Forces chatApi to use localStorage backend
- Can then mock localStorage or seed test data

**Cons:**
- Still testing integration of adapter + chatApi + storage
- Not true unit test isolation

**Effort:** Small (S)
**BEE model:** Haiku

---

### Option B: Factory pattern 🏗️ BEST ARCHITECTURE
**Pattern:** Dependency injection for testability

```typescript
// Refactor chatHistoryAdapter to accept dependencies
export function createChatHistoryAdapter(deps: { chatApi: ChatApi }) {
  return {
    getTree: async () => {
      const conversations = await deps.chatApi.listConversations();
      // ... rest of logic
    }
  };
}

// In tests, pass mocked chatApi
const mockChatApi = { listConversations: vi.fn() };
const adapter = createChatHistoryAdapter({ chatApi: mockChatApi });
```

**Pros:**
- True unit test isolation
- Better architecture (explicit dependencies)
- Easier to test edge cases
- Reusable pattern for other adapters

**Cons:**
- Requires source code changes (not just tests)
- Larger refactor
- May affect adapter registration system

**Effort:** Medium (M)
**BEE model:** Sonnet

---

### Option C: Integration test approach 🔗 PRAGMATIC
**Pattern:** Accept that adapter tests are integration tests

```typescript
beforeEach(async () => {
  // Clear localStorage
  localStorage.clear();

  // Seed test data via chatApi functions
  await chatApi.createConversation('conv-1', { title: 'Test Chat' });
  await chatApi.createConversation('conv-2', { title: 'Another Chat' });
});

it('groups conversations by date', async () => {
  const tree = await adapter.getTree();
  // Assert on real data we just seeded
  expect(tree[0].children).toHaveLength(2);
});
```

**Pros:**
- Tests real behavior (adapter + chatApi + localStorage)
- No mocking complexity
- Fast to implement
- Tests are more realistic

**Cons:**
- Slower tests (real localStorage I/O)
- Not true unit tests (tests multiple layers)
- Harder to test error cases

**Effort:** Small-Medium (S-M)
**BEE model:** Haiku or Sonnet

---

## My Recommendation

**Option A (mock fetch globally)** for now, with future refactor to Option B.

**Reasoning:**
1. **Fast:** Can be done in 1-2 hours (Haiku)
2. **Low risk:** Only changes test file, no source code changes
3. **Unblocks:** Gets tests passing quickly
4. **Path forward:** Can refactor to Option B later when we have time for architectural improvements

**Option B is the "right" architecture**, but it's a larger change that should be done when we're ready to refactor all adapters consistently.

**Option C is pragmatic** but makes tests slower and harder to maintain long-term.

---

## Decision Required from Q88N

**Choose one:**
- [ ] **Option A** — Mock fetch globally (FAST, low risk) ← Q88NR recommends
- [ ] **Option B** — Factory pattern (BEST, larger refactor)
- [ ] **Option C** — Integration tests (PRAGMATIC, not true unit tests)
- [ ] **Option D** — Something else (please specify)

**Once chosen, I will:**
1. Create BUG030C spec with chosen approach
2. Dispatch appropriate BEE (Haiku for A/C, Sonnet for B)
3. Monitor completion
4. Report results

---

## Files for Reference

**Investigation reports:**
- `.deia/hive/responses/20260318-FIX-BUG030-FINAL-REPORT.md` — Fix Cycle 1 summary
- `.deia/hive/responses/20260318-TASK-BUG030B-RESPONSE.md` — BEE analysis (detailed)
- `.deia/hive/responses/20260318-SPEC-fix-BUG030-FINAL-RESPONSE.md` — This spec completion

**Specs moved to _needs_review/:**
- `2026-03-18-2007-SPEC-fix-REQUEUE-BUG030-chat-tree-empty.md`
- `2026-03-18-2038-SPEC-fix-REQUEUE-BUG030-chat-tree-empty.md`

**Test file:**
- `browser/src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts` (275 lines)

**Source file (correct, no changes needed):**
- `browser/src/primitives/tree-browser/adapters/chatHistoryAdapter.ts` (103 lines)

---

## Current Test Status

```bash
cd browser && npx vitest run src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts
```

**Result:**
- ✅ 2 passing
- ❌ 7 failing (localStorage isolation)

**Passing tests:**
- uses conversation ID for label when title is null
- handles conversations with zero messages

**Failing tests:**
- returns empty array when no conversations exist
- groups conversations by date
- sorts conversations by updated_at (newest first)
- includes volume status badge
- truncates long conversation titles
- returns empty array on error
- includes metadata for conversation nodes

---

## Budget Impact

**Already spent (Fix Cycle 1):**
- Clock: ~2.25 hours
- Cost: ~$0.15 USD
- Carbon: ~15g CO2e

**Estimated for BUG030C:**
- Option A: ~$0.05 USD (Haiku, 1-2 hours)
- Option B: ~$0.15 USD (Sonnet, 3-4 hours)
- Option C: ~$0.08 USD (Haiku/Sonnet, 2-3 hours)

**Total budget estimate (A):** ~$0.20 USD
**Total budget estimate (B):** ~$0.30 USD
**Total budget estimate (C):** ~$0.23 USD

---

**Q88NR SIGNATURE:** REGENT-QUEUE-TEMP-2026-03-18-2038-SPE
**AWAITING:** Q88N decision on Option A, B, C, or D
**NEXT ACTION:** Create BUG030C spec once decision received
