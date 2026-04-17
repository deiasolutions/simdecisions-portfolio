# BUG-028 (RE-QUEUE): Efemera channels not wired — clicking does nothing

## Background — Why Re-Queued
Previous bee claimed 6/7 tests passing but channelsAdapter.ts has zero references to `channel:selected` event. The click handler was never wired. Backend routes exist at /efemera/ and work. This is a frontend wiring issue.

## Objective
Fix the Efemera EGG so clicking a channel in the channel list selects it and shows messages for that channel.

## Current State
- channelsAdapter.ts exists but does NOT emit `channel:selected` on click
- relayPoller.ts exists for fetching messages
- text-pane chatRenderer handles `channel:message-received` events
- Backend `/efemera/` routes work (29 passing tests)

## Files to Read First
- `eggs/efemera.egg.md`
- `browser/src/primitives/tree-browser/adapters/channelsAdapter.ts`
- `browser/src/primitives/text-pane/services/chatRenderer.tsx`
- `browser/src/services/efemera/relayPoller.ts`
- `hivenode/efemera/routes.py`

## Deliverables
- [ ] channelsAdapter emits `channel:selected` bus event on click
- [ ] text-pane listens for `channel:selected` and fetches messages for that channel
- [ ] relayPoller starts polling for new messages on selected channel
- [ ] Visual highlight on selected channel in tree-browser
- [ ] Tests for channel selection → message display flow

## Acceptance Criteria
- [ ] Clicking a channel selects it (visual highlight)
- [ ] Selected channel's messages appear in text-pane
- [ ] Tests pass
- [ ] No regressions in tree-browser or text-pane tests

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/adapters/__tests__/`
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/text-pane/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- MUST modify channelsAdapter.ts source code

## Model Assignment
sonnet

## Priority
P0

## Re-Queue Metadata
- Original spec: `_done/2026-03-17-SPEC-TASK-BUG028-efemera-channels-not-wired.md`
- Previous response: `20260317-BUG-028-RESPONSE.md`
- Failure reason: channel:selected event never emitted from channelsAdapter
