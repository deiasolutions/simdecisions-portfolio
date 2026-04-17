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

# SPEC-DES-COLORED-ARCS-001

**Title:** Add arc filtering for colored Petri nets  
**Priority:** P3  
**Status:** DRAFT  
**Date:** 2026-04-15  
**Author:** Q88N  
**Depends on:** None

---

## Problem

PRISM-IR supports colored tokens — tokens carry properties (attributes) that distinguish them:

```yaml
token.properties = {
    "customer_type": "vip",
    "region": "EU",
    "priority": 3
}
```

But from the audit (2026-04-14):
> "gap_008: No colored Petri net arc filters"

Edges can have guards (`c:` conditions) that evaluate to true/false. But they can't filter WHICH tokens to accept based on color. All tokens of any color traverse if the guard passes.

Colored Petri net semantics require arc inscriptions — filters that match specific token colors.

---

## Use Case

```yaml
edges:
  - s: order_queue
    t: vip_handler
    filter: "token.properties.customer_type == 'vip'"
  
  - s: order_queue
    t: standard_handler
    filter: "token.properties.customer_type != 'vip'"
```

Without arc filters, both edges fire for every token (if guards pass). With arc filters, VIP tokens go to vip_handler, others go to standard_handler.

This is different from a decision node — the filtering happens at the arc level, enabling pattern-matching dispatch from queues and places.

---

## Solution

Add `filter` field to edges that selects which tokens can traverse.

---

## Requirements

### R1: Filter field on edges

```yaml
edges:
  - s: source
    t: target
    c: "flow.status == 'active'"     # Guard: must be true to consider edge
    filter: "token.properties.color == 'red'"  # Filter: token must match
```

Semantics:
1. **Guard (`c:`)** — Evaluated once. If false, edge is disabled for all tokens.
2. **Filter (`filter:`)** — Evaluated per token. Only matching tokens traverse.

Both must pass for a token to traverse.

### R2: Filter expression language

Same expression language as guards:

```yaml
# Exact match
filter: "token.properties.region == 'US'"

# Membership
filter: "token.properties.priority in [1, 2, 3]"

# Compound
filter: "token.properties.type == 'order' and entity.amount > 1000"

# Negation
filter: "token.properties.status != 'cancelled'"
```

### R3: Multiple outbound edges with filters

When a node has multiple outbound edges with filters:

```yaml
edges:
  - { s: dispatch, t: handler_a, filter: "token.properties.type == 'a'" }
  - { s: dispatch, t: handler_b, filter: "token.properties.type == 'b'" }
  - { s: dispatch, t: handler_c, filter: "true" }  # Catch-all
```

Evaluation order:
1. Evaluate all edge filters against the token
2. Token traverses ALL matching edges (colored PN semantics)
3. If multiple match, token may fork (like inclusive decision)

To get exclusive routing, use mutually exclusive filters or a decision node.

### R4: No-match behavior

If a token matches no outbound filters:

```yaml
nodes:
  - id: dispatch
    t: task
    no_filter_match: error  # error | hold | default_edge
```

- `error`: Raise exception (default)
- `hold`: Token stays at node, state = `waiting_filter`
- `default_edge`: Use edge with `filter: "true"` or no filter

### R5: Filter on join arcs

Joins can filter which tokens they accept:

```yaml
edges:
  - { s: branch_a, t: join_point, filter: "token.properties.branch == 'a'" }
  - { s: branch_b, t: join_point, filter: "token.properties.branch == 'b'" }
```

Join only considers tokens that pass their respective arc filters.

### R6: Resource queue filtering

When releasing a resource, filter which waiting token to wake:

```yaml
resources:
  - id: specialists
    capacity: 5
    dispatch:
      mode: priority
      filter: "token.properties.specialist_type == resource.specialist_type"
```

Only tokens matching the filter are candidates for this resource.

### R7: Trace events

Log filter evaluations:

```python
emit_event(
    event_type="filter_evaluated",
    payload={
        "edge_id": edge_id,
        "token_id": token_id,
        "filter_expr": filter_expr,
        "result": True/False,
        "token_properties": token.properties
    }
)
```

Only emit for edges that have filters (avoid noise).

---

## Implementation Location

| File | Change |
|------|--------|
| `simdecisions/phase_ir/primitives.py` | Add `filter` field to Edge |
| `simdecisions/des/edges.py` | Evaluate filter per token in edge traversal |
| `simdecisions/des/core.py` | Check filter before emitting token to edge |
| `simdecisions/des/resources.py` | Apply filter in queue dispatch |

---

## Test Cases

### T1: Basic filter

```yaml
edges:
  - { s: start, t: red_handler,  filter: "token.properties.color == 'red'" }
  - { s: start, t: blue_handler, filter: "token.properties.color == 'blue'" }
```

- Red token → red_handler
- Blue token → blue_handler

### T2: Filter with guard

```yaml
edges:
  - s: dispatch
    t: premium
    c: "flow.premium_enabled"
    filter: "token.properties.tier == 'gold'"
```

- If `flow.premium_enabled == false`: edge disabled, no tokens traverse
- If enabled: only gold tokens traverse

### T3: Multiple matches (fork)

```yaml
edges:
  - { s: notify, t: email, filter: "entity.channels.email" }
  - { s: notify, t: sms,   filter: "entity.channels.sms" }
```

Token with `{email: true, sms: true}`:
- Matches both → forks to email AND sms

### T4: No match error

```yaml
edges:
  - { s: route, t: known, filter: "token.properties.type == 'known'" }
```

Token with `type: 'unknown'`:
- Matches nothing → error (default behavior)

### T5: Catch-all

```yaml
edges:
  - { s: route, t: special, filter: "token.properties.vip == true" }
  - { s: route, t: normal,  filter: "true" }  # Catch-all
```

- VIP tokens match both → fork to special AND normal
- Non-VIP tokens match only normal

To make exclusive:
```yaml
edges:
  - { s: route, t: special, filter: "token.properties.vip == true" }
  - { s: route, t: normal,  filter: "token.properties.vip != true" }
```

### T6: Resource filter

```yaml
resources:
  - id: language_agents
    capacity: 10
    dispatch:
      filter: "token.properties.language == agent.language"
```

Spanish-speaking token only matches Spanish-speaking agent.

---

## Acceptance Criteria

- [ ] `filter` field on edges evaluated per token
- [ ] Guard (`c:`) and filter both must pass for traversal
- [ ] Multiple matching edges cause token fork
- [ ] No-match behavior configurable (error/hold/default)
- [ ] Filters work on join inbound edges
- [ ] Resource dispatch respects filter
- [ ] `filter_evaluated` events emitted for filtered edges
- [ ] Expression language consistent with guards
- [ ] Existing tests still pass

---

## Out of Scope

- **Arc weights with filters** — filter + weight combinations (future)
- **Dynamic filter modification** — changing filters at runtime
- **Filter optimization** — indexing tokens by properties for fast lookup

---

## Estimated Effort

4-5 hours. Expression evaluation exists. Main work is per-token filter check in edge traversal and resource dispatch.

---

## Notes

Arc filters complete the colored Petri net support. Without them:
- Colored tokens exist but can't be routed by color
- Must use decision nodes for all color-based routing
- Resource matching by token properties impossible

With filters, the flow graph itself becomes color-aware.

## Triage History
- 2026-04-16T14:49:55.189592Z — requeued (empty output)
- 2026-04-16T15:09:55.212633Z — requeued (empty output)
- 2026-04-16T15:14:55.234358Z — requeued (empty output)
