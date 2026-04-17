# TASK-BENCH-003 — Results Collector and Statistics

**Priority:** P0
**Model:** Sonnet
**Type:** Code implementation
**Date:** 2026-04-13
**Wave:** A — Infrastructure
**Estimated Cost:** $3.50

---

## Objective

Implement ResultsCollector: poll completed benchmark tasks from results directory, aggregate per benchmark, compute statistics (Welford online algorithm for mean/variance, Mann-Whitney U test for significance), and prepare data for publishing.

---

## Context

After benchmark tasks complete and write results to `.deia/benchmark/results/`, the ResultsCollector aggregates them by benchmark and computes statistical comparisons between baseline and SimDecisions tracks. Uses existing Welford implementation from `simdecisions/des/statistics.py` for numerically stable online statistics. Mann-Whitney U test is non-parametric (does not assume normal distribution).

### Q88N Decisions (binding)

- **Statistics:** Welford's algorithm for mean/variance (reuse existing code), Mann-Whitney U for significance
- **Results location:** `.deia/benchmark/results/` (local first, publish manually later)
- **Aggregation:** Per benchmark, per track, across all trials
- **No polling logic yet:** This task implements the aggregation and statistics functions; BENCH-005 wires polling into factory completion

---

## Files to Read First

- `docs/specs/SPEC-BENCHMARK-SUITE-001.md`
  Section 3.4 (Statistical Reporting) for required metrics and table format

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/statistics.py`
  RunningStats class (Welford's algorithm) — reuse this, do NOT reimplement

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/types.py`
  BenchmarkResult dataclass (created by BENCH-001)

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/schemas.py`
  Result YAML schema (created by BENCH-001)

---

## Deliverables

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/collector.py`
  - `ResultsCollector` class with methods:
    - `__init__(results_dir: str)` — set results directory path
    - `load_results(benchmark_name: str) -> list[BenchmarkResult]` — load all result YAML files for a benchmark
    - `aggregate_by_track(results: list[BenchmarkResult]) -> dict[str, list[BenchmarkResult]]` — group by track (baseline, simdecisions)
    - `compute_statistics(track_results: list[BenchmarkResult]) -> dict` — compute mean ± std for accuracy, CLOCK, COIN, CARBON, variance (coefficient of variation)
    - `compare_tracks(baseline_stats: dict, simdecisions_stats: dict, baseline_results: list[BenchmarkResult], simdecisions_results: list[BenchmarkResult]) -> dict` — compute deltas and p-values
    - `generate_summary_table(comparison: dict) -> str` — format as markdown table matching SPEC Section 3.4
    - `export_aggregated_results(benchmark_name: str, output_path: str) -> None` — write aggregated stats to JSON

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/significance.py`
  - `mann_whitney_u(group_a: list[float], group_b: list[float]) -> float` — non-parametric significance test
    - Implementation: Rank all values, compute U statistic, convert to z-score, return p-value
    - Reference: Standard Mann-Whitney U formula (no scipy dependency)
    - Return p-value (0.0–1.0), where < 0.05 indicates statistical significance

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/metrics.py`
  - `coefficient_of_variation(values: list[float]) -> float` — std_dev / mean
  - `recovery_rate(results: list[BenchmarkResult]) -> dict` — extract errors_encountered, errors_recovered from metadata, compute rate
  - `extract_metric(results: list[BenchmarkResult], metric_name: str) -> list[float]` — pull specific metric (e.g., "clock_seconds") from all results

### Output directory

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/benchmark/results/` (new directory)
  - Completed benchmark tasks will write result YAML files here (BENCH-005 writes them)
  - This task reads from here

---

## Test Requirements

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/benchmark/test_collector.py`
  - Test load_results() with mock YAML files
  - Test aggregate_by_track() groups correctly
  - Test compute_statistics() uses RunningStats correctly
  - Test compute_statistics() calculates mean, std_dev, min, max for all currencies
  - Test compare_tracks() computes deltas correctly
  - Test generate_summary_table() produces markdown matching SPEC format
  - Test export_aggregated_results() writes valid JSON
  - 14 tests minimum

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/benchmark/test_significance.py`
  - Test mann_whitney_u() with known datasets
  - Test mann_whitney_u() with identical groups returns p ≈ 1.0
  - Test mann_whitney_u() with clearly different groups returns p < 0.05
  - Test mann_whitney_u() with small sample sizes
  - Test edge case: one group has all same values
  - 8 tests minimum

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/benchmark/test_metrics.py`
  - Test coefficient_of_variation() with known values
  - Test recovery_rate() with mock BenchmarkResult objects
  - Test extract_metric() pulls correct field from results
  - Test edge cases: empty results list, missing metadata fields
  - 8 tests minimum

**Total test count:** 30 minimum (14 + 8 + 8)

**TDD required:** Write tests first, then implementation

---

## Constraints

- No file over 500 lines (split: collector.py, significance.py, metrics.py)
- MUST reuse `simdecisions.des.statistics.RunningStats` — do NOT reimplement Welford's algorithm
- Mann-Whitney U implementation must be self-contained (no scipy dependency)
- Summary table format must match SPEC Section 3.4 exactly
- No stubs

---

## Dependencies

**Depends on:** BENCH-001 (types, schemas)

**Blocks:** BENCH-004 (publisher needs aggregated stats)

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:

`C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/responses/20260413-TASK-BENCH-003-RESPONSE.md`

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
