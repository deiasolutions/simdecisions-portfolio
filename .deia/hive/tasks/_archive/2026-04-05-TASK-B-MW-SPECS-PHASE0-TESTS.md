# TASK-B: Generate MW Spec Files — Phase 0 Specs + Phase 0.5 Tests

## Objective
Generate spec files for the remaining Phase 0 spec tasks (MW-S04 through MW-S08) and all Phase 0.5 test tasks (MW-T01 through MW-T08). Total: 13 spec files.

## Context
The Mobile Workdesk scheduler has 66 tasks. Only 3 spec files exist (MW-S01, MW-S02, MW-S03). The dispatcher needs spec files in `.deia/hive/queue/backlog/` to dispatch tasks.

Your job: write spec files for Phase 0 (remaining specs) and Phase 0.5 (all test tasks). These are the foundation tasks that define what components need to be built and what tests need to be written before building.

**Phase 0 (Remaining Specs):**
- MW-S04: SPEC: conversation-pane
- MW-S05: SPEC: mobile-nav
- MW-S06: SPEC: notification-pane
- MW-S07: SPEC: queue-pane
- MW-S08: SPEC: diff-viewer

**Phase 0.5 (All Tests):**
- MW-T01: TEST: command-interpreter
- MW-T02: TEST: voice-input
- MW-T03: TEST: quick-actions
- MW-T04: TEST: conversation-pane
- MW-T05: TEST: mobile-nav
- MW-T06: TEST: notification-pane
- MW-T07: TEST: queue-pane
- MW-T08: TEST: diff-viewer

## Files to Read First
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py` — task registry with IDs, descriptions, dependencies, durations
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/_active/SPEC-MW-S01-command-interpreter.md` — spec template (format, sections)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/_active/SPEC-MW-S02-voice-input.md` — spec template
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/_active/SPEC-MW-S03-quick-actions.md` — spec template
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/Shell.tsx` — shell structure (for context on how components integrate)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/` — existing primitive patterns (directory listing)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/docs/specs/SPEC-MOBILE-WORKDESK-001.md` — high-level Mobile Workdesk spec (if it exists)

## Deliverables
Write 13 spec files to `.deia/hive/queue/backlog/`:
- [ ] `SPEC-MW-S04-conversation-pane.md`
- [ ] `SPEC-MW-S05-mobile-nav.md`
- [ ] `SPEC-MW-S06-notification-pane.md`
- [ ] `SPEC-MW-S07-queue-pane.md`
- [ ] `SPEC-MW-S08-diff-viewer.md`
- [ ] `SPEC-MW-T01-test-command-interpreter.md`
- [ ] `SPEC-MW-T02-test-voice-input.md`
- [ ] `SPEC-MW-T03-test-quick-actions.md`
- [ ] `SPEC-MW-T04-test-conversation-pane.md`
- [ ] `SPEC-MW-T05-test-mobile-nav.md`
- [ ] `SPEC-MW-T06-test-notification-pane.md`
- [ ] `SPEC-MW-T07-test-queue-pane.md`
- [ ] `SPEC-MW-T08-test-diff-viewer.md`

## Spec Writing Guidelines
Each spec must have:
1. **## Priority** — always P1
2. **## Objective** — 1-2 sentences describing what the bee must build/design
3. **## Context** — what the component/test does, how it fits in Mobile Workdesk, key requirements
4. **## Files to Read First** — absolute paths to relevant source files (Shell.tsx, existing primitives, hooks, etc.)
5. **## Acceptance Criteria** — concrete deliverables as checkboxes (8-12 items)
6. **## Smoke Test** — 4-6 verification steps
7. **## Model Assignment** — "sonnet" for all specs/tests
8. **## Constraints** — file locations, max lines (500), CSS variables only, TDD, no stubs

**IMPORTANT:**
- NO BOILERPLATE. Each spec needs real content based on the task description in `scheduler_mobile_workdesk.py`.
- Read existing components in `browser/src/primitives/` to understand patterns (e.g., how tree-browser works, how command-palette works).
- For TEST tasks: the spec should describe what test file to create, what to test (component behavior, hooks, integration), and what coverage is expected.
- For SPEC tasks: the spec should describe the component's behavior, UI requirements, integration points, and accessibility.
- Use absolute Windows paths (C:/Users/davee/...).
- Phase 0.5 tests depend on corresponding Phase 0 specs (e.g., MW-T01 depends on MW-S01).

## Test Requirements
N/A — this task is spec-writing, not code. No tests to run.

## Acceptance Criteria
- [ ] 13 spec files created in `.deia/hive/queue/backlog/`
- [ ] Each spec is 50-100 lines (not just 20-line stubs)
- [ ] Each spec has real content (specific component requirements, not generic boilerplate)
- [ ] "Files to Read First" sections list actual source files that exist in the repo
- [ ] "Depends On" correctly reflects task registry dependencies from scheduler_mobile_workdesk.py
- [ ] All specs use "sonnet" model assignment
- [ ] All specs follow the format from MW-S01/MW-S02/MW-S03
- [ ] Naming convention: `SPEC-MW-{ID}-{short-description}.md`

## Smoke Test
- [ ] All 13 files exist in `.deia/hive/queue/backlog/`
- [ ] Each file contains sections: Priority, Objective, Context, Files to Read First, Acceptance Criteria, Smoke Test, Model Assignment, Constraints
- [ ] Dependencies match scheduler_mobile_workdesk.py TASKS list
- [ ] Open 3 random specs — they contain specific requirements, not boilerplate

## Constraints
- Output location: `.deia/hive/queue/backlog/`
- Each spec: 50-100 lines
- Follow exact format from existing MW-S01/MW-S02/MW-S03 specs
- NO STUBS — write real content
- Read codebase first to understand component patterns
- Use absolute paths for "Files to Read First"

## Response Requirements — MANDATORY
When you finish your work, write a response file:
  `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/responses/20260405-TASK-B-MW-SPECS-PHASE0-TESTS-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — N/A (no code tests, but verify files exist)
5. **Build Verification** — N/A (spec files don't build)
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
