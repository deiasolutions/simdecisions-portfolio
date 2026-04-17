# SPEC: Scheduler Backlog Scanning

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective
Make the scheduler daemon scan `backlog/` for SPEC-*.md files and merge them into the task list alongside workdesk tasks. Currently the scheduler only reads from the hardcoded `TASKS` list in `scheduler_mobile_workdesk.py` (line 553 of `scheduler_daemon.py`). Specs added to `backlog/` are invisible to the scheduler, which means the dispatcher never dispatches them.

## Design Reference
Full design is in `.deia/hive/coordination/2026-04-06-BRIEFING-SCHEDULER-BACKLOG-SCANNING.md`. Read it first.

## Key Files
- `hivenode/scheduler/scheduler_daemon.py` — the daemon (line 553 is the gap)
- `hivenode/scheduler/scheduler_mobile_workdesk.py` — current workdesk (TASKS list, Task dataclass)
- `.deia/hive/scripts/queue/spec_parser.py` — spec file parser (use this, don't reinvent)

## Acceptance Criteria
- [ ] `scan_backlog(backlog_dir)` function reads SPEC-*.md from backlog/, returns list of Task objects
- [ ] `extract_task_id(stem)` handles all filename formats: EST-02, IRD-01, MCP-QUEUE-05, MW-031
- [ ] `_daemon_loop()` rescans backlog on every cycle, merges with workdesk tasks
- [ ] Workdesk tasks take priority over backlog tasks with same task_id
- [ ] Backlog specs use their own Priority field (P0/P1/P2/P3), not lower priority than workdesk
- [ ] Dependencies from `## Depends On` are parsed and fed to the OR-Tools solver
- [ ] Duration estimated from model assignment if not explicit: haiku=3h, sonnet=5h, opus=8h
- [ ] Graceful handling: missing sections, malformed specs, duplicate task IDs
- [ ] Backlog scan completes in <100ms for 100 specs (no LLM calls)
- [ ] 10+ tests covering scanning, ID extraction, merging, dependency resolution
- [ ] Do NOT remove workdesk support — keep it as primary, backlog as supplementary
- [ ] Use spec_parser.py for parsing — do not reinvent

## Smoke Test
```bash
# Create a test spec in backlog/
echo "# SPEC: Test\n## Priority\nP1\n## Model Assignment\nsonnet" > .deia/hive/queue/backlog/SPEC-TEST-99-smoke.md

# Restart scheduler daemon, check schedule.json includes TEST-99
curl -s http://127.0.0.1:8420/build/status | python -c "import sys,json; print(json.loads(sys.stdin.buffer.read().decode('utf-8')))"

# Clean up
rm .deia/hive/queue/backlog/SPEC-TEST-99-smoke.md
```

## Constraints
- No file over 500 lines
- TDD where applicable
- spec_parser.py is the source of truth for parsing
- Do not change spec file format
