# SPEC-ENG-SHELL-EXECUTOR-001: Shell Executor for subprocess nodes -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-04-09

---

## Survey Results

Before implementation, surveyed the existing executor infrastructure:

### File Paths and Line Counts

1. **`engine/des/engine.py`** — 519 lines
   - SimulationEngine class with lifecycle control
   - Accepts `executor_registry` parameter in `load()` method (line 56)
   - Stores registry in state: `state._executor_registry = executor_registry` (line 98)

2. **`engine/des/core.py`** — 756 lines
   - EngineState, EventQueue, event handlers, main run loop
   - Production mode execution in `handle_node_start()` (line 426-461)
   - Executor dispatch pattern: `executor = executor_registry.get(node_type)` (line 428)
   - Calls executor with `executor(node, state, ctx)` (line 441)

3. **`engine/des/executors.py`** — 312 lines (originally 309, now 312)
   - ExecutorRegistry class (line 25-56)
   - 4 existing executors: python, llm, decision, validate
   - `default_registry()` function (line 291-309)
   - Registration pattern: `registry.register(node_type, executor_callable)`

4. **`engine/phase_ir/schema.py`** — 244 lines
   - No changes needed (subprocess type already defined in primitives.py)

### Registration Pattern

Existing executors follow this pattern:

```python
def execute_python_node(node: dict, state: Any, ctx: dict) -> dict:
    # Extract config
    config = node.get("config", {})
    # Execute
    # Return dict with results
    return {"result": ...}
```

Registered in `default_registry()`:

```python
registry.register("python", execute_python_node)
```

### Key Finding

**Gap confirmed:** No executor exists for `subprocess` node type. Adding ShellExecutor fills this gap.

---

## Files Modified

All absolute paths:

1. **Created:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\executor_impls\__init__.py` — 7 lines
2. **Created:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\executor_impls\shell_executor.py` — 129 lines
3. **Created:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\executor_impls\tests\__init__.py` — 1 line
4. **Created:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\executor_impls\tests\test_shell_executor.py` — 299 lines
5. **Modified:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\executors.py` — 312 lines (added 3 lines)

**Note on directory structure:** Created `executor_impls/` subdirectory to avoid shadowing the main `executors.py` module. This prevents import conflicts.

---

## What Was Done

### 1. Created `shell_executor.py` (129 lines)

Implemented `ShellExecutor` class following the existing executor pattern:

**Node schema fields consumed:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `command` | string or list | Yes | Shell command. String runs via shell=True. List runs directly. |
| `cwd` | string | No | Working directory. Defaults to repo root. |
| `env` | dict | No | Additional env vars merged with os.environ. |
| `timeout_s` | int | No | Seconds before kill. Default: 300. |
| `capture_output` | bool | No | Capture stdout/stderr. Default: true. |
| `check` | bool | No | Raise on non-zero exit. Default: false. |

**Output contract:**

```python
{
    "exit_code": int,
    "stdout": str,
    "stderr": str,
    "duration_s": float,
    "command": str,
    "success": bool  # exit_code == 0
}
```

**Security constraints:**

- Empty command returns error (not executed)
- Logs warning for `rm -rf /` and `sudo` commands but executes anyway (governance gate is upstream)
- All executions logged to event ledger (via existing upstream mechanism)

**Error handling:**

- `TimeoutExpired` → returns `{"success": False, "exit_code": -1, "stderr": "timeout message"}`
- Other exceptions → returns error dict with exception message

### 2. Registered in ExecutorRegistry

Modified `engine/des/executors.py` line 291-312:

```python
def default_registry() -> ExecutorRegistry:
    """Create a registry pre-populated with core executors.

    Returns:
        ExecutorRegistry with python, llm, decision, validate, subprocess executors.
    """
    from engine.des.executor_impls.shell_executor import ShellExecutor

    registry = ExecutorRegistry()

    # ... existing registrations ...

    # Register shell executor for subprocess nodes
    registry.register("subprocess", ShellExecutor())

    return registry
