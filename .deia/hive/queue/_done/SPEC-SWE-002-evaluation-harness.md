# SPEC-SWE-002-evaluation-harness: SWE-bench Evaluation Harness and Results Reporter

## Priority
P0

## Depends On
SWE-001

## Model Assignment
sonnet

## Objective

Build `_tools/swebench_eval.py` — a CLI that collects patches produced by factory bees, assembles them into the swebench predictions format, runs Docker-based evaluation, and produces a results report. This is the second half of the SWE-bench pipeline. The evaluation harness applies each patch to the target repo inside a Docker container, runs the repo's test suite, and checks whether the fix resolves the issue.

## Files to Read First

- _tools/benchmark.py
- _tools/benchmark_preflight.py
- .deia/config/benchmarks.yml

## Acceptance Criteria

- [ ] `_tools/swebench_eval.py` exists with four subcommands: `collect`, `evaluate`, `report`, `status`
- [ ] `collect` subcommand scans `.deia/benchmark/swebench/patches/` for `*.diff` files, reads `.deia/benchmark/swebench/sample.json` to match instance_ids, assembles a predictions JSON file at `.deia/benchmark/swebench/predictions.json` in swebench format: list of `{"instance_id": str, "model_name_or_path": "simdecisions-factory", "model_patch": str}`
- [ ] `collect` reports how many patches found vs how many tasks in sample (e.g. "Collected 47/50 patches")
- [ ] `evaluate` subcommand runs swebench evaluation via subprocess: `python -m swebench.harness.run_evaluation --dataset_name princeton-nlp/SWE-bench_Verified --split test --predictions_path .deia/benchmark/swebench/predictions.json --run_id {timestamp} --max_workers {--workers, default 4} --timeout {--timeout, default 1800} --report_dir .deia/benchmark/swebench/results/`
- [ ] `evaluate` runs the subprocess inside WSL if `sys.platform == "win32"` (prepend `wsl` to the command) since swebench harness requires Linux
- [ ] `evaluate` streams subprocess stdout/stderr to console in real-time so user can monitor progress
- [ ] `report` subcommand reads evaluation results from `.deia/benchmark/swebench/results/`, parses report JSON files, and produces a summary markdown at `.deia/benchmark/swebench/results/summary.md`
- [ ] Summary report includes: total tasks, patches submitted, resolved count, resolved percentage, per-repo breakdown (repo, submitted, resolved, percentage), top 5 easiest resolved, top 5 hardest unresolved, total evaluation wall time, model name
- [ ] `status` subcommand checks: how many sample tasks exist, how many patches collected, how many evaluated, how many resolved — quick progress overview
- [ ] Tests in `tests/integration/test_swebench_eval.py` with 12+ tests covering: collect finds diff files, collect produces valid predictions JSON, collect reports correct counts, collect handles missing patches, predictions JSON has correct schema, report parses mock result JSONs, report computes resolved percentage, report produces markdown table, status reports correct counts, evaluate builds correct subprocess command, evaluate prepends wsl on Windows, collect skips patches not in sample
- [ ] All tests pass via `pytest tests/integration/test_swebench_eval.py -v`

## Smoke Test

- [ ] `python _tools/swebench_eval.py status` prints progress without errors
- [ ] `python _tools/swebench_eval.py collect` produces `.deia/benchmark/swebench/predictions.json`
- [ ] `pytest tests/integration/test_swebench_eval.py -v` passes

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations (no commits, no pushes)
- Do NOT import `swebench.harness` modules directly — they use `import resource` which fails on Windows. Run evaluation via subprocess only
- Use `wsl` prefix for evaluation subprocess on Windows (Docker runs Linux containers via WSL2, and swebench harness needs Linux Python)
- Predictions JSON must match swebench format exactly: keys `instance_id`, `model_name_or_path`, `model_patch`
- Report format: markdown with tables, suitable for inclusion in a PR description or benchmark dashboard
- TDD: write tests first, then implementation

## Files to Modify

- _tools/swebench_eval.py (create)
- tests/integration/test_swebench_eval.py (create)
