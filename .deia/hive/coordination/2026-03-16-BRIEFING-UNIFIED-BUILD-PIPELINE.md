# BRIEFING: Unified Build Pipeline

**Date:** 2026-03-16
**From:** Q88NR (Regent)
**To:** Q33N (Queen Coordinator)
**Source Spec:** SPEC-PIPELINE-001
**Model Assignment:** Sonnet

---

## Objective

Build a unified build pipeline that consolidates five overlapping processes into one coherent system with two runtimes (filesystem-based production mode + DES simulation mode). The pipeline tracks work from Q88N direction through to shipped code, with IR fidelity gates, LLM triage, and Event Ledger integration.

---

## Context from Q88N

The current state has five processes describing overlapping stages:
- PROCESS-0013 (Build Integrity — IR fidelity gates)
- PROCESS-0018 (Living Feature Inventory)
- PROCESS-0016/0019 (Bee Response Format)
- Q33NR directory state machine proposal
- Q33NR dev process flow proposal

None of these processes form a complete end-to-end picture. The queue runner is filesystem-only and cannot simulate pipeline behavior for capacity planning.

The solution: **One pipeline. Two runtimes. Same IR.**

---

## What Q33N Must Deliver

### Wave 1 — Foundation (No dependencies)

**TASK W1-A: PipelineStore Protocol + FilesystemPipelineStore**
- Define `PipelineStore` ABC with methods: `list_specs()`, `move_spec()`, `append_section()`, `get_done_ids()`, `deps_satisfied()`, `emit_event()`, `get_orphans()`
- Implement `FilesystemPipelineStore` that wraps existing queue runner filesystem operations
- Refactor `run_queue.py` to use `PipelineStore` interface (pure refactor, zero new behavior)
- All existing queue runner tests still pass
- Estimated: ~130 lines, Haiku model

**TASK W1-B: Validation Ledger Events**
- Add `phase_validation` and `bee_execution` event types to Event Ledger schema
- Create `emit_validation_event()` and `emit_execution_event()` helper functions
- Wire into existing code paths (fidelity checks, bee dispatches)
- Estimated: ~40 lines, Haiku model

### Wave 2 — State Machine (Depends on W1-A)

**TASK W2-A: Directory State Machine**
- Implement transitions: `queue/` → `_active/` (with manifest), `_active/` → `_done/`/`_failed/`, crash recovery (orphan scan)
- Pickup logic: priority (P0–P3), dependency checking, FIFO within priority, capacity limit
- Manifest appending: `bee_id`, `model`, `session_id`, `started_at`, `pid`
- Completion record appending: `completed_at`, `result`, `response_file`, `tests_before`, `tests_after`, `cost_usd`, `wall_time_seconds`
- Failure log appending on errors
- All operations through `PipelineStore` interface
- New tests: ~15 (transitions, crash recovery, failure log)
- Estimated: ~110 lines, Sonnet model

**TASK W2-B: InMemoryPipelineStore**
- Dict-backed implementation of `PipelineStore` protocol
- In-memory event list (append-only)
- Tests mirror filesystem tests but run in-memory
- Estimated: ~60 lines + ~10 tests, Haiku model

### Wave 3 — Intelligence Layer (Depends on W2-A + W2-B)

**TASK W3-A: PHASE-IR Flow Encoding**
- Author `.ir.json` describing the full pipeline as PHASE-IR flow
- Nodes for every stage (Gate 0, Phase 0–2, Task Breakdown, Dispatch, Bee Execution, etc.)
- Edges for every transition
- Resources: bee pool (capacity 5), human reviewer (capacity 1), LLM triage (capacity 3)
- Decision nodes: fidelity checks, heal loops, triage verdicts
- This artifact enables DES consumption + self-documentation via round-trip
- Estimated: ~200 lines (IR JSON), Sonnet model

**TASK W3-B: LLM Triage Functions**
- Three functions: `triage_crash_recovery()`, `triage_failure()`, `validate_completion()`
- Each dispatches Haiku, returns verdict enum
- Crash recovery verdicts: COMPLETE_ENOUGH, PARTIAL_SAFE, REVERT
- Failure diagnosis routing: Ambiguous spec, Coding error, Dependency issue, Environment issue
- Completion validation: advisory only in Phase 1, gating in Phase 2
- Wired into state machine transitions from W2-A
- Estimated: ~100 lines, Sonnet model

