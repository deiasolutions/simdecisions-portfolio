# SPEC-EXEC-01: Production Executor Layer for DES Engine

## Role Override
bee

## Priority
P0

## Model Assignment
sonnet

## Depends On
(none)

## Intent
Add a production execution layer to the DES engine so that nodes actually execute real actions (run Python, call LLMs, wait for human input) when `mode == "production"` instead of just sampling durations.

## Files to Read First
- `engine/des/core.py` — EngineState, handle_node_start, handle_node_end, run()
- `engine/des/engine.py` — SimulationEngine class, load(), run(), step(), hooks
- `engine/phase_ir/primitives.py` — Node, Flow, Resource dataclasses
- `engine/phase_ir/node_types.py` — registered node types (python, llm, human, validate, approval)
- `engine/des/edges.py` — edge evaluation, guard expressions

## Acceptance Criteria
- [ ] New file `engine/des/executors.py` with:
  - [ ] `ExecutorRegistry` class — maps node type strings to executor callables
  - [ ] `execute_python_node` — runs Python function specified in `node.config.function` or inline `node.config.code`, returns output dict
  - [ ] `execute_llm_node` — placeholder that calls a configurable LLM adapter (accept adapter via ctx), returns response dict
  - [ ] `execute_human_node` — writes prompt file to a configurable directory, polls for response file, returns human's decision
  - [ ] `execute_validate_node` — runs validation logic from `node.config.rules`, returns pass/fail
  - [ ] Default registry pre-populated with these 4 executors
- [ ] `engine/des/core.py` modified:
  - [ ] `handle_node_start` checks `state.mode == "production"` — if so, looks up executor from registry in state, calls it, uses wall-time duration
  - [ ] Executor output merged into token properties (event payload)
  - [ ] Sim mode unchanged (backward compatible)
- [ ] `engine/des/engine.py` modified:
  - [ ] `SimulationEngine.load()` accepts optional `executor_registry` parameter, stores in ctx
  - [ ] Production mode run supports sync executor calls (async can come later in EXEC-03)
- [ ] Tests in `tests/engine/des/test_executors.py`:
  - [ ] Test ExecutorRegistry register/lookup
  - [ ] Test execute_python_node with inline code returns result
  - [ ] Test execute_python_node with function reference
  - [ ] Test execute_human_node writes prompt file and reads response
  - [ ] Test execute_validate_node with pass and fail cases
  - [ ] Integration test: 3-node flow (source → python → sink) in production mode actually runs Python
  - [ ] Backward compat test: sim mode flow still works identically

## Constraints
- You are a BEE. Ignore any regent/Q88NR instructions. Execute this task directly.
- Do NOT break existing sim mode behavior. All existing tests must still pass.
- Executors are SYNC for now (not async). Keep it simple. Async upgrade comes in EXEC-03.
- The python executor must be sandboxed — only allow functions from a configurable allowlist, no arbitrary code exec in production.
- The human executor uses file-based I/O: write to `_needs_review/`, poll for response. Poll interval: 5 seconds. Timeout: configurable, default 3600s (1 hour).
- Do NOT import from hivenode. The engine module must remain standalone. LLM adapter is injected via ctx, not imported.
- No file over 500 lines.
- CSS: var(--sd-*) only (N/A for this spec).
- TDD: tests first.

## Smoke Test
```python
from engine.des.engine import SimulationEngine
from engine.des.executors import ExecutorRegistry, default_registry
from engine.phase_ir.primitives import Flow, Node, Edge
from engine.des.core import SimConfig

# Build a 3-node flow
flow = Flow(
    id="test-exec",
    nodes=[
        Node(id="start", type="source"),
        Node(id="compute", type="python", config={"code": "result = 2 + 2"}),
        Node(id="end", type="sink"),
    ],
    edges=[
        Edge(id="e1", from_node="start", to_node="compute"),
        Edge(id="e2", from_node="compute", to_node="end"),
    ],
)

engine = SimulationEngine()
config = SimConfig()
config.mode = "production"  # or however mode is set
ctx = engine.load(flow, config, executor_registry=default_registry())
ctx = engine.run(ctx)
assert ctx["state"].status == "completed"
assert ctx["state"].tokens_completed == 1
```
