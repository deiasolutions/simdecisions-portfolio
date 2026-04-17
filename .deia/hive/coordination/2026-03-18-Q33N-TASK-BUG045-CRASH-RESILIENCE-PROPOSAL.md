# Q33N Task Breakdown Proposal: BUG-045 Queue Runner Crash Resilience

**Date:** 2026-03-18
**From:** Q33N (Queen Coordinator)
**To:** Q33NR (Regent)
**Briefing:** 2026-03-18-BRIEFING-BUG-045-queue-runner-crash-resilience

---

## Summary

After reviewing the briefing and reading all four core files (run_queue.py, fix_cycle.py, spec_processor.py, auto_commit.py), I propose a **single task** approach instead of multiple task files. Here's why:

**Current state:**
- `run_queue.py`: 1,220 lines (already at 2.4x the 500-line rule, hard limit at 1,000 is 1.2x exceeded)
- Good news: **auto_commit.py already has comprehensive error handling** (lines 81-130) — all git operations wrapped in try/except
- The briefing requests adding crash resilience to 5 areas across 4 files

**The problem:**
Adding error handling wrappers across all these locations will push run_queue.py even larger. We're constrained by BOOT.md Rule #4: "No file over 500 lines. Modularize at 500. Hard limit: 1,000."

**The better approach:**
1. **Single comprehensive task** to add crash resilience across all files
2. **As part of this work**, refactor run_queue.py to split it into modules (move functions to new files)
3. Result: crash resilience AND file size compliance

---

## Proposed Task Breakdown

### TASK-BUG-045: Queue Runner Crash Resilience + Modularization

**Objective:**
Make the queue runner crash-proof by wrapping all exception-prone code in try/except blocks, AND modularize run_queue.py to comply with the 500-line rule.

**Deliverables:**

1. **run_queue.py modifications:**
   - Wrap watch loop in try/except (preserve KeyboardInterrupt passthrough)
   - Create `_safe_move_spec()` helper function for all file moves
   - Use `_safe_move_spec()` in `_handle_spec_result()` and elsewhere
   - Wrap all error-prone sections with detailed error logging

2. **fix_cycle.py modifications:**
   - Wrap `write_text()` calls in try/except
   - Return None on failure instead of raising
   - Callers check for None and handle gracefully

3. **spec_processor.py modifications:**
   - Already has good error handling in `process_batch()` (lines 472-480, 496-505)
   - Verify subprocess calls are wrapped (they appear to be)
   - Add any missing wrappers if found

4. **auto_commit.py status:**
   - **ALREADY COMPLETE** — lines 81-130 show comprehensive try/except around git operations
   - No changes needed here

5. **Modularization (NEW — to stay under file limits):**
   - Extract functions from run_queue.py into new modules:
     - `queue_pool.py` — `_process_queue_pool()` + helpers (~260 lines)
     - `queue_batch.py` — `_process_queue_batch()` + helpers (~150 lines)
     - `queue_util.py` — utility functions like `_safe_move_spec()`, `_get_done_ids()`, etc.
   - Result: run_queue.py drops to ~400 lines (main entry point + orchestration)

6. **Tests:**
   - Test file: `.deia/hive/scripts/queue/tests/test_crash_resilience.py`
   - Minimum 15 tests covering:
     - Watch loop exception handling (preserve KeyboardInterrupt)
     - File move failures in `_handle_spec_result()`
     - Fix spec generation failures (fix_cycle.py returns None)
     - Git command failures (already handled by auto_commit.py)
     - `_safe_move_spec()` error cases
     - Modularized imports work correctly

**Constraints:**
- No file over 500 lines after modularization
- All errors logged with `[QUEUE] ERROR:` prefix and traceback
- Existing queue tests must still pass
- No logic changes — only error handling and code movement

**Model Assignment:**
sonnet (complexity of refactoring + error handling requires careful work)

---

## Why Single Task Instead of Multiple?

1. **Dependency:** Modularization affects where error handling goes. Doing them separately creates merge conflicts.
2. **Context:** A single bee needs to see the full picture to split run_queue.py correctly.
3. **Testing:** Tests for crash resilience need to import the modularized functions.
4. **Efficiency:** One bee session, one review cycle, one commit.

---

## Files to Review (for the bee)

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` (1,220 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\fix_cycle.py` (191 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py` (509 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\auto_commit.py` (137 lines — ALREADY HAS ERROR HANDLING)

---

## Risk Assessment

**Low risk:**
- Error handling is additive (doesn't change logic)
- Modularization is mechanical (move functions to new files, update imports)
- auto_commit.py already has the resilience we need (no work required there)

**Test coverage:**
- Existing queue tests (116 passing) ensure no regressions
- New tests verify crash resilience works

---

## Q33NR Review Points

Please confirm:
1. ✅ Single task approach (crash resilience + modularization together)
2. ✅ Modularization is necessary to comply with Rule #4 (no file over 500 lines)
3. ✅ auto_commit.py already has error handling — no changes needed
4. ✅ Sonnet model assignment (complexity justifies it)

If approved, I'll write the full task file and return it for your review before dispatch.

---

**Status:** AWAITING Q33NR APPROVAL
