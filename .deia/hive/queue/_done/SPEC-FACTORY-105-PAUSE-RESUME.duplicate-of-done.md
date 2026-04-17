## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

# SPEC-FACTORY-105: Pause/Resume Queue & Task Reassignment

**MODE: EXECUTE**

**Spec ID:** SPEC-FACTORY-105
**Created:** 2026-04-09
**Author:** Q88N
**Type:** FEATURE
**Status:** READY
**Phase:** P1

---

## Priority
P1

## Depends On
- SPEC-FACTORY-002 (queue-pane registered)
- SPEC-FACTORY-006 (backend routes)

## Model Assignment
sonnet

## Purpose

Add queue control actions: pause/resume the queue runner, and reassign a task to a different model. Essential for mobile factory management when something goes wrong.

**Deliverable:** Queue controls + reassign action (~120 lines)

---

## Features

### 1. Pause/Resume Queue

Stop dispatching new tasks without killing active bees. Resume when ready.

**States:**
- `running` — queue runner actively dispatching
- `paused` — no new dispatches, active tasks continue
- `stopped` — runner not running (error or manual kill)

### 2. Reassign Task

Move a queued or failed task to a different model:
- Haiku task failing? Reassign to Sonnet.
- Complex task assigned wrong? Fix it.

---

## UI Changes

### Queue Header Controls

```
┌─────────────────────────────────┐
│ Queue              [⏸️] [↻]    │  ← pause, refresh
│ ──────────────────────────────  │
│ 2 active · 5 queued · 1 blocked │
└─────────────────────────────────┘
```

When paused:
```
┌─────────────────────────────────┐
│ Queue (PAUSED)     [▶️] [↻]    │  ← resume, refresh
│ ──────────────────────────────  │
│ 2 active · 5 queued · 1 blocked │
└─────────────────────────────────┘
```

### Task Long-Press Menu

Long-press a task card to show actions:

```
┌─────────────────────────┐
│ TASK-127               │
├─────────────────────────┤
│ ⟳  Reassign to Haiku   │
│ ⟳  Reassign to Sonnet  │
│ ⟳  Reassign to Opus    │
├─────────────────────────┤
│ 🗑️ Cancel Task         │
│ ⬆️ Bump Priority        │
└─────────────────────────┘
```

---

## API Endpoints

### POST /factory/queue/pause

Pause the queue runner.

**Response:**
```json
{
  "success": true,
  "state": "paused",
  "activeCount": 2,
  "message": "Queue paused. 2 active tasks will complete."
}
```

### POST /factory/queue/resume

Resume the queue runner.

**Response:**
```json
{
  "success": true,
  "state": "running",
  "queuedCount": 5
}
```

### GET /factory/queue/state

Get current queue state.

**Response:**
```json
{
  "state": "running",
  "activeCount": 2,
  "queuedCount": 5,
  "blockedCount": 1,
  "lastDispatch": "2026-04-09T12:35:00Z"
}
```

### POST /factory/task/{taskId}/reassign

Reassign a task to a different model.

**Request:**
```json
{
  "model": "sonnet"
}
```

**Response:**
```json
{
  "success": true,
  "taskId": "TASK-127",
  "previousModel": "haiku",
  "newModel": "sonnet",
  "status": "queued"
}
```

---

## Frontend Implementation

### Queue Controls

```typescript
// browser/src/primitives/queue-pane/QueueControls.tsx

import { Pause, Play, RefreshCw } from 'lucide-react';
import { useQueueStore } from './queueStore';

export function QueueControls() {
  const { state, pause, resume, refresh, loading } = useQueueStore();
  
  return (
    <div className="hhp-queue-controls">
      {state === 'running' ? (
        <button onClick={pause} aria-label="Pause queue">
          <Pause size={18} />
        </button>
      ) : (
        <button onClick={resume} aria-label="Resume queue">
          <Play size={18} />
        </button>
      )}
      <button onClick={refresh} disabled={loading} aria-label="Refresh">
        <RefreshCw size={18} className={loading ? 'spin' : ''} />
      </button>
    </div>
  );
}
```

### Task Context Menu

