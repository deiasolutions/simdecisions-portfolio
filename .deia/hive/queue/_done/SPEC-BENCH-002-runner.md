---
id: BENCH-002
priority: P0
model: sonnet
role: bee
depends_on: [BENCH-001]
---
# TASK-BENCH-002 — Benchmark Runner Core

**Priority:** P0
**Model:** Sonnet
**Type:** Code implementation
**Date:** 2026-04-13
**Wave:** A — Infrastructure
**Estimated Cost:** $4.00

---

## Objective

Implement the BenchmarkRunner: manifest loader (benchmarks.yml), budget estimator, factory task generator (wraps benchmark tasks in SPEC format), and CLI at `_tools/benchmark.py`.

---

## Context

The BenchmarkRunner orchestrates benchmark execution. It loads a manifest of registered benchmarks, estimates cost before running, generates factory-compatible SPEC task files for each benchmark work item, and provides a CLI interface. It does NOT manage concurrency — tasks are submitted to the factory queue which handles scheduling.

### Q88N Decisions (binding)

- **Factory format:** Wrap benchmark tasks in standard SPEC-*.md format (one queue, one format)
- **CLI location:** Standalone script at `_tools/benchmark.py`, thin alias in hivenode shell
- **benchmarks.yml:** Created as part of this task's deliverable
- **Budget limits:** max_coin_per_run=$50, max_clock_per_task=600s, budget_limit_usd=$0.50 per task item
- **No dispatch:** Runner generates task files but does NOT dispatch them (factory integration is BENCH-005)

---

## Files to Read First

- `docs/specs/SPEC-BENCHMARK-SUITE-001.md`
  Section 3 (Execution Protocol), Section 6 (Factory Task Format), Section 7 (Wave A tasks)

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/types.py`
  BenchmarkTask and result dataclasses (created by BENCH-001)

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/adapter.py`
  BenchmarkAdapter interface (created by BENCH-001)

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/tasks/TASK-BENCH-001.md`
  Completed dependency for types and adapter

---

## Deliverables

### Python modules

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/runner.py`
  - `BenchmarkRunner` class with methods:
    - `__init__(manifest_path: str)` — load benchmarks.yml
    - `load_manifest() -> dict` — parse YAML manifest
    - `get_adapter(benchmark_name: str) -> BenchmarkAdapter` — instantiate adapter for given benchmark
    - `estimate_budget(benchmark_name: str, trials: int, sample_size: int | None) -> dict` — calculate estimated work items, CLOCK, COIN, CARBON
    - `generate_tasks(benchmark_name: str, trials: int, models: list[str], sample_size: int | None) -> list[str]` — generate SPEC task file paths (files written to `.deia/benchmark/tasks/`)
    - `_generate_task_file(task: BenchmarkTask, output_path: str) -> None` — write one SPEC-*.md file for a benchmark work item

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/estimator.py`
  - `estimate_clock(benchmark_name: str, task_count: int, avg_task_duration: float) -> float` — estimate wall time
  - `estimate_coin(model: str, task_count: int, avg_tokens_per_task: int) -> float` — estimate USD cost
  - `estimate_carbon(model: str, task_count: int, avg_tokens_per_task: int) -> float` — estimate CO2e using carbon.py
  - `format_budget_summary(estimates: dict) -> str` — pretty-print budget for CLI display

### CLI script

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/_tools/benchmark.py`
  - `estimate` subcommand: `python _tools/benchmark.py estimate <benchmark> [--trials N] [--sample N]`
    - Display: task count, estimated CLOCK, COIN, CARBON
  - `run` subcommand: `python _tools/benchmark.py run <benchmark> [--trials N] [--models MODEL1,MODEL2] [--dry-run] [--sample N]`
    - If `--dry-run`: display task list without executing
    - Otherwise: generate task files, display summary, prompt for approval (unless budget < $5.00 auto-approve threshold)
  - `list` subcommand: `python _tools/benchmark.py list`
    - Display registered benchmarks from manifest with version and description

### Config file

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/config/benchmarks.yml`
  - Schema:
    ```yaml
    benchmarks:
      - name: prism-bench
        version: "0.1.0"
        adapter: simdecisions.benchmark.adapters.prism_bench.PRISMBenchAdapter
        description: "Native PRISM-IR benchmark suite"
        enabled: true
        defaults:
          trials: 5
          models: [claude-sonnet-4-5]
          budget_limit_usd: 0.50
          timeout_seconds: 600
    ```
  - Wave A includes ONLY `prism-bench` entry (no SWE-bench yet)

### Output directory

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/benchmark/tasks/` (new directory)
  - Generated SPEC-*.md files will be written here

