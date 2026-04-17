# TASK-BUG030D: Fix Chat Tree Duplicate Conversations (Runtime Deduplication)

## Objective

Fix the runtime bug in `chatHistoryAdapter.ts` where the same conversation appears 40+ times in the chat tree-browser by adding explicit deduplication at the adapter level, ensuring each conversation appears exactly once.

## Context

**Issue:** The chat tree-browser is showing the same conversation duplicated 40+ times across different date groups ("Today", "Yesterday", "Last Week"). This is a RUNTIME bug.

**Root cause investigation:**
1. `chatApi.ts` `readIndex()` already deduplicates when merging home:// and cloud:// indexes (lines 204-211)
2. However, the adapter calls `listConversations()` which could potentially return duplicates if:
   - The same conversation ID exists multiple times within a single volume's index file
   - The adapter is being called multiple times and accumulating results
   - The deduplication in chatApi is failing silently

**Previous fix attempts only addressed test mocks, not the actual adapter source.**

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts` — the adapter (MODIFY THIS)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatApi.ts` — the API layer (reference only, has dedup logic)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\chatHistoryAdapter.test.ts` — existing tests (ADD dedup test)

## Deliverables

### Code Changes

- [ ] Modify `chatHistoryAdapter.ts` to add explicit deduplication:
  - After calling `listConversations()`, deduplicate by conversation ID
  - Use a Map or Set to ensure each ID appears only once
  - Prefer most recent `updated_at` if duplicates exist
  - This is a defensive layer even though chatApi should already dedupe

- [ ] Add a new test to `chatHistoryAdapter.test.ts`:
  - Test name: `'deduplicates conversations with same ID'`
  - Mock scenario: `/storage/read` returns array with duplicate conversation IDs (same ID appears 3 times)
  - Verify: Result tree contains each conversation exactly once
  - Verify: No conversation appears in multiple date groups

### Implementation Details

**In `chatHistoryAdapter.ts`, modify `loadChatHistory()` function:**

```typescript
export async function loadChatHistory(): Promise<TreeNodeData[]> {
  try {
    const conversations = await listConversations();

    if (conversations.length === 0) return [];

    // DEFENSIVE DEDUPLICATION: Even though chatApi should dedupe,
    // ensure each conversation ID appears only once
    const deduped = new Map<string, Conversation>();
    for (const conv of conversations) {
      const existing = deduped.get(conv.id);
      if (!existing || new Date(conv.updated_at) > new Date(existing.updated_at)) {
        deduped.set(conv.id, conv);
      }
    }

    // Sort newest first
    const sorted = Array.from(deduped.values()).sort(
      (a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime(),
    );

    // ... rest of function unchanged
```

**In `chatHistoryAdapter.test.ts`, add new test:**

```typescript
it('deduplicates conversations with same ID', async () => {
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate()).toISOString();

  // Create duplicate conversations with same ID but different updated_at
  const mockConversations: Conversation[] = [
    {
      id: 'conv-DUPLICATE-ID',
      title: 'Older Version',
      created_at: today,
      updated_at: new Date(Date.now() - 5000).toISOString(), // Older
      message_count: 3,
      volume: 'home://',
      volume_preference: 'both',
    },
    {
      id: 'conv-DUPLICATE-ID',
      title: 'Newer Version',
      created_at: today,
      updated_at: new Date().toISOString(), // Newer
      message_count: 5,
      volume: 'cloud://',
      volume_preference: 'both',
    },
    {
      id: 'conv-DUPLICATE-ID',
      title: 'Middle Version',
      created_at: today,
      updated_at: new Date(Date.now() - 2000).toISOString(), // Middle
      message_count: 4,
      volume: 'home://',
      volume_preference: 'both',
    },
  ];

  mockFetch.mockImplementation((url) => {
    if (url.includes('/health')) {
      return Promise.resolve({ ok: true });
    }
    if (url.includes('/storage/read')) {
      return Promise.resolve({
        ok: true,
        text: async () => JSON.stringify(mockConversations),
      });
    }
    if (url.includes('/node/discover')) {
      return Promise.resolve({
        ok: true,
        json: async () => ({
          nodes: [
            {
              node_id: 'node-1',
              volumes: ['home'],
              last_seen: new Date().toISOString(),
              online: false,
            },
          ],
        }),
      });
    }
    return Promise.reject(new Error('Unknown endpoint'));
  });

  const result = await loadChatHistory();

  // Should have only 1 group (Today)
  expect(result).toHaveLength(1);
  expect(result[0].label).toBe('Today');

  // Should have exactly 1 child (deduplicated)
  expect(result[0].children).toHaveLength(1);

  // Should use the NEWEST version
  expect(result[0].children![0].label).toBe('Newer Version');
  expect(result[0].children![0].meta?.conversationId).toBe('conv-DUPLICATE-ID');
});
```

## Test Requirements

### TDD Workflow
- [ ] Write the deduplication test FIRST (add to existing test file)
- [ ] Run test, verify it FAILS (shows current bug)
- [ ] Modify adapter to add deduplication
- [ ] Run test, verify it PASSES
- [ ] Run full test suite, verify no regressions

### Test Commands

```bash
# Run adapter tests only
cd browser && npx vitest run src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts --reporter=verbose

# Run all tree-browser tests
cd browser && npx vitest run src/primitives/tree-browser/ --reporter=verbose

# Run full browser test suite
cd browser && npx vitest run
```

### Success Criteria
- [ ] New deduplication test passes
- [ ] All existing chatHistoryAdapter tests pass (9 total)
- [ ] No regressions in tree-browser tests
- [ ] No regressions in full browser test suite

## Constraints

- No file over 500 lines (chatHistoryAdapter.ts is 125 lines, well under limit)
- CSS: `var(--sd-*)` only (not applicable, no CSS changes)
- No stubs (full implementation required)
- Must import `Conversation` type from correct path
- Must maintain existing function signature for `loadChatHistory()`

## Acceptance Criteria

- [ ] `chatHistoryAdapter.ts` modified to add explicit deduplication by conversation ID
- [ ] Deduplication prefers most recent `updated_at` when duplicates exist
- [ ] New test `'deduplicates conversations with same ID'` added and passing
- [ ] Test uses 3 duplicate IDs to verify dedup logic
- [ ] Test verifies only 1 conversation appears in result (newest version)
- [ ] All existing tests continue to pass
- [ ] No console errors or warnings during test run

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260319-TASK-BUG030D-RESPONSE.md`

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
