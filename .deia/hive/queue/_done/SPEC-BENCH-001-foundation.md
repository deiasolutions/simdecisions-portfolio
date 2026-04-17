---
id: BENCH-001
priority: P0
model: sonnet
role: bee
---
# TASK-BENCH-001 — Benchmark Infrastructure Foundation

**Priority:** P0
**Model:** Sonnet
**Type:** Code implementation
**Date:** 2026-04-13
**Wave:** A — Infrastructure
**Estimated Cost:** $3.00

---

## Objective

Implement the foundational benchmark infrastructure: BenchmarkAdapter base class, dataclasses for benchmark tasks and results, YAML results schema, and CARBON computation function using the existing carbon.yml configuration.

---

## Context

This task creates the core types and interfaces that all other Wave A tasks depend on. The benchmark suite will run SimDecisions-augmented workflows against baselines, measuring accuracy, cost (CLOCK/COIN/CARBON), and recovery rate. CARBON computation uses model-specific energy factors and regional grid intensity from `.deia/config/carbon.yml`.

### Q88N Decisions (binding)

- **CARBON formula:** `carbon_kg = (tokens_in × input_kwh_per_1k + tokens_out × output_kwh_per_1k) / 1000 × grid_carbon_intensity_kg_per_kwh`
- **Results format:** YAML (schema defined in this task)
- **Three currencies:** CLOCK (wall time), COIN (USD from API), CARBON (computed from tokens + model)
- **No external benchmarks yet:** Wave A uses 5 trivial PRISM-IR test tasks only

---

## Files to Read First

- `docs/specs/SPEC-BENCHMARK-SUITE-001.md`
  Full spec with architecture, results schema, and Wave A requirements

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/config/carbon.yml`
  CARBON config with per-model energy factors and regional grid intensities

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/statistics.py`
  Reference for dataclass patterns and statistical types (RunningStats, etc.)

---

## Deliverables

Create new directory and files:

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/` (new directory)
- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/__init__.py`
- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/types.py`
  - `BenchmarkTask` dataclass (id, benchmark_name, benchmark_version, track, trial, model, task_data)
  - `BaselineResult` dataclass (task_id, track="baseline", output, clock_seconds, coin_usd, carbon_kg, tokens_in, tokens_out, model_calls, started_at, completed_at, metadata)
  - `SimResult` dataclass (task_id, track="simdecisions", output, clock_seconds, coin_usd, carbon_kg, tokens_in, tokens_out, model_calls, started_at, completed_at, metadata, ir_used)
  - `EvalResult` dataclass (task_id, passed, partial_credit, score_metadata)
  - `BenchmarkResult` dataclass (benchmark, benchmark_version, simdecisions_version, task_id, track, trial, model, score, currencies, recovery, metadata)

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/adapter.py`
  - `BenchmarkAdapter` abstract base class with:
    - `name: str` (property)
    - `version: str` (property)
    - `load_tasks() -> list[BenchmarkTask]` (abstract method)
    - `task_to_ir(task: BenchmarkTask) -> dict` (abstract method)
    - `run_baseline(task: BenchmarkTask, model: str) -> BaselineResult` (abstract method)
    - `run_simdecisions(task: BenchmarkTask, ir: dict, model: str) -> SimResult` (abstract method)
    - `evaluate(task: BenchmarkTask, output) -> EvalResult` (abstract method)

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/carbon.py`
  - `compute_carbon(model: str, tokens_in: int, tokens_out: int, region: str = "us_average") -> float`
    - Load carbon.yml config
    - Look up model energy factors (input_kwh_per_1k, output_kwh_per_1k)
    - Look up region grid intensity (default to us_average if not found)
    - Apply formula: `(tokens_in × input_kwh_per_1k + tokens_out × output_kwh_per_1k) / 1000 × grid_carbon_intensity_kg_per_kwh`
    - Return carbon in kg CO2e

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/schemas.py`
  - `RESULT_SCHEMA` constant: YAML schema string matching the results schema from SPEC-BENCHMARK-SUITE-001 section 1.4
  - `validate_result(result: dict) -> bool` function
  - Helper functions for serializing BenchmarkResult to YAML

