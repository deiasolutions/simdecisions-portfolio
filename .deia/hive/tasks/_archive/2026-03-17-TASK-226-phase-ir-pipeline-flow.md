# TASK-226: PHASE-IR Pipeline Flow Encoding (W3-A)

## Objective

Author the `.ir.json` file that describes the complete build pipeline as a PHASE-IR flow, enabling DES simulation and self-documenting process definitions.

## Context

This task creates the bridge between the filesystem-based queue runner (production) and DES simulation (analysis). The IR flow encodes all pipeline stages, transitions, resources, and service time distributions. Once complete, the DES engine can answer questions about throughput, bottlenecks, optimal pool size, and failure impact.

**Dependencies (both complete):**
- ✅ TASK-224 (directory state machine) — in `_done/`
- ✅ TASK-225 (InMemoryPipelineStore) — in `_done/`

**Pipeline Stages (from SPEC-PIPELINE-001 Section 3):**
1. Gate 0 (Intent Validation) — 5s constant
2. Phase 0 (Coverage Validation) — 8s constant
3. Phase 1 (SPEC Fidelity) — 12s constant
4. Phase 2 (TASK Fidelity) — 12s constant
5. Task Breakdown (Q33N writes task files) — 30s constant
6. Q33NR Review (human approval) — uniform(60s, 300s)
7. Dispatch (bee assignment) — 2s constant
8. Bee Execution (TDD, code, response) — lognormal(mean=180s, sigma=1.5)
9. Post-Dispatch Verification — 10s constant
10. Q33N Review (response validation) — 30s constant
11. Archive + Inventory — 5s constant

**Decision Nodes:**
1. Fidelity Check (after Gate 0, Phase 0-2): PASS (≥0.85) → next / FAIL (<0.85) → heal loop
2. Heal Loop: Retry (attempt < 3) → re-validate / Escalate (attempt ≥ 3) → human
3. Bee Result: CLEAN → _done / TIMEOUT → triage / CRASH → recovery / NEEDS_DAVE → triage
4. Triage Verdict: COMPLETE_ENOUGH → _done / PARTIAL_SAFE → continuation / REVERT → retry

**Resources:**
- bee_pool: capacity=5, type=bot
- human_reviewer: capacity=1, type=human
- llm_triage: capacity=3, type=bot

## Files to Read First

### Primary References
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md`
   - Section 3: Pipeline Stages (full sequence with input/output artifacts)
   - Section 7: DES Model of the Pipeline (node mapping, resources, decisions)
   - Section 7.1: Service time sources for each stage
   - Section 7.2: Resources (capacities)
   - Section 7.3: Decision nodes (branching logic)

### PHASE-IR Format References
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\primitives.py`
   - Flow, Node, Edge, Resource, Distribution, Variable dataclass structures
   - Node types: human, python, llm, http, subprocess, solver, wait, signal, source, sink
   - Edge types: then, fork, join, switch, any, repeat, wait, timeout, emit, on

3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\schema.py`
   - Serialization: `flow_to_json()`, `json_to_flow()`, `flow_to_dict()`, `dict_to_flow()`
   - Validation: `validate_flow_structure()` (V-001 through V-010 checks)

### Store Protocol (for context)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\pipeline_store.py`
   - PipelineStore protocol interface
   - SpecFile dataclass

5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\inmemory_store.py`
   - InMemoryPipelineStore implementation (TASK-225 deliverable)

## Deliverables

### 1. PHASE-IR JSON File
- [ ] File created: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\pipeline.ir.json`
- [ ] Flow metadata populated: id="build-pipeline-v1", name, intent, phase_ir_version="1.0.0"
- [ ] At least 11 activity nodes representing pipeline stages:
  - [ ] gate_0 (Intent Validation)
  - [ ] phase_0 (Coverage Validation)
  - [ ] phase_1 (SPEC Fidelity)
  - [ ] phase_2 (TASK Fidelity)
  - [ ] task_breakdown (Q33N writes task files)
  - [ ] q33nr_review (human approval)
  - [ ] dispatch (bee assignment)
  - [ ] bee_execution (TDD, code, response)
  - [ ] post_dispatch_verify (test count comparison)
  - [ ] q33n_review (response validation)
  - [ ] archive_inventory (feature registration)
