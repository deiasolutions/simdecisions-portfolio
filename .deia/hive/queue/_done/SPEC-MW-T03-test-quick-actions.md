# SPEC: TEST — Quick-Actions FAB Component Coverage

## Priority
P1

## Objective
Write comprehensive test suite for the QuickActionsFAB component that validates button states, menu expansion, keyboard shortcuts, touch targets, and safe area handling with 100% coverage.

## Context
This is a TDD task — write tests FIRST, before implementation exists. Tests must fail initially, then pass after MW-006/MW-007 implementation.

Test coverage must include:
- Component render: FAB visible bottom-right, "+" icon
- Menu expansion: tap FAB → menu expands with 3 buttons (mic, palette, settings)
- Button actions: tap mic → voice-input starts, tap palette → command palette opens, tap settings → settings pane opens
- Keyboard shortcuts: Ctrl+Space → mic, Ctrl+K → palette, Ctrl+, → settings
- Touch targets: all buttons ≥48px tap target
- Accessibility: ARIA labels, keyboard navigation
- Safe area: respects env(safe-area-inset-bottom) on notched devices
- Animation: menu expansion animates smoothly (200ms spring)

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-S03-quick-actions.md` — spec to test against
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/quick-actions-fab/QuickActionsFAB.tsx` — component structure (if exists)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/command-palette/__tests__/CommandPalette.test.tsx` — test patterns
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:71` — task context

## Acceptance Criteria
- [ ] Test file: `browser/src/primitives/quick-actions-fab/__tests__/QuickActionsFAB.test.tsx` (Jest + React Testing Library)
- [ ] 10+ test cases covering: render, expand, buttons, keyboard, touch, a11y, safe area, animation
- [ ] Test render: FAB visible, "+" icon present, positioned bottom-right
- [ ] Test expansion: click FAB → menu visible, 3 buttons rendered (mic, palette, settings)
- [ ] Test button actions: click mic → onMicClick called, click palette → onPaletteClick called, click settings → onSettingsClick called
- [ ] Test keyboard shortcuts: fireEvent.keyDown(Ctrl+Space) → onMicClick, fireEvent.keyDown(Ctrl+K) → onPaletteClick
- [ ] Test touch targets: measure button dimensions ≥48px x 48px
- [ ] Test accessibility: ARIA labels present, tab navigation works
- [ ] Test safe area: CSS variable env(safe-area-inset-bottom) applied
- [ ] Test animation: menu expansion duration ~200ms (use jest.useFakeTimers)
- [ ] Tests initially FAIL (no implementation exists yet)
- [ ] All tests use screen.getByRole, screen.getByLabelText for queries
- [ ] No stubs in tests — real assertions with expected values

## Smoke Test
- [ ] Run `npm test QuickActionsFAB.test.tsx` → 10+ tests FAIL (component doesn't exist yet)
- [ ] Check test_render() → asserts FAB button exists
- [ ] Check test_expansion() → asserts 3 buttons visible after click
- [ ] Check test_mic_button() → asserts onMicClick called
- [ ] Check test_keyboard_shortcut() → asserts Ctrl+Space triggers mic action
- [ ] All tests use descriptive names (it("should ..."))

## Model Assignment
sonnet

## Depends On
MW-S03

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/quick-actions-fab/__tests__/QuickActionsFAB.test.tsx` (new file)
- TDD: tests MUST be written before implementation (they will fail initially)
- Max 250 lines for test file
- Use @testing-library/react for component testing
- Use jest.useFakeTimers() for animation timing tests
- No implementation code in this task — tests only
- Tests must be runnable even if `QuickActionsFAB.tsx` doesn't exist yet (import should handle missing module gracefully)
