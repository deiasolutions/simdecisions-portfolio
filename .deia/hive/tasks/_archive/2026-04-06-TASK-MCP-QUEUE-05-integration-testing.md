# TASK-MCP-QUEUE-05: Integration Testing Suite

## Objective

Create comprehensive E2E and integration tests for the MCP queue notification system, verifying the full pipeline from file move → event → scheduler/dispatcher reaction.

## Context

Tasks 01-04 built the MCP notification system. This task validates the full integration with realistic scenarios, failure modes, and load testing.

**Design:** `.deia/hive/responses/20260406-MCP-QUEUE-NOTIFICATIONS-DESIGN.md` (section: Testing & Documentation)

## Files to Read First

- `tests/scheduler/test_scheduler_mcp_e2e.py` (created by TASK-MCP-QUEUE-03)
  - Scheduler E2E test pattern
- `tests/scheduler/test_dispatcher_mcp_e2e.py` (created by TASK-MCP-QUEUE-04)
  - Dispatcher E2E test pattern
- `hivenode/queue_watcher.py` (created by TASK-MCP-QUEUE-01)
  - Watcher implementation to test

## Deliverables

- [ ] `tests/integration/test_mcp_queue_full_pipeline.py` — Full pipeline tests
  - Test 1: Spec queued → active → done → scheduler recalculates
  - Test 2: Spec done → dispatcher frees slot → moves from backlog
  - Test 3: Parallel completions (5 specs finish within 1s) → all handled correctly
  - Test 4: Rapid moves (queue → active → done within 500ms) → debouncing works
- [ ] `tests/integration/test_mcp_failure_modes.py` — Failure mode tests
  - Test 1: MCP server down on startup → daemons fall back to polling
  - Test 2: Network timeout (subscriber unreachable) → other subscribers still get events
  - Test 3: Malformed event payload → logged, no crash
  - Test 4: Subscriber returns 500 error → logged, retry not attempted
  - Test 5: Watcher thread crash → restart on next file event
- [ ] `tests/integration/test_mcp_performance.py` — Performance tests
  - Test 1: 100 specs moved rapidly → no event loss
  - Test 2: Debouncing under load → no duplicates
  - Test 3: Latency measurement → events delivered <100ms avg
  - Test 4: Memory leak check → no unbounded growth in event cache
- [ ] Test report: `.deia/hive/responses/20260406-TASK-MCP-QUEUE-05-TEST-REPORT.md`
  - Summary of all tests (pass/fail)
  - Performance metrics (latency p50/p95/p99)
  - Failure mode verification
  - Recommendations for production deployment

## Test Requirements

- [ ] All tests pass
- [ ] Edge cases covered:
  - MCP server crash mid-operation
  - Event storm (1000 events/sec)
  - Scheduler/dispatcher crash and restart (state recovery)
  - File moved outside watched directories (ignored)

## Acceptance Criteria

- [ ] Full pipeline test verifies end-to-end flow (spec → event → reaction)
- [ ] Failure mode tests verify graceful degradation
- [ ] Performance tests verify no event loss under load (100 specs)
- [ ] Debouncing prevents duplicates (verified under load)
- [ ] Latency measurement: p95 < 200ms, p99 < 500ms
- [ ] No memory leaks (event cache bounded, old entries purged)
- [ ] Test report written with metrics and recommendations
- [ ] All tests: 15+ tests, all passing
- [ ] Test coverage: ≥80% for new code (watcher, MCP endpoints, daemon event handlers)

## Implementation Notes

### Full Pipeline Test Structure

```python
@pytest.mark.integration
async def test_full_pipeline_spec_completion():
    """Test: spec queued → active → done → scheduler recalculates."""
    # Setup
    queue_dir = tmp_path / ".deia/hive/queue"
    queue_dir.mkdir(parents=True)

    # Start services
    watcher = start_watcher(queue_dir)
    scheduler = start_scheduler_daemon(mcp_enabled=True)
    dispatcher = start_dispatcher_daemon(mcp_enabled=True)

    # Create spec in queue/
    spec_path = queue_dir / "SPEC-TEST-001-test-spec.md"
    spec_path.write_text("# Test Spec\n**Priority:** P1")

    # Wait for event
    await asyncio.sleep(0.5)

    # Move to _active/
    active_dir = queue_dir / "_active"
    active_dir.mkdir(exist_ok=True)
    shutil.move(spec_path, active_dir / spec_path.name)

    await asyncio.sleep(0.5)

    # Move to _done/
    done_dir = queue_dir / "_done"
    done_dir.mkdir(exist_ok=True)
    shutil.move(active_dir / spec_path.name, done_dir / spec_path.name)

    # Wait for scheduler to recalculate
    await asyncio.sleep(2)

    # Verify schedule.json updated
    schedule_path = queue_dir.parent / "schedule.json"
    assert schedule_path.exists()

    schedule = json.loads(schedule_path.read_text())
    assert "computed_at" in schedule

    # Verify latency <2s (computed_at timestamp vs file move timestamp)
    computed_time = datetime.fromisoformat(schedule["computed_at"].replace("Z", "+00:00"))
    file_move_time = datetime.fromtimestamp(
        (done_dir / spec_path.name).stat().st_mtime,
        tz=timezone.utc
    )
    latency = (computed_time - file_move_time).total_seconds()
    assert latency < 2.0, f"Latency too high: {latency}s"

    # Cleanup
    stop_services(watcher, scheduler, dispatcher)
```