- [ ] At least 4 decision nodes (type="signal"):
  - [ ] decision_fidelity (fidelity check after gates)
  - [ ] decision_heal (heal or escalate)
  - [ ] decision_bee_result (CLEAN/TIMEOUT/CRASH/NEEDS_DAVE router)
  - [ ] decision_triage (LLM verdict router)
- [ ] At least 3 resources defined:
  - [ ] bee_pool (type="bot", capacity=5)
  - [ ] human_reviewer (type="human", capacity=1)
  - [ ] llm_triage (type="bot", capacity=3)
- [ ] At least 9 distributions defined matching service times:
  - [ ] dist_gate0: constant(5s)
  - [ ] dist_phase0: constant(8s)
  - [ ] dist_phase1: constant(12s)
  - [ ] dist_phase2: constant(12s)
  - [ ] dist_task_breakdown: constant(30s)
  - [ ] dist_q33nr_review: uniform(60s, 300s)
  - [ ] dist_dispatch: constant(2s)
  - [ ] dist_bee_exec: lognormal(mean=180, sigma=1.5)
  - [ ] dist_verify: constant(10s)
  - [ ] dist_q33n_review: constant(30s)
  - [ ] dist_archive: constant(5s)
- [ ] At least 20 edges covering all transitions:
  - [ ] Sequential flows (type="then")
  - [ ] Decision branches (type="switch" with guard conditions)
  - [ ] Failure/healing loops (type="repeat")
  - [ ] Escalation routes (to human_reviewer)
- [ ] Each activity node references its service time distribution via config.service_time

### 2. Tests
- [ ] File created: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_pipeline_ir.py`
- [ ] Minimum 8 tests covering:
  - [ ] Test 1: IR file loads without error (file exists, valid JSON)
  - [ ] Test 2: IR validates against PHASE-IR schema (validate_flow_structure returns True, no errors)
  - [ ] Test 3: All 11 pipeline stages are represented as activity nodes
  - [ ] Test 4: All 4 decision nodes are present with correct types
  - [ ] Test 5: All 3 resources defined with correct capacities and types
  - [ ] Test 6: All 9+ distributions defined with correct types and params
  - [ ] Test 7: Round-trip preserves structure (IR → dict → IR equals original)
  - [ ] Test 8: Node IDs are unique (no duplicate node IDs)
  - [ ] Test 9: All edges reference existing nodes (no dangling references)
  - [ ] Test 10: Sequential flow exists from gate_0 through archive_inventory
  - [ ] Test 11: Healing loop exists (phase validation → heal decision → retry or escalate)
  - [ ] Test 12: Bee result routing exists (bee_execution → decision_bee_result → _done/triage)

## Test Requirements

### TDD Approach
- [ ] Tests written FIRST before IR file is created
- [ ] Tests initially fail (IR file does not exist)
- [ ] IR file created to pass tests
- [ ] All tests pass after implementation

### Edge Cases
- [ ] IR passes validate_flow_structure() with zero errors
- [ ] All node IDs are unique (no duplicates)
- [ ] All edges have valid from_node and to_node references
- [ ] All resource/distribution/variable references in node configs are valid
- [ ] Decision nodes have at least 2 outgoing edges (branches)
- [ ] Activity nodes reference service time distributions
- [ ] Healing loops have guard conditions (attempt < 3 for retry, attempt ≥ 3 for escalate)
- [ ] Fidelity checks have guard conditions (fidelity >= 0.85 for pass, < 0.85 for fail)

### Test Execution
```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue
python -m pytest tests/test_pipeline_ir.py -v
```

Expected output: 12 passed (minimum 8 required, but recommend 12 for thorough coverage)

## Constraints

### Hard Limits
- [ ] No file over 500 lines
  - If IR JSON exceeds 500 lines, use compact formatting (no comments, minimal whitespace)
  - Alternative: split into modular components if needed
- [ ] TDD: Tests written first, then implementation
- [ ] No stubs: The IR must be complete (all stages, all decision nodes, all resources, all edges)
- [ ] Validation: The IR must pass `validate_flow_structure()` from `engine/phase_ir/schema.py`
- [ ] Absolute paths: All file paths in this task file are absolute (Windows format)

### IR Completeness Requirements
- [ ] Every pipeline stage from SPEC-PIPELINE-001 Section 3 has a corresponding node
- [ ] Every transition from SPEC-PIPELINE-001 Section 3 has a corresponding edge
- [ ] Every decision point from SPEC-PIPELINE-001 Section 7.3 has a decision node + edges
- [ ] Every resource from SPEC-PIPELINE-001 Section 7.2 has a Resource entry
- [ ] Every service time from SPEC-PIPELINE-001 Section 7.1 has a Distribution entry
- [ ] No stages, transitions, or resources are omitted

## IR Structure Template

Use the following structure as a guide:

```python
from engine.phase_ir.primitives import Flow, Node, Edge, Resource, Distribution

