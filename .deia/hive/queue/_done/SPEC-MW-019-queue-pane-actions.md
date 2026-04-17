# SPEC: Queue-Pane Tap Actions

## Priority
P2

## Depends On
MW-018

## Objective
Implement tap actions for queue pane tasks: view details, cancel task (active only), retry task (failed only), and view response file (complete only).

## Context
Tasks in the queue-pane should be actionable:
- Tap task card → expand/collapse details (from MW-018)
- Long-press or swipe-left → action menu (Cancel, Retry, View Response)
- Cancel: only available for active tasks (POST /build/cancel)
- Retry: only available for failed tasks (re-dispatch to queue)
- View Response: only available for complete tasks (navigate to response file)
- Confirmation dialog for destructive actions (Cancel)

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/queue-pane/QueuePane.tsx` — pane from MW-017/018
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/queue-pane/queueStore.ts` — store from MW-017
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/routes/build_monitor.py` — cancel endpoint (if exists)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/infrastructure/relay_bus.ts` — bus events

## Acceptance Criteria
- [ ] Long-press task card → action menu appears (Cancel, Retry, View Response)
- [ ] Action menu visibility based on task status:
  - Active tasks: Cancel only
  - Failed tasks: Retry only
  - Complete tasks: View Response only
  - Queued tasks: Cancel only
- [ ] Cancel action: POST /build/cancel (if endpoint exists) or bus event, show confirmation dialog
- [ ] Retry action: re-dispatch task to queue (POST /build/retry or manual dispatch)
- [ ] View Response action: navigate to response file (e.g., `.deia/hive/responses/TASK-ID-RESPONSE.md`)
- [ ] Confirmation dialog for Cancel: "Cancel task MW-123?" with Yes/No buttons
- [ ] Action feedback: toast message on success ("Task cancelled"), error toast on failure
- [ ] All CSS variables only (no hardcoded colors)
- [ ] 10+ unit tests (action menu, cancel, retry, view response) + 2 E2E tests
- [ ] Accessible: action menu is keyboard-accessible, ARIA labels

## Smoke Test
- [ ] Long-press active task → action menu shows "Cancel"
- [ ] Tap "Cancel" → confirmation dialog appears
- [ ] Tap "Yes" → task cancelled, toast "Task cancelled"
- [ ] Long-press failed task → action menu shows "Retry"
- [ ] Tap "Retry" → task re-dispatched to queue
- [ ] Long-press complete task → action menu shows "View Response"
- [ ] Tap "View Response" → navigate to response file

## Model Assignment
sonnet

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/queue-pane/QueuePane.tsx` (modify)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/queue-pane/queueStore.ts` (modify — add cancel/retry methods)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/queue-pane/__tests__/QueuePane.test.tsx` (modify)
- Backend: if `POST /build/cancel` does not exist, create it in `build_monitor.py`
- TDD: tests first
- Max 150 lines of changes to QueuePane.tsx
- Max 100 lines of changes to queueStore.ts
- Max 50 lines for cancel endpoint (if needed)
- Long-press: 500ms threshold (use setTimeout + cleanup)
- Confirmation dialog: use native confirm() or custom modal