### Failure Mode Test Structure

```python
@pytest.mark.integration
async def test_mcp_server_down_fallback():
    """Test: MCP server down → daemons fall back to polling."""
    # Start scheduler with MCP server port blocked
    with patch('socket.socket') as mock_socket:
        mock_socket.side_effect = OSError("Address already in use")

        scheduler = SchedulerDaemon(
            tasks=[], min_bees=5, max_bees=10,
            schedule_dir=tmp_path, queue_dir=tmp_path / "queue",
            mcp_enabled=True
        )
        scheduler.start()

        # Verify MCP disabled after failure
        assert scheduler.mcp_enabled == False

        # Verify fallback polling works
        await asyncio.sleep(65)  # Wait for fallback poll
        assert scheduler.velocity > 0  # Schedule computed via poll
```

### Performance Test Structure

```python
@pytest.mark.integration
async def test_performance_100_specs_no_loss():
    """Test: 100 specs moved rapidly → no event loss."""
    queue_dir = tmp_path / ".deia/hive/queue"
    done_dir = queue_dir / "_done"
    done_dir.mkdir(parents=True)

    watcher = start_watcher(queue_dir)
    event_log = queue_dir.parent / "queue_events.jsonl"

    # Create and move 100 specs
    start_time = time.time()
    for i in range(100):
        spec_path = done_dir / f"SPEC-PERF-{i:03d}-test.md"
        spec_path.write_text(f"# Spec {i}")

    # Wait for events to settle
    await asyncio.sleep(5)

    # Count events in log
    events = [json.loads(line) for line in event_log.read_text().splitlines()]
    done_events = [e for e in events if e["event"] == "queue.spec_done"]

    # Verify all 100 specs logged
    assert len(done_events) == 100

    # Verify no duplicates (unique spec_file values)
    spec_files = [e["spec_file"] for e in done_events]
    assert len(spec_files) == len(set(spec_files))

    duration = time.time() - start_time
    print(f"100 specs processed in {duration:.2f}s ({100/duration:.1f} specs/sec)")
```

### Latency Measurement

```python
@pytest.mark.integration
async def test_latency_measurement():
    """Test: Measure event delivery latency (p50/p95/p99)."""
    latencies = []

    for i in range(50):
        spec_path = queue_dir / f"SPEC-LAT-{i:03d}.md"

        # Record move time
        move_time = time.time()
        spec_path.write_text("# Test")

        # Wait for event in log
        while True:
            events = [json.loads(line) for line in event_log.read_text().splitlines()]
            matching = [e for e in events if e["spec_file"] == spec_path.name]
            if matching:
                event_time = datetime.fromisoformat(matching[0]["timestamp"].replace("Z", "+00:00")).timestamp()
                latency_ms = (event_time - move_time) * 1000
                latencies.append(latency_ms)
                break
            await asyncio.sleep(0.01)

    # Calculate percentiles
    latencies.sort()
    p50 = latencies[len(latencies) // 2]
    p95 = latencies[int(len(latencies) * 0.95)]
    p99 = latencies[int(len(latencies) * 0.99)]

    print(f"Latency: p50={p50:.1f}ms, p95={p95:.1f}ms, p99={p99:.1f}ms")

    assert p95 < 200, f"p95 latency too high: {p95:.1f}ms"
    assert p99 < 500, f"p99 latency too high: {p99:.1f}ms"
```

### Test Report Template

```markdown
# MCP Queue Notifications — Integration Test Report

**Date:** 2026-04-06
**Test Suite:** TASK-MCP-QUEUE-05

## Summary

- Total tests: 18
- Passed: 18
- Failed: 0
- Skipped: 0

## Full Pipeline Tests (4)

✓ Spec queued → active → done → scheduler recalculates
✓ Spec done → dispatcher frees slot → backlog dispatch
✓ Parallel completions (5 specs within 1s)
✓ Rapid moves (debouncing under 500ms)

## Failure Mode Tests (5)

✓ MCP server down → fallback polling
✓ Network timeout → other subscribers unaffected
✓ Malformed event → logged, no crash
✓ Subscriber 500 error → logged, no retry
✓ Watcher thread crash → auto-restart

## Performance Tests (4)

✓ 100 specs → no event loss
✓ Debouncing under load → no duplicates
✓ Latency: p50=45ms, p95=120ms, p99=280ms ✓
✓ Memory leak check → cache size bounded

## Recommendations

1. Deploy to staging first, monitor latency for 24h
2. Set up alerting for MCP server health
3. Consider bumping fallback interval to 90s (currently 60s)
4. Add Prometheus metrics for event delivery rate
```

## Constraints

- Use pytest with async support (`pytest-asyncio`)
- Tests must be reproducible (use tmp_path fixtures)
- Tests must clean up (stop threads, close sockets)
- Tests must be fast (<5min total suite runtime)
- No file over 500 lines (split into multiple test files)
- No stubs — all tests fully implemented

## Dependencies

**Depends on:** TASK-MCP-QUEUE-01, TASK-MCP-QUEUE-02, TASK-MCP-QUEUE-03, TASK-MCP-QUEUE-04

## Estimated Duration

2-2.5 hours (Sonnet)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260406-TASK-MCP-QUEUE-05-RESPONSE.md`

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

ALSO include the test report as `.deia/hive/responses/20260406-TASK-MCP-QUEUE-05-TEST-REPORT.md`.
