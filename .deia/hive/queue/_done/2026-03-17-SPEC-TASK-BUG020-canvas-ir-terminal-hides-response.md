# BUG-020: Canvas expanded IR terminal hides to_user response

## Objective
Fix the Canvas expanded IR terminal so it shows the to_user response content instead of hiding it.

## Context
When Canvas IR terminal is expanded, the to_user response from LLM processing is hidden or not rendered. The terminal output component may be filtering or not recognizing the to_user envelope type.

## Files to Read First
- `browser/src/primitives/terminal/TerminalOutput.tsx`
- `browser/src/primitives/terminal/TerminalApp.tsx`
- `browser/src/primitives/terminal/useTerminal.ts`
- `eggs/canvas.egg.md`

## Deliverables
- [ ] Trace to_user response rendering in terminal output
- [ ] Fix terminal output to display to_user content
- [ ] Ensure expanded mode shows all response types
- [ ] Tests for to_user response visibility in terminal

## Acceptance Criteria
- [ ] to_user responses visible in expanded IR terminal
- [ ] Response content renders with correct formatting
- [ ] Both collapsed and expanded terminal modes show responses
- [ ] Tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/terminal/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
haiku

## Priority
P0
