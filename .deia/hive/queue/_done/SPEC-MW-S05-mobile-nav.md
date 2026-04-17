# SPEC: Mobile-Nav Nested Hub Navigation

## Priority
P1

## Objective
Design a mobile navigation component with nested hub structure, back gesture support, drill-down navigation, and FAB integration for the Mobile Workdesk.

## Context
The mobile-nav replaces the desktop menu-bar with a mobile-optimized navigation hierarchy. It must:
- Use nested hub structure: Home → Apps → Specific App → Sub-view
- Support back gesture (swipe from left edge) and back button
- Integrate with FAB for quick actions at any nav level
- Show breadcrumb trail at top (collapsible on scroll)
- Persist navigation state across sessions (localStorage)

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/bottom-nav/BottomNav.tsx` — existing nav patterns
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/menu-bar/MenuBar.tsx` — desktop navigation structure
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/Shell.tsx` — shell integration points
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:61` — task context

## Acceptance Criteria
- [ ] `MobileNav` component with nested hub structure
- [ ] Navigation levels: Home (landing) → Hubs (Workspace, Tools, Settings) → Detail views
- [ ] Back gesture: swipe from left edge (TouchEvent with deltaX threshold 50px) → navigate up one level
- [ ] Back button: fixed top-left, shows current depth indicator (e.g., "← Workspace / Files")
- [ ] Breadcrumb trail: collapsible bar at top, shows full path, each segment tappable
- [ ] FAB integration: FAB visible at all nav levels, context-aware actions
- [ ] Drill-down animation: slide-in from right (200ms ease-out)
- [ ] Navigation state persistence: save/restore current path to localStorage `mw_nav_state`
- [ ] Safe area aware: respects notched devices (env(safe-area-inset-top))
- [ ] Accessibility: ARIA navigation landmarks, focus management on nav change
- [ ] 12+ unit tests + 2 E2E tests (drill-down, back gesture, breadcrumb navigation)

## Smoke Test
- [ ] Open Mobile Workdesk → Home view renders with hub options
- [ ] Tap "Workspace" hub → drill-down animation, workspace view appears
- [ ] Swipe from left edge → back gesture triggers, return to Home
- [ ] Tap back button → same result as swipe
- [ ] Tap breadcrumb segment ("Home") → jump directly to Home
- [ ] Reload page → navigation state restored (last viewed hub)

## Model Assignment
sonnet

## Depends On
None (Phase 0 spec)

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/mobile-nav/MobileNav.tsx` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/mobile-nav/mobile-nav.css` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/mobile-nav/__tests__/MobileNav.test.tsx`
- TDD: tests first
- Max 400 lines for component
- Max 120 lines for CSS
- Max 180 lines for tests
- CSS variables only, no hardcoded colors
- No external routing libs — manual state management with history API
- No stubs — full navigation logic with gesture handling
