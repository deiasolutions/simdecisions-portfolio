# BL-206: Regent must report expected bee count to hivenode so queue runner reserves slots

## Objective
Add slot reservation so the regent (Q33N) reports how many bees it expects to dispatch, and the queue runner reserves those slots to prevent oversubscription.

## Context
When Q33N dispatches multiple bees, the queue runner doesn't know how many to expect and may oversubscribe. The regent should report expected_bees count, and the queue runner should reserve slots accordingly.

## Files to Read First
- `.deia/hive/scripts/queue/run_queue.py`
- `.deia/hive/scripts/queue/spec_processor.py`
- `.deia/config/queue.yml`
- `hivenode/routes/build_monitor.py`

## Deliverables
- [ ] Regent reports expected_bees count via API or coordination file
- [ ] Queue runner reads expected count and reserves slots
- [ ] Slot reservation prevents other specs from claiming reserved slots
- [ ] Release reserved slots when bees complete or timeout
- [ ] Tests for reservation and release

## Acceptance Criteria
- [ ] Regent can report expected bee count
- [ ] Queue runner reserves N slots for a batch
- [ ] Reserved slots are released on completion/timeout
- [ ] Tests pass

## Smoke Test
- [ ] `cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter" && python -m pytest .deia/hive/scripts/queue/tests/ -v`

## Constraints
- No file over 500 lines
- No stubs

## Depends On
- BL203 (heartbeat must be split before adding reservation signals)

## Model Assignment
haiku

## Priority
P0
