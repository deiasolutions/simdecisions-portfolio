# TASK-226: Phase-IR Pipeline Flow Module

## Objective

Create a pipeline flow module that converts Phase-IR execution traces into pipeline stage metrics (stage durations, bottleneck identification, throughput calculations).

## Context

**What exists:**
- Phase-IR library at `engine/phase_ir/` with 248 passing tests and 15 API endpoints
- Pipeline simulation endpoint at `hivenode/routes/pipeline_sim.py` (TASK-228)
- DES engine at `engine/des/` for discrete event simulation

**What this task creates:**
A bridge module that reads Phase-IR execution traces and computes flow metrics:
- Stage durations (min, max, avg, p50, p95)
- Bottleneck identification (stage with highest avg WIP)
- Throughput calculations (specs/hour)
- WIP distribution by stage
- Cycle time analysis (time from start to done)

**How it will be used:**
- TASK-228 (`pipeline_sim.py`) loads pipeline IR via `_load_pipeline_ir()`
- This module provides utilities to analyze trace data from DES runs
- Results feed into `/api/pipeline/simulate` response

## Files to Read First

**Phase-IR core:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\__init__.py` (81 exports)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\primitives.py` (core data structures)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\schema.py` (flow serialization)

**DES engine (for trace structure):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\engine.py` (SimulationEngine)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\core.py` (SimConfig)

**Pipeline simulation (consumer):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\pipeline_sim.py` (253 lines)

**Check for existing schema:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\schemas\pipeline.ir.json` (if exists)

## Files You May Modify

**Maximum 3 files:**

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\pipeline_flow.py` (NEW)
   - Create module with flow analysis functions

2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\engine\phase_ir\test_pipeline_flow.py` (NEW)
   - Create comprehensive test suite (minimum 8 tests)

3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\__init__.py` (MODIFY)
   - Add exports for pipeline_flow functions

## Files You Must NOT Modify

- **NO modifications to `browser/`** — frontend is protected (recovery work)
- **NO modifications to `hivenode/routes/`** — pipeline_sim.py is complete
- **NO modifications to other Phase-IR modules** — only pipeline_flow.py
- **NO modifications to DES engine** — engine/des/ is stable

## Deliverables

- [ ] **Create `engine/phase_ir/pipeline_flow.py`** with these functions:
  - `calculate_stage_durations(trace_data: list[dict]) -> dict[str, dict]`
    - Returns: `{"stage_name": {"min": float, "max": float, "avg": float, "p50": float, "p95": float}}`
  - `identify_bottleneck(wip_distribution: dict[str, float]) -> str`
    - Returns: stage name with highest avg WIP
  - `calculate_throughput(specs_completed: int, sim_time_hours: float) -> float`
    - Returns: specs per hour
  - `calculate_wip_distribution(trace_data: list[dict]) -> dict[str, float]`
    - Returns: `{"stage_name": avg_wip_count}`
  - `calculate_cycle_time(trace_data: list[dict]) -> dict`
    - Returns: `{"avg": float, "min": float, "max": float, "p95": float}`

- [ ] **All functions fully implemented** (no stubs, no TODO comments)

- [ ] **Type hints on all functions** (use `from typing import ...` as needed)

- [ ] **Docstrings with Args/Returns sections** for every public function

- [ ] **Update `engine/phase_ir/__init__.py`** to export new functions

- [ ] **Create comprehensive test file** (minimum 8 tests, TDD approach)

## Test Requirements

**Create:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\engine\phase_ir\test_pipeline_flow.py`

- [ ] **Tests written FIRST** (TDD)
- [ ] **Minimum 8 tests:**
  1. Test `calculate_stage_durations()` with valid trace data
  2. Test `calculate_stage_durations()` with empty trace
  3. Test `identify_bottleneck()` with valid WIP distribution
  4. Test `identify_bottleneck()` with empty distribution
  5. Test `calculate_throughput()` with valid inputs
  6. Test `calculate_throughput()` with zero time (edge case)
  7. Test `calculate_wip_distribution()` with valid trace
  8. Test `calculate_cycle_time()` with valid trace
- [ ] **All tests pass**
- [ ] **No stubs** — every test fully implemented
- [ ] **Test file under 500 lines**

**Minimum: 8 tests**

## Constraints

- **No file over 500 lines** — modularize if needed
- **No stubs** — every function fully implemented
- **Absolute paths** in all file references
- **TDD** — write tests first
- **No hardcoded values** — use function parameters
- **Type safety** — use type hints everywhere

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260319-TASK-226-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy deliverables from above, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Acceptance Criteria

- [ ] 8+ tests written and passing
- [ ] `pipeline_flow.py` created with all 5 functions
- [ ] All functions have type hints and docstrings
- [ ] No stubs or TODO comments
- [ ] Exports added to `__init__.py`
- [ ] All existing Phase-IR tests still pass (no regressions)
- [ ] No file over 500 lines

## Build Verification Commands

```bash
# Run new pipeline flow tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter && python -m pytest tests/engine/phase_ir/test_pipeline_flow.py -v

# Regression check: all Phase-IR tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter && python -m pytest tests/engine/phase_ir/ -v

# Full engine test suite
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter && python -m pytest tests/engine/ -v
```

## Dependencies

- **Depends on:** Phase-IR library (already exists, 248 tests passing)
- **Used by:** TASK-228 (pipeline_sim.py) — already complete, will import this module
- **Can run in parallel:** Yes — no conflicts with other tasks

## Notes for Bee

1. **Trace data structure:** Examine DES engine output to understand trace format. Each trace entry should have: timestamp, stage, token_id, event_type (enter/exit).

2. **Statistics calculation:** Use Python's `statistics` module for percentile calculations (p50, p95).

3. **WIP calculation:** WIP = work in progress = number of tokens in a stage at a given time. Track enter/exit events to compute time-weighted average.

4. **Bottleneck heuristic:** Stage with highest average WIP is the bottleneck (Little's Law: WIP = Throughput × Cycle Time).

5. **Edge cases to handle:**
   - Empty trace data → return zeros or empty dicts
   - Zero simulation time → avoid division by zero
   - Missing stage names → skip or use "unknown"
   - Malformed trace entries → log warning and skip

6. **Type hints example:**
   ```python
   from typing import Dict, List, Union

   def calculate_stage_durations(trace_data: List[dict]) -> Dict[str, Dict[str, float]]:
       """Calculate stage duration statistics from trace data.

       Args:
           trace_data: List of trace event dicts with timestamp, stage, event_type

       Returns:
           Dict mapping stage names to duration stats (min, max, avg, p50, p95)
       """
       ...
   ```

7. **Test pattern:**
   ```python
   import pytest
   from engine.phase_ir.pipeline_flow import calculate_stage_durations

   def test_calculate_stage_durations_valid_trace():
       trace = [
           {"timestamp": 0, "stage": "parse", "event_type": "enter", "token_id": "t1"},
           {"timestamp": 5, "stage": "parse", "event_type": "exit", "token_id": "t1"},
       ]
       result = calculate_stage_durations(trace)
       assert "parse" in result
       assert result["parse"]["avg"] == 5.0
   ```

8. **Integration note:** This module is a library, not an endpoint. It provides utilities for other code to use. No FastAPI routes needed.

---

**End of Task File**
