# TASK-238: chat.egg.md Verified (W4 — 4.10)

## Objective
Verify the Chat EGG renders correctly as a 3-pane layout: chat history sidebar (left), chat output (center-top), terminal input (center-bottom).

## Context
Wave 4 Product Polish. The chat EGG is one of three product faces. Must render with proper proportions and seamless border between chat output and terminal.

## Source Spec
`docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.10

## Files to Read First
- `eggs/chat.egg.md` — Chat EGG layout definition (131 lines)
- `browser/src/shell/eggLoader.ts` — EGG parsing
- `browser/src/primitives/text-pane/` — Text pane / chat renderer
- `browser/src/primitives/terminal/` — Terminal input

## Deliverables
- [ ] Load `?egg=chat` in browser and verify:
  - Left sidebar (22%): chat-history tree-browser
  - Center top (70%): chat output text-pane with bubble rendering
  - Center bottom (30%): terminal with `routeTarget: "ai"`
  - Seamless border between chat output and terminal
- [ ] Verify chat bubbles render (user right, AI left) per TASK-229
- [ ] Verify terminal sends to AI provider and response appears in chat
- [ ] Verify 3-currency status bar shows (clock, coin, carbon)
- [ ] Fix any layout or rendering issues
- [ ] Run: `cd browser && npx vitest run`

## Priority
P1

## Model
haiku
