# TASK-023A: Queue Config YAML

## Objective
Create the queue configuration file at `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\queue.yml` with budget limits, model assignments, paths, deploy config, and git settings.

## Context
This is part of SPEC-BUILD-QUEUE-001 Phase 1. The queue runner (`run_queue.py`) will read this config to enforce budget, assign models to different roles (regent, Q33N, bees), and manage queue paths. The config format is defined in section 4 of the spec.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-BUILD-QUEUE-001.md` (section 4)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\carbon.yml` (existing config example)

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\queue.yml`
- [ ] Include all required sections: `budget`, `models`, `paths`, `deploy`, `git`
- [ ] Match the exact structure from spec section 4
- [ ] All paths relative to repo root (`.deia/hive/...`)
- [ ] Model assignments: regent=ollama:llama3.1:8b, q33n=claude-sonnet-4-6, bee_default=claude-haiku-4-5, bee_complex=claude-sonnet-4-6
- [ ] Budget: max_session_usd=20.00, warn_threshold=0.80, max_fix_cycles_per_spec=2, max_specs_per_session=50, max_parallel_bees=3
- [ ] Deploy URLs: Railway dev-api health + Vercel dev frontend
- [ ] Git: branch=dev, commit_prefix=[Q33N], auto_push=true

## Test Requirements
- [ ] Write test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_queue_config.py`
- [ ] Test: Load the YAML and verify all required top-level keys exist (budget, models, paths, deploy, git)
- [ ] Test: Verify budget.max_session_usd is a number > 0
- [ ] Test: Verify budget.warn_threshold is between 0 and 1
- [ ] Test: Verify all paths keys exist (queue_dir, needs_review_dir, done_dir, smoke_dir, coordination_dir, tasks_dir, responses_dir)
- [ ] Test: Verify all model keys exist (regent_bot, q33n, bee_default, bee_complex)
- [ ] Test: Verify deploy keys exist (railway_health_url, vercel_url, health_poll_interval_seconds, health_poll_timeout_seconds)
- [ ] Test: Verify git keys exist (branch, commit_prefix, auto_push)
- [ ] Minimum 7 tests (one per section + one for overall structure)

## Constraints
- Pure YAML — no inline comments except section headers
- No file over 500 lines (this will be ~50 lines)
- CSS: N/A (not a UI file)
- No stubs

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260311-TASK-023A-RESPONSE.md`

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
