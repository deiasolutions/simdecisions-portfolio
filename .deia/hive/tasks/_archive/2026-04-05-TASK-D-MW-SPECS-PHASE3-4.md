# TASK-D: Generate MW Spec Files — Phase 3-4 Navigation + Destination Panes

## Objective
Generate spec files for Phase 3 (mobile navigation) and Phase 4 (destination panes: notifications, queue, diff-viewer). Total: 16 spec files.

## Context
Phase 3 builds the mobile navigation hub structure (nested drill-down, back gestures, FAB integration). Phase 4 builds the destination panes that mobile nav routes to.

**Phase 3 (Navigation Build):**
- MW-011: BUILD: mobile-nav nested hub structure
- MW-012: BUILD: mobile-nav back gesture + drill-down
- MW-013: BUILD: mobile-nav FAB integration
- MW-V05: VERIFY: mobile-nav

**Phase 4 (Destination Panes Build):**
- MW-014: BUILD: notification-pane data model + home
- MW-015: BUILD: notification-pane badges + swipe
- MW-016: BUILD: notification-pane tap-to-navigate
- MW-V06: VERIFY: notification-pane
- MW-017: BUILD: queue-pane hivenode fetch
- MW-018: BUILD: queue-pane state display
- MW-019: BUILD: queue-pane tap actions
- MW-V07: VERIFY: queue-pane
- MW-020: BUILD: diff-viewer parsing + layout
- MW-021: BUILD: diff-viewer expand/collapse
- MW-022: BUILD: diff-viewer swipe actions
- MW-V08: VERIFY: diff-viewer

## Files to Read First
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py` — task registry
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/_active/SPEC-MW-S01-command-interpreter.md` — spec template
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/Shell.tsx` — shell structure, navigation patterns
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/` — existing pane primitives
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/routes/` — backend routes for queue data, notifications
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/state/` — state management patterns (if any)

## Deliverables
Write 16 spec files to `.deia/hive/queue/backlog/`:

**Phase 3:**
- [ ] `SPEC-MW-011-mobile-nav-hub.md`
- [ ] `SPEC-MW-012-mobile-nav-gestures.md`
- [ ] `SPEC-MW-013-mobile-nav-fab.md`
- [ ] `SPEC-MW-V05-verify-mobile-nav.md`

**Phase 4 (Notifications):**
- [ ] `SPEC-MW-014-notification-pane-data.md`
- [ ] `SPEC-MW-015-notification-pane-badges.md`
- [ ] `SPEC-MW-016-notification-pane-tap.md`
- [ ] `SPEC-MW-V06-verify-notification-pane.md`

**Phase 4 (Queue):**
- [ ] `SPEC-MW-017-queue-pane-fetch.md`
- [ ] `SPEC-MW-018-queue-pane-display.md`
- [ ] `SPEC-MW-019-queue-pane-actions.md`
- [ ] `SPEC-MW-V07-verify-queue-pane.md`

**Phase 4 (Diff Viewer):**
- [ ] `SPEC-MW-020-diff-viewer-parse.md`
- [ ] `SPEC-MW-021-diff-viewer-collapse.md`
- [ ] `SPEC-MW-022-diff-viewer-swipe.md`
- [ ] `SPEC-MW-V08-verify-diff-viewer.md`

## Spec Writing Guidelines
Same format as TASK-B and TASK-C.

**Mobile-nav specs:** Focus on touch gestures (swipe back, tap drill-down), nested hub structure (breadcrumbs, parent/child navigation), safe area handling, FAB integration (how FAB is positioned in nav).

**Notification-pane specs:** Data model (what notifications look like), badge rendering (unread count), swipe gestures (dismiss, archive), tap-to-navigate (routing to notification source).

**Queue-pane specs:** Hivenode API integration (`GET /build/status`), state display (active, queued, done), tap actions (view details, cancel, retry).

**Diff-viewer specs:** Unified diff parsing, syntax highlighting (if any), expand/collapse hunks, swipe actions (approve, reject, comment).

**VERIFY specs:** List all critical paths, E2E scenarios, edge cases. Must cover happy path + error states.

## Test Requirements
N/A — spec-writing task.

## Acceptance Criteria
- [ ] 16 spec files created in `.deia/hive/queue/backlog/`
- [ ] Each spec is 50-100 lines (VERIFY specs 30-50)
- [ ] Each spec has real content (not boilerplate)
- [ ] "Files to Read First" lists actual source files
- [ ] Dependencies match scheduler_mobile_workdesk.py
- [ ] All specs use "sonnet" model
- [ ] Naming: `SPEC-MW-{ID}-{short-description}.md`

## Smoke Test
- [ ] All 16 files exist in `.deia/hive/queue/backlog/`
- [ ] Each file has all required sections
- [ ] Dependencies match TASKS list
- [ ] Open MW-011 spec — describes nested hub structure with concrete UI requirements
- [ ] Open MW-017 spec — describes hivenode API endpoint, fetch logic, error handling

## Constraints
- Output location: `.deia/hive/queue/backlog/`
- Each BUILD spec: 50-100 lines
- Each VERIFY spec: 30-50 lines
- NO STUBS — write real content
- Read codebase first (Shell.tsx, existing primitives)
- Use absolute paths

## Response Requirements — MANDATORY
When you finish your work, write a response file:
  `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/responses/20260405-TASK-D-MW-SPECS-PHASE3-4-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — N/A
5. **Build Verification** — N/A
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
