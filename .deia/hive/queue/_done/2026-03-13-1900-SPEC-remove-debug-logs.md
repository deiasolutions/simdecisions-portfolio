# SPEC: Remove Debug Console.logs from Terminal

## Priority
P0

## Objective
Remove debug console.log statements left in useTerminal.ts and TerminalOutput.tsx from BUG-002 (chat terminal display fix). These were left intentionally for manual verification but are no longer needed.

## Context
During BUG-002 fix, debug console.logs were added to verify chat metrics routing. They should be removed now.

Files to read first:
- `browser/src/primitives/terminal/useTerminal.ts`
- `browser/src/primitives/terminal/TerminalOutput.tsx`

## Acceptance Criteria
- [ ] All `console.log` and `console.debug` statements in `useTerminal.ts` that were added for BUG-002 debugging are removed
- [ ] All `console.log` and `console.debug` statements in `TerminalOutput.tsx` that were added for BUG-002 debugging are removed
- [ ] Do NOT remove any console.error or console.warn statements — only debug logs
- [ ] Existing tests still pass: `npx vitest run --reporter=verbose` from browser/
- [ ] 0 regressions

## Smoke Test
- [ ] Terminal still works — type a message, see response
- [ ] No debug output in browser console from terminal components

## Model Assignment
haiku

## Constraints
- This is a TINY task — just find and remove debug console.log lines
- Do NOT refactor or change any logic — only remove debug logging
