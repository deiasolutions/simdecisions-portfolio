# TASK-BUG-045: Queue Runner Crash Resilience + Modularization

## Objective

Make the queue runner crash-proof by wrapping all exception-prone code in try/except blocks, AND modularize run_queue.py (currently 1,219 lines) to comply with BOOT.md Rule #4 (500-line limit, hard max 1,000).

## Context

The queue runner (`run_queue.py`) is the automation backbone of the build pipeline. It currently crashes from unhandled exceptions (exit code 127, file path errors, OS errors) and is 2.4x over the 500-line modularization threshold (1.2x over hard limit of 1,000 lines).

**Current State:**
- `run_queue.py`: 1,219 lines (VIOLATES Rule #4)
- Watch loop can crash from any unhandled exception
- Individual spec failures can kill entire queue
- File I/O errors propagate upward
- `auto_commit.py` ALREADY HAS comprehensive error handling (lines 81-130) — no changes needed there

**Required Outcome:**
1. Queue runner never crashes from unhandled exceptions (except KeyboardInterrupt)
2. All files comply with 500-line rule
3. All errors logged with traceback
4. Queue continues processing after any single-spec failure

## Files to Read First

### Core Queue Files (read in order):
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` (1,219 lines — entire file)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py` (509 lines)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\fix_cycle.py` (191 lines)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\auto_commit.py` (137 lines — has error handling, reference only)
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\scope_detector.py` (referenced by run_queue)
6. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_parser.py` (referenced by run_queue)

### Test Files (for patterns):
7. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_run_queue.py` (existing tests — must still pass)
8. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\BOOT.md` (Rule #4: No file over 500 lines)

## Deliverables

### Part 1: Crash Resilience (Error Handling)

- [ ] **Watch loop resilience** — Wrap the main `while True` loop in `run_queue()` with try/except that catches `Exception` (NOT `BaseException` — preserve KeyboardInterrupt passthrough). Log errors with `[QUEUE] ERROR:` prefix and full traceback. Continue to next tick.

- [ ] **Result handling resilience** — Wrap all code in `_handle_spec_result()` in try/except. If processing one spec's result fails, log error, move spec to `_needs_review/` with error details, continue.

- [ ] **File move resilience** — Create `_safe_move_spec()` helper function that wraps `Path.rename()` / `shutil.move()` in try/except. Handle `FileNotFoundError`, `PermissionError`, `OSError`. Log failures. Return `True` on success, `False` on failure. Use this helper in ALL places where specs are moved between directories.

- [ ] **Fix cycle resilience** — In `fix_cycle.py`, wrap all `write_text()` calls in try/except. Return `None` on failure instead of raising. Callers must check for `None` and handle gracefully (move original spec to `_needs_review/`, log error, continue).

- [ ] **spec_processor verification** — Verify that `spec_processor.py` already has error handling around subprocess dispatch calls (lines 472-480, 496-505 per proposal). Add any missing wrappers if found.

- [ ] **All errors logged** — Every caught exception must be logged with:
  - `[QUEUE] ERROR:` prefix
  - Full exception traceback via `traceback.format_exc()`
  - Spec ID if applicable
  - Timestamp

### Part 2: Modularization (File Size Compliance)

- [ ] **Extract queue pool processing** — Move `_process_queue_pool()` and related helper functions to new file `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\queue_pool.py` (~260 lines estimated)

- [ ] **Extract queue batch processing** — Move `_process_queue_batch()` and related helper functions to new file `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\queue_batch.py` (~150 lines estimated)

- [ ] **Extract utility functions** — Move utility functions (`_safe_move_spec()`, `_get_done_ids()`, file path helpers, etc.) to new file `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\queue_util.py`

- [ ] **Update imports in run_queue.py** — Add relative imports for new modules. Verify no circular dependencies.

- [ ] **Verify run_queue.py is now ≤500 lines** — After extraction, run_queue.py should be ~400 lines (main entry point, orchestration, watch loop). Count lines and verify compliance.

- [ ] **Verify new modules are ≤500 lines each** — Check line counts for `queue_pool.py`, `queue_batch.py`, `queue_util.py`. All must be under 500 lines.

- [ ] **No logic changes** — Modularization is purely mechanical code movement. Do NOT change behavior. Only move functions to new files and update imports.

## Test Requirements

### TDD Approach
- [ ] **Write tests FIRST** — Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_crash_resilience.py` before implementing changes
- [ ] **Minimum 15 tests** covering:

#### Watch Loop Tests (3 tests):
1. Test watch loop continues after generic exception in tick
2. Test watch loop preserves KeyboardInterrupt (raises, not catches)
3. Test watch loop logs exception with traceback

#### File Move Tests (4 tests):
4. Test `_safe_move_spec()` handles `FileNotFoundError`
5. Test `_safe_move_spec()` handles `PermissionError`
6. Test `_safe_move_spec()` returns `True` on success
7. Test `_safe_move_spec()` returns `False` on failure

#### Result Handling Tests (3 tests):
8. Test `_handle_spec_result()` continues after exception
9. Test spec moved to `_needs_review/` on error
10. Test error details logged with spec ID

#### Fix Cycle Tests (3 tests):
11. Test `generate_fix_spec()` returns `None` on file I/O error
12. Test `generate_q33n_fix_spec()` returns `None` on file I/O error
13. Test caller handles `None` return gracefully

#### Modularization Tests (2 tests):
14. Test all modularized functions import correctly
15. Test existing queue tests still pass after modularization

### All Tests Must Pass:
- [ ] `python -m pytest .deia/hive/scripts/queue/tests/ -v` — all existing + new tests pass
- [ ] No regressions in existing 116 queue tests

## Edge Cases to Handle

1. **File system race conditions** — Spec file deleted between queue load and processing
2. **Concurrent file access** — Another process locks a file during move
3. **Disk full** — File write operations fail with OSError
4. **Malformed spec files** — YAML parse errors (should already be handled by spec_parser)
5. **Git command failures** — Exit code 127, lock files (already handled by auto_commit.py)
6. **Subprocess failures** — Claude Code crashes or hangs (handled by timeout in spec_processor)
7. **Network failures** — Hivenode down during slot reservation checks (already uses try/except)

## Constraints

- **No file over 500 lines** — This is MANDATORY. After modularization, verify ALL files comply.
- **No logic changes** — Only add error handling and move code. Do NOT change queue behavior.
- **No stubs** — Every function fully implemented. No `TODO`, no placeholder returns.
- **Preserve KeyboardInterrupt** — Do NOT catch `BaseException`. Catch `Exception` only.
- **Log everything** — Silent failures are worse than crashes. Every error gets a traceback log.
- **TDD** — Tests written FIRST, then implementation.
- **auto_commit.py is off-limits** — It already has comprehensive error handling (lines 81-130). Do NOT modify it.

## File Size Targets (After Modularization)

| File | Current | Target | Status |
|------|---------|--------|--------|
| `run_queue.py` | 1,219 | ≤500 | ❌ MUST FIX |
| `queue_pool.py` | 0 (new) | ~260 | ✅ NEW |
| `queue_batch.py` | 0 (new) | ~150 | ✅ NEW |
| `queue_util.py` | 0 (new) | ~100 | ✅ NEW |
| `spec_processor.py` | 509 | 509 | ⚠️ CLOSE (verify no growth) |
| `fix_cycle.py` | 191 | 191 | ✅ OK |
| `auto_commit.py` | 137 | 137 | ✅ OK (no changes) |

## Acceptance Criteria

- [ ] Watch loop never crashes from unhandled exceptions (except KeyboardInterrupt)
- [ ] Individual spec failures isolated (don't kill queue)
- [ ] All file moves use `_safe_move_spec()` and handle errors
- [ ] Fix cycle functions return `None` on failure, callers handle it
- [ ] All errors logged with `[QUEUE] ERROR:` prefix and traceback
- [ ] `run_queue.py` is ≤500 lines
- [ ] All new modules are ≤500 lines
- [ ] `python -m pytest .deia/hive/scripts/queue/tests/ -v` — all pass (116 existing + 15 new = 131 total)
- [ ] No regressions in existing queue behavior
- [ ] No stubs shipped (every function complete)
- [ ] Test coverage includes all resilience scenarios

## Smoke Test

```bash
# Run all queue tests
python -m pytest .deia/hive/scripts/queue/tests/ -v

# Verify file sizes
wc -l .deia/hive/scripts/queue/run_queue.py      # must be ≤500
wc -l .deia/hive/scripts/queue/queue_pool.py     # must be ≤500
wc -l .deia/hive/scripts/queue/queue_batch.py    # must be ≤500
wc -l .deia/hive/scripts/queue/queue_util.py     # must be ≤500
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-BUG-045-RESPONSE.md`

The response MUST contain these 8 sections:

### 1. Header
- Task ID: TASK-BUG-045
- Title: Queue Runner Crash Resilience + Modularization
- Status: COMPLETE | FAILED (with reason)
- Model: Sonnet
- Date: 2026-03-18

### 2. Files Modified
List EVERY file created/modified/deleted with absolute paths:
- Created: `queue_pool.py`, `queue_batch.py`, `queue_util.py`, `tests/test_crash_resilience.py`
- Modified: `run_queue.py`, `fix_cycle.py`, etc.

### 3. What Was Done
Bullet list of concrete changes (not intent):
- Added try/except wrapper to watch loop in run_queue() lines X-Y
- Created _safe_move_spec() helper in queue_util.py
- Moved _process_queue_pool() to queue_pool.py (260 lines)
- etc.

### 4. Test Results
- Test files run: `test_crash_resilience.py`, `test_run_queue.py`, etc.
- Pass/fail counts: 131 passed (116 existing + 15 new)
- Specific test output

### 5. Build Verification
- Did tests pass? Include pytest summary line.
- File size verification: `run_queue.py: 412 lines`, etc.

### 6. Acceptance Criteria
Copy from task above, mark `[x]` done or `[ ]` not done with explanation.

### 7. Clock / Cost / Carbon
- **Clock:** wall time (e.g., 45 minutes)
- **Cost:** estimated USD (sonnet pricing)
- **Carbon:** estimated CO2e

### 8. Issues / Follow-ups
- Any errors encountered
- Edge cases discovered
- Recommended next tasks
- Any regressions found

DO NOT skip any section.

---

## Model Assignment

**sonnet** — Complexity of refactoring 1,219 lines + adding comprehensive error handling + ensuring no logic changes requires careful analysis.

---

## Context for Modularization

The functions to move are grouped by responsibility. Read run_queue.py and identify:

**Pool processing group (~260 lines):**
- `_process_queue_pool()` — main pool orchestrator
- Related helpers called only by pool processing

**Batch processing group (~150 lines):**
- `_process_queue_batch()` — main batch orchestrator
- Related helpers called only by batch processing

**Utility group (~100 lines):**
- `_get_done_ids()` — utility
- `_safe_move_spec()` — NEW utility (you create this)
- Other small helpers used across multiple contexts

**Keep in run_queue.py (~400 lines):**
- `main()` — CLI entry point
- `run_queue()` — main watch loop orchestrator
- `_handle_spec_result()` — result dispatcher
- Top-level imports and constants
- Any functions that coordinate between pool/batch/util

---

## Additional Notes

1. **Import Strategy:** Use relative imports in the new modules:
   ```python
   # In queue_pool.py
   from .queue_util import _safe_move_spec
   from .spec_processor import process_batch
   ```

2. **Error Logging Pattern:** Use this format consistently:
   ```python
   except Exception as e:
       print(f"[QUEUE] ERROR: {context_description}")
       print(traceback.format_exc())
       # handle recovery (move spec, continue, etc.)
   ```

3. **Do NOT modify auto_commit.py** — It already has lines 81-130 with comprehensive error handling. You verified this. Leave it alone.

4. **spec_processor.py** — Verify it has error handling around subprocess calls. If already present (per proposal), do not add redundant wrappers.

5. **Function Signatures:** When moving functions, preserve signatures exactly. Do not change parameter names or return types.

6. **Testing Philosophy:** Mock exceptions at the right level. Use `unittest.mock.patch` to make functions raise errors, then verify the queue continues and logs correctly.

---

**END OF TASK FILE**
