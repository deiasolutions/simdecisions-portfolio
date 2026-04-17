# TASK-W1-B: Queue runner slot polling and gating

## Objective
Modify the queue runner to poll hivenode's `/build/slot-status` endpoint BEFORE submitting each spec, and only submit if `available >= 1`. This prevents the queue runner from launching unlimited bees.

## Context
The queue runner currently uses a pool model (see `_process_queue_pool` in `run_queue.py`). It backfills slots as bees complete, but it treats 1 spec = 1 slot. Internally, a spec can spawn N bees (via regent → Q33N → N bees), creating uncontrolled concurrency.

After TASK-W1-A, hivenode exposes `/build/slot-status` which reports:
- `total_capacity: 10` (from `queue.yml`)
- `reserved: N` (slots reserved by regent via `/slot-reserve`)
- `available: M` (capacity - reserved)
- `reservations: {"spec-id": count, ...}`

The queue runner must poll this endpoint BEFORE submitting a new spec. If `available < 1`, wait 10 seconds and poll again. Only submit when slots free up.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` — queue runner, `_process_queue_pool` function (line 338)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` — slot-status endpoint (added by TASK-W1-A)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\queue.yml` — `max_parallel_bees: 10`

## Deliverables

### 1. Add `httpx` dependency to queue runner
- [ ] Import `httpx` at the top of `run_queue.py`
- [ ] Add helper function `_get_hivenode_url() -> str` — returns `http://localhost:8000` (hardcode for now, can be config later)

### 2. Add slot polling function
- [ ] `_poll_slot_status() -> dict | None`
  - Call `GET http://localhost:8000/build/slot-status`
  - Return JSON response if successful
  - Return `None` on error (HTTP error, connection error, timeout)
  - Use 5-second timeout
  - Log errors but don't crash

### 3. Modify `_process_queue_pool` to poll before submitting each spec
- [ ] After each spec completes (line ~495, before backfill), poll slot status
- [ ] If `available < 1`, enter a wait loop:
  - Log: `"[QUEUE] Slots full (reserved: N, available: 0). Waiting..."`
  - Sleep 10 seconds
  - Poll again
  - Repeat until `available >= 1` OR session budget exhausted
- [ ] If `available >= 1`, proceed with backfill (submit next spec)
- [ ] Log slot status on each poll: `"[QUEUE] Slot status: reserved=N, available=M"`

### 4. Graceful fallback if hivenode is unreachable
- [ ] If `_poll_slot_status()` returns `None` (hivenode down or not responding), fall back to default behavior:
  - Assume 1 slot per spec (current behavior)
  - Log: `"[QUEUE] Hivenode unreachable, falling back to 1-slot-per-spec"`
  - Do NOT block the queue

### 5. Initial slot check before starting pool
- [ ] Before entering `_process_queue_pool`, poll slot status ONCE
- [ ] If `available < 1` at start, log: `"[QUEUE] All slots reserved at start. Waiting for free slots..."`
- [ ] Wait loop (same as above) before launching first spec

## Test Requirements

Write tests FIRST (TDD). Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\queue\test_slot_polling.py`

### Minimum 10 tests:
- [ ] `_poll_slot_status()` returns dict with `total_capacity`, `reserved`, `available`, `reservations`
- [ ] `_poll_slot_status()` returns `None` on HTTP error (mock httpx to raise exception)
- [ ] `_poll_slot_status()` returns `None` on timeout (mock httpx to timeout)
- [ ] Queue runner submits spec if `available >= 1`
- [ ] Queue runner waits if `available < 1`, polls again after 10 seconds
- [ ] Queue runner falls back to default behavior if hivenode unreachable
- [ ] Queue runner logs slot status on each poll
- [ ] Queue runner breaks wait loop if session budget exhausted
- [ ] Queue runner handles `available = 0` at start (waits before launching first spec)
- [ ] Queue runner handles `available = -5` (oversubscribed) — waits until positive

## Constraints
- No file over 500 lines — `run_queue.py` is currently 944 lines, approaching the 1,000 hard limit. Do NOT add more than 100 lines. If necessary, extract helper functions to a separate file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\slot_poller.py`
- TDD: tests first
- No stubs
- Graceful fallback: if hivenode is down, queue runner proceeds with default behavior (1-slot-per-spec)
- Log all slot polling events (reserved count, available count)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-W1-B-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Model Assignment
**Haiku** — straightforward polling logic.

## Success Criteria
- All 10+ tests pass
- Queue runner polls hivenode before submitting each spec
- Queue runner waits if `available < 1`, proceeds when slots free
- Queue runner falls back gracefully if hivenode is unreachable
- All polling events logged
- No file exceeds 500 lines
