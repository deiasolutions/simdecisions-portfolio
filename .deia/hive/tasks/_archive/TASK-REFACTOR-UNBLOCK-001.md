# TASK-REFACTOR-UNBLOCK-001: Clear MW-V04 Blocker and Resume Pipeline

## Role
Queen (Q33N)

## Context

The overnight refactor pipeline on `refactor/auto-2026-04-07` is blocked at 45% (9/20 specs done). The dispatcher daemon is stuck trying to dispatch MW-V04, a zombie spec that doesn't exist in the queue.

### The Problem
- `schedule.json` has MW-V04 with status "ready"
- MW-V04 spec file is in `_zombies/` (or `_dead/`), NOT in `backlog/`
- Dispatcher logs `spec_not_found` every cycle and can't dispatch anything else
- REFACTOR-031 is sitting in queue root waiting to be processed but the dispatcher is deadlocked

### Current Pipeline State
- Done: REFACTOR-010 through 030 (9 specs)
- Blocked: REFACTOR-031 through 063 (11 specs remaining)
- REFACTOR-031 may be in queue root, `_needs_review/`, or `backlog/` — check first

## Your Job

### Step 1: Restart the Scheduler Daemon

The scheduler daemon regenerates `schedule.json` from current queue state. Restarting it will remove the MW-V04 ghost.

```bash
# Find and kill the scheduler daemon
tasklist | findstr python
# Look for the one running scheduler_daemon.py

# Kill it (use PID from tasklist)
taskkill //PID <pid> //F

# Restart it
python hivenode/scheduler/scheduler_daemon.py --schedule-dir .deia/hive --queue-dir .deia/hive/queue &
```

Wait 30 seconds, then verify:
```bash
# Check schedule.json no longer has MW-V04
python -c "import json; s=json.load(open('.deia/hive/schedule.json')); print([t['task_id'] for t in s.get('tasks',s) if 'MW-V04' in t.get('task_id','')])"
```

### Step 2: Ensure REFACTOR-031 is Dispatchable

After scheduler restart, REFACTOR-031 should be in the new schedule as "ready" (since 030 is in `_done/`).

Check:
```bash
# Where is 031?
ls .deia/hive/queue/ | grep "031"
ls .deia/hive/queue/_needs_review/ | grep "031"
ls .deia/hive/queue/backlog/ | grep "031"
ls .deia/hive/queue/_active/ | grep "031"
```

If 031 is in `_needs_review/`:
```bash
mv .deia/hive/queue/_needs_review/SPEC-REFACTOR-031-set-md-configs.md .deia/hive/queue/backlog/
```

If 031 is in queue root but dispatcher isn't picking it up after restart, manually dispatch:
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/queue/backlog/SPEC-REFACTOR-031-set-md-configs.md --model sonnet --role bee --inject-boot
```

### Step 3: Monitor Until 031 Completes

Wait for REFACTOR-031 to complete (up to 15 minutes). Check:
```bash
ls .deia/hive/queue/_active/ | grep REFACTOR
ls .deia/hive/queue/_done/ | grep "031"
ls .deia/hive/refactor/ | grep "changes-031"
```

### Step 4: Verify Pipeline Resumes

After 031 completes, the scheduler should mark 032 as ready and dispatch it. Monitor for one more spec (032) to confirm the pipeline is flowing again.

### Step 5: Monitor Through Remaining Phase 2

If time permits (up to 45 minutes total), watch 032-034 process:
- 032: wire egg loading
- 033: dedupe utilities
- 034: remove dead code

For each completion, verify:
- Output file exists: `changes-0XX.json`
- No build breaks: `cd browser && npx tsc --noEmit 2>&1 | head -5`
- Next spec auto-dispatches

### Step 6: If Phase 2 Completes, Monitor Phase 3 Start

Phase 3 specs (depend on 034):
- 040: DES UI surface
- 041: finish partial features
- 042: implement missing features

Just confirm 040 dispatches after 034 completes.

## Response

Write to `.deia/hive/responses/20260407-REFACTOR-UNBLOCK-001-RESPONSE.md`:
- Whether scheduler restart worked
- Whether MW-V04 was cleared from schedule
- REFACTOR-031 dispatch status
- How far the pipeline advanced during your session
- Any new blockers

## Constraints
- Stay on branch `refactor/auto-2026-04-07`
- Do NOT modify application code — only restart services, move specs, dispatch bees
- Windows: use `taskkill //PID <n> //F` (double slashes), NOT `/PID`
- MSYS path fix: If running Railway commands, use `MSYS_NO_PATHCONV=1` prefix
