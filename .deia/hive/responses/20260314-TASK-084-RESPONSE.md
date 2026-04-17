# TASK-084: Expandable Input Overlay -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku 4.5
**Date:** 2026-03-14

## Files Modified

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts` - Added `expandMode?: 'expand-up' | 'fixed'` to TerminalEggConfig
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalPrompt.tsx` - Added expand props, expand logic effect
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalApp.tsx` - Added expand state, pass-through, submit handler reset
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminal.css` - Added expand-up overlay styles
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\TerminalPrompt.expand.test.tsx` - Created new test file (8 tests)
6. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\TerminalApp.expand.test.tsx` - Created new test file (9 tests)

## What Was Done

- **Type Definition Update:** Added `expandMode?: 'expand-up' | 'fixed'` to TerminalEggConfig with JSDoc describing expand-up overlay behavior and fixed default
- **TerminalPrompt.tsx Changes:**
  - Added 3 new props to interface: `expandMode`, `inputExpanded`, `setInputExpanded`
  - Added default values: `expandMode = 'fixed'`, `inputExpanded = false`
  - Implemented useEffect hook that counts lines using regex `(value.match(/\n/g) || []).length + 1`
  - Effect triggers `setInputExpanded(true)` when lineCount > 3 in expand-up mode, `false` otherwise
  - Effect includes early returns for safety: skips if not expand-up mode or setter not provided
- **TerminalApp.tsx Changes:**
  - Added `useState(false)` for `inputExpanded` state
  - Extracted `expandMode = eggConfig?.expandMode || 'fixed'` with default
  - Added `data-input-expanded` attribute to `.terminal-prompt-area` div with state value
  - Wrapped `terminal.handleSubmit()` in custom callback that calls `setInputExpanded(false)` first
  - Passed `expandMode`, `inputExpanded`, `setInputExpanded` to TerminalPrompt component
- **CSS Changes in terminal.css:**
  - Added base transition to `.terminal-prompt-area`: `transition: position 0.15s ease, max-height 0.15s ease, box-shadow 0.15s ease`
  - Added `.terminal-prompt-area[data-input-expanded="true"]` rule with:
    - `position: absolute` (overlay mode)
    - `bottom: 0`, `left: 0`, `right: 0` (full-width positioning)
    - `z-index: 100` (overlay above siblings)
    - `max-height: 50vh` (50% viewport constraint)
    - `overflow-y: auto` (scrollable when needed)
    - `box-shadow: 0 -4px 12px var(--sd-shadow-lg)` (visual emphasis)
- **Tests Written:**
  - TerminalPrompt.expand.test.tsx: 8 tests covering expand logic, fixed mode, line counting, edge cases
  - TerminalApp.expand.test.tsx: 9 tests covering prop passing, state initialization, mode handling
  - Total: 17 new tests for expand feature

## Test Results

**Terminal Test Suite Summary:**
- Test Files: 16 passed (2 new expand test files added)
- Total Tests: 152 passed (17 new tests + 135 existing)
- Duration: 30.12s
- All tests green, no failures

**Specific Expand Tests:**
- TerminalPrompt.expand.test.tsx: 8/8 passed (100%)
- TerminalApp.expand.test.tsx: 9/9 passed (100%)

Key test scenarios verified:
- Fixed mode never expands (regardless of line count)
- Expand-up mode expands when lines > 3
- Expand-up mode collapses when lines <= 3
- Expand state resets on submit
- CSS classes applied correctly
- Edge cases handled (empty text, undefined setter, wrong mode)

## Build Verification

```
> npm test -- --run src/primitives/terminal/

Test Files: 16 passed (16)
Tests: 152 passed (152)
Duration: 30.12s
No failures, no errors
```

All existing terminal tests continue to pass. No regressions introduced.

## Acceptance Criteria

- [x] Terminal input expands upward when text exceeds 3 lines
- [x] Expansion overlays the neighboring pane (position: absolute, z-index above sibling)
- [x] Maximum expansion: 50% of viewport height (50vh)
- [x] Input collapses back to normal height on submit (Enter or send button)
- [x] Smooth CSS transition on expand/collapse (150ms ease)
- [x] Works in both seamless and non-seamless splits
- [x] Config flag: `expandMode: 'expand-up' | 'fixed'` (default 'fixed')
- [x] 17 tests (exceeds 6+ requirement)
- [x] CSS: var(--sd-*) only (no hex, rgb, or named colors)

## Clock / Cost / Carbon

- **Clock:** 47 minutes (08:25 - 09:12 local time during implementation, testing, debug, response)
- **Cost:** Token-based computation only, no LLM API calls generated during test execution
- **Carbon:** Estimated < 1g CO2e for local test execution and file operations

## Issues / Follow-ups

**None** - Feature fully implemented and tested.

### Technical Notes
- Fixed critical test issue: JSX attribute string literals like `value="line1\nline2"` don't interpret `\n` as newlines. Tests corrected to use template literals in variables.
- Line counting logic: `(value.match(/\n/g) || []).length + 1` correctly counts lines regardless of trailing newlines.
- Expand state is purely visual overlay - no changes to split pane resize logic required.
- Z-index: 100 ensures overlay above neighboring panes without interfering with modals (which use higher z-indices).
- Smooth transitions applied to position, max-height, and box-shadow for polished UX.

---

**BEE-2026-03-14-TASK-084-expandable** ✓
