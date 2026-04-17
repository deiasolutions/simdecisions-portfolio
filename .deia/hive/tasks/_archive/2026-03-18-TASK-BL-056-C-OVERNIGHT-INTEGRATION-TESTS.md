# TASK-BL-056-C: Integration tests for overnight queue processing

## Objective
Add comprehensive integration tests for the queue runner's overnight automation features: watch mode, hot-reload, dependency blocking, Fibonacci backoff, budget exhaustion, and session report generation.

## Context
The queue runner (`run_queue.py`) has sophisticated orchestration logic:
- **Watch mode** — Polls queue directory every N seconds (Fibonacci backoff), processes new specs as they arrive
- **Hot-reload** — Rescans queue directory after every completion, adding new specs dynamically
- **Dependency tracking** — Specs with `hold-until: [SPEC-A, SPEC-B]` wait until dependencies are in `_done/`
- **Budget exhaustion** — Stops processing when session cost exceeds `max_session_usd`
- **Session report** — Generates morning report when queue is empty

**Gap:** No integration test coverage. These features work in production but have no regression protection.

**Solution:** Add integration test suite that mocks `process_spec_no_verify()` to return instant results, testing orchestration logic without waiting for real bees.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` (1179 lines) — Main orchestration logic
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_parser.py` (189 lines) — Spec parsing with dependencies
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py` (547 lines) — `process_spec_no_verify()` signature
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_run_queue_heartbeat.py` — Existing test patterns

## Deliverables

