# TASK-228: DES Runner for Build Pipeline (W4-A)

## Objective
Load the PHASE-IR flow from TASK-226, instantiate InMemoryPipelineStore, run through DES engine with service time distributions. Expose as FastAPI endpoint.

## Context
Part of SPEC-PIPELINE-001 (Unified Build Pipeline). This is the simulation runtime — the same pipeline executed in-memory with statistical service times instead of real LLM calls. Answers: throughput, bottleneck analysis, WIP distribution, optimal pool size.

## Depends On
- TASK-226 (PHASE-IR flow JSON must exist)
- TASK-225 (InMemoryPipelineStore must exist)

## Source Spec
`docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Sections 7.4 and 7.5

## Files to Read First
- `docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Section 7
- `.deia/hive/scripts/queue/pipeline.ir.json` — the pipeline flow (from TASK-226)
- `.deia/hive/scripts/queue/inmemory_store.py` — InMemoryPipelineStore (from TASK-225)
- `engine/phase_ir/` — DES engine, execution runtime
- `hivenode/routes/des_routes.py` — existing DES endpoint pattern

## Deliverables
- [ ] Create `hivenode/routes/pipeline_sim.py`
  - `POST /api/pipeline/simulate` endpoint
  - Request body: pool_size (int), num_specs (int), failure_rate (float), fidelity_threshold (float)
  - Loads pipeline IR from file
  - Instantiates InMemoryPipelineStore
  - Runs DES engine with service time distributions (hardcoded initially):
    - Gate 0: ~5s, Phase 0: ~8s, Phase 1: ~12s, Phase 2: ~12s
    - Bee execution: LogNormal(mean=180s, std=120s)
    - Human review: Exponential(mean=300s)
  - Returns JSON: throughput (specs/hour), bottleneck_stage, avg_cycle_time, wip_distribution, optimal_pool_size
- [ ] Register route in `hivenode/routes/__init__.py`
- [ ] Create tests in `tests/hivenode/routes/test_pipeline_sim.py`
  - Test endpoint returns valid response
  - Test throughput increases with pool size (up to a point)
  - Test bottleneck identification
  - Test with different failure rates
  - ~8 tests minimum

## Priority
P1

## Model
sonnet