```typescript
// browser/src/primitives/queue-pane/TaskContextMenu.tsx

interface TaskContextMenuProps {
  task: QueueItem;
  onClose: () => void;
  position: { x: number; y: number };
}

export function TaskContextMenu({ task, onClose, position }: TaskContextMenuProps) {
  const { reassignTask, cancelTask, bumpPriority } = useQueueStore();
  
  const handleReassign = async (model: string) => {
    await reassignTask(task.id, model);
    onClose();
  };
  
  return (
    <div 
      className="hhp-context-menu"
      style={{ top: position.y, left: position.x }}
    >
      <div className="hhp-context-menu-section">
        <button onClick={() => handleReassign('haiku')}>
          ⟳ Reassign to Haiku
        </button>
        <button onClick={() => handleReassign('sonnet')}>
          ⟳ Reassign to Sonnet
        </button>
        <button onClick={() => handleReassign('opus')}>
          ⟳ Reassign to Opus
        </button>
      </div>
      <div className="hhp-context-menu-section">
        <button onClick={() => cancelTask(task.id)}>
          🗑️ Cancel Task
        </button>
        <button onClick={() => bumpPriority(task.id)}>
          ⬆️ Bump Priority
        </button>
      </div>
    </div>
  );
}
```

### Store Updates

```typescript
// Add to queueStore.ts

reassignTask: async (taskId: string, model: string) => {
  await fetch(`/factory/task/${taskId}/reassign`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model }),
  });
  // Refresh queue
  get().fetchQueue();
  messageBus.publish('factory:task-reassigned', { taskId, model });
},

pause: async () => {
  await fetch('/factory/queue/pause', { method: 'POST' });
  set({ state: 'paused' });
  messageBus.publish('factory:queue-paused', {});
},

resume: async () => {
  await fetch('/factory/queue/resume', { method: 'POST' });
  set({ state: 'running' });
  messageBus.publish('factory:queue-resumed', {});
},
```

---

## File Targets

| File | Action | Lines |
|------|--------|-------|
| `hivenode/routes/factory_routes.py` | MODIFY | +40 |
| `browser/src/primitives/queue-pane/QueueControls.tsx` | CREATE | ~40 |
| `browser/src/primitives/queue-pane/TaskContextMenu.tsx` | CREATE | ~60 |
| `browser/src/primitives/queue-pane/queueStore.ts` | MODIFY | +30 |
| `browser/src/primitives/queue-pane/QueuePane.tsx` | MODIFY | +20 |

---

## Reference Files

Read before implementation:
- `browser/src/primitives/queue-pane/QueuePane.tsx`
- `browser/src/primitives/queue-pane/queueStore.ts`
- `hivenode/routes/factory_routes.py`
- `.deia/hive/scripts/queue/run_queue.py` — for pause/resume mechanism

---

## Acceptance Criteria

- [ ] Pause button stops new dispatches
- [ ] Resume button starts dispatching again
- [ ] Queue state reflected in header ("PAUSED" badge)
- [ ] Long-press task shows context menu
- [ ] Reassign moves task to different model
- [ ] Cancel removes task from queue
- [ ] Bump priority moves task up in queue
- [ ] Fr4nk can "pause the queue" via voice

## Smoke Test

```bash
# Backend endpoints
curl -X POST http://127.0.0.1:8420/factory/queue/pause | jq
curl http://127.0.0.1:8420/factory/queue/state | jq
curl -X POST http://127.0.0.1:8420/factory/queue/resume | jq

# Manual frontend test:
# 1. Open queue-pane
# 2. Tap pause button
# 3. Verify "PAUSED" badge appears
# 4. Long-press a queued task
# 5. Tap "Reassign to Opus"
# 6. Verify task model updated
```

## Constraints

- Pause affects dispatcher, not active tasks
- Reassign only works for queued/failed tasks (not active)
- Context menu closes on outside tap
- All API calls require auth

## Response File

`.deia/hive/responses/20260409-FACTORY-105-RESPONSE.md`

---

*SPEC-FACTORY-105 — Q88N — 2026-04-09*

## Triage History
- 2026-04-12T18:52:40.078856Z — requeued (empty output)