flow = Flow(
    id="build-pipeline-v1",
    name="Unified Build Pipeline",
    intent="Complete software delivery pipeline from spec to archive",
    phase_ir_version="1.0.0",
    nodes=[
        # Activity nodes (11 stages)
        Node(id="gate_0", type="llm", name="Intent Validation",
             config={"service_time": "dist_gate0", "resource": "llm_triage"}),
        Node(id="phase_0", type="llm", name="Coverage Validation",
             config={"service_time": "dist_phase0", "resource": "llm_triage"}),
        Node(id="phase_1", type="llm", name="SPEC Fidelity",
             config={"service_time": "dist_phase1", "resource": "llm_triage"}),
        Node(id="phase_2", type="llm", name="TASK Fidelity",
             config={"service_time": "dist_phase2", "resource": "llm_triage"}),
        Node(id="task_breakdown", type="llm", name="Task Breakdown (Q33N)",
             config={"service_time": "dist_task_breakdown"}),
        Node(id="q33nr_review", type="human", name="Q33NR Review",
             config={"service_time": "dist_q33nr_review", "resource": "human_reviewer"}),
        Node(id="dispatch", type="subprocess", name="Dispatch Bee",
             config={"service_time": "dist_dispatch"}),
        Node(id="bee_execution", type="subprocess", name="Bee Execution",
             config={"service_time": "dist_bee_exec", "resource": "bee_pool"}),
        Node(id="post_dispatch_verify", type="subprocess", name="Post-Dispatch Verify",
             config={"service_time": "dist_verify"}),
        Node(id="q33n_review", type="llm", name="Q33N Review",
             config={"service_time": "dist_q33n_review"}),
        Node(id="archive_inventory", type="subprocess", name="Archive + Inventory",
             config={"service_time": "dist_archive"}),

        # Decision nodes (4 routing points)
        Node(id="decision_fidelity_gate0", type="signal", name="Fidelity Check (Gate 0)"),
        Node(id="decision_fidelity_phase0", type="signal", name="Fidelity Check (Phase 0)"),
        Node(id="decision_fidelity_phase1", type="signal", name="Fidelity Check (Phase 1)"),
        Node(id="decision_fidelity_phase2", type="signal", name="Fidelity Check (Phase 2)"),
        Node(id="decision_heal", type="signal", name="Heal or Escalate"),
        Node(id="decision_bee_result", type="signal", name="Bee Result Router"),
        Node(id="decision_triage", type="signal", name="Triage Verdict"),
    ],
    edges=[
        # Sequential flows
        Edge(id="e1", from_node="gate_0", to_node="decision_fidelity_gate0", type="then"),
        Edge(id="e2", from_node="decision_fidelity_gate0", to_node="phase_0", type="switch", guard="fidelity >= 0.85"),
        Edge(id="e3", from_node="decision_fidelity_gate0", to_node="decision_heal", type="switch", guard="fidelity < 0.85"),

        # Healing loop
        Edge(id="e4", from_node="decision_heal", to_node="gate_0", type="repeat", guard="attempt < 3"),
        Edge(id="e5", from_node="decision_heal", to_node="q33nr_review", type="then", guard="attempt >= 3"),

        # Phase 0 flow
        Edge(id="e6", from_node="phase_0", to_node="decision_fidelity_phase0", type="then"),
        Edge(id="e7", from_node="decision_fidelity_phase0", to_node="phase_1", type="switch", guard="fidelity >= 0.85"),
        Edge(id="e8", from_node="decision_fidelity_phase0", to_node="decision_heal", type="switch", guard="fidelity < 0.85"),

        # Continue for all stages...
        # Bee result routing
        Edge(id="e20", from_node="bee_execution", to_node="decision_bee_result", type="then"),
        Edge(id="e21", from_node="decision_bee_result", to_node="post_dispatch_verify", type="switch", guard="result == 'CLEAN'"),
        Edge(id="e22", from_node="decision_bee_result", to_node="decision_triage", type="switch", guard="result in ['TIMEOUT', 'NEEDS_DAVE', 'CRASH']"),

        # Triage routing
        Edge(id="e23", from_node="decision_triage", to_node="post_dispatch_verify", type="switch", guard="verdict == 'COMPLETE_ENOUGH'"),
        Edge(id="e24", from_node="decision_triage", to_node="dispatch", type="switch", guard="verdict == 'PARTIAL_SAFE'"),
        Edge(id="e25", from_node="decision_triage", to_node="dispatch", type="switch", guard="verdict == 'REVERT'"),

        # Final stages
        Edge(id="e26", from_node="post_dispatch_verify", to_node="q33n_review", type="then"),
        Edge(id="e27", from_node="q33n_review", to_node="archive_inventory", type="then"),
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
        Distribution(id="dist_task_breakdown", type="constant", params={"value": 30}, unit="seconds"),
        Distribution(id="dist_q33nr_review", type="uniform", params={"min": 60, "max": 300}, unit="seconds"),
        Distribution(id="dist_dispatch", type="constant", params={"value": 2}, unit="seconds"),
        Distribution(id="dist_bee_exec", type="lognormal", params={"mean": 180, "sigma": 1.5}, unit="seconds"),
        Distribution(id="dist_verify", type="constant", params={"value": 10}, unit="seconds"),
        Distribution(id="dist_q33n_review", type="constant", params={"value": 30}, unit="seconds"),
        Distribution(id="dist_archive", type="constant", params={"value": 5}, unit="seconds"),
    ],
)

