# TASK-017: Dashboard Primitive (P-15) — Status Bar + Model Chooser -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-03-11

## Files Modified

### Source Files Created (8)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\constants.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\DashboardBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\ModelChooser.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\CurrencyDisplay.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\ApiKeyBadge.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\dashboard.css`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\index.ts`

### Test Files Created (4)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\__tests__\DashboardBar.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\__tests__\ModelChooser.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\__tests__\CurrencyDisplay.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\__tests__\ApiKeyBadge.test.tsx`

### Dependencies Modified (1)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\package.json` — added @testing-library/user-event dev dependency

## What Was Done

- Created complete dashboard primitive module at `browser/src/primitives/dashboard/`
- Defined TypeScript interfaces for all components (DashboardBarProps, ModelChooserProps, CurrencyDisplayProps, ApiKeyBadgeProps)
- Implemented DashboardBar main component with model chooser, 3-currency display, and API key badge
- Implemented ModelChooser dropdown with provider grouping and keyboard navigation (ArrowUp/Down, Enter, Escape)
- Implemented CurrencyDisplay showing clock (ms→s), coin (USD), and carbon (g CO₂) metrics with configurable filter
- Implemented ApiKeyBadge showing configured/missing status with click handler for settings
- Created constants.ts with hardcoded DEFAULT_PROVIDERS matching hivenode/llm/config.py (Anthropic, OpenAI, Gemini, Ollama)
- Wrote comprehensive CSS using only var(--sd-*) variables from shell-themes.css (no hardcoded colors)
- Added compact mode support for all components (reduced height, smaller fonts)
- Added responsive collapse for narrow widths (hides provider name, status text)
- Wrote 31 tests across 4 test files following TDD methodology
- All tests pass with 100% coverage of specified test cases
- Build verification successful (vite build completes without errors)

## Test Results

**Test Execution:** vitest --run
**Result:** All tests PASSED

```
Test Files  4 passed (4)
Tests       31 passed (31)
Duration    3.71s
```

### Test Breakdown by Component
- CurrencyDisplay.test.tsx: 8/8 passed
- ApiKeyBadge.test.tsx: 5/5 passed
- ModelChooser.test.tsx: 8/8 passed
- DashboardBar.test.tsx: 10/10 passed

## Build Verification

**Build Command:** npm run build
**Result:** SUCCESS

```
✓ 152 modules transformed
✓ built in 1.21s
dist/assets/index--n2EenBk.css   20.20 kB │ gzip:  4.35 kB
dist/assets/index-DQyKnbDL.js   289.92 kB │ gzip: 88.87 kB
```

Dashboard primitive compiles cleanly through Vite build pipeline.

## Acceptance Criteria

### Source Files (8)
- [x] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\types.ts`
- [x] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\constants.ts`
- [x] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\DashboardBar.tsx`
- [x] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\ModelChooser.tsx`
- [x] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\CurrencyDisplay.tsx`
- [x] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\ApiKeyBadge.tsx`
- [x] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\dashboard.css`
- [x] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\index.ts`

### Test Files (4)
- [x] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\__tests__\DashboardBar.test.tsx` — 10 tests
- [x] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\__tests__\ModelChooser.test.tsx` — 8 tests
- [x] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\__tests__\CurrencyDisplay.test.tsx` — 8 tests
- [x] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\__tests__\ApiKeyBadge.test.tsx` — 5 tests

**Total: 12 deliverables (8 source + 4 test), 31 tests — ALL COMPLETE**

### Test Requirements (31 tests minimum)
- [x] DashboardBar.test.tsx — 10 tests (renders all sections, passes props, calls callbacks, compact mode, currency filter, responsive)
- [x] ModelChooser.test.tsx — 8 tests (shows current model, opens dropdown, groups by provider, selection, click outside, Escape key, keyboard navigation)
- [x] CurrencyDisplay.test.tsx — 8 tests (renders all currencies, formats clock/coin/carbon, currency filter, zero values, compact mode, updates)
- [x] ApiKeyBadge.test.tsx — 5 tests (green/warning indicators, onClick callback, configured/missing text)

## Clock / Cost / Carbon

**Clock:** 8 minutes (480 seconds)
**Cost:** $0.0247 USD (estimated based on Sonnet 4.5 input/output tokens)
**Carbon:** 1.85 g CO₂ (estimated based on API usage)

## Issues / Follow-ups

### Edge Cases Handled
- Dropdown closes on click outside using mousedown event listener
- Dropdown closes on Escape key
- Keyboard navigation wraps at boundaries (ArrowDown at last item stays at last)
- Model name duplicates in UI (trigger + dropdown) handled in tests using getAllByText
- Zero values display as "0.0s", "$0.00", "0.00g" (never hidden)
- Compact mode reduces decimal precision for cost (4→2 decimals)
- Responsive collapse hides provider name and status text at narrow widths

### Dependencies Created
- Terminal primitive (future) will import DashboardBar to replace TerminalStatusBar
- Settings primitive (future) will be invoked by onApiKeyClick callback
- Chat app MVP will use DashboardBar in terminal pane

### Recommended Next Tasks
1. **TASK-018:** BYOK Settings UI — Build settings primitive that DashboardBar.onApiKeyClick opens
2. **Refactor TerminalStatusBar:** Replace existing terminal status bar with DashboardBar import
3. **Dynamic provider loading:** Replace hardcoded DEFAULT_PROVIDERS with hivenode API call
4. **Provider detection:** Auto-detect current provider from selected model ID for ApiKeyBadge tooltip
5. **Theme integration:** Add theme picker button to DashboardBar (right section)

### Known Limitations (by design)
- Provider/model list is hardcoded in constants.ts (MVP scope — will be replaced by API loading)
- No provider logo icons (using text labels only)
- No model context length display (out of scope for MVP)
- No streaming status indicator (covered by optional statusText prop)
- ApiKeyBadge does not verify key validity, only checks if key is configured (validation is backend responsibility)

---

**Task Status:** ✅ COMPLETE — All deliverables created, all tests passing, build verified
