# TASK-DES-INVESTIGATE-001 — DES Engine Deep Investigation
## Code Review + Live Simulation Verification

**Priority:** P1
**Model:** Opus
**Type:** Research and verification only — no code changes, no fixes, no refactoring
**Date:** 2026-04-06

---

## Objective

Documented claims exist about what the DES engine can do. Verify them against actual code and
prove them with live simulation runs. At the end of this task the answer to each of these
questions must be clear: what actually works, what is wired, what is broken, and what the engine
can demonstrably produce today.

---

## Part 1 — Code Review: Verify Every Capability Claim

Read each file listed below. For each claimed capability, verify it exists in code, is not a
stub, and has passing tests. Report file path, line numbers, and a one-line verdict:
**CONFIRMED**, **PARTIAL**, or **STUB**.

### Files to read

- `simdecisions/des/core.py`
- `simdecisions/des/engine.py`
- `simdecisions/des/sweep.py`
- `simdecisions/des/replication.py`
- `simdecisions/des/resources.py`
- `simdecisions/des/tokens.py`
- `simdecisions/des/distributions.py`
- `simdecisions/des/statistics.py`
- `simdecisions/des/ledger_adapter.py`
- `simdecisions/des/replay.py` (if exists)
- `simdecisions/des/trace_writer.py` (if exists)
- All test files in `tests/simdecisions/` covering DES
- `simdecisions/optimization/core.py`
- `simdecisions/surrogates/` — full directory (if exists)
- `simdecisions/dialects/` — full directory (if exists)

### Capabilities to verify

| Capability | Claimed Location | Verify |
|------------|-----------------|--------|
| Priority-queue event scheduler | core.py | Code exists + tests pass |
| 14 statistical distributions | distributions.py | Count them, name them all |
| Seeded RNG reproducibility | engine.py | Same seed = identical output |
| Welford online statistics | statistics.py | Implementation not scipy |
| Time-weighted metrics | statistics.py | Confirm |
| Little's Law verification | statistics.py | Confirm |
| MSER-5 warmup detection | replication.py | Confirm |
| Cornish-Fisher CI without scipy | replication.py | Confirm |
| Common Random Numbers variance reduction | replication.py | Confirm |
| Paired A/B comparison | replication.py | Confirm |
| Full factorial parameter sweep | sweep.py | Confirm |
| Sensitivity analysis OAT + Pearson | sweep.py | Confirm |
| Checkpoint / fork / restore | engine.py | Confirm all three operations |
| Step-forward replay | replay.py | Confirm |
| Step-backward replay (rebuild from start) | replay.py | Confirm |
| Playback speed control 0.1x–100x | replay.py | Confirm |
| Visualization hooks on_event / on_frame | replay.py | Confirm hooks exist and are callable |
| Trace levels: minimal / standard / verbose | trace_writer.py | Confirm all three |
| JSONL export/import | trace_writer.py | Confirm round-trip |
| Ledger adapter to_ledger_event() | ledger_adapter.py | Confirm schema match to Event Ledger |
| 6 queue disciplines in resources | resources.py | Name all 6 |
| 12 token states | tokens.py | Name all 12 |
| Pareto frontier computation | optimization/core.py | Confirm |
| Surrogate drift detection | surrogates/drift.py | Confirm |
| BPMN dialect compiler | dialects/ | Confirm bidirectional |
| SBML dialect compiler | dialects/ | Confirm |
| L-systems compiler | dialects/ | Confirm |
| English→IR roundtrip validation | dialects/roundtrip.py | Confirm |

---

## Part 2 — Integration Audit: What Is Actually Wired

For each connection point below, trace the actual code path. Verdict must be one of:
- **WIRED** — works end to end, confirmed by code trace
- **PARTIAL** — one direction works or incomplete path
- **ADJACENT** — both sides exist in code, not connected
- **MISSING** — one or both sides do not exist

| Connection | Expected Path | Verdict |
|------------|---------------|---------|
| Canvas → PHASE-IR → DES run | Canvas export → API → engine | ? |
| DES ledger_adapter → Event Ledger write | to_ledger_event() → ledger.append() | ? |
| Surrogate pipeline ← live ledger data | ledger query → training dataset | ? |
| Replay hooks → any UI component | on_event/on_frame → frontend | ? |
| Pareto frontier → any display | optimization result → UI | ? |
| Alterverse branch → visual comparison | fork() → diff view | ? |
| Sweep API route → sweep.py | POST /api/des/sweep → parameter_sweep() | ? |
| Sensitivity API route → sweep.py | POST /api/des/sensitivity → sensitivity_analysis() | ? |
| DES run → Three Currencies ledger event | run complete → CLOCK/COIN/CARBON written | ? |

---

## Part 3 — Live Simulation Runs

