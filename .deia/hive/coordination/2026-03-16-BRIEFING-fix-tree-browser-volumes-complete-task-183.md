# BRIEFING: Complete tree-browser-volumes by dispatching TASK-183

**Date:** 2026-03-16
**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-16-1339-SPE)
**To:** Q33N (Queen Coordinator)
**Priority:** P0 (fix cycle 1/2)

---

## Context

The original spec `2026-03-16-1032-SPEC-w2-07-tree-browser-volumes` was reported as a "timeout" failure, but investigation shows it actually **completed successfully** — just without the final E2E integration test (TASK-183).

### What Actually Happened

The queue runner reported:
```
Pool exception: Command '...' timed out after 10 seconds
```

This error message is misleading. What really happened:
1. ✅ Q33N was dispatched and created 4 task files (TASK-180, 181, 182, 183)
2. ✅ TASK-180 (volume adapter backend wire) — **COMPLETE**, 9 tests passing
3. ✅ TASK-181 (tree-browser file-select bus) — **COMPLETE**, 33 tests passing
4. ✅ TASK-182 (text-pane file load) — **COMPLETE**, 39 tests passing
5. ❌ TASK-183 (E2E integration test) — **NEVER DISPATCHED**

The "timeout" was a watchdog heartbeat timeout during Q33N's coordination phase. But Q33N's work (creating task files) was already complete. The bees executed successfully. Only TASK-183 was never dispatched.

### Root Cause

TASK-183 was the final task in a **sequential dispatch chain**:
- Batch 1 (parallel): TASK-180 + TASK-181
- Batch 2 (sequential): TASK-182
- Batch 3 (sequential): TASK-183 ← **THIS ONE**

Q33N's coordination session was killed by the watchdog before it could dispatch Batch 3.

---

## Objective

**Complete the tree-browser-volumes work by dispatching TASK-183.**

This is NOT a fix — it's a completion task. All implementation is done. We just need the integration test.

---

## Your Task

### Step 1: Verify Current State

Read these response files to confirm status:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-180-VOLUME-ADAPTER-RESPONSE.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-181-RESPONSE.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-182-RESPONSE.md`

Verify:
- [x] All 3 tasks show status COMPLETE
- [x] All tests passing (9 + 33 + 39 = 81 tests minimum)
- [x] No regressions reported

### Step 2: Dispatch TASK-183

Read the task file:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-16-TASK-183-volume-integration-e2e-test.md`

Dispatch the bee:
```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-16-TASK-183-volume-integration-e2e-test.md \
  --model sonnet \
  --role bee \
  --inject-boot \
  --timeout 1200
```

**Note:** Use Sonnet for this task (it requires integration thinking).

### Step 3: Wait for Completion

TASK-183 should complete in ~30-45 minutes. Wait for the response file:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-183-RESPONSE.md`

### Step 4: Write Completion Report

When TASK-183 completes, write a completion report to:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-Q33N-tree-browser-volumes-COMPLETION-REPORT.md`

Include:
- Summary of all 4 tasks (180, 181, 182, 183)
- Total tests added (should be ~87+ new tests)
- Verification that smoke test passes: `cd browser && npx vitest run src/primitives/tree-browser/`
- Map to original spec acceptance criteria:
  - [x] home:// lists real directories → TASK-180
  - [x] File contents load in text-pane → TASK-182
  - [x] File metadata (size, date) displayed → TASK-180
  - [x] Tests written and passing → TASK-183 verifies

### Step 5: Return to Q33NR

Report completion status. If TASK-183 passes, this spec is CLEAN and ready for archive.

---

## Constraints

- **Do NOT rewrite any existing task files.** They are already correct.
- **Do NOT re-dispatch TASK-180, 181, or 182.** They are complete.
- **Only dispatch TASK-183.**
- **Do NOT create new task files.** Use the existing TASK-183 file as-is.
- **Model assignment:** sonnet (for TASK-183)
- **Max timeout:** 1200 seconds (20 minutes) — E2E tests can be slow

---

## Success Criteria

When you return to Q33NR, confirm:
- [x] TASK-183 dispatched successfully
- [x] TASK-183 response file written (all 8 sections)
- [x] TASK-183 tests passing (minimum 6 integration tests)
- [x] No regressions on existing tree-browser tests
- [x] Smoke test passes
- [x] Completion report written

---

## Expected Files Modified by TASK-183

TASK-183 creates **new test files only**. No implementation files should be modified (implementation is already complete).

Expected new files:
- Backend test: `tests/hivenode/routes/test_storage_integration.py` (or similar)
- Frontend test: Additional test cases in existing test files or new integration test file

---

## Notes for Q33NR

This is a **completion task**, not a fix cycle. The original spec succeeded — we're just finishing the last step.

After TASK-183 completes:
- Move the fix spec (`2026-03-16-1339-SPEC-fix-w2-07-tree-browser-volumes.md`) to `_done/`
- Move the original spec (`2026-03-16-1032-SPEC-w2-07-tree-browser-volumes.md`) remains in `_done/` (already there)
- Archive all 4 task files (TASK-180, 181, 182, 183) to `.deia/hive/tasks/_archive/`
- Run inventory commands to register the feature
- Mark spec as CLEAN in session events

---

**Q33NR (REGENT-QUEUE-TEMP-2026-03-16-1339-SPE)**
**Briefing written: 2026-03-16**
