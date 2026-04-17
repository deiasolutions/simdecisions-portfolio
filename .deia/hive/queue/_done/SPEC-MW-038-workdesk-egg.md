# SPEC: Mobile Workdesk EGG Configuration

## Priority
P2

## Objective
Author the `workdesk.set.md` EGG configuration file that composes all Mobile Workdesk primitives (command-interpreter, voice-input, quick-actions-fab, conversation-pane, mobile-nav, notification-pane, queue-pane, diff-viewer) into a working mobile product. Defines layout, permissions, UI config, and default tabs.

## Context
EGG files (.set.md) are ShiftCenter's product configuration format. They define the layout tree (split panes, tabs), permissions (bus events, storage, network), UI chrome mode, and metadata. The Mobile Workdesk EGG assembles all primitives built in Phases 1-5 into a cohesive mobile experience.

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/eggs/apps.set.md` — example EGG config (App Directory)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/eggs/canvas.set.md` — example multi-pane layout
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/eggs/build-monitor.set.md` — example with polling and bus events
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:154` — task context in scheduler

## Dependencies
- MW-037 (Shell.tsx responsive wiring must be complete)

## Acceptance Criteria
- [ ] File: `eggs/workdesk.set.md` with YAML frontmatter + markdown body + code fences
- [ ] Frontmatter:
  - `egg: workdesk`, `version: 0.1.0`, `schema_version: 3`
  - `displayName: Mobile Workdesk`, `author: daaaave-atx`, `license: MIT`
  - `defaultRoute: /workdesk`, `auth: required`, `_stub: false`
- [ ] Layout (```layout``` code fence): JSON tree with 4 main sections:
  - Top: conversation-pane (1fr)
  - Middle: terminal with suggestion pills (300px)
  - Bottom tabs: [notification-pane, queue-pane, diff-viewer] (250px)
  - Overlay: quick-actions-fab (floating)
- [ ] UI config (```ui``` code fence):
  - `chromeMode: "minimal"` (hides menu-bar on mobile, uses drawer)
  - `commandPalette: true`, `akk: true`
  - `mobileNav: true` (enables MobileNav component)
- [ ] Tabs (```tabs``` code fence): 4 tabs
  - "Conversation" (conversation-pane, active)
  - "Notifications" (notification-pane)
  - "Queue" (queue-pane)
  - "Diffs" (diff-viewer)
- [ ] Permissions (```permissions``` code fence):
  - `storage: { localStorage: true, sessionStorage: true }`
  - `network: { allowedDomains: ["localhost", "hivenode.railway.app"] }`
  - `bus_emit: ["prism:ir", "voice:start", "voice:stop", "terminal:suggest"]`
  - `bus_receive: ["prism:result", "voice:transcript", "terminal:history"]`
- [ ] Settings (```settings``` code fence):
  - `voiceEnabled: true`, `suggestionsEnabled: true`, `autoExecuteThreshold: 0.9`
- [ ] Markdown body: 3-4 paragraphs describing the Mobile Workdesk product (purpose, features, workflow)
- [ ] EGG loads successfully (test via egg-loader)

## Smoke Test
- [ ] File exists at `eggs/workdesk.set.md`
- [ ] YAML frontmatter parses without errors
- [ ] Layout JSON is valid (no syntax errors)
- [ ] Load EGG in ShiftCenter: `/workdesk` route renders Mobile Workdesk layout
- [ ] All 4 tabs render and switch correctly
- [ ] QuickActionsFAB appears in mobile viewport
- [ ] MobileNav appears in mobile viewport
- [ ] No console errors on load

## Model Assignment
sonnet

## Constraints
- Location: `eggs/workdesk.set.md` (new file)
- Schema version: 3 (current EGG schema)
- Layout: must be valid JSON (use JSON.parse to verify)
- All pane types must exist: conversation-pane, notification-pane, queue-pane, diff-viewer, terminal
- Permissions: follow principle of least privilege (only emit/receive necessary bus events)
- Max 150 lines total (frontmatter + layout + markdown)
- Reference existing EGG files for format/structure
