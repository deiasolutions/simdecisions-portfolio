# BRIEFING: Fix BUG-030 Chat Tree Duplicate Conversations (REQUEUE)

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-19
**Priority:** P0
**Model Assignment:** Sonnet

---

## Objective

Fix the runtime bug in `chatHistoryAdapter.ts` where the same conversation appears 40+ times across different date groups in the chat tree-browser. Previous attempts only fixed test mocks — this time we fix the actual adapter source code.

---

## Background

The chat tree-browser panel is showing the same conversation duplicated 40+ times across "Today", "Yesterday", and "Last Week" date groups. This is a RUNTIME bug in the adapter logic, not a test issue.

**Previous attempts:**
- Fixed test mocks in `chatHistoryAdapter.test.ts`
- Did NOT fix the actual adapter source code

**Root cause (suspected):**
`chatHistoryAdapter.ts` is either:
1. Not deduplicating results (same conversation appears multiple times)
2. Fetching from multiple sources and concatenating without dedup
3. The date grouping logic is assigning the same conversation to multiple date buckets

---

## What Q33N Must Deliver

**Task file(s) for a bee to:**
1. Read the adapter and trace how conversations are fetched
2. Find where duplicates are introduced
3. Deduplicate conversations by ID before grouping
4. Ensure each conversation appears in exactly one date group based on its most recent timestamp
5. Add tests that verify no duplicates appear

---

## Files to Reference

**PRIMARY (THE BUG IS HERE):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts` — MODIFY THIS FILE to fix dedup/grouping logic

**SUPPORTING:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\chatHistoryAdapter.test.ts` — add dedup test
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\chat\chatApi.ts` — what the adapter calls

---

## Deliverables (for bee task file)

- [ ] Each conversation appears exactly ONCE in the tree
- [ ] Conversations grouped into correct date bucket (Today/Yesterday/Last Week/Older)
- [ ] Grouping based on most recent message timestamp, not creation date
- [ ] Test that verifies no duplicates when same conversation appears in API response multiple times
- [ ] No regressions in tree-browser tests

---

## Test Requirements

**Acceptance criteria:**
- [ ] Open chat EGG → tree shows unique conversations only (no duplicates)
- [ ] `cd browser && npx vitest run src/primitives/tree-browser/` — all tests pass
- [ ] `cd browser && npx vitest run` — no regressions

**Smoke test command:**
```bash
cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/
cd browser && npx vitest run
```

---

## Constraints

- No file over 500 lines
- CSS: `var(--sd-*)` only
- No stubs
- MUST modify adapter source code, not just tests
- Model: **Sonnet** (complexity requires Sonnet-level reasoning)

---

## Next Steps for Q33N

1. Read the adapter file to understand current fetch/grouping logic
2. Write a task file for a bee (model: Haiku is fine for implementation once logic is clear)
3. Return to Q33NR for review
4. After Q33NR approval, dispatch the bee
5. Review bee response file
6. Report results to Q33NR

---

## Notes

This is a **REQUEUE** — previous attempts failed because they fixed tests but not the actual source code. Make sure the task file explicitly instructs the bee to:
- **MODIFY `chatHistoryAdapter.ts`** (the actual source)
- **ADD tests** to verify deduplication works

Do NOT accept a task file that only modifies tests.
