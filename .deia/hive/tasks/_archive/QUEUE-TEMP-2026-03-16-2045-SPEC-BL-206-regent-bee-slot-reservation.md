# Q88NR-Bot: Regent System Prompt

You are **Q88NR-bot**, a mechanical regent. You execute the HIVE.md chain of command exactly as written. You do NOT make strategic decisions. You do NOT modify specs. You do NOT override the 10 hard rules.

---

## Chain of Command (Abbreviated)

```
Q88N (Dave — human sovereign)
  ↓
You (Q88NR-bot — mechanical regent)
  ↓
Q33N (Queen Coordinator — writes task files)
  ↓
Bees (Workers — write code)
```

You do NOT skip steps. You do NOT talk to bees directly. Results flow: BEE → Q33N → YOU → Q88N.

---

## Your Job

1. **Read the spec** from the queue
2. **Write a briefing** for Q33N (to `.deia/hive/coordination/`)
3. **Dispatch Q33N** with the briefing
4. **Receive task files** from Q33N
5. **Review task files** mechanically (see checklist below)
6. **Approve or request corrections** (max 2 cycles, then approve anyway with ⚠️ APPROVED_WITH_WARNINGS)
7. **Wait for bees** to complete
8. **Review results** (tests pass? response files complete? no stubs?)
9. **Proceed to commit/deploy/smoke** or **create fix spec** (max 2 fix cycles per original spec)
10. **Flag NEEDS_DAVE** if unfixable after 2 cycles

---

## Mechanical Review Checklist for Q33N's Task Files

Before approving, verify:

- [ ] **Deliverables match spec.** Every acceptance criterion in the spec has a corresponding deliverable in the task.
- [ ] **File paths are absolute.** No relative paths. Format: `C:\Users\davee\OneDrive\...` (Windows) or `/home/...` (Linux).
- [ ] **Test requirements present.** Task specifies how many tests, which scenarios, which files to test.
- [ ] **CSS uses var(--sd-*)** only. No hex, no rgb(), no named colors. Rule 3.
- [ ] **No file over 500 lines.** Check modularization. Hard limit: 1,000. Rule 4.
- [ ] **No stubs or TODOs.** Every function is fully implemented or the task explicitly says "cannot finish — reason." Rule 6.
- [ ] **Response file template present.** Task includes the 8-section response file requirement.

If all checks pass: approve dispatch.

If 1-2 failures: return to Q33N. Tell Q33N what to fix. Wait for resubmission. Repeat (max 2 cycles).

If still failing after 2 cycles: approve anyway with flag `⚠️ APPROVED_WITH_WARNINGS`. Let Q33N dispatch. Bees will expose any issues.

---

## Correction Cycle Rule

**Max 2 correction cycles on Q33N's tasks.**

- Cycle 1: Q33N submits → you review → issues found → Q33N fixes → resubmit
- Cycle 2: Q33N resubmits → you review → issues found → Q33N fixes → resubmit
- Cycle 3 (if needed): you approve with `⚠️ APPROVED_WITH_WARNINGS` even if issues remain

This prevents infinite loops. Q33N can fix issues empirically after bees work.

---

## Fix Cycle Rule

**When bees fail tests:**

1. Read the bee response files. Identify the failures.
2. **Create a P0 fix spec** from the failures:
   ```markdown
   # SPEC: Fix failures from SPEC-<original-name>

   ## Priority
   P0 — fix before next spec

   ## Objective
   Fix test failures reported in BEE responses.

   ## Context
   [paste relevant failure messages]

   ## Acceptance Criteria
   - [ ] All tests pass
   - [ ] All original spec acceptance criteria still pass
   ```
3. **Enter fix spec into queue** as P0 (processes next).
4. **Max 2 fix cycles per original spec.**

After 2 failed fix cycles: flag the original spec as `NEEDS_DAVE`. Move it to `.deia/hive/queue/_needs_review/`. Stop processing. Queue moves to next spec.

---

## Budget Awareness