---

## Test Requirements

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/benchmark/test_runner.py`
  - Test BenchmarkRunner loads manifest correctly
  - Test get_adapter() returns correct adapter class
  - Test estimate_budget() calculates work items correctly (10 tasks × 2 tracks × 5 trials = 100 items)
  - Test generate_tasks() creates correct number of SPEC files
  - Test _generate_task_file() writes valid SPEC-*.md format
  - Test SPEC file includes: task_id, type=benchmark, priority=P2, budget_limit_usd, timeout_seconds, acceptance criteria
  - 12 tests minimum

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/benchmark/test_estimator.py`
  - Test estimate_clock() with known task counts
  - Test estimate_coin() with known models and token counts
  - Test estimate_carbon() delegates to carbon.compute_carbon()
  - Test format_budget_summary() produces readable output
  - 8 tests minimum

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/benchmark/test_cli.py`
  - Test `benchmark.py estimate` with mock manifest
  - Test `benchmark.py list` displays benchmarks
  - Test `benchmark.py run --dry-run` does not write files
  - Test `benchmark.py run` prompts for approval when budget > $5.00
  - Test CLI exits with error if benchmark not found in manifest
  - 10 tests minimum (use subprocess or click.testing.CliRunner if using click)

**Total test count:** 30 minimum (12 + 8 + 10)

**TDD required:** Write tests first, then implementation

---

## Acceptance Criteria

- [ ] `simdecisions/benchmark/runner.py` with `BenchmarkRunner` class (methods: `__init__`, `load_manifest`, `get_adapter`, `estimate_budget`, `generate_tasks`, `_generate_task_file`)
- [ ] `simdecisions/benchmark/estimator.py` with `estimate_clock()`, `estimate_coin()`, `estimate_carbon()`, `format_budget_summary()` functions
- [ ] `_tools/benchmark.py` CLI with `estimate`, `run`, and `list` subcommands
- [ ] `.deia/config/benchmarks.yml` manifest with `prism-bench` entry (version, adapter path, defaults)
- [ ] `.deia/benchmark/tasks/` output directory created
- [ ] `BenchmarkRunner.estimate_budget()` correctly calculates: tasks x tracks x trials = total work items
- [ ] `BenchmarkRunner.generate_tasks()` writes valid SPEC-*.md files with task_id, type=benchmark, priority=P2, budget_limit_usd, timeout_seconds
- [ ] CLI `run` subcommand prompts for approval when estimated COIN > $5.00, auto-approves below threshold
- [ ] CLI `run --dry-run` displays task list without writing files
- [ ] Tests in `tests/simdecisions/benchmark/test_runner.py` -- 12+ tests passing
- [ ] Tests in `tests/simdecisions/benchmark/test_estimator.py` -- 8+ tests passing
- [ ] Tests in `tests/simdecisions/benchmark/test_cli.py` -- 10+ tests passing
- [ ] No file exceeds 500 lines

---

## Constraints

- No file over 500 lines (split: runner.py, estimator.py, CLI separate)
- SPEC task files must match format from SPEC-BENCHMARK-SUITE-001 Section 6
- Budget approval gate required if estimated COIN > $5.00
- CLI must be runnable standalone: `python _tools/benchmark.py`
- No hardcoded benchmark configs — all from benchmarks.yml
- No stubs

---

## Dependencies

**Depends on:** BENCH-001 (types, adapter, carbon.py)

**Blocks:** BENCH-005 (factory integration needs task generator)

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:

`C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/responses/20260413-TASK-BENCH-002-RESPONSE.md`

The response MUST contain these 8 sections:

1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full absolute paths
3. **What Was Done** — bullet list of concrete changes (not intent)
4. **Test Results** — test files run, pass/fail counts, pytest output summary
5. **Build Verification** — did tests pass? Include last 5 lines of pytest output
6. **Acceptance Criteria** — copy from task, mark [x] or [ ] with explanation if not done
7. **Clock / Cost / Carbon** — all three currencies, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, recommended next tasks

DO NOT skip any section.
