---
id: BENCH-006
priority: P0
model: sonnet
role: bee
depends_on: []
---

# SPEC-BENCH-006: Wave A Integration — PRISMBenchAdapter + CLI Fixes

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

Wire the benchmark infrastructure end-to-end so `python _tools/benchmark.py run prism-bench --trials 2 --dry-run` works. Wave A built 6 modules independently; this task connects them by creating the missing `PRISMBenchAdapter` and fixing CLI issues. The Wave A exit criteria require `benchmark run prism-bench` to work end-to-end with the 5 trivial PRISM-IR test workflows.

## Files to Read First

- simdecisions/benchmark/adapter.py
- simdecisions/benchmark/runner.py
- simdecisions/benchmark/executor.py
- simdecisions/benchmark/types.py
- simdecisions/benchmark/estimator.py
- simdecisions/benchmark/test_workflows/workflow_01_simple_queue.json
- _tools/benchmark.py
- .deia/config/benchmarks.yml

## Deliverables

| # | File | What |
|---|------|------|
| 1 | `simdecisions/benchmark/adapters/__init__.py` | Package init |
| 2 | `simdecisions/benchmark/adapters/prism_bench.py` | `PRISMBenchAdapter(BenchmarkAdapter)` — loads 5 test workflows, implements all 5 abstract methods |
| 3 | `_tools/benchmark.py` | Fix Unicode crash on Windows (replace emoji with ASCII), fix `cmd_run` to handle `--dry-run` before adapter instantiation |
| 4 | `tests/simdecisions/benchmark/test_prism_bench_adapter.py` | Tests for the adapter |
| 5 | `tests/simdecisions/benchmark/test_benchmark_cli_integration.py` | Integration tests: `list`, `estimate`, `run --dry-run` all succeed |

## Implementation Details

### PRISMBenchAdapter

Must subclass `BenchmarkAdapter` from `simdecisions/benchmark/adapter.py` and implement:

| Method | Implementation |
|--------|---------------|
| `name` property | Return `"prism-bench"` |
| `version` property | Return `"0.1.0"` |
| `load_tasks()` | Read all 5 JSON files from `simdecisions/benchmark/test_workflows/`, return list of `BenchmarkTask` objects |
| `task_to_ir(task)` | Return the workflow JSON dict directly (already PRISM-IR format) |
| `run_baseline(task, model)` | Placeholder: return `BaselineResult` with `output="baseline_placeholder"` and zero metrics. Real execution comes in Wave B. |
| `run_simdecisions(task, ir, model)` | Placeholder: return `SimResult` with `output="simdecisions_placeholder"`, `ir_used=ir` and zero metrics. Real execution comes in Wave B. |
| `evaluate(task, output)` | Placeholder: return `EvalResult` with `score=0.0`, `passed=False`, `details="evaluation not implemented"`. Real scoring comes in Wave B. |

The `load_tasks()` method must:
- Locate workflow dir relative to adapter file: `Path(__file__).parent.parent / "test_workflows"`
- Load each `.json` file, parse with `json.load()`
- Create `BenchmarkTask` with `id` from workflow JSON `id` field, `benchmark_name="prism-bench"`, `benchmark_version="0.1.0"`, `track=""`, `trial=0`, `model=""`, `task_data=<full workflow dict>`
- Return sorted by filename for deterministic ordering

### CLI Fixes (`_tools/benchmark.py`)

| Line | Problem | Fix |
|------|---------|-----|
| 148 | `print(f"{enabled} ...")` uses `\u2713` / `\u2717` | Replace with `[Y]` / `[N]` ASCII |
| 96 | `print(f"⚠️  Budget...")` uses emoji | Replace with `WARNING:` |
| 102 | `print(f"✓ Budget...")` uses checkmark | Replace with `OK:` |
| 114 | `print(f"✓ Generated...")` uses checkmark | Replace with `OK:` |

### benchmarks.yml

No changes needed. The adapter path `simdecisions.benchmark.adapters.prism_bench.PRISMBenchAdapter` will resolve once the module exists.

## Acceptance Criteria

- [ ] `simdecisions/benchmark/adapters/__init__.py` exists and exports `PRISMBenchAdapter`
- [ ] `simdecisions/benchmark/adapters/prism_bench.py` exists with class `PRISMBenchAdapter(BenchmarkAdapter)`
- [ ] `PRISMBenchAdapter.load_tasks()` returns exactly 5 `BenchmarkTask` objects (one per test workflow)
- [ ] `PRISMBenchAdapter.task_to_ir()` returns a dict with `id`, `nodes`, `edges` keys
- [ ] `PRISMBenchAdapter.run_baseline()` returns a `BaselineResult` instance
- [ ] `PRISMBenchAdapter.run_simdecisions()` returns a `SimResult` instance with `ir_used` set
- [ ] `PRISMBenchAdapter.evaluate()` returns an `EvalResult` instance
- [ ] `python _tools/benchmark.py list` runs without error and shows `prism-bench`
- [ ] `python _tools/benchmark.py estimate prism-bench --trials 2` runs without error and prints budget
- [ ] `python _tools/benchmark.py run prism-bench --trials 2 --dry-run` runs without error
- [ ] No Unicode/encoding errors on Windows (no emoji characters in CLI output)
- [ ] All existing benchmark tests still pass: `pytest tests/simdecisions/benchmark/ -x`
- [ ] New adapter tests pass: `pytest tests/simdecisions/benchmark/test_prism_bench_adapter.py -x`
- [ ] New CLI integration tests pass: `pytest tests/simdecisions/benchmark/test_benchmark_cli_integration.py -x`
- [ ] No file exceeds 500 lines

## Smoke Test

- [ ] `python _tools/benchmark.py list` prints `prism-bench (v0.1.0)` with no crash
- [ ] `python _tools/benchmark.py estimate prism-bench --trials 2` prints work items, CLOCK, COIN, CARBON
- [ ] `python _tools/benchmark.py run prism-bench --trials 2 --dry-run` prints `[DRY RUN]` task count

## Constraints

- No file over 500 lines
- No stubs beyond the placeholder returns documented above (those are intentional — real execution is Wave B)
- No git operations
- TDD: write tests first
- Use `var(--sd-*)` CSS variables only (N/A for this task)
- `run_baseline` / `run_simdecisions` / `evaluate` return valid typed objects, not `None`
