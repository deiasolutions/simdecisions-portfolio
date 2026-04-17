# PROPOSAL: Factory Refactor — Scheduler as Gatekeeper, Executor as Machinery

**Date:** 2026-04-07
**From:** Q33NR
**Status:** AWAITING Q88N REVIEW

---

## Problem

Three independent processes (scheduler, queue runner, dispatcher) scan overlapping directories with duplicated logic. The scheduler computes schedules nobody reads. The queue runner independently resolves dependencies and decides dispatch order. The dispatcher watches counts but doesn't consume the schedule. Specs get processed but the architecture is accidental — it works by coincidence, not by design.

## Principle

**Scheduler is the brain. Executor is the machinery.**

One process decides. One process executes. No overlap. No duplicated logic. Once a spec enters `ready/`, it moves through the pipeline like a part on an assembly line — no decisions, no branching, no scanning. Pure execution.

## File Lifecycle

```
backlog/  ──►  ready/  ──►  _active/  ──►  _done/
  │              │             │              │
  │ Scheduler    │  Executor   │  Executor    │
  │ decides      │  picks up   │  runs bee    │  (or _needs_review/)
```

### Scheduler owns: `backlog/ → ready/`

- Scans `backlog/` for `SPEC-*.md`
- Resolves dependencies (checks `_done/`)
- Evaluates priority ordering
- When a spec is cleared: moves the file to `ready/` and adds it to `ready/manifest.json`
- Once moved, the spec leaves `backlog/` — no re-announcement, no tracking state needed

### Executor owns: `ready/ → _active/ → _done/`

- Reads `ready/manifest.json` for dispatch order
- Picks the next unstarted entry
- Moves spec file from `ready/` to `_active/`
- Updates manifest entry status to `active`
- Dispatches bee (Claude Code subprocess)
- On completion: moves spec to `_done/` or `_needs_review/`
- Updates manifest entry status to `done` or `review`
- Sends heartbeats to `/build/heartbeat` during execution (existing behavior)

### Feedback loop

- Scheduler's next scan sees new file in `_done/`
- Recomputes: are any blocked specs in `backlog/` now unblocked?
- If yes: moves them to `ready/`, appends to manifest
- Cycle continues until `backlog/` is empty

---

## Manifest Format

`ready/manifest.json`:

```json
{
  "version": 1,
  "updated_at": "2026-04-07T11:30:00Z",
  "entries": [
    {
      "spec_id": "FLAPPY-002",
      "spec_file": "SPEC-FLAPPY-002-learning-ai.md",
      "model": "sonnet",
      "role": "bee",
      "priority": "P1",
      "queued_at": "2026-04-07T11:30:00Z",
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "result": null
    },
    {
      "spec_id": "EXEC-03",
      "spec_file": "SPEC-EXEC-03-queue-runner-integration.md",
      "model": "sonnet",
      "role": "bee",
      "priority": "P0",
      "queued_at": "2026-04-07T11:30:05Z",
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "result": null
    }
  ]
}
```

**Rules:**
- Scheduler APPENDS entries. Never reorders existing entries. Never removes entries.
- Executor UPDATES status fields (`status`, `started_at`, `completed_at`, `result`). Never adds entries.
- Order in the `entries` array IS the dispatch order. Executor processes top-down, skipping non-pending.
- `status` values: `pending` → `active` → `done` | `review` | `failed`

---

## What Gets Deleted

### From queue runner (`run_queue.py`):
- `load_queue()` calls — no more scanning
- `_deps_satisfied()` — scheduler handles this
- `_is_valid_spec_filename()` — scheduler handles this
- Priority sorting logic — scheduler handles this
- Watch loop with Fibonacci backoff — replaced by manifest polling
- Gate 0 / validation before dispatch — this stays OR moves to scheduler (see open question below)

### From scheduler (`scheduler_daemon.py`):
- "Discovered N new specs" spam — spec physically leaves `backlog/`, nothing to re-discover
- Schedule JSON that nobody reads — replaced by manifest + file movement

