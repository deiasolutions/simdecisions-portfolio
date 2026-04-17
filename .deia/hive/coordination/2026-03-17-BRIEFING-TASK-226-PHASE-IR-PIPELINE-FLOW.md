# BRIEFING: TASK-226 PHASE-IR Pipeline Flow Encoding (W3-A)

**To:** Q33N (Queen Coordinator)
**From:** Q88NR-bot (Mechanical Regent)
**Date:** 2026-03-17
**Source Spec:** `QUEUE-TEMP-2026-03-16-SPEC-TASK-226-phase-ir-pipeline-flow.md`
**Priority:** P1
**Model:** Sonnet

---

## Objective

Author the `.ir.json` file that describes the full build pipeline as a PHASE-IR flow. This is the artifact that enables DES (Discrete Event Simulation) engine to consume and simulate the build pipeline. It also allows round-trip rendering to English (the process documents itself).

---

## Context

**What This Is:**
- Part of SPEC-PIPELINE-001 (Unified Build Pipeline), Wave 3 task (W3-A)
- Creates the bridge between the filesystem-based queue runner (production) and DES simulation (analysis)
- The IR flow encodes: all pipeline stages (Gate 0, Phase 0-2, Task Breakdown, Dispatch, Bee Execution, Post-Dispatch Verify, Q33N Review, Archive), all transitions (including failure/healing loops), all resources (bee pool, human reviewer, LLM triage), all service time distributions

**Dependencies (both complete):**
- ✅ TASK-224 (directory state machine) — in `_done/`
- ✅ TASK-225 (InMemoryPipelineStore) — in `_done/`

**Why This Matters:**
- Once the IR exists, DES engine can answer: throughput, bottlenecks, optimal pool size, failure impact, fidelity ROI
- The IR is the canonical process definition — English docs render FROM it, not maintained separately

---

## Source Documents

### Primary References
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md`
   - **Section 3:** Pipeline Stages (full sequence with input/output artifacts, success criteria, failure routes)
   - **Section 7:** DES Model of the Pipeline (node mapping, resources, decision nodes, calibration)
   - **Section 7.1:** Service time sources for each stage
   - **Section 7.2:** Resources (bee pool capacity=5, human reviewer capacity=1, LLM triage capacity=3)
   - **Section 7.3:** Decision nodes (fidelity check, heal loop, bee result, triage verdict)

### PHASE-IR Format References
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\primitives.py`
   - Dataclass structures: Flow, Node, Edge, Resource, Distribution, Variable, etc.
   - Node types: human, python, llm, http, subprocess, solver, wait, signal, source, sink, batch, separate
   - Edge types: then, fork, join, switch, any, repeat, wait, timeout, emit, on

3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\schema.py`
   - Serialization: `flow_to_json()`, `json_to_flow()`, `flow_to_dict()`, `dict_to_flow()`
   - Validation: `validate_flow_structure()` (V-001 through V-010 checks)

### Existing Store Implementations (for testing)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\pipeline_store.py` — PipelineStore protocol
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\inmemory_store.py` — InMemoryPipelineStore implementation

---

## Deliverables

Your task file MUST specify the following deliverables:

### 1. PHASE-IR JSON File
- **File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\pipeline.ir.json`
- **Format:** JSON encoding of a PHASE-IR Flow dataclass
- **Content Requirements:**
  - Flow metadata: id, name, intent, phase_ir_version=1.0.0
  - **Activity nodes** for every pipeline stage (at least 9):
    - Gate 0 (Intent Validation)
    - Phase 0 (Coverage Validation)
    - Phase 1 (SPEC Fidelity)
    - Phase 2 (TASK Fidelity)
    - Task Breakdown (Q33N writes task files)
    - Q33NR Review (human approval)
    - Dispatch (bee assignment)
    - Bee Execution (TDD, code, response)
    - Post-Dispatch Verification (test count, regression check)
    - Q33N Review (response complete? stubs?)
    - Archive + Inventory
  - **Decision nodes** for:
    - Fidelity check (PASS ≥0.85 → next / FAIL → heal)
    - Heal loop (retry < 3 → re-validate / escalate ≥ 3 → human)
    - Bee result (CLEAN → _done / TIMEOUT → triage / CRASH → recovery / NEEDS_DAVE → triage)
    - Triage verdict (COMPLETE_ENOUGH → _done / PARTIAL_SAFE → continuation / REVERT → retry)
  - **Resources** (3):
    - id=bee_pool, type=bot, capacity=5
    - id=human_reviewer, type=human, capacity=1
    - id=llm_triage, type=bot, capacity=3
  - **Distributions** for service times (per Section 7.1):
    - Gate 0: constant, 5 seconds
    - Phase 0: constant, 8 seconds
    - Phase 1: constant, 12 seconds
    - Phase 2: constant, 12 seconds
    - Post-Dispatch Verify: constant, 10 seconds
    - Q33N Review: constant, 30 seconds
    - Archive: constant, 5 seconds
    - Bee Execution: lognormal (mean=180s, sigma=1.5) — heavy right tail
    - Q33NR Review: uniform (min=60s, max=300s)
  - **Edges** for all transitions:
    - Sequential flows (then)
    - Decision branches (switch with guard conditions)
    - Failure/healing loops (repeat)
    - Escalation routes (to human_reviewer)

