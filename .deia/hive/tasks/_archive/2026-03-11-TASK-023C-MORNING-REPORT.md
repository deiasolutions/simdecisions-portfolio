# TASK-023C: Morning Report Generator

## Objective
Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\morning_report.py` — a script that reads queue session event logs and generates a markdown morning report summarizing what the queue processed overnight.

## Context
This is part of SPEC-BUILD-QUEUE-001 Phase 1. After the queue runner finishes processing specs (either queue empty or budget exhausted), it calls `generate_morning_report()` to create a human-readable summary for Dave to review in the morning. The report shows: specs processed, success/fail counts, session cost/duration, completed specs table, failed specs needing review, screenshot paths, and remaining queue.

The morning report reads from a session event log (JSON file) written by `run_queue.py`. The event log structure will be defined by the queue runner, but for this task, define a minimal `QueueEvent` dataclass that can be imported by both scripts.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-BUILD-QUEUE-001.md` (sections 8.3, 10)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\BOOT.md` (file system paths)

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\morning_report.py`
- [ ] Function: `generate_morning_report(session_events: list[QueueEvent], queue_dir: Path, output_path: Path) -> Path`
- [ ] Define `QueueEvent` dataclass with fields: event_type (str), timestamp (str), spec_id (str), cost_usd (float), duration_ms (int), model_used (str), details (dict)
- [ ] Generate markdown with sections: Queue Summary, Completed, Needs Your Review, Screenshots, Remaining Queue
- [ ] Queue Summary: specs processed/succeeded/failed/remaining, session cost (sum of all cost_usd), session duration (first to last timestamp)
- [ ] Completed table: Spec | Status | Tests | Cost | Time (extract from QUEUE_BEES_COMPLETE events)
- [ ] Needs Review table: Spec | Issue | Fix Attempts (extract from QUEUE_NEEDS_DAVE events)
- [ ] Screenshots section: list paths from .deia/hive/smoke/ if they exist
- [ ] Remaining Queue section: read queue_dir, list unprocessed .md files with priority
- [ ] Output file: `YYYY-MM-DD-MORNING-REPORT.md` in queue_dir
- [ ] Pure Python, no external deps beyond stdlib (Path, dataclasses, datetime, json)

## Test Requirements
- [ ] Write test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_morning_report.py`
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - [ ] Empty event list (no specs processed)
  - [ ] All specs succeeded (no failures)
  - [ ] All specs failed (no successes)
  - [ ] Mixed success/fail
  - [ ] Zero cost (free models)
  - [ ] Session duration calculation (first event to last event)
  - [ ] Remaining queue detection (unprocessed .md files)
  - [ ] Output file path returned correctly
- [ ] Minimum 5 tests

## Constraints
- No file over 500 lines
- Pure Python 3.13 — only stdlib imports
- No stubs
- Must be importable by `run_queue.py` (will call `generate_morning_report()`)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260311-TASK-023C-RESPONSE.md`

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
