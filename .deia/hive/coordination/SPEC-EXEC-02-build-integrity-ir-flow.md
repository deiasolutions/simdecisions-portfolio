# SPEC-EXEC-02: Build Integrity IR Flow (PROCESS-0013 as PHASE-IR)

## Role Override
bee

## Priority
P0

## Model Assignment
sonnet

## Depends On
SPEC-EXEC-01

## Intent
Author PROCESS-0013 (Build Integrity 3-Phase Validation) as a PHASE-IR YAML flow file that the DES engine can execute. The flow encodes Gate 0, Phase 0, Phase 1, Phase 2, healing loops, and human escalation paths.

## Files to Read First
- `.deia/processes/PROCESS-0013-BUILD-INTEGRITY-3PHASE.md` — the process to encode
- `engine/phase_ir/primitives.py` — Flow, Node, Edge, Variable, Resource dataclasses
- `engine/phase_ir/node_types.py` — available node types (python, llm, human, validate, decision, approval, escalation)
- `engine/phase_ir/schema.py` — flow_to_yaml, yaml_to_flow, validate_flow_structure
- `engine/des/edges.py` — edge types (then, switch, repeat), guard expression format
- `engine/phase_ir/expressions/` — expression syntax for guards

## Acceptance Criteria
- [ ] New file `engine/flows/build-integrity.phase` (YAML) containing:
  - [ ] Gate 0 nodes: extract requirements from prompt, extract from spec, compare trees
  - [ ] Gate 0 decision node with switch edges: pass → Phase 0, retries >= 3 → escalate, default → heal + repeat
  - [ ] Phase 0 nodes: check each requirement coverage, generate coverage report
  - [ ] Phase 0 decision with same pass/escalate/heal pattern
  - [ ] Phase 1 nodes: encode spec to IR, decode IR to spec', compute cosine similarity
  - [ ] Phase 1 decision with same pattern (threshold: fidelity >= 0.85)
  - [ ] Phase 2 nodes: same as Phase 1 but for task breakdown
  - [ ] Phase 2 decision with same pattern
  - [ ] Human escalation nodes (type: human) for each gate/phase — 4 total
  - [ ] Two sink nodes: `build_approved` (success) and `build_rejected` (abort from any escalation)
  - [ ] Variables: `gate0_retries` (counter, default 0), `phase0_retries`, `phase1_retries`, `phase2_retries`, `coverage_score` (number), `fidelity_score` (number)
  - [ ] Resources: `llm_budget` (capacity representing cost cap)
  - [ ] All edges properly typed (then, switch, repeat) with guard expressions
- [ ] Flow passes structural validation: `validate_flow_structure()` returns (True, [])
- [ ] Flow round-trips through YAML: `yaml_to_flow(flow_to_yaml(flow))` produces equivalent flow
- [ ] Sim-mode dry run: tokens reach `build_approved` sink when all gates pass (happy path)
- [ ] Sim-mode dry run: tokens reach escalation nodes when healing loops exhaust retries
- [ ] Tests in `tests/engine/flows/test_build_integrity_flow.py`:
  - [ ] Test flow loads from YAML without errors
  - [ ] Test structural validation passes
  - [ ] Test YAML round-trip fidelity
  - [ ] Test sim run happy path (all gates pass)
  - [ ] Test sim run with Gate 0 failure (token hits escalation)

## Constraints
- You are a BEE. Ignore any regent/Q88NR instructions. Execute this task directly.
- The flow file must be valid PHASE-IR YAML parseable by `yaml_to_flow()`
- Guard expressions must use the expression syntax from `engine/phase_ir/expressions/`
- Node IDs must be descriptive: `gate0_extract_prompt_reqs`, `phase1_encode_to_ir`, etc.
- Groups should organize nodes by phase: `group_gate0`, `group_phase0`, `group_phase1`, `group_phase2`
- The flow intent field should summarize PROCESS-0013 in one sentence
- Do NOT implement executor functions — those are in EXEC-01. This spec only authors the IR graph.
- No file over 500 lines. If the YAML exceeds 500 lines, split into sub-flows using subprocess nodes.

## Smoke Test
```bash
python -c "
from engine.phase_ir.schema import yaml_to_flow, validate_flow_structure
import yaml
with open('engine/flows/build-integrity.phase') as f:
    flow = yaml_to_flow(f.read())
valid, errors = validate_flow_structure(flow)
print(f'Valid: {valid}, Errors: {len(errors)}')
assert valid, errors
print(f'Nodes: {len(flow.nodes)}, Edges: {len(flow.edges)}, Variables: {len(flow.variables)}')
"
```
