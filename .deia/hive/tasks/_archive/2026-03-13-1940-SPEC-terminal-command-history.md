# SPEC: Terminal Up-Arrow Command History (BL-069)

## Priority
P1

## Objective
Add up/down arrow key command history navigation to the terminal input. Pressing up-arrow recalls the previous command, down-arrow goes forward. Ring buffer, 100 entries max. History is per session (not persisted to localStorage or backend).

## Context
The terminal input lives in the terminal primitive. Users type commands and press Enter. There is no command history recall — every new prompt starts blank.

Files to read first:
- `browser/src/primitives/terminal/` — directory listing to find the input component
- `browser/src/primitives/terminal/useTerminal.ts` — terminal hook
- `browser/src/primitives/terminal/TerminalPrompt.tsx` — input component (if it exists, check directory)
- `browser/src/primitives/terminal/types.ts` — terminal types

## Acceptance Criteria
- [ ] Up-arrow in empty input recalls the most recent command
- [ ] Repeated up-arrow walks backwards through history (most recent → oldest)
- [ ] Down-arrow walks forward through history (oldest → most recent)
- [ ] Down-arrow past the newest entry restores the empty input (or whatever the user was typing before pressing up)
- [ ] Ring buffer capped at 100 entries — oldest entries dropped when full
- [ ] Duplicate consecutive commands are NOT added (typing "help" twice only stores one entry)
- [ ] History is per terminal instance, stored in the hook state (useRef or useState)
- [ ] History is NOT persisted — fresh on every page load
- [ ] Cursor moves to end of line after history recall
- [ ] 5+ tests:
  - Test: up-arrow recalls last command
  - Test: multiple up-arrows walk through history in order
  - Test: down-arrow after up returns to newer entry
  - Test: ring buffer drops oldest at 101 entries
  - Test: consecutive duplicates are deduplicated

## Smoke Test
- [ ] Type "hello", Enter, "world", Enter, press up-arrow — see "world"
- [ ] Press up-arrow again — see "hello"
- [ ] Press down-arrow — see "world" again

## Model Assignment
haiku

## Constraints
- Do NOT persist history to localStorage or backend — session only
- Do NOT change the terminal output or response handling — only the input behavior
- Keep it simple — no fuzzy search, no Ctrl+R, just up/down arrow
