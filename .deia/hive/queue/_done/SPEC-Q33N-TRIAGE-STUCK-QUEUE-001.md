# SPEC-Q33N-TRIAGE-STUCK-QUEUE-001: Root-Cause 18-Hour Queue Stall + Reconcile Divergent Spec

**MODE: EXECUTE**

## Priority
P0

## Model Assignment
sonnet

## Role
queen

## Objective

Root-cause why `QUEUE-TEMP-SPEC-RESEARCH-INVENTORY-RAILWAY-001` ran for 18+ hours with only "Processing..." heartbeats and zero token accounting, and why the `POST /build/cancel` endpoint failed to actually stop it (the task resumed a "running" status minutes after cancellation). Reconcile one divergent spec file that Q33NR flagged during the `_active/` cleanup. Produce a triage report with root cause, prevention recommendations, and reconciliation decision.

**Do not build code. Do not kill claude.exe subprocesses. Do not delete any spec files.**

## Context — What Q33NR Already Did

On 2026-04-10 Q33NR did a startup checklist and found:
- `QUEUE-TEMP-SPEC-RESEARCH-INVENTORY-RAILWAY-001` (sonnet) had been "running" since 2026-04-09 12:52:43 — **18+ hours** of only "Processing..." heartbeats and $0 token accounting
- `.deia/hive/queue/_active/` contained 19 spec files, most with no matching live bee

**Q33NR actions already completed:**
1. Cancelled the stuck task via `POST http://127.0.0.1:8420/build/cancel` — endpoint returned `{"ok": true, "status": "cancelled"}`.
2. Observed that the same task ID resumed "running" status within minutes — **cancel was not effective**; the underlying process kept heartbeating and reset the state. Q88N decided to leave the claude.exe subprocesses alone rather than risk killing the wrong PID.
3. Audited all 19 specs in `_active/` against `monitor-state.json` and classified each.
4. Moved 19/19 specs out of `_active/`:
   - 12 COMPLETED-NOT-MOVED → `_done/`
   - 2 DEAD (status=failed) → `_dead/`
   - 1 rejection-loop artifact → `_needs_review/`
   - 3 duplicates-of-done (content identical to `_done/` copy) → `_needs_review/` with `.duplicate-of-done.md` suffix
   - 1 divergent (content differs from `_done/` copy) → `_needs_review/SPEC-WIKI-101-database-schema-tables.active-divergent.md`
5. `_active/` is now empty of `.md` files. The live queue runner continues to process real work normally.

