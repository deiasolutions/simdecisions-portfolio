# TASK-BUG-030-C: Fix Chat History Adapter Test Mocks

**Date:** 2026-03-18
**Model:** sonnet
**Priority:** P0
**Parent:** BUG-030 (Re-Queue 3)

---

## Objective

Fix the broken test mocks in `chatHistoryAdapter.test.ts` so all 8 tests pass. The adapter source code is correct — only the test infrastructure needs to be fixed.

---

## Context

BUG-030 has been re-queued twice. Previous fix attempts failed because:
1. First attempt: Modified adapter source (wrong approach)
2. Second attempt: All 4 fix cycles hit _active/ path bug (now fixed by spec_processor.py)

**Current status:** 7 failing / 2 passing (only 2 passing because they don't call the adapter fully)

**Root cause:** The test mocks are defined with `vi.mock()` but are NOT intercepting the real API calls. Real functions (`listConversations`, `getVolumeStatus`) are being called instead of mocks, causing:
- 401 errors from `/node/discover`
- Random conversation IDs instead of test data
- Unpredictable test results

### Evidence from Test Output

```
[volumeStatus] Failed to check volume status: Error: /node/discover returned 401
    at getNodeList (volumeStatus.ts:51:11)
```

This proves the **real** `getVolumeStatus()` is being called, not the mocked version.

### Why Current Mocks Don't Work

The current test file (lines 8-38) uses this pattern:

```typescript
// Lines 9-18: vi.mock() with factory returning vi.fn()
vi.mock('../../../../services/terminal/chatApi', async () => {
  return {
    listConversations: vi.fn(),
    // ...
  };
});

// Lines 22-29: Same pattern for volumeStatus
vi.mock('../../../../services/volumes/volumeStatus', async () => {
  return {
    getVolumeStatus: vi.fn(),
    // ...
  };
});

// Lines 31-33: Import adapter and functions
import { loadChatHistory } from '../chatHistoryAdapter';
import { listConversations } from '../../../../services/terminal/chatApi';
import { getVolumeStatus } from '../../../../services/volumes/volumeStatus';

// Lines 36-37: Get mocked versions
const mockListConversations = vi.mocked(listConversations);
const mockGetVolumeStatus = vi.mocked(getVolumeStatus);

// Lines 40-46: Configure in beforeEach
beforeEach(() => {
  mockListConversations.mockClear();
  mockGetVolumeStatus.mockClear();
  localStorage.clear();
  mockListConversations.mockResolvedValue([]);
  mockGetVolumeStatus.mockResolvedValue('offline');
});
```

**The problem:** The `vi.fn()` calls in the factory create new mock functions, but the `mockResolvedValue()` calls in `beforeEach` are configuring DIFFERENT mock instances. The factory runs at hoist time, returning new functions, but the test is trying to configure them later.

---

## Solution Approach

**Use the global fetch mock pattern** (proven pattern from `volumeStatus.test.ts`, lines 8-9):

```typescript
const mockFetch = vi.fn();
global.fetch = mockFetch;
```

Since both `chatApi.ts` and `volumeStatus.ts` use `fetch()` internally, mocking `fetch` globally will intercept all HTTP calls and give us full control over responses.

### Implementation Steps

1. **Remove the current `vi.mock()` calls** for chatApi and volumeStatus (lines 9-29)
2. **Add global fetch mock** at the top (after imports)
3. **Configure fetch mock in beforeEach** to return proper responses for:
   - `/health` endpoint (chatApi backend detection)
   - `/node/discover` endpoint (volumeStatus calls)
   - `/storage/read` endpoint (listConversations calls)
4. **Import real functions** (no mocking needed — fetch intercepts)
5. **Keep all test assertions unchanged** (they're correct)

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\chatHistoryAdapter.test.ts` (FIX THIS)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\volumes\__tests__\volumeStatus.test.ts` (reference — shows working fetch mock pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts` (DO NOT MODIFY — adapter is correct)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\volumes\volumeStatus.ts` (understand how it uses fetch)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatApi.ts` (understand how it uses fetch)

---

## Deliverables

### Must Complete

- [ ] Remove current `vi.mock()` calls for chatApi and volumeStatus from test file
- [ ] Add global `fetch` mock following volumeStatus.test.ts pattern
- [ ] Configure fetch mock in `beforeEach` to return proper responses for all endpoints
- [ ] All 8 tests pass (0 failed): `cd browser && npx vitest run src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts`
- [ ] No changes to adapter source code (`chatHistoryAdapter.ts`)
- [ ] Test output shows NO 401 errors
- [ ] Test data uses expected conversation IDs (no random IDs)

### Optional Improvements

- [ ] Add comments explaining which fetch responses map to which API calls

---

## Test Requirements

### Tests to Pass (All 8)

1. ✓ returns empty array when no conversations exist
2. ✓ groups conversations by date
3. ✓ sorts conversations by updated_at (newest first)
4. ✓ includes volume status badge
5. ✓ truncates long conversation titles
6. ✓ uses conversation ID for label when title is null
7. ✓ returns empty array on error
8. ✓ includes metadata for conversation nodes

### Edge Cases to Cover

- Empty conversation list
- Multiple date groups (Today, Yesterday, This Week, Older)
- Conversations sorted by updated_at (newest first)
- Volume status badges (online/offline)
- Long title truncation (> 40 chars)
- Null title fallback (use conversation ID)
- Error handling (network failures)
- Metadata extraction (conversationId, volume, etc.)
- Zero message count handling

### Current Test Status

```bash
# Before fix:
7 failed | 2 passed (9 total)

# After fix target:
0 failed | 9 passed (9 total)
```

---

## Acceptance Criteria

- [ ] **All tests pass:** `cd browser && npx vitest run src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts` shows `9 passed | 0 failed`
- [ ] **No 401 errors** in test output (proves mocks are working)
- [ ] **No random conversation IDs** in test output (proves mock data is used)
- [ ] **No changes** to `chatHistoryAdapter.ts` (adapter source)
- [ ] **No regressions** in other tests: `cd browser && npx vitest run src/primitives/tree-browser/` — all pass
- [ ] **Test file follows fetch mock pattern** from volumeStatus.test.ts

---

## Constraints

- **TDD:** Tests exist — fix mocks only, not source code
- **No file over 500 lines:** Test file is currently 287 lines (safe)
- **No stubs:** N/A (only fixing test infrastructure)
- **DO NOT modify adapter source** (`chatHistoryAdapter.ts`) — it is correct
- **CSS: var(--sd-*) only:** N/A (no CSS changes)
- **No git operations** without Q88N approval

---

## Smoke Tests

### Primary Test (Must Pass)

```bash
cd browser && npx vitest run src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts --reporter=verbose
```

**Expected:** 9 passed | 0 failed | No 401 errors | No random IDs

### Regression Tests (Must Not Break)

```bash
# All tree-browser tests
cd browser && npx vitest run src/primitives/tree-browser/

# Full browser test suite
cd browser && npx vitest run
```

**Expected:** All tests that passed before still pass

---

## Implementation Notes

### Fetch Mock Pattern (from volumeStatus.test.ts)

```typescript
// At top of test file (after imports)
const mockFetch = vi.fn();
global.fetch = mockFetch;

// In beforeEach
beforeEach(() => {
  vi.clearAllMocks();
  clearDiscoverCache();

  // Configure fetch responses
  mockFetch.mockImplementation((url) => {
    if (url.includes('/health')) {
      return Promise.resolve({
        ok: true,
        json: async () => ({}),
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
              online: true,
            },
          ],
        }),
      });
    }
    if (url.includes('/storage/read')) {
      return Promise.resolve({
        ok: true,
        json: async () => ({ conversations: [] }),
      });
    }
    return Promise.reject(new Error('Unknown endpoint'));
  });
});
```

### API Endpoints to Mock

Based on chatApi.ts and volumeStatus.ts:

1. **`/health`** — chatApi backend detection (return `ok: true`)
2. **`/node/discover`** — volumeStatus node list (return nodes with volumes)
3. **`/storage/read`** — chatApi conversation index (return conversations array)

### Test Data Structure

Each test will override the default fetch mock with `mockFetch.mockResolvedValueOnce()` to return specific test data. Example:

```typescript
it('groups conversations by date', async () => {
  const today = new Date().toISOString();
  const yesterday = new Date(Date.now() - 86_400_000).toISOString();

  mockFetch.mockImplementation((url) => {
    if (url.includes('/health')) {
      return Promise.resolve({ ok: true });
    }
    if (url.includes('/storage/read')) {
      return Promise.resolve({
        ok: true,
        json: async () => ([
          {
            id: 'conv-1773866695314-abc123',
            title: 'Today Conversation',
            created_at: today,
            updated_at: today,
            message_count: 5,
            volume: 'home://',
            volume_preference: 'both',
          },
          {
            id: 'conv-1773866695315-def456',
            title: 'Yesterday Conversation',
            created_at: yesterday,
            updated_at: yesterday,
            message_count: 3,
            volume: 'home://',
            volume_preference: 'both',
          },
        ]),
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
              online: true,
            },
          ],
        }),
      });
    }
    return Promise.reject(new Error('Unknown endpoint'));
  });

  const result = await loadChatHistory();

  expect(result).toHaveLength(2);
  expect(result[0].label).toBe('Today');
  expect(result[1].label).toBe('Yesterday');
});
```

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-BUG030C-RESPONSE.md`

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

---

## Reference: volumeStatus.test.ts (Working Pattern)

Lines 7-9 show the working global fetch mock pattern:

```typescript
// Mock fetch globally
const mockFetch = vi.fn();
global.fetch = mockFetch;
```

Lines 12-15 show proper setup:

```typescript
beforeEach(() => {
  vi.clearAllMocks();
  clearDiscoverCache();
});
```

Lines 25-37 show how to configure fetch responses per test:

```typescript
mockFetch.mockResolvedValueOnce({
  ok: true,
  json: async () => ({
    nodes: [
      {
        node_id: 'node-1',
        volumes: ['home'],
        last_seen: fourMinutesAgo.toISOString(),
        online: true,
      },
    ],
  }),
});
```

**Follow this exact pattern.**

---

**BEE: Read this task file, read the reference files, implement the global fetch mock pattern, and ensure all 8 tests pass. Write your response file when complete.**
