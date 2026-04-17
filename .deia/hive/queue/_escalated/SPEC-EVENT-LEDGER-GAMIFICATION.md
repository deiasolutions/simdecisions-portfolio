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

# Event Ledger Gamification Integration Specification

**Spec ID:** SPEC-EVENT-LEDGER-GAMIFICATION
**Created:** 2026-04-06
**Status:** DRAFT
**Depends On:** ADR-001-Event-Ledger-Foundation
**Ships With:** V1.0

---

## Executive Summary

This spec defines the **event shapes** that feed both the wiki system and gamification. The Event Ledger is the single source of truth. Everything emits. Everything is scorable.

### Core Principle

> **ABCDG: Always Be Collecting Data for Gamification.**
>
> Capture first, score later. Events are immutable. Scoring rules evolve.
> If you capture the event, you can score it later.
> If you don't capture it, it's gone.

---

## 1. Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Any ShiftCenter Action                          │
│  (task, wiki, notebook, review, deploy, search, navigation, etc.)       │
└─────────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           Event Emitter                                  │
│  emit_event(kind, actor, target, context, currencies)                   │
└─────────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          Event Ledger                                    │
│  Append-only. Hash-chained. Immutable.                                  │
│  Source of truth for all downstream consumers.                          │
└─────────────────────────────────────────────────────────────────────────┘
                │
        ┌───────┴───────┐
        ▼               ▼
