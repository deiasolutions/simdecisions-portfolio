---
id: EXEC-02
priority: P0
model: sonnet
role: bee
depends_on:
  - EXEC-01
---
# SPEC-EXEC-02: Build Integrity IR Flow (PROCESS-0013 as PRISM-IR)

## Intent
Author PROCESS-0013 (Build Integrity 3-Phase Validation) as a PRISM-IR flow file that the DES engine can execute. The flow encodes Gate 0, Phase 0, Phase 1, Phase 2, healing loops, and decision escalation paths.

## Files to Read First
- `.deia/processes/PROCESS-0013-BUILD-INTEGRITY-3PHASE.md` — the process to encode
- `.wiki/specs/PRISM-IR-SPEC.md` — canonical PRISM-IR specification (v1.0)
- `engine/phase_ir/primitives.py` — Flow, Node, Edge, Variable, Resource dataclasses
- `engine/phase_ir/node_types.py` — available node types per PRISM-IR spec (start, end, task, decision, fork, join, vote, checkpoint, event_wait, cancel)
- `engine/phase_ir/schema.py` — prism_to_flow, flow_to_prism, validate_flow_structure
- `engine/des/edges.py` — edge conditions, guard expression format

## Acceptance Criteria
- [ ] New file `.wiki/processes/build-integrity.prism.md` containing:
  - [ ] YAML frontmatter: `prism: build-integrity`, `version: 1.0.0`
  - [ ] Gate 0 nodes (type: `task`, operator: `llm`):
    - `gate0_extract_prompt_reqs` — prompt: `[[.wiki/prompts/extract-requirements]]`
    - `gate0_extract_spec_reqs` — prompt: `[[.wiki/prompts/extract-requirements]]`
    - `gate0_compare_trees` — prompt: `[[.wiki/prompts/compare-requirement-trees]]`
  - [ ] Gate 0 decision node with edges: pass → Phase 0, retries >= 3 → escalate, default → heal + repeat
  - [ ] Phase 0 nodes (type: `task`, operator: `llm`):
    - `phase0_check_coverage` — prompt: `[[.wiki/prompts/check-coverage]]`
    - `phase0_generate_report` — prompt: `[[.wiki/prompts/generate-phase-report]]`
  - [ ] Phase 0 decision with same pass/escalate/heal pattern
  - [ ] Phase 1 nodes (type: `task`, operator: `llm`):
    - `phase1_encode_to_ir` — prompt: `[[.wiki/prompts/encode-spec-to-ir]]`
    - `phase1_decode_to_spec` — prompt: `[[.wiki/prompts/decode-ir-to-spec]]`
    - `phase1_compute_fidelity` — prompt: `[[.wiki/prompts/compute-fidelity]]`
  - [ ] Phase 1 decision with same pattern (threshold: fidelity >= 0.85)
  - [ ] Phase 2 nodes: same as Phase 1 but for task breakdown
  - [ ] Phase 2 decision with same pattern
  - [ ] Decision escalation nodes (type: `decision`, allowed_deciders: `[human]`) for each gate/phase — 4 total
  - [ ] Two end nodes: `build_approved` (success) and `build_rejected` (abort from any escalation)
  - [ ] Variables: `gate0_retries`, `phase0_retries`, `phase1_retries`, `phase2_retries`, `coverage_score`, `fidelity_score`
  - [ ] Resources: `llm_budget` (capacity representing cost cap)
  - [ ] All edges with proper conditions (`c:` field)
- [ ] Prompt wiki pages created in `.wiki/prompts/`:
  - [ ] `extract-requirements.md` — extracts requirement tree from text
  - [ ] `compare-requirement-trees.md` — compares two trees, returns coverage
  - [ ] `check-coverage.md` — checks if spec covers all requirements
  - [ ] `generate-phase-report.md` — generates PROCESS-0013 format report
  - [ ] `encode-spec-to-ir.md` — encodes spec to PRISM-IR
  - [ ] `decode-ir-to-spec.md` — decodes PRISM-IR back to spec
  - [ ] `compute-fidelity.md` — computes similarity score
  - [ ] `heal-spec.md` — regenerates spec based on diagnostic
- [ ] Flow passes structural validation: `validate_flow_structure()` returns (True, [])
- [ ] Flow round-trips through PRISM: `prism_to_flow(flow_to_prism(flow))` produces equivalent flow
- [ ] Sim-mode dry run: tokens reach `build_approved` sink when all gates pass (happy path)
- [ ] Sim-mode dry run: tokens reach escalation nodes when healing loops exhaust retries
- [ ] Tests in `tests/engine/flows/test_build_integrity_flow.py`:
  - [ ] Test flow loads from `.prism.md` without errors
  - [ ] Test structural validation passes
  - [ ] Test PRISM round-trip fidelity
  - [ ] Test sim run happy path (all gates pass)
  - [ ] Test sim run with Gate 0 failure (token hits escalation)

## Constraints
- You are a BEE. Ignore any regent/Q88NR instructions. Execute this task directly.
- The flow file must be valid PRISM-IR per `.wiki/specs/PRISM-IR-SPEC.md`
- File extension: `.prism.md` with YAML frontmatter
- Location: `.wiki/processes/` (it's knowledge, not code)
- **All gate/phase nodes are `type: task` with `o: {op: llm}`** — LLM-first, code later as optimization
- **Prompts live in wiki pages** — nodes reference them via `[[.wiki/prompts/prompt-name]]`
- Node IDs must be descriptive: `gate0_extract_prompt_reqs`, `phase1_encode_to_ir`, etc.
- Groups should organize nodes by phase: `group_gate0`, `group_phase0`, `group_phase1`, `group_phase2`
- The flow intention field should summarize PROCESS-0013 in one sentence
- Do NOT implement executor functions — those are in EXEC-01. This spec only authors the IR graph.
- No file over 500 lines. If the flow exceeds 500 lines, split into sub-flows using subprocess nodes.

## Smoke Test
```bash
python -c "
from engine.phase_ir.schema import prism_to_flow, validate_flow_structure

with open('.wiki/processes/build-integrity.prism.md') as f:
    content = f.read()
    # Skip frontmatter, extract YAML block
    flow = prism_to_flow(content)

valid, errors = validate_flow_structure(flow)
print(f'Valid: {valid}, Errors: {len(errors)}')
assert valid, errors
print(f'Nodes: {len(flow.nodes)}, Edges: {len(flow.edges)}, Variables: {len(flow.variables)}')
"
```
