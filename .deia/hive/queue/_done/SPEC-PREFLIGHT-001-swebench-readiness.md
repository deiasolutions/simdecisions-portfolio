# SPEC-PREFLIGHT-001-swebench-readiness: Run SWE-bench Environment Preflight Check

## Priority
P0

## Depends On
None

## Model Assignment
haiku

## Objective

Run `_tools/benchmark_preflight.py` on the local machine, capture the full output and JSON report, and write a response summarizing which checks passed, which failed, and what blockers exist for running SWE-bench Verified evaluation. Write tests for the preflight script, then execute it and report results.

## Files to Read First

- _tools/benchmark_preflight.py
- .deia/config/benchmarks.yml

## Acceptance Criteria

- [ ] Tests exist at `tests/integration/test_benchmark_preflight.py` with 6+ tests covering: check() function records results, run_cmd() handles timeout, run_cmd() handles missing command, main() produces report JSON, report JSON has required keys (timestamp, machine, results, ready), results list contains at least 10 checks
- [ ] All tests pass via `pytest tests/integration/test_benchmark_preflight.py -v`
- [ ] Script was executed via `python _tools/benchmark_preflight.py` and full stdout captured in response
- [ ] JSON report file `benchmark_preflight_report.json` contents included in response
- [ ] Response clearly lists all FAIL items as blockers
- [ ] Response clearly lists all WARN items as warnings
- [ ] Response states whether machine is ready (ready=true) or not (ready=false)

## Smoke Test

- [ ] `pytest tests/integration/test_benchmark_preflight.py -v` passes
- [ ] `python _tools/benchmark_preflight.py` runs without errors and produces `benchmark_preflight_report.json`

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Script is read-only diagnostics — do NOT modify the preflight script itself
- Tests must mock external commands (docker, curl, etc.) — do not require Docker to be installed for tests to pass
- Report the raw output exactly as produced — do not editorialize or filter results
