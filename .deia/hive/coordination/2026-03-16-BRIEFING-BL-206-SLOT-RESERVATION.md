# Briefing: BL-206 — Regent Bee Slot Reservation Protocol

**Date:** 2026-03-16
**Priority:** P0
**From:** Q88NR
**To:** Q33N

## Objective

Implement a bidirectional slot reservation protocol between the queue runner and regent (Q88NR-bot) so the queue runner can track how many bee slots each spec will consume BEFORE allowing more specs to launch. This prevents uncontrolled concurrency explosions.

## Problem

Today's queue runner treats 1 spec = 1 slot, but internally a spec can spawn N bees. This creates a race condition where 10 specs can launch 50+ bees uncontrollably.

**Current flow (broken):**
1. Queue runner picks spec → 1 slot consumed
2. Regent dispatches Q33N → Q33N dispatches N bees
3. Queue runner has no idea N bees are running
4. Queue runner fills remaining 9 slots → more specs → more bees
5. Result: 50+ concurrent bees, resource exhaustion

**Required flow (new):**
1. Queue runner picks spec → 1 slot tentatively consumed
2. Regent reads spec → determines needs N bees
3. **Regent calls hivenode:** `POST /build/slot-reserve` with `bee_count: N`
4. **Queue runner polls hivenode:** `GET /build/slot-status` → sees N slots reserved
5. Queue runner does NOT submit new specs until enough slots free
6. As each bee completes → regent calls `POST /build/slot-release` with `released: 1`
7. Queue runner sees freed slot → can submit next spec if slots available
8. When all bees done → regent releases all remaining slots

## Context

### Files to Read First

**Queue runner (Python):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` — queue runner, pool model (`_process_queue_pool`), slot management
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py` — `process_spec_no_verify`, dispatches regent

**Hivenode (Python):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` — existing `/build/heartbeat`, `/build/claim`, `/build/release` endpoints (extend this)

**Config:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\queue.yml` — `max_parallel_bees: 10` setting

### Key Constraints from Spec

1. Max 500 lines per file
2. TDD: tests first
3. No stubs
4. Hivenode slot state is **in-memory (dict)** — no database, resets on restart
5. Backward compatible: if regent does NOT call `/slot-reserve`, queue runner defaults to 1-slot-per-spec

### Components to Build

**Hivenode (3 new endpoints):**
- `POST /build/slot-reserve` — regent calls after reading spec. Body: `{"spec_id": "string", "bee_count": int}`. Returns `{"ok": true, "total_reserved": N}`
- `POST /build/slot-release` — regent calls as each bee completes. Body: `{"spec_id": "string", "released": int}`. Returns `{"ok": true, "remaining": N}`
- `GET /build/slot-status` — queue runner polls. Returns `{"total_capacity": 10, "reserved": N, "available": M, "reservations": {"spec-id": count, ...}}`

**Queue Runner (run_queue.py changes):**
- After submitting spec, poll `GET /build/slot-status` before submitting next
- Only submit if `available >= 1`
- Poll interval: 10 seconds while waiting
- Log slot status on each poll

**Regent (Q88NR-bot changes):**
- After reading spec, estimate bee count (count acceptance criteria sections OR read `## Bee Count` header if present)
- POST to `/build/slot-reserve` with estimated count
- After each bee completes (response file written), POST to `/build/slot-release` with `released: 1`
- Before approving Q33N to dispatch another bee, check `GET /build/slot-status` — if `available < 1`, tell Q33N to wait
- On spec completion (all bees done), POST final `/build/slot-release` to free remaining

**Spec format addition:**
- Specs MAY include `## Bee Count` header with an integer
- If present, regent uses it directly
- If absent, regent estimates from structure (count acceptance criteria groups, task sections, etc.)

## Deliverables

Q33N will write task files for:

1. **TASK-A: Hivenode slot reservation endpoints** (backend, TDD)
   - 3 new routes in `build_monitor.py` (or new file if `build_monitor.py` approaches 500 lines)
   - In-memory dict to track reservations: `{"spec-id": count}`
   - Tests for reserve, release, status endpoints (edge cases: double reserve, release more than reserved, etc.)

2. **TASK-B: Queue runner slot polling** (Python, TDD)
   - Modify `run_queue.py` to poll `/build/slot-status` after each spec submission
   - Only submit next spec if `available >= 1`
   - Log slot status on each poll
   - Tests for slot-aware queue behavior (mock HTTP calls)

3. **TASK-C: Regent slot estimation and reservation** (this is a SYSTEM PROMPT update for Q88NR-bot, NOT code)
   - Q33N will write a PROCESS DOC (`.deia/processes/P-XX-SLOT-RESERVATION.md`) detailing:
     - How regent estimates bee count from spec
     - When to call `/slot-reserve`
     - When to call `/slot-release`
     - How to check `/slot-status` before approving Q33N to dispatch next bee
   - This is NOT a code task — it's a workflow/instruction doc for future Q88NR sessions

4. **TASK-D: Integration smoke test** (end-to-end test)
   - Test that queue runner + hivenode + regent protocol work together
   - Scenario: 3 specs in queue, first spec needs 8 bees, queue runner waits for slots to free before launching second spec
   - Can be a manual test script or automated E2E test

## Test Requirements

- **Hivenode endpoints:** 15+ tests (reserve, release, status, edge cases)
- **Queue runner:** 10+ tests (slot polling, submission gating, fallback to 1-slot-per-spec)
- **Integration:** 1+ smoke test (manual or automated)

## Constraints

- No file over 500 lines
- TDD: tests first
- No stubs
- Hivenode slot state is in-memory (no DB dependency)
- Backward compatible: queue runner falls back to 1-slot-per-spec if `/slot-reserve` not called

## Model Assignment

- **TASK-A (hivenode endpoints):** Haiku (straightforward HTTP routes)
- **TASK-B (queue runner polling):** Haiku (straightforward polling logic)
- **TASK-C (process doc):** Sonnet (requires understanding regent workflow, writing clear instructions)
- **TASK-D (integration test):** Haiku (execute test scenario)

## Success Criteria

- All hivenode tests pass
- All queue runner tests pass
- Integration smoke test passes
- Queue runner no longer launches unlimited bees
- Regent can control bee dispatch by checking slot availability

## Notes for Q33N

- This is infrastructure work — no UI changes
- Hivenode slot state is ephemeral (in-memory) — this is intentional
- Queue runner must gracefully handle hivenode restart (slot state resets → queue runner sees 10 available slots, proceeds)
- Regent workflow doc (TASK-C) is CRITICAL — future Q88NR sessions will read this to know how to use the protocol
