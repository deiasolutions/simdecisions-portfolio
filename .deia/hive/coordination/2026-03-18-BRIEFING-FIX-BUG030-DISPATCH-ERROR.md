# BRIEFING: Fix BUG030 Test Mocks (Dispatch Correction)

**From:** Q88NR-bot (Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-18
**Priority:** P0

---

## Problem

The queue runner dispatched `2026-03-18-SPEC-REQUEUE-BUG030-chat-tree-empty.md` with **role=regent** instead of **role=bee**. This caused the regent bot to run an investigation instead of a bee fixing the test mocks.

**Result:** Commit 1aa7aa8 has "NEEDS_DAVE" flag. No test fixes were applied.

---

## Objective

Dispatch a BEE (sonnet) to fix the test mocks in `chatHistoryAdapter.test.ts` as specified in the original spec.

---

## Context from Investigation

Previous regent investigation (20260318-Q88NR-BUG030-REQUEUE-ANALYSIS.md) found:

- **Adapter source code is CORRECT** — no changes needed
- **AUTO_EXPAND fix is CORRECT** — already applied
- **Test mocks are BROKEN** — 30 tests failing due to mock setup issues

### Test Failures
```bash
cd browser && npx vitest run src/primitives/tree-browser/
# Result: 30 failed | 163 passed (193 total)
```

### Root Cause
File: `browser/src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts`

Test expectations don't match actual API behavior:
- Expected `conversationId: 'conv-1'` but API generates dynamic IDs like `'conv-1773866695314-3hhi8o'`
- Expected `volume: 'cloud://'` but API defaults to `'home://'`
- Expected `volumePreference: 'cloud-only'` but API defaults to `'both'`
- Expected badge `'🟢'` but API returns `'🔴'` (offline status when mocked)

---

## Task File Already Exists

**File:** `.deia/hive/tasks/2026-03-18-TASK-BUG030B-fix-chat-history-tests.md`

**Review this task file** and confirm it's correct. If it is, dispatch a BEE (sonnet) immediately. If corrections are needed, fix it first, then dispatch.

---

## Deliverables Expected from BEE

- [ ] Fix mock expectations in `chatHistoryAdapter.test.ts`
- [ ] Use pattern matching for dynamic conversationIds (not hardcoded values)
- [ ] Fix volume defaults to 'home://' (not 'cloud://')
- [ ] Fix volumePreference defaults to 'both' (not 'cloud-only')
- [ ] Fix badge expectations to '🔴' (offline) or mock volumeStatus to return 'online'
- [ ] All 30 tests pass
- [ ] No changes to adapter source code
- [ ] No regressions in other tree-browser tests

---

## Files BEE Should Read

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\chatHistoryAdapter.test.ts` (failing tests — FIX THIS)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts` (adapter — reference only, DON'T MODIFY)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatApi.ts` (API contract)

---

## Acceptance Criteria

- [ ] `cd browser && npx vitest run src/primitives/tree-browser/` — all tests pass (0 failed)
- [ ] No changes to adapter source files (only test file changes)
- [ ] Mock functions properly intercept real API calls
- [ ] Test data matches expected conversation format (pattern matching, not hardcoded)

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

**sonnet** — Test fixing requires understanding API contracts and mock expectations

---

## Your Action Items

1. Review task file `.deia/hive/tasks/2026-03-18-TASK-BUG030B-fix-chat-history-tests.md`
2. If correct, dispatch BEE immediately:
   ```bash
   python .deia/hive/scripts/dispatch/dispatch.py \
     .deia/hive/tasks/2026-03-18-TASK-BUG030B-fix-chat-history-tests.md \
     --model sonnet \
     --role bee \
     --inject-boot
   ```
3. If task file needs corrections, fix it first then dispatch
4. Monitor BEE output
5. Report results to Q88NR

---

## Expected Result

BEE response file: `.deia/hive/responses/20260318-TASK-BUG030B-RESPONSE.md`

With status: **COMPLETE**
With test results: **193 passed | 0 failed**