┌───────────────┐ ┌───────────────┐
│ Gamification  │ │ Other         │
│ Consumer      │ │ Consumers     │
│               │ │ (audit, ML,   │
│ XP, badges,   │ │ surrogate     │
│ progression   │ │ training)     │
└───────────────┘ └───────────────┘
```

---

## 2. Event Schema

### 2.1 Base Event Structure

```json
{
  "event_id": "uuid",
  "kind": "TASK_APPROVED",
  "timestamp": "2026-04-06T14:30:00.000Z",
  
  "actor": {
    "id": "uuid",
    "type": "human|bee|system",
    "name": "Q88N"
  },
  
  "target": {
    "id": "uuid",
    "type": "task|page|notebook|egg|deploy",
    "path": "MW-S01"
  },
  
  "context": {
    // Event-specific details
  },
  
  "currencies": {
    "clock": 45000,        // milliseconds
    "coin": 0.0023,        // USD
    "carbon": 0.00001      // kg CO2e
  },
  
  "prev_hash": "sha256...",
  "event_hash": "sha256..."
}
```

### 2.2 Actor Types

| Type | Description |
|------|-------------|
| `human` | User action via UI or CLI |
| `bee` | LLM worker (BEE-001, etc.) |
| `system` | Automated process (scheduler, compiler) |
| `queen` | Orchestrator (Q33N, Q33NR) |

### 2.3 Target Types

| Type | Description | Example Path |
|------|-------------|--------------|
| `task` | Hive task | MW-S01 |
| `page` | Wiki page | architecture/event-ledger |
| `notebook` | Jupyter notebook | tutorials/getting-started.ipynb |
| `egg` | Packaged unit | feature.egg |
| `deploy` | Deployment | prod-2026-04-06-001 |
| `review` | Code review | PR-123 |
| `spec` | Specification | SPEC-WIKI-V1 |
| `session` | User session | session-uuid |

---

## 3. Event Kinds

### 3.1 Task Events

| Kind | Emitted When | Context Fields |
|------|--------------|----------------|
| `TASK_CREATED` | Task file written to backlog | `priority`, `estimated_hours`, `model` |
| `TASK_DISPATCHED` | Task moved to queue | `slot_number`, `bee_id` |
| `TASK_STARTED` | Bee begins work | `bee_id`, `start_time` |
| `TASK_COMPLETED` | Bee finishes (success) | `duration_ms`, `output_path` |
| `TASK_FAILED` | Bee finishes (failure) | `error_type`, `error_message` |
| `TASK_APPROVED` | Human approves | `review_time_ms`, `was_modified` |
| `TASK_REJECTED` | Human rejects | `rejection_reason`, `feedback` |
| `TASK_NEEDS_HUMAN` | Parked for review | `reason`, `blocking_issue` |

**Context Example:**

```json
{
  "kind": "TASK_APPROVED",
  "context": {
    "time_to_decision_ms": 45000,
    "was_modified": false,
    "rejection_count_prior": 0,
    "queue_position_at_approval": 3,
    "task_priority": "P1"
  }
}
```

### 3.2 Wiki Events

| Kind | Emitted When | Context Fields |
|------|--------------|----------------|
| `PAGE_CREATED` | New wiki page saved | `page_type`, `word_count`, `has_frontmatter` |
| `PAGE_UPDATED` | Existing page edited | `version`, `diff_size`, `sections_changed` |
| `PAGE_DELETED` | Page soft-deleted | `reason` |
| `PAGE_VIEWED` | Page opened for reading | `view_duration_ms`, `scroll_depth` |
| `PAGE_LINKED` | New backlink created | `source_page`, `link_text` |
| `PAGE_UNLINKED` | Backlink removed | `source_page` |

**Context Example:**

```json
{
  "kind": "PAGE_CREATED",
  "context": {
    "page_type": "adr",
    "word_count": 450,
    "has_frontmatter": true,
    "outbound_links": ["three-currencies", "process-13"],
    "tags": ["architecture", "decisions"]
  }
}
```

### 3.3 Notebook Events

| Kind | Emitted When | Context Fields |
|------|--------------|----------------|
| `NOTEBOOK_OPENED` | Notebook loaded | `cell_count`, `has_outputs` |
| `NOTEBOOK_RUN` | Cell(s) executed | `cells_run`, `execution_time_ms`, `runtime` |
| `NOTEBOOK_SAVED` | Notebook saved (no outputs) | `cells_modified` |
| `NOTEBOOK_EXPORTED` | Export generated | `export_format`, `file_size` |
| `NOTEBOOK_ERROR` | Execution error | `cell_index`, `error_type`, `traceback` |

**Context Example:**

```json
{
  "kind": "NOTEBOOK_RUN",
  "context": {
    "cells_run": 3,
    "execution_time_ms": 1250,
    "runtime": "pyodide",
    "outputs_generated": true,
    "errors": 0
  }
}
```

### 3.4 Egg Events

| Kind | Emitted When | Context Fields |
|------|--------------|----------------|
| `EGG_PACKED` | Egg created from directory | `file_count`, `total_size`, `notebook_count` |
| `EGG_VALIDATED` | Egg passed integrity check | `warnings` |
| `EGG_INFLATED` | Egg extracted | `files_extracted`, `target_path` |
| `EGG_FAILED` | Pack/inflate failed | `error_type`, `error_message` |

### 3.5 Review Events

| Kind | Emitted When | Context Fields |
|------|--------------|----------------|
| `REVIEW_STARTED` | Review begun | `artifact_type`, `artifact_id` |
| `REVIEW_COMPLETED` | Review finished | `verdict`, `comments_count`, `time_spent_ms` |
| `BUG_CAUGHT` | Bug found in review | `severity`, `bug_type`, `file_path` |
| `REVIEW_REQUESTED` | Review requested from another | `requested_from` |

### 3.6 Deploy Events

| Kind | Emitted When | Context Fields |
|------|--------------|----------------|
| `DEPLOY_STARTED` | Deploy initiated | `environment`, `version`, `commit_sha` |
| `DEPLOY_COMPLETED` | Deploy successful | `duration_ms`, `services_updated` |
| `DEPLOY_FAILED` | Deploy failed | `error_type`, `rollback_initiated` |
| `ROLLBACK_EXECUTED` | Rollback completed | `from_version`, `to_version`, `reason` |

### 3.7 Spec Events

| Kind | Emitted When | Context Fields |
|------|--------------|----------------|
| `SPEC_CREATED` | New spec written | `spec_id`, `word_count`, `sections` |
| `SPEC_UPDATED` | Spec revised | `version`, `sections_changed` |
| `SPEC_APPROVED` | Spec approved for build | `approver`, `time_to_approval_ms` |
| `SPEC_SHIPPED` | Spec fully deployed | `tasks_completed`, `total_duration_ms` |

### 3.8 Session Events

| Kind | Emitted When | Context Fields |
|------|--------------|----------------|
| `SESSION_STARTED` | User logs in | `device`, `location` |
| `SESSION_ENDED` | User logs out / timeout | `duration_ms`, `actions_count` |
| `SESSION_IDLE` | No activity for 5min | `idle_start` |
| `SESSION_RESUMED` | Activity after idle | `idle_duration_ms` |

### 3.9 Search Events

| Kind | Emitted When | Context Fields |
|------|--------------|----------------|
| `SEARCH_EXECUTED` | Search performed | `query`, `result_count`, `time_ms` |
| `SEARCH_CLICKED` | Result clicked | `result_position`, `result_type` |

---

## 4. Three Currencies

Every event that consumes resources must include currency data:

```json
"currencies": {
  "clock": 45000,        // milliseconds of wall-clock time
  "coin": 0.0023,        // USD cost (LLM tokens, compute, etc.)
  "carbon": 0.00001      // kg CO2e (estimated)
}
```

### 4.1 Currency Sources

| Currency | Source | Notes |
|----------|--------|-------|
| `clock` | `performance.now()` or timestamp diff | Always measurable |
| `coin` | Token cost × rate | From LLM provider pricing |
| `carbon` | Coin × carbon factor | Estimated from cloud region |

### 4.2 Zero-Cost Events

Events with no resource consumption emit zeroes:

```json
"currencies": {
  "clock": 0,
  "coin": 0,
  "carbon": 0
}
```

---

## 5. Hash Chaining

Events are hash-chained for tamper detection:

```python
def compute_event_hash(event: dict, prev_hash: str) -> str:
    # Canonical JSON serialization
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

