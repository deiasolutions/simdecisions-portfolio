# BRIEFING: Fix BUG030 chatHistoryAdapter Test Mocks

**From:** Q88NR-bot (Regent) — Bot ID: REGENT-QUEUE-TEMP-2026-03-18-2007-SPE
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-18
**Priority:** P0
**Fix Cycle:** 1 of 2

---

## Problem

Fix spec `2026-03-18-2007-SPEC-fix-REQUEUE-BUG030-chat-tree-empty.md` was created after the queue runner dispatched the REQUEUE spec with wrong role (regent instead of bee).

A corrective action was taken: TASK-BUG030B was created and a BEE was dispatched at ~20:30. However, there's no response file yet, which means either:
1. The BEE is still running (unlikely — it's been ~90 minutes)
2. The BEE failed silently
3. The dispatch itself failed

**Current test status:**
```bash
cd browser && npx vitest run src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts
# Tests are STILL FAILING
# Error: volumeStatus.getVolumeStatus is not properly mocked
# Real API calls returning 401
```

---

## Root Cause Analysis

Test file `chatHistoryAdapter.test.ts` has mock declarations, but they're not intercepting the real calls. The actual error:
```
[volumeStatus] Failed to check volume status: Error: /node/discover returned 401
    at getNodeList (volumeStatus.ts:51:11)
    at Module.getVolumeStatus (volumeStatus.ts:79:19)
    at conversationToNode (chatHistoryAdapter.ts:50:18)
```

This means:
- The `volumeStatus` module mock is not working
- Real `volumeStatus.getVolumeStatus()` is being called
- Needs proper `vi.mock()` setup for `volumeStatus`

---

## Objective

Review TASK-BUG030B task file, verify it's correct, then **dispatch a BEE (sonnet) immediately** to fix the test mocks.

---

## Task File Location

**File:** `.deia/hive/tasks/2026-03-18-TASK-BUG030B-fix-chat-history-tests.md`

**Review checklist:**
- [ ] Deliverables match spec (fix test mocks, not source code)
- [ ] File paths are absolute
- [ ] Test requirements present
- [ ] No CSS changes (N/A)
- [ ] File under 500 lines
- [ ] No stubs specified
- [ ] Response file template present
- [ ] **NEW:** Specifies volumeStatus must be mocked

---

## What BEE Must Deliver

**Primary fix:**
- [ ] Add proper `vi.mock()` for `'../../services/volumes/volumeStatus'`
- [ ] Mock `getVolumeStatus` to return `'online'` by default
- [ ] Ensure mock is established BEFORE importing chatHistoryAdapter
- [ ] Fix test expectations to match API defaults (home://, both, dynamic IDs)

**Test requirements:**
- [ ] All 9 tests in chatHistoryAdapter.test.ts pass
- [ ] No regressions in other tree-browser tests (should be 163+ passing total)
- [ ] No changes to adapter source code

---

## Files BEE Should Read

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\chatHistoryAdapter.test.ts` (failing tests — FIX THIS)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\volumes\volumeStatus.ts` (API contract for mocking)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts` (adapter — reference only, DON'T MODIFY)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\channelsAdapter.test.ts` (reference for correct mock pattern)

---

## Acceptance Criteria

- [ ] `cd browser && npx vitest run src/primitives/tree-browser/` — all tests pass (0 failed)
- [ ] No volumeStatus 401 errors in test output
- [ ] No changes to adapter source files (only test file changes)
- [ ] Mock functions properly intercept real API calls
- [ ] Test data matches expected conversation format

---

## Constraints

- **DO NOT modify chatHistoryAdapter.ts source code** — it's correct
- **DO NOT modify treeBrowserAdapter.tsx** — AUTO_EXPAND fix already applied
- **ONLY fix the test file** — chatHistoryAdapter.test.ts
- No file over 500 lines
- No stubs
- TDD: Tests exist, fix mocks not source code

---

## Model Assignment

**sonnet** — Test fixing requires understanding vitest mock setup and API contracts

---

## Your Action Items (Q33N)

1. **Review task file** `.deia/hive/tasks/2026-03-18-TASK-BUG030B-fix-chat-history-tests.md`
2. **Check if it mentions volumeStatus mock issue.** If not, update the task file to add:
   ```markdown
   ### Critical Issue
   The volumeStatus module is not properly mocked. Add:
   ```typescript
   vi.mock('../../services/volumes/volumeStatus', () => ({
     getVolumeStatus: vi.fn().mockResolvedValue('online')
   }))
   ```
   BEFORE any imports that use it.
   ```
3. **Dispatch BEE immediately:**
   ```bash
   python .deia/hive/scripts/dispatch/dispatch.py \
     .deia/hive/tasks/2026-03-18-TASK-BUG030B-fix-chat-history-tests.md \
     --model sonnet \
     --role bee \
     --inject-boot
   ```
4. **Monitor BEE output**
5. **Report results to Q88NR**

---

## Expected BEE Deliverable

**Response file:** `.deia/hive/responses/20260318-TASK-BUG030B-RESPONSE.md`

**Status:** COMPLETE

**Test results:** 193 passed | 0 failed (tree-browser suite)

**Files modified:** Only `chatHistoryAdapter.test.ts`

---

## Budget Note

- Previous dispatch (if it ran): unknown cost
- This dispatch: estimated $0.10-0.20 (sonnet, test fix)
- Total fix cycle 1: < $0.25

---

## Timeline

- Original REQUEUE spec dispatched: ~20:00
- Fix cycle 1 spec created: ~20:07
- First corrective dispatch attempted: ~20:30
- Current briefing: ~21:00
- **Target BEE dispatch: IMMEDIATELY**
- **Target completion: Within 30 minutes**
