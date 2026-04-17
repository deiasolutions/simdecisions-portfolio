# INFRA-STARTUP: Local Development Startup Script

## Objective
Create a single startup script that launches all four local services needed for a development session: hivenode, Vite dev server, queue runner, and MCP server.

## Build Type
**New** — New script in `_tools/`.

## Problem Analysis
Every session requires manually starting 4 separate services before work can begin. A single startup script eliminates this friction and ensures nothing is forgotten.

## Services to Start
1. **Hivenode** — FastAPI backend (`python -m uvicorn hivenode.main:app`)
2. **Vite dev server** — Browser frontend (`cd browser && npm run dev`)
3. **Queue runner** — Watches queue, dispatches bees (`.deia/hive/scripts/queue/run_queue.py --watch`)
4. **MCP server** — Live telemetry (`hivenode/hive_mcp/local_server.py`)

## Files to Read First
- hivenode/main.py
- browser/package.json
- .deia/hive/scripts/queue/run_queue.py
- hivenode/hive_mcp/local_server.py

## Files to Modify
- _tools/start.py — NEW: startup script

## Deliverables
- [ ] Single `python _tools/start.py` launches all 4 services as background processes
- [ ] Each service gets its own labeled output (prefixed log lines or separate log files)
- [ ] Health check: waits for each service to respond before reporting ready
- [ ] `Ctrl+C` tears down all 4 cleanly (no orphaned processes)
- [ ] Works on Windows 11

## Acceptance Criteria
- [ ] All 4 services start from one command
- [ ] Output shows which services are up
- [ ] Clean shutdown kills all child processes (no orphaned node.exe or python.exe)
- [ ] Script exits with error if any service fails to start within timeout

## Test Requirements
- [ ] Manual smoke test: run script, verify all 4 services respond
- [ ] Manual smoke test: Ctrl+C, verify all processes terminated

## Constraints
- No file over 500 lines
- No stubs
- Windows 11 compatible (no bash-only constructs)
- Python only (no PowerShell, no batch files)

## Depends On
- Nothing

## Model Assignment
sonnet

## Priority
P2
