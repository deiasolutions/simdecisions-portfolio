# TASK-SD-03: Create Backlog Directory and Seed Test Specs

## Objective
Create `.deia/hive/queue/backlog/` directory and write 2-3 small test spec files to verify the scheduler+dispatcher pipeline works end-to-end.

## Context
The dispatcher (TASK-SD-02) moves spec files from `backlog/` to `queue/` root. The backlog/ directory does not exist yet. This task creates it and seeds it with minimal test specs that correspond to tasks in the Mobile Workdesk schedule (from scheduler_mobile_workdesk.py TASKS list).

The test specs should be real SPEC files (not stubs) but minimal — just enough to verify:
1. Scheduler computes schedule with these tasks
2. Dispatcher finds them in backlog/
3. Dispatcher moves them to queue/
4. Queue-runner can pick them up (though we won't run queue-runner in this test)

Use the first 3 tasks from TASKS list in scheduler_mobile_workdesk.py:
- MW-S01: SPEC: command-interpreter (3 hours)
- MW-S02: SPEC: voice-input (2 hours)
- MW-S03: SPEC: quick-actions (FAB) (2 hours)

All three are independent (no deps), so they're ready to dispatch immediately.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\scheduler\scheduler_mobile_workdesk.py`
  Lines 53-60: First 3 SPEC tasks (MW-S01, MW-S02, MW-S03)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\_done\`
  Check a few completed specs to see the format (if any exist)

## Deliverables
- [ ] Create directory: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\backlog\`
- [ ] Write 3 spec files:
  - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\backlog\SPEC-MW-S01-command-interpreter.md`
  - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\backlog\SPEC-MW-S02-voice-input.md`
  - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\backlog\SPEC-MW-S03-quick-actions.md`
- [ ] Each spec file must contain:
  - `## Priority` (P1)
  - `## Depends On` (none for these 3 tasks)
  - `## Model Assignment` (sonnet)
  - `## Acceptance Criteria` (1-2 bullet points, real criteria)
  - `## Smoke Test` (1-2 steps to verify it works)
  - `## Constraints` (TDD, no stubs, no hardcoded colors, max 500 lines)
- [ ] Content should be real spec content (not "TODO" or "TBD") — write actual requirements for:
  - MW-S01: command-interpreter spec (natural language → fuzzy match → PRISM-IR)
  - MW-S02: voice-input spec (Web Speech API → command-interpreter)
  - MW-S03: quick-actions spec (FAB with mic + keyboard buttons)
- [ ] Each spec should be 50-100 lines (real content, not filler)
- [ ] Use absolute paths in specs (C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\...)

## Test Requirements
- [ ] No tests needed — this is file creation only
- [ ] Verification: `ls -la .deia/hive/queue/backlog/` shows 3 SPEC-MW-*.md files
- [ ] Verification: Each file is 50-100 lines
- [ ] Verification: Each file has all required sections (Priority, Depends On, Model Assignment, Acceptance Criteria, Smoke Test, Constraints)

## Constraints
- No file over 500 lines (N/A — these specs will be 50-100 lines each)
- CSS: N/A
- No stubs — specs must have real content
- Follow existing spec format (check `.deia/hive/queue/_done/` for examples if available)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260405-TASK-SD-03-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — "No tests required (file creation only)" + verification steps
5. **Build Verification** — "N/A (no code to build)"
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — platform-populated from build monitor telemetry (do not estimate manually)
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