Scripts used (preserved for audit):
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/scripts/cancel_stuck.py`
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/scripts/audit_active_queue.py`
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/scripts/move_stale_active.py`

**What is left for this Q33N:** the *why* and the *how to prevent it*, plus the WIKI-101 reconciliation.

## Files to Read First

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/BOOT.md`
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/HIVE.md`
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/queue/monitor-state.json` (521KB — use jq or Python to query, do not read full file into context)
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/queue_events.jsonl` — grep for the stuck task_id
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/dispatched.jsonl` — grep for the stuck task_id
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/dispatcher_log.jsonl` — grep for the stuck task_id
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/hivenode/routes/build_monitor.py` — `/cancel`, `/heartbeat`, `/ping` endpoints. Understand the interaction between cancel (sets status=FAILED) and incoming heartbeats (re-set status=RUNNING).
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/scripts/queue/run_queue.py` — the queue runner daemon
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/queue/_needs_review/SPEC-WIKI-101-database-schema-tables.active-divergent.md`
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/queue/_done/SPEC-WIKI-101-database-schema-tables.md`

## Steps

### 1. Find the stuck task's spec

Locate the current resting place of the `QUEUE-TEMP-SPEC-RESEARCH-INVENTORY-RAILWAY-001` spec file. Check `_done/`, `_needs_review/`, `_dead/`, `backlog/`, and root. It may have been re-claimed and moved by the running bee while Q33NR was doing the cleanup — search everywhere.

### 2. Build a timeline

Grep `queue_events.jsonl`, `dispatcher_log.jsonl`, `dispatched.jsonl`, and any raw transcript files under `.deia/hive/responses/` matching `*RESEARCH-INVENTORY-RAILWAY*` for the task_id. Produce a chronological event list from dispatch through cancel attempts through the resumed "running" status.

### 3. Diagnose the stall

Answer these specific questions:
- What was the bee actually doing during the 18 hours? (plan mode? tool-use loop? waiting on file I/O? Claude API retries?)
- Why are token counts zero in `monitor-state.json` for this task? Is token accounting broken, or is the bee genuinely not calling the model?
- Is there a raw transcript? What does the last line say?

### 4. Diagnose the cancel failure

Read `build_monitor.py`'s `cancel_task` handler (line ~676) and `heartbeat` handler (line ~545). Answer:
- Does `cancel_task` do anything to prevent subsequent `heartbeat`/`ping` calls from resetting the status?
- Is there a "cancelled" sentinel state? Or does the state machine only distinguish running/complete/failed/timeout?
- Why did the `last_heartbeat` timestamp advance past the cancel time?
- Does `run_queue.py` watch for externally-set FAILED status and terminate the bee subprocess, or does it only care about its own dispatched bees?

### 5. Prevention recommendations (document only, do not implement)

Based on findings from steps 3-4, recommend 2-4 concrete follow-up specs. Example candidates (only pick ones that actually address observed root causes):
- A "cancelled" sentinel state in `build_monitor.py` that blocks subsequent heartbeat resets
- A wall-time guard in `run_queue.py` that force-terminates bees exceeding N hours
- A zero-progress watchdog that alerts when a task has recorded zero tokens for > N minutes
- A sanity check comparing `last_heartbeat - first_seen` on the `/build/status` response so stuck tasks surface
- A process-tree tracker so `cancel_task` can SIGTERM the right PID

**Do not write these specs or implement them.** Just describe them in one paragraph each with proposed priority.

### 6. Reconcile WIKI-101 divergence

Read both:
- `.deia/hive/queue/_needs_review/SPEC-WIKI-101-database-schema-tables.active-divergent.md` (the copy Q33NR pulled from `_active/`)
- `.deia/hive/queue/_done/SPEC-WIKI-101-database-schema-tables.md` (the authoritative completed copy)

Diff them. Determine:
- Which is newer (check git log if applicable, or mtime, or content clues)
- Are the differences substantive (new requirements, changed scope) or cosmetic (whitespace, reordering)?
- Does the `_done/` version actually cover everything in the divergent version?
- Recommend one of: (a) delete the divergent copy because `_done/` is authoritative and complete, (b) requeue the divergent copy as a new spec because it has unaddressed requirements, (c) escalate to Q33NR because reconciliation needs Q88N input.

**Do not delete or move the file.** Just make the recommendation in the report.

## Deliverables

A single triage report at:
`C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/responses/YYYYMMDD-Q33N-TRIAGE-STUCK-QUEUE-RESPONSE.md`

Using the 8-section response template from BOOT.md. In addition, embed these subsections inside "What Was Done":

- **Stuck spec location** — current path
- **Timeline** — chronological events
- **Stall diagnosis** — what the bee was doing during the 18 hours
- **Cancel-failure diagnosis** — why the cancel endpoint didn't actually stop it
- **Prevention recommendations** — 2-4 concrete follow-up spec ideas with proposed priorities
- **WIKI-101 reconciliation** — diff summary + recommendation

## Acceptance Criteria

- [ ] Stuck task's spec file located and path reported
- [ ] Timeline reconstructed from logs with at least 5 anchoring events
- [ ] Stall diagnosis answers all 3 questions in step 3
- [ ] Cancel-failure diagnosis answers all 4 questions in step 4 with line-number references into `build_monitor.py`
- [ ] 2-4 prevention recommendations documented, each with a proposed priority
- [ ] WIKI-101 diff summarized and a reconciliation recommendation made
- [ ] No code written
- [ ] No bees dispatched
- [ ] No spec files moved, renamed, or deleted by this Q33N
- [ ] No claude.exe processes killed
- [ ] Response file exists at the documented path with all 8 mandatory sections

## Constraints

- Read-only analysis. The file-move portion of the original triage was already done by Q33NR.
- Do NOT implement any of the prevention recommendations — those become separate specs if Q33NR approves them.
- Do NOT attempt to cancel the stuck task again — Q88N has accepted that it will either run to completion or be terminated separately.
- Do NOT call `inventory.py`.
- Do NOT read `monitor-state.json` into full context; it is ~521KB. Use targeted grep or a small Python query.

## Response File

`.deia/hive/responses/YYYYMMDD-Q33N-TRIAGE-STUCK-QUEUE-RESPONSE.md` (use today's date)
