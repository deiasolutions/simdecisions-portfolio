# SPEC-EVENT-LEDGER-GAMIFICATION: Event Shapes for Ledger + Gamification

## Priority
P2

## Depends On
ADR-001-Event-Ledger-Foundation

## Model Assignment
sonnet

## Objective

Define the immutable event shapes that feed both the Event Ledger and the gamification system. The ledger is the single source of truth — everything emits, everything is scorable. Capture first, score later. Events are immutable; scoring rules evolve.

## Files to Read First

- hivenode/ledger/schema.py
- hivenode/ledger/emitter.py
- hivenode/ledger/writer.py
- hivenode/ledger/reader.py
- hivenode/ledger/aggregation.py
- hivenode/routes/ledger_routes.py

## Acceptance Criteria

- [ ] Base event schema defined (event_id, kind, timestamp, actor, target, context, currencies, prev_hash, event_hash)
- [ ] Actor types enumerated: human, bee, system, queen
- [ ] Target types enumerated: task, page, notebook, egg, deploy, review, spec, session
- [ ] Task events emitting: CREATED, DISPATCHED, STARTED, COMPLETED, FAILED, APPROVED, REJECTED, NEEDS_HUMAN
- [ ] Wiki events emitting: PAGE_CREATED, PAGE_UPDATED, PAGE_DELETED, PAGE_VIEWED, PAGE_LINKED, PAGE_UNLINKED
- [ ] Notebook events emitting: OPENED, RUN, SAVED, EXPORTED, ERROR
- [ ] Egg events emitting: PACKED, VALIDATED, INFLATED, FAILED
- [ ] Review events emitting: STARTED, COMPLETED, BUG_CAUGHT, REQUESTED
- [ ] Deploy events emitting: STARTED, COMPLETED, FAILED, ROLLBACK_EXECUTED
- [ ] Spec events emitting: CREATED, UPDATED, APPROVED, SHIPPED
- [ ] Session events emitting: STARTED, ENDED, IDLE, RESUMED
- [ ] Search events emitting: EXECUTED, CLICKED
- [ ] Three Currencies (clock, coin, carbon) populated on every resource-consuming event
- [ ] Zero-cost events emit zeroes for all currencies
- [ ] Hash chaining implemented via SHA-256 with canonical JSON serialization
- [ ] emit_event() Python API functional with actor, target, context, currencies params
- [ ] emitEvent() TypeScript API functional with matching interface
- [ ] @track_event decorator pattern available for auto-instrumented functions
- [ ] Gamification consumer receives events via async event bus
- [ ] XP_MAP defined mapping event kinds to point values
- [ ] Badge triggers fire on event patterns (e.g., BUG_CAUGHT count >= 1)
- [ ] Streak detection works from event history
- [ ] Events append-only, hash chain verifiable
- [ ] Events queryable by kind, actor, target, time range
- [ ] Collection rules: all state changes, user actions, errors always collected; navigation sampled at 10%
- [ ] Privacy exclusions enforced: no keystrokes, mouse movements, clipboard, or draft content

## Smoke Test

- [ ] Emit a TASK_APPROVED event via Python API — confirm it appears in ledger with correct hash chain
- [ ] Emit a PAGE_CREATED event via TypeScript API — confirm currencies populated
- [ ] Query ledger by kind=TASK_APPROVED — confirm event returned
- [ ] Verify hash chain integrity on 10+ sequential events
- [ ] Trigger BUG_CAUGHT event — confirm badge check fires

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Event emission must not block main flow (fire-and-forget with retry queue)
- High-frequency events (NOTEBOOK_RUN) must support batched writes
- Retention: all events indefinite (compressed after 90 days), hash chain never deleted

---

## Architecture

```
Any ShiftCenter Action
        │
        ▼
   Event Emitter
   emit_event(kind, actor, target, context, currencies)
        │
        ▼
   Event Ledger (append-only, hash-chained, immutable)
        │
   ┌────┴────┐
   ▼         ▼
Gamification  Other Consumers
(XP, badges)  (audit, ML, surrogate training)
```

