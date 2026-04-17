# BUG-027: Turtle-draw EGG shows unregistered chat-cli app type in right pane

## Objective
Fix the Turtle-draw EGG so all its panes load correctly, specifically the right pane which shows "unregistered app type: chat-cli".

## Context
The turtle-draw EGG config references an app type "chat-cli" that is not registered in appRegistry.ts. Either the app type needs to be registered with the correct adapter, or the EGG config needs to reference an existing app type (like "terminal" or "chat").

## Files to Read First
- `eggs/turtle-draw.egg.md`
- `browser/src/shell/components/appRegistry.ts`
- `browser/src/primitives/terminal/`
- `browser/src/apps/`

## Deliverables
- [ ] Identify if "chat-cli" should map to an existing type or needs a new adapter
- [ ] Either register "chat-cli" in appRegistry or fix the EGG config
- [ ] Turtle-draw EGG loads all panes without errors
- [ ] Test that turtle-draw EGG parses and all app types resolve

## Acceptance Criteria
- [ ] ?egg=turtle-draw loads without "unregistered app type" errors
- [ ] All turtle-draw panes render
- [ ] No console errors
- [ ] Test passes

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/shell/__tests__/eggToShell.test.ts`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
haiku

## Priority
P0
