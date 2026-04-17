---
id: BENCH-009
priority: P1
model: sonnet
role: bee
depends_on: [BENCH-007, BENCH-008]
---

# SPEC-BENCH-009: PRISM-bench Adapter Wiring

## Priority
P1

## Depends On
- BENCH-007 (20 PRISM-bench tasks must exist)
- BENCH-008 (PRISMBenchHarness must be implemented)

## Model Assignment
sonnet

## Objective

Replace placeholder implementations in simdecisions/benchmark/adapters/prism_bench.py with real DES execution, wiring the adapter to load tasks from prism_bench_tasks/ directory, execute workflows through SimulationEngine (baseline and SimDecisions tracks), and evaluate results using PRISMBenchHarness. The adapter must handle DES statistics collection (wired in SPEC-DES-STATS-WIRING-001) and return complete BenchmarkResult objects matching the results schema from SPEC-BENCHMARK-SUITE-001.

## Files to Read First

- docs/specs/SPEC-BENCHMARK-SUITE-001.md
- simdecisions/benchmark/adapters/prism_bench.py
- simdecisions/benchmark/adapter.py
- simdecisions/benchmark/types.py
- simdecisions/des/engine.py
- simdecisions/des/core.py
- simdecisions/des/statistics.py
- simdecisions/benchmark/harness.py
- .deia/hive/queue/SUBMISSION-CHECKLIST.md

## Acceptance Criteria

- [ ] Method `PRISMBenchAdapter.load_tasks()` loads from `simdecisions/benchmark/prism_bench_tasks/` (not test_workflows)
- [ ] Method `PRISMBenchAdapter.load_tasks()` returns 20 BenchmarkTask objects (one per JSON file in prism_bench_tasks/)
- [ ] Method `PRISMBenchAdapter.run_baseline(task, model)` executes workflow using SimulationEngine in sim mode with no production executors
- [ ] Method `PRISMBenchAdapter.run_simdecisions(task, ir, model)` executes workflow using SimulationEngine with DEF→SIM→BRA→COMP→DEC→EXE loop (placeholder for now, real implementation in later wave)
- [ ] Both run methods capture wall time (CLOCK), query Event Ledger for COIN via ledger_utils.query_task_cost(), count model_calls via ledger_utils.count_model_calls()
- [ ] Both run methods compute CARBON using carbon.compute_carbon() from tokens_in/tokens_out
- [ ] Method `PRISMBenchAdapter.evaluate(task, output)` calls PRISMBenchHarness.evaluate() with workflow metadata and result dict
- [ ] Adapter extracts DES statistics from SimulationEngine context after run: tokens_created, tokens_completed, cycle_time, throughput
- [ ] BaselineResult and SimResult objects include all fields from types.py: task_id, track, output, currencies, started_at, completed_at, metadata
- [ ] Integration test `tests/simdecisions/benchmark/test_prism_bench_adapter.py` runs one task through both tracks and verifies result format
- [ ] Integration test verifies result.currencies has all 6 fields: clock_seconds, coin_usd, carbon_kg, tokens_in, tokens_out, model_calls
- [ ] Integration test verifies DES statistics are captured in result.metadata
- [ ] Test loads all 20 tasks and verifies each has task_id matching workflow id
- [ ] Test verifies evaluate() returns EvalResult with score, partial_credit, score_metadata

## Files to Modify

| File Path | Purpose |
|-----------|---------|
| `simdecisions/benchmark/adapters/prism_bench.py` | Replace placeholders with real execution |
| `tests/simdecisions/benchmark/test_prism_bench_adapter.py` | Integration tests |

## Smoke Test

- [ ] `python -c "from simdecisions.benchmark.adapters.prism_bench import PRISMBenchAdapter; a = PRISMBenchAdapter(); tasks = a.load_tasks(); print(len(tasks))"` prints 20
- [ ] `pytest tests/simdecisions/benchmark/test_prism_bench_adapter.py -v` passes all tests
- [ ] `pytest tests/simdecisions/benchmark/test_prism_bench_adapter.py::test_baseline_execution -v` passes
- [ ] `pytest tests/simdecisions/benchmark/test_prism_bench_adapter.py::test_simdecisions_execution -v` passes

## Constraints

- No file over 500 lines
- No stubs — every method fully implemented
- No git operations
- TDD: write tests first, then implementation
- Use existing SimulationEngine from simdecisions.des.engine (do not reimplement DES logic)
- Use existing ledger_utils from simdecisions.benchmark.ledger_utils (do not duplicate ledger queries)
- Use existing carbon.compute_carbon() for CARBON calculation
- Use existing PRISMBenchHarness from BENCH-008 for evaluation
- DES statistics must come from StatisticsCollector in engine context, not recomputed
- For now, run_simdecisions() can use same execution path as run_baseline() (real DEF→SIM→BRA→COMP loop comes in later wave)

## Implementation Guide

### load_tasks() Implementation

