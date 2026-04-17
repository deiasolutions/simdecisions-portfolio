# Briefing: Wire DES Engine Production Execution Layer + Build Integrity Flow

## Objective

Turn the SimDecisions DES engine from a simulator into a process executor, then express PROCESS-0013 (Build Integrity 3-Phase Validation) as a PHASE-IR flow that the engine runs in production mode. The queue runner calls the engine instead of dispatching regent bots directly.

## Why

The build pipeline dispatches bees and captures raw output, but skips all quality gates. PROCESS-0013 defines Gate 0 (disambiguation), Phase 0 (coverage), Phase 1 (spec fidelity), Phase 2 (task fidelity) with healing loops and human escalation. This process exists on paper but isn't enforced. By expressing it as an executable IR flow, the DES engine orchestrates the gates automatically.

## Architecture

### Current State
```
spec → queue runner → dispatch regent bot → bee writes code → RAW.txt captured → _done/
```
No gates. No validation. No response file enforcement.

### Target State
```
spec → queue runner → DES engine (production mode) loads build-integrity.phase
  → Gate 0: extract requirements, compare trees, heal if needed
  → Phase 0: coverage validation, heal if needed
  → Phase 1: spec→IR→spec' fidelity check, heal if needed
  → Phase 2: task→IR→task' fidelity check, heal if needed
  → All pass → dispatch bee
  → 3x fail → escalate to _needs_review/ (file-based, human approves/edits/aborts)
```

### The Gap: Production Mode Executors

The engine has `mode: "production"` as a concept but nodes don't execute real actions. Need an executor registry:

- `python` nodes → actually run Python functions
- `llm` nodes → actually call LLM APIs (via hivenode/llm/router.py)
- `human` nodes → write prompt to `_needs_review/`, poll for response file
- `validate` nodes → run validation logic, return pass/fail
- `approval` nodes → same as human, but with approve/reject semantics

## 3 Specs (Sequential)

### SPEC-EXEC-01: Production Executor Layer
- New file: `engine/des/executors.py` — executor registry + async handlers
- Modify: `engine/des/core.py` — `handle_node_start` checks mode, calls executor in production
- Modify: `engine/des/engine.py` — async support for production mode `run()`
- Test: simple 3-node flow (source → python → sink) that actually runs Python code
- Acceptance: `python -m pytest tests/engine/des/test_executors.py` passes

### SPEC-EXEC-02: Build Integrity IR Flow
- New file: `engine/flows/build-integrity.phase` — PROCESS-0013 as PHASE-IR YAML
- ~25 nodes: sources, python, llm, decision, human (escalation), sinks
- Variables: retry counters, coverage score, fidelity scores
- Resources: llm_budget, human_reviewer
- Edge types: then, switch (gate decisions), repeat (healing loops)
- Test: structural validation passes, sim run completes with tokens reaching all sinks

### SPEC-EXEC-03: Queue Runner Integration
- Modify: `.deia/hive/scripts/queue/spec_processor.py` — load and run build-integrity flow
- Spec enters queue → engine runs gates → dispatch on success, `_needs_review/` on escalation
- End-to-end test with a test spec

## Key Files

| Existing | Purpose |
|----------|---------|
| `engine/des/core.py` | Event handlers, `handle_node_start`, `EngineState` |
| `engine/des/engine.py` | `SimulationEngine.load()`, `.run()`, `.step()`, hooks |
| `engine/phase_ir/primitives.py` | Flow, Node, Edge, Resource, Variable dataclasses |
| `engine/phase_ir/node_types.py` | 28 registered node types (python, llm, human, validate, approval, etc.) |
| `engine/des/edges.py` | Guard evaluation, switch/fork/join/repeat edge logic |
| `engine/phase_ir/schema.py` | YAML/JSON serialization, structural validation |
| `hivenode/llm/router.py` | Multi-vendor LLM routing (for llm node executor) |
| `.deia/processes/PROCESS-0013-BUILD-INTEGRITY-3PHASE.md` | The process to encode as IR |
| `.deia/hive/scripts/queue/spec_processor.py` | Current queue runner spec processing |

## Human Escalation Design

File-based:
1. Engine writes `ESCALATION-<spec-id>.md` to `_needs_review/` with diagnostic
2. Engine checkpoints and pauses flow
3. Human creates response file (`approve`/`edited`/`abort`)
4. Engine polls, detects response, resumes or terminates flow

## Model Assignments

- EXEC-01: **sonnet** (core engine work, async patterns)
- EXEC-02: **sonnet** (IR authoring needs understanding of both PROCESS-0013 and PHASE-IR schema)
- EXEC-03: **sonnet** (integration work touching queue runner and engine)
