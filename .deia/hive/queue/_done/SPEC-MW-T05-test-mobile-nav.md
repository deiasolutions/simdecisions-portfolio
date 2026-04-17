# SPEC: TEST — Mobile-Nav Component Coverage

## Priority
P1

## Objective
Write comprehensive test suite for the MobileNav component that validates nested hub navigation, back gestures, breadcrumb trails, drill-down animations, and navigation state persistence with 100% coverage.

## Context
This is a TDD task — write tests FIRST, before implementation exists. Tests must fail initially, then pass after MW-011/MW-012/MW-013 implementation.

Test coverage must include:
- Component render: home view with hub options
- Drill-down navigation: tap hub → navigate to detail view
- Back gesture: swipe from left edge → navigate up one level
- Back button: tap back button → same as back gesture
- Breadcrumb trail: shows current path, segments tappable
- Navigation persistence: state saved to localStorage, restored on reload
- Animation: drill-down slide-in animation (200ms)
- Safe area: respects env(safe-area-inset-top) on notched devices

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-S05-mobile-nav.md` — spec to test against
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/bottom-nav/__tests__/BottomNav.test.tsx` — test patterns
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:73` — task context

## Acceptance Criteria
- [ ] Test file: `browser/src/primitives/mobile-nav/__tests__/MobileNav.test.tsx` (Jest + React Testing Library)
- [ ] 12+ test cases covering: render, drill-down, back gesture, back button, breadcrumb, persistence, animation, safe area
- [ ] Test render: home view displays hub options (Workspace, Tools, Settings)
- [ ] Test drill-down: click "Workspace" → workspace view rendered, breadcrumb shows "Home / Workspace"
- [ ] Test back gesture: swipe from left (touchstart, touchmove, touchend) → navigate to Home
- [ ] Test back button: click back button → navigate to Home
- [ ] Test breadcrumb: click "Home" in breadcrumb → jump to Home view
- [ ] Test persistence: navigate to Workspace, reload → Workspace view restored
- [ ] Test localStorage: verify `mw_nav_state` key written on navigation
- [ ] Test animation: drill-down triggers slide-in (check CSS class or transition)
- [ ] Test safe area: CSS variable env(safe-area-inset-top) applied
- [ ] Tests initially FAIL (no implementation exists yet)
- [ ] All tests use screen.getByRole, screen.getByText for queries
- [ ] No stubs in tests — real assertions with expected values

## Smoke Test
- [ ] Run `npm test MobileNav.test.tsx` → 12+ tests FAIL (component doesn't exist yet)
- [ ] Check test_render() → asserts 3 hub options visible
- [ ] Check test_drill_down() → asserts workspace view rendered after click
- [ ] Check test_back_gesture() → asserts home view restored after swipe
- [ ] Check test_persistence() → asserts localStorage updated on navigation
- [ ] All tests use descriptive names (it("should ..."))

## Model Assignment
sonnet

## Depends On
MW-S05

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/mobile-nav/__tests__/MobileNav.test.tsx` (new file)
- TDD: tests MUST be written before implementation (they will fail initially)
- Max 300 lines for test file
- Use @testing-library/react for component testing
- Use fireEvent for touch gesture simulation (touchstart, touchmove, touchend)
- Mock localStorage (jest.spyOn(Storage.prototype, 'setItem'))
- No implementation code in this task — tests only
- Tests must be runnable even if `MobileNav.tsx` doesn't exist yet (import should handle missing module gracefully)
