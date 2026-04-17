# SPEC: Notification-Pane Data Model + Home

## Priority
P2

## Depends On
MW-T06, MW-V05

## Objective
Build the notification pane data model, home view, and data fetching logic for the Mobile Workdesk. Notifications include build events (bee started, completed, failed), inventory updates, and system alerts.

## Context
The notification-pane is a destination from mobile-nav that shows build activity and system events. It must:
- Fetch notifications from hivenode API (`GET /build/notifications`)
- Store notifications in client-side state (React Context or Zustand)
- Display notifications in reverse-chronological order (newest first)
- Support notification types: build_event, inventory_update, system_alert
- Persist unread count in localStorage
- Auto-refresh every 30 seconds (polling)

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/routes/build_monitor.py` — build events API
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/progress-pane/ProgressPane.tsx` — existing build progress UI
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/state/` — state management patterns
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/infrastructure/relay_bus.ts` — bus events

## Acceptance Criteria
- [ ] `Notification` interface: id, type, title, message, timestamp, read, metadata
- [ ] `NotificationStore` with Zustand or React Context: notifications[], unreadCount, fetch(), markRead()
- [ ] `GET /build/notifications` endpoint (hivenode backend) — returns last 100 notifications
- [ ] `NotificationPane` component with home view (list of notifications)
- [ ] Reverse-chronological sort (newest first)
- [ ] Auto-refresh: polling every 30 seconds (use setInterval + cleanup)
- [ ] Notification types: build_event (bee events), inventory_update (feature added), system_alert (error)
- [ ] Unread count persisted in localStorage (`sd:notification_unread_count`)
- [ ] Loading state while fetching
- [ ] Error state if fetch fails (with retry button)
- [ ] All CSS variables only (no hardcoded colors)
- [ ] 12+ unit tests (fetch, store, types, refresh) + 3 E2E tests
- [ ] Accessible: ARIA labels, semantic HTML (ul/li)

## Smoke Test
- [ ] Open notification-pane → loading spinner, then list of notifications
- [ ] Notifications sorted newest-first (check timestamp)
- [ ] Unread count visible (badge on nav icon)
- [ ] Wait 30 seconds → auto-refresh triggered (new notifications appear)
- [ ] Offline: fetch fails → error message with "Retry" button
- [ ] Tap "Retry" → fetch retries

## Model Assignment
sonnet

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/notification-pane/NotificationPane.tsx` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/notification-pane/notificationStore.ts` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/routes/notifications.py` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/notification-pane/__tests__/NotificationPane.test.tsx`
- TDD: tests first
- Max 300 lines for pane
- Max 150 lines for store
- Max 200 lines for backend endpoint
- Max 200 lines for tests
- Use Zustand (not Redux) for state management
- localStorage key: `sd:notification_unread_count`
