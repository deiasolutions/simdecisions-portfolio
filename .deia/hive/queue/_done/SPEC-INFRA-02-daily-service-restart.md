# SPEC-INFRA-02: Daily Service Restart Maintenance Script

## Priority
P2

## Model Assignment
haiku

## Depends On
None

## Intent

Create a daily maintenance script that restarts all local development services cleanly. Services drift over long uptimes — the queue runner dies silently, the scheduler accumulates stale state, and Vite's HMR can degrade. A daily restart is cheap insurance.

## Files to Read First

- hivenode/main.py
- hivenode/scheduler/scheduler_daemon.py
- hivenode/queue_bridge.py

## Services to Restart

1. **hivenode** (port 8420) — FastAPI backend, embedded queue runner, queue watcher
2. **vite** (port 5173) — Frontend dev server
3. **scheduler daemon** — Runs as standalone Python process

## Work Required

### 1. Create restart script

Write `_tools/restart-services.sh` (bash, Windows Git Bash compatible):

- Find and kill processes on ports 8420, 5173
- Find and kill any `scheduler_daemon.py` processes
- Wait for ports to be free
- Start hivenode: `python -m uvicorn hivenode.main:app --host 127.0.0.1 --port 8420`
- Start vite: `cd browser && npx vite --port 5173`
- Start scheduler: `python hivenode/scheduler/scheduler_daemon.py --schedule-dir .deia/hive --queue-dir .deia/hive/queue`
- Health check: poll `/health` endpoint until 200 or timeout after 30s
- Verify queue runner: check `/build/queue-runner-status` returns `running: true`
- Report: print status of each service (up/down)

### 2. Make it safe

- Script must be idempotent — safe to run even if services are already stopped
- Must not kill unrelated Python/Node processes
- Must handle port conflicts gracefully
- Use `MSYS_NO_PATHCONV=1` prefix for any taskkill commands (Git Bash compatibility)

## Acceptance Criteria

- [ ] Script restarts all 3 services cleanly
- [ ] Script is idempotent (safe to run when services already stopped)
- [ ] Health check confirms hivenode is up after restart
- [ ] Queue runner status confirmed alive after restart
- [ ] Script works in Git Bash on Windows 11
- [ ] No hardcoded absolute paths (uses relative paths from repo root)

## Constraints

- No file over 500 lines
- No stubs
- No git operations
- 8-section response file on completion

## Smoke Test

Run `bash _tools/restart-services.sh` from repo root. All 3 services come up. `/health` returns 200. `/build/queue-runner-status` returns `running: true`.
