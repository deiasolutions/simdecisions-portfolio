---
name: factory-health-check
description: >-
  Diagnose stuck, dead, or missing factory tasks. Use when a dispatched
  task has gone silent, the queue runner seems unresponsive, results
  haven't appeared, or Q88N asks "where is my build?" Covers queue
  runner health, MCP server status, stuck task detection, and result
  retrieval.
license: Proprietary
compatibility: Requires curl, netstat, Python 3.12+
metadata:
  author: Q88N
  version: "1.0"
  deia:
    cert_tier: 3
    carbon_class: none
    requires_human: false
---

# Factory Health Check

## When to Use

- A dispatched task has been "active" with 0 tokens for more than 5 minutes
- Q88N asks "where is X?" or "progress?" and there's nothing to report
- The queue runner returned a result but no output files appeared
- You suspect the MCP server or queue runner crashed
- After killing a direct dispatch that might conflict with a factory dispatch

## Steps

### Step 1: Check Queue Runner Health

```bash
curl -s http://127.0.0.1:8420/ 2>&1
```

**Expected:** `{"service":"hivenode","version":"X.X.X","mode":"local"}`
**If connection refused:** Queue runner is down. Tell Q88N to restart it.
**If timeout:** Network issue or process hung.

### Step 2: Check Queue Status

Write output to a temp file first (Windows cp1252 safety):

```bash
curl -s http://127.0.0.1:8420/build/status > /tmp/qs.json 2>&1
```

Then parse with Python:

```bash
C:/Python312/python.exe -c "
import json
d = json.load(open('/tmp/qs.json', 'r', encoding='utf-8'))
print('Active:', len(d.get('active', [])))
print('Queued:', len(d.get('queue', [])))
for t in d.get('active', []):
    print(f'  {t[\"task_id\"]}  status={t[\"status\"]}  tokens={t.get(\"output_tokens\",0)}  last_msg={t.get(\"last_logged_message\",\"none\")}')
"
```

**Stuck task indicators:**
- `status=dispatched` + `output_tokens=0` for more than 5 minutes = likely stuck
- `last_heartbeat` unchanged for more than 5 minutes = likely dead
- `last_logged_message=role=bee` with no follow-up = never started processing

### Step 3: Check MCP Server

```bash
netstat -ano | grep -E "842[0-9]"
```

**Expected ports:**
- 8420 — queue runner (required)
- 8421 — queue runner secondary (expected)
- 8422, 8423 — MCP servers (check PIDs)

If 8420 is listening but 8422/8423 are not, MCP servers are down. The factory can accept tasks but can't dispatch them to bees.

### Step 4: Check for Landed Results

Even if the queue shows "active", the bee may have finished and written files:

```bash
# Check for response files from today
ls -lt .deia/hive/responses/ | head -10
```

```bash
# Check for the specific task's output
# Replace TASK-ID with the actual task name
ls -la .deia/hive/responses/*TASK-ID*
```

Also check if the bee wrote files to the wrong location (common bee error):

```bash
# Check for recently modified files anywhere in repo
C:/Python312/python.exe -c "
import os, time
now = time.time()
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'media']]
    for f in files:
        p = os.path.join(root, f)
        if now - os.path.getmtime(p) < 1800:  # last 30 min
            print(f'{time.strftime(\"%H:%M:%S\", time.localtime(os.path.getmtime(p)))}  {p}')
"
```

### Step 5: Check for Dispatch Conflicts

If a direct dispatch (via `dispatch.py`) was run AND the factory also picked up the same task, they can collide. Check for:

```bash
# Look for temp dirs that failed to clean up
ls .deia/hive/temp/ 2>/dev/null
```

```bash
# Check if multiple Claude Code processes are running for the same task
tasklist | grep -i claude | head -10
```

### Step 6: Diagnose and Report

Based on findings, report one of:

| Finding | Diagnosis | Action |
|---|---|---|
| Queue runner down (connection refused) | Service crashed | Tell Q88N to restart |
| MCP ports not listening | MCP servers down | Tell Q88N to restart MCP |
| Task stuck at `dispatched`, 0 tokens, 5+ min | Never started | Kill and re-dispatch directly |
| Task stuck mid-processing, heartbeat stale | Bee died mid-run | Check for partial results, re-dispatch |
| Task shows active but results already exist | Queue status stale | Report results, ignore queue status |
| Temp dir cleanup failed | Lock conflict from killed dispatch | Remove stale temp dir manually |
| Everything looks fine, just slow | Large task, still processing | Wait and check again in 5 min |

## Output Format

Report to Q88N as a concise status block:

```
FACTORY HEALTH CHECK — [TIMESTAMP]
Queue runner: UP / DOWN
MCP server: UP / DOWN / UNKNOWN
Active tasks: [count]
Task [TASK-ID]: [status] — [diagnosis]
Action: [what to do next]
```

## Gotchas

- Windows `curl` output can have cp1252 encoding issues. Always write to a temp file before parsing with Python, using `encoding='utf-8'`.
- `netstat` output on Windows uses different formatting than Linux. Grep for port numbers, not service names.
- The queue runner can show a task as "active" long after the bee finished if the completion callback failed. Always check for landed result files before concluding a task is stuck.
- A killed direct dispatch (`dispatch.py`) can leave a stale temp dir in `.deia/hive/temp/` that blocks the factory from picking up the same task. Check and clean if needed.
- The queue runner status endpoint can return very large JSON (300+ KB) if there are many completed tasks. Don't try to print the whole thing — parse specific fields.
- `[DISPATCH] MCP unavailable, proceeding without MCP integration` in dispatch output means the bee ran without MCP tools. This is normal for direct dispatches but may indicate MCP is down if seen in factory dispatches.
