# SPEC: MCP Queue — Integration Testing Suite

## Priority
P1

## Depends On
MCP-QUEUE-01, MCP-QUEUE-02, MCP-QUEUE-03, MCP-QUEUE-04

## Objective
Create comprehensive E2E and integration tests for the MCP queue notification system, verifying the full pipeline from file move -> event -> scheduler/dispatcher reaction.

## Context
Tasks 01-04 built the MCP notification system. This task validates the full integration with realistic scenarios, failure modes, and load testing.

Design doc: `.deia/hive/responses/20260406-MCP-QUEUE-NOTIFICATIONS-DESIGN.md`
Task file: `.deia/hive/tasks/2026-04-06-TASK-MCP-QUEUE-05-integration-testing.md`

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/queue_watcher.py` — watcher (QUEUE-01)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/routes/queue_events.py` — endpoints (QUEUE-02)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/tests/hivenode/scheduler/test_scheduler_mcp_e2e.py` — scheduler E2E pattern (QUEUE-03)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/tests/hivenode/scheduler/test_dispatcher_mcp_e2e.py` — dispatcher E2E pattern (QUEUE-04)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/tasks/2026-04-06-TASK-MCP-QUEUE-05-integration-testing.md` — full task spec with test code

## Acceptance Criteria
- [ ] Full pipeline test: spec queued -> active -> done -> scheduler recalculates
- [ ] Full pipeline test: spec done -> dispatcher frees slot -> backlog dispatch
- [ ] Parallel completions test: 5 specs finish within 1s, all handled
- [ ] Failure mode: MCP server down -> daemons fall back to polling
- [ ] Failure mode: subscriber unreachable -> other subscribers still get events
- [ ] Failure mode: malformed event payload -> logged, no crash
- [ ] Performance: 100 specs moved rapidly -> no event loss
- [ ] Performance: debouncing under load -> no duplicates
- [ ] Latency: p95 < 200ms, p99 < 500ms
- [ ] Test report written with metrics
- [ ] 15+ tests, all passing

## Smoke Test
- [ ] `python -m pytest tests/integration/test_mcp_queue_full_pipeline.py -v`
- [ ] `python -m pytest tests/integration/test_mcp_failure_modes.py -v`
- [ ] `python -m pytest tests/integration/test_mcp_performance.py -v`

## Model Assignment
sonnet

## Constraints
- Use pytest-asyncio for async tests
- Tests must use tmp_path fixtures (reproducible)
- Tests must clean up (stop threads, close sockets)
- Total suite runtime < 5min
- No file over 500 lines
- Response file: `.deia/hive/responses/20260406-TASK-MCP-QUEUE-05-RESPONSE.md`
- Test report: `.deia/hive/responses/20260406-TASK-MCP-QUEUE-05-TEST-REPORT.md`
