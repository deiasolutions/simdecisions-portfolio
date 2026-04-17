# TASK-131: Ship Plan Queue Feeder v2

**Role:** Q33NR (regent)
**Model:** sonnet
**Priority:** P0

## Role Override
regent

## Objective

You are the Ship Plan Queue Feeder. You read `docs/specs/SHIP-PLAN.md` and feed items into `.deia/hive/queue/` one or two at a time, waiting for the queue to drain before adding more.

You are NOT the queue runner. The queue runner is a separate process (`run_queue.py`) that processes whatever is in the queue directory. Your job is to control WHAT goes in and WHEN.

## Feeding Rules

1. **1-2 items at a time.** Never more than 2 specs in the queue at once.
2. **Big items go solo.** If an item is estimated at >1 hour or >1000 lines, send it alone. Do not pair it.
3. **No conflicting pairs.** Two items that touch the same files or the same module cannot be in the queue at the same time. Examples of conflicts:
   - Two items both editing `browser/src/shell/` files
   - Two items both editing `hivenode/routes/`
   - Two items both needing to run and pass the same test suite
4. **Follow ship plan order.** Work through the plan top-to-bottom, wave by wave. Don't skip ahead.
5. **Skip non-bee items.** Tasks marked "Q33NR direct", "Q33NR", "Config", or "Verify" in the ship plan are not for bees. Skip them (or do them yourself if they're simple like DB queries).
6. **Wait for drain.** After adding specs, poll the queue directory every 60 seconds. When no `.md` files remain (excluding MORNING-REPORT files), the queue is drained. Then add the next batch.

## How to Create a Spec File

Write a markdown file to `.deia/hive/queue/` with this format:

```markdown
# SPEC: {title}

## Priority
P0

## Model Assignment
{haiku or sonnet — use the model from the ship plan}

## Objective
{What the bee should accomplish. Be specific about files, paths, line counts.}

## Acceptance Criteria
- [ ] {Specific deliverable 1}
- [ ] {Specific deliverable 2}
- [ ] All tests pass
- [ ] No regressions

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only

## Smoke Test
- [ ] python -m pytest {relevant test path} passes
- [ ] No new test failures
```

Filename format: `2026-03-15-{HHMM}-SPEC-{short-description}.md`

Use current time for HHMM so each spec has a unique filename.

## Polling

After adding spec(s) to the queue, check if the queue is drained:

```python
import time, os
from pathlib import Path

queue = Path(".deia/hive/queue")
while True:
    specs = [f for f in queue.glob("*.md")
             if "MORNING-REPORT" not in f.name
             and "event-log" not in f.name
             and "session-" not in f.name
             and "monitor-state" not in f.name]
    if len(specs) == 0:
        break
    time.sleep(60)
```

When drained, add the next 1-2 items.

## What to Do First

1. Read `docs/specs/SHIP-PLAN.md` completely
2. Check what's already in the queue (`.deia/hive/queue/`) — don't duplicate
3. Check what's already done (`.deia/hive/queue/_done/`) — don't redo
4. Start from Wave 0, item 0.1 (or wherever the plan hasn't been done yet)
5. Create 1-2 spec files for the first non-conflicting, bee-dispatchable items
6. Poll until drained
7. Continue

## Reporting

After every 5 items processed, write a progress update to:
`.deia/hive/responses/20260315-SHIP-FEEDER-PROGRESS.md`

Include: items completed, items remaining, any failures, blockers.

## Build Monitor Heartbeats

Every spec you create MUST include this constraint in the Constraints section:

```
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "<spec_filename>", "status": "running", "model": "<model>", "message": "<progress>"}
```

This ensures the build monitor dashboard shows progress for every dispatched bee. The watchdog kills bees that stop heartbeating.

You (the feeder) should also heartbeat your own status:

```python
import urllib.request, json
payload = json.dumps({
    "task_id": "ship-plan-feeder",
    "status": "running",
    "model": "sonnet",
    "message": f"Wave {wave_num}: {completed}/{total} items done"
}).encode("utf-8")
req = urllib.request.Request(
    "http://localhost:8420/build/heartbeat",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST"
)
try:
    urllib.request.urlopen(req, timeout=2)
except Exception:
    pass
```

## Important Context

- The queue runner must already be running separately for specs to be processed
- Start it with: `python .deia/hive/scripts/queue/run_queue.py --watch`
- The `--watch` flag keeps it polling for new specs instead of exiting when the queue is empty
- There are already some specs in the queue from a previous session — check before adding
- The ship plan estimates ~500 minutes of total bee compute across 6 waves
- Read `.deia/BOOT.md` for repo conventions and hard rules
