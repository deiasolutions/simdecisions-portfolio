# PROPOSAL: Directory-Based State Machine for Queue Runner

**Author:** Q33NR
**Date:** 2026-03-16
**Status:** AWAITING Q88N APPROVAL

---

## Problem

The queue runner has no visibility into in-flight work. When the process dies (crash, context loss, machine reboot), specs that were being processed disappear into a void — no record they were started, no cleanup of partial work, no automatic recovery. The current system tracks state in `monitor-state.json` (volatile) and directory placement (`_done/`, `_needs_review/`) but has a gap between "picked up" and "finished."

Additionally, priority ordering uses fractional floats (P0.05, P1.25) that conflict with the categorical system (P0–P3) used by the inventory/backlog. Dependencies between specs are implicit (controlled by feeder drip rate) rather than declared.

## Solution

**The filesystem IS the state machine.** A spec's directory is its state. No JSON tracking, no marker files, no external databases. `ls` any folder and you see exactly what's in that stage.

---

## Directory Layout

```
.deia/hive/queue/
├── *.md              ← PENDING: eligible for pickup (sorted by priority, then FIFO)
├── _hold/            ← HELD: not yet released (human gate, e.g. Wave 3 waiting)
├── _active/          ← IN-FLIGHT: bee is currently working on this spec
├── _done/            ← COMPLETED: bee returned CLEAN, tests passed
├── _failed/          ← FAILED: bee returned error, timeout, or process died mid-run
├── _needs_review/    ← BLOCKED: needs human decision (regressions, ambiguous failures)
└── _dead/            ← CANCELLED: permanently removed from pipeline
```

## State Transitions

```
                    ┌──────────────────────────────────────────────┐
                    │                                              │
  _hold/ ──────→ queue/ ──────→ _active/ ──────→ _done/           │
  (human)        (eligible)    (bee working)    (success)          │
                    ▲                │                              │
                    │                ├──────────→ _failed/ ────────┘
                    │                │            (retry eligible)
                    │                │                │
                    │                │                ├──→ _dead/
                    │                │                │    (max retries)
                    │                │                │
                    │                │                └──→ _needs_review/
                    │                │                     (human decision)
                    │                │
                    │                └──────────→ _needs_review/
                    │                             (regression detected)
                    │
                    └─── fix spec generated (new file in queue/)
```

## Transition Rules

### 1. _hold/ → queue/ (Wave Release)
- **Trigger:** Human moves files manually, or a release command
- **Who:** Q88N or Q33NR
- **Rule:** Files in `_hold/` are never touched by the queue runner

### 2. queue/ → _active/ (Pickup)
- **Trigger:** Queue runner selects next eligible spec
- **Who:** Queue runner (automatic)
- **Eligibility check (in order):**
  1. Priority: P0 before P1 before P2 before P3 (integer only)
  2. Dependencies: all items in `## Depends On` must have matching filenames in `_done/`
  3. Hold: `## Hold` timestamp must be in the past (or absent)
  4. FIFO: among equal priority + satisfied deps, earliest `added_at` wins
- **Action:** `spec.path.rename(queue_dir / "_active" / spec.path.name)`
- **Logging:** `[QUEUE] PICKUP: spec-name.md → _active/ (P1, slot 2/5)`

### 3. _active/ → _done/ (Success)
- **Trigger:** Bee returns status CLEAN
- **Who:** Queue runner (automatic)
- **Action:** Move spec to `_done/`
- **Side effects:**
  - Re-check `_failed/` and `queue/` for specs whose dependencies are now satisfied
  - Log completion event to session events
  - Release all file claims for this spec

### 4. _active/ → _failed/ (Failure)
- **Trigger:** Bee returns NEEDS_DAVE, TIMEOUT, or pool exception
- **Who:** Queue runner (automatic)
- **Action:** Move spec to `_failed/`, generate fix spec in `queue/` if retries remain
- **Metadata:** Append failure reason to spec file as `## Failure Log` section:
  ```markdown
  ## Failure Log
  - 2026-03-16T14:30:00 | TIMEOUT | Attempt 1/2 | Fix spec: SPEC-fix-foo.md
  - 2026-03-16T14:45:00 | NEEDS_DAVE | Attempt 2/2 | Max retries exhausted
  ```
- **Retry logic:**
  - Attempt < max_fix_cycles → generate fix spec in `queue/`, original stays in `_failed/`
  - Attempt >= max_fix_cycles → stays in `_failed/`, event logged as NEEDS_DAVE
  - Regression detected → move to `_needs_review/` (human must decide)

### 5. _active/ → queue/ (Crash Recovery)
- **Trigger:** Queue runner starts up and finds orphans in `_active/`
- **Who:** Queue runner (automatic, on startup)
- **Action:** For each file in `_active/`:
  - Check if it has a `## Failure Log` with prior attempts
  - If retries remain: move back to `queue/` for re-pickup
  - If max retries exhausted: move to `_needs_review/`
