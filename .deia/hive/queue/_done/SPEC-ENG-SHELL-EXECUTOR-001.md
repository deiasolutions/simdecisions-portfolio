# SPEC-ENG-SHELL-EXECUTOR-001

**MODE: EXECUTE**

**Spec ID:** SPEC-ENG-SHELL-EXECUTOR-001
**Created:** 2026-04-09
**Author:** Q88N

---

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

---

## Objective

Wire a shell executor into the production engine's `ExecutorRegistry` so
that PRISM-IR task nodes with `type: subprocess` can run arbitrary shell
commands — `git`, `npm`, `python` subprocesses — and capture stdout,
stderr, and exit code as node output. This is Gap 1 from EXP-IR-READINESS
survey. It unblocks IR encoding of SPEC-EXPERIMENT-HIVE-VS-OPUS-001.

---

## Background

The readiness survey (`20260409-EXP-IR-READINESS-RESPONSE.md`) confirmed:

- `type: subprocess` is already defined in the IR schema
- The `ExecutorRegistry` exists and dispatches by node type
- No executor is registered for `subprocess` — calling it raises
  `UnknownExecutorType` or equivalent
- 8 existing types: `human`, `python`, `llm`, `http`, `subprocess`,
  `solver`, `wait`, `signal`

The executor needs to be written and registered. No schema changes needed.

---

## Survey First

Before writing any code, read:

- `engine/des/engine.py` — find `ExecutorRegistry`, confirm how executors
  are registered and called
- `engine/des/core.py` — find the node execution dispatch path
- `engine/phase_ir/schema.py` — confirm `subprocess` node schema fields
- Any existing executor (e.g. `http` or `python`) as the implementation
  pattern to follow
- `.deia/hive/responses/20260409-EXP-IR-READINESS-RESPONSE.md` — prior
  survey results for file+line context

Report file paths, line counts, and the exact registration pattern before
writing any new code.

---

## What To Build

### 1. `engine/des/executors/shell_executor.py` (new file)

```python
class ShellExecutor:
    """
    Executor for subprocess-type IR nodes.
    Runs shell commands, captures output, returns result to engine.
    """
```

Node schema fields consumed:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `command` | string or list | Yes | Shell command. String runs via shell=True. List runs directly. |
| `cwd` | string | No | Working directory. Defaults to repo root. |
| `env` | dict | No | Additional env vars merged with os.environ. |
| `timeout_s` | int | No | Seconds before kill. Default: 300. |
| `capture_output` | bool | No | Capture stdout/stderr. Default: true. |
| `check` | bool | No | Raise on non-zero exit. Default: false — caller handles. |

Output contract (what the executor returns to the engine):

```python
{
    "exit_code": int,
    "stdout": str,          # empty string if not captured
    "stderr": str,          # empty string if not captured
    "duration_s": float,
    "command": str,         # the command as executed
    "success": bool         # exit_code == 0
}
```

The engine stores this as the node's `output` payload. Downstream nodes
can read `output.exit_code`, `output.stdout`, etc. via token attributes.

Security constraints (enforce in executor):

- `command` must not be empty
- If `command` is a string containing `rm -rf /` or `sudo` — log warning,
  execute anyway (governance gate is upstream, not here). Do not silently
  block.
- Log every execution to the event ledger stub: command, cwd, exit_code,
  duration_s, node_id

### 2. Register in ExecutorRegistry

Find the registration point (likely `engine.py` or a `__init__.py`).
Add:

```python
registry.register("subprocess", ShellExecutor())
```

Follow the exact pattern used by the existing executors.

### 3. `engine/des/executors/tests/test_shell_executor.py` (new file)

Minimum 12 tests. All use `unittest.mock` to mock `subprocess.run` —
no real shell commands during testing.

Required test cases:

```
test_string_command_uses_shell_true
test_list_command_uses_shell_false
test_stdout_captured_in_output
test_stderr_captured_in_output
test_exit_code_zero_sets_success_true
test_nonzero_exit_sets_success_false
test_timeout_raises_or_returns_error_exit
test_custom_cwd_passed_to_subprocess
test_env_merged_with_os_environ
test_duration_recorded_in_output
test_empty_command_raises_value_error
test_executor_registered_in_registry
```

---

## Acceptance Criteria

- [ ] `engine/des/executors/shell_executor.py` exists, under 200 lines
- [ ] `ShellExecutor` registered in `ExecutorRegistry` under key `subprocess`
- [ ] String commands run with `shell=True`; list commands run with `shell=False`
- [ ] stdout and stderr captured and returned in output dict
- [ ] exit_code and success fields present in all outputs
- [ ] duration_s recorded as wall time float
- [ ] timeout_s honored — process killed on expiry
- [ ] `test_shell_executor.py` — 12 tests, all pass, no stubs
- [ ] All tests mock `subprocess.run` — no real shell calls in test run
- [ ] Existing engine tests unbroken — run full test suite, report result
- [ ] No file over 500 lines

---

## Smoke Test

```bash
# Confirm executor registered
python -c "
from engine.des.engine import ExecutorRegistry
r = ExecutorRegistry()
print('subprocess' in r._executors)
"
# Expected: True

# Run new tests
python -m pytest engine/des/executors/tests/test_shell_executor.py -v
# Expected: 12 passed

# Run full engine test suite
python -m pytest engine/ -q
# Expected: all existing tests still pass
```

---

## Constraints

- No file over 500 lines
- All tests use `unittest.mock` — no real subprocess calls during testing
- Follow existing executor registration pattern exactly — do not invent
  a new pattern
- Do not modify `schema.py` — `subprocess` type is already defined
- Do not modify existing executors
- ASCII-safe output (Windows compatible)
- Python 3.13

---

## Response File

`.deia/hive/responses/YYYYMMDD-SPEC-ENG-SHELL-EXECUTOR-001-RESPONSE.md`

All 8 sections mandatory: Header, Survey Results, Files Modified,
What Was Done, Test Results, Acceptance Criteria, Clock/Coin/Carbon,
Issues/Follow-ups.

---

*SPEC-ENG-SHELL-EXECUTOR-001 — Q88N — 2026-04-09*