Run the following simulations using the actual engine. Use existing API routes or call Python
directly. Capture real output — not mocked, not described. Actual numbers.

If a simulation fails to run, capture the exact error and stop that simulation. Do not fabricate
output.

### Simulation 1: Basic flow, single run

Define a minimal PHASE-IR flow:
- Source node: Poisson arrivals, rate 10/hr
- Queue node: FIFO, capacity 20
- Service node: exponential service time, mean 5 min, 3 servers
- Sink node

Run to completion (simulate 8 hours). Report:
- Throughput (entities/hr)
- Mean cycle time (min)
- Queue utilization (%)
- Server utilization (%)
- Any ledger events emitted (count and types)

### Simulation 2: Monte Carlo replication

Same flow as Simulation 1. Run 30 replications with different seeds. Report:
- Mean cycle time with 95% CI
- Throughput with 95% CI
- Whether MSER-5 warmup detection triggered and at what replication
- How many replications before precision threshold met (if early stopping triggered)
- Total wall-clock time for 30 replications

### Simulation 3: Checkpoint and fork (Alterverse)

Run the Simulation 1 flow to T=60min. Take a checkpoint. Fork two branches:
- Branch A: increase server count from 3 to 5, run to T=120min
- Branch B: reduce arrival rate from 10/hr to 7/hr, run to T=120min
- Branch 0 (baseline): no changes, run to T=120min

Report for each branch at T=120min:
- Mean cycle time
- Queue depth
- Server utilization
- Which branch performed best on cycle time
- Which branch performed best on utilization

### Simulation 4: Parameter sweep

Sweep two parameters, full factorial:
- Server count: [1, 2, 3, 4, 5]
- Arrival rate: [5/hr, 10/hr, 15/hr, 20/hr]

20 combinations total. Report:
- Best configuration for minimum cycle time
- Best configuration for maximum throughput
- Pareto frontier if optimizing both simultaneously
- Sensitivity: which parameter has highest elasticity on cycle time (Pearson correlation)
- Full results table: server_count × arrival_rate → cycle_time, utilization

### Simulation 5: Dialect compiler — BPMN

Locate an existing BPMN file in the codebase, or create a minimal one representing the
Simulation 1 flow (source → queue → service → sink). Run it through the BPMN compiler to
PHASE-IR. Validate the resulting IR. Run it through the DES engine. Report:
- Did the compiler produce valid IR (yes/no)
- Did the DES run without error (yes/no)
- Any structural differences between hand-written IR and compiled IR
- Compiler round-trip: IR → BPMN → IR, does it match

### Simulation 6: Surrogate pipeline

Attempt to use the sweep results from Simulation 4 as a training dataset for the surrogate
pipeline.

If wired: train a gradient boost surrogate on the 20 sweep results. Predict cycle time for
server_count=4, arrival_rate=12/hr (not in the sweep). Run the actual DES for that configuration.
Report: predicted vs actual, error %.

If not wired to live data: report exactly what function calls or data format changes would be
needed to connect sweep output to surrogate training input. What does the surrogate expect as
input format? What does sweep produce? Where is the gap?

---

## Part 4 — Honest Gap Report

### 4.1 Confirmed capabilities

List every capability from Part 1 that is CONFIRMED, with the evidence: file path, line
numbers, test file that covers it, and one sentence on what you saw in the code.

### 4.2 Overstated or unverified capabilities

List every capability that came back PARTIAL or STUB. No judgment. Just: what was claimed,
what was actually found, and what would be needed to make the claim true.

### 4.3 Integration gap list

List every connection from Part 2 that is not WIRED. Order by impact: which gap, if closed,
would make the most capability visible to a user? For each gap: what is the missing piece, how
many lines of code is a rough estimate to close it?

---

## Part 5 — Calibration Recommendation

Based on findings from Parts 1–4: what is the realistic scope of work to make the DES engine
visually exposed and demonstrable to a non-technical observer watching a screen?

Answer in tasks, not hours. Name the three highest-leverage tasks that would have the most
impact. For each task: one sentence on what it does, one sentence on what it unlocks.

---

## Constraints

- No code changes
- No fixes
- No refactoring
- No improvements
- Investigation and reporting only
- Simulation runs are permitted — read and execute, do not modify
- If a simulation fails, report the error exactly as received

## Acceptance Criteria

- [ ] All 28 capabilities in Part 1 have a verdict (CONFIRMED / PARTIAL / STUB)
- [ ] All 9 integration connections in Part 2 have a verdict
- [ ] All 6 simulations attempted — actual output or exact error captured for each
- [ ] Part 4 gap report contains no fabricated claims — only what was seen in code or output
- [ ] Part 5 names exactly 3 highest-leverage tasks with justification

## Deliverable

8-section response file on completion. Parts 1–5 as subsections within section 3 (What Was Done).
Simulation output as literal output blocks, not paraphrased.
