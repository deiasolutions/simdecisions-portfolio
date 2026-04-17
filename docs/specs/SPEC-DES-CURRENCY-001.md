# SPEC-DES-CURRENCY-001

**Title:** Implement COIN (USD) currency computation  
**Priority:** P1  
**Status:** DRAFT  
**Date:** 2026-04-15  
**Author:** Q88N  
**Depends on:** None for cost computation. Test cases T2/T5 use resources but test cost arithmetic only — do not assert on resource utilization (that requires SPEC-DES-RESOURCE-BINDING-001).

---

## Problem

The DES engine tracks three currencies per the platform architecture:
- **CLOCK** — simulation time. ✓ Implemented. Emitted as `cost_tokens`.
- **COIN** — USD cost. ✗ Placeholder. Always emits `cost_usd=0.0`.
- **CARBON** — emissions. ✗ Heuristic. Separate spec (SPEC-DES-CARBON-001).

From the audit (2026-04-14):
> "COIN: PARTIAL — emitted as cost_usd=0.0 (placeholder, not computed from node execution costs)"

The ledger schema has the `cost_usd` column. The emission path exists. But nothing computes actual costs.

---

## Solution

Compute COIN from node execution based on operator type and resource usage.

### Cost Sources

| Source | How to compute |
|--------|----------------|
| LLM node | `tokens_in * input_cost + tokens_out * output_cost` per model |
| HTTP node | Fixed cost per call (from node config) or response-based |
| Script node | Fixed cost per invocation (from node config) |
| Human node | `duration * hourly_rate` (from resource config) |
| Resource hold | `hold_duration * cost_per_hour` (from resource config) |

### Cost Flow

```
node_start:
  → record start_time
  → IF operator is LLM:
      → estimate tokens (from input size)
      → record estimated_cost

node_end:
  → IF operator is LLM:
      → actual_cost = tokens_in * input_rate + tokens_out * output_rate
  → ELIF operator is HTTP:
      → actual_cost = node.cost_per_call (or from response header)
  → ELIF operator is human:
      → actual_cost = duration * resource.hourly_rate
  → ELIF operator is script:
      → actual_cost = node.cost_per_call (default 0)
  
  → accumulate in token.cost_usd
  → accumulate in flow.total_cost_usd
  → emit cost_usd in ledger event
```

---

## Requirements

### R1: LLM cost schema

Add cost configuration to LLM operator definitions:

```yaml
# Flow-level or global config
llm_costs:
  - model: "claude-sonnet-4"
    input_per_1k: 0.003    # USD per 1K input tokens
    output_per_1k: 0.015   # USD per 1K output tokens
  - model: "gpt-4o"
    input_per_1k: 0.005
    output_per_1k: 0.015
  - model: "default"       # Fallback
    input_per_1k: 0.001
    output_per_1k: 0.002
```

Node-level override:

```yaml
- id: risk_assessment
  t: task
  o: 
    op: llm
    model: "claude-sonnet-4"
    tier: 2
  cost:
    input_per_1k: 0.003
    output_per_1k: 0.015
```

### R2: LLM token estimation (simulation mode)

In simulation, LLM nodes don't actually call an LLM. Estimate tokens:

```yaml
- id: risk_assessment
  t: task
  o: { op: llm, tier: 2 }
  cost:
    est_tokens_in: 500     # Estimated input tokens
    est_tokens_out: 200    # Estimated output tokens
```

If not specified, use defaults:
- `est_tokens_in`: 500
- `est_tokens_out`: 200

Cost = `(est_tokens_in / 1000) * input_per_1k + (est_tokens_out / 1000) * output_per_1k`

### R3: HTTP node cost

```yaml
- id: credit_check
  t: task
  o: { op: http, url: "https://api.experian.com/check" }
  cost:
    per_call: 0.10   # USD per API call
```

Default: 0.0 if not specified.

### R4: Human operator cost

From resource definition:

```yaml
resources:
  - id: senior_reviewers
    capacity: 5
    cost:
      hourly_rate: 75.00  # USD per hour
```

Cost = `(node_duration / 3600) * hourly_rate`

For simulation, `node_duration` comes from the sampled duration.

### R5: Script node cost

```yaml
- id: run_validation
  t: task
  o: { op: script, cmd: "python validate.py" }
  cost:
    per_call: 0.001  # Compute cost estimate
```

Default: 0.0 if not specified.

### R6: Cost accumulation

Track costs at multiple levels:

| Level | Field | Description |
|-------|-------|-------------|
| Event | `cost_usd` | Cost of this specific event |
| Token | `token.cost_usd` | Cumulative cost for this work item |
| Flow | `flow.total_cost_usd` | Total cost across all tokens |
| Statistics | `stats.total_cost_usd` | Same as flow, accessible from stats |

### R7: Ledger emission

Emit `cost_usd` in every `node_completed` event:

