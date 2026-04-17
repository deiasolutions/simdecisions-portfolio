# TASK-025A: Wire process_spec() to Real Dispatch

**From:** Q33N
**To:** BEE (Sonnet)
**Date:** 2026-03-12
**Depends On:** TASK-023A-D (Phase 1 complete)

---

## Objective

Replace the stub implementation of `process_spec()` in `run_queue.py` (lines 165-245) with real dispatch integration. The function must call `dispatch.py` via subprocess to execute Q88NR-bot for each spec, then parse the response to extract cost, duration, and success status.

---

## Context

Phase 1 (TASK-023A-D) built the queue runner skeleton with:
- Spec parsing and priority sorting
- Budget enforcement
- File movement (queue → _done or _needs_review)
- Event logging
- Morning report generation

The stub `process_spec()` at line 165 currently simulates dispatch with hardcoded cost ($0.50) and always returns CLEAN status. Phase 2 wires it to the real HIVE.md chain through dispatch.py.

### How Dispatch Works

`dispatch.py` expects:
- A task file in `.deia/hive/tasks/`
- `--model` flag (e.g., "haiku", "sonnet", "opus")
- `--role` flag (e.g., "queen", "bee", "regent")
- `--inject-boot` flag to append BOOT.md rules to the prompt
- `--timeout` in seconds

It writes a response file to `.deia/hive/responses/` with header:
```
# BEE RESPONSE: <task_id>
# Adapter: <adapter_type>
# Model: <model>
# Role: <role>
# Timestamp: <timestamp>
# Task file: <task_file_name>
# Success: True/False
# Duration: <seconds>s
# Files modified: <count> (verified)
# Cost (USD): $<amount>
# Turns: <count>
# API duration (ms): <milliseconds>
# Session ID: <session_id>
# Boot injected: True/False

---

<response content>
```

### Integration Strategy

1. Load regent bot prompt from `.deia/config/regent-bot-prompt.md`
2. Inject the spec content into the prompt (spec becomes the "task" for Q88NR-bot)
3. Create a temporary task file in `.deia/hive/tasks/` (needed because dispatch.py validates task files are in that directory)
4. Call dispatch.py via `subprocess.run()`
5. Parse the response file header to extract cost, duration, success
6. Determine result status (CLEAN if success, otherwise check fix cycles)
7. Clean up the temporary task file
8. Return SpecResult with actual metrics

---

## Files to Read

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` — current stub at line 165
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py` — understand the CLI interface
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\regent-bot-prompt.md` — the Q88NR-bot system prompt
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\queue.yml` — config["models"]["regent_bot"]

---

## Deliverables

### 1. Replace process_spec() stub (run_queue.py:165-245)

**New implementation must:**

1. **Load regent bot prompt**
   ```python
   regent_prompt_path = repo_root / ".deia" / "config" / "regent-bot-prompt.md"
   regent_prompt = regent_prompt_path.read_text(encoding="utf-8")
   ```

2. **Read spec content**
   ```python
   spec_content = spec.path.read_text(encoding="utf-8")
   ```

3. **Merge prompt + spec**
   ```python
   merged_task = f"{regent_prompt}\n\n---\n\n{spec_content}"
   ```

4. **Create temporary task file**
   ```python
   temp_task_path = repo_root / ".deia" / "hive" / "tasks" / f"QUEUE-TEMP-{spec.path.stem}.md"
   temp_task_path.write_text(merged_task, encoding="utf-8")
   ```

5. **Call dispatch.py via subprocess**
   ```python
   dispatch_script = repo_root / ".deia" / "hive" / "scripts" / "dispatch" / "dispatch.py"
   regent_model = config["models"]["regent_bot"]

   cmd = [
       "python",
       str(dispatch_script),
       str(temp_task_path),
       "--model", regent_model,
       "--role", "queen",
       "--inject-boot",
       "--timeout", "1800"  # 30 min timeout
   ]

   result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(repo_root))
   ```

6. **Find the response file**
   - Parse stdout from subprocess to find the response file path
   - Look for line containing "Response:" and extract the file path
   - If not found in stdout, search `.deia/hive/responses/` for most recent file matching the pattern

7. **Parse response file header**
   ```python
   response_content = response_path.read_text(encoding="utf-8")

   # Extract from header:
   # Success: True/False
   # Duration: <N>s
   # Cost (USD): $<amount>

   success_match = re.search(r'^# Success: (True|False)', response_content, re.MULTILINE)
   duration_match = re.search(r'^# Duration: ([\d.]+)s', response_content, re.MULTILINE)
   cost_match = re.search(r'^# Cost \(USD\): \$([\d.]+)', response_content, re.MULTILINE)
   ```

8. **Determine status**
   ```python
   if success_match and success_match.group(1) == "True":
       status = "CLEAN"
   else:
       # Will be handled by fix cycle logic in TASK-025B
       # For now, just return failure status
       status = "NEEDS_DAVE"
   ```

