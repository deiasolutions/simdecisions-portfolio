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
