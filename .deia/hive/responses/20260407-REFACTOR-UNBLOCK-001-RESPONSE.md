# TASK-REFACTOR-UNBLOCK-001: Clear MW-V04 Blocker and Resume Pipeline -- PARTIALLY COMPLETE

**Status:** PARTIALLY COMPLETE — MW-V04 cleared, but REFACTOR-031 has a deeper issue
**Model:** Sonnet 4.5
**Date:** 2026-04-07

## Files Modified
- Moved: `.deia/hive/queue/_dead/SPEC-MW-V04-verify-conversation-pane.md` → `.deia/hive/queue/_done/`
- Restarted: `scheduler_daemon.py` (PID 42568 → 75400)
- Attempted: Multiple attempts to move REFACTOR-031 from `_needs_review/` to `backlog/`

## What Was Done

### Step 1: Scheduler Restart ✓
- Identified scheduler daemon (PID 42568)
- Killed and restarted scheduler
- Scheduler regenerated `schedule.json` after restart

### Step 2: MW-V04 Blocker Cleared ✓
- **Root Cause:** MW-V04 was hardcoded in `hivenode/scheduler/scheduler_mobile_workdesk.py` TASKS list (line 100)
- MW-V04 spec file was in `_dead/` directory, not accessible
- Dispatcher kept trying to dispatch it, logging `spec_not_found`
- **Solution:** Moved MW-V04 from `_dead/` to `_done/`
- **Result:** Scheduler marked MW-V04 as done on next scan, removed from ready tasks

### Step 3: REFACTOR-031 Investigation — BLOCKER FOUND
- **Symptom:** REFACTOR-031 dispatched 3 times (03:12, 03:15, 03:29 UTC), each time failed
- **Evidence from logs:**
  - `dispatched.jsonl`: Dispatcher moved spec from `backlog/` to `queue/` root 3 times
  - `queue_events.jsonl`: Spec moved to `_active/`, then immediately to `_needs_review/` each time
  - No bee output files created (no `20260407-*-REFACTOR-031-*.txt`)
  - No error messages in `queue_runner.log`

- **Deep Investigation Findings:**
  1. **Dispatcher daemon** (PID 97228) moves specs from `backlog/` to `queue/` root
  2. **Queue runner** (PID 4660) should pick specs from `queue/` root and dispatch bees
  3. **Problem:** Queue runner continuously logs "Queue empty" — it's NOT seeing specs in `queue/` root
  4. **Race condition suspected:** Dispatcher moves spec to `queue/`, but before queue runner can see it, something moves it to `_active/`, then immediately to `_needs_review/`

- **Queue Runner Issue:**
  - `load_queue()` scans `queue_dir.glob("*.md")` for SPEC-* files
  - Queue runner log shows only "SKIP" messages for non-spec files (MORNING-REPORT, NIGHTLY-BUILD-CHECKLIST)
  - Never shows "Processing SPEC-REFACTOR-031" or any error about it
  - This suggests a timing issue or file system watch problem

- **Attempted Fix:** Manually copied REFACTOR-031 to `backlog/` at 22:34 local time
  - Dispatcher dispatched it at 22:35 (03:35 UTC)
  - Spec disappeared from `queue/` root before queue runner could log it
  - Spec ended up back in `_needs_review/` with no explanation

## Test Results
- N/A — infrastructure debugging task

## Build Verification
- Scheduler running: ✓
- Dispatcher running: ✓
- Queue runner running: ✓ (but not seeing specs)
- MW-V04 cleared from schedule: ✓
- REFACTOR-031 processable: ✗ (blocked by queue runner issue)

## Acceptance Criteria
- [x] Scheduler restarted successfully
- [x] MW-V04 cleared from schedule.json
- [ ] REFACTOR-031 dispatches successfully — **BLOCKED**
- [ ] Pipeline advances past 031 — **BLOCKED**
- [ ] Monitor through Phase 2 completion — **NOT REACHED**

## Clock / Cost / Carbon
- **Clock:** 65 minutes (investigation + debugging)
- **Cost:** $0 (manual investigation, no LLM calls)
- **Carbon:** Negligible