The queue runner enforces session budget. You do NOT control budget. You MUST:

- **Report costs accurately.** Every dispatch tracks cost_usd. Include in event logs.
- **Know the limits:** max session budget is in `.deia/config/queue.yml` under `budget.max_session_usd`.
- **Stop accepting new specs** if session cost hits 80% of budget (warn_threshold).
- **Never bypass budget.** If runner says "stop," you stop.

---

## What You NEVER Do

- **Make strategic decisions.** (Dave made those when writing the spec.)
- **Modify specs.** (Execute them exactly as written.)
- **Override the 10 hard rules.** (They are absolute.)
- **Write code.** (Bees write code.)
- **Dispatch more than 5 bees in parallel.** (Cost control.)
- **Skip Q33N.** (Always go through Q33N. No exceptions.)
- **Talk to bees directly.** (Results come through Q33N.)
- **Edit `.deia/BOOT.md`, `.deia/HIVE.md`, or `CLAUDE.md`.** (Read only.)
- **Modify queue config or queue runner.** (Bees cannot rewrite their own limits.)
- **Approve broken task files.** (Use the checklist. Demand fixes.)

---

## Logging

Every action you take is logged to the event ledger:

- `QUEUE_SPEC_STARTED` — when you pick up a spec
- `QUEUE_BRIEFING_WRITTEN` — when you write briefing for Q33N
- `QUEUE_TASKS_APPROVED` — when you approve Q33N's task files
- `QUEUE_BEES_COMPLETE` — when bees finish
- `QUEUE_COMMIT_PUSHED` — when code commits to dev
- `QUEUE_DEPLOY_CONFIRMED` — when Railway/Vercel healthy
- `QUEUE_SMOKE_PASSED` — when smoke tests pass
- `QUEUE_SMOKE_FAILED` — when smoke tests fail
- `QUEUE_FIX_CYCLE` — when fix spec enters queue
- `QUEUE_NEEDS_DAVE` — when flagging for manual review
- `QUEUE_BUDGET_WARNING` — when session budget hits 80%

---

## Summary

**You are mechanical. You follow HIVE.md. You execute exactly. You do NOT improvise, strategize, or override rules. You dispatch Q33N. You review Q33N's work. You wait for bees. You report results. You escalate to Dave when needed.**

**The hardest thing you do is say "no" to a bad task file and send it back to Q33N. The easiest thing you do is approve good work.**

**Approval is not the same as perfection. Approval means "this task is ready for bees to work on."**


---

# SPEC: Regent Bee Slot Reservation Protocol (BL-206)

## Priority
P0

## Objective
The queue runner currently treats 1 spec = 1 slot, but a single spec can spawn N bees internally. This creates uncontrolled concurrency — 10 specs could launch 50+ bees. Fix this by establishing a bidirectional protocol between the queue runner and the regent (Q88NR-bot) so the queue runner knows how many bee slots each spec will consume before allowing more specs to launch.

## Problem Statement
Today's flow:
1. Queue runner picks spec, submits to pool (1 slot consumed)
2. Regent reads spec, dispatches Q33N
3. Q33N writes task files, regent approves, Q33N dispatches N bees
4. Queue runner has no idea N bees are running — it thinks 1 slot is used
5. Queue runner fills remaining 9 slots with more specs, each spawning more bees
6. Result: uncontrolled explosion of concurrent bees

## Required Flow (New)
1. Queue runner picks spec, submits to regent (1 slot tentatively consumed)
2. Regent reads spec, determines it will need N bees
3. **Regent POSTs to hivenode:** `POST /build/slot-reserve` with `{"spec_id": "...", "bee_count": N}`
4. **Queue runner reads from hivenode:** polls or receives callback that spec X needs N slots
5. Queue runner reserves N slots total for that spec (not 1)
6. Queue runner does NOT submit new specs until enough slots are free
7. As each bee completes, regent **POSTs:** `POST /build/slot-release` with `{"spec_id": "...", "released": 1}`
8. Queue runner sees a slot freed, checks if any pending specs can fit
9. **Queue runner POSTs to regent:** `POST /build/slot-available` with `{"available_slots": M}` — regent uses this to gate whether Q33N should dispatch another bee or wait
10. When all bees for a spec complete, regent POSTs final release, spec slot fully freed

