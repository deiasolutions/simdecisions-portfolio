# BRIEFING: BUG-045 Queue Runner Crash Resilience

**Date:** 2026-03-18
**From:** Q33NR
**To:** Q33N
**Priority:** P0
**Model Assignment:** sonnet

---

## Objective

Make the queue runner's watch loop completely crash-proof. It must catch ALL exceptions, log them, and continue running. The queue runner should never exit unless explicitly killed.

## Context from Q88N

The queue runner (`run_queue.py`) keeps dying from unhandled exceptions during watch mode. Exit code 127 (command not found), file path errors, and other transient failures kill the entire process. This means specs stop being processed and the build pipeline stalls silently.

## What Needs to Happen

### 1. Top-level try/except in the watch loop
The watch loop (the `while True` polling loop inside `run_queue()`) must wrap every tick in a broad try/except. Catch `Exception` (not `BaseException` — let KeyboardInterrupt through). Log the traceback. Continue to next tick.

### 2. Per-spec try/except in result handling
`_process_result()` is now `_handle_spec_result()`. It handles individual spec results (CLEAN, TIMEOUT, NEEDS_DAVE). If one spec's result processing throws, it must not kill the entire queue. Catch, log, move the spec to `_needs_review/` with error details, continue.

### 3. Auto-commit failure isolation
`auto_commit_bee_output()` runs git commands. If git fails (exit code 127, lock file, etc.), it must not propagate. Wrap in try/except, log the failure, continue without committing.

### 4. Fix cycle failure isolation
`generate_fix_spec()` and `generate_q33n_fix_spec()` write files. If file I/O fails, catch it, log it, move original spec to `_needs_review/`, continue.

### 5. _active/ directory operations
All file moves (queue → _active, _active → _done, _active → _needs_review) must handle FileNotFoundError, PermissionError, and other OS errors gracefully. Log and continue.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` (the entire file — understand the watch loop, run_queue(), _handle_spec_result(), auto_commit_bee_output())
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\fix_cycle.py` (generate_fix_spec, generate_q33n_fix_spec)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py` (process_spec — where dispatch happens)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\auto_commit.py` (auto_commit_bee_output)

## Files to Modify

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` — add crash resilience at all levels
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\fix_cycle.py` — wrap file I/O in try/except
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py` — wrap dispatch subprocess in try/except (if not already)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\auto_commit.py` — wrap git operations in try/except

## Deliverables

- [ ] Watch loop never crashes from unhandled exceptions
- [ ] Individual spec failures don't kill the queue
- [ ] Auto-commit failures don't kill the queue
- [ ] Fix cycle file I/O failures don't kill the queue
- [ ] File move failures don't kill the queue
- [ ] All errors logged with `[QUEUE] ERROR:` prefix and traceback
- [ ] Tests for crash resilience (mock exceptions, verify queue continues)

## Acceptance Criteria

- [ ] `python -m pytest .deia/hive/scripts/queue/tests/ -v` — all pass
- [ ] Queue runner survives: FileNotFoundError, PermissionError, subprocess failures, malformed spec files
- [ ] KeyboardInterrupt still stops the queue cleanly

## Smoke Test

```bash
python -m pytest .deia/hive/scripts/queue/tests/ -v
```

## Constraints

- No file over 500 lines
- Do not change queue logic or dispatch behavior
- Only add error handling and resilience
- Log everything — silent failures are worse than crashes
- All file paths must be absolute in task files
- TDD: Write tests first, then implementation
- No stubs — every function fully implemented

## Q33N Instructions

1. Read all files listed in "Files to Read First"
2. Write task files breaking this work into bee-sized units (one task per file typically)
3. Each task must include:
   - Objective (one sentence)
   - Context (what the bee needs to know)
   - Files to Read First (absolute paths)
   - Deliverables (concrete, testable outputs)
   - Test Requirements (TDD, edge cases, pass criteria)
   - Constraints (500 line limit, no stubs, etc.)
   - Response Requirements (all 8 sections mandatory)
4. Return task files to Q33NR for review
5. DO NOT dispatch bees until Q33NR approves
6. After Q33NR approval, dispatch bees and monitor results
7. Report completion to Q33NR

## Expected Task Breakdown

Suggested task structure (Q33N may adjust based on code review):

- **TASK-BUG-045-A**: Wrap watch loop in exception handler (run_queue.py main loop)
- **TASK-BUG-045-B**: Wrap _handle_spec_result() in exception handler
- **TASK-BUG-045-C**: Wrap auto_commit_bee_output() in exception handler (auto_commit.py)
- **TASK-BUG-045-D**: Wrap fix cycle file I/O in exception handlers (fix_cycle.py)
- **TASK-BUG-045-E**: Wrap file move operations in exception handlers (all move/rename calls)
- **TASK-BUG-045-F**: Write tests for crash resilience (mock exceptions, verify queue continues)

---

**Q33NR Note:** This is a critical infrastructure fix. The queue runner is the automation backbone. It MUST be bulletproof. No shortcuts, no "good enough for now." Every exception must be caught and logged, and the queue must continue running.
