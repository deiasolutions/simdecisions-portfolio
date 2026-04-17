# BL-056: Automated overnight build pipeline improvements

## Objective
Improve the automated build pipeline so it can run overnight unattended, processing queued specs, dispatching bees, and reporting results.

## Context
The queue runner in .deia/hive/scripts/queue/ handles spec processing and bee dispatch. It needs reliability improvements: better error recovery, stale process detection, result aggregation, and morning report generation.

## Files to Read First
- `.deia/hive/scripts/queue/run_queue.py`
- `.deia/hive/scripts/queue/spec_processor.py`
- `.deia/hive/scripts/queue/spec_parser.py`
- `.deia/hive/scripts/queue/morning_report.py`
- `.deia/config/queue.yml`

## Deliverables
- [ ] Error recovery: retry failed dispatches with backoff
- [ ] Stale process detection: kill bees that exceed timeout
- [ ] Result aggregation: collect all response files per batch
- [ ] Morning report: summary of overnight results
- [ ] Tests for error recovery and stale detection

## Acceptance Criteria
- [ ] Failed dispatches retry up to 3 times with backoff
- [ ] Stale bees killed after timeout
- [ ] Morning report generated with pass/fail summary
- [ ] Tests pass

## Smoke Test
- [ ] `cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter" && python -m pytest .deia/hive/scripts/queue/tests/ -v`

## Constraints
- No file over 500 lines
- No stubs

## Model Assignment
sonnet

## Priority
P0
