# SPEC-DES-BATCH-001

**Title:** Implement batch and separate node executors  
**Priority:** P2  
**Status:** DRAFT  
**Date:** 2026-04-15  
**Author:** Q88N  
**Depends on:** SPEC-DES-RESOURCE-BINDING-001 (batch nodes often use resources)

---

## Problem

PRISM-IR defines `batch` and `separate` node types for grouping and ungrouping tokens:
- **batch:** Collect N tokens, process as a group, emit one combined token
- **separate:** Take a batch token, emit N individual tokens

The node types are in the schema. But from the audit (2026-04-14):
> "gap_005: batch/separate nodes incomplete (no executors)"

The engine has no `handle_batch` or `handle_separate` in core.py. Tokens hitting these nodes get stuck or error.

---

## Use Cases

1. **Batch API calls:** Collect 100 requests, send one batch API call, fan results back out
2. **Batch review:** Collect similar items for a human to review together
3. **Bulk processing:** Accumulate orders, process in one database transaction
4. **Report generation:** Collect data points, generate one summary report

---

## Solution

Implement batch/separate executors with configurable collection rules.

### Batch Behavior

```
tokens arrive at batch node
  → add to batch buffer
  → IF batch_ready (size OR timeout OR condition):
      → create batch_token with collected entities
      → execute node (if has operator)
      → emit batch_token to outbound edge
      → clear buffer
  → ELSE:
      → token state = waiting_batch
      → RETURN (wait for more)
```

### Separate Behavior

```
batch_token arrives at separate node
  → extract individual entities from batch
  → create N individual tokens
  → emit each to outbound edge
```

---

## Requirements

### R1: Batch node schema

```yaml
- id: batch_requests
  t: batch
  batch:
    size: 100              # Emit when N tokens collected
    timeout: 60            # OR emit after N seconds (sim time)
    condition: null        # OR emit when expression true
    mode: all              # all | any (which trigger fires)
  o: { op: http }          # Optional: process the batch
  tm: { d: constant, value: 5 }
```

**Trigger modes:**
- `size` only: Wait until exactly N tokens
- `timeout` only: Wait until timeout, emit whatever collected
- `size + timeout`: Whichever comes first
- `condition`: Custom expression (e.g., `batch.total_value > 10000`)

### R2: Batch buffer

Track pending tokens per batch node:

```python
@dataclass
class BatchBuffer:
    node_id: str
    tokens: List[Token] = field(default_factory=list)
    first_arrival: float = None  # Sim time of first token
    
    def add(self, token: Token, sim_time: float):
        if self.first_arrival is None:
            self.first_arrival = sim_time
        self.tokens.append(token)
    
    def is_ready(self, config: BatchConfig, sim_time: float) -> bool:
        if config.size and len(self.tokens) >= config.size:
            return True
        if config.timeout and (sim_time - self.first_arrival) >= config.timeout:
            return True
        if config.condition and evaluate(config.condition, self.tokens):
            return True
        return False
    
    def flush(self) -> List[Token]:
        tokens = self.tokens
        self.tokens = []
        self.first_arrival = None
        return tokens
```

### R3: Batch token creation

When batch fires, create a combined token:

```python
def create_batch_token(tokens: List[Token], node_id: str) -> Token:
    return Token(
        id=generate_id(),
        entity={
            "type": "batch",
            "items": [t.entity for t in tokens],
            "count": len(tokens),
            "source_tokens": [t.id for t in tokens]
        },
        properties={
            "is_batch": True,
            "batch_size": len(tokens),
            "batch_node": node_id
        },
        state="created"
    )
```

### R4: Timeout scheduling

When first token arrives at batch node:

```python
def handle_batch_arrival(token, node, sim_time):
    buffer = get_or_create_buffer(node.id)
    
    if buffer.first_arrival is None and node.batch.timeout:
        # Schedule timeout event
        schedule_event(Event(
            time=sim_time + node.batch.timeout,
            event_type="batch_timeout",
            node_id=node.id
        ))
    
    buffer.add(token, sim_time)
    token.state = "waiting_batch"
    
    if buffer.is_ready(node.batch, sim_time):
        fire_batch(node, buffer, sim_time)
```

### R5: Separate node schema

```yaml
- id: fan_out_results
  t: separate
  separate:
    source: entity.items    # Path to array to split
    preserve_batch: false   # Keep batch token alive after split?
```

### R6: Separate executor

