# Briefing: Build Queue Phase 2 — Wire Real Dispatch + Fix Cycles

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-12
**Priority:** Alpha Part 2, Phase 2

---

## Objective

Replace the `process_spec()` stub in `run_queue.py` with real dispatch integration, and wire the fix cycle logic so failed specs can be retried automatically (max 2 cycles, then NEEDS_DAVE).

Phase 1 built the queue runner skeleton with budget enforcement, spec parsing, file movement, event logging, and morning reports. Phase 2 makes it actually dispatch work through the HIVE.md chain.

---

## What Exists (Phase 1 — DO NOT rewrite)

These files were built last night. Read them. Do not rewrite them. Extend them.

| File | What it does | Lines |
|------|-------------|-------|
| `.deia/hive/scripts/queue/run_queue.py` | Queue orchestration loop. `process_spec()` at line 165 is a stub that simulates dispatch with fixed $0.50 cost. Everything else (queue loading, priority sorting, budget enforcement, file movement, event logging, morning report generation) is complete and tested. | 439 |
| `.deia/hive/scripts/queue/morning_report.py` | Morning report generator. `generate_morning_report()` takes events and writes markdown. QueueEvent dataclass. Complete. | 248 |
| `.deia/config/queue.yml` | Budget, model assignments, paths, deploy config, git settings. | ~30 |
| `.deia/config/regent-bot-prompt.md` | System prompt template for Q88NR-bot. 141 lines. Mechanical review checklist. | 141 |
| `.deia/hive/scripts/dispatch/dispatch.py` | The dispatch script. `dispatch_bee()` dispatches a task file to a Claude instance. Supports `--role bee/queen/regent`, `--model`, `--inject-boot`. Returns response file path. | 353 |

---

## Deliverable 1: Wire process_spec() to dispatch Q88NR-bot

Replace the stub in `run_queue.py:165-245` with real dispatch logic.

### What process_spec() must do:

1. **Load the regent bot prompt** from `.deia/config/regent-bot-prompt.md`
2. **Inject the spec content** into the regent bot prompt (the spec becomes the "task" for Q88NR-bot)
3. **Create a temporary task file** in `.deia/hive/tasks/` containing the merged prompt + spec. This is needed because `dispatch.py` validates that task files are in `.deia/hive/tasks/`. (Note: TASK-024 is fixing dispatch.py to also accept `.deia/hive/coordination/`, but the temporary file approach works regardless.)
4. **Call dispatch.py** via subprocess:
   ```bash
   python .deia/hive/scripts/dispatch/dispatch.py <temp_task_file> --model <regent_bot_model> --role queen --inject-boot --timeout <timeout>
   ```
   The model comes from `config["models"]["regent_bot"]` in queue.yml.
5. **Read the response file** that dispatch.py creates in `.deia/hive/responses/`
6. **Parse the response** to extract: success/failure, cost, duration, test counts
7. **Determine result status**:
   - If response indicates all tests pass and no stubs → `CLEAN`
   - If response indicates failures → check fix cycle count, either re-queue or `NEEDS_DAVE`
8. **Clean up** the temporary task file
9. **Return SpecResult** with actual cost, duration, and status

### Important constraints:
- The regent bot prompt already has the Q88NR-bot's full workflow. You don't need to re-teach it the HIVE.md chain. You just inject the spec.
- Use `subprocess.run()` to call dispatch.py. Do NOT import dispatch.py functions directly — it has global state that makes it messy to call as a library.
- Capture stdout/stderr from the subprocess for logging.
- Parse the response file header to extract cost and duration. The header format is:
  ```
  # Cost (USD): $X.XX
  # Duration: Xs
  # Success: True/False
  ```

---

## Deliverable 2: Fix Cycle Logic

When a spec's result is not CLEAN, the queue runner should:

1. **Check fix cycle count** for this spec. Track via a dict: `fix_cycles: dict[str, int]` keyed by original spec ID.
2. **If fix_cycles < max_fix_cycles_per_spec** (from queue.yml, default 2):
   - Generate a fix spec from the failure details
   - Write it to `.deia/hive/queue/` as a P0 spec with naming: `YYYY-MM-DD-HHMM-SPEC-fix-<original-spec-name>.md`
   - Increment fix cycle count
   - Log `QUEUE_FIX_CYCLE` event
   - Insert the fix spec at the front of the remaining queue (P0 = process next)
3. **If fix_cycles >= max_fix_cycles_per_spec**:
   - Set status to `NEEDS_DAVE`
   - Move original spec to `_needs_review/`
   - Log `QUEUE_NEEDS_DAVE` event
   - Include error details in the event for the morning report

### Fix Spec Format

```markdown
# SPEC: Fix failures from <original-spec-name>

## Priority
P0

## Objective
Fix the errors reported after processing <original-spec-name>. See error details below.

## Context
Original spec: <path to original spec>
Fix cycle: <N> of <max>

### Error Details
<paste from response file: test failures, stderr, etc.>

## Acceptance Criteria
- [ ] All original acceptance criteria still pass
- [ ] Reported errors are resolved
- [ ] No new test regressions

## Model Assignment
<same model as original spec>

## Constraints
- Do not break existing tests
- Fix the reported errors, do not refactor
```

### Function signature

```python
def generate_fix_spec(
    original_spec: SpecFile,
    error_details: str,
    fix_cycle: int,
    max_cycles: int,
    queue_dir: Path
) -> Path:
    """Generate a fix spec and write it to the queue directory.

    Returns:
        Path to the generated fix spec file
    """
```

---

## Files to Read

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` (the main target)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py` (understand how to call it)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\regent-bot-prompt.md` (the prompt template)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\queue.yml` (config structure)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\morning_report.py` (QueueEvent dataclass)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-BUILD-QUEUE-001.md` (full spec, sections 4, 7, 8)

---

## Model Assignments

- This work should be split into **2 tasks** dispatched to **Sonnet** bees:
  - **TASK-025A**: Wire `process_spec()` — replace stub with real dispatch via subprocess
  - **TASK-025B**: Fix cycle logic — `generate_fix_spec()` + fix cycle tracking in `run_queue()`

TASK-025B depends on TASK-025A (fix cycles need the real process_spec to know what failed). Dispatch sequentially.

---

## Test Requirements

### TASK-025A tests:
- process_spec() calls subprocess with correct arguments
- Response file parsing extracts cost, duration, success
- CLEAN result when dispatch succeeds
- Error handling when dispatch fails (subprocess error, missing response file)
- Temporary task file is created and cleaned up
- Use `unittest.mock.patch('subprocess.run')` to mock dispatch — do NOT actually dispatch bees during tests

### TASK-025B tests:
- generate_fix_spec() creates valid markdown with correct format
- Fix spec is P0 priority
- Fix spec references original spec
- Fix cycle count tracked correctly
- After max cycles, status is NEEDS_DAVE
- Fix spec inserted at front of remaining queue
- QUEUE_FIX_CYCLE event logged
- QUEUE_NEEDS_DAVE event logged after max cycles

---

## Constraints

- run_queue.py must stay under 500 lines. If adding process_spec() and fix cycle logic pushes it over, extract into a separate module (e.g., `dispatch_handler.py` or `fix_cycle.py`).
- Do NOT modify morning_report.py or queue.yml
- Do NOT modify dispatch.py (TASK-024 handles that)
- All tests use mocks — no real dispatch during testing
- No stubs. Every function complete.

---

## What This Does NOT Cover (Phase 3)

- Smoke test scripts (Playwright, health checks)
- Deploy polling (Railway/Vercel health endpoints)
- `hive dispatch-queue` CLI entry point
- Event Ledger integration (hivenode API calls)

Those are Phase 3. This briefing is Phase 2 only.
