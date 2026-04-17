## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

# SPEC-DES-DECISION-001

**Title:** Implement decision node executor  
**Priority:** P2  
**Status:** DRAFT  
**Date:** 2026-04-15  
**Author:** Q88N  
**Depends on:** None

---

## Problem

PRISM-IR defines `t: decision` nodes for conditional routing:

```yaml
- id: route_by_risk
  t: decision
  mode: exclusive
  out:
    low_risk: fast_track
    high_risk: manual_review
    default: standard_path
```

From the audit (2026-04-14):
> "gap_007: decision node execution incomplete"

The engine doesn't properly:
- Evaluate decision conditions
- Support `mode: exclusive` vs `mode: inclusive`
- Handle `out:` mapping syntax
- Support expression-based, LLM-based, or HTTP-based decisions
- Emit decision outcomes to ledger

Tokens hitting decision nodes may not route correctly.

---

## Solution

Implement full decision node executor with multiple decision modes.

### Decision Modes

| Mode | Behavior |
|------|----------|
| `exclusive` | Exactly one outbound edge fires (first match or default) |
| `inclusive` | All matching edges fire (token may fork) |

### Decision Methods

| Method | How it decides |
|--------|----------------|
| `expression` | Evaluate condition expressions on edges (default) |
| `llm` | LLM picks outcome (simulation: sample from distribution) |
| `http` | External API returns decision (simulation: sample from distribution) |
| `lookup` | Table lookup based on entity attributes |

---

## Requirements

### R1: Expression-based decision (default)

Evaluate edge conditions, route to first match:

```yaml
- id: risk_decision
  t: decision
  mode: exclusive

edges:
  - { s: risk_decision, t: fast_track,    c: "entity.risk_score < 0.3" }
  - { s: risk_decision, t: manual_review, c: "entity.risk_score >= 0.7" }
  - { s: risk_decision, t: standard,      c: "true" }  # default
```

Execution:
1. Get outbound edges sorted by definition order
2. Evaluate each edge condition against token context
3. `exclusive`: emit to first matching edge, stop
4. `inclusive`: emit to all matching edges (may create multiple tokens)

### R2: Out mapping syntax

Support `out:` block as shorthand for edge conditions:

```yaml
- id: approval_decision
  t: decision
  mode: exclusive
  decision:
    expr: "entity.status"  # Expression to evaluate
  out:
    approved: end_approved      # if expr == "approved" → end_approved
    rejected: end_rejected      # if expr == "rejected" → end_rejected
    pending: review_queue       # if expr == "pending" → review_queue
    default: error_handler      # fallback
```

This desugars to edge conditions internally:
```yaml
edges:
  - { s: approval_decision, t: end_approved,  c: "entity.status == 'approved'" }
  - { s: approval_decision, t: end_rejected,  c: "entity.status == 'rejected'" }
  - { s: approval_decision, t: review_queue,  c: "entity.status == 'pending'" }
  - { s: approval_decision, t: error_handler, c: "true" }
```

### R3: LLM-based decision (simulation mode)

For decisions that would use an LLM in production:

```yaml
- id: sentiment_decision
  t: decision
  mode: exclusive
  decision:
    method: llm
    model: "claude-sonnet-4"
    prompt: "Classify sentiment: ${entity.text}"
    outcomes:
      - { value: positive, weight: 0.6 }
      - { value: negative, weight: 0.3 }
      - { value: neutral,  weight: 0.1 }
  out:
    positive: happy_path
    negative: escalate
    neutral: standard
```

In simulation:
- Sample outcome from weighted distribution
- Route based on sampled value
- Log the simulated decision

### R4: HTTP-based decision (simulation mode)

For decisions that call external APIs:

```yaml
- id: fraud_check
  t: decision
  mode: exclusive
  decision:
    method: http
    url: "https://fraud.api/check"
    outcomes:
      - { value: clear, weight: 0.95 }
      - { value: flag,  weight: 0.04 }
      - { value: block, weight: 0.01 }
  out:
    clear: continue
    flag: review
    block: reject
```

In simulation: sample from weighted distribution.

### R5: Lookup-based decision

Table lookup for deterministic routing:

```yaml
- id: region_route
  t: decision
  mode: exclusive
  decision:
    method: lookup
    key: "entity.region"
    table:
      US: us_handler
      EU: eu_handler
      APAC: apac_handler
    default: global_handler
```

### R6: Inclusive mode (fork on decision)

When multiple conditions match, fork token:

```yaml
- id: notification_decision
  t: decision
  mode: inclusive  # All matches fire

edges:
  - { s: notification_decision, t: send_email, c: "entity.prefs.email == true" }
  - { s: notification_decision, t: send_sms,   c: "entity.prefs.sms == true" }
  - { s: notification_decision, t: send_push,  c: "entity.prefs.push == true" }
```

