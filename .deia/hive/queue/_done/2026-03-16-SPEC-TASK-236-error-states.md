# TASK-236: Error States — Pane Error Messages for Failed Applets (W4 — 4.8)

## Objective
Wire the existing error classifier and error message system into the terminal UI. Ensure PaneErrorBoundary catches applet load failures gracefully. Users should see helpful error messages, not blank screens or raw stack traces.

## Context
Wave 4 Product Polish. Three error systems exist but aren't fully wired:
1. `PaneErrorBoundary.tsx` (158 lines) — catches React render errors, shows retry button
2. `errorClassifier.ts` — classifies 7 error types (api_unreachable, timeout, auth_failure, rate_limit, server_error, network_error, unknown)
3. `errorMessages.ts` — user-friendly messages with actionable suggestions

The classifier and message modules exist but are NOT integrated into the terminal output display.

## Source Spec
`docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.8

## Files to Read First
- `browser/src/shell/components/PaneErrorBoundary.tsx` — Error boundary (158 lines)
- `browser/src/primitives/terminal/errorClassifier.ts` — Error type classification
- `browser/src/primitives/terminal/errorMessages.ts` — User-friendly messages
- `browser/src/primitives/terminal/terminal-errors.css` — Error styling
- `browser/src/primitives/terminal/TerminalOutput.tsx` — Where errors render
- `browser/src/primitives/terminal/useTerminal.ts` — Terminal state management

## Deliverables
- [ ] Wire `errorClassifier` into terminal error handling:
  - When terminal receives an error response, classify it
  - Display the user-friendly message from `errorMessages` instead of raw error text
  - Show actionable suggestion (e.g., "Check your API key" for auth_failure)
- [ ] Add `--sd-yellow` to `shell-themes.css` if not already added by TASK-233
  - Fallback: define it locally in `terminal-errors.css` with a comment referencing TASK-233
- [ ] Verify PaneErrorBoundary catches component crashes and shows retry button
- [ ] Add test: error classifier returns correct type for each error pattern
- [ ] Add test: terminal displays friendly message instead of raw error
- [ ] Run: `cd browser && npx vitest run src/primitives/terminal/ && npx vitest run src/shell/`

## Priority
P1

## Model
sonnet
