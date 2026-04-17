# SPEC: Queue-Pane Hivenode Fetch

## Priority
P2

## Depends On
MW-T07, MW-V05

## Objective
Build the queue pane data fetching logic that connects to the hivenode build monitor API (`GET /build/status`) and displays active, queued, and completed tasks in the Mobile Workdesk.

## Context
The queue-pane shows the current build queue state:
- Active tasks (currently running bees)
- Queued tasks (waiting for slot)
- Completed tasks (done in last 24 hours)
- Failed tasks (errors in last 24 hours)

The pane must fetch from `GET /build/status` and support:
- Auto-refresh every 10 seconds (polling)
- Manual refresh (pull-to-refresh gesture on mobile)
- Filtering by task status (active, queued, complete, failed)
- Sorting by start time (newest first)

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/routes/build_monitor.py` — build status API
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/progress-pane/ProgressPane.tsx` — existing build progress UI
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/state/` — state management patterns
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/infrastructure/relay_bus.ts` — bus events

## Acceptance Criteria
- [ ] `QueueTask` interface: id, spec_id, status, bee_id, started_at, completed_at, cost, tokens
- [ ] `QueueStore` with Zustand: tasks[], fetch(), refresh(), filterByStatus()
- [ ] `GET /build/status` integration (use existing endpoint, no backend changes needed)
- [ ] `QueuePane` component with task list view
- [ ] Auto-refresh: polling every 10 seconds (use setInterval + cleanup)
- [ ] Manual refresh: pull-to-refresh gesture (swipe down from top)
- [ ] Filter tabs: All, Active, Queued, Complete, Failed
- [ ] Sort by start time: newest first (reverse-chronological)
- [ ] Loading state while fetching
- [ ] Error state if fetch fails (with retry button)
- [ ] All CSS variables only (no hardcoded colors)
- [ ] 12+ unit tests (fetch, store, filter, refresh) + 3 E2E tests
- [ ] Accessible: ARIA labels, semantic HTML (table or ul/li)

## Smoke Test
- [ ] Open queue-pane → loading spinner, then list of tasks
- [ ] Tasks sorted newest-first (check started_at timestamp)
- [ ] Filter by "Active" → only active tasks visible
- [ ] Wait 10 seconds → auto-refresh triggered (new tasks appear)
- [ ] Pull down from top → manual refresh triggered (loading indicator)
- [ ] Offline: fetch fails → error message with "Retry" button

## Model Assignment
sonnet

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/queue-pane/QueuePane.tsx` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/queue-pane/queueStore.ts` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/queue-pane/__tests__/QueuePane.test.tsx`
- No backend changes — use existing `GET /build/status` endpoint
- TDD: tests first
- Max 300 lines for pane
- Max 150 lines for store
- Max 200 lines for tests
- Use Zustand (not Redux) for state management
- Pull-to-refresh: use native CSS overscroll-behavior or custom TouchEvent hook