---

## 6. Emission API

### 6.1 Python

```python
from shiftcenter.ledger import emit_event

emit_event(
    kind="TASK_APPROVED",
    actor_id=current_user.id,
    actor_type="human",
    target_id=task.id,
    target_type="task",
    target_path=task.path,
    context={
        "time_to_decision_ms": 45000,
        "was_modified": False
    },
    currencies={
        "clock": 45000,
        "coin": 0,
        "carbon": 0
    }
)
```

### 6.2 TypeScript

```typescript
import { emitEvent } from '@shiftcenter/ledger';

emitEvent({
  kind: 'PAGE_CREATED',
  actorId: currentUser.id,
  actorType: 'human',
  targetId: page.id,
  targetType: 'page',
  targetPath: page.path,
  context: {
    page_type: 'adr',
    word_count: 450
  },
  currencies: {
    clock: 1200,
    coin: 0,
    carbon: 0
  }
});
```

### 6.3 Decorator Pattern

```python
from shiftcenter.ledger import track_event

@track_event("NOTEBOOK_RUN")
async def run_notebook_cell(notebook_id: str, cell_index: int):
    # Function execution is automatically tracked
    # Currencies measured from start to end
    result = await execute_cell(notebook_id, cell_index)
    return result
```

---

## 7. Collection Rules

### 7.1 What to Collect

| Category | Collect | Why |
|----------|---------|-----|
| All state changes | ✓ Always | Core audit trail |
| All user actions | ✓ Always | Gamification source |
| View/read events | ✓ With context | Engagement metrics |
| Search queries | ✓ Always | Improve search, ML training |
| Errors/failures | ✓ Always | Debugging, improvement |
| Performance metrics | ✓ Always | Optimization data |
| Navigation | ○ Sample | Can be noisy; 10% sample OK |

### 7.2 What NOT to Collect

| Category | Reason |
|----------|--------|
| Keystrokes | Privacy, noise |
| Mouse movements | Privacy, storage cost |
| Clipboard contents | Privacy |
| Draft content before save | Privacy, noise |

### 7.3 Retention Policy

| Event Category | Retention |
|----------------|-----------|
| All events | Indefinite (compressed after 90 days) |
| Hash chain | Indefinite (never delete) |
| Raw context | 1 year (then summarize) |

---

## 8. Gamification Integration

### 8.1 Scorable Events

Every event kind maps to a potential XP source:

```python
XP_MAP = {
    # Tasks
    "TASK_APPROVED": 10,
    "TASK_REJECTED": 5,
    "TASK_COMPLETED": 25,
    "TASK_DISPATCHED": 2,
    
    # Wiki
    "PAGE_CREATED": 15,
    "PAGE_UPDATED": 5,
    "PAGE_LINKED": 5,
    
    # Notebooks
    "NOTEBOOK_RUN": 2,
    "NOTEBOOK_EXPORTED": 10,
    
    # Eggs
    "EGG_PACKED": 25,
    "EGG_INFLATED": 5,
    
    # Reviews
    "REVIEW_COMPLETED": 15,
    "BUG_CAUGHT": 50,
    
    # Specs
    "SPEC_CREATED": 30,
    "SPEC_SHIPPED": 100,
    
    # Deploys
    "DEPLOY_COMPLETED": 20,
    "ROLLBACK_EXECUTED": 10,
}
```

