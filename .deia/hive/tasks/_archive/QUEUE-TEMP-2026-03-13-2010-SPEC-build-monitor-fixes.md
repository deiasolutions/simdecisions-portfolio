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

# SPEC: Build Monitor UI Fixes + Token/Timing Display

## Priority
P0

## Objective
Fix the build monitor UI layout and add token/timing data to heartbeats and display.

## Context
The build monitor lives at:
- Backend: `hivenode/routes/build_monitor.py` — heartbeat API, SSE stream, in-memory state
- Frontend: `browser/src/apps/buildMonitorAdapter.tsx` — EventSource SSE client, task list + log feed
- Dispatch: `.deia/hive/scripts/dispatch/dispatch.py` — sends heartbeats on dispatch/complete, parses adapter results

Files to read first:
- `browser/src/apps/buildMonitorAdapter.tsx` — current UI (task list left, log right)
- `hivenode/routes/build_monitor.py` — HeartbeatPayload model, BuildState, SSE endpoint
- `.deia/hive/scripts/dispatch/dispatch.py` — send_heartbeat function, result parsing after adapter.send_task()

## Acceptance Criteria

### Layout fixes (buildMonitorAdapter.tsx)
- [ ] Log panel fills ALL remaining width to the right edge of the pane. No wasted space. Left panel is fixed-width, log panel is flex-grow.
- [ ] Log messages do NOT truncate. Full text, word-wrap if needed. No `text-overflow: ellipsis`, no `overflow: hidden` on message text.
- [ ] Each log entry shows the FULL spec name (not truncated) and the FULL message text.
- [ ] Timestamps in log entries show HH:MM:SS only. No date. Use `toLocaleTimeString()` or equivalent.

### Token data (dispatch.py → build_monitor.py → buildMonitorAdapter.tsx)
- [ ] In `dispatch.py`, after `adapter.send_task()` returns, parse `input_tokens` and `output_tokens` from the result/usage dict. Pass both to `send_heartbeat()` on completion.
- [ ] Update `send_heartbeat()` function signature to accept `input_tokens` and `output_tokens` (integers).
- [ ] Update `HeartbeatPayload` in `build_monitor.py` to include `input_tokens: Optional[int]` and `output_tokens: Optional[int]` fields.
- [ ] Update `BuildState.record_heartbeat()` to accumulate `input_tokens` and `output_tokens` per task and in totals.
- [ ] Build monitor header shows running token totals: "12,430↑ 3,210↓" format (↑ = input/up, ↓ = output/down).
- [ ] Each log entry shows tokens if available: "12,430↑ 3,210↓" appended to the message.

### Elapsed time (buildMonitorAdapter.tsx)
- [ ] Each RUNNING task in the left panel shows a live elapsed timer: "RUNNING 4m 32s". Updates every second via setInterval.
- [ ] Timer starts from the task's `first_seen` timestamp.
- [ ] Timer stops when task status changes from "running" to "complete" or "failed".

### Bee completion display
- [ ] When a bee completes, the log entry message includes duration and tokens: "COMPLETE — 7m 14s, 12,430↑ 3,210↓"
- [ ] The left panel task entry for completed tasks also shows duration and tokens in the same format.
- [ ] Duration is calculated from `first_seen` to `last_seen` timestamps.

### Token display format (everywhere)
- [ ] Input tokens displayed as number + ↑ (e.g. "12,430↑")
- [ ] Output tokens displayed as number + ↓ (e.g. "3,210↓")
- [ ] Numbers use comma formatting for thousands (e.g. 12430 → "12,430")
- [ ] Format used consistently in: header totals, log entries, left panel task entries

### CSS
- [ ] All colors use `var(--sd-*)` CSS variables only
- [ ] No hardcoded hex, rgb, or named colors

### Tests
- [ ] 5+ tests for token formatting helper (commas, ↑↓ symbols, zero handling, null handling)
- [ ] 2+ tests for timestamp formatting (HH:MM:SS only)
- [ ] 1+ test for elapsed time formatting (minutes + seconds)
- [ ] All existing build monitor tests still pass

## Smoke Test
- [ ] Load `localhost:5173?egg=monitor` — log panel fills full width
- [ ] Log messages wrap, no truncation
- [ ] Timestamps show HH:MM:SS only
- [ ] Running tasks show live elapsed timer
- [ ] Completed tasks show duration + tokens

## Model Assignment
sonnet

## Constraints
- Do NOT change the heartbeat API contract in a breaking way — add new optional fields only
- Do NOT change the SSE event format — same event types, just richer data in the payload
- Keep buildMonitorAdapter.tsx under 500 lines — extract formatting helpers if needed