### Dispatcher (`dispatch.py` background process):
- Merged into executor. One process, not two.

---

## What Gets Built

### 1. Scheduler additions (`scheduler_daemon.py`)
- `promote_to_ready()`: moves spec file from `backlog/` to `ready/`, appends manifest entry
- `should_promote()`: deps met + not already in ready/active/done
- Manifest writer: atomic JSON writes (write tmp, rename)
- Track `_done/` changes to trigger re-evaluation of blocked specs

### 2. New executor process (`executor.py` — new file, replaces queue runner + dispatcher)
- `run()`: main loop — poll manifest, pick next pending, execute, update
- `execute_spec()`: move to `_active/`, dispatch bee subprocess, wait, move to `_done/`
- Manifest reader/updater: read entries, update status fields
- Heartbeat forwarding to `/build/heartbeat` (existing behavior, moved here)
- Parallel execution: respect `max_parallel_bees` from config — can run N specs simultaneously if manifest has N pending

### 3. `ready/` directory
- New directory in `queue/`
- Contains spec files and `manifest.json`
- Scheduler writes here. Executor reads here.

---

## What Does NOT Change

- Spec file format (YAML frontmatter + markdown body)
- `_done/`, `_needs_review/`, `_active/` directories and their meaning
- `/build/heartbeat` and `/build/status` API endpoints
- Spec parser (`spec_parser.py`) — still used by scheduler to parse specs
- Bee dispatch mechanism (Claude Code subprocess via `dispatch.py`)
- Response file generation (bee writes to `responses/`)
- Build monitor UI

---

## Open Questions

### 1. Where does Gate 0 / spec validation live?

Currently the queue runner validates specs before dispatching. Two options:

**A. Scheduler validates before promoting to `ready/`.** Invalid specs stay in `backlog/` or move to `_needs_review/`. Only validated specs reach `ready/`. Executor never sees bad specs.

**B. Executor validates after picking up.** Spec reaches `ready/` based on deps/priority only. Executor validates before dispatching. Failed validation → `_needs_review/`.

Recommendation: **Option A.** If something is in `ready/`, it is ready. No surprises. The executor is machinery — it doesn't make judgments.

### 2. Max parallel bees

The executor needs to handle parallelism. If `max_parallel_bees = 3` and the manifest has 5 pending specs, the executor should run 3 simultaneously and pick up the next as each completes. This is a loop change, not an architectural one.

### 3. Stale manifest entries

If a spec is `active` but the bee process died (crash, timeout), the executor needs recovery logic. Proposal: if a manifest entry has been `active` for longer than `max_bee_timeout` (from config), the executor marks it `failed` and optionally creates a retry entry.

### 4. Backlog hot-reload

User drops a new spec into `backlog/` mid-run. The scheduler picks it up on next scan (30s), evaluates deps, and if ready, promotes to `ready/` and appends to manifest. The executor sees the new entry on its next poll. No restart needed. This already works by design.

---

## Migration Path

1. Create `ready/` directory
2. Build executor as new file alongside existing queue runner
3. Add `promote_to_ready()` to scheduler
4. Test: scheduler promotes, executor dispatches, end-to-end
5. Once verified: stop old queue runner and dispatcher processes
6. Remove dead code from `run_queue.py` (or archive the file)

No flag day. Old and new can coexist during testing because they watch different directories.

---

## Success Criteria

- [ ] Spec dropped in `backlog/` → scheduler promotes to `ready/` within 30s
- [ ] Executor picks up from manifest and dispatches bee within 10s
- [ ] Bee completes → spec in `_done/` → blocked specs unblock on next scheduler cycle
- [ ] Scheduler logs each spec exactly ONCE (no re-announcement spam)
- [ ] `ready/manifest.json` is the single source of truth for dispatch state
- [ ] Old queue runner and dispatcher processes are stopped
- [ ] Parallel dispatch works (2+ bees running simultaneously)
- [ ] Crashed/timed-out bees are detected and recovered
