# TASK-D: Generate MW Spec Files — Phase 3-4 Navigation + Destination Panes -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-05

## Files Modified

### Created (16 spec files)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-011-mobile-nav-hub.md`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-012-mobile-nav-gestures.md`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-013-mobile-nav-fab.md`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-V05-verify-mobile-nav.md`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-014-notification-pane-data.md`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-015-notification-pane-badges.md`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-016-notification-pane-tap.md`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-V06-verify-notification-pane.md`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-017-queue-pane-fetch.md`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-018-queue-pane-display.md`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-019-queue-pane-actions.md`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-V07-verify-queue-pane.md`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-020-diff-viewer-parse.md`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-021-diff-viewer-collapse.md`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-022-diff-viewer-swipe.md`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-V08-verify-diff-viewer.md`

## What Was Done

### Phase 3: Mobile Navigation (4 specs)
- **MW-011 (62 lines):** Mobile-nav nested hub structure with breadcrumb trails, safe area handling, parent/child navigation hierarchy, and slide animations
- **MW-012 (57 lines):** Mobile-nav back gesture (iOS-style edge swipe) and tap-to-drill-down with velocity tracking, cancel threshold, and visual feedback
- **MW-013 (57 lines):** Mobile-nav FAB integration with smart positioning (portrait/landscape), z-index management, and safe area awareness
- **MW-V05 (41 lines):** VERIFY spec for mobile-nav covering 30 unit tests, 7 E2E tests, cross-device compatibility, and edge cases

### Phase 4: Notification-Pane (4 specs)
- **MW-014 (64 lines):** Notification-pane data model, Zustand store, hivenode API integration (`GET /build/notifications`), auto-refresh polling, and notification types (build_event, inventory_update, system_alert)
- **MW-015 (61 lines):** Notification-pane badge rendering (unread count on nav icon + per-notification), swipe gestures (dismiss, archive), and haptic feedback
- **MW-016 (59 lines):** Notification-pane tap-to-navigate functionality with RTD bus events, mark-as-read, and navigation targets based on notification type
- **MW-V06 (40 lines):** VERIFY spec for notification-pane covering 30 unit tests, 7 E2E tests, and edge cases (offline, race conditions, rapid taps)

### Phase 4: Queue-Pane (4 specs)
- **MW-017 (67 lines):** Queue-pane hivenode fetch integration (`GET /build/status`), Zustand store, auto-refresh polling (10s), pull-to-refresh gesture, and filter tabs (All, Active, Queued, Complete, Failed)
- **MW-018 (61 lines):** Queue-pane state display with QueueTaskCard component, status indicators (color-coded), progress bars, metadata display (bee_id, cost, tokens, duration), and expandable details
- **MW-019 (65 lines):** Queue-pane tap actions with long-press action menu (Cancel, Retry, View Response), confirmation dialogs, and toast feedback
- **MW-V07 (40 lines):** VERIFY spec for queue-pane covering 32 unit tests, 7 E2E tests, and edge cases (offline, race conditions, long-press performance)

### Phase 4: Diff-Viewer (4 specs)
- **MW-020 (63 lines):** Diff-viewer unified diff parsing, side-by-side/unified layout rendering, color-coded additions/deletions, file/hunk headers, multi-file support, and optional syntax highlighting
- **MW-021 (60 lines):** Diff-viewer expand/collapse for file headers (and optional hunks), state persistence in localStorage, keyboard shortcuts (Ctrl+E, Ctrl+Shift+E), and chevron icons
- **MW-022 (62 lines):** Diff-viewer swipe actions (stage/unstage lines), visual feedback with action icons (✓, ✗), state persistence, and optional long-press comment action
- **MW-V08 (40 lines):** VERIFY spec for diff-viewer covering 32 unit tests, 7 E2E tests, and edge cases (malformed diffs, rapid swipes, 1000-line diffs)

