# SPEC-BL-950: Efemera Terminal Minimal 2-Line Mode -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-27

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts` — Added `displayMode?: 'minimal' | 'full'` to TerminalEggConfig
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalApp.tsx` — Added minimal mode rendering logic, hide response pane and status bar in minimal mode, pass `isMinimal` to TerminalPrompt
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalPrompt.tsx` — Added `isMinimal` prop, hide file attachment and voice buttons in minimal mode
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminal.css` — Added `.terminal-pane--minimal` CSS class (flex: 0 0 auto, justify-content: flex-end)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\efemera.egg.md` — Updated terminal config to use `displayMode: 'minimal'`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\terminal-minimal-mode.test.tsx` — 11 tests validating minimal mode behavior (all passing)

## What Was Done

- Added `displayMode` config option to TerminalEggConfig with values 'minimal' | 'full'
- Implemented minimal mode in TerminalApp:
  - When `displayMode: 'minimal'`, terminal renders with `terminal-pane--minimal` CSS class
  - Response pane is hidden (no zone 2 scrollback)
  - Status bar is hidden
  - API key warning is hidden (relay mode doesn't need it)
  - Only prompt area renders (2-line input + system messages)
- Modified TerminalPrompt to hide file attachment and voice buttons in minimal mode
- Added CSS rule for `.terminal-pane--minimal` to prevent flex expansion
- Updated efemera.egg.md to use `displayMode: 'minimal'` in terminal config
- All 11 minimal mode tests pass
- No regression in existing terminal tests (248 tests pass, 13 unrelated failures due to missing hivenodeUrl file)

## Test Results

```
✓ terminal-minimal-mode.test.tsx (11 tests, all passing)
  ✓ renders in minimal mode with 2 lines
  ✓ hides status bar in minimal mode
  ✓ shows system message line when submitting without channel
  ✓ accepts text input in minimal mode
  ✓ sends message on Enter in minimal mode
  ✓ does NOT show file attachment button in minimal mode
  ✓ does NOT show voice button in minimal mode
  ✓ shows compact single-line input in minimal mode
  ✓ clears system message when channel selected
  ✓ minimal mode does NOT render API key warning
  ✓ minimal mode renders with correct CSS variables
```

Terminal suite: 248 tests passing, 13 unrelated failures (hivenodeUrl missing).

## Smoke Test

```bash
cd browser && npx vitest run src/primitives/terminal/__tests__/terminal-minimal-mode.test.tsx
```

Result: ✓ 11 passed

## Deliverables Status

- [x] New `displayMode: 'minimal'` config option for terminal pane
- [x] Minimal mode rendering: 2-line input + status bar (hidden), no chrome
- [x] efemera.egg.md updated to use minimal mode
- [x] Tests for minimal mode rendering
- [x] Full terminal mode still works unchanged (no regression)
- [x] No stubs

## Notes

- Minimal mode automatically hides status bar (effectiveHideStatusBar = true)
- Minimal mode hides zone 2 response pane entirely
- Minimal mode hides file attachment and voice input buttons (clean 2-line input)
- System messages (relay errors like "Select a channel first") render above prompt
- CSS variables only (var(--sd-*)), no hardcoded colors
- All acceptance criteria met
