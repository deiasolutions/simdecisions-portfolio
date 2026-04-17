# SPEC-DES-RESOURCE-BINDING-001

**Title:** Wire node.resource to automatic acquire/release  
**Priority:** P0 (blocker)  
**Status:** READY
**Date:** 2026-04-15  
**Author:** Q88N  
**Validated by:** Call center simulation failure (2026-04-15)

---

## Problem

The DES engine has resource primitives:
- `ResourceManager` with capacity tracking
- 6 queue disciplines (FIFO, LIFO, priority, SJF, EDF, WFQ)
- 4 preemption modes (none, resume, restart, abort)
- `acquire()` and `release()` methods
- Tests proving the resource system works in isolation

But **node execution ignores the `resource` field**. When a node specifies `resource: agents`, the engine:
- Does NOT acquire before processing
- Does NOT queue tokens when capacity exhausted
- Does NOT release after processing
- Does NOT emit resource events to the trace

Result: every token gets instant service. No queueing. No wait time. No capacity-constrained simulation. The call center test proved this — 500 agents, 5000 calls/hour, and utilization was 0%.

---

## Solution

Wire the resource lifecycle into the node processing pipeline.

### Execution Flow (current)

```
token arrives at node
  → schedule node_start event
  → sample duration
  → schedule node_end event
  → emit to next edge
```

### Execution Flow (target)

```
token arrives at node
  → IF node.resource is set:
      → emit resource_requested event
      → call ResourceManager.acquire(resource_id, token)
      → IF capacity available:
          → emit resource_acquired event
          → proceed to node_start
      → ELSE:
          → token state = waiting_resource
          → add to resource queue (per queue discipline)
          → RETURN (do not schedule node_start)
  → ELSE:
      → proceed to node_start (no resource needed)

node_start:
  → emit node_started event
  → sample duration
  → schedule node_end event

node_end:
  → emit node_completed event
  → IF node.resource is set:
      → call ResourceManager.release(resource_id, token)
      → emit resource_released event
      → check resource queue for waiting tokens
      → IF waiting tokens:
          → acquire for next token (per queue discipline)
          → emit resource_acquired event
          → schedule that token's node_start
  → emit to next edge
```

---

## Requirements

### R0: Load flow-level resources into ResourceManager

`load_flow_v2()` in `simdecisions/des/loader_v2.py` currently ignores top-level `flow.resources[]`. Add resource loading so the ResourceManager is populated before simulation runs.

For each entry in `flow.get("resources", [])`:

0.1. Call `ResourceManager.register(resource_id, capacity, discipline)` where:
   - `resource_id` = entry `id`
   - `capacity` = entry `capacity` (default 1)
   - `discipline` = entry `dispatch.mode` mapped to ResourceManager discipline names (e.g. `"fifo"` → `"FIFO"`)

0.2. Store the ResourceManager on `state` so `handle_token_arrive` and `handle_node_end` can access it (same pattern as `state._generators`).

0.3. Also check `flow.metadata.resources` as a fallback (same pattern used for generators/pools).

**API reference** (already implemented in `simdecisions/des/resources.py`):
```python
ResourceManager.register(resource_id: str, capacity: int = 1, discipline: str = "FIFO", preemptive: bool = False, preempt_mode: str = "non_preemptive")
ResourceManager.acquire(resource_id: str, token_id: str, quantity: int = 1, priority: int = 0) -> bool
ResourceManager.release(resource_id: str, token_id: str, quantity: int | None = None)
ResourceManager.enqueue(resource_id: str, request: QueuedRequest)
ResourceManager.dequeue_next(resource_id: str) -> QueuedRequest | None
```

`QueuedRequest` dataclass fields: `token_id, quantity, priority, arrival_time, deadline, expected_service, weight`

### R1: Auto-acquire on node entry

When a token arrives at a node with `resource` field set:

1.1. Emit `resource_requested` trace event with `{node_id, token_id, resource_id, sim_time}`

1.2. Call `ResourceManager.acquire(resource_id, token_id, priority)`
   - Priority derived from `token.properties` or `entity` attributes per resource config

1.3. If capacity available:
   - Decrement available capacity
   - Emit `resource_acquired` trace event with `{node_id, token_id, resource_id, sim_time, wait_time=0}`
   - Proceed to node execution

1.4. If capacity exhausted:
   - Set `token.state = "waiting_resource"`
   - Add token to resource queue (respecting `dispatch.mode`)
   - Do NOT schedule `node_start` — token waits

### R2: Auto-release on node completion

When a node with `resource` field completes:

2.1. Call `ResourceManager.release(resource_id, token_id)`
   - Increment available capacity

2.2. Emit `resource_released` trace event with `{node_id, token_id, resource_id, sim_time, hold_time}`

2.3. Check resource queue for waiting tokens

2.4. If queue non-empty:
   - Dequeue next token (per queue discipline)
   - Acquire resource for that token
   - Emit `resource_acquired` event with `wait_time = sim_time - requested_time`
   - Schedule `node_start` for that token

