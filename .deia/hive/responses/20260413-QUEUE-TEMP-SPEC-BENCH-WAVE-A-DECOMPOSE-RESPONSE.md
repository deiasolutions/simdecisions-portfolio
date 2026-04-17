# QUEUE-TEMP-SPEC-BENCH-WAVE-A-DECOMPOSE — COMPLETE

**Status:** COMPLETE
**Model:** Sonnet (Q33N)
**Date:** 2026-04-13
**Bot ID:** QUEEN-QUEUE-TEMP-SPEC-BENCH-WAVE-A-D

---

## Files Modified

All files created (absolute paths):

1. `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/tasks/TASK-BENCH-001.md`
2. `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/tasks/TASK-BENCH-001-5.md`
3. `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/tasks/TASK-BENCH-002.md`
4. `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/tasks/TASK-BENCH-003.md`
5. `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/tasks/TASK-BENCH-004.md`
6. `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/tasks/TASK-BENCH-005.md`
7. `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/responses/20260413-QUEUE-TEMP-SPEC-BENCH-WAVE-A-DECOMPOSE-RESPONSE.md`

---

## What Was Done

### Task File Creation

Created 6 bee-dispatchable task files for Wave A of SPEC-BENCHMARK-SUITE-001:

**TASK-BENCH-001** — Benchmark Infrastructure Foundation (Sonnet, $3.00)
- BenchmarkAdapter base class
- 5 dataclasses (BenchmarkTask, BaselineResult, SimResult, EvalResult, BenchmarkResult)
- YAML results schema
- CARBON computation function using carbon.yml
- 26 tests minimum (types, adapter, carbon, schemas)

**TASK-BENCH-001.5** — Create 5 Trivial PRISM-IR Test Workflows (Haiku, $0.50)
- 5 minimal PRISM-IR workflow JSON files for end-to-end validation
- Each workflow: 3-8 nodes, <10 second runtime, deterministic pass/fail
- Validation tests (5 tests checking PRISM-IR schema compliance)

**TASK-BENCH-002** — Benchmark Runner Core (Sonnet, $4.00)
- BenchmarkRunner class (manifest loader, adapter getter, budget estimator, task generator)
- Budget estimator module
- CLI at `_tools/benchmark.py` (estimate, run, list subcommands)
- benchmarks.yml config (Wave A: prism-bench only)
- 30 tests minimum (runner, estimator, CLI)

**TASK-BENCH-003** — Results Collector and Statistics (Sonnet, $3.50)
- ResultsCollector class (load, aggregate, compute stats, compare tracks)
- Mann-Whitney U significance test (non-parametric, no scipy)
- Metrics module (coefficient of variation, recovery rate, metric extraction)
- Reuses existing Welford's algorithm from `simdecisions/des/statistics.py`
- 30 tests minimum (collector, significance, metrics)

**TASK-BENCH-004** — Results Publisher (Haiku, $1.00)
- Publisher class (markdown summary, raw JSON, trend CSV)
- Versioned output structure: `.deia/benchmark/results/{benchmark}/YYYY-MM-vX.Y.Z/`
- 12 tests minimum

**TASK-BENCH-005** — Factory Integration (Sonnet, $5.00)
- BenchmarkTaskExecutor (execute baseline/simdecisions, measure currencies, write results)
- Ledger query utilities (query_task_cost, count_model_calls, extract_token_counts)
- Benchmark-specific Event Ledger event types
- 32 tests minimum (executor, ledger utils, events)
- Wave A exit criteria validation included

### Task File Quality Checklist

Each task file includes:
- [x] Objective (one-sentence deliverable)
- [x] Context (Q88N decisions, binding constraints)
- [x] Files to Read First (absolute paths with annotations)
- [x] Deliverables (concrete, checklist format)
- [x] Test Requirements (TDD, specific test count, scenarios)
- [x] Constraints (500-line limit, no stubs, no hardcoded values)
- [x] Dependencies (depends_on, blocks)
- [x] Response Requirements (8-section mandatory template)

### Dependency Order

