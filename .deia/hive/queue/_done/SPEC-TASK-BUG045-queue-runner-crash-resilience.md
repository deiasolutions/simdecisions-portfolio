# BUG-045: Queue runner must never crash

## Priority
P0

## Objective
Make the queue runner's watch loop completely crash-proof. It must catch ALL exceptions, log them, and continue running. The queue runner should never exit unless explicitly killed.

## Problem
The queue runner (`run_queue.py`) keeps dying from unhandled exceptions during watch mode. Exit code 127 (command not found), file path errors, and other transient failures kill the entire process. This means specs stop being processed and the build pipeline stalls silently.

## What Needs to Happen

### 1. Top-level try/except in the watch loop
The watch loop (the `while True` polling loop inside `run_queue()`) must wrap every tick in a broad try/except. Catch `Exception` (not `BaseException` — let KeyboardInterrupt through). Log the traceback. Continue to next tick.

### 2. Per-spec try/except in result handling
`_process_result()` handles individual spec results (CLEAN, TIMEOUT, NEEDS_DAVE). If one spec's result processing throws, it must not kill the entire queue. Catch, log, move the spec to `_needs_review/` with error details, continue.

### 3. Auto-commit failure isolation
`auto_commit_bee_output()` runs git commands. If git fails (exit code 127, lock file, etc.), it must not propagate. Wrap in try/except, log the failure, continue without committing.

### 4. Fix cycle failure isolation
`generate_fix_spec()` and `generate_q33n_fix_spec()` write files. If file I/O fails, catch it, log it, move original spec to `_needs_review/`, continue.

### 5. _active/ directory operations
All file moves (queue → _active, _active → _done, _active → _needs_review) must handle FileNotFoundError, PermissionError, and other OS errors gracefully. Log and continue.

## Files to Read First
- `.deia/hive/scripts/queue/run_queue.py` (the entire file — understand the watch loop, run_queue(), _process_result(), auto_commit_bee_output())
- `.deia/hive/scripts/queue/fix_cycle.py` (generate_fix_spec, generate_q33n_fix_spec)
- `.deia/hive/scripts/queue/spec_processor.py` (process_spec — where dispatch happens)

## Files to Modify
- `.deia/hive/scripts/queue/run_queue.py` — add crash resilience at all levels
- `.deia/hive/scripts/queue/fix_cycle.py` — wrap file I/O in try/except
- `.deia/hive/scripts/queue/spec_processor.py` — wrap dispatch subprocess in try/except (if not already)

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

## Model Assignment
sonnet
