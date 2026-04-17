# PROPOSAL: Queue Runner MCP Wake Integration

## Problem
The queue runner (`run_queue.py`) is a standalone Python process that polls the filesystem on Fibonacci backoff (up to 21 minutes between checks). When new specs are added to the queue, there's no way to wake it — you wait or restart it. The MCP server (port 8421) runs inside hivenode but has no channel to the runner.

## Current Architecture
```
┌─────────────┐     heartbeat/ping     ┌─────────────┐     starts     ┌──────────┐
│ Queue Runner │ ──────────────────────>│  Hivenode    │ ─────────────>│ MCP      │
│ (standalone) │     POST :8420        │  :8420       │  async task   │ :8421    │
│ time.sleep() │                       │              │               │          │
└─────────────┘                        └──────────────┘               └──────────┘
       │                                      │                            │
       │  reads/writes                        │  reads                     │  reads
       v                                      v                            v
   .deia/hive/queue/*.md              monitor-state.json            queue/*.md (read-only)
```
Three isolated processes. Queue runner can't be signaled. MCP can read queue but can't dispatch or wake.

## Options

### Option A: Bring Queue Runner Into Hivenode (Recommended)
Move the queue loop into hivenode as an async background task, like the MCP server already is.

**How it works:**
- `run_queue.py` logic becomes an async function in `hivenode/queue_runner.py`
- Hivenode lifespan starts it as `asyncio.create_task(queue_loop())`
- Replace `time.sleep(interval)` with `asyncio.wait_for(wake_event.wait(), timeout=interval)`
- MCP gets a `queue_wake` tool that sets the `wake_event`
- Hivenode REST also gets `POST /build/queue-wake` for non-MCP callers

**Architecture after:**
```
┌──────────────────────────────────────────────────┐
│  Hivenode :8420                                  │
│  ┌────────────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Queue Runner   │  │ MCP      │  │ REST API │ │
│  │ (async task)   │<─│ :8421    │  │ :8420    │ │
│  │ Event.wait()   │  │queue_wake│  │/build/   │ │
│  └────────────────┘  └──────────┘  └──────────┘ │
│         │ shared asyncio.Event                   │
└──────────────────────────────────────────────────┘
```

**Pros:**
- Single process, shared memory — `asyncio.Event` is instant, zero IPC
- MCP and REST both wake the runner through the same Event
- No file watchers, no HTTP calls between processes, no named pipes
- Queue runner gets access to hivenode's DB, bus, state directly
- Eliminates orphan process management (runner dies when hivenode dies)
- Heartbeat/ping to self is eliminated (runner IS hivenode)

**Cons:**
- Largest refactor — `run_queue.py` (900+ lines) must become async
- Dispatch subprocess calls (`claude` CLI) need `asyncio.create_subprocess_exec`
- Queue runner crash could take down hivenode (mitigate with try/except in task)
- Can't run queue runner independently anymore (standalone mode needs preserved as fallback)

**Effort:** M (1-2 sessions). The core loop logic doesn't change, just the sleep/dispatch mechanics.

---

### Option B: HTTP Wake Endpoint on Queue Runner
Queue runner starts a tiny HTTP server on a secondary port. MCP calls it to wake.

**How it works:**
- Queue runner starts a `threading.Thread` with a minimal HTTP server on port 8422
- Exposes `POST /wake` — sets a `threading.Event`
- Main loop replaces `time.sleep(interval)` with `wake_event.wait(timeout=interval)`
- MCP gets a `queue_wake` tool that POSTs to `http://127.0.0.1:8422/wake`

**Pros:**
- Minimal change to queue runner (add ~40 lines)
- Runner stays standalone
- Any process can wake it (MCP, hivenode, CLI, curl)

**Cons:**
- Yet another port (8422)
- Three separate processes still
- Runner must handle HTTP server lifecycle alongside queue loop
- Port conflicts possible

**Effort:** S (30 min).

---

### Option C: Hivenode Proxies Wake via REST
Hivenode gets a `POST /build/queue-wake` endpoint. Queue runner polls it (or subscribes to SSE) instead of sleeping blind.

**How it works:**
- Hivenode adds `POST /build/queue-wake` — sets a flag in BuildState
- Hivenode adds `GET /build/queue-wake-poll` — returns flag and clears it
- Queue runner replaces `time.sleep(interval)` with polling `/build/queue-wake-poll` every N seconds during sleep
- MCP's `queue_wake` tool calls the hivenode REST endpoint

**Pros:**
- Queue runner stays standalone
- MCP → hivenode → runner chain uses existing HTTP
- No new ports

**Cons:**
- Still polling (just faster — every 2-5s during sleep vs 21min)
- Not a true instant wake, just reduced latency
- Extra HTTP chatter during idle

**Effort:** S (30 min).

---

### Option D: File Sentinel
MCP writes `.deia/hive/queue/.wake`. Runner checks for it in sleep loop.

**Pros:** Trivially simple (10 lines).
**Cons:** Still polling. Filesystem-based IPC is fragile. Not a real solution.

**Not recommended.**

---

## Recommendation

**Option A** is the right architecture. The queue runner being a separate process is a historical artifact from before hivenode had the MCP. Now that hivenode is the coordination hub (REST + MCP + build monitor), the queue runner belongs inside it.

Option B is the fast fallback if A is too much for this session.

## Decision Needed
Which option? If A, should standalone mode be preserved as a CLI fallback (`python run_queue.py --standalone`)?