### R3: Queue discipline support

Resource `dispatch.mode` determines dequeue order:

| Mode | Behavior |
|------|----------|
| `fifo` | First-in, first-out (default) |
| `lifo` | Last-in, first-out |
| `priority` | Highest priority first (from `priority_expr`) |
| `sjf` | Shortest job first (from node duration estimate) |
| `edf` | Earliest deadline first (from `entity.deadline`) |
| `wfq` | Weighted fair queueing |

### R4: Trace events

Emit these events to the trace (ADR-001 compliant):

| Event Type | When | Payload |
|------------|------|---------|
| `resource_requested` | Token needs resource | `{resource_id, token_id, node_id, sim_time}` |
| `resource_acquired` | Token gets resource | `{resource_id, token_id, node_id, sim_time, wait_time}` |
| `resource_released` | Token releases resource | `{resource_id, token_id, node_id, sim_time, hold_time}` |

These events enable:
- Wait time calculation: `acquired.sim_time - requested.sim_time`
- Hold time calculation: `released.sim_time - acquired.sim_time`
- Service level: `count(wait_time <= SLA) / count(acquired)`
- Utilization: `sum(hold_time) / (sim_duration * capacity)`

### R5 & R6: OUT OF SCOPE

R5 (multi-unit acquire) and R6 (preemption) are deferred to a future spec. This spec delivers R0–R4 only: resource loading, acquire/queue/release, and trace events.

---

## Implementation Location

Based on audit:

| File | Change |
|------|--------|
| `simdecisions/des/loader_v2.py` | **R0:** Load `flow.resources[]` into ResourceManager, store on `state` |
| `simdecisions/des/core.py` | **R1:** Modify `handle_token_arrive()` to check `node.resource` and call acquire/enqueue |
| `simdecisions/des/core.py` | **R2:** Modify `handle_node_end()` to call release, dequeue, and schedule waiting tokens |
| `simdecisions/des/resources.py` | Already has `acquire()`, `release()`, queue logic — wire it up |
| `simdecisions/des/trace_writer.py` | **R4:** Add `resource_requested`, `resource_acquired`, `resource_released` event types |
| `simdecisions/des/tokens.py` | Token state `waiting_resource` already exists — use it |

---

## Test Cases

### T1: Basic acquire/release

```yaml
resources:
  - id: agents
    capacity: 1

nodes:
  - id: work
    t: task
    resource: agents
    tm: { d: constant, value: 10 }
```

- Send 1 token → completes at t=10
- Agent utilization = 100% during [0, 10]

### T2: Queueing

Same flow, send 2 tokens at t=0:
- Token 1: acquired at t=0, completes at t=10
- Token 2: waits [0, 10], acquired at t=10, completes at t=20
- Token 2 wait_time = 10

### T3: FIFO vs Priority

```yaml
resources:
  - id: agents
    capacity: 1
    dispatch:
      mode: priority
      priority_expr: "entity.priority"
```

Send 3 tokens at t=0 with priorities [1, 3, 2]:
- Token with priority=3 served first after initial token completes

### T4: Call center scenario

500 agents, 5000 calls/hour, 5 min handle time, 1 hour run:
- Utilization > 0%
- Wait times measurable
- Service level computable

---

## Acceptance Criteria

- [ ] **R0:** `flow.resources[]` loaded into ResourceManager during `load_flow_v2()`
- [ ] **R1:** Nodes with `resource` field auto-acquire before `node_start`
- [ ] **R1:** Tokens queue when capacity exhausted (state = `waiting_resource`)
- [ ] **R2:** Resources auto-release after `node_end`
- [ ] **R2:** Queued tokens wake up when resource freed (dequeue → acquire → schedule node_start)
- [ ] **R4:** `resource_requested`, `resource_acquired`, `resource_released` trace events emitted
- [ ] **R4:** Wait time computable from trace (`acquired.sim_time - requested.sim_time`)
- [ ] **R3:** All 6 queue disciplines work (FIFO at minimum; others via existing ResourceManager)
- [ ] **T4:** Call center simulation (`call_center_500.prism.md` + `run_call_center.py`) shows non-zero utilization and measurable service level
- [ ] Existing 888 DES tests still pass (`python -m pytest tests/simdecisions/des/ -v`)

---

## Dependencies

None. ResourceManager and queue disciplines already implemented and tested. This spec wires them into the execution pipeline.

**Validation files (already in repo root):**
- `call_center_500.prism.md` — 500-agent call center flow
- `run_call_center.py` — runner script (translates prism format, runs sim, reports SLA)

The bee should use these as the end-to-end smoke test after wiring is complete.

---

## Estimated Effort

4-6 hours. The primitives exist; this is plumbing.

---

## Notes

This is the P0 blocker. Without resource binding, the DES engine cannot simulate any capacity-constrained process: call centers, manufacturing lines, healthcare staffing, checkout queues, API rate limits, etc. The entire value proposition of "simulate before you execute" depends on this.
