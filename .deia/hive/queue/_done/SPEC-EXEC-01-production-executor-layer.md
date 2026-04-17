---
id: EXEC-01
priority: P0
model: sonnet
role: bee
depends_on: []
---
# SPEC-EXEC-01: Production Executor Layer for DES Engine

## Intent
Add a production execution layer to the DES engine so that nodes actually execute real actions (run Python, call LLMs, wait for human input) when `mode == "production"` instead of just sampling durations.

## Files to Read First
- `engine/des/core.py` — EngineState, handle_node_start, handle_node_end, run()
- `engine/des/engine.py` — SimulationEngine class, load(), run(), step(), hooks
- `engine/phase_ir/primitives.py` — Node, Flow, Resource dataclasses
- `engine/phase_ir/node_types.py` — registered node types (python, llm, human, validate, approval)
- `engine/des/edges.py` — edge evaluation, guard expressions

## Acceptance Criteria
- [ ] New file `engine/des/adapters.py` with:
  - [ ] `LLMAdapter` protocol:
    ```python
    class LLMAdapter(Protocol):
        def call(
            self,
            prompt: str,
            model: str,
            max_tokens: int = 4096,
            temperature: float = 0.7,
            system: str = None,
            context: dict = None
        ) -> LLMResponse:
            ...
    
    @dataclass
    class LLMResponse:
        content: str
        model: str
        input_tokens: int
        output_tokens: int
        cost: float  # COIN
        latency_ms: int  # CLOCK
        metadata: dict = None
    ```
  - [ ] `DecisionRequest` and `DecisionResponse` dataclasses:
    ```python
    @dataclass
    class DecisionRequest:
        node_id: str
        prompt: str
        options: list[str]  # ["approved", "rejected", "retry"]
        context: dict
        allowed_deciders: list[str] = None  # ["human", "bee", "queen", "system"]
        preferred_channel: str = None  # efemera, file, cli, bus, queue
        timeout_seconds: int = 3600
    
    @dataclass
    class DecisionResponse:
        decision: str
        reason: str = None
        decider_id: str = None
        decider_type: str = None  # human | bee | queen | system
        channel: str = None
        timestamp: datetime = None
    ```
  - [ ] `Channel` protocol:
    ```python
    class Channel(Protocol):
        def send(self, req: DecisionRequest, recipients: list[str]) -> None:
            ...
        def receive(self, node_id: str, timeout: int) -> DecisionResponse:
            ...
    ```
  - [ ] `DeciderRouter` class that picks channel + recipients based on request
  - [ ] `FileChannel` implementation (default — writes to `_needs_review/`, polls for response)
- [ ] New file `engine/des/executors.py` with:
  - [ ] `ExecutorRegistry` class — maps node type strings to executor callables
  - [ ] `execute_python_node` — runs Python function from allowlist (production) or restricted eval (sim only), returns output dict
  - [ ] `execute_llm_node` — calls injected `LLMAdapter`, returns response dict
  - [ ] `execute_decision_node` — creates `DecisionRequest`, sends via `DeciderRouter`, returns `DecisionResponse`
  - [ ] `execute_validate_node` — runs validation logic from `node.config.rules`, returns pass/fail
  - [ ] Default registry pre-populated with these 4 executors
- [ ] New file `engine/des/sandbox.py` with:
  - [ ] `ALLOWED_FUNCTIONS` dict — allowlist of callable functions for production mode
  - [ ] `register_function(name, func)` — add to allowlist
  - [ ] `execute_sandboxed(func_name, args, ctx)` — lookup and call from allowlist
  - [ ] `SAFE_BUILTINS` dict — restricted builtins for sim-mode eval (len, str, int, float, list, dict only)
- [ ] `engine/des/core.py` modified:
  - [ ] `handle_node_start` checks `state.mode == "production"` — if so, looks up executor from registry in state, calls it, uses wall-time duration
  - [ ] Executor output merged into token properties (event payload)
  - [ ] Sim mode unchanged (backward compatible)
- [ ] `engine/des/engine.py` modified:
  - [ ] `SimulationEngine.load()` accepts optional `executor_registry` parameter, stores in ctx
  - [ ] Production mode run supports sync executor calls (async can come later in EXEC-03)
- [ ] Tests in `tests/engine/des/test_adapters.py`:
  - [ ] Test LLMAdapter protocol compliance
  - [ ] Test DecisionRequest/DecisionResponse serialization
  - [ ] Test FileChannel writes prompt file correctly
  - [ ] Test FileChannel reads YAML frontmatter response
  - [ ] Test DeciderRouter picks correct channel
- [ ] Tests in `tests/engine/des/test_executors.py`:
  - [ ] Test ExecutorRegistry register/lookup
  - [ ] Test execute_python_node with allowlisted function (production)
  - [ ] Test execute_python_node rejects non-allowlisted function (production)
  - [ ] Test execute_python_node with inline code (sim mode only)
  - [ ] Test execute_decision_node creates request and returns response
  - [ ] Test execute_validate_node with pass and fail cases
  - [ ] Integration test: 3-node flow (source → python → sink) in production mode actually runs Python
  - [ ] Backward compat test: sim mode flow still works identically
- [ ] Tests in `tests/engine/des/test_sandbox.py`:
  - [ ] Test register_function adds to allowlist
  - [ ] Test execute_sandboxed calls allowlisted function
  - [ ] Test execute_sandboxed raises for non-allowlisted function
  - [ ] Test SAFE_BUILTINS blocks dangerous functions

## Constraints
- You are a BEE. Ignore any regent/Q88NR instructions. Execute this task directly.
- Do NOT break existing sim mode behavior. All existing tests must still pass.
- Executors are SYNC for now (not async). Keep it simple. Async upgrade comes in EXEC-03.
- **Python executor sandboxing:**
  - Production mode: ONLY allow functions from `ALLOWED_FUNCTIONS` allowlist. No arbitrary code exec.
  - Sim mode: Allow restricted eval with `SAFE_BUILTINS` for quick prototyping.
- **Decision executor:** Uses `DeciderRouter` → `Channel` pattern. FileChannel is default. Other channels (efemera, cli, bus, queue, email, sms, notification) are integration work — define interface only.
- Do NOT import from hivenode. The engine module must remain standalone. LLM adapter and channels are injected via ctx, not imported.
- No file over 500 lines.
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