### 2. Tests
- **File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_pipeline_ir.py`
- **Minimum:** 8 tests
- **Test scenarios:**
  1. IR file loads without error
  2. IR validates against PHASE-IR schema (via `validate_flow_structure()`)
  3. All pipeline stages are represented as nodes (at least 9 activity nodes)
  4. All transitions are represented as edges (at least 15 edges)
  5. All resources are defined with correct capacities
  6. All distributions are defined with correct params
  7. Round-trip: IR → dict → IR preserves structure
  8. Node IDs are unique (no duplicates)

---

## Constraints

- **No file over 500 lines.** If the IR exceeds 500 lines, split into modular components OR use compact JSON formatting (no comments, minimal whitespace).
- **TDD:** Tests written first, then implementation.
- **No stubs:** The IR must be complete. Every stage, every decision node, every resource, every edge.
- **Validation:** The IR must pass `validate_flow_structure()` from `engine/phase_ir/schema.py`.
- **Absolute paths:** All file paths in the task file must be absolute (Windows format: `C:\Users\davee\...`).

---

## Notes for Q33N

### IR Structure Template

```python
from engine.phase_ir.primitives import Flow, Node, Edge, Resource, Distribution

flow = Flow(
    id="build-pipeline-v1",
    name="Unified Build Pipeline",
    intent="Complete software delivery pipeline from spec to archive",
    phase_ir_version="1.0.0",
    nodes=[
        # Activity nodes (type="subprocess" or "llm" or "human")
        Node(id="gate_0", type="llm", name="Intent Validation", config={"service_time": "dist_gate0"}),
        Node(id="phase_0", type="llm", name="Coverage Validation", config={"service_time": "dist_phase0"}),
        # ... (9+ activity nodes)

        # Decision nodes (type="signal" with switch edges)
        Node(id="decision_fidelity", type="signal", name="Fidelity Check"),
        Node(id="decision_heal", type="signal", name="Heal or Escalate"),
        Node(id="decision_bee_result", type="signal", name="Bee Result Router"),
        Node(id="decision_triage", type="signal", name="Triage Verdict"),
    ],
    edges=[
        # Sequential flows
        Edge(id="e1", from_node="gate_0", to_node="decision_fidelity_gate0", type="then"),

        # Decision branches
        Edge(id="e2", from_node="decision_fidelity", to_node="phase_1", type="switch", guard="fidelity >= 0.85"),
        Edge(id="e3", from_node="decision_fidelity", to_node="decision_heal", type="switch", guard="fidelity < 0.85"),

        # Healing loop
        Edge(id="e4", from_node="decision_heal", to_node="phase_0", type="repeat", guard="attempt < 3"),
        Edge(id="e5", from_node="decision_heal", to_node="human_reviewer", type="then", guard="attempt >= 3"),

        # ... (15+ edges)
    ],
    resources=[
        Resource(id="bee_pool", type="bot", capacity=5),
        Resource(id="human_reviewer", type="human", capacity=1),
        Resource(id="llm_triage", type="bot", capacity=3),
    ],
    distributions=[
        Distribution(id="dist_gate0", type="constant", params={"value": 5}, unit="seconds"),
        Distribution(id="dist_phase0", type="constant", params={"value": 8}, unit="seconds"),
        Distribution(id="dist_phase1", type="constant", params={"value": 12}, unit="seconds"),
        Distribution(id="dist_phase2", type="constant", params={"value": 12}, unit="seconds"),
        Distribution(id="dist_verify", type="constant", params={"value": 10}, unit="seconds"),
        Distribution(id="dist_q33n_review", type="constant", params={"value": 30}, unit="seconds"),
        Distribution(id="dist_archive", type="constant", params={"value": 5}, unit="seconds"),
        Distribution(id="dist_bee_exec", type="lognormal", params={"mean": 180, "sigma": 1.5}, unit="seconds"),
        Distribution(id="dist_q33nr_review", type="uniform", params={"min": 60, "max": 300}, unit="seconds"),
    ],
)