### Spec Quality Assurance
- All BUILD specs: 57-67 lines (target: 50-100 lines) ✓
- All VERIFY specs: 40-41 lines (target: 30-50 lines) ✓
- All specs include: Priority, Depends On, Objective, Context, Files to Read First, Acceptance Criteria, Smoke Test, Model Assignment, Constraints
- All file paths are absolute (C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/...)
- Dependencies match scheduler_mobile_workdesk.py task registry
- All specs use "sonnet" model
- NO STUBS — all specs have real content with concrete UI requirements, data models, gesture thresholds, API endpoints, test counts

## Test Results
N/A — spec-writing task (no code to test)

## Build Verification
N/A — spec-writing task (no build artifacts)

## Acceptance Criteria
- [x] 16 spec files created in `.deia/hive/queue/backlog/`
- [x] Each spec is 50-100 lines (VERIFY specs 30-50)
- [x] Each spec has real content (not boilerplate)
- [x] "Files to Read First" lists actual source files
- [x] Dependencies match scheduler_mobile_workdesk.py
- [x] All specs use "sonnet" model
- [x] Naming: `SPEC-MW-{ID}-{short-description}.md`

## Clock / Cost / Carbon

**Clock:** 18 minutes (spec research 5min, Phase 3 writing 4min, Phase 4 writing 9min)
**Cost:** $0.085 (estimated based on token usage)
**Carbon:** 2.1g CO2e (estimated based on compute time)

## Issues / Follow-ups

### Edge Cases Identified
1. **Mobile-nav (MW-012):** Swipe velocity threshold (0.3px/ms) may need tuning based on device testing — some Android devices have different touch response
2. **Notification-pane (MW-014):** Polling interval (30s) may cause battery drain on mobile — consider SSE or WebSocket upgrade path
3. **Queue-pane (MW-019):** Cancel endpoint (`POST /build/cancel`) may not exist in hivenode yet — needs backend implementation or bus event fallback
4. **Diff-viewer (MW-020):** Syntax highlighting adds bundle size (~50KB for Prism.js) — marked as optional with graceful fallback

### Dependencies
- MW-011 depends on MW-T05, MW-V02, MW-V03 (tests must be written first per TDD)
- MW-014, MW-017, MW-020 depend on MW-V05 (mobile-nav must be complete before destination panes)
- All VERIFY specs depend on their respective BUILD specs (strict linear dependency)

### Next Tasks
- **TASK-E (Phase 5):** Generate specs for mobile CSS adaptations (MW-023 to MW-033) — 11 specs for existing primitives
- **TASK-F (Phase 6-7):** Generate specs for terminal enhancements (MW-034 to MW-036) and integration (MW-037 to MW-042) — 9 specs
- **Phase 0.5 tests:** MW-T05 to MW-T08 must be written before any Phase 3-4 BUILD tasks can start (TDD constraint)

### Codebase Observations
- **Shell.tsx** already imports `QuickActionsFAB` and `MobileNav` components (lines 23, 18) — MW-S03 likely already complete
- **build_monitor.py** has `GET /build/status` endpoint (lines 1-80) — MW-017 can use existing API without backend changes
- **Existing pane primitives:** ProgressPane, TerminalResponsePane, ChatNavigatorPane, KanbanPane show established patterns for pane structure
- **Safe area CSS:** Shell.tsx and existing CSS files should already use `env(safe-area-inset-*)` — pattern to follow for mobile-nav

### Recommendations
1. **Backend prep:** Verify `POST /build/cancel` and `GET /build/notifications` endpoints exist before dispatching MW-019 and MW-014
2. **Test infrastructure:** Ensure E2E test framework supports mobile viewport emulation and touch events before dispatching Phase 3-4 tests
3. **Bundle size:** Profile bundle size after MW-020 (diff-viewer with Prism.js) — may need code splitting
4. **Gesture conflicts:** MW-012 (swipe-back), MW-015 (swipe-dismiss), MW-022 (swipe-stage) all use swipe gestures — ensure no conflicts when panes are nested
