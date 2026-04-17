# TASK-023D: Queue Runner Script

## Objective
Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` — the core queue orchestration loop that processes specs, dispatches Q88NR-bot, tracks costs, logs events, and generates the morning report.

## Context
This is part of SPEC-BUILD-QUEUE-001 Phase 1 — the most complex deliverable. The queue runner is the automation engine that Dave starts before going to sleep. It loads specs from `.deia/hive/queue/`, sorts by priority (P0 → P1 → P2), dispatches Q88NR-bot for each spec, tracks cost, enforces budget limits, handles fix cycles, moves completed/failed specs, logs events, and generates a morning report at the end.

This task depends on TASK-023C (morning_report.py) for the report generator and TASK-023A (queue.yml) for config. Import `generate_morning_report()` and `QueueEvent` from morning_report.py.

The queue runner does NOT implement the full HIVE.md chain itself — it dispatches Q88NR-bot (via dispatch.py), which drives the chain. The runner only orchestrates: load queue → dispatch regent → track cost → move files → log → report.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-BUILD-QUEUE-001.md` (sections 3, 4, 7, 8, 9, 10)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py` (understand how to call it)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\morning_report.py` (import generate_morning_report)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\queue.yml` (read this for config)

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py`
- [ ] CLI interface: `python run_queue.py [--config path] [--dry-run]`
- [ ] `--config`: path to queue.yml (default: `.deia/config/queue.yml`)
- [ ] `--dry-run`: parse specs, print execution plan, don't dispatch
- [ ] Function: `load_queue(queue_dir: Path) -> list[SpecFile]` — find all .md files in queue_dir, sort by priority (P0/P1/P2 extracted from spec), then by filename
- [ ] Function: `parse_spec(spec_path: Path) -> SpecFile` — extract priority, objective, acceptance criteria, model assignment, smoke test criteria from spec markdown
- [ ] Dataclass: `SpecFile` with fields: path, priority, objective, acceptance_criteria, model, smoke_test, constraints
- [ ] Function: `process_spec(spec: SpecFile, config: dict, session_events: list[QueueEvent]) -> SpecResult` — dispatch Q88NR-bot with spec, track cost, log events, return result
- [ ] Dataclass: `SpecResult` with fields: spec_id, status (CLEAN/NEEDS_DAVE/BUDGET_EXCEEDED), cost_usd, duration_ms, error_msg
- [ ] Function: `run_queue(queue_dir: Path, config_path: Path, dry_run: bool) -> None` — main entry point
- [ ] Budget enforcement: track cumulative session_cost_usd, warn at 80%, stop at 100%
- [ ] Fix cycle logic: when spec fails, Q88NR-bot creates a fix spec (P0), enters queue, max 2 fix cycles, then move to _needs_review/
- [ ] Event logging: write session-YYYY-MM-DD-HHMM.json to queue_dir with all QueueEvent objects
- [ ] File movement: CLEAN specs → _done/, NEEDS_DAVE specs → _needs_review/
- [ ] After queue finishes: call `generate_morning_report(session_events, queue_dir, output_path)`
- [ ] Use `dispatch.py` for ALL dispatches — never call claude CLI directly
- [ ] Load config from queue.yml via PyYAML (or stdlib json if you convert yaml to json in tests)
- [ ] Python 3.13, under 500 lines (if over, split into modules like spec_parser.py, event_logger.py)

## Test Requirements
- [ ] Write test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_run_queue.py`
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - [ ] Queue sorting: P0 before P1 before P2, same priority sorted by filename
  - [ ] Spec parsing: extract priority from markdown section `## Priority\nP0`
  - [ ] Budget enforcement: warn at 80%, stop at 100%
  - [ ] Fix cycle limits: max 2 fix cycles, then NEEDS_DAVE
  - [ ] Dry-run mode: prints plan but doesn't dispatch
  - [ ] Empty queue: generates report with "0 specs processed"
  - [ ] Config loading: reads queue.yml, validates required keys
  - [ ] Event logging: writes valid JSON with all required fields
  - [ ] File movement: moves specs to _done/ or _needs_review/
  - [ ] Morning report called at end
- [ ] Minimum 15 tests (spec says 15+)
- [ ] Use mock dispatch (don't actually call dispatch.py in tests)

## Constraints
- No file over 500 lines (split into modules if needed)
- Python 3.13
- No stubs
- Must use existing `dispatch.py` — never call claude CLI directly
- Must NOT modify `.deia/config/`, `.deia/BOOT.md`, `.deia/HIVE.md`, or `CLAUDE.md`
- All paths relative to repo root (resolve via `Path(__file__).resolve().parents[N]`)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260311-TASK-023D-RESPONSE.md`

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