```python
emit_event(
    event_type="node_completed",
    actor=f"node:{node_id}",
    target=f"token:{token_id}",
    payload_json=json.dumps({
        "node_id": node_id,
        "duration": duration,
        "operator": operator_type,
        # ... existing fields
    }),
    cost_tokens=int(sim_time),      # CLOCK (existing)
    cost_usd=node_cost,             # COIN (new)
    cost_carbon=carbon_estimate     # CARBON (existing heuristic)
)
```

### R8: Cost summary in statistics

Add to `StatisticsCollector`:

```python
stats.total_cost_usd          # Total USD spent
stats.mean_cost_per_token()   # Average cost per completed token
stats.cost_by_node()          # Dict of {node_id: total_cost}
stats.cost_by_operator_type() # Dict of {op_type: total_cost}
```

---

## Implementation Location

| File | Change |
|------|--------|
| `simdecisions/phase_ir/primitives.py` | Add `o` (operator) field to Node if not present — PRISM-IR spec defines this, implementation must match. Add `cost` block to Node. Add `hourly_rate` to Resource (alongside existing `cost_per_use`). |
| `simdecisions/des/core.py` | Compute cost in `handle_node_end()` based on `node.o.op` type |
| `simdecisions/des/statistics.py` | Add cost accumulators and summary methods |
| `simdecisions/des/ledger_adapter.py` | Pass computed `cost_usd` to emitter |
| `simdecisions/des/loader_v2.py` | Load `llm_costs` from flow config |

### Schema Notes

**Operator field (`o`):** PRISM-IR spec defines `o: { op: llm|human|http|script, tier: 0-4 }` on task nodes. If primitives.py Node dataclass lacks this field, add it. This is implementing the spec, not extending it.

**Resource cost fields:** 
- `cost_per_use` (existing, line 29) — fixed cost per acquire/release cycle
- `hourly_rate` (new) — duration-based cost for human operators

Both are valid. `cost_per_use` for transactional resources (API calls, permits). `hourly_rate` for time-based resources (humans, compute).

---

## Test Cases

### T1: LLM node cost

```yaml
llm_costs:
  - model: "default"
    input_per_1k: 0.001
    output_per_1k: 0.002

nodes:
  - id: analyze
    t: task
    o: { op: llm }
    cost:
      est_tokens_in: 1000
      est_tokens_out: 500
```

Expected cost: `(1000/1000)*0.001 + (500/1000)*0.002 = 0.001 + 0.001 = $0.002`

### T2: Human node cost (cost arithmetic only)

```yaml
resources:
  - id: reviewers
    capacity: 1
    cost:
      hourly_rate: 60.00

nodes:
  - id: review
    t: task
    resource: reviewers
    tm: { d: constant, value: 600 }  # 10 minutes
```

Expected cost: `(600/3600) * 60.00 = $10.00`

**Note:** Tests cost computation from sampled duration. Does not assert on resource acquire/release behavior (requires RESOURCE-BINDING-001).

### T3: HTTP node cost

```yaml
nodes:
  - id: api_call
    t: task
    o: { op: http }
    cost:
      per_call: 0.05
```

Expected cost: `$0.05`

### T4: Cost accumulation

Flow with 3 nodes (LLM + Human + HTTP), run 100 tokens:
- `stats.total_cost_usd` should equal sum of all node costs
- `stats.cost_by_node()` should break down by node
- Each token's `token.cost_usd` should equal sum of its node costs

### T5: Call center cost (cost arithmetic only)

Modify call center flow to add hourly rate:

```yaml
resources:
  - id: agents
    capacity: 500
    cost:
      hourly_rate: 25.00
```

After 1-hour sim with ~5000 calls, ~5 min avg handle:
- Total handle time ≈ 5000 * 5 min = 25000 min ≈ 417 hours
- Expected cost ≈ 417 * $25 = ~$10,400

**Note:** Tests cost accumulation from sampled durations. Does not assert on utilization or wait times (requires RESOURCE-BINDING-001).

---

## Acceptance Criteria

- [ ] LLM nodes compute cost from token estimates and model rates
- [ ] HTTP nodes compute cost from `per_call` config
- [ ] Human nodes compute cost from duration and `hourly_rate`
- [ ] Script nodes compute cost from `per_call` config (default 0)
- [ ] Costs accumulate at token and flow levels
- [ ] `cost_usd` emitted in ledger events (non-zero for costed nodes)
- [ ] `StatisticsCollector` provides cost summaries
- [ ] Existing tests still pass
- [ ] Call center sim shows realistic total cost

---

## Out of Scope

- **Actual LLM calls** — this is simulation mode; we estimate tokens, not call APIs
- **Dynamic pricing** — no time-of-day or volume discounts
- **Currency conversion** — USD only
- **CARBON computation** — separate spec (SPEC-DES-CARBON-001)

---

## Estimated Effort

3-4 hours. Schema additions, cost computation in node handler, stats accumulation.

---

## Notes

COIN is the second currency. With CLOCK (time) and COIN (money) working, the DES becomes useful for capacity planning and cost projection. CARBON (emissions) is P2 and more complex (requires external data or measurement).
