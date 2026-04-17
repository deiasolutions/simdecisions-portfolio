# TASK-230: Terminal Up-Arrow Command History (W4 — 4.2)

## Objective
Verify terminal command history works with up-arrow/down-arrow navigation and add persistent localStorage storage so history survives page reloads.

## Context
Wave 4 Product Polish (BL-069). The command history logic already exists with a 100-item ring buffer and deduplication. Up-arrow/down-arrow navigation is wired in TerminalPrompt.tsx. What's missing: persistent storage across sessions via localStorage.

## Source Spec
`docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.2

## Files to Read First
- `browser/src/primitives/terminal/TerminalPrompt.tsx` — Input component with ArrowUp/Down handlers (lines 94-111)
- `browser/src/primitives/terminal/__tests__/commandHistory.test.ts` — History logic tests (197 lines)
- `browser/src/primitives/terminal/useTerminal.ts` — Terminal hook (manages state)

## Deliverables
- [ ] Verify up-arrow recalls previous commands in single-line mode
- [ ] Verify down-arrow navigates forward through history
- [ ] Verify consecutive duplicate commands are deduplicated
- [ ] Verify history caps at 100 items
- [ ] Add localStorage persistence: save history on each command, restore on mount
  - Key: `sd_terminal_history` (or per-pane key if scoped)
  - Save: `JSON.stringify(history)` after each push
  - Restore: `JSON.parse(localStorage.getItem(...))` on init
- [ ] Add tests for persistence: save, restore, corruption handling
- [ ] Run: `cd browser && npx vitest run src/primitives/terminal/`

## Priority
P1

## Model
haiku