### Wave 4 — Simulation Runtime (Depends on W3-A)

**TASK W4-A: DES Runner for Build Pipeline**
- Load PHASE-IR flow from W3-A
- Instantiate `InMemoryPipelineStore`
- Run through DES engine with service time distributions (hardcoded initially, calibrated from ledger later)
- FastAPI endpoint on Railway: `POST /api/pipeline/simulate`
- Returns: throughput, bottleneck analysis, WIP distribution, optimal pool size recommendation
- Estimated: ~120 lines, Sonnet model

---

## File Paths (Absolute)

### Existing Files to Read
- Queue runner: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py`
- Queue modules: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_parser.py`, `spec_processor.py`, `fix_cycle.py`, `morning_report.py`
- Event Ledger: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\inventory\ledger.py`
- DES engine: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\` (PHASE-IR port complete, 248 tests passing)
- DES routes: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py` (22 tests passing)

### New Files to Create
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\pipeline_store.py` (PipelineStore ABC)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\triage.py` (LLM triage functions)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\pipeline.ir.json` (PHASE-IR flow encoding)
- Tests: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\queue\test_pipeline_store.py`, `test_state_machine.py`, `test_triage.py`
- DES runner route: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\pipeline_sim_routes.py`

---

## Constraints from BOOT.md

1. **No file over 500 lines.** Modularize at 500. Hard limit: 1,000.
2. **TDD.** Tests first, then implementation. No exceptions.
3. **NO STUBS.** Every function fully implemented.
4. **All file paths must be absolute** in task docs.
5. **NO GIT OPERATIONS.** No commits without Q88N approval. Reading git status/log/diff is allowed.

---

## Success Criteria (from Spec)

This spec is done when:

1. `run_queue.py` uses `PipelineStore` interface (no raw pathlib calls)
2. Specs move through `_active/` with manifests and completion records
3. Crash recovery triages with LLM instead of blind retry
4. Every validation gate and bee execution emits to Event Ledger
5. `InMemoryPipelineStore` passes the same test suite as filesystem version
6. DES engine can load the pipeline IR and produce throughput/bottleneck analysis
7. After 50 specs, the data answers: "Is the IR fidelity gate worth its tokens?"

---

## Open Questions from Spec (for Q88N)

The spec lists 5 open questions for Q88N. Q33N does NOT answer these — they are noted for awareness:

1. Fidelity threshold: 0.85 vs 0.90 after initial data?
2. Triage model: Haiku for all, or Sonnet for crash recovery?
3. `_needs_review/` timeout: 24 hours before warning?
4. DES endpoint: part of existing Railway backend or separate service?
5. PROCESS-0020 naming: Unified Build Pipeline or something else?

---

## Wave Structure

| Wave | Tasks | Dependencies | Parallelizable |
|------|-------|--------------|----------------|
| W1 | W1-A, W1-B | None | YES (both can run in parallel) |
| W2 | W2-A, W2-B | W1-A | W2-B can start when W2-A starts (both depend only on W1-A) |
| W3 | W3-A, W3-B | W2-A + W2-B | W3-A and W3-B can run in parallel |
| W4 | W4-A | W3-A | NO (sequential dependency) |

**Max parallel:** 2 bees at a time (W1-A + W1-B in Wave 1; W2-A + W2-B in Wave 2; W3-A + W3-B in Wave 3).

---

## Q33N's Next Steps

1. Read existing queue runner files (`run_queue.py`, `spec_parser.py`, `spec_processor.py`)
2. Read Event Ledger implementation (`hivenode/inventory/ledger.py`)
3. Write task files for W1-A and W1-B (no dependencies, can dispatch immediately after Q33NR review)
4. Return to Q33NR with task file summary for review
5. **DO NOT dispatch bees yet** — wait for Q33NR approval

---

## Cost Estimate (from Spec)

- Total tasks: 7
- Total new code: ~560 lines
- Total new tests: ~40
- LLM cost: ~$7–10
- Sessions: 2–3 overnight queue runs (if bees were queued)

Since this is live coordination (Q33NR → Q33N → bees), timeline is: 2–3 dispatch cycles over 1–2 days.

---

**Q33N: Read the spec, read the existing queue runner, write task files for Wave 1 (W1-A and W1-B). Return for Q33NR review before dispatching bees.**
