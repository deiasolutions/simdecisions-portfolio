# BRIEFING: BUG-045 — Queue Runner Crash Resilience

**Date:** 2026-03-18
**From:** Q33NR (Regent)
**To:** Q33N (Queen Coordinator)
**Spec:** SPEC-TASK-BUG045-queue-runner-crash-resilience
**Priority:** P0
**Model Assignment:** sonnet

---

## Objective

Make the queue runner completely crash-proof. Wrap all exception-prone code in try/except blocks so the queue runner survives transient failures (file I/O errors, git failures, subprocess crashes, malformed specs) and continues processing.

---

## Context

The queue runner (`run_queue.py`) is currently dying from unhandled exceptions during watch mode. Exit code 127 (command not found), file path errors, and other transient failures kill the entire process. This causes specs to stop being processed and the build pipeline to stall silently.

**Key crash points identified:**
1. Watch loop — any exception in the polling tick kills the entire runner
2. `_handle_spec_result()` — file move failures, fix spec generation failures
3. `auto_commit_bee_output()` — git command failures (exit code 127, lock files)
4. `generate_fix_spec()` / `generate_q33n_fix_spec()` — file I/O failures
5. File move operations — FileNotFoundError, PermissionError during queue → _active, _active → _done, _active → _needs_review

---

## Files to Review

**Core files:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` (1,220 lines) — Main runner with watch loop, `_handle_spec_result()`, `_process_queue_pool()`, `run_queue()`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\fix_cycle.py` (191 lines) — `generate_fix_spec()`, `generate_q33n_fix_spec()`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py` (509 lines) — `process_spec()`, `process_spec_no_verify()`, `process_batch()`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\auto_commit.py` — Git operations (need to check if this exists)

---

## What Needs to Happen

### 1. Watch loop resilience (run_queue.py)

The watch loop starting at line ~1045 must wrap the entire tick in try/except. If any exception occurs during a tick (spec processing, hot-reload, cleanup), log it and continue to the next tick.

```python
while watch and session_cost < max_budget:
    try:
        # Entire tick logic here
        # ...
    except KeyboardInterrupt:
        raise  # Let Ctrl+C through
    except Exception as e:
        print(f"[QUEUE] ERROR in watch tick: {e}", flush=True)
        import traceback
        traceback.print_exc()
        # Continue to next tick
```

### 2. _handle_spec_result resilience (run_queue.py)

The `_handle_spec_result()` function (line ~291) handles file moves, fix spec generation, and result logging. Wrap each failure mode:

- **File move failures:** `spec.path.rename(dest)` can raise FileNotFoundError, PermissionError. Wrap in try/except, log, move to _needs_review if move fails.
- **Fix spec generation failures:** `generate_fix_spec()` / `generate_q33n_fix_spec()` can raise file I/O errors. Wrap, log, move original spec to _needs_review if fix spec creation fails.

### 3. auto_commit_bee_output resilience

Git commands can fail (exit code 127, lock files, network issues). Wrap all subprocess calls in try/except. If git fails, log the error and continue WITHOUT committing. **Do not crash the queue.**

### 4. Fix cycle file I/O resilience (fix_cycle.py)

`generate_fix_spec()` and `generate_q33n_fix_spec()` both call `fix_spec_path.write_text()`. Wrap in try/except. If write fails, return None and let caller handle it (move original spec to _needs_review).

### 5. File move helper function

Create a helper function `_safe_move_spec()` in run_queue.py that wraps `Path.rename()` with error handling. Use it everywhere specs are moved.

```python
def _safe_move_spec(spec_path: Path, dest_dir: Path, label: str) -> bool:
    """Move spec file to destination directory with error handling.

    Returns True on success, False on failure (logs error).
    """
    try:
        dest_dir.mkdir(exist_ok=True)
        dest = dest_dir / spec_path.name
        if spec_path.exists():
            spec_path.rename(dest)
            print(f"[QUEUE] {label}: {spec_path.name} -> {dest_dir.name}/", flush=True)
            return True
        else:
            print(f"[QUEUE] ERROR: {label} failed — {spec_path.name} does not exist", flush=True)
            return False
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"[QUEUE] ERROR: {label} failed for {spec_path.name}: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return False
```

---

## Deliverables

1. **run_queue.py modifications:**
   - Watch loop wrapped in try/except (preserves KeyboardInterrupt)
   - `_handle_spec_result()` wraps all file operations in try/except
   - `_safe_move_spec()` helper function added
   - All file moves use `_safe_move_spec()`

2. **fix_cycle.py modifications:**
   - `generate_fix_spec()` wraps `write_text()` in try/except, returns None on failure
   - `generate_q33n_fix_spec()` wraps `write_text()` in try/except, returns None on failure
   - Callers check for None return and handle gracefully

3. **spec_processor.py modifications (if needed):**
   - Wrap dispatch subprocess calls in try/except (may already be handled)

4. **auto_commit.py modifications:**
   - Wrap all git subprocess calls in try/except
   - Log failures, continue without crashing

5. **Tests:**
   - Mock exceptions in `_handle_spec_result()` and verify queue continues
   - Mock file I/O errors in fix spec generation and verify fallback to _needs_review
   - Mock git failures in auto_commit and verify queue continues
   - Test KeyboardInterrupt still works (Ctrl+C stops queue cleanly)

---

## Test Requirements

- All existing queue tests must pass
- New tests for crash resilience (mock exceptions, verify queue continues)
- Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_crash_resilience.py`
- Minimum 10 tests covering:
  - Watch loop exception handling
  - File move failures
  - Fix spec generation failures
  - Git command failures
  - KeyboardInterrupt passthrough

---

## Acceptance Criteria

- [ ] Watch loop never crashes from unhandled exceptions
- [ ] Individual spec failures don't kill the queue
- [ ] Auto-commit failures don't kill the queue
- [ ] Fix cycle file I/O failures don't kill the queue
- [ ] File move failures don't kill the queue
- [ ] All errors logged with `[QUEUE] ERROR:` prefix and traceback
- [ ] Tests for crash resilience pass
- [ ] KeyboardInterrupt still stops the queue cleanly
- [ ] All existing queue tests still pass

---

## Constraints

- No file over 500 lines (run_queue.py is already 1,220 — do NOT add bulk, only error handling)
- Do not change queue logic or dispatch behavior
- Only add error handling and resilience
- Log everything — silent failures are worse than crashes
- Use Python's `traceback.print_exc()` for detailed error logs

---

## Model Assignment

sonnet — This requires careful error handling across multiple files and understanding of edge cases.

---

## Next Steps

1. Q33N reads this briefing
2. Q33N reads the three core files (run_queue.py, fix_cycle.py, spec_processor.py)
3. Q33N checks if auto_commit.py exists and reads it
4. Q33N writes task files for implementing crash resilience
5. Q33N returns task files to Q33NR for review
6. After Q33NR approval, Q33N dispatches bees
