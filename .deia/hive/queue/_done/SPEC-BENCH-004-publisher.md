---
id: BENCH-004
priority: P0
model: haiku
role: bee
depends_on: [BENCH-001, BENCH-003]
---
# TASK-BENCH-004 — Results Publisher

**Priority:** P0
**Model:** Haiku
**Type:** Code implementation
**Date:** 2026-04-13
**Wave:** A — Infrastructure
**Estimated Cost:** $1.00

---

## Objective

Implement the Publisher: markdown summary generator, raw JSON exporter, and trend chart data preparation. Takes aggregated statistics from ResultsCollector and produces publication-ready outputs.

---

## Context

After ResultsCollector aggregates and computes statistics, the Publisher formats results for human consumption (markdown reports) and machine consumption (JSON for charts/APIs). Wave A only outputs to local `.deia/benchmark/results/`; automated publishing to benchmarks.simdecisions.com is Wave E.

### Q88N Decisions (binding)

- **Output formats:** Markdown summary, raw JSON, CSV for trend charts
- **Results location:** Local `.deia/benchmark/results/` (publish manually to public repo later)
- **No web generation yet:** Static site generation is Wave E

---

## Files to Read First

- `docs/specs/SPEC-BENCHMARK-SUITE-001.md`
  Section 3.4 (Statistical Reporting), Section 4 (Publishing) for output format requirements

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/collector.py`
  ResultsCollector (created by BENCH-003) — publisher consumes its output

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/types.py`
  BenchmarkResult dataclass (created by BENCH-001)

---

## Deliverables

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/publisher.py`
  - `Publisher` class with methods:
    - `__init__(results_dir: str)` — set results directory
    - `publish_summary(benchmark_name: str, comparison: dict, output_path: str) -> None`
      - Write markdown file with:
        - Benchmark name, version, SimDecisions version
        - Statistical comparison table (from ResultsCollector.generate_summary_table())
        - Trial count, model used
        - Date generated
      - Output: `{benchmark_name}_summary.md`
    - `publish_raw_json(benchmark_name: str, results: list[BenchmarkResult], output_path: str) -> None`
      - Write all raw result objects as JSON array
      - Output: `{benchmark_name}_raw.json`
    - `publish_trend_data(benchmark_name: str, historical_results: list[dict], output_path: str) -> None`
      - Write CSV with columns: simdecisions_version, date, metric_name, baseline_mean, simdecisions_mean, delta, p_value
      - For trend charts showing improvement over SimDecisions versions
      - Output: `{benchmark_name}_trends.csv`
    - `publish_all(benchmark_name: str, collector: ResultsCollector) -> None`
      - Generate all three outputs (summary, raw, trends)
      - Organize into: `.deia/benchmark/results/{benchmark_name}/YYYY-MM-vX.Y.Z/`

---

## Test Requirements

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/benchmark/test_publisher.py`
  - Test publish_summary() creates valid markdown file
  - Test markdown includes all required sections
  - Test publish_raw_json() writes valid JSON (parseable, contains all results)
  - Test publish_trend_data() creates valid CSV with correct columns
  - Test CSV format is parseable by pandas (no extra quotes, correct delimiters)
  - Test publish_all() creates all three files in correct directory structure
  - Test publish_all() creates versioned subdirectory: `{benchmark}/YYYY-MM-vX.Y.Z/`
  - Test edge case: empty results list
  - Test edge case: single trial (no variance)
  - 12 tests minimum

**Total test count:** 12 minimum

**TDD required:** Write tests first, then implementation

---

## Acceptance Criteria

- [ ] `simdecisions/benchmark/publisher.py` with `Publisher` class (methods: `__init__`, `publish_summary`, `publish_raw_json`, `publish_trend_data`, `publish_all`)
- [ ] `publish_summary()` writes valid CommonMark markdown with benchmark name, version, statistical comparison table, trial count, model, date
- [ ] `publish_raw_json()` writes valid JSON array of all raw BenchmarkResult objects
- [ ] `publish_trend_data()` writes CSV with columns: `simdecisions_version`, `date`, `metric_name`, `baseline_mean`, `simdecisions_mean`, `delta`, `p_value`
- [ ] `publish_all()` creates versioned subdirectory structure: `.deia/benchmark/results/{benchmark_name}/YYYY-MM-vX.Y.Z/`
- [ ] SimDecisions version read dynamically from `simdecisions.__version__` or git tag -- not hardcoded
- [ ] CSV output is parseable by standard CSV readers (correct delimiters, proper quoting)
- [ ] Edge case: empty results list handled without error
- [ ] Edge case: single trial (no variance) handled gracefully
- [ ] Tests in `tests/simdecisions/benchmark/test_publisher.py` -- 12+ tests passing
- [ ] No file exceeds 500 lines

---

## Constraints

- No file over 500 lines (single file acceptable for this task)
- Markdown output must be valid CommonMark
- JSON output must be valid (parseable by standard JSON libraries)
- CSV must use standard format (comma-separated, quoted strings if needed)
- No hardcoded SimDecisions version — read from `simdecisions.__version__` or git tag
- No stubs

---

## Dependencies

**Depends on:** BENCH-001 (types), BENCH-003 (collector)

**Blocks:** None (BENCH-005 can proceed in parallel)

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:

`C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/responses/20260413-TASK-BENCH-004-RESPONSE.md`

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
