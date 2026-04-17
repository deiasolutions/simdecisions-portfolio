# BL-203: Split heartbeat into silent liveness ping + state transition log

## Objective
Split the build monitor heartbeat into two signals: a silent liveness ping (frequent, lightweight) and a state transition log (only on status changes).

## Context
Currently heartbeats carry state info on every ping, creating noise. Split into: (1) lightweight liveness ping every N seconds, (2) state transition events only when status actually changes (idle->building, building->done, etc.).

## Files to Read First
- `hivenode/routes/build_monitor.py`
- `tests/hivenode/routes/test_build_monitor_integration.py`
- `.deia/hive/scripts/queue/run_queue.py`

## Deliverables
- [ ] Liveness ping endpoint (lightweight, no state payload)
- [ ] State transition log (only emitted on actual status changes)
- [ ] Queue runner sends both appropriately
- [ ] Tests for both signal types

## Acceptance Criteria
- [ ] Liveness pings are lightweight (< 100 bytes)
- [ ] State transitions only fire on actual changes
- [ ] Build monitor frontend can consume both
- [ ] Tests pass

## Smoke Test
- [ ] `cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter" && python -m pytest tests/hivenode/routes/test_build_monitor_integration.py -v`

## Constraints
- No file over 500 lines
- No stubs

## Model Assignment
haiku

## Priority
P0