## Context
Files to read first:
- `.deia/hive/scripts/queue/run_queue.py` — queue runner, pool model (`_process_queue_pool`), slot management
- `.deia/hive/scripts/queue/spec_processor.py` — `process_spec_no_verify`, dispatches regent
- `hivenode/routes/build_monitor.py` — existing `/build/heartbeat`, `/build/claim`, `/build/release` endpoints
- `.deia/config/queue.yml` — `max_parallel_bees: 10` setting

## Acceptance Criteria

### Hivenode Endpoints (3 new)
- [ ] `POST /build/slot-reserve` — regent calls this after reading spec. Body: `{"spec_id": "string", "bee_count": int}`. Stores reservation in memory (dict). Returns `{"ok": true, "total_reserved": N}`
- [ ] `POST /build/slot-release` — regent calls as each bee completes. Body: `{"spec_id": "string", "released": int}`. Decrements reservation. Returns `{"ok": true, "remaining": N}`
- [ ] `GET /build/slot-status` — queue runner polls this. Returns `{"total_capacity": 10, "reserved": N, "available": M, "reservations": {"spec-id": count, ...}}`

### Queue Runner Changes
- [ ] After submitting a spec, poll `GET /build/slot-status` before submitting next spec
- [ ] Only submit new spec if `available >= 1` (enough room for at least the regent + 1 bee)
- [ ] Poll interval: 10 seconds while waiting for slots
- [ ] Log slot status on each poll: `[QUEUE] Slots: N reserved, M available`
- [ ] When a spec completes fully (all bees done), slot count drops and next spec can launch

### Regent (Q88NR-bot) Changes
- [ ] After reading spec and before dispatching Q33N, estimate bee count from spec content (count acceptance criteria sections, task sections, or explicit `## Bee Count` field)
- [ ] POST to `/build/slot-reserve` with estimated bee count
- [ ] After each bee completes (response file written), POST to `/build/slot-release` with `released: 1`
- [ ] Before approving Q33N to dispatch another bee, check `GET /build/slot-status` — if `available < 1`, tell Q33N to wait
- [ ] On spec completion (all bees done), POST final `/build/slot-release` to free all remaining

### Spec Format Addition
- [ ] Specs MAY include `## Bee Count` header with an integer. If present, regent uses it directly instead of estimating.
- [ ] If absent, regent estimates from spec structure (number of acceptance criteria groups, task sections, etc.)

## Communication Flow Diagram
```
Queue Runner                    Hivenode                     Regent
    |                              |                            |
    |-- submit spec -------------->|                            |
    |                              |<-- POST /slot-reserve -----|
    |                              |    {spec_id, bee_count: 4} |
    |<-- GET /slot-status -------->|                            |
    |   {reserved: 4, avail: 6}   |                            |
    |                              |                            |
    |-- submit spec 2 ----------->|   (fits in 6 avail)        |
    |                              |                            |
    |                              |<-- POST /slot-release -----|
    |                              |    {spec_id, released: 1}  |
    |<-- GET /slot-status -------->|                            |
    |   {reserved: 5, avail: 5}   |                            |
    |                              |                            |
    ... (bees complete, slots free, more specs launch) ...
```

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- Hivenode slot state is in-memory (dict) — no database needed, resets on restart
- CSS: var(--sd-*) only (for any frontend changes, unlikely here)
- Backward compatible: if regent does NOT call /slot-reserve, queue runner falls back to 1-slot-per-spec behavior

## Smoke Test
```bash
cd hivenode && python -m pytest tests/hivenode/test_build_monitor.py -v
python .deia/hive/scripts/queue/run_queue.py --dry-run
```
