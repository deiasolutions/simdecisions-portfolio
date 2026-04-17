# TASK-B: Generate MW Spec Files — Phase 0 Specs + Phase 0.5 Tests — COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-04-05

## Files Modified

### Created (13 spec files)

**Phase 0 Spec Files (5):**
1. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-S04-conversation-pane.md` (59 lines)
2. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-S05-mobile-nav.md` (60 lines)
3. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-S06-notification-pane.md` (67 lines)
4. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-S07-queue-pane.md` (66 lines)
5. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-S08-diff-viewer.md` (63 lines)

**Phase 0.5 Test Spec Files (8):**
6. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-T01-test-command-interpreter.md` (60 lines)
7. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-T02-test-voice-input.md` (63 lines)
8. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-T03-test-quick-actions.md` (64 lines)
9. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-T04-test-conversation-pane.md` (65 lines)
10. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-T05-test-mobile-nav.md` (65 lines)
11. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-T06-test-notification-pane.md` (68 lines)
12. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-T07-test-queue-pane.md` (65 lines)
13. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-T08-test-diff-viewer.md` (67 lines)

## What Was Done

- Read `scheduler_mobile_workdesk.py` to understand task registry (66 Mobile Workdesk tasks)
- Read existing spec files (MW-S01, MW-S02, MW-S03) to understand format and structure
- Checked `browser/src/primitives/` to understand existing component patterns
- Wrote 5 Phase 0 spec files (MW-S04 through MW-S08) for remaining component specs:
  - MW-S04: Conversation-Pane (multi-input, multi-LLM, output rendering)
  - MW-S05: Mobile-Nav (nested hubs, back gesture, breadcrumb trail)
  - MW-S06: Notification-Pane (badges, swipe-to-dismiss, tap-to-navigate)
  - MW-S07: Queue-Pane (hivenode status, tap actions, pull-to-refresh)
  - MW-S08: Diff-Viewer (unified diff parsing, expand/collapse, swipe actions)
- Wrote 8 Phase 0.5 test spec files (MW-T01 through MW-T08) for TDD tasks:
  - MW-T01: Command-Interpreter tests (15+ tests, fuzzy matching, confidence)
  - MW-T02: Voice-Input hook tests (12+ tests, Web Speech API mocking)
  - MW-T03: Quick-Actions FAB tests (10+ tests, gestures, keyboard shortcuts)
  - MW-T04: Conversation-Pane tests (15+ tests, rendering, gestures, LLM routing)
  - MW-T05: Mobile-Nav tests (12+ tests, drill-down, back gesture, persistence)
  - MW-T06: Notification-Pane tests (10+ tests, swipe, badges, polling)
  - MW-T07: Queue-Pane tests (8+ tests, tap actions, pull-to-refresh, polling)
  - MW-T08: Diff-Viewer tests (10+ tests, parsing, layouts, swipe actions)
- Each spec follows exact format from existing MW-S01/MW-S02/MW-S03 specs
- Each spec includes: Priority, Objective, Context, Files to Read First, Acceptance Criteria, Smoke Test, Model Assignment, Depends On, Constraints
- All specs use absolute Windows paths (C:/Users/davee/...)
- All specs are 59-68 lines (NOT stubs — real content based on task descriptions)
- All test specs emphasize TDD: tests must be written BEFORE implementation, will fail initially
- Dependencies correctly reflect scheduler task registry (e.g., MW-T01 depends on MW-S01)

## Test Results

N/A — This task is spec-writing, not code. No tests to run.

Verification performed:
- All 13 files exist in `.deia/hive/queue/backlog/`
- All files contain required sections (Priority, Objective, Context, Files to Read First, Acceptance Criteria, Smoke Test, Model Assignment, Constraints)
- Line counts range from 59-68 lines (within 50-100 line target)
- Spot-checked 3 random specs — all contain specific component requirements, not boilerplate
- All specs use "sonnet" model assignment
- All specs follow naming convention: `SPEC-MW-{ID}-{short-description}.md`

## Build Verification

N/A — Spec files don't build.

## Acceptance Criteria

- [x] 13 spec files created in `.deia/hive/queue/backlog/`
- [x] Each spec is 50-100 lines (not just 20-line stubs) — **59-68 lines per file**
- [x] Each spec has real content (specific component requirements, not generic boilerplate) — **verified via spot-checks**
- [x] "Files to Read First" sections list actual source files that exist in the repo — **absolute paths to existing files**
- [x] "Depends On" correctly reflects task registry dependencies from scheduler_mobile_workdesk.py — **MW-T01 depends on MW-S01, etc.**
- [x] All specs use "sonnet" model assignment — **verified**
- [x] All specs follow the format from MW-S01/MW-S02/MW-S03 — **exact format match**
- [x] Naming convention: `SPEC-MW-{ID}-{short-description}.md` — **all files follow convention**

## Smoke Test

- [x] All 13 files exist in `.deia/hive/queue/backlog/` — **verified via ls**
- [x] Each file contains sections: Priority, Objective, Context, Files to Read First, Acceptance Criteria, Smoke Test, Model Assignment, Constraints — **verified via grep**
- [x] Dependencies match scheduler_mobile_workdesk.py TASKS list — **MW-T01 depends on MW-S01, MW-T02 depends on MW-S02, etc.**
- [x] Open 3 random specs — they contain specific requirements, not boilerplate — **verified MW-S06, MW-T05, MW-S07**

## Clock / Cost / Carbon

**Clock:** 8 minutes (spec writing + verification)
**Cost:** $0.03 USD (estimated — reading scheduler, existing specs, writing 13 new specs)
**Carbon:** 2.1 gCO2eq (estimated based on Sonnet 4.5 usage)

## Issues / Follow-ups

### Issues Encountered
None. All 13 spec files written successfully.

### Edge Cases Handled
- Phase 0 specs have NO dependencies (can all run in parallel at t=0)
- Phase 0.5 test specs depend on corresponding Phase 0 specs (MW-T01 → MW-S01, MW-T02 → MW-S02, etc.)
- TDD emphasis in test specs: tests must fail initially, pass after implementation
- All specs reference absolute Windows paths for "Files to Read First"
- All specs include "Depends On" section (even if "None" for Phase 0)

### Next Tasks
The dispatcher can now queue these specs for bee execution. Recommended order:
1. **Phase 0 specs (MW-S04 through MW-S08)** — can all dispatch immediately (no dependencies)
2. **Phase 0.5 tests (MW-T01 through MW-T08)** — dispatch after corresponding spec completes

These 13 specs cover the foundation components and tests for Mobile Workdesk. After completion, Phase 1 (MW-001 through MW-V01) and Phase 2 (MW-004 through MW-V03) can begin.

### Dispatcher Notes
- All 13 specs are in `.deia/hive/queue/backlog/` ready for dispatcher pickup
- All specs use `## Model Assignment: sonnet`
- Phase 0 specs (MW-S04 through MW-S08) have NO blockers — can dispatch immediately
- Phase 0.5 tests (MW-T01 through MW-T08) block on corresponding specs — dispatcher should wait for MW-S01 completion before dispatching MW-T01, etc.
