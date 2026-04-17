# TASK-REFACTOR-UNBLOCK-002: Clear MW-V04 and Dispatch REFACTOR-031

## Role
Bee (execute immediately, no planning)

## You are in EXECUTE mode. Do NOT enter plan mode. Do NOT ask for approval. Just do it.

## Steps (do these in order, stop after each confirms success)

### Step 1: Move REFACTOR-031 from _needs_review to backlog
```bash
mv .deia/hive/queue/_needs_review/SPEC-REFACTOR-031-set-md-configs.md .deia/hive/queue/backlog/
```

### Step 2: Delete the MW-V04 zombie from everywhere
```bash
rm -f .deia/hive/queue/_zombies/SPEC-MW-V04-verify-conversation-pane.md
rm -f .deia/hive/queue/_dead/SPEC-MW-V04-verify-conversation-pane.md
```

### Step 3: Restart scheduler daemon
Find and kill the scheduler, then restart it:
```bash
# Find PIDs - look for scheduler_daemon
tasklist | findstr python

# Kill ALL python processes running scheduler_daemon.py
# Use: taskkill //PID <number> //F
# IMPORTANT: double slashes on Windows, e.g. taskkill //PID 12345 //F
```

Then restart:
```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter
python hivenode/scheduler/scheduler_daemon.py --schedule-dir .deia/hive --queue-dir .deia/hive/queue &
```

Wait 30 seconds for it to regenerate schedule.json.

### Step 4: Verify MW-V04 is gone from schedule
```bash
python -c "import json; s=json.load(open('.deia/hive/schedule.json')); mw=[t for t in s.get('tasks',s) if 'MW-V04' in t.get('task_id','')]; print('MW-V04 CLEARED' if not mw else 'MW-V04 STILL PRESENT')"
```

### Step 5: Check if 031 dispatches automatically
Wait 2 minutes, then check:
```bash
ls .deia/hive/queue/_active/ | grep REFACTOR
ls .deia/hive/queue/backlog/ | grep "031"
```

### Step 6: If 031 is NOT active after 2 minutes, manually dispatch it
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/queue/backlog/SPEC-REFACTOR-031-set-md-configs.md --model sonnet --role bee --inject-boot
```

After dispatch, move original to _done:
```bash
mv .deia/hive/queue/backlog/SPEC-REFACTOR-031-set-md-configs.md .deia/hive/queue/_done/
```

### Step 7: Confirm pipeline is flowing
```bash
echo "=== DONE ===" && ls .deia/hive/queue/_done/ | grep REFACTOR
echo "=== ACTIVE ===" && ls .deia/hive/queue/_active/ | grep REFACTOR
```

## Response
Write a SHORT status to `.deia/hive/responses/20260408-REFACTOR-UNBLOCK-002-RESPONSE.md`

## Constraints
- Branch: refactor/auto-2026-04-07
- Windows: use //PID and //F (double slashes) for taskkill
- Do NOT modify application code
- Do NOT monitor for extended periods — just unblock and report