---

## Test Requirements

Create test directory and files:

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/benchmark/` (new directory)
- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/benchmark/__init__.py`
- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/benchmark/test_types.py`
  - Test all 5 dataclasses instantiate correctly
  - Test serialization to dict
  - Test deserialization from dict
  - 8 tests minimum

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/benchmark/test_adapter.py`
  - Test BenchmarkAdapter cannot be instantiated (abstract)
  - Test concrete adapter subclass with mock implementations
  - 4 tests minimum

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/benchmark/test_carbon.py`
  - Test compute_carbon() with claude-sonnet-4-5 (known model from carbon.yml)
  - Test compute_carbon() with different regions (us_average, california, france)
  - Test compute_carbon() with unknown model raises error
  - Test compute_carbon() with unknown region falls back to default
  - Test carbon.yml file loads correctly
  - Test formula accuracy: given tokens_in=10000, tokens_out=5000, model=claude-sonnet-4-5, region=us_average, verify exact carbon_kg output
  - 8 tests minimum

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/benchmark/test_schemas.py`
  - Test RESULT_SCHEMA constant is valid YAML
  - Test validate_result() with valid result dict
  - Test validate_result() with missing required fields
  - Test serialization of BenchmarkResult to YAML matches schema
  - 6 tests minimum

**Total test count:** 26 minimum (8 + 4 + 8 + 6)

**TDD required:** Write tests first, then implementation

---

## Acceptance Criteria

- [ ] `simdecisions/benchmark/__init__.py` created with public API exports
- [ ] `simdecisions/benchmark/types.py` with 5 dataclasses: `BenchmarkTask`, `BaselineResult`, `SimResult`, `EvalResult`, `BenchmarkResult`
- [ ] `simdecisions/benchmark/adapter.py` with abstract `BenchmarkAdapter` class (5 abstract methods: `load_tasks`, `task_to_ir`, `run_baseline`, `run_simdecisions`, `evaluate`)
- [ ] `simdecisions/benchmark/carbon.py` with `compute_carbon()` function loading from `.deia/config/carbon.yml`
- [ ] `simdecisions/benchmark/schemas.py` with `RESULT_SCHEMA` constant and `validate_result()` function
- [ ] Tests in `tests/simdecisions/benchmark/test_types.py` -- 8+ tests passing (instantiation, serialization, deserialization for all 5 dataclasses)
- [ ] Tests in `tests/simdecisions/benchmark/test_adapter.py` -- 4+ tests passing (abstract instantiation guard, concrete subclass with mocks)
- [ ] Tests in `tests/simdecisions/benchmark/test_carbon.py` -- 8+ tests passing (known model, regions, unknown model error, unknown region fallback, formula accuracy)
- [ ] Tests in `tests/simdecisions/benchmark/test_schemas.py` -- 6+ tests passing (valid YAML, valid/invalid result dicts, serialization)
- [ ] CARBON formula matches: `(tokens_in * input_kwh_per_1k + tokens_out * output_kwh_per_1k) / 1000 * grid_carbon_intensity_kg_per_kwh`
- [ ] No file exceeds 500 lines

---

## Constraints

- No file over 500 lines (modularize: types.py, adapter.py, carbon.py, schemas.py)
- No hardcoded colors (N/A for this task)
- All file paths absolute
- No stubs — full implementation
- CARBON formula must match SPEC exactly
- Must load carbon.yml from `.deia/config/carbon.yml` at runtime, not embed values

---

## Dependencies

This task has no dependencies. All other Wave A tasks depend on this one.

**Blocks:** BENCH-001.5, BENCH-002, BENCH-003, BENCH-005

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:

`C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/responses/20260413-TASK-BENCH-001-RESPONSE.md`

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
