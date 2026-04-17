---
id: BENCH-001-5
priority: P0
model: haiku
role: bee
---
# TASK-BENCH-001.5 — Create 5 Trivial PRISM-IR Test Workflows

**Priority:** P0
**Model:** Haiku
**Type:** Test fixture creation
**Date:** 2026-04-13
**Wave:** A — Infrastructure
**Estimated Cost:** $0.50

---

## Objective

Create 5 minimal PRISM-IR workflow files for Wave A exit validation. These workflows will be used by the benchmark runner to verify end-to-end functionality before external benchmarks are added in Waves B and C.

---

## Context

Wave A builds benchmark infrastructure without external benchmarks. To validate the runner works end-to-end, we need trivial test tasks that can run quickly through both baseline and SimDecisions tracks. These workflows must be valid PRISM-IR but simple enough to complete in <10 seconds each.

### Requirements per Workflow

- Valid PRISM-IR format (Flow schema)
- 3-8 nodes maximum
- No complex branching or multi-agent coordination
- Deterministic or simple stochastic elements
- Clear pass/fail evaluation criteria
- Total runtime per workflow: <10 seconds

---

## Files to Read First

- `docs/specs/SPEC-BENCHMARK-SUITE-001.md`
  Section 7 Wave A for context on test workflow requirements

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/phase_ir/primitives.py`
  PRISM-IR schema and Flow structure

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/engine.py`
  Reference for what the DES engine expects in a Flow

---

## Deliverables

Create new directory and 5 workflow files:

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/test_workflows/` (new directory)

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/test_workflows/workflow_01_simple_queue.json`
  **Description:** Source -> Queue -> Service -> Sink
  **Nodes:** Source (Poisson lambda=5), Queue (FIFO cap=10), Service (exponential mu=6, 1 server), Sink
  **Evaluation:** Throughput > 4 entities/min, mean cycle time < 3 min
  **Expected runtime:** ~5 seconds

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/test_workflows/workflow_02_multi_server.json`
  **Description:** Source -> Queue -> Service (3 servers) -> Sink
  **Nodes:** Source (Poisson lambda=10), Queue (FIFO cap=20), Service (exponential mu=4, 3 servers), Sink
  **Evaluation:** Server utilization < 90%, queue depth < 15
  **Expected runtime:** ~5 seconds

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/test_workflows/workflow_03_priority_queue.json`
  **Description:** Source -> Priority Queue -> Service -> Sink
  **Nodes:** Source (Poisson lambda=8, tokens tagged with priority 1-3), Queue (PRIORITY), Service (exponential mu=10, 2 servers), Sink
  **Evaluation:** High-priority tokens (priority=1) have mean cycle time < low-priority (priority=3)
  **Expected runtime:** ~5 seconds

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/test_workflows/workflow_04_branch_merge.json`
  **Description:** Source -> Branch -> [Path A, Path B] -> Merge -> Sink
  **Nodes:** Source, Branch (50/50 split), Service A (mean=2), Service B (mean=4), Merge, Sink
  **Evaluation:** 45-55% of tokens went through each branch
  **Expected runtime:** ~5 seconds

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/test_workflows/workflow_05_resource_contention.json`
  **Description:** 2 Sources -> Shared Resource Pool -> Service -> Sink
  **Nodes:** Source1 (lambda=3), Source2 (lambda=3), Shared Resource (capacity=2), Service (exponential mu=8), Sink
  **Evaluation:** Resource utilization 70-90%, no deadlocks
  **Expected runtime:** ~5 seconds

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/benchmark/test_workflows/README.md`
  Document each workflow: name, description, evaluation criteria, expected runtime

---

## Test Requirements

No unit tests required for this task (these workflows ARE the test fixtures).

Instead, create validation script:

- [ ] `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/benchmark/test_workflows_valid.py`
  - Load each workflow JSON file
  - Validate against PRISM-IR Flow schema
  - Verify all required fields present (id, nodes, edges, resources if applicable)
  - 5 tests (one per workflow)

**Total test count:** 5 validation tests

**TDD approach:** Write validation tests first, then create workflow JSON files to pass validation

---

## Acceptance Criteria

- [ ] `simdecisions/benchmark/test_workflows/` directory created
- [ ] `simdecisions/benchmark/test_workflows/workflow_01_simple_queue.json` is valid PRISM-IR with 4 nodes (Source, Queue, Service, Sink)
- [ ] `simdecisions/benchmark/test_workflows/workflow_02_multi_server.json` is valid PRISM-IR with 4 nodes and 3-server configuration
- [ ] `simdecisions/benchmark/test_workflows/workflow_03_priority_queue.json` is valid PRISM-IR with priority queue discipline
- [ ] `simdecisions/benchmark/test_workflows/workflow_04_branch_merge.json` is valid PRISM-IR with branch/merge topology (6 nodes)
- [ ] `simdecisions/benchmark/test_workflows/workflow_05_resource_contention.json` is valid PRISM-IR with shared resource pool
- [ ] `simdecisions/benchmark/test_workflows/README.md` documents all 5 workflows with name, description, evaluation criteria, expected runtime
- [ ] All 5 workflow JSON files load without error and contain `id`, `nodes`, `edges` fields
- [ ] No workflow exceeds 8 nodes
- [ ] Tests in `tests/simdecisions/benchmark/test_workflows_valid.py` -- 5 tests passing (one per workflow, schema validation)
- [ ] Each workflow has clear pass/fail evaluation criteria defined in metadata

---

## Constraints

- Each workflow must be valid PRISM-IR (loadable by DES engine)
- No workflow exceeds 8 nodes
- All workflows must complete in <10 seconds when simulated
- No stubs — full valid JSON for each workflow
- File format: JSON (not YAML) for consistency with PRISM-IR examples

---

## Dependencies

**Depends on:** BENCH-001 (for BenchmarkTask type, though not strictly required for this task)

**Blocks:** BENCH-002 (runner needs test workflows to validate against)

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:

`C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/responses/20260413-TASK-BENCH-001-5-RESPONSE.md`

The response MUST contain these 8 sections:

1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full absolute paths
3. **What Was Done** — bullet list of concrete changes (not intent)
4. **Test Results** — test files run, pass/fail counts, pytest output summary
5. **Build Verification** — did tests pass? Include last 5 lines of pytest output
6. **Acceptance Criteria** — copy from task, mark [x] or [ ] with explanation if not done
7. **Clock / Cost / Carbon** — all three currencies, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, recommended next tasks

DO NOT skip any section.
