# SPEC-INFRA-02: Daily Service Restart Maintenance Script -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-04-06

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\restart-services.sh` (created)

## What Was Done

- Created `_tools/restart-services.sh` bash script (366 lines) with the following capabilities:
  - Kills processes on ports 8420 (hivenode) and 5173 (vite) using netstat + taskkill
  - Kills scheduler_daemon.py processes by name using tasklist + wmic
  - Waits up to 10 seconds for ports to be freed (graceful cleanup)
  - Starts hivenode FastAPI server via uvicorn on port 8420
  - Starts vite dev server on port 5173
  - Starts scheduler daemon with correct arguments (--schedule-dir, --queue-dir)
  - Health checks hivenode /health endpoint with 30s timeout (6 attempts x 5s)
  - Verifies queue runner status at /build/queue-runner-status
  - Reports final status of all 3 services with color-coded output
  - Uses MSYS_NO_PATHCONV=1 prefix for taskkill (Git Bash compatibility)
  - Logs all services to repo root (hivenode.log, vite.log, scheduler.log)
  - Idempotent (safe to run when services already stopped/started)
  - No hardcoded absolute paths (uses relative paths from repo root)

## Tests Run

### Manual Smoke Test

Executed `bash _tools/restart-services.sh` from repo root:

```bash
cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter
bash _tools/restart-services.sh
```

**Results:**
- ✓ Script executed successfully
- ✓ All 3 services stopped cleanly (hivenode, vite, scheduler)
- ✓ All 3 services restarted successfully
- ✓ Health check passed: `curl http://127.0.0.1:8420/health` → `{"status":"ok"}`
- ✓ Queue runner verified alive: `curl http://127.0.0.1:8420/build/queue-runner-status` → `{"running":true}`
- ✓ Idempotent: safe to run multiple times
- ✓ Windows Git Bash compatible (no pgrep/pkill dependencies)

### Acceptance Criteria Verification

- [x] Script restarts all 3 services cleanly
- [x] Script is idempotent (safe to run when services already stopped)
- [x] Health check confirms hivenode is up after restart
- [x] Queue runner status confirmed alive after restart
- [x] Script works in Git Bash on Windows 11
- [x] No hardcoded absolute paths (uses relative paths from repo root)

## Learnings

1. **pgrep/pkill not available in Git Bash** — Used tasklist + wmic instead for Windows compatibility
2. **Port cleanup timing** — Some processes take >2s to release ports after taskkill, needed 10s retry loop
3. **Scheduler daemon check** — Most reliable method is checking recent log file content vs. process name matching
4. **Git Bash path translation** — MSYS_NO_PATHCONV=1 prefix required for taskkill to prevent path mangling
5. **nohup background processes** — Services must be started with nohup + background (&) for daemon mode

## Edge Cases Handled

1. **Services already stopped** — Script continues gracefully (idempotent)
2. **Ports still in use after kill** — Script warns but continues (allows retry on next run)
3. **Missing log files** — Gracefully handled with conditional checks
4. **Multiple Python processes** — Filters by scheduler_daemon.py in command line
5. **Health check timeout** — Retries 6 times with 5s sleep between attempts

## Known Limitations

1. **Port cleanup warnings** — If port is stubborn (process takes >10s to die), script continues but warns
2. **Scheduler daemon status** — Detection via log file only (no PID tracking in status output)
3. **Windows-specific** — Uses taskkill, netstat, wmic (Linux would need different commands)

## Deployment Notes

- Script is ready for daily cron/scheduled task execution
- Recommended: Run as `bash _tools/restart-services.sh >> restart.log 2>&1` to capture full output
- Services log to: hivenode.log, vite.log, scheduler.log (all in repo root)
- No git operations required (script only manages processes)

## Cost

Estimated: 0.5 hours (model: haiku)
Actual: ~0.7 hours (including testing and refinements)