# Serialize to JSON
from engine.phase_ir.schema import flow_to_json
json_output = flow_to_json(flow)

# Write to file
with open("pipeline.ir.json", "w") as f:
    f.write(json_output)
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-226-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full absolute paths
3. **What Was Done** — bullet list of concrete changes (not intent)
4. **Test Results** — test files run, pass/fail counts, output summary
5. **Build Verification** — pytest output showing all tests pass
6. **Acceptance Criteria** — copy from task deliverables, mark [x] or [ ] with explanation
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, recommended next tasks

DO NOT skip any section.

## Success Criteria

The task is complete when:

1. ✅ `pipeline.ir.json` exists at the specified path
2. ✅ IR is valid JSON that can be parsed
3. ✅ IR passes `validate_flow_structure()` with zero errors
4. ✅ At least 11 activity nodes exist (matching pipeline stages)
5. ✅ At least 4 decision nodes exist (fidelity, heal, bee result, triage)
6. ✅ At least 20 edges exist (covering all transitions including loops)
7. ✅ 3 resources defined with correct capacities and types
8. ✅ 9+ distributions defined with correct params and units
9. ✅ All tests pass (minimum 8 tests, recommend 12)
10. ✅ Response file written with all 8 sections

## Notes

- Use the template above as a starting point, but ensure ALL stages from SPEC-PIPELINE-001 are represented
- Decision nodes need multiple fidelity checks (one after each gate/phase)
- Healing loop edges need guard conditions (attempt < 3 vs attempt >= 3)
- Bee result routing needs branches for all outcomes (CLEAN, TIMEOUT, NEEDS_DAVE, CRASH)
- Triage verdict routing needs branches for all verdicts (COMPLETE_ENOUGH, PARTIAL_SAFE, REVERT)
- If IR exceeds 500 lines, use compact JSON formatting (indent=None or indent=0)
- Test the round-trip: IR → dict → IR should preserve all structure
- Node IDs must be unique and edges must reference valid node IDs
