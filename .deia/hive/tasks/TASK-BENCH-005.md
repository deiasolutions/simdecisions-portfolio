# TASK-BENCH-005 — Factory Integration

**Priority:** P0
**Model:** Sonnet
**Type:** Code implementation + integration
**Date:** 2026-04-13
**Wave:** A — Infrastructure
**Estimated Cost:** $5.00

---

## Objective

Integrate the benchmark suite with the factory queue: benchmark SPEC tasks enter queue, Event Ledger captures three currencies (CLOCK from wall time, COIN from API cost, CARBON from carbon.yml formula), model_calls counted from ledger entries, results written on completion.

---

## Context

This task closes the loop: BENCH-002 generates SPEC task files, this task ensures they can enter the factory queue, execute, emit ledger events, and write results. Event Ledger already exists (ADR-001); this task adds benchmark-specific event types and result-writing logic.

### Q88N Decisions (binding)

- **Queue integration:** Benchmark SPEC tasks are P2 priority (below production P0/P1)
- **Event Ledger:** Use existing ledger, add benchmark event types
- **model_calls:** Count from ledger entries with event_type matching LLM calls
- **Results writing:** On task completion, write BenchmarkResult YAML to `.deia/benchmark/results/`
- **No auto-dispatch:** Tasks enter queue manually or via queue runner (not implemented in this task)

---

## Files to Read First

- `docs/specs/SPEC-BENCHMARK-SUITE-001.md`
  Section 1.4 (Results Schema), Section 6 (Factory Task Format), Section 7 (Wave A BENCH-005)

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/hivenode/ledger/writer.py`
  Event Ledger write API

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/hivenode/ledger/schema.py`
  Event schema definitions

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/types.py`
  BenchmarkResult dataclass (created by BENCH-001)

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/carbon.py`
  compute_carbon() function (created by BENCH-001)

---

## Deliverables

### Benchmark task executor

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/executor.py`
  - `BenchmarkTaskExecutor` class with methods:
    - `__init__(ledger_writer, adapter: BenchmarkAdapter)` — inject ledger and adapter
    - `execute_baseline(task: BenchmarkTask) -> BaselineResult`
      - Emit ledger event: `benchmark_task_start` (task_id, track, model)
      - Call adapter.run_baseline()
      - Capture wall time (CLOCK)
      - Query ledger for COIN (sum of API cost events during task)
      - Count model_calls from ledger entries
      - Compute CARBON using carbon.compute_carbon(model, tokens_in, tokens_out)
      - Emit ledger event: `benchmark_task_complete` (task_id, currencies, metadata)
      - Return BaselineResult
    - `execute_simdecisions(task: BenchmarkTask, ir: dict) -> SimResult`
      - Same as baseline but call adapter.run_simdecisions()
      - Include ir_used field in SimResult
    - `write_result(result: BaselineResult | SimResult, output_dir: str) -> None`
      - Serialize result to YAML matching RESULT_SCHEMA
      - Write to `.deia/benchmark/results/{benchmark}/{task_id}_{track}_trial{N}.yml`

### Event Ledger extensions

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/hivenode/ledger/benchmark_events.py` (new file)
  - Define benchmark-specific event types:
    - `benchmark_task_start` — (task_id, benchmark, track, trial, model, started_at)
    - `benchmark_task_complete` — (task_id, clock_seconds, coin_usd, carbon_kg, tokens_in, tokens_out, model_calls, completed_at)
    - `benchmark_task_failed` — (task_id, error_message, completed_at)
  - Register event types with ledger schema (import into `hivenode/ledger/schema.py`)

### Ledger query utilities

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/ledger_utils.py`
  - `query_task_cost(ledger, task_id: str, start_time: datetime, end_time: datetime) -> float`
    - Query ledger for all events with matching task_id in time range
    - Sum COIN from API cost events
    - Return total USD
  - `count_model_calls(ledger, task_id: str, start_time: datetime, end_time: datetime) -> int`
    - Query ledger for LLM call events in time range
    - Return count
  - `extract_token_counts(ledger, task_id: str, start_time: datetime, end_time: datetime) -> tuple[int, int]`
    - Sum tokens_in, tokens_out from LLM events
    - Return (total_tokens_in, total_tokens_out)

---

## Test Requirements

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/benchmark/test_executor.py`
  - Test execute_baseline() with mock adapter
  - Test execute_simdecisions() with mock adapter and IR
  - Test CLOCK measurement (wall time captured)
  - Test COIN query from ledger
  - Test CARBON computation delegates to carbon.compute_carbon()
  - Test model_calls counted correctly
  - Test write_result() creates valid YAML file
  - Test YAML matches RESULT_SCHEMA
  - Test ledger events emitted (benchmark_task_start, benchmark_task_complete)
  - 16 tests minimum

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/benchmark/test_ledger_utils.py`
  - Test query_task_cost() with mock ledger data
  - Test count_model_calls() with mock ledger data
  - Test extract_token_counts() with mock ledger data
  - Test edge case: no matching events (returns 0 or empty)
  - Test edge case: multiple tasks in ledger (filters correctly by task_id)
  - 10 tests minimum

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/hivenode/ledger/test_benchmark_events.py`
  - Test benchmark_task_start event schema validates
  - Test benchmark_task_complete event schema validates
  - Test benchmark_task_failed event schema validates
  - Test events serialize to JSON correctly
  - 6 tests minimum

**Total test count:** 32 minimum (16 + 10 + 6)

**TDD required:** Write tests first, then implementation

---

## Constraints

- No file over 500 lines (split: executor.py, ledger_utils.py, benchmark_events.py)
- MUST use existing Event Ledger (hivenode/ledger/) — do NOT create separate logging
- CARBON computation must use carbon.yml (via carbon.compute_carbon())
- Results YAML must validate against RESULT_SCHEMA from BENCH-001
- No stubs
- No hardcoded currency values — all measured or computed

---

## Dependencies

**Depends on:** BENCH-001 (types, carbon), BENCH-002 (task generator creates SPEC files this executor runs)

**Blocks:** Wave A exit criteria (end-to-end run)

---

## Wave A Exit Criteria (validate after this task completes)

After BENCH-005 completes, the following must work:

1. `python _tools/benchmark.py estimate prism-bench` displays task count and estimated cost
2. `python _tools/benchmark.py run prism-bench --trials 2 --dry-run` shows task list
3. `python _tools/benchmark.py run prism-bench --trials 2` completes, writes results to `.deia/benchmark/results/`
4. 5 trivial PRISM-IR test tasks run through both tracks (baseline + simdecisions)
5. Statistics computed (mean, std dev, delta, p-value)
6. Budget estimation works
7. All 6 tasks in Wave A (BENCH-001 through BENCH-005, including BENCH-001.5) have passing tests

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:

`C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/responses/20260413-TASK-BENCH-005-RESPONSE.md`

The response MUST contain these 8 sections:

1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full absolute paths
3. **What Was Done** — bullet list of concrete changes (not intent)
4. **Test Results** — test files run, pass/fail counts, pytest output summary
5. **Build Verification** — did tests pass? Include last 5 lines of pytest output
6. **Acceptance Criteria** — copy from task, mark [x] or [ ] with explanation if not done
7. **Clock / Cost / Carbon** — all three currencies, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, recommended next tasks, **Wave A exit criteria validation results**

DO NOT skip any section.
