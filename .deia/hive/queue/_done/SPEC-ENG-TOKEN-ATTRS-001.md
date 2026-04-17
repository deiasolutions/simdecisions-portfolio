# SPEC-ENG-TOKEN-ATTRS-001

**MODE: EXECUTE**

**Spec ID:** SPEC-ENG-TOKEN-ATTRS-001
**Created:** 2026-04-09
**Author:** Q88N

---

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

---

## Objective

Add token attribute read/write access to production engine node execution
so that PRISM-IR task nodes can read attributes like `treatment`,
`run_number`, and `branch` from the current token, and write new
attributes back. This is Gap 2 from EXP-IR-READINESS survey. It enables
the decision node that routes hive vs opus_solo treatment paths in
SPEC-EXPERIMENT-HIVE-VS-OPUS-001.

---

## Background

The readiness survey (`20260409-EXP-IR-READINESS-RESPONSE.md`) confirmed:

- Tokens exist and carry a state machine with lifecycle tracking
- Token attributes (arbitrary key-value metadata) are not accessible
  inside executor `execute()` calls
- The `ExecutorContext` or equivalent passed to executors does not
  currently expose the active token or its attributes
- Decision nodes (type: `decision`) need to evaluate expressions against
  token attributes to route correctly

The fix is to pass token attribute access into the executor context so
node handlers — including `ShellExecutor`, decision evaluators, and LLM
executors — can read and conditionally write token attributes.

---

## Survey First

Before writing any code, read:

- `engine/des/tokens.py` — token data model, attribute storage,
  how attributes are currently set/read
- `engine/des/engine.py` — how executor context is constructed and
  passed to `execute()` calls
- `engine/des/core.py` — EngineState, how tokens are accessed
- `engine/phase_ir/expressions/evaluator.py` — expression evaluation,
  confirm if token attributes are in scope
- Any existing executor as a reference for how context is consumed
- `.deia/hive/responses/20260409-EXP-IR-READINESS-RESPONSE.md` —
  prior survey results for file+line context

Report file paths, line counts, and the exact context construction
pattern before writing any new code.

---

## What To Build

### 1. Token attribute access surface

Tokens must expose a clean read/write interface. If this does not already
exist on the `Token` class, add it:

```python
# Read
token.get_attr(key: str, default=None) -> Any

# Write
token.set_attr(key: str, value: Any) -> None

# Read all
token.attrs() -> dict
```

Attributes are arbitrary JSON-serializable key-value pairs. Store in
an `_attributes: dict` field on the token. Initialize as `{}`.

If the `Token` class already has an `attributes` dict or equivalent,
use it — do not duplicate. Report what you find in the survey section.

### 2. Executor context includes active token

The context object passed to every `executor.execute(node, context)`
call must include a reference to the active token. Specifically:

```python
context["token"] = active_token       # Token object (read/write)
context["token_attrs"] = active_token.attrs()  # Snapshot dict (read-only copy)
```

`context["token"]` is the live object — mutations via `set_attr` persist.
`context["token_attrs"]` is a snapshot dict for use in expression
evaluation (safe, no mutation risk).

Find where `ExecutorContext` (or the equivalent dict) is constructed
before dispatch. Add both fields there. One change, one location.

### 3. Expression evaluator has token attrs in scope

The expression evaluator (`evaluator.py`) is used for decision node
guard conditions. Token attributes must be in its evaluation scope:

```python
# Guard expression examples that must now work:
"token.treatment == 'opus_solo'"
"token.run_number <= 3"
"token.branch != ''"
```

Find where the evaluator constructs its scope dict. Add:

```python
scope["token"] = context.get("token_attrs", {})
```

This is a read-only snapshot — guard expressions do not mutate tokens.

### 4. PRISM-IR node schema: `inputs` and `outputs` for token attrs

Document (do not enforce with validation) that nodes can declare:

```yaml
- id: route_by_treatment
  type: decision
  guard: "token.treatment == 'opus_solo'"
```

And executors can declare outputs that set token attrs:

