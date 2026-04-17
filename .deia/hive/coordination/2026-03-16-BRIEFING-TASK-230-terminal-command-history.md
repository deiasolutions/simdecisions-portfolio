# Briefing: TASK-230 Terminal Command History Persistence

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-16
**Model:** Haiku

---

## Objective

Verify terminal command history navigation (up/down arrows) works, then add localStorage persistence so command history survives page reloads.

---

## Context from Q88N

This is Wave 4 Product Polish (BL-069), task 4.2 from `docs/specs/WAVE-4-PRODUCT-POLISH.md`.

The command history logic already exists with:
- 100-item ring buffer
- Deduplication
- Up-arrow/down-arrow navigation wired in TerminalPrompt.tsx

What's missing: **persistent storage across sessions via localStorage**.

---

## Files to Investigate

### Terminal Implementation
- `browser/src/primitives/terminal/TerminalPrompt.tsx` — Input component with ArrowUp/Down handlers (lines 94-111)
- `browser/src/primitives/terminal/__tests__/commandHistory.test.ts` — History logic tests (197 lines)
- `browser/src/primitives/terminal/useTerminal.ts` — Terminal hook (manages state)

---

## Requirements

### Verification (Already Built)
- [ ] Up-arrow recalls previous commands in single-line mode
- [ ] Down-arrow navigates forward through history
- [ ] Consecutive duplicate commands are deduplicated
- [ ] History caps at 100 items

### New Work (localStorage Persistence)
- [ ] Add localStorage persistence
  - Key: `sd_terminal_history` (or per-pane key if scoped)
  - Save: `JSON.stringify(history)` after each command
  - Restore: `JSON.parse(localStorage.getItem(...))` on mount
- [ ] Add tests for persistence: save, restore, corruption handling
- [ ] Run: `cd browser && npx vitest run src/primitives/terminal/`

---

## Constraints

- **No hardcoded colors.** CSS variables (`var(--sd-*)`) only.
- **No file over 500 lines.** Modularize at 500. Hard limit: 1,000.
- **TDD.** Tests first, then implementation.
- **NO STUBS.** Every function fully implemented.
- **Response file MANDATORY.** All 8 sections.

---

## Your Task

1. Read the terminal implementation files listed above
2. Write a single task file for a bee (haiku model)
3. Task should verify existing behavior THEN add localStorage persistence
4. Include specific test requirements (how many tests, which scenarios)
5. Return the task file to me for review
6. **DO NOT dispatch the bee yet** — wait for my approval

---

## Response Format

Return a summary:
- Task file path
- Task ID assigned
- Model assigned
- Key deliverables (bullet list)

Then wait for my review and approval before dispatching.
