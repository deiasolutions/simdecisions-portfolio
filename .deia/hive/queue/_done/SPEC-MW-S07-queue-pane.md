# SPEC: Queue-Pane Hivenode Status Display

## Priority
P1

## Objective
Design a queue pane component for the Mobile Workdesk that fetches and displays hivenode build queue status, active bees, and spec task states with tap-to-view-details and tap-to-cancel actions.

## Context
The queue-pane is a destination hub in mobile-nav that shows real-time build queue state:
- Active specs (currently being processed by bees)
- Queued specs (waiting for dispatch)
- Completed specs (last 20)
- Failed specs (with error messages)

It must support:
- Tap on active spec → view bee logs in modal
- Tap on queued spec → view spec file content
- Tap on failed spec → view error details
- Pull-to-refresh for manual status update

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/routes/build_routes.py` — `/build/status` endpoint
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/progress-pane/ProgressPane.tsx` — progress display patterns
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/scripts/queue/run_queue.py` — queue runner state format
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:63` — task context

## Acceptance Criteria
- [ ] `QueuePane` component with status list rendering
- [ ] Data model: `{ spec_id, status: "active" | "queued" | "done" | "failed", bee_id, started_at, duration }`
- [ ] Section headers: Active (collapsible), Queued (collapsible), Completed (last 20), Failed
- [ ] Status indicators: spinner for active, clock for queued, checkmark for done, X for failed
- [ ] Tap on active spec → open modal with streaming bee logs
- [ ] Tap on queued spec → open modal with spec file content (markdown)
- [ ] Tap on failed spec → open modal with error traceback
- [ ] Pull-to-refresh: gesture to manually fetch latest queue status
- [ ] Polling: auto-refresh every 15 seconds
- [ ] Empty state: "Queue is empty" with friendly icon
- [ ] Accessibility: ARIA labels for status icons, focus management in modals
- [ ] 8+ unit tests + 2 E2E tests (tap-to-view, pull-to-refresh, polling)

## Smoke Test
- [ ] Open queue pane → status list renders with 3 active, 5 queued, 10 completed
- [ ] Active spec shows spinner + bee ID + elapsed time
- [ ] Tap active spec → modal opens with streaming bee logs
- [ ] Tap queued spec → modal opens with spec file markdown
- [ ] Pull down to refresh → loading indicator, status updates
- [ ] Failed spec shows error icon + "View error" button

## Model Assignment
sonnet

## Depends On
None (Phase 0 spec)

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/queue-pane/QueuePane.tsx` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/queue-pane/queue-pane.css` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/queue-pane/__tests__/QueuePane.test.tsx`
- TDD: tests first
- Max 400 lines for component
- Max 100 lines for CSS
- Max 150 lines for tests
- CSS variables only, no hardcoded colors
- No external data fetching libs — use fetch API directly
- No stubs — full modal logic with log streaming