9. **Clean up temp file**
   ```python
   temp_task_path.unlink()
   ```

10. **Return SpecResult**
    ```python
    return SpecResult(
        spec_id=spec_id,
        status=status,
        cost_usd=cost_usd,
        duration_ms=duration_ms,
        error_msg=error_details if status != "CLEAN" else None
    )
    ```

### 2. Error Handling

Handle these failure modes:
- dispatch.py subprocess fails (non-zero exit code)
- Response file not found
- Response file header missing expected fields
- Timeout (dispatch runs longer than allowed)

For subprocess errors, capture stderr and include in error_msg.

### 3. Logging

Keep existing event logging:
- `QUEUE_SPEC_STARTED` at start (already in stub)
- `QUEUE_BEES_COMPLETE` on success (already in stub)
- Update to use actual cost/duration from response file
- Add subprocess stdout/stderr to session log for debugging

---

## Test Requirements

Write tests in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_run_queue_dispatch.py`

### Test Cases (minimum 10)

1. **test_process_spec_loads_regent_prompt** — verify regent-bot-prompt.md is read
2. **test_process_spec_merges_prompt_and_spec** — verify spec content injected after prompt
3. **test_process_spec_creates_temp_task_file** — verify temp file created in .deia/hive/tasks/
4. **test_process_spec_calls_subprocess_with_correct_args** — mock subprocess.run, verify cmd args
5. **test_process_spec_parses_response_success** — mock response file, extract cost/duration/success=True
6. **test_process_spec_parses_response_failure** — mock response file with success=False
7. **test_process_spec_cleans_up_temp_file** — verify temp file deleted after dispatch
8. **test_process_spec_subprocess_error** — subprocess returns non-zero, verify error handling
9. **test_process_spec_response_file_not_found** — response file missing, verify error handling
10. **test_process_spec_response_header_malformed** — header missing cost field, verify graceful degradation
11. **test_process_spec_timeout_handling** — subprocess timeout, verify error logged

### Mocking Strategy

**DO NOT actually dispatch bees during tests.** Use `unittest.mock.patch`:

```python
from unittest.mock import patch, MagicMock
import subprocess

@patch('subprocess.run')
def test_process_spec_calls_subprocess(mock_run):
    # Setup
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout="[DISPATCH] Response: 20260312-1234-BEE-HAIKU-QUEUE-TEMP-SPEC-TEST-RAW.txt",
        stderr=""
    )

    # Also mock the response file read
    # ...

    # Execute
    result = process_spec(spec, config, events, repo_root)

    # Assert subprocess.run called with correct args
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert args[0] == "python"
    assert "--role" in args and "queen" in args
```

Mock file reads with `patch('pathlib.Path.read_text')` or use temporary files for response file parsing tests.

---

## Constraints

- **No changes to dispatch.py** — use it as-is via subprocess
- **No changes to regent-bot-prompt.md** — just load and inject
- **No changes to queue.yml** — read config only
- **Keep run_queue.py under 500 lines** — if new implementation pushes over, extract helper functions to a new module `dispatch_handler.py`
- **No stubs** — every code path fully implemented
- **All tests use mocks** — no actual Claude API calls during testing

---

## Model Assignment

**Sonnet** — subprocess handling, response parsing, error handling require precision

---

## Acceptance Criteria

- [ ] process_spec() loads regent bot prompt from config file
- [ ] process_spec() creates temporary task file in .deia/hive/tasks/
- [ ] process_spec() calls dispatch.py via subprocess with correct arguments (--model, --role queen, --inject-boot, --timeout)
- [ ] process_spec() parses response file to extract cost_usd, duration_ms, success status
- [ ] process_spec() returns SpecResult with status="CLEAN" when success=True
- [ ] process_spec() returns SpecResult with status="NEEDS_DAVE" when success=False (fix cycle logic in TASK-025B will refine this)
- [ ] process_spec() deletes temporary task file after dispatch
- [ ] process_spec() handles subprocess errors (non-zero exit, stderr captured)
- [ ] process_spec() handles missing response file
- [ ] process_spec() handles malformed response headers
- [ ] All 11 test cases pass
- [ ] run_queue.py total line count ≤ 500 (modularize if needed)
- [ ] No stubs or TODOs in implementation

---

## Response File — MANDATORY

When done, write: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260312-TASK-025A-RESPONSE.md`

Must include all 8 sections:
1. **Status:** COMPLETE | FAILED (reason)
2. **Files Modified** (absolute paths)
3. **What Was Done** (bullet list of concrete changes)
4. **Tests Added/Modified** (file paths + counts)
5. **Test Results** (pass count, any failures)
6. **Clock** (start time, end time, duration)
7. **Cost** (model, turns, estimated USD)
8. **Next Steps** (if any blockers or follow-up needed)

---

**End of TASK-025A**
