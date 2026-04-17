# SPEC: TEST — Queue-Pane Component Coverage

## Priority
P1

## Objective
Write comprehensive test suite for the QueuePane component that validates queue status rendering, tap actions, pull-to-refresh, polling, and modal displays with 100% coverage.

## Context
This is a TDD task — write tests FIRST, before implementation exists. Tests must fail initially, then pass after MW-017/MW-018/MW-019 implementation.

Test coverage must include:
- Component render: status list with active, queued, completed, failed sections
- Status indicators: spinner for active, clock for queued, checkmark for done, X for failed
- Tap actions: tap active → modal with bee logs, tap queued → modal with spec content, tap failed → modal with error
- Pull-to-refresh: gesture triggers status refresh
- Polling: auto-refresh every 15 seconds
- Empty state: "Queue is empty" message
- Section collapsing: collapsible headers for Active, Queued, Completed
- Accessibility: ARIA labels, focus management in modals

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-S07-queue-pane.md` — spec to test against
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/progress-pane/__tests__/ProgressPane.test.tsx` — test patterns (if exists)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:75` — task context

## Acceptance Criteria
- [ ] Test file: `browser/src/primitives/queue-pane/__tests__/QueuePane.test.tsx` (Jest + React Testing Library)
- [ ] 8+ test cases covering: render, indicators, tap actions, pull-to-refresh, polling, empty, collapse, a11y
- [ ] Test render: sections for Active (3), Queued (5), Completed (10), Failed (1)
- [ ] Test indicators: active shows spinner, queued shows clock, done shows checkmark, failed shows X
- [ ] Test tap active: click active spec → modal opens with bee logs
- [ ] Test tap queued: click queued spec → modal opens with spec content
- [ ] Test tap failed: click failed spec → modal opens with error details
- [ ] Test pull-to-refresh: swipe down gesture → loading indicator, fetch called
- [ ] Test polling: jest.useFakeTimers() → advance 15s → fetch called again
- [ ] Test empty state: 0 specs → "Queue is empty" message displayed
- [ ] Tests initially FAIL (no implementation exists yet)
- [ ] All tests use screen.getByRole, screen.getByText for queries
- [ ] No stubs in tests — real assertions with expected values

## Smoke Test
- [ ] Run `npm test QueuePane.test.tsx` → 8+ tests FAIL (component doesn't exist yet)
- [ ] Check test_render() → asserts 3 active, 5 queued, 10 completed specs
- [ ] Check test_indicators() → asserts spinner present for active spec
- [ ] Check test_tap_active() → asserts modal opened with logs
- [ ] Check test_polling() → asserts fetch called after 15s
- [ ] All tests use descriptive names (it("should ..."))

## Model Assignment
sonnet

## Depends On
MW-S07

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/queue-pane/__tests__/QueuePane.test.tsx` (new file)
- TDD: tests MUST be written before implementation (they will fail initially)
- Max 250 lines for test file
- Use @testing-library/react for component testing
- Use jest.useFakeTimers() for polling tests
- Use fireEvent for pull-to-refresh gesture simulation
- Mock fetch API for /build/status endpoint
- No implementation code in this task — tests only
- Tests must be runnable even if `QueuePane.tsx` doesn't exist yet (import should handle missing module gracefully)