**Round 1 (parallel):** BENCH-001, BENCH-001.5
**Round 2 (parallel after round 1):** BENCH-002, BENCH-003, BENCH-004
**Round 3 (after round 2):** BENCH-005

### Budget Allocation

Total Wave A development cost estimate: $17.00 (within $25 budget)

| Task | Model | Estimate |
|------|-------|----------|
| BENCH-001 | Sonnet | $3.00 |
| BENCH-001.5 | Haiku | $0.50 |
| BENCH-002 | Sonnet | $4.00 |
| BENCH-003 | Sonnet | $3.50 |
| BENCH-004 | Haiku | $1.00 |
| BENCH-005 | Sonnet | $5.00 |

---

## Test Results

N/A — This is a task decomposition task. No code written, no tests run.

---

## Build Verification

N/A — No code changes. Task files are markdown documentation.

---

## Acceptance Criteria

- [x] All 6 task files follow HIVE.md task file format exactly
- [x] Each task has concrete acceptance criteria (not vague)
- [x] TDD requirement included in every task
- [x] No task references packages/ or other dead paths (verified: all paths use new flattened structure)
- [x] Budget constraint ($25 total for Wave A dev) is respected in model assignments ($17 estimated)
- [x] Task files do NOT dispatch bees — Q33NR must review first (confirmed: deliverables only)
- [x] All file paths are absolute and verified to exist (or marked as "create new")
- [x] Dependency order documented in each task (confirmed: depends_on and blocks sections)
- [x] No task exceeds scope of a single bee session (verified: largest is BENCH-005 at ~500 lines estimated)

---

## Clock / Cost / Carbon

**Clock:** 38 minutes (reading spec, carbon.yml, statistics.py, engine.py, writing 6 task files)
**Cost:** $0.42 (estimated, Sonnet Q33N session)
**Carbon:** 0.018 kg CO2e (estimated using carbon.yml: sonnet, ~28k tokens in, ~14k tokens out, us_average grid)

---

## Issues / Follow-ups

### Recommendations for Q33NR Review

1. **TASK-BENCH-001.5 dependency:** Currently marked as depending on BENCH-001 ("for BenchmarkTask type"), but the workflows are self-contained JSON files. This dependency is soft — could run in true parallel with BENCH-001. Q33NR may choose to dispatch both in Round 1.

2. **BENCH-003 Mann-Whitney U:** Task specifies self-contained implementation. If scipy is acceptable, this could be simplified to `from scipy.stats import mannwhitneyu`. Current spec mandates no scipy to keep dependencies minimal.

3. **BENCH-005 ledger queries:** Task assumes Event Ledger has query API (by task_id, time range). If not implemented, BENCH-005 may need to add ledger query functions or use raw SQL against ledger store.

4. **Wave A exit validation:** BENCH-005 deliverable includes running all 6 exit criteria checks. If any fail, Q33NR should create a P0 fix spec before Wave B starts.

5. **CLI shell alias:** BENCH-002 mentions "thin alias in hivenode shell (not a shell subcommand)". This is not specified as a deliverable. If required, add to BENCH-002 or create follow-up task.

### Test Count Summary

| Task | Min Tests |
|------|-----------|
| BENCH-001 | 26 |
| BENCH-001.5 | 5 |
| BENCH-002 | 30 |
| BENCH-003 | 30 |
| BENCH-004 | 12 |
| BENCH-005 | 32 |
| **Total** | **135** |

All Wave A tasks combined will produce 135+ tests. This establishes strong test coverage for the benchmark infrastructure.

### Next Steps for Q33NR

1. Review all 6 task files against HIVE.md checklist
2. Verify dependency order is correct
3. Approve dispatch or request corrections
4. On approval: dispatch Round 1 (BENCH-001, BENCH-001.5) in parallel
5. Wait for Round 1 completion
6. Dispatch Round 2 (BENCH-002, BENCH-003, BENCH-004) in parallel
7. Wait for Round 2 completion
8. Dispatch Round 3 (BENCH-005)
9. Validate Wave A exit criteria
10. Report to Q88N

---

**Q33N ready for Q33NR review. No bees dispatched. Awaiting approval.**
