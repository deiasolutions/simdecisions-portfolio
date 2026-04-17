# TASK-MCP-QUEUE-02: Add MCP Event HTTP Endpoints

## Objective

Create HTTP endpoints in hivenode, scheduler, and dispatcher to enable MCP event delivery via POST requests.

## Context

TASK-MCP-QUEUE-01 creates a folder watcher that emits events. This task creates the transport layer for delivering those events to scheduler and dispatcher via HTTP POST.

**Design:** `.deia/hive/responses/20260406-MCP-QUEUE-NOTIFICATIONS-DESIGN.md` (section: MCP Event Contract)

## Files to Read First

- `hivenode/routes/queue_events.py` (created by TASK-MCP-QUEUE-01)
  - Event payload format
- `hivenode/scheduler/scheduler_daemon.py`
  - Daemon loop structure to understand where to hook events
- `hivenode/scheduler/dispatcher_daemon.py`
  - Daemon loop structure
- `hivenode/main.py`
  - FastAPI app structure

## Deliverables

- [ ] `hivenode/routes/queue_events.py` modifications
  - `POST /mcp/queue/broadcast` endpoint — receives events from watcher, forwards to subscribers
  - Subscriber registry (in-memory list of URLs)
  - Async HTTP POST to each subscriber (use httpx.AsyncClient)
  - Error handling (log failed deliveries, don't block)
- [ ] `hivenode/scheduler/scheduler_mcp_server.py` — NEW FILE
  - Lightweight FastAPI app on port 8422
  - `POST /mcp/event` endpoint — receives events, calls daemon.on_mcp_event()
  - Health check: `GET /health`
  - CORS disabled (local-only)
- [ ] `hivenode/scheduler/dispatcher_mcp_server.py` — NEW FILE
  - Lightweight FastAPI app on port 8423
  - `POST /mcp/event` endpoint — receives events, calls daemon.on_mcp_event()
  - Health check: `GET /health`
  - CORS disabled (local-only)
- [ ] Subscriber registration logic
  - Scheduler/dispatcher register on startup via `POST /mcp/queue/subscribe`
  - Payload: `{"service": "scheduler", "url": "http://localhost:8422/mcp/event"}`
  - Hivenode stores in-memory subscriber list
- [ ] Integration tests: `tests/integration/test_mcp_http.py`
  - Test event broadcast (1 event → 2 subscribers)
  - Test failed delivery (subscriber down)
  - Test duplicate suppression (same event within 500ms)
  - Test subscription registration

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Subscriber HTTP timeout (5s timeout)
  - Subscriber returns 500 error
  - Malformed event payload
  - No subscribers registered (no-op)

## Acceptance Criteria

- [ ] Hivenode broadcasts events to all registered subscribers
- [ ] Scheduler MCP server runs on port 8422, receives events
- [ ] Dispatcher MCP server runs on port 8423, receives events
- [ ] Failed deliveries logged but don't block other subscribers
- [ ] Broadcast is async (doesn't block watcher thread)
- [ ] Subscription API works (POST /mcp/queue/subscribe)
- [ ] Integration tests: 8+ tests, all passing
- [ ] No file over 500 lines

## Implementation Notes

### Event Broadcast Flow

```
[Watcher detects file move]
    ↓
[QueueEventHandler.on_moved()]
    ↓
[POST http://localhost:8420/mcp/queue/broadcast]
    ↓
[Hivenode routes/queue_events.py]
    ↓ (async for each subscriber)
    ├─→ POST http://localhost:8422/mcp/event (scheduler)
    └─→ POST http://localhost:8423/mcp/event (dispatcher)
```

### Subscriber Registry (In-Memory)

```python
# In hivenode state manager or global
subscribers: list[dict] = [
    {"service": "scheduler", "url": "http://localhost:8422/mcp/event"},
    {"service": "dispatcher", "url": "http://localhost:8423/mcp/event"},
]
```

### Broadcast Implementation

```python
async def broadcast_event(event: dict):
    """Broadcast event to all subscribers."""
    async with httpx.AsyncClient() as client:
        tasks = []
        for subscriber in subscribers:
            task = client.post(
                subscriber["url"],
                json=event,
                timeout=5.0
            )
            tasks.append(task)

        # Fire and forget (log errors)
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Failed to deliver to {subscribers[i]['service']}: {result}")
```

### Scheduler MCP Server

```python
# hivenode/scheduler/scheduler_mcp_server.py
from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

# Global reference to daemon (set on startup)
daemon = None

@app.post("/mcp/event")
async def receive_event(request: Request):
    event = await request.json()
    if daemon:
        daemon.on_mcp_event(event)
    return {"ok": True}

@app.get("/health")
async def health():
    return {"status": "ok"}

def run_server(daemon_instance, port: int = 8422):
    global daemon
    daemon = daemon_instance
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="error")
```

### Integration with Daemon

Scheduler/dispatcher daemons will be modified in TASK-MCP-QUEUE-03/04. For now, create stub `on_mcp_event()` methods:

```python
# In SchedulerDaemon
def on_mcp_event(self, event: dict):
    """Handle MCP event (stub for TASK-MCP-QUEUE-03)."""
    logger.info(f"Received MCP event: {event['event']}")
    # TODO: Implement wake logic in TASK-MCP-QUEUE-03
```

## Constraints

- No file over 500 lines
- Use FastAPI for HTTP servers (consistent with hivenode)
- Use httpx for async HTTP client (not requests)
- Timeout: 5s for subscriber POSTs
- No hardcoded URLs (read from env or config)
- Thread-safe subscriber registry (use lock if modified at runtime)
- No stubs in HTTP handlers (only in daemon hooks)

## Dependencies

**Depends on:** TASK-MCP-QUEUE-01 (folder watcher must exist)

## Estimated Duration

1.5-2 hours (Sonnet)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260406-TASK-MCP-QUEUE-02-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
