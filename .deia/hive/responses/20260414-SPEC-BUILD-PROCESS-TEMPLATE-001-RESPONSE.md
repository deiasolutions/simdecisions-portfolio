# SPEC-BUILD-PROCESS-TEMPLATE-001: Build Process Template IR + Wiring -- BLOCKED

**Status:** BLOCKED (role mismatch)
**Model:** Sonnet 4.5
**Date:** 2026-04-14
**Bot ID:** BEE-QUEUE-TEMP-SPEC-BUILD-PROCESS-

## Files Modified

None (task not started)

## What Was Done

**BLOCKER REPORT: This task was dispatched to a worker bee (b33) but requires Q33N coordination.**

### Why This is Not Bee-Sized Work

This spec contains **6 distinct tasks** that span multiple systems:

1. **Task 1:** Wire `des_integration.py` into `run_queue.py` (1 hour)
2. **Task 2:** Add SMOKE node to `pipeline.ir.json` (30 min)
3. **Task 3:** Add CATALOG node to `pipeline.ir.json` (30 min)
4. **Task 4:** Add HAT node to `pipeline.ir.json` (1 hour)
5. **Task 5:** Add front-end phases (IDEATE, DESIGN, TABLETOP, etc.) to `pipeline.ir.json` (4 hours)
6. **Task 6:** Wire EfemeraChannel to DeciderRouter in `simdecisions/des/adapters.py` (2 hours)

**Total estimated effort:** ~9 hours across multiple subsystems

### What Should Happen

According to `.deia/HIVE.md`:

1. **Q33NR** should write a briefing for Q33N
2. **Q33N** should read this spec, break it into bee-sized tasks, and return task files to Q33NR
3. **Q33NR** should review and approve the task breakdown
4. **Q33N** should then dispatch individual bees for each task

### Current State

- This spec was dispatched directly to a bee (me)
- No task breakdown exists
- No Q33NR review has occurred
- Work scope exceeds single bee capacity

## Test Results

N/A — task not started

## Build Verification

N/A — task not started

## Acceptance Criteria

From spec:
- [ ] `des_integration.py` called from `run_queue.py` for opted-in specs
- [ ] SMOKE node added to `pipeline.ir.json` and executing
- [ ] CATALOG node added and auto-updating `inv_features`
- [ ] HAT node added with file-based human gate
- [ ] Front-end phases (IDEATE through SPEC-REVIEW) added
- [ ] Skip logic implemented via guard expressions
- [ ] Event Ledger captures all phase transitions
- [ ] At least one spec successfully runs through IR-driven execution

**Status:** None completed — task requires Q33N breakdown first

## Clock / Cost / Carbon

- **Clock:** 0.2 hours (blocker analysis)
- **Cost:** ~$0.15 USD (reading spec + coordination files + writing response)
- **Carbon:** ~0.001 kg CO2e

## Issues / Follow-ups

### Immediate Action Required

**Route this spec to Q33NR for proper workflow:**

1. Move `SPEC-BUILD-PROCESS-TEMPLATE-001.md` from queue to `.deia/hive/coordination/` as briefing material
2. Q33NR should write a briefing for Q33N
3. Q33N should create 6 individual task files (one per wiring task listed above)
4. Q33NR should review task files
5. Q33N should dispatch bees after approval

### Why This Matters

Per Hard Rule 7: **"STAY IN YOUR LANE. Only work on tasks explicitly assigned to you."**

A worker bee executing this full spec would:
- Violate the chain of command
- Skip Q33NR review
- Create untested integration points across 6 subsystems
- Bypass the task breakdown that ensures proper TDD, file size limits, and modular design

### Recommended Task Breakdown (for Q33N)

When Q33N receives this spec, suggested breakdown:

1. **TASK-BPT-001:** Wire DES integration into queue runner (Task 1)
2. **TASK-BPT-002:** Add SMOKE + CATALOG nodes to pipeline.ir.json (Tasks 2-3 combined, closely related)
3. **TASK-BPT-003:** Add HAT node with FileChannel gate (Task 4)
4. **TASK-BPT-004:** Add front-end phases to pipeline.ir.json (Task 5, largest task)
5. **TASK-BPT-005:** Wire EfemeraChannel to DeciderRouter (Task 6)
6. **TASK-BPT-006:** End-to-end IR execution test (verify all nodes work together)

Each task should have:
- Clear file scope
- Test requirements
- Acceptance criteria from parent spec
- Absolute file paths

## Escalation Path

**To Q88N (Dave):**

This spec entered the queue but was dispatched directly to a bee without Q33N task breakdown. The queue runner or dispatcher may need adjustment to:

1. Recognize specs vs tasks (specs have multiple acceptance criteria spanning multiple files)
2. Route specs to Q33NR → Q33N → task breakdown → bee dispatch
3. Reserve direct bee dispatch for single-task files only

**Question for Q88N:** Should specs in `.deia/hive/queue/` automatically trigger Q33NR workflow, or should they be pre-processed into task files before entering the queue?

---

**Summary:** This bee correctly identified a role mismatch and stopped before violating the chain of command. Work requires Q33N coordination. Ready for proper workflow routing.