### 8.2 Badge Triggers

Events feed badge detection:

```python
# Example: Check for "Bug Hunter" badge
def check_bug_hunter(user_id: str) -> bool:
    count = ledger.count_events(
        actor_id=user_id,
        kind="BUG_CAUGHT"
    )
    return count >= 1
```

### 8.3 Streak Detection

```python
# Check if user has activity today
def has_activity_today(user_id: str) -> bool:
    today = date.today()
    return ledger.has_events(
        actor_id=user_id,
        since=datetime.combine(today, time.min),
        kinds=SCORABLE_EVENTS
    )
```

---

## 9. ML/Training Data

### 9.1 RLHF Gold

Task approval/rejection pairs:

```python
# Extract preference pairs
approved = ledger.get_events(kind="TASK_APPROVED")
rejected = ledger.get_events(kind="TASK_REJECTED")

# Each pair: (task_output, approved=True/False, feedback)
# Gold for RLHF fine-tuning
```

### 9.2 Surrogate Training

Event sequences for prediction:

```python
# Predict: will this task be approved?
features = extract_features(task)
label = ledger.get_outcome(task_id)  # APPROVED or REJECTED
```

### 9.3 Behavior Modeling

Session patterns for personalization:

```python
# User engagement patterns
sessions = ledger.get_events(
    actor_id=user_id,
    kinds=["SESSION_*", "PAGE_VIEWED", "SEARCH_*"]
)
# → Time-of-day preferences, topic interests, etc.
```

---

## 10. Event Consumer Interface

### 10.1 Subscription

```python
class GamificationConsumer(EventConsumer):
    
    SUBSCRIBED_KINDS = [
        "TASK_*",
        "PAGE_*", 
        "NOTEBOOK_*",
        "EGG_*",
        "REVIEW_*",
        "SPEC_*",
        "DEPLOY_*"
    ]
    
    async def on_event(self, event: LedgerEvent):
        xp = self.calculate_xp(event)
        await self.update_progression(event.actor.id, xp)
        await self.check_badges(event.actor.id, event)
```

### 10.2 Replay

```python
# Recalculate all XP from scratch
async def replay_all():
    async for event in ledger.stream_all():
        await gamification.process_event(event)
```

---

## 11. Acceptance Criteria

### 11.1 Event Emission

- [ ] All task operations emit events
- [ ] All wiki operations emit events
- [ ] All notebook operations emit events
- [ ] All egg operations emit events
- [ ] Events include full context
- [ ] Three Currencies populated where applicable

### 11.2 Event Structure

- [ ] Events conform to base schema
- [ ] Actor and target correctly populated
- [ ] Timestamps in ISO 8601 UTC
- [ ] Hash chain maintained

### 11.3 Gamification Integration

- [ ] Gamification consumer receives events
- [ ] XP calculated from events
- [ ] Badge triggers fire on event patterns
- [ ] Streak detection works from event history

### 11.4 Storage

- [ ] Events append-only
- [ ] Hash chain verifiable
- [ ] Events queryable by kind, actor, target, time range

---

## 12. Implementation Notes

### 12.1 Event Bus

Use async event bus for decoupling:

```python
# Emit
await event_bus.publish("ledger.event", event)

# Subscribe
@event_bus.subscribe("ledger.event")
async def handle_event(event):
    await gamification.process(event)
```

### 12.2 Batching

For high-frequency events (NOTEBOOK_RUN), batch writes:

```python
# Buffer events, flush every 100ms or 10 events
event_buffer.add(event)
if event_buffer.should_flush():
    await ledger.write_batch(event_buffer.drain())
```

### 12.3 Error Handling

Event emission must not block main flow:

```python
try:
    await emit_event(...)
except LedgerError:
    # Log, don't crash
    logger.error("Event emission failed", exc_info=True)
    # Queue for retry
    retry_queue.add(event)
```

---

**Spec Version:** 1.0
**Author:** Q88N × Claude
**Review Required:** Integration with existing ADR-001 Event Ledger

## Triage History
- 2026-04-12T18:52:40.073856Z — requeued (empty output)
- 2026-04-12T18:57:40.127934Z — requeued (empty output)
- 2026-04-12T19:02:40.215667Z — requeued (empty output)
