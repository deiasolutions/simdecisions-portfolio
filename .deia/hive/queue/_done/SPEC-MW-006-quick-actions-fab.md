# SPEC: Quick-Actions FAB Component

## Priority
P1

## Depends On
MW-T03, MW-V01

## Objective
Build the Floating Action Button (FAB) component for Mobile Workdesk. This is the primary entry point for quick actions: voice input, keyboard shortcuts, and common commands.

## Context
The FAB is a circular button fixed to the bottom-right of the mobile screen. It:
- Expands to show quick action buttons (mic, keyboard, common commands)
- Uses spring animations for smooth open/close
- Integrates with command-interpreter for action execution
- Follows Material Design FAB patterns with ShiftCenter styling

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/` — existing primitive patterns
- Look for existing button components to reuse styling

## Acceptance Criteria
- [ ] `QuickActions.tsx` component in `browser/src/primitives/quick-actions/`
- [ ] FAB button fixed to bottom-right with `position: fixed` and safe area insets
- [ ] Expand/collapse animation using CSS transitions or Framer Motion
- [ ] Expanded state shows 3-5 action buttons (mic, keyboard, recent commands)
- [ ] Collapsed state shows single FAB icon (plus or menu icon)
- [ ] Click outside to close expanded FAB
- [ ] Swipe down gesture to close (mobile-friendly)
- [ ] Accessibility: keyboard navigation, ARIA labels, focus management
- [ ] Styling: CSS variables only (no hardcoded colors), mobile-first responsive
- [ ] Z-index management: FAB above other content but below modals
- [ ] Component tests: 10+ tests covering expand, collapse, click, keyboard, accessibility
- [ ] Visual polish: shadow, hover states, active states

## Smoke Test
- [ ] Render `<QuickActions />` — FAB visible bottom-right
- [ ] Click FAB → expands to show action buttons
- [ ] Click outside → FAB collapses
- [ ] Click mic button → triggers voice input (integration tested in MW-007)
- [ ] Run `npm test QuickActions.test.tsx` — all tests pass

## Model Assignment
sonnet

## Constraints
- Location: `browser/src/primitives/quick-actions/QuickActions.tsx` (new file)
- Location: `browser/src/primitives/quick-actions/QuickActions.test.tsx` (new file)
- Location: `browser/src/primitives/quick-actions/QuickActions.css` (new file)
- TDD: Write tests first
- CSS variables only (no hardcoded colors)
- Max 300 lines for component
- Max 200 lines for tests
- Max 150 lines for CSS
- NO STUBS — full animation and interaction implementation
- Must work on touch devices (not just mouse)
