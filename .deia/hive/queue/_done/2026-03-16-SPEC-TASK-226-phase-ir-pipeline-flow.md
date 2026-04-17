# TASK-226: PHASE-IR Flow Encoding of Build Pipeline (W3-A)

## Objective
Author the `.ir.json` that describes the full build pipeline as a PHASE-IR flow. Nodes for every stage, edges for every transition, resources for bee pool and human reviewer.

## Context
Part of SPEC-PIPELINE-001 (Unified Build Pipeline). This is the artifact that lets the DES engine consume the build pipeline. The IR can also be rendered to English via round-trip (the process documents itself).

## Depends On
- TASK-224 (directory state machine must be defined)
- TASK-225 (InMemoryPipelineStore must exist for testing)

## Source Spec
`docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Sections 3 and 7

## Files to Read First
- `docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Sections 3, 7.1–7.4
- `engine/phase_ir/` — existing PHASE-IR format, node types, schema
- `engine/phase_ir/schema.json` — IR schema definition

## Deliverables
- [ ] Create `.deia/hive/scripts/queue/pipeline.ir.json`
  - Activity nodes for every pipeline stage (Gate 0, Phase 0-2, Task Breakdown, Dispatch, Bee Execution, Post-Dispatch Verify, Q33N Review, Archive)
  - Decision nodes for: fidelity check (PASS/FAIL), heal loop (retry/escalate), bee result (CLEAN/TIMEOUT/CRASH), triage verdict
  - Resource definitions: bee pool (capacity=5), human reviewer (capacity=1), LLM triage (capacity=3)
  - Service time distributions per Section 7.1 of the spec
  - Edges for all transitions including failure/healing loops
- [ ] Validate against `engine/phase_ir/schema.json`
- [ ] Create tests in `.deia/hive/scripts/queue/tests/test_pipeline_ir.py`
  - Test IR loads and validates against schema
  - Test all pipeline stages are represented as nodes
  - Test all transitions are represented as edges
  - Test resources are defined with correct capacities
  - ~8 tests minimum

## Priority
P1

## Model
sonnet
