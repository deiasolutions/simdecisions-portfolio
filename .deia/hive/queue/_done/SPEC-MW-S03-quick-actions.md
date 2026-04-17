# SPEC: Quick-Actions FAB Component

## Priority
P1

## Objective
Design a floating action button (FAB) component for the Mobile Workdesk that exposes quick-action buttons: microphone (trigger voice-input), keyboard (trigger command-palette), and expanded menu for power actions.

## Context
The FAB is the primary interaction point on mobile. It must be:
- Fixed position, bottom-right (respects safe area on notched devices)
- Expandable menu with label-only + icon buttons
- Accessible from any view (nav, pane, modal overlay)
- Touch-optimized tap targets (48px minimum)
- Keyboard shortcuts support (Ctrl+Space for mic, Ctrl+K for palette)

Files to read first:
- `browser/src/primitives/settings/settingsStore.ts` — settings/keyboard mapping pattern
- `browser/src/shell/Shell.tsx` — layout structure and z-index considerations
- Material Design FAB guidelines (https://material.io/components/buttons-floating-action-button)
- `browser/src/hooks/useVoiceInput.ts` — voice-input integration (from MW-S02)

## Acceptance Criteria
- [ ] `QuickActionsFAB` component (mobile-specific variant)
- [ ] Primary FAB button: "+" icon, centered bottom-right with 16px margin + safe area
- [ ] Expanded menu with 3+ quick actions: Mic (voice-input), Palette (command), Settings
- [ ] Menu animation: spring easing, 200ms duration, labeled buttons visible on expand
- [ ] Mic button: triggers `useVoiceInput()` hook, visual feedback while listening
- [ ] Keyboard button: triggers CommandPalette globally (via useCommandPalette hook)
- [ ] Settings button: navigates to settings pane/modal
- [ ] Keyboard shortcuts: Ctrl+Space (mic), Ctrl+K (palette), Ctrl+, (settings)
- [ ] Touch-optimized: 48px minimum tap target, enough padding between buttons
- [ ] Safe area aware: respects notched devices (env(safe-area-inset-*))
- [ ] All CSS variables only, no hardcoded colors
- [ ] 10+ unit tests (button states, animations, keyboard) + 2 E2E tests
- [ ] Accessible: ARIA labels, focusable, keyboard navigable menu

## Smoke Test
- [ ] On mobile viewport: FAB visible bottom-right with "+" icon
- [ ] Tap/click FAB → menu expands with 3 buttons (mic, palette, settings)
- [ ] Tap mic → voice-input starts, visual feedback (mic icon highlights)
- [ ] Tap palette → command palette opens
- [ ] Tap settings → settings pane opens
- [ ] Keyboard: Ctrl+Space → voice-input starts

## Model Assignment
sonnet

## Constraints
- Location: `browser/src/primitives/quick-actions-fab/QuickActionsFAB.tsx` (new file)
- Location: `browser/src/primitives/quick-actions-fab/quick-actions-fab.css` (new file)
- Location: `browser/src/primitives/quick-actions-fab/__tests__/QuickActionsFAB.test.tsx`
- TDD: tests first
- No material-ui or external component libs — CSS-only animation
- Max 250 lines for component
- Max 100 lines for CSS
- Max 150 lines for tests
- Use React.memo for performance
- No stubs — full implementation with all actions wired
- Safe area CSS: env(safe-area-inset-bottom) used correctly