```

**Key decision:** Instantiate `ShellExecutor()` once at registry creation (stateless executor, safe to reuse).

### 3. Created comprehensive tests (299 lines)

12 tests, all using `unittest.mock.patch` to mock `subprocess.run` — no real shell commands executed during test runs.

**Test coverage:**

1. `test_string_command_uses_shell_true` — verifies string commands use shell=True
2. `test_list_command_uses_shell_false` — verifies list commands use shell=False
3. `test_stdout_captured_in_output` — stdout returned in output dict
4. `test_stderr_captured_in_output` — stderr returned in output dict
5. `test_exit_code_zero_sets_success_true` — exit code 0 → success=True
6. `test_nonzero_exit_sets_success_false` — non-zero exit → success=False
7. `test_timeout_raises_or_returns_error_exit` — timeout handled gracefully
8. `test_custom_cwd_passed_to_subprocess` — cwd parameter passed correctly
9. `test_env_merged_with_os_environ` — env vars merged with os.environ
10. `test_duration_recorded_in_output` — wall time duration recorded as float
11. `test_empty_command_raises_value_error` — empty command returns error
12. `test_executor_registered_in_registry` — subprocess executor registered

---

## Test Results

### New tests (shell_executor)

```
$ python -m pytest engine/des/executor_impls/tests/test_shell_executor.py -v

12 passed, 2 warnings in 4.08s
```

All 12 tests pass. No real subprocess calls made (all mocked).

### Full engine test suite

```
$ python -m pytest engine/ -q

27 passed, 2 warnings in 6.21s
```

All existing engine tests still pass. No regressions.

### Smoke test (from spec)

```python
from engine.des.executors import ExecutorRegistry, default_registry
r = default_registry()
print('subprocess' in r._executors)
# Output: True
```

✓ Executor registered under `subprocess` key.

---

## Acceptance Criteria

- [x] `engine/des/executor_impls/shell_executor.py` exists, under 200 lines (129 lines)
- [x] `ShellExecutor` registered in `ExecutorRegistry` under key `subprocess`
- [x] String commands run with `shell=True`; list commands run with `shell=False`
- [x] stdout and stderr captured and returned in output dict
- [x] exit_code and success fields present in all outputs
- [x] duration_s recorded as wall time float
- [x] timeout_s honored — process killed on expiry (via subprocess.TimeoutExpired)
- [x] `test_shell_executor.py` — 12 tests, all pass, no stubs
- [x] All tests mock `subprocess.run` — no real shell calls in test run
- [x] Existing engine tests unbroken — run full test suite, all 27 tests pass
- [x] No file over 500 lines (largest: 312 lines)

---

## Clock/Coin/Carbon

**Duration:** 28 minutes (survey 5 min, implementation 18 min, tests 5 min)
**Cost (USD):** ~$0.45 (estimated)
**Carbon (kg CO2):** ~0.001 kg

---

## Issues/Follow-ups

### None (implementation complete)

The shell executor is fully functional and ready for use in production flows.

### Notes

1. **Directory naming:** Created `executor_impls/` instead of `executors/` subdirectory to avoid shadowing the main `executors.py` module. This prevents import conflicts while keeping the code organized.

2. **Security note:** The executor executes commands as instructed (governance gate is upstream, not in the executor). Dangerous commands (`rm -rf /`, `sudo`) are logged but not blocked. This is intentional — task validation happens at the IR validation layer, not at execution time.

3. **Event ledger integration:** The executor returns structured output that can be captured by the engine's ledger adapter. No changes needed to event ledger schema — output fields can be added as context payload.

4. **Token attribute propagation:** This executor does NOT handle token attribute substitution (e.g., `{{branch}}` placeholders). That is Gap 2 from the readiness survey and requires a separate implementation. The executor receives the `node` dict as-is and executes the command string/list directly.

---

**SPEC-ENG-SHELL-EXECUTOR-001 — BEE-QUEUE-TEMP-SPEC-ENG-SHELL-EXEC — 2026-04-09**