```python
def handle_separate(batch_token, node, sim_time):
    items = resolve_path(batch_token.entity, node.separate.source)
    
    for i, item in enumerate(items):
        new_token = Token(
            id=generate_id(),
            entity=item,
            properties={
                "from_batch": batch_token.id,
                "batch_index": i
            },
            state="created"
        )
        emit_to_outbound_edges(new_token, node, sim_time)
    
    if not node.separate.preserve_batch:
        batch_token.state = "completed"
```

### R7: Trace events

```python
# When token joins batch
emit_event(
    event_type="batch_token_added",
    payload={"node_id": node_id, "token_id": token_id, "buffer_size": len(buffer)}
)

# When batch fires
emit_event(
    event_type="batch_fired",
    payload={"node_id": node_id, "batch_size": count, "trigger": "size|timeout|condition"}
)

# When batch separated
emit_event(
    event_type="batch_separated",
    payload={"node_id": node_id, "batch_token_id": batch_id, "output_count": count}
)
```

### R8: Statistics

Add to `StatisticsCollector`:

```python
stats.batch_stats(node_id)  # Returns BatchNodeStats
# - batches_fired: int
# - avg_batch_size: float
# - avg_wait_time: float (time in buffer)
# - timeout_fires: int (how many fired by timeout vs size)
```

---

## Implementation Location

| File | Change |
|------|--------|
| `simdecisions/des/core.py` | Add `handle_batch_arrival()`, `handle_batch_timeout()`, `handle_separate()` |
| `simdecisions/des/tokens.py` | Add `waiting_batch` state handling, batch buffer management |
| `simdecisions/des/statistics.py` | Add `BatchNodeStats` |
| `simdecisions/des/trace_writer.py` | Add batch event types |
| `simdecisions/phase_ir/primitives.py` | Verify `batch` and `separate` node configs in schema |

---

## Test Cases

### T1: Size-triggered batch

```yaml
- id: batch_5
  t: batch
  batch:
    size: 5
```

Send 12 tokens at t=0:
- Batch 1 fires at t=0 with tokens 1-5
- Batch 2 fires at t=0 with tokens 6-10
- Tokens 11-12 remain in buffer (waiting_batch)

### T2: Timeout-triggered batch

```yaml
- id: batch_timeout
  t: batch
  batch:
    timeout: 10
```

Send 3 tokens at t=0:
- No immediate fire
- At t=10: batch fires with 3 tokens

### T3: Size or timeout

```yaml
- id: batch_either
  t: batch
  batch:
    size: 10
    timeout: 5
```

Send 3 tokens at t=0, then 3 more at t=3:
- At t=5: timeout fires batch with 6 tokens (timeout before size reached)

Send 15 tokens at t=0:
- At t=0: batch fires with 10 tokens (size reached)
- At t=5: timeout fires with remaining 5 tokens

### T4: Separate node

```yaml
- id: split
  t: separate
  separate:
    source: entity.items
```

Batch token with `entity.items = [a, b, c]`:
- Emits 3 tokens with entities a, b, c
- Each has `properties.from_batch` set

### T5: Batch + process + separate round-trip

```yaml
nodes:
  - id: collect
    t: batch
    batch: { size: 10 }
  
  - id: bulk_api
    t: task
    o: { op: http }
    tm: { d: constant, value: 1 }
  
  - id: fan_out
    t: separate
    separate: { source: entity.items }

edges:
  - { s: collect, t: bulk_api }
  - { s: bulk_api, t: fan_out }
```

Send 30 tokens:
- 3 batches of 10 created
- Each batch processed by bulk_api
- Each batch separated back to 10 tokens
- 30 tokens complete at end

---

## Acceptance Criteria

- [ ] `t: batch` nodes collect tokens until trigger fires
- [ ] Size trigger fires when count reached
- [ ] Timeout trigger fires after duration (sim time)
- [ ] Combined batch token created with collected entities
- [ ] `t: separate` nodes split batch back to individual tokens
- [ ] Batch events emitted to trace
- [ ] Statistics track batch metrics
- [ ] Tokens in buffer have state `waiting_batch`
- [ ] Existing tests still pass

---

## Out of Scope

- **Partial batch processing** — process some items, keep others (future)
- **Batch routing** — different batches to different paths (use decision node after batch)
- **Nested batches** — batch of batches (not supported)

---

## Estimated Effort

5-6 hours. Buffer management, timeout scheduling, and separate logic are the bulk.

---

## Notes

Batch/separate enables efficient bulk operations. Without it, you can't simulate:
- Batch API calls (common in integrations)
- Human batch review (reviewer sees 10 items at once)
- Database bulk inserts
- Report aggregation

Common pattern: `batch → process → separate` as a subflow.