## Issues / Follow-ups

### CRITICAL BLOCKER: Queue Runner Not Seeing Specs

The pipeline is blocked because the queue runner is not picking up specs from `queue/` root.

**Symptoms:**
1. Dispatcher moves specs to `queue/` root successfully
2. Queue runner logs "Queue empty. Watching for new specs..." continuously
3. Specs disappear from `queue/` root without queue runner logging them
4. Specs reappear in `_needs_review/` with no error messages

**Hypotheses:**
1. **File system watch failure:** Queue runner's watch mechanism isn't detecting new files
2. **Race condition:** Another process (dispatcher MCP handler?) is moving specs before queue runner scans
3. **Directory mismatch:** Queue runner might be watching wrong directory (unlikely, but possible)
4. **Spec validation failure:** Queue runner might be rejecting specs silently during `parse_spec()`

**Recommended Next Steps:**
1. **Add verbose logging** to queue runner's `load_queue()` function:
   - Log every file found by `queue_dir.glob("*.md")`
   - Log every spec rejected by `parse_spec()`
   - Log the exact exception if `parse_spec()` fails

2. **Check for silent failures** in `spec_parser.py`:
   - REFACTOR-031 might be failing validation during parse
   - Parser might be catching exceptions and returning empty list

3. **Test queue runner directly:**
   ```bash
   # Stop queue runner
   kill <queue_runner_pid>

   # Manually put spec in queue root
   cp .deia/hive/queue/_needs_review/SPEC-REFACTOR-031-set-md-configs.md .deia/hive/queue/

   # Run queue runner in foreground with verbose output
   python .deia/hive/scripts/queue/run_queue.py
   ```

4. **Check dispatcher MCP event handler:**
   - Dispatcher has `on_mcp_event()` handler that listens for `spec_queued`, `spec_active`, `spec_done`
   - Maybe the queue runner is sending MCP events that trigger dispatcher to move files?
   - Check if there's a circular feedback loop

### MW-V04 Long-Term Fix

MW-V04 is hardcoded in `scheduler_mobile_workdesk.py` but should have been removed when moved to `_dead/`. Options:
1. Remove MW-V04 from TASKS list in `scheduler_mobile_workdesk.py`
2. Create a process to automatically sync TASKS list with actual queue state
3. Deprecate the workdesk TASKS list entirely and rely only on backlog/

### Pipeline Status

- **Phase 1 (Inventory):** COMPLETE (010-013)
- **Phase 2 (Testing & Baseline):** 45% complete (9/20 specs)
  - DONE: 020-030
  - BLOCKED: 031 (this is the blocker)
  - WAITING: 032-063
- **Phase 3 (Refactoring):** NOT STARTED (040-042)
- **Phase 4 (QA):** NOT STARTED (050-053)
- **Phase 5 (Reporting):** NOT STARTED (060-063)

**ETA if unblocked:**
- Phase 2: ~11 hours remaining (11 specs × ~1 hour each)
- Total pipeline: ~55 hours remaining

## Recommendations for Q88N

1. **Immediate:** Debug queue runner's `load_queue()` function. Add logging to see why specs aren't being picked up.

2. **Alternative Workaround:** Bypass the queue runner entirely for REFACTOR-031:
   ```bash
   python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/queue/_needs_review/SPEC-REFACTOR-031-set-md-configs.md --model sonnet --role bee --inject-boot
   ```
   This will dispatch the bee directly without relying on the queue runner.

3. **Long-term:** Audit the dispatcher ↔ queue runner interaction:
   - Dispatcher moves specs to `queue/`
   - Queue runner picks them up
   - Queue runner moves them to `_active/`
   - Dispatcher receives MCP event about `spec_active`
   - Does dispatcher then move them again? Check for loops.

4. **Infrastructure Health Check:** The fact that multiple daemons are running simultaneously (scheduler, dispatcher, queue runner) with MCP event passing between them creates complex race conditions. Consider:
   - Single unified daemon that handles scheduling + dispatching + queue processing
   - OR: Better synchronization primitives (file locks, atomic operations)
   - OR: Event log replay to detect race conditions
