# QUEUE-TEMP-SPEC-BENCH-006-wave-a-integration: Wave A Integration — PRISMBenchAdapter + CLI Fixes -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-13

## Files Modified

1. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions\benchmark\adapters\__init__.py` - Created
2. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions\benchmark\adapters\prism_bench.py` - Created
3. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\_tools\benchmark.py` - Modified (Unicode fixes)
4. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\tests\simdecisions\benchmark\test_prism_bench_adapter.py` - Created
5. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\tests\simdecisions\benchmark\test_benchmark_cli_integration.py` - Created

## What Was Done

- Created `simdecisions/benchmark/adapters/` package with `__init__.py`
- Implemented `PRISMBenchAdapter` class with all 5 abstract methods from `BenchmarkAdapter`
- `load_tasks()` loads all 5 JSON test workflows from `test_workflows/` directory, sorted by filename
- `task_to_ir()` returns workflow dict directly (identity transform for PRISM-IR)
- `run_baseline()` returns `BaselineResult` with placeholder output and zero metrics
- `run_simdecisions()` returns `SimResult` with placeholder output, `ir_used` field, and zero metrics
- `evaluate()` returns `EvalResult` with `passed=False`, `score=0.0`, placeholder metadata
- Fixed Unicode crashes in `_tools/benchmark.py`:
  - Line 96: `⚠️` → `WARNING:`
  - Line 102: `✓` → `OK:`
  - Line 114: `✓` → `OK:`
  - Line 146: `✓` / `✗` → `[Y]` / `[N]`
- Wrote 9 unit tests for PRISMBenchAdapter in `test_prism_bench_adapter.py`
- Wrote 8 integration tests for CLI in `test_benchmark_cli_integration.py`
- All tests pass (153 total benchmark tests)

## Tests Run

```
pytest tests/simdecisions/benchmark/ -x
153 passed in 18.21s
```

**New tests:**
- `test_prism_bench_adapter.py`: 9 tests (all passed)
- `test_benchmark_cli_integration.py`: 8 tests (all passed)

**Coverage:**
- Adapter name and version properties
- Loading all 5 test workflows
- Deterministic ordering
- PRISM-IR translation (identity)
- Baseline execution with placeholder result
- SimDecisions execution with placeholder result and `ir_used`
- Evaluation with placeholder result
- Workflow data structure validation
- CLI `list` command
- CLI `estimate` command with/without sampling
- CLI `run --dry-run` command with/without sampling
- Unicode error prevention on Windows
- Error handling for unknown benchmarks

## Blockers

None

## Acceptance Criteria Status

- [x] `simdecisions/benchmark/adapters/__init__.py` exists and exports `PRISMBenchAdapter`
- [x] `simdecisions/benchmark/adapters/prism_bench.py` exists with class `PRISMBenchAdapter(BenchmarkAdapter)`
- [x] `PRISMBenchAdapter.load_tasks()` returns exactly 5 `BenchmarkTask` objects (one per test workflow)
- [x] `PRISMBenchAdapter.task_to_ir()` returns a dict with `id`, `nodes`, `edges` keys
- [x] `PRISMBenchAdapter.run_baseline()` returns a `BaselineResult` instance
- [x] `PRISMBenchAdapter.run_simdecisions()` returns a `SimResult` instance with `ir_used` set
- [x] `PRISMBenchAdapter.evaluate()` returns an `EvalResult` instance
- [x] `python _tools/benchmark.py list` runs without error and shows `prism-bench`
- [x] `python _tools/benchmark.py estimate prism-bench --trials 2` runs without error and prints budget
- [x] `python _tools/benchmark.py run prism-bench --trials 2 --dry-run` runs without error
- [x] No Unicode/encoding errors on Windows (no emoji characters in CLI output)
- [x] All existing benchmark tests still pass: `pytest tests/simdecisions/benchmark/ -x`
- [x] New adapter tests pass: `pytest tests/simdecisions/benchmark/test_prism_bench_adapter.py -x`
- [x] New CLI integration tests pass: `pytest tests/simdecisions/benchmark/test_benchmark_cli_integration.py -x`
- [x] No file exceeds 500 lines

## Smoke Test Results

**✓ Smoke Test 1: `python _tools/benchmark.py list`**
```
[Y] prism-bench (v0.1.0)
  Native PRISM-IR benchmark suite

Total: 1 benchmark(s)
```

**✓ Smoke Test 2: `python _tools/benchmark.py estimate prism-bench --trials 2`**
```
Estimated Budget
================
Work items: 20
CLOCK:      12.0 minutes (720 seconds)
COIN:       $2.40 USD
CARBON:     540 g CO2e (0.540 kg)
```

**✓ Smoke Test 3: `python _tools/benchmark.py run prism-bench --trials 2 --dry-run`**
```
Estimated Budget
================
Work items: 20
CLOCK:      12.0 minutes (720 seconds)
COIN:       $2.40 USD
CARBON:     540 g CO2e (0.540 kg)

[DRY RUN] Would generate 20 task files
[DRY RUN] Models: claude-sonnet-4-5
[DRY RUN] Output directory: C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\benchmark\tasks
```

## File Sizes

All files well under 500-line limit:
- `adapters/__init__.py`: 8 lines
- `adapters/prism_bench.py`: 163 lines
- `test_prism_bench_adapter.py`: 177 lines
- `test_benchmark_cli_integration.py`: 152 lines

## Notes

Wave A integration is complete. The PRISMBenchAdapter successfully:

1. Loads all 5 test workflows from `simdecisions/benchmark/test_workflows/`
2. Provides identity translation (workflows already in PRISM-IR format)
3. Returns valid typed objects for all execution methods
4. Uses placeholder implementations as specified (real execution in Wave B)

The CLI now runs without Unicode errors on Windows, using ASCII replacements:
- `[Y]` / `[N]` for enabled/disabled status
- `OK:` for success messages
- `WARNING:` for warnings

All 153 benchmark tests pass, including 17 new tests for Wave A integration.

Ready for Wave B: real execution via SimDecisions DES engine.
