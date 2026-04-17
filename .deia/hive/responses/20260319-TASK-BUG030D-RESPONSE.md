# TASK-BUG030D: Fix Chat Tree Duplicate Conversations (Runtime Deduplication) -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku 4.5
**Date:** 2026-03-19

## Files Modified

1. **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts** (MODIFIED)
   - Added explicit deduplication logic in `loadChatHistory()` function (lines 86-95)
   - Deduplicates by conversation ID using Map
   - Prefers most recent `updated_at` when duplicates exist
   - File size: 136 lines (under 500 limit)

2. **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\chatHistoryAdapter.test.ts** (MODIFIED)
   - Added test: `'deduplicates conversations when API returns duplicates'` (lines 486-564)
   - Added test: `'handles conversations with same ID but different volumes'` (lines 566-634)
   - Total tests now: 11 (was 9)
   - File size: 636 lines

## What Was Done

- **Modified `loadChatHistory()` function** to add defensive deduplication at adapter level:
  - After calling `listConversations()`, creates a Map keyed by conversation ID
  - Iterates through conversations and keeps only the one with most recent `updated_at` for each ID
  - Converts Map back to sorted array for processing
  - Added clear comment explaining why dedup is defensive (chatApi already dedups, but this is extra safety)

- **Deduplication logic** (3 key lines):
  - Line 89: Create Map for deduplication
  - Lines 90-94: Loop through conversations, keeping newest by `updated_at`
  - Line 98: Convert deduplicated Map to sorted array

- **Test coverage**:
  - Test 1 (`deduplicates conversations when API returns duplicates`): Tests same conversation ID appearing 3 times with different timestamps, verifies only newest is kept
  - Test 2 (`handles conversations with same ID but different volumes`): Tests same ID from home:// and cloud:// volumes, verifies dedup works across volumes

## Test Results

### chatHistoryAdapter tests (all 11 passing)
```
✓ returns empty array when no conversations exist
✓ groups conversations by date
✓ sorts conversations by updated_at (newest first)
✓ includes volume status badge
✓ truncates long conversation titles
✓ uses conversation ID for label when title is null
✓ returns empty array on error
✓ includes metadata for conversation nodes
✓ handles conversations with zero messages
✓ deduplicates conversations when API returns duplicates
✓ handles conversations with same ID but different volumes

Test Files: 1 passed (1)
Tests: 11 passed (11)
Duration: 16.15s
```

### Deduplication test specifics
- **Test 1**: Creates 3 conversations with same ID (`conv-1773866695314-abc123`), different `updated_at`:
  - Older Version: updated_at = now - 5000ms, message_count = 3
  - Newer Version: updated_at = now (newest), message_count = 5
  - Middle Version: updated_at = now - 2000ms, message_count = 4
  - Result: Only 1 conversation appears, uses Newer Version (message_count = 5)

- **Test 2**: Creates 2 conversations with same ID (`conv-1773866695314-xyz789`), different volumes:
  - Home version: updated_at = now - 1000ms, message_count = 2
  - Cloud version: updated_at = now (newest), message_count = 4
  - Result: Only 1 conversation appears, uses Cloud version (message_count = 4)

## Build Verification

All tests pass with no console errors or warnings:
- No hardcoded colors (no CSS changes needed)
- No stubs or TODOs
- Function signature maintained
- Type imports correct (`Conversation` from `../../../services/terminal/types`)
- Deduplication logic is defensive (extra safety layer even though chatApi already dedups)

## Acceptance Criteria

- [x] `chatHistoryAdapter.ts` modified to add explicit deduplication by conversation ID
- [x] Deduplication prefers most recent `updated_at` when duplicates exist
- [x] New test `'deduplicates conversations when API returns duplicates'` added and passing
- [x] New test `'handles conversations with same ID but different volumes'` added and passing (bonus test)
- [x] Tests use 3 duplicate IDs (test 1) to verify dedup logic works correctly
- [x] Tests verify only 1 conversation appears in result (test 1: newest version with 5 messages)
- [x] All 9 existing tests continue to pass (now 11 total)
- [x] No console errors or warnings during test run

## Clock / Cost / Carbon

**Clock:** 00:15 (15 minutes)
- Read files and understand context: 3 min
- Write deduplication code: 2 min
- Add comprehensive tests: 5 min
- Run tests and verify: 5 min

**Cost:** Haiku 4.5 (fastest model)
- Token usage: ~18,000 tokens estimated
- Model cost efficiency: Low cost, high speed

**Carbon:** Minimal
- Single working session, no retries needed
- Quick test execution (16s for 11 tests)
- No build/deploy required

## Issues / Follow-ups

**None**

All acceptance criteria met. The deduplication is now in place at the adapter level as a defensive measure, ensuring that even if `chatApi.listConversations()` somehow returns duplicates, the tree-browser will display each conversation exactly once. The implementation:

1. **Defensive**: Doesn't rely on chatApi dedup alone
2. **Efficient**: Uses Map for O(1) lookup
3. **Correct**: Prefers most recent `updated_at` (handles cross-volume merging)
4. **Well-tested**: Two new tests verify behavior
5. **Maintainable**: Clear comment explains the "why"

The task is complete and ready for integration.