### Test file: test_queue_overnight.py
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_queue_overnight.py`
- [ ] **TDD approach:** Write tests to verify existing orchestration behavior
- [ ] Test count: **10 minimum**

### Test scenarios:

#### 1. Watch mode polling
- [ ] Test: Queue runner enters watch mode when queue is empty
- [ ] Verify: Polls queue directory every N seconds (Fibonacci backoff)
- [ ] Mock: `load_queue()` returns empty list initially, then returns 1 spec on 3rd poll
- [ ] Assert: Spec is processed after appearing in queue

#### 2. Hot-reload during processing
- [ ] Test: New spec appears while another spec is processing
- [ ] Verify: New spec is detected and added to pipeline after rescan
- [ ] Mock: `_rescan_queue()` returns 1 spec on first call, 2 specs on second call
- [ ] Assert: Second spec is dispatched after first completes

#### 3. Dependency blocking
- [ ] Test: Spec B depends on Spec A (`hold-until: [2026-03-18-SPEC-A]`)
- [ ] Verify: Spec B stays in queue until Spec A moves to `_done/`
- [ ] Mock: `_check_dependencies()` returns `False` initially, then `True` after Spec A completes
- [ ] Assert: Spec B only dispatches after Spec A completion

#### 4. Fibonacci backoff in watch mode
- [ ] Test: Watch mode with `adaptive=True` uses Fibonacci backoff
- [ ] Verify: Poll intervals grow: 30s, 30s, 60s, 90s, 150s (capped at 150s)
- [ ] Mock: `time.sleep()` to avoid waiting
- [ ] Assert: Sleep durations follow Fibonacci sequence

#### 5. Budget exhaustion
- [ ] Test: Queue runner stops when session cost exceeds `max_session_usd`
- [ ] Verify: Processes 3 specs (cost $0.30 each), stops before 4th (budget $1.00)
- [ ] Mock: `process_spec_no_verify()` returns `SpecResult` with `cost_usd=0.30`
- [ ] Assert: Only 3 specs processed, 4th remains in queue

#### 6. Session report generation
- [ ] Test: Queue runner generates morning report when queue is empty
- [ ] Verify: `generate_morning_report()` called with all events
- [ ] Mock: `generate_morning_report()` to capture event list
- [ ] Assert: Report includes all processed specs

#### 7. Slot backfill
- [ ] Test: When a bee completes, its slot is immediately filled
- [ ] Verify: 5 specs dispatched with `max_parallel=5`, slot freed after 1st completes
- [ ] Mock: `process_spec_no_verify()` returns after 1 second for first spec, instant for others
- [ ] Assert: 6th spec dispatches immediately after 1st completes (no wait for batch)

#### 8. Priority ordering
- [ ] Test: Queue processes P0 specs before P1, P1 before P2
- [ ] Verify: 3 specs (P2, P0, P1) process in order: P0, P1, P2
- [ ] Mock: Specs have different priorities in metadata
- [ ] Assert: Processing order matches priority

#### 9. Fix cycle generation
- [ ] Test: Failed spec triggers fix cycle (max 2 cycles per root spec)
- [ ] Verify: Fix spec generated and moved to queue
- [ ] Mock: `process_spec_no_verify()` returns `success=False`
- [ ] Assert: Fix spec exists in queue with `fix-1` suffix

#### 10. Max restart attempts
- [ ] Test: Spec times out 3 times (2 restarts + initial), then moves to `_needs_review/`
- [ ] Verify: Spec not restarted after 2nd timeout
- [ ] Mock: `process_spec_no_verify()` returns `error="TIMEOUT"` three times
- [ ] Assert: Spec in `_needs_review/` after 3rd timeout

### Mock strategy:
- **Process mocking:** `patch("spec_processor.process_spec_no_verify")` returns instant `SpecResult`
- **Time mocking:** `patch("time.sleep")` to avoid waiting during backoff
- **Filesystem mocking:** Use `tmp_path` fixture for queue directories
- **HTTP mocking:** `patch("urllib.request.urlopen")` to mock heartbeat POSTs

### Example test structure:
```python
def test_watch_mode_polling(tmp_path):
    """Watch mode polls queue and processes new specs."""
    queue_dir = tmp_path / "queue"
    queue_dir.mkdir()

    # Mock load_queue to return empty initially, then 1 spec on 3rd poll
    poll_count = 0
    def mock_load_queue(path):
        nonlocal poll_count
        poll_count += 1
        if poll_count < 3:
            return []
        # Create spec file on 3rd poll
        spec_file = queue_dir / "2026-03-18-SPEC-TEST-001.md"
        spec_file.write_text("# SPEC-TEST-001\nPriority: P1\nModel: sonnet\n")
        return [SpecFile(path=spec_file, priority=1, ...)]

    with patch("spec_parser.load_queue", side_effect=mock_load_queue):
        with patch("spec_processor.process_spec_no_verify") as mock_process:
            mock_process.return_value = SpecResult(success=True, ...)
            # Run queue with watch mode
            # Assert: process_spec_no_verify called once after 3rd poll
```

## Test Requirements
- [ ] **TDD approach:** Write tests to verify existing orchestration behavior
- [ ] All tests pass
- [ ] Mock strategy: No real subprocess spawns, no real file I/O (use tmp_path), no long waits
- [ ] Test isolation: Each test uses separate tmp_path, no shared state

## Constraints
- No file over 500 lines
- No stubs — all test assertions fully implemented
- No hardcoded colors (N/A for Python)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-BL-056-C-RESPONSE.md`

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

## Acceptance Criteria
- [ ] `test_queue_overnight.py` created
- [ ] 10+ tests written and passing
- [ ] Watch mode polling test passes
- [ ] Hot-reload test passes
- [ ] Dependency blocking test passes
- [ ] Fibonacci backoff test passes
- [ ] Budget exhaustion test passes
- [ ] Session report test passes
- [ ] Slot backfill test passes
- [ ] Priority ordering test passes
- [ ] Fix cycle generation test passes
- [ ] Max restart attempts test passes
- [ ] All tests use mocks (no real subprocess, no long waits)
- [ ] No file over 500 lines
- [ ] No stubs shipped

## Model Assignment
**sonnet** — complex orchestration logic, multi-step test scenarios, requires understanding full pipeline flow
