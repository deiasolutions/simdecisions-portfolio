# SPEC-DES-CURRENCY-002

**Title:** Per-transition cost aggregation  
**Priority:** P1  
**Status:** DRAFT  
**Date:** 2026-04-15  
**Author:** Q88N  
**Depends on:** SPEC-DES-CURRENCY-001 (node-level cost computation must exist first)

---

## Problem

CURRENCY-001 computes cost per node execution. But the DES engine doesn't aggregate costs:
- Per edge (how much does path A→B cost?)
- Per path (how much does the happy path cost vs. the escalation path?)
- Per run (total CLOCK/COIN/CARBON for one token's journey)

From the audit (2026-04-14):
> "gap_001: No per-transition cost aggregation"

Without this, you can't answer: "What does it cost when a loan gets escalated vs. auto-approved?"

---

## Solution

Track and aggregate costs at edge, path, and run levels.

### Data Model

```
Token carries:
  - cost_clock: float    # Cumulative sim_time spent
  - cost_coin: float     # Cumulative USD spent
  - cost_carbon: float   # Cumulative kg CO2e

Edge accumulates:
  - traversal_count: int
  - total_clock: float
  - total_coin: float
  - total_carbon: float

Path (start → end sequence):
  - path_signature: str  # Hash of node sequence
  - count: int
  - total_clock/coin/carbon: float
```

### Cost Flow

```
edge_traversed:
  → record edge in token.path_history
  → increment edge.traversal_count
  → accumulate token's current costs to edge totals

token_completed:
  → compute path_signature from token.path_history
  → accumulate token costs to path totals
  → emit run summary to ledger
```

---

## Requirements

### R1: Token-level cost accumulation

Each token tracks its cumulative costs:

```python
@dataclass
class Token:
    # ... existing fields
    cost_clock: float = 0.0   # Sim time spent in nodes
    cost_coin: float = 0.0    # USD spent
    cost_carbon: float = 0.0  # kg CO2e
    path_history: List[str] = field(default_factory=list)  # Node IDs visited
```

On `node_end`:
- Add node's duration to `token.cost_clock`
- Add node's cost_usd to `token.cost_coin`
- Add node's cost_carbon to `token.cost_carbon`

### R2: Edge-level aggregation

Track costs per edge:

```python
@dataclass
class EdgeStats:
    edge_id: str           # "source->target"
    traversal_count: int = 0
    total_clock: float = 0.0
    total_coin: float = 0.0
    total_carbon: float = 0.0
    
    def mean_clock(self) -> float:
        return self.total_clock / self.traversal_count if self.traversal_count else 0
    
    # Similarly for mean_coin, mean_carbon
```

On `edge_traversed`:
- Increment `edge.traversal_count`
- Add token's cost delta since last edge to edge totals

### R3: Path-level aggregation

Track costs per unique path through the flow:

```python
@dataclass
class PathStats:
    path_signature: str     # Hash or string of node sequence
    path_nodes: List[str]   # Ordered list of node IDs
    count: int = 0
    total_clock: float = 0.0
    total_coin: float = 0.0
    total_carbon: float = 0.0
```

On `token_completed`:
- Compute `path_signature` from `token.path_history`
- Find or create PathStats for this signature
- Increment count, add token's final costs

### R4: Trace events

Emit edge traversal with cost snapshot:

```python
emit_event(
    event_type="edge_traversed",
    actor=f"token:{token_id}",
    target=f"edge:{source}->{target}",
    payload_json=json.dumps({
        "source": source,
        "target": target,
        "token_cost_clock": token.cost_clock,
        "token_cost_coin": token.cost_coin,
        "token_cost_carbon": token.cost_carbon
    }),
    cost_tokens=int(sim_time),
    cost_usd=0,        # Edge itself has no cost; this is a snapshot
    cost_carbon=0
)
```

### R5: Run summary event

On token completion, emit summary:

```python
emit_event(
    event_type="run_completed",
    actor=f"token:{token_id}",
    target=f"flow:{flow_id}",
    payload_json=json.dumps({
        "path": token.path_history,
        "path_signature": compute_signature(token.path_history),
        "total_clock": token.cost_clock,
        "total_coin": token.cost_coin,
        "total_carbon": token.cost_carbon,
        "node_count": len(token.path_history),
        "outcome": outcome  # e.g., "approved", "rejected", "abandoned"
    }),
    cost_tokens=int(token.cost_clock),
    cost_usd=token.cost_coin,
    cost_carbon=token.cost_carbon
)
```

### R6: Statistics API

Add to `StatisticsCollector`:

```python
# Edge stats
stats.edge_stats()                    # Dict[edge_id, EdgeStats]
stats.edge_cost(edge_id)              # (clock, coin, carbon) tuple
stats.hottest_edges(n=10)             # Top N by traversal count
stats.most_expensive_edges(n=10)      # Top N by total_coin

# Path stats
stats.path_stats()                    # Dict[path_signature, PathStats]
stats.path_cost(signature)            # (clock, coin, carbon) tuple
stats.most_common_paths(n=10)         # Top N by count
stats.most_expensive_paths(n=10)      # Top N by mean_coin

# Comparative
stats.compare_paths(sig_a, sig_b)     # Returns cost deltas
```

---

## Implementation Location

| File | Change |
|------|--------|
| `simdecisions/des/tokens.py` | Add `cost_clock`, `cost_coin`, `cost_carbon`, `path_history` to Token |
| `simdecisions/des/statistics.py` | Add `EdgeStats`, `PathStats` dataclasses and aggregation methods |
| `simdecisions/des/core.py` | Accumulate to token on `node_end`, record edge on `edge_traversed`, emit `run_completed` |
| `simdecisions/des/trace_writer.py` | Add `edge_traversed`, `run_completed` event types |

---

## Test Cases

### T1: Single-path flow

```
start → task_a (cost $1) → task_b (cost $2) → end
```

Run 10 tokens:
- Each token: `cost_coin = $3`
- Edge `start→task_a`: 10 traversals, $0 (start has no cost)
- Edge `task_a→task_b`: 10 traversals, $10 total ($1 × 10)
- Edge `task_b→end`: 10 traversals, $30 total ($3 × 10)
- Path stats: 1 unique path, 10 count, $30 total

### T2: Branching flow

```
start → decision → [approved] → end_approved
                 → [rejected] → end_rejected
```

With costs: decision=$0.50, approved path adds $1, rejected path adds $0.25

Run 100 tokens (60 approved, 40 rejected):
- Path `start→decision→end_approved`: 60 count, mean $1.50
- Path `start→decision→end_rejected`: 40 count, mean $0.75
- `stats.compare_paths()` shows approved costs 2× rejected

### T3: Call center paths

Different paths: quick resolution vs. escalation vs. callback

After 1-hour sim:
- `stats.most_expensive_paths(5)` shows escalation path costs most
- `stats.most_common_paths(5)` shows quick resolution is dominant

---

## Acceptance Criteria

- [ ] Tokens accumulate CLOCK/COIN/CARBON as they traverse
- [ ] `token.path_history` records node sequence
- [ ] Edge stats track traversal counts and cost totals
- [ ] Path stats aggregate by unique node sequence
- [ ] `edge_traversed` events emitted with cost snapshot
- [ ] `run_completed` events emitted with full cost summary
- [ ] Statistics API provides edge/path queries
- [ ] Compare branching paths shows cost difference
- [ ] Existing tests still pass

---

## Out of Scope

- **Path visualization** — UI concern, not engine
- **Path prediction** — ML layer, not this spec
- **Real-time path monitoring** — production engine concern

---

## Estimated Effort

4-5 hours. Token changes are simple. Statistics aggregation is the bulk of work.

---

## Notes

This completes the cost observability story. With CURRENCY-001 (node costs) and CURRENCY-002 (aggregation), you can answer:
- "How much does the average loan approval cost?"
- "What's the cost difference between auto-approve and escalation?"
- "Which path is the bottleneck?"

These questions are the whole point of simulating before executing.
