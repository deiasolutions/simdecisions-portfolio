# BUG-028: Efemera channels not wired - clicking channels does nothing

## Objective
Fix the Efemera EGG so clicking a channel in the channel list actually selects it and shows messages for that channel.

## Context
The Efemera EGG has channels listed in the tree-browser but clicking them does nothing. The channelsAdapter needs to emit channel:selected bus events, and the text-pane needs to listen and display messages for the selected channel. Backend routes exist at /efemera/.

## Files to Read First
- `eggs/efemera.egg.md`
- `browser/src/primitives/tree-browser/adapters/channelsAdapter.ts`
- `browser/src/primitives/text-pane/services/chatRenderer.tsx`
- `browser/src/services/efemera/relayPoller.ts`
- `hivenode/efemera/routes.py`
- `hivenode/efemera/store.py`

## Deliverables
- [ ] Fix channelsAdapter to emit channel:selected on click
- [ ] Fix text-pane to listen for channel:selected and load messages
- [ ] Wire relayPoller to fetch messages for selected channel
- [ ] Tests for channel selection flow end-to-end

## Acceptance Criteria
- [ ] Clicking a channel selects it (visual highlight)
- [ ] Selected channel's messages appear in text-pane
- [ ] Sending a message in selected channel works
- [ ] Tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/adapters/__tests__/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
sonnet

## Priority
P0