```python
def load_tasks(self) -> list[BenchmarkTask]:
    """Load all 20 PRISM-bench tasks from prism_bench_tasks/ directory."""
    # Update workflow_dir to point to prism_bench_tasks instead of test_workflows
    workflow_dir = Path(__file__).parent.parent / "prism_bench_tasks"

    # Load all .json files (should be 20 files from BENCH-007)
    workflow_files = sorted(workflow_dir.glob("*.json"))

    tasks = []
    for workflow_file in workflow_files:
        with open(workflow_file, "r", encoding="utf-8") as f:
            workflow_data = json.load(f)

        task = BenchmarkTask(
            id=workflow_data["id"],
            benchmark_name="prism-bench",
            benchmark_version="0.1.0",
            track="",
            trial=0,
            model="",
            task_data=workflow_data,
        )
        tasks.append(task)

    return tasks
```

### run_baseline() Implementation

```python
def run_baseline(self, task: BenchmarkTask, model: str) -> BaselineResult:
    """Execute task with raw model (no SimDecisions)."""
    from simdecisions.des.engine import SimulationEngine
    from simdecisions.des.core import SimConfig
    import time

    # Create engine and load workflow
    engine = SimulationEngine()
    config = SimConfig(seed=42, max_sim_time=1000.0)
    ctx = engine.load(task.task_data, config)

    # Measure wall time
    started_at = datetime.now()
    wall_start = time.time()

    # Run simulation
    ctx = engine.run(ctx)

    wall_end = time.time()
    completed_at = datetime.now()
    clock_seconds = wall_end - wall_start

    # Extract DES statistics
    stats = ctx["stats"].summary(ctx["state"].clock.sim_time)

    # Query ledger for COIN, tokens, model_calls (placeholder for now)
    # In real execution, ledger would be attached to ctx
    coin_usd = 0.0  # Placeholder
    tokens_in = 0
    tokens_out = 0
    model_calls = 0

    # Compute CARBON
    from simdecisions.benchmark.carbon import compute_carbon
    carbon_kg = compute_carbon(model, tokens_in, tokens_out)

    # Build result
    return BaselineResult(
        task_id=task.id,
        track="baseline",
        output=stats,  # DES statistics as output
        clock_seconds=clock_seconds,
        coin_usd=coin_usd,
        carbon_kg=carbon_kg,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        model_calls=model_calls,
        started_at=started_at,
        completed_at=completed_at,
        metadata={"des_stats": stats},
    )
```

### run_simdecisions() Implementation

For Wave B, this can mirror run_baseline() since the real DEF→SIM→BRA→COMP loop is not yet implemented. The placeholder should still use SimulationEngine and return a valid SimResult:

```python
def run_simdecisions(self, task: BenchmarkTask, ir: dict, model: str) -> SimResult:
    """Execute task through SimDecisions loop (Wave B: same as baseline)."""
    # Same execution as baseline for now
    # Real DEF→SIM→BRA→COMP implementation comes in later wave
    baseline_result = self.run_baseline(task, model)

    # Convert to SimResult
    return SimResult(
        task_id=baseline_result.task_id,
        track="simdecisions",
        output=baseline_result.output,
        clock_seconds=baseline_result.clock_seconds,
        coin_usd=baseline_result.coin_usd,
        carbon_kg=baseline_result.carbon_kg,
        tokens_in=baseline_result.tokens_in,
        tokens_out=baseline_result.tokens_out,
        model_calls=baseline_result.model_calls,
        started_at=baseline_result.started_at,
        completed_at=baseline_result.completed_at,
        metadata=baseline_result.metadata,
        ir_used=ir,
    )
```

### evaluate() Implementation

```python
def evaluate(self, task: BenchmarkTask, output) -> EvalResult:
    """Score output using PRISMBenchHarness."""
    from simdecisions.benchmark.harness import PRISMBenchHarness

    harness = PRISMBenchHarness()

    # Build result dict for harness
    result_dict = {
        "task_id": task.id,
        "currencies": {
            "clock_seconds": output.get("mean_cycle_time", 0.0),
            "coin_usd": 0.0,
            "carbon_kg": 0.0,
            "tokens_in": 0,
            "tokens_out": 0,
            "model_calls": 0,
        },
        "recovery": {
            "errors_encountered": 0,
            "errors_recovered": 0,
            "human_interventions": 0,
        },
        "metadata": output,
    }

    eval_result = harness.evaluate(task.task_data, result_dict)

    return EvalResult(
        task_id=task.id,
        passed=eval_result["score"] >= 0.7,  # 70% threshold
        partial_credit=eval_result["partial_credit"],
        score_metadata=eval_result,
    )
```

### Test Structure

Minimum 5 tests:
1. `test_load_tasks()` — verify 20 tasks loaded
2. `test_baseline_execution()` — run one task through baseline, verify result format
3. `test_simdecisions_execution()` — run one task through simdecisions, verify SimResult
4. `test_evaluate()` — verify EvalResult returned with score
5. `test_des_statistics_captured()` — verify DES stats in result.metadata
