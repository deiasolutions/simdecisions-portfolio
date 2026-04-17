# TASK-QUEUE-TRIAGE-001 — Triage Failed/Stalled Specs and Requeue

**Priority:** P0
**Model:** Sonnet
**Role:** Q33N
**Type:** Triage + Fix — get specs back into scheduler
**Date:** 2026-04-08

---

## Objective

Scan ALL queue directories for specs that fell out of the pipeline — failed, stalled, stuck in _needs_review, or sitting in _active with no bee running. Fix them and get them back into backlog so the scheduler can pick them up.

---

## Steps

### 1. Scan Every Queue Directory

Check ALL of these:
- `.deia/hive/queue/_needs_review/` — specs that failed and need fixing
- `.deia/hive/queue/_active/` — specs that may be stuck (no bee running)
- `.deia/hive/queue/_dead/` — specs that died
- `.deia/hive/queue/_stage/` — specs that were staged but never queued
- `.deia/hive/queue/` (root) — any orphaned specs

For each spec found, report: spec ID, title, why it's there, when it last moved.

### 2. Check for Missing Response Files

For each spec in _done/, verify a response file exists in `.deia/hive/responses/`. If a spec is marked done but has no response and no code deliverables, it didn't actually complete — flag it.

### 3. Read the Failure Evidence

For each failed/stalled spec:
- Read the spec itself
- Read the raw transcript if one exists (`.deia/hive/responses/*RAW*`)
- Check `queue_events.jsonl` for timeline
- Determine root cause (plan mode? missing file? crash? timeout?)

### 4. Fix and Requeue

For each fixable spec:
- Apply the fix (update file refs, add EXECUTE directive, fix dependencies, etc.)
- Move the fixed spec to `.deia/hive/queue/backlog/`
- Document what you changed and why

For specs that CAN'T be fixed (obsolete, superseded, duplicate):
- Move to `.deia/hive/queue/_archive/` or delete
- Document why

### 5. Check monitor-state.json

Read `.deia/hive/queue/monitor-state.json` — is anything stuck in "claimed" state with no active bee? Clear stale claims if needed.

---

## Deliverables

1. Triage report at `.deia/hive/responses/20260408-QUEUE-TRIAGE-RESPONSE.md`
2. All fixable specs moved to `backlog/` with fixes applied
3. Unfixable specs archived or deleted with explanation

---

## Constraints

- Do NOT build code. Fix specs and move files only.
- Every fixed spec MUST have an explicit "EXECUTE mode" directive.
- Every fixed spec MUST have valid file references in "Files to Read First".
- Verify file references actually exist on disk before requeuing.

---

## Response Location

`.deia/hive/responses/20260408-QUEUE-TRIAGE-RESPONSE.md`
