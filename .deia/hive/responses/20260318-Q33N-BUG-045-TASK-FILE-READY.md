# Q33N Report: TASK-BUG-045 Task File Ready for Review

**Date:** 2026-03-18
**From:** Q33N (Queen Coordinator)
**To:** Q33NR (Regent)
**Re:** BUG-045 Queue Runner Crash Resilience + Modularization

---

## Status: TASK FILE READY FOR REVIEW

I have written the comprehensive task file as approved in your decision memo.

**Task File Location:**
`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-18-TASK-BUG-045-queue-crash-resilience.md`

---

## Task File Summary

### Single Comprehensive Task Approach
As approved, this is ONE task combining crash resilience + modularization (interdependent work).

### Deliverables Overview

**Part 1: Crash Resilience (Error Handling)**
1. Watch loop wrapped in try/except (preserves KeyboardInterrupt)
2. `_handle_spec_result()` wrapped for per-spec isolation
3. `_safe_move_spec()` helper for all file moves
4. Fix cycle functions (`fix_cycle.py`) return `None` on errors
5. Verification that `spec_processor.py` has error handling
6. All errors logged with `[QUEUE] ERROR:` and traceback

**Part 2: Modularization (File Size Compliance)**
1. Extract pool processing → `queue_pool.py` (~260 lines)
2. Extract batch processing → `queue_batch.py` (~150 lines)
3. Extract utilities → `queue_util.py` (~100 lines)
4. Update imports in `run_queue.py`
5. Verify `run_queue.py` drops to ≤500 lines (~400 expected)
6. Verify all new modules ≤500 lines

### Test Requirements
- Minimum 15 new tests in `test_crash_resilience.py`
- All 116 existing queue tests must still pass
- Total: 131 passing tests expected

### Constraints Met
- ✅ TDD approach required
- ✅ No file over 500 lines (explicit file size targets table included)
- ✅ No logic changes (modularization is mechanical code movement only)
- ✅ No stubs (every function fully implemented)
- ✅ auto_commit.py off-limits (already has error handling lines 81-130)
- ✅ Preserve KeyboardInterrupt (catch Exception, not BaseException)

### Model Assignment
**Sonnet** — Justified by complexity of:
- Refactoring 1,219 lines into 4 files
- Adding comprehensive error handling throughout
- Ensuring zero logic changes during refactoring
- Careful coordination of imports across new modules

---

## Quality Checklist (Completed)

I verified the task file includes:

- [x] Deliverables are concrete and measurable
- [x] File paths are absolute (Windows format: `C:\Users\davee\...`)
- [x] Test requirements specify exact scenarios (15 tests listed)
- [x] CSS requirement not applicable (Python code only)
- [x] File size targets table with before/after line counts
- [x] No stubs allowed (explicit in constraints)
- [x] Response file template included (all 8 sections)
- [x] Edge cases enumerated (7 scenarios)
- [x] Acceptance criteria clear and testable
- [x] Smoke test commands provided

---

## Key Highlights for Your Review

### 1. File Size Compliance Table
I included a table showing current vs. target line counts for all affected files. This makes it crystal clear that `run_queue.py` at 1,219 lines VIOLATES Rule #4 and MUST be fixed.

### 2. Two-Part Deliverables Structure
The deliverables are split into Part 1 (Crash Resilience) and Part 2 (Modularization), making it clear these are interconnected but distinct concerns.

### 3. Explicit "Off-Limits" Callout
I explicitly state that `auto_commit.py` is NOT to be modified since it already has comprehensive error handling (lines 81-130). This prevents wasted effort.

### 4. Error Logging Pattern
I provided a concrete code example for the error logging pattern to ensure consistency.

### 5. Import Strategy
I included guidance on using relative imports to prevent circular dependencies.

### 6. Test Requirements Detail
Instead of just "write tests," I listed the exact 15 test scenarios covering all resilience areas.

---

## Recommended Review Focus

When reviewing, please verify:

1. **Completeness:** Does the task cover all 5 areas from your briefing?
   - Watch loop ✅
   - Result handling ✅
   - File moves ✅
   - Fix cycle ✅
   - spec_processor verification ✅

2. **Modularization Plan:** Is the split logical?
   - Pool processing → separate file ✅
   - Batch processing → separate file ✅
   - Utilities → separate file ✅
   - run_queue.py keeps orchestration ✅

3. **Test Coverage:** Are all edge cases covered?
   - I enumerated 7 edge case scenarios
   - 15 specific test requirements
   - Explicit requirement for existing tests to still pass

4. **Constraints Clarity:** Are the rules unambiguous?
   - No file over 500 lines (with table) ✅
   - No logic changes (repeated 3x) ✅
   - TDD required ✅
   - No stubs ✅

---

## Dispatch Readiness

If approved, this task is ready for immediate dispatch:

```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-18-TASK-BUG-045-queue-crash-resilience.md \
  --model sonnet \
  --role bee \
  --inject-boot
```

No additional task breakdown required. This is a single comprehensive bee assignment.

---

## Awaiting Your Decision

Please review the task file and either:
1. **APPROVE** → I will dispatch the bee immediately
2. **REQUEST CORRECTIONS** → Specify changes needed, I will revise and re-submit

---

**Q33N Standing By**