- **Logging:** `[QUEUE] RECOVERY: spec-name.md was in-flight, moved back to queue/`

### 6. _failed/ → _dead/ (Give Up)
- **Trigger:** Human decision, or automatic after max retries with no fix spec possible
- **Who:** Q88N or Q33NR (manual), or queue runner (automatic max-retry)
- **Action:** Move to `_dead/`. No further processing.

### 7. _failed/ → _needs_review/ (Human Required)
- **Trigger:** Regression detected, ambiguous failure, or spec needs redesign
- **Who:** Queue runner (automatic on regression), or human
- **Action:** Move to `_needs_review/`. Human reviews and either:
  - Moves back to `queue/` (retry with edits)
  - Moves to `_dead/` (abandon)
  - Writes new spec in `queue/` (redesign)

---

## Priority System (Simplified)

| Priority | Meaning | Use Case |
|----------|---------|----------|
| **P0** | Emergency | Hotfixes, blockers, broken production |
| **P1** | Current wave | Normal work items in the active wave |
| **P2** | Next wave | Queued but not urgent |
| **P3** | Backlog | Do when idle, nice-to-have |

- **Integer only.** P0, P1, P2, P3. No fractional values.
- **Existing fractional specs are floored:** P0.05 → P0, P1.25 → P1.
- **Within a priority tier:** FIFO by file modification time.
- **Matches inventory/backlog system** — no conversion needed for archival.

## Dependency System

Specs declare dependencies via a `## Depends On` section:

```markdown
## Depends On
- w2-04-flow-des-wire
- w2-05-des-canvas-visual
```

- Queue runner checks: for each dep ID, does any filename in `_done/` contain that ID as a substring?
- All deps satisfied → eligible for pickup
- Any dep unsatisfied → blocked (stays in `queue/`, logged as BLOCKED)
- After each completion, re-scan blocked specs for newly eligible items

**This replaces the feeder's ordering logic.** Instead of drip-feeding one at a time, dump an entire wave into `queue/` with deps declared. The runner sorts it out.

---

## Code Changes Required

### spec_parser.py (DONE)
- [x] `depends_on: list[str]` field on SpecFile
- [x] Parse `## Depends On` section
- [x] Priority coercion: float → int (floor)

### run_queue.py
- [x] `_get_done_ids()` — scan `_done/` for completed spec IDs
- [x] `_deps_satisfied()` — check all deps met
- [x] Filter blocked specs in `_process_queue_pool()`
- [x] Re-check blocked specs after each completion (UNBLOCK logic)
- [ ] **NEW: Move spec to `_active/` before dispatching bee**
- [ ] **NEW: Move from `_active/` to `_done/` or `_failed/` on result**
- [ ] **NEW: Startup recovery — scan `_active/` for orphans**
- [ ] **NEW: Append `## Failure Log` to failed specs**

### Tests (DONE + TODO)
- [x] 24 tests for priority coercion, dep parsing, dep satisfaction, sort order
- [ ] **NEW: Tests for _active/ transition (pickup, success, failure)**
- [ ] **NEW: Tests for crash recovery (orphan detection, retry logic)**
- [ ] **NEW: Tests for failure log appending**

---

## DES Modeling Compatibility

This directory-based state machine maps directly to a DES flow model:

| Directory | DES Primitive | Role |
|-----------|---------------|------|
| `_hold/` | Source node (gated) | Work enters system when released |
| `queue/` | FIFO queue | Waiting for available worker |
| `_active/` | Activity node | Being serviced (bee processing) |
| `_done/` | Sink node | Exits system successfully |
| `_failed/` | Decision node | Branch: retry, review, or dead |
| `_needs_review/` | Queue (human resource) | Waiting for human capacity |
| `_dead/` | Sink node | Exits system permanently |

**Resources:**
- Bee pool: capacity = max_parallel (currently 5)
- Human reviewer: capacity = 1 (Q88N)

**Measurable metrics:**
- Cycle time: `_active/` entry → `_done/` entry (per spec)
- Throughput: specs moved to `_done/` per hour
- WIP: count of files in `_active/`
- Queue depth: count of files in `queue/`
- Failure rate: `_failed/` count / total processed
- Recovery rate: orphans recovered / orphans detected

All observable by counting files in directories. No database query needed.

---

## Migration

1. Create `_active/` directory (doesn't exist yet)
2. `_failed/` directory (doesn't exist yet — failures currently go to `_needs_review/`)
3. Existing specs in `queue/`, `_done/`, `_hold/`, `_dead/`, `_needs_review/` stay as-is
4. No data migration — new behavior only affects future processing
5. Fractional priorities in existing specs automatically floor to integer on next parse

---

## Estimated Scope

- **spec_parser.py:** Done (dependency + priority changes committed)
- **run_queue.py:** ~50 lines for directory transitions + ~30 lines for crash recovery
- **Tests:** ~15 new tests for transitions and recovery
- **Total:** Small. The state machine is simple because the filesystem does the work.
