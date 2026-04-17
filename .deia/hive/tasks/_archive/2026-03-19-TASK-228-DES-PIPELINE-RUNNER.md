# TASK-228: DES Pipeline Runner for Build Pipeline Simulation

## Objective
Create a FastAPI endpoint that loads the PHASE-IR pipeline flow from TASK-226, instantiates InMemoryPipelineStore, and runs it through the DES engine with service time distributions to analyze throughput, bottlenecks, and optimal pool size.

## Context
Part of SPEC-PIPELINE-001 (Unified Build Pipeline). This is the simulation runtime — the same pipeline executed in-memory with statistical service times instead of real LLM calls. Answers questions like: What's the throughput? Where are the bottlenecks? What's the optimal bee pool size?

Dependencies TASK-225 (InMemoryPipelineStore) and TASK-226 (pipeline.ir.json) are COMPLETE — both files exist.

## Source Spec
From `.deia/hive/queue/_done/2026-03-16-SPEC-TASK-228-des-pipeline-runner.md`
Reference: `docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Sections 7.4 and 7.5

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` (Section 7)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\pipeline.ir.json` (the pipeline flow from TASK-226)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\inmemory_store.py` (InMemoryPipelineStore from TASK-225)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\` (DES engine modules)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py` (existing DES endpoint pattern to follow)

## Files You May Modify
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\pipeline_sim.py` (CREATE NEW)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` (add router import + include_router call)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_pipeline_sim.py` (CREATE NEW)

## Files You Must NOT Modify
- Any files in `browser/` directory
- Any files in `engine/` directory (read only)
- Any files in `.deia/hive/scripts/queue/` (read only — don't modify inmemory_store.py or pipeline.ir.json)
- Any other route files besides the ones listed above
- Database schema files

## Deliverables
- [ ] Create `hivenode/routes/pipeline_sim.py`:
  - Define FastAPI router with prefix `/api/pipeline`
  - Implement `POST /api/pipeline/simulate` endpoint
  - Request schema (Pydantic): `PipelineSimRequest`
    - pool_size: int (bee pool size)
    - num_specs: int (number of specs to simulate)
    - failure_rate: float (probability of bee failure)
    - fidelity_threshold: float (quality gate threshold)
  - Response schema (Pydantic): `PipelineSimResponse`
    - throughput: float (specs/hour)
    - bottleneck_stage: str (which stage is the bottleneck)
    - avg_cycle_time: float (seconds per spec)
    - wip_distribution: dict[str, float] (work-in-progress by stage)
    - optimal_pool_size: int (recommended pool size)
  - Load pipeline IR from `.deia/hive/scripts/queue/pipeline.ir.json`
  - Instantiate InMemoryPipelineStore
  - Run DES engine with service time distributions (hardcoded initially):
    - Gate 0 (triage): Normal(mean=5s, std=2s)
    - Phase 0 (parse): Normal(mean=8s, std=3s)
    - Phase 1 (dispatch): Normal(mean=12s, std=4s)
    - Phase 2 (monitor): Normal(mean=12s, std=4s)
    - Bee execution: LogNormal(mean=180s, std=120s)
    - Human review: Exponential(mean=300s)
  - Return simulation results
- [ ] Register route in `hivenode/routes/__init__.py`:
  - Import: `from hivenode.routes import pipeline_sim`
  - Include: `router.include_router(pipeline_sim.router, tags=['pipeline-sim'])`
- [ ] Create tests in `tests/hivenode/routes/test_pipeline_sim.py`:
  - Test endpoint returns valid response schema
  - Test throughput increases with pool size (up to a point)
  - Test bottleneck identification is non-empty string
  - Test with different failure rates (0.0, 0.1, 0.5)
  - Test with different pool sizes (1, 5, 10)
  - Test avg_cycle_time is positive
  - Test wip_distribution sums to reasonable value
  - Test optimal_pool_size recommendation is within reason
  - Minimum 8 tests

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases covered:
  - pool_size = 1 (minimum)
  - pool_size = 50 (large)
  - failure_rate = 0.0 (no failures)
  - failure_rate = 1.0 (all failures)
  - num_specs = 1 (single spec)
  - num_specs = 100 (large batch)

## Constraints
- No file over 500 lines (if pipeline_sim.py approaches 500, refactor into modules)
- No stubs — full implementation
- No hardcoded colors (N/A for backend)
- All absolute paths in docs
- Follow existing des_routes.py pattern for consistency

## Acceptance Criteria
- [ ] `POST /api/pipeline/simulate` endpoint exists
- [ ] Endpoint accepts all required request parameters
- [ ] Endpoint returns all required response fields
- [ ] Pipeline IR loaded from file successfully
- [ ] InMemoryPipelineStore instantiated correctly
- [ ] DES engine runs simulation with service time distributions
- [ ] Throughput calculated correctly (specs/hour)
- [ ] Bottleneck stage identified
- [ ] WIP distribution calculated
- [ ] Optimal pool size recommended
- [ ] Router registered in `__init__.py`
- [ ] All tests pass: `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter && python -m pytest tests/hivenode/routes/test_pipeline_sim.py -v`
- [ ] No regressions in other route tests

## Model Assignment
sonnet

## Priority
P1

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260319-TASK-228-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
