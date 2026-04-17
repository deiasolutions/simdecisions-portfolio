# SPEC-BENCH-WAVE-A-DECOMPOSE: Decompose Benchmark Suite Wave A into Bee Task Files

**MODE: EXECUTE**

## Priority
P0

## Model Assignment
sonnet

## Role
queen

## Objective

Create 6 bee-dispatchable task files for Wave A of SPEC-BENCHMARK-SUITE-001. Each task file follows the `.deia/hive/tasks/` format per HIVE.md. Do NOT dispatch bees — return task files for Q33NR review.

## Context

Q88N has approved SPEC-BENCHMARK-SUITE-001 with all blockers resolved. Wave A builds the benchmark infrastructure. Wave B (PRISM-bench) and Wave C (SWE-bench) follow sequentially.

### Q88N Decisions (binding)

**CARBON:** Token-based computation using `.deia/config/carbon.yml`. Formula: `carbon_kg = (tokens_in × input_kwh_per_1k + tokens_out × output_kwh_per_1k) / 1000 × grid_carbon_intensity_kg_per_kwh`. Config already exists with per-model energy factors and regional grid intensities.

**CLI:** Standalone script at `_tools/benchmark.py`. Thin alias in hivenode shell (not a shell subcommand).

**Factory format:** Wrap benchmark tasks in standard SPEC-*.md format. One format, one queue.

**5 test workflows:** New task BENCH-001.5 creates them. Assign haiku.

**benchmarks.yml:** Created as part of BENCH-002 deliverable, not a separate task.

**Results:** Local first at `.deia/benchmark/results/`. Publish to public repo manually.

**model_calls:** Count Event Ledger entries per task. No new instrumentation.

**Budget:** max_coin_per_run=$50, max_clock_per_task=600s, budget_limit_usd=$0.50 per task item.

**gpt-5.4:** Deferred to Wave C. Wave A uses claude-sonnet-4-5 only.

### Wave A Tasks to Decompose

| Task | Description | Model |
|------|-------------|-------|
| BENCH-001 | BenchmarkAdapter base class, BenchmarkTask/BaselineResult/SimResult/EvalResult dataclasses, results schema (YAML), CARBON computation function using carbon.yml | sonnet |
| BENCH-001.5 | Create 5 trivial PRISM-IR test workflows for Wave A exit validation | haiku |
| BENCH-002 | BenchmarkRunner: manifest loader (benchmarks.yml), budget estimator, factory task generator (wraps in SPEC format), CLI at _tools/benchmark.py | sonnet |
| BENCH-003 | ResultsCollector: poll completed tasks, aggregate per benchmark, compute statistics (Welford online + Mann-Whitney U significance) | sonnet |
| BENCH-004 | Publisher: markdown summary generator, raw JSON exporter, trend chart data | haiku |
| BENCH-005 | Factory integration: benchmark SPEC tasks enter queue, Event Ledger captures three currencies (CLOCK from wall time, COIN from API cost, CARBON from carbon.yml formula), model_calls counted from ledger entries, results written on completion | sonnet |

### Wave A Exit Criteria

`python _tools/benchmark.py estimate prism-bench` displays task count and estimated cost.
`python _tools/benchmark.py run prism-bench --trials 2 --dry-run` shows task list.
`python _tools/benchmark.py run prism-bench --trials 2` completes, writes results to `.deia/benchmark/results/`.
5 trivial PRISM-IR test tasks run through both tracks (baseline + simdecisions).
Statistics computed. Budget estimation works.

### File Locations

All new code lives under the simdecisions repo:
- Benchmark runner + adapters: `simdecisions/benchmark/` (new directory)
- CLI: `_tools/benchmark.py`
- Results: `.deia/benchmark/results/`
- Config: `.deia/config/carbon.yml` (exists)
- Test workflows: `simdecisions/benchmark/test_workflows/` (new)
- Tests: `tests/simdecisions/benchmark/` (new)

### Dependencies Between Tasks

BENCH-001 → BENCH-001.5, BENCH-002, BENCH-003, BENCH-005 (all depend on base classes)
BENCH-002 → BENCH-005 (runner generates tasks, factory integration runs them)
BENCH-003 + BENCH-004 are independent of each other but both depend on BENCH-001
BENCH-005 depends on BENCH-001 and BENCH-002

### Dispatch Order

Round 1 (parallel): BENCH-001, BENCH-001.5
Round 2 (parallel after round 1): BENCH-002, BENCH-003, BENCH-004
Round 3 (after round 2): BENCH-005

## Files to Read First

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/BOOT.md` — task file format, 8-section response template
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/HIVE.md` — Q33N workflow, task file requirements
- `C:/Users/davee/Downloads/SPEC-BENCHMARK-SUITE-001.md` — full spec
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/config/carbon.yml` — CARBON config
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/statistics.py` — Welford implementation (reuse)
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/engine.py` — DES engine interface

## Deliverables

- [ ] 6 task files written to `.deia/hive/tasks/`, named `TASK-BENCH-001.md` through `TASK-BENCH-005.md` (with TASK-BENCH-001-5.md)
- [ ] Each task file has: Objective, Context, Files to Read First, Deliverables, Test Requirements, Constraints, Response Requirements (per HIVE.md template)
- [ ] Dependency order documented in each task
- [ ] No task exceeds scope of a single bee session
- [ ] All file paths are absolute and verified to exist (or marked as "create new")

## Acceptance Criteria

- [ ] All 6 task files follow HIVE.md task file format exactly
- [ ] Each task has concrete acceptance criteria (not vague)
- [ ] TDD requirement included in every task
- [ ] No task references packages/ or other dead paths
- [ ] Budget constraint ($25 total for Wave A dev) is respected in model assignments
- [ ] Task files do NOT dispatch bees — Q33NR must review first

## Constraints

- Do NOT dispatch bees. Write task files only.
- Do NOT write code.
- All file paths must be absolute.
- Follow HIVE.md task file template exactly.
- Return to Q33NR for review before any dispatch.
