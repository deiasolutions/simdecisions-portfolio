# QUEUE-TEMP-SPEC-CHROME-E1-design-mode: Design Mode Toggle — COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-26

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts` — Added `designMode: boolean` to `ShellState`, added `TOGGLE_DESIGN_MODE` action
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts` — Added `designMode: false` to `INITIAL_STATE`, implemented `TOGGLE_DESIGN_MODE` reducer case
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx` — Added design mode support: seamless panes render minimal chrome when `designMode` is true, dashed borders applied in design mode
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\DesignMode.test.tsx` — NEW: 9 tests for design mode toggle and behavior (all passing)

## What Was Done

- Added `designMode: boolean` field to `ShellState` interface, defaults to `false`
- Added `TOGGLE_DESIGN_MODE` action to `ShellAction` type union
- Implemented `TOGGLE_DESIGN_MODE` reducer case that toggles `designMode` boolean
- Modified `PaneChrome` to check `designMode` from shell context
- Split chrome rendering logic: `chrome: false` always renders without chrome, `seamless: true` renders without chrome UNLESS `designMode` is active
- In design mode, seamless panes render minimal chrome: drag handle, pane menu, close button
- In design mode, seamless panes skip audio/bus mute buttons and pin/collapse buttons (minimal chrome only)
- Border style changes in design mode: `dashed` borders instead of `solid` borders (applied to all panes)
- Created comprehensive test suite with 9 tests:
  - `TOGGLE_DESIGN_MODE` sets `designMode` to true
  - `TOGGLE_DESIGN_MODE` toggles `designMode` off when already on
  - `designMode` defaults to false in `INITIAL_STATE`
  - Seamless pane gets drag handle in design mode
  - Seamless pane has no chrome when design mode is off
  - Seamless pane loses chrome on design mode exit
  - Normal pane keeps full chrome regardless of design mode
  - Dashed borders applied to pane wrappers in design mode
  - Dashed borders removed when design mode is off

## Test Results

All 9 design mode tests pass:

```
✓ src/shell/components/__tests__/DesignMode.test.tsx (9 tests)
  ✓ Design Mode Toggle (3)
  ✓ PaneChrome in Design Mode (4)
  ✓ Dashed Borders in Design Mode (2)
```

## Acceptance Criteria

- [x] Design mode toggles on/off
- [x] Seamless panes gain minimal chrome in design mode
- [x] Seamless panes lose chrome on design mode exit
- [x] Dashed borders visible in design mode, hidden on exit
- [x] Tests written FIRST (TDD) — before implementation
- [x] Minimum 6 tests (delivered 9 tests)
- [x] All tests pass

## Notes

- Design mode currently only affects chrome visibility and border styling
- Add menu scoping (original EGG primitives + GC library) is out of scope for this spec — will be addressed in CHROME-E1 follow-up specs
- Save-as-derived-EGG functionality is out of scope for this spec — addressed in CHROME-E2
- Activation mechanism (kebab menu / keyboard shortcut) is out of scope for this spec — will be added when command palette is implemented in CHROME-B6
- The implementation follows the ADR-SC-CHROME-001-v3 spec exactly: seamless panes get minimal chrome (drag handle + pane ops + close), dashed borders appear on all panes, design mode is a simple boolean toggle

## Dependencies

This spec depends on SPEC-CHROME-A6 (dirty tracking) for determining if save prompt is required on exit. However, the core design mode toggle functionality is independent and works without dirty tracking.