# Serialize to JSON
from engine.phase_ir.schema import flow_to_json
json_output = flow_to_json(flow)
```

### Service Time Mapping (from SPEC Section 7.1)

| Pipeline Stage | DES Node Type | Service Time Distribution |
|---------------|---------------|--------------------------|
| Gate 0 (Intent) | llm | constant(5s) |
| Phase 0 (Coverage) | llm | constant(8s) |
| Phase 1 (SPEC Fidelity) | llm | constant(12s) |
| Phase 2 (TASK Fidelity) | llm | constant(12s) |
| Task Breakdown | llm | constant(30s) — Q33N writes |
| Q33NR Review | human | uniform(60s, 300s) |
| Dispatch | subprocess | constant(2s) |
| Bee Execution | subprocess | lognormal(mean=180s, sigma=1.5) |
| Post-Dispatch Verify | subprocess | constant(10s) |
| Q33N Review | llm | constant(30s) |
| Archive | subprocess | constant(5s) |

### Decision Logic (from SPEC Section 7.3)

1. **Fidelity Check (after Gate 0, Phase 0, Phase 1, Phase 2):**
   - PASS (fidelity ≥ 0.85) → next stage
   - FAIL (fidelity < 0.85) → heal loop

2. **Heal Loop:**
   - Retry (attempt < 3) → re-validate
   - Escalate (attempt ≥ 3) → human reviewer

3. **Bee Result:**
   - CLEAN → _done/ (Post-Dispatch Verify)
   - TIMEOUT → LLM triage
   - CRASH → crash recovery triage
   - NEEDS_DAVE → LLM triage

4. **Triage Verdict (from LLM triage):**
   - COMPLETE_ENOUGH → _done/
   - PARTIAL_SAFE → continuation spec generated
   - REVERT → retry from beginning

---

## Success Criteria

The task is complete when:

1. ✅ `pipeline.ir.json` exists and is valid JSON
2. ✅ IR passes `validate_flow_structure()` (no V-001..V-010 violations)
3. ✅ At least 9 activity nodes exist (matching pipeline stages)
4. ✅ At least 4 decision nodes exist (fidelity, heal, bee result, triage)
5. ✅ At least 15 edges exist (covering all transitions including loops)
6. ✅ 3 resources defined with correct capacities
7. ✅ 9 distributions defined with correct params
8. ✅ All tests pass (at least 8 tests)

---

## Your Next Step, Q33N

1. Read all source documents listed above
2. Write a complete task file to `.deia/hive/tasks/2026-03-17-TASK-226-phase-ir-pipeline-flow.md`
3. Ensure the task file includes:
   - **Objective** (one sentence)
   - **Context** (what the bee needs to know)
   - **Files to Read First** (absolute paths)
   - **Deliverables** (checklist with concrete outputs)
   - **Test Requirements** (TDD, edge cases, minimum 8 tests)
   - **Constraints** (500-line limit, no stubs, absolute paths)
   - **Response Requirements** (8-section mandatory template)
4. Return the task file path to me for review
5. **DO NOT dispatch the bee yet** — wait for my approval

---

**Q88NR-bot (Mechanical Regent)**
