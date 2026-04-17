# SPEC: RTD Bus Integration for New Mobile Primitives

## Priority
P2

## Objective
Wire the new mobile primitives (quick-actions-fab, mobile-nav, notification-pane, queue-pane, diff-viewer) to the RTD (Relay Transit Dispatch) bus system for inter-component communication. Implements subscribe/publish patterns for bus events, ensuring components react to state changes and emit events for cross-primitive coordination.

## Context
The RTD bus is ShiftCenter's event system for decoupled component communication (similar to Redux middleware or EventEmitter). Components subscribe to bus events (e.g., `prism:result`) and publish events (e.g., `terminal:suggest`). This spec integrates the 5 new mobile primitives into the bus so they can participate in the Mobile Workdesk workflow.

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/infrastructure/relay_bus.ts` — RTD bus implementation (if exists, else find equivalent)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/Shell.tsx` — Shell uses MessageBus + ShellCtx
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/terminal/TerminalApp.tsx` — example bus subscriber
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-038-workdesk-egg.md` — EGG permissions (bus_emit, bus_receive)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:155` — task context in scheduler

## Dependencies
- MW-V08 (diff-viewer must be verified before integration)

## Acceptance Criteria
- [ ] QuickActionsFAB integration:
  - Publish: `voice:start`, `voice:stop`, `command:show-palette`
  - Subscribe: `voice:active`, `command:executing`
- [ ] MobileNav integration:
  - Publish: `nav:navigate`, `nav:back`, `nav:home`
  - Subscribe: `shell:pane-activated`, `shell:tab-changed`
- [ ] NotificationPane integration:
  - Publish: `notification:dismiss`, `notification:navigate`
  - Subscribe: `notification:new`, `shell:alert`, `queue:status-changed`
- [ ] QueuePane integration:
  - Publish: `queue:cancel`, `queue:retry`, `queue:navigate`
  - Subscribe: `queue:status-changed`, `queue:task-complete`, `queue:task-failed`
- [ ] DiffViewer integration:
  - Publish: `diff:expand`, `diff:collapse`, `diff:apply`
  - Subscribe: `diff:show`, `queue:task-complete` (auto-show diffs for completed tasks)
- [ ] All primitives use `useContext(ShellCtx)` or `useBus()` hook to access bus
- [ ] Event payloads follow schema: `{ type: string, payload: any, source: string, timestamp: number }`
- [ ] All bus events logged in dev mode (console.debug)
- [ ] 15+ integration tests covering event flows (React Testing Library + mock bus)

## Smoke Test
- [ ] Click FAB mic button → publishes `voice:start` → terminal subscribes, shows voice UI
- [ ] Queue task completes → publishes `queue:task-complete` → DiffViewer subscribes, shows diff
- [ ] Click notification → publishes `notification:navigate` → MobileNav subscribes, navigates to target pane
- [ ] 15+ tests pass covering all subscribe/publish patterns

## Model Assignment
sonnet

## Constraints
- Location: modify each primitive component to add bus integration:
  - `browser/src/primitives/quick-actions-fab/QuickActionsFAB.tsx`
  - `browser/src/shell/components/MobileNav.tsx`
  - `browser/src/primitives/notification-pane/NotificationPane.tsx` (create if new)
  - `browser/src/primitives/queue-pane/QueuePane.tsx` (create if new)
  - `browser/src/primitives/diff-viewer/DiffViewer.tsx` (create if new)
- Use existing bus patterns from Shell.tsx and TerminalApp.tsx
- No new bus infrastructure (use MessageBus from Shell.tsx)
- Max 50 lines added per component for bus integration
- Max 200 lines for integration tests
- TDD: tests first, then implementation
