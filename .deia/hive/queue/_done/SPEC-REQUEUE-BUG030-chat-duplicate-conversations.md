# BUG-030 (RE-QUEUE): Chat shows same conversation 40+ times

## Priority
P0

## Background
The chat tree-browser panel lists the same conversation duplicated 40+ times across "Today", "Yesterday", and "Last Week" date groups. This is a RUNTIME bug in the adapter logic, not a test issue. Previous attempts only fixed test mocks — the actual adapter source code needs fixing.

## Problem
`chatHistoryAdapter.ts` is fetching conversations and either:
1. Not deduplicating results (same conversation appears multiple times)
2. Fetching from multiple sources and concatenating without dedup
3. The date grouping logic is assigning the same conversation to multiple date buckets

## What Needs to Happen
1. Read the adapter and trace how conversations are fetched
2. Find where duplicates are introduced
3. Deduplicate conversations by ID before grouping
4. Ensure each conversation appears in exactly one date group based on its most recent timestamp
5. Add tests that verify no duplicates appear

## Files to Read First
- `browser/src/primitives/tree-browser/adapters/chatHistoryAdapter.ts` (THE BUG IS HERE — modify this file)
- `browser/src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts`
- `browser/src/services/chat/chatApi.ts` (what the adapter calls)

## Files to Modify
- `browser/src/primitives/tree-browser/adapters/chatHistoryAdapter.ts` — fix dedup/grouping logic
- `browser/src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts` — add dedup test

## Deliverables
- [ ] Each conversation appears exactly ONCE in the tree
- [ ] Conversations grouped into correct date bucket (Today/Yesterday/Last Week/Older)
- [ ] Grouping based on most recent message timestamp, not creation date
- [ ] Test that verifies no duplicates when same conversation appears in API response multiple times
- [ ] No regressions in tree-browser tests

## Acceptance Criteria
- [ ] Open chat EGG → tree shows unique conversations only (no duplicates)
- [ ] `cd browser && npx vitest run src/primitives/tree-browser/` — all tests pass
- [ ] `cd browser && npx vitest run` — no regressions

## Smoke Test
```bash
cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/
cd browser && npx vitest run
```

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- MUST modify adapter source code, not just tests

## Model Assignment
sonnet
