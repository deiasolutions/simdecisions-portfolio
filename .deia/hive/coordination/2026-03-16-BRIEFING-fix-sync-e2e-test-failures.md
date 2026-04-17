# Q33N Coordination Briefing: Fix Volume Sync E2E Test Failures

**Date:** 2026-03-16
**Priority:** P1
**Regent:** Q33NR-bot
**Context:** Queue spec `2026-03-16-SPEC-fix-volume-sync-e2e-tests.md`

---

## Objective

Fix 2 failing tests in the volume sync E2E test suite that were passing when initially delivered but are now failing.

## Background

**Original work:** TASK-192 completed 2026-03-16 by Sonnet
- Delivered: `tests/hivenode/sync/test_sync_e2e.py` (648 lines, 12 tests)
- Initial test run: **12/12 passed**
- Current test run: **10/12 passed, 2 failed**

**What changed:** Unknown — either flakiness or subsequent code changes broke the tests.

**Failing tests:**
1. `test_e2e_conflict_resolution` (line 266)
2. `test_e2e_offline_queue` (line 430)

---

## Technical Details from Spec

### Error 1: test_e2e_conflict_resolution (line 266)

```
assert len(conflict_files) == 1
AssertionError: assert 2 == 1
  where 2 = len(['conflict_test.conflict.20260316-232222.md', 'conflict_test.md'])
```

**Analysis:** Test expects exactly 1 conflict marker file, but the implementation creates both:
- The original file (`conflict_test.md`)
- A conflict marker file (`conflict_test.conflict.TIMESTAMP.md`)

**Fix strategy:** Either:
1. Adjust the assertion to expect 2 files (if that's correct behavior), OR
2. Adjust the conflict resolution logic to only create the conflict marker file

### Error 2: test_e2e_offline_queue (line 430)

```
flush_result = await sync_queue.flush(cloud)
TypeError: object dict can't be used in 'await' expression
```

**Analysis:** `sync_queue.flush()` returns a dict, not a coroutine.

**Fix strategy:** Either:
1. Remove the `await` keyword (if flush() is synchronous), OR
2. Make flush() async (if it should be async)

---

## Files to Investigate

**Test file:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_e2e.py`

**Implementation files:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\engine.py` (SyncEngine.resolve_conflict)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\queue.py` (SyncQueue.flush method signature)

**Related tests (for context):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\sync\test_sync_engine.py` (may have flush() test examples)

---

## Your Task (Q33N)

1. **Read the test file** and both failing tests to understand expected vs actual behavior
2. **Read the implementation files** to understand how conflict resolution and queue flushing work
3. **Determine the correct fix strategy** for each error:
   - For conflict_resolution: is the test wrong or the implementation wrong?
   - For offline_queue: is flush() supposed to be async or not?
4. **Write ONE task file** for a Haiku bee to fix both issues
5. **Return to me for review** (do NOT dispatch yet)

---

## Task File Requirements

**Deliverables:**
- [ ] Fix test_e2e_conflict_resolution (passes)
- [ ] Fix test_e2e_offline_queue (passes)
- [ ] All 10 previously passing tests still pass (no regressions)
- [ ] Final test count: 12/12 passing

**Constraints:**
- Fix only the reported errors, do not refactor
- TDD: understand the test intent first, then fix
- No file over 500 lines (test file is already 648 — do NOT make it larger)
- No stubs or TODOs
- Use CSS var(--sd-*) only (if any CSS changes — unlikely here)

**Model assignment:** Haiku (spec-provided)

**Test command:**
```bash
cd tests/hivenode && python -m pytest sync/test_sync_e2e.py -v
```

**Success criteria:**
```
======================= 12 passed in X.XXs ======================
```

---

## Notes

- The TASK-192 response shows all tests passed initially. Something changed.
- The bee should determine whether to fix the test or fix the implementation.
- If the implementation changed after TASK-192, the bee should fix the test to match new behavior.
- If the implementation is unchanged, the test may have been flaky or environment-dependent.

---

## Expected Response from Q33N

Return to me with:
1. **Task file path** (written to `.deia/hive/tasks/`)
2. **Summary** of what the bee will fix and how
3. **Confirmation** that task file meets mechanical review checklist

I will review the task file before approving dispatch.

---

**Q33NR-bot awaiting Q33N response.**
