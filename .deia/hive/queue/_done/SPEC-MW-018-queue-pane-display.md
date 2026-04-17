# SPEC: Queue-Pane State Display

## Priority
P2

## Depends On
MW-017

## Objective
Build the visual display for queue pane tasks, including status indicators (running, queued, complete, failed), progress bars for active tasks, and metadata display (bee_id, cost, tokens, duration).

## Context
Each task in the queue-pane needs visual representation:
- Status indicator: color-coded icon/badge (green = complete, blue = running, yellow = queued, red = failed)
- Progress bar for active tasks (if duration estimate available)
- Metadata: bee_id, cost ($0.042), tokens (5.2K), duration (2.5h)
- Expandable details: tap to expand full task details (logs, files touched, errors)
- Responsive layout: card-based on mobile, table-based on desktop

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/queue-pane/QueuePane.tsx` — pane from MW-017
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/progress-pane/ProgressPane.tsx` — existing progress UI patterns
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/constants.ts` — color constants (CSS variables)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/routes/build_monitor.py` — task data structure

## Acceptance Criteria
- [ ] `QueueTaskCard` component: displays task with status, metadata, progress
- [ ] Status indicator: icon + badge with color (green/blue/yellow/red)
- [ ] Progress bar for active tasks: percentage complete (0-100%), indeterminate if estimate unavailable
- [ ] Metadata display: bee_id, cost (formatted $0.042), tokens (formatted 5.2K), duration (formatted 2.5h)
- [ ] Expandable details: tap card → expand to show logs, files touched, errors
- [ ] Collapse: tap expanded card → collapse to summary view
- [ ] Responsive: card layout on mobile (<768px), table layout on desktop (>=768px)
- [ ] Loading skeleton while fetching (ghost cards)
- [ ] Empty state: "No tasks in queue" message when list is empty
- [ ] All CSS variables only (no hardcoded colors)
- [ ] 10+ unit tests (card rendering, expand/collapse, metadata formatting) + 2 E2E tests
- [ ] Accessible: status has aria-label, expandable cards use aria-expanded

## Smoke Test
- [ ] Open queue-pane → tasks render as cards (mobile) or table rows (desktop)
- [ ] Active task: status indicator is blue, progress bar shows percentage
- [ ] Complete task: status indicator is green, no progress bar
- [ ] Failed task: status indicator is red, error message visible
- [ ] Tap task card → expands to show full details (logs, files)
- [ ] Tap expanded card → collapses to summary

## Model Assignment
sonnet

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/queue-pane/QueuePane.tsx` (modify)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/queue-pane/QueueTaskCard.tsx` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/queue-pane/__tests__/QueueTaskCard.test.tsx`
- TDD: tests first
- Max 250 lines for QueueTaskCard component
- Max 100 lines for card CSS
- Max 150 lines for tests
- Use React.memo for performance (list virtualization if >100 tasks)
- Status colors must use CSS variables (--sd-status-*)
- Metadata formatting: use Intl.NumberFormat for currency/numbers