## Base Event Schema

```json
{
  "event_id": "uuid",
  "kind": "TASK_APPROVED",
  "timestamp": "2026-04-06T14:30:00.000Z",
  "actor": { "id": "uuid", "type": "human|bee|system|queen", "name": "Q88N" },
  "target": { "id": "uuid", "type": "task|page|notebook|egg|deploy|review|spec|session", "path": "MW-S01" },
  "context": { },
  "currencies": { "clock": 45000, "coin": 0.0023, "carbon": 0.00001 },
  "prev_hash": "sha256...",
  "event_hash": "sha256..."
}
```

## Event Kinds Summary

### Task Events
| Kind | Emitted When |
|------|--------------|
| `TASK_CREATED` | Task file written to backlog |
| `TASK_DISPATCHED` | Task moved to queue |
| `TASK_STARTED` | Bee begins work |
| `TASK_COMPLETED` | Bee finishes (success) |
| `TASK_FAILED` | Bee finishes (failure) |
| `TASK_APPROVED` | Human approves |
| `TASK_REJECTED` | Human rejects |
| `TASK_NEEDS_HUMAN` | Parked for review |

### Wiki Events
| Kind | Emitted When |
|------|--------------|
| `PAGE_CREATED` | New wiki page saved |
| `PAGE_UPDATED` | Existing page edited |
| `PAGE_DELETED` | Page soft-deleted |
| `PAGE_VIEWED` | Page opened for reading |
| `PAGE_LINKED` | New backlink created |
| `PAGE_UNLINKED` | Backlink removed |

### Notebook Events
| Kind | Emitted When |
|------|--------------|
| `NOTEBOOK_OPENED` | Notebook loaded |
| `NOTEBOOK_RUN` | Cell(s) executed |
| `NOTEBOOK_SAVED` | Notebook saved |
| `NOTEBOOK_EXPORTED` | Export generated |
| `NOTEBOOK_ERROR` | Execution error |

### Egg, Review, Deploy, Spec, Session, Search Events
See full event tables in original design doc. All follow the same base schema with kind-specific context fields.

## Three Currencies

Every resource-consuming event includes:

```json
"currencies": {
  "clock": 45000,     // milliseconds wall-clock
  "coin": 0.0023,     // USD cost
  "carbon": 0.00001   // kg CO2e
}
```

Sources: clock from `performance.now()` or timestamp diff, coin from token cost × rate, carbon from coin × cloud-region factor.

## Hash Chaining

```python
def compute_event_hash(event: dict, prev_hash: str) -> str:
    payload = json.dumps({
        "event_id": event["event_id"],
        "kind": event["kind"],
        "timestamp": event["timestamp"],
        "actor": event["actor"],
        "target": event["target"],
        "context": event["context"],
        "currencies": event["currencies"],
        "prev_hash": prev_hash
    }, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(payload.encode()).hexdigest()
```

## Gamification Integration

```python
XP_MAP = {
    "TASK_APPROVED": 10, "TASK_COMPLETED": 25, "TASK_DISPATCHED": 2,
    "PAGE_CREATED": 15, "PAGE_UPDATED": 5, "PAGE_LINKED": 5,
    "NOTEBOOK_RUN": 2, "NOTEBOOK_EXPORTED": 10,
    "EGG_PACKED": 25, "EGG_INFLATED": 5,
    "REVIEW_COMPLETED": 15, "BUG_CAUGHT": 50,
    "SPEC_CREATED": 30, "SPEC_SHIPPED": 100,
    "DEPLOY_COMPLETED": 20, "ROLLBACK_EXECUTED": 10,
}
```

Badge triggers and streak detection consume from the same event stream via async `EventConsumer` subscription.

## ML/Training Data

- RLHF gold: TASK_APPROVED/TASK_REJECTED pairs for preference learning
- Surrogate training: event sequences for outcome prediction
- Behavior modeling: session patterns for personalization

---

**Spec Version:** 1.0
**Author:** Q88N x Claude
