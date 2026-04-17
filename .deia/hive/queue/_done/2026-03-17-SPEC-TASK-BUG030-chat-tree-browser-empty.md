# BUG-030: Chat tree-browser shows empty list with only date headers, no conversations

## Objective
Fix the Chat EGG's tree-browser panel so it shows actual conversation entries, not just empty date headers.

## Context
The Chat EGG has a tree-browser pane that should show conversation history. Currently it renders date group headers but no conversation items underneath them. The chatHistoryAdapter or data source is returning empty groups.

## Files to Read First
- `eggs/chat.egg.md`
- `browser/src/primitives/tree-browser/`
- `browser/src/apps/`
- `browser/src/primitives/tree-browser/adapters/`

## Deliverables
- [ ] Trace chat history adapter data flow
- [ ] Fix adapter to return conversation entries under date groups
- [ ] If no conversations exist, show "No conversations yet" placeholder
- [ ] Tests for populated and empty conversation lists

## Acceptance Criteria
- [ ] Chat tree-browser shows conversation entries when they exist
- [ ] Date headers group conversations correctly
- [ ] Empty state shows placeholder text
- [ ] Tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
haiku

## Priority
P0