```yaml
- id: create_branch
  type: subprocess
  command: "git checkout -b {{ token.branch }}"
  outputs:
    - attr: branch_created
      value: "{{ output.success }}"
```

The `{{ token.X }}` template syntax is already in scope if the expression
evaluator is wired correctly. Confirm it works with the smoke test.

### 5. `engine/des/tests/test_token_attrs.py` (new file)

Minimum 15 tests.

Required test cases:

```
test_token_initializes_with_empty_attrs
test_set_attr_stores_value
test_get_attr_returns_value
test_get_attr_returns_default_when_missing
test_attrs_returns_full_dict
test_attrs_snapshot_is_copy_not_reference
test_executor_context_includes_token
test_executor_context_includes_token_attrs_snapshot
test_token_attrs_accessible_in_expression_evaluator
test_treatment_attr_routes_decision_node_correctly
test_run_number_attr_accessible_in_guard
test_set_attr_in_executor_persists_to_next_node
test_token_attrs_snapshot_does_not_mutate_token
test_multiple_attrs_set_and_read
test_attrs_survives_engine_checkpoint_restore
```

---

## Acceptance Criteria

- [ ] `Token.get_attr()`, `Token.set_attr()`, `Token.attrs()` exist
      and work (or equivalent already exists and is confirmed working)
- [ ] `context["token"]` present in every executor call
- [ ] `context["token_attrs"]` present as read-only snapshot dict
- [ ] Expression evaluator has `token` in scope for guard expressions
- [ ] Guard `"token.treatment == 'opus_solo'"` evaluates correctly
- [ ] Guard `"token.run_number <= 3"` evaluates correctly
- [ ] `set_attr` on token in one node is readable by the next node
- [ ] `test_token_attrs.py` — 15 tests, all pass, no stubs
- [ ] Existing engine tests unbroken — run full suite, report result
- [ ] No file over 500 lines (if `tokens.py` is large, do not add to it
      beyond the three methods; extract to `token_attrs.py` if needed)

---

## Smoke Test

```bash
# Confirm token attr access works end-to-end
python -c "
from engine.des.tokens import Token
t = Token(id='test-1', node_id='start')
t.set_attr('treatment', 'hive')
t.set_attr('run_number', 2)
print(t.get_attr('treatment'))   # hive
print(t.get_attr('run_number'))  # 2
print(t.attrs())                 # {'treatment': 'hive', 'run_number': 2}
print(t.get_attr('missing', 'default'))  # default
"
# Expected: all four print correctly

# Confirm expression evaluator resolves token attrs
python -c "
from engine.phase_ir.expressions.evaluator import evaluate_expression
ctx = {'token': {'treatment': 'opus_solo', 'run_number': 1}}
print(evaluate_expression(\"token['treatment'] == 'opus_solo'\", ctx))  # True
print(evaluate_expression(\"token['run_number'] <= 3\", ctx))           # True
"
# Expected: True, True

# Run new tests
python -m pytest engine/des/tests/test_token_attrs.py -v
# Expected: 15 passed

# Run full engine test suite
python -m pytest engine/ -q
# Expected: all existing tests still pass
```

---

## Constraints

- No file over 500 lines
- If `tokens.py` is already large, add only the three methods and extract
  helpers to `token_attrs.py` rather than bloating `tokens.py`
- Do not change the token state machine or lifecycle — only add attrs
- Do not change expression evaluator logic — only add token to scope
- All tests use in-process objects — no subprocess calls, no disk I/O
- ASCII-safe output (Windows compatible)
- Python 3.13

---

## Response File

`.deia/hive/responses/YYYYMMDD-SPEC-ENG-TOKEN-ATTRS-001-RESPONSE.md`

All 8 sections mandatory: Header, Survey Results, Files Modified,
What Was Done, Test Results, Acceptance Criteria, Clock/Coin/Carbon,
Issues/Follow-ups.

---

*SPEC-ENG-TOKEN-ATTRS-001 — Q88N — 2026-04-09*
