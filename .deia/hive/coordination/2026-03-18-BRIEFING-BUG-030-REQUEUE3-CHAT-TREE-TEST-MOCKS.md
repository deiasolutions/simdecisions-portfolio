# BRIEFING: BUG-030 (Re-Queue 3) — Fix Chat History Adapter Test Mocks

**Date:** 2026-03-18
**From:** Q33NR (Regent)
**To:** Q33N (Coordinator)
**Priority:** P0
**Model Assignment:** sonnet

---

## Objective

Fix the broken test mocks in `chatHistoryAdapter.test.ts` so all 30 failing tests pass. **DO NOT modify the adapter source code** — it is correct. Only fix the test mocks.

---

## Background

BUG-030 has been re-queued twice before. Previous attempts failed due to:
1. First attempt: Tried to modify adapter source code (wrong approach)
2. Second attempt: All 4 fix cycles hit _active/ path bug (now fixed)

**Root issue identified**: The test mocks are defined but NOT being applied. Real API functions (`listConversations`, `getVolumeStatus`) are being called instead of mocks, causing 401 errors and random conversation IDs.

---

## Problem Analysis

### Current Test Behavior
```bash
cd browser && npx vitest run src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts
# Result: 0 passed | 8 failed
```

### Error Pattern
```
[volumeStatus] Failed to check volume status: Error: /node/discover returned 401
```

This proves the real `getVolumeStatus()` is being called, not the mocked version.

### Why Mocks Aren't Working

Current test file structure (lines 8-29):
```typescript
// Lines 8-10: Declare mock functions
const mockListConversations = vi.fn();
const mockGetVolumeStatus = vi.fn();

// Lines 12-27: vi.mock() calls
vi.mock('../../../../services/terminal/chatApi', () => ({
  listConversations: () => mockListConversations(),
  ...
}));

vi.mock('../../../../services/volumes/volumeStatus', () => ({
  getVolumeStatus: () => mockGetVolumeStatus(),
  ...
}));

// Line 29: Import adapter AFTER mocks
import { loadChatHistory } from '../chatHistoryAdapter';
```

**Problem**: The mock factory functions (`() => mockListConversations()`) are called ONCE at hoist time, but `mockListConversations` hasn't been configured yet. The `mockResolvedValue()` calls in `beforeEach` happen AFTER the module is already imported.

---

## Solution

There are two valid approaches:

### Approach A: Direct Mock Implementation (Recommended)
Replace the current mock pattern with direct implementations in the `vi.mock()` factory:

```typescript
vi.mock('../../../../services/terminal/chatApi', () => ({
  listConversations: vi.fn().mockResolvedValue([]),
  createConversation: vi.fn(),
  // ...
}));

vi.mock('../../../../services/volumes/volumeStatus', () => ({
  getVolumeStatus: vi.fn().mockResolvedValue('offline'),
  // ...
}));

import { loadChatHistory } from '../chatHistoryAdapter';
import { listConversations } from '../../../../services/terminal/chatApi';
import { getVolumeStatus } from '../../../../services/volumes/volumeStatus';

// In beforeEach:
vi.mocked(listConversations).mockResolvedValue([]);
vi.mocked(getVolumeStatus).mockResolvedValue('offline');
```

### Approach B: Mock fetch Globally (Alternative)
If the above doesn't work, mock `fetch` globally like `volumeStatus.test.ts` does, and let the real functions run but intercept the HTTP calls.

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\chatHistoryAdapter.test.ts` (failing tests — FIX THIS)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\volumes\__tests__\volumeStatus.test.ts` (reference: shows global fetch mocking pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts` (adapter — DO NOT MODIFY)

---

## Deliverables

1. **Fix test mocks** in `chatHistoryAdapter.test.ts`
2. **All 8 tests pass** (0 failed)
3. **No changes to adapter source** code (only test file changes)
4. **No regressions** in other tree-browser tests

---

## Acceptance Criteria

- [ ] `cd browser && npx vitest run src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts` — all tests pass (0 failed)
- [ ] Mock functions properly intercept real API calls (no 401 errors in test output)
- [ ] Test data uses expected conversation IDs (no random IDs like `conv-1773866695314-...`)
- [ ] No changes to `chatHistoryAdapter.ts` (adapter source)
- [ ] All other tree-browser tests still pass: `cd browser && npx vitest run src/primitives/tree-browser/`

---

## Smoke Test

```bash
cd browser && npx vitest run src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts --reporter=verbose
cd browser && npx vitest run src/primitives/tree-browser/
cd browser && npx vitest run
```

---

## Constraints

- **TDD**: Tests exist. Fix mocks, not source code.
- **No file over 500 lines**
- **No stubs**
- **DO NOT modify adapter source code** — only fix test mocks
- **CSS: var(--sd-*) only** (N/A — no CSS changes)

---

## Notes

- The adapter source code is CORRECT and working
- AUTO_EXPAND fix was CORRECT (groups auto-expand now)
- This is purely a test infrastructure issue (mock setup)
- Reference `volumeStatus.test.ts` for working mock patterns

---

**Q33N: Read this briefing, read the files listed, analyze the mock issue, write a task file, and return it to me (Q33NR) for review before dispatching any bees.**
