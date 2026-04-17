# SPEC-DES-INVESTIGATE-001: DES Engine Deep Investigation

**MODE: EXECUTE**

## Priority
P1

## Model Assignment
opus

## Role
bee

## Objective

Verify every capability claim about the DES engine against actual code and prove them with live simulation runs. Produce an honest gap report: what works, what's wired, what's broken, what the engine can demonstrably produce today.

## Context

The benchmark suite (SPEC-BENCHMARK-SUITE-001) depends on the SimDecisions loop (DEF → SIM → BRA → COMP → DEC → EXE) working end-to-end. This investigation gates Wave B of that spec. We need ground truth on the engine's state.

## Files to Read First

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/core.py`
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/engine.py`
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/sweep.py`
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/replication.py`
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/resources.py`
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/tokens.py`
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/distributions.py`
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/statistics.py`
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/ledger_adapter.py`
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/optimization/core.py`
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/tasks/TASK-DES-INVESTIGATE-001.md` — full investigation protocol with 28 capabilities, 9 integration connections, 6 live simulations

## Deliverables

- [ ] All 28 capabilities from the investigation protocol have a verdict (CONFIRMED / PARTIAL / STUB)
- [ ] All 9 integration connections have a verdict (WIRED / PARTIAL / ADJACENT / MISSING)
- [ ] All 6 simulations attempted with actual output or exact error captured
- [ ] Part 4 gap report with no fabricated claims
- [ ] Part 5 names exactly 3 highest-leverage tasks with justification

## Acceptance Criteria

- [ ] Investigation protocol from TASK-DES-INVESTIGATE-001 followed in full (Parts 1-5)
- [ ] Response file written with all 8 mandatory sections
- [ ] No code changes made — investigation and reporting only
- [ ] Simulation runs use actual engine output, not mocked data

## Constraints

- No code changes, no fixes, no refactoring
- Investigation and reporting only
- Simulation runs permitted — read and execute, do not modify
- If a simulation fails, capture the exact error and stop that simulation