If entity has email and push but not sms:
- Fork into 2 tokens
- One goes to send_email, one goes to send_push

### R7: Decision outcome tracking

Record decision in token:

```python
token.properties["decisions"] = token.properties.get("decisions", [])
token.properties["decisions"].append({
    "node_id": node_id,
    "method": method,
    "outcome": outcome_value,
    "sim_time": sim_time
})
```

### R8: Trace events

```python
emit_event(
    event_type="decision_made",
    actor=f"node:{node_id}",
    target=f"token:{token_id}",
    payload_json=json.dumps({
        "method": method,        # expression|llm|http|lookup
        "outcome": outcome,      # The decided value
        "target_node": target,   # Where token is going
        "mode": mode,            # exclusive|inclusive
        "fork_count": fork_count # 1 for exclusive, N for inclusive
    })
)
```

### R9: No match handling

If no condition matches and no default:

```yaml
decision:
  no_match: error    # error | skip | default_edge
```

- `error`: Raise exception (default)
- `skip`: Token completes with outcome "no_match"
- `default_edge`: Use last edge as default

---

## Implementation Location

| File | Change |
|------|--------|
| `simdecisions/des/core.py` | Add `handle_decision()` with mode/method dispatch |
| `simdecisions/des/edges.py` | Condition evaluation (may already exist) |
| `simdecisions/phase_ir/primitives.py` | Verify decision node schema has `mode`, `decision`, `out` |
| `simdecisions/des/trace_writer.py` | Add `decision_made` event type |
| `simdecisions/des/loader_v2.py` | Desugar `out:` block to edge conditions |

---

## Test Cases

### T1: Exclusive expression-based

```yaml
- id: decide
  t: decision
  mode: exclusive

edges:
  - { s: decide, t: path_a, c: "entity.value > 100" }
  - { s: decide, t: path_b, c: "entity.value > 50" }
  - { s: decide, t: path_c, c: "true" }
```

- `entity.value = 150` → path_a (first match)
- `entity.value = 75` → path_b
- `entity.value = 25` → path_c (default)

### T2: Out mapping

```yaml
- id: status_route
  t: decision
  decision:
    expr: "entity.status"
  out:
    active: handle_active
    inactive: handle_inactive
    default: handle_unknown
```

- `entity.status = "active"` → handle_active
- `entity.status = "foo"` → handle_unknown

### T3: Inclusive mode

```yaml
- id: multi_notify
  t: decision
  mode: inclusive

edges:
  - { s: multi_notify, t: email, c: "entity.channels.email" }
  - { s: multi_notify, t: sms,   c: "entity.channels.sms" }
```

- `entity.channels = {email: true, sms: true}` → fork to both
- 2 tokens emitted

### T4: LLM simulation

```yaml
- id: classify
  t: decision
  decision:
    method: llm
    outcomes:
      - { value: a, weight: 0.5 }
      - { value: b, weight: 0.5 }
  out:
    a: path_a
    b: path_b
```

Run 1000 tokens with same seed:
- Approximately 500 to path_a, 500 to path_b
- Exact split reproducible with seed

### T5: No match error

```yaml
- id: strict_route
  t: decision
  mode: exclusive
  decision:
    no_match: error

edges:
  - { s: strict_route, t: known, c: "entity.type == 'known'" }
```

- `entity.type = "unknown"` → raises error (no match, no default)

---

## Acceptance Criteria

- [ ] `t: decision` nodes evaluate conditions and route tokens
- [ ] `mode: exclusive` routes to first match only
- [ ] `mode: inclusive` forks to all matches
- [ ] `out:` block desugars to edge conditions
- [ ] `method: expression` evaluates edge conditions (default)
- [ ] `method: llm` samples from weighted outcomes
- [ ] `method: http` samples from weighted outcomes
- [ ] `method: lookup` uses table mapping
- [ ] `decision_made` events emitted with outcome
- [ ] Token tracks decision history in properties
- [ ] No-match behavior configurable (error/skip/default)
- [ ] Existing tests still pass

---

## Out of Scope

- **Actual LLM calls** — simulation samples from distribution
- **Actual HTTP calls** — simulation samples from distribution
- **Decision caching** — same entity gets same decision (future optimization)
- **Decision explanation** — why this outcome (future)

---

## Estimated Effort

4-5 hours. Expression evaluation likely exists. Main work is mode handling, out desugaring, and method dispatch.

---

## Notes

Decision nodes are the routing backbone. Without proper execution:
- Conditional flows don't work
- Simulation can't model branching probabilities
- Path analysis (CURRENCY-002) has nothing to analyze

This spec makes decision nodes first-class citizens in the engine.

## Triage History
- 2026-04-16T14:49:55.193593Z — requeued (empty output)
- 2026-04-16T15:09:55.212633Z — requeued (empty output)
- 2026-04-16T15:14:55.238377Z — requeued (empty output)
