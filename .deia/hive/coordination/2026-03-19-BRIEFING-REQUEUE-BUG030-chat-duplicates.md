# BRIEFING: BUG-030 RE-QUEUE — Chat Duplicate Conversations

**Date:** 2026-03-19
**From:** Q33NR (Regent)
**To:** Q33N (Queen Coordinator)
**Spec File:** `.deia/hive/queue/_active/SPEC-REQUEUE-BUG030-chat-duplicate-conversations.md`
**Priority:** P0
**Model Assignment:** sonnet

---

## Objective

Fix runtime bug where chat tree-browser shows the same conversation duplicated 40+ times across date groups.

---

## Context

### Previous Attempts
- Multiple failed attempts (specs in `_done`: SPEC-TASK-BUG030, SPEC-REQUEUE-BUG030, SPEC-REQUEUE3-BUG030)
- Multiple dead specs in `_dead/` (2007, 2038, 2044, 2047)
- Previous attempts only fixed test mocks, NOT the actual adapter source code

### The Real Problem
The bug is in **RUNTIME behavior** in `chatHistoryAdapter.ts`. The adapter is:
1. Not deduplicating fetched conversations by ID, OR
2. Fetching from multiple sources and concatenating without dedup, OR
3. Assigning the same conversation to multiple date buckets in the grouping logic

### What Needs to Happen
The bee must:
1. Read the adapter source code and trace conversation fetching
2. Find where duplicates are introduced
3. Add deduplication logic by conversation ID before grouping
4. Ensure each conversation appears in EXACTLY ONE date group based on its most recent timestamp
5. Add tests that verify no duplicates when API returns duplicate conversations

---

## Files Involved

### MUST READ FIRST:
- `browser/src/primitives/tree-browser/adapters/chatHistoryAdapter.ts` (THE BUG IS HERE)
- `browser/src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts`
- `browser/src/services/chat/chatApi.ts`

### MUST MODIFY:
- `browser/src/primitives/tree-browser/adapters/chatHistoryAdapter.ts` — fix dedup/grouping logic
- `browser/src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts` — add dedup test

---

## Constraints (HARD RULES)

- No file over 500 lines
- CSS: `var(--sd-*)` only (though unlikely to touch CSS here)
- **NO STUBS** — full implementation required
- **MUST modify adapter source code**, not just tests
- TDD: Tests first, then implementation

---

## Task File Requirements

Write ONE task file for a sonnet bee:

**Task Deliverables:**
- [ ] Deduplicate conversations by ID in `chatHistoryAdapter.ts`
- [ ] Each conversation appears exactly ONCE in tree
- [ ] Conversations grouped into correct date bucket (Today/Yesterday/Last Week/Older)
- [ ] Grouping based on most recent message timestamp
- [ ] Test that verifies no duplicates when API response contains duplicate conversations
- [ ] No regressions in tree-browser tests
- [ ] All tests pass

**Test Requirements:**
- [ ] Add test case: API returns same conversation multiple times → tree shows it once
- [ ] Add test case: Conversation with multiple messages → grouped by most recent message timestamp
- [ ] Run: `cd browser && npx vitest run src/primitives/tree-browser/` — all tests pass
- [ ] Run: `cd browser && npx vitest run` — no regressions

**Acceptance Criteria:**
- [ ] Open chat EGG → tree shows unique conversations only
- [ ] All tree-browser tests pass
- [ ] Full browser test suite passes (no regressions)

---

## What To Check in Review

When Q33N returns the task file, verify:

1. **File paths are absolute** (Windows format: `C:\Users\davee\...`)
2. **Test requirements are specific** (which test cases, which scenarios)
3. **Dedup logic is specified** (dedup by ID before grouping)
4. **No stubs allowed** (must be fully implemented)
5. **Response file template is included** (8 sections)
6. **Model assignment is sonnet** (as specified in spec)

---

## Critical Notes

- This is the **4th attempt** at BUG-030 (3 in `_done`, multiple in `_dead`)
- Previous attempts only fixed test mocks
- The bee MUST modify the adapter SOURCE CODE
- The bee MUST add deduplication logic
- The bee MUST test with duplicate input data

---

## Your Action Items

1. Read the adapter source code
2. Understand the current fetching and grouping logic
3. Write ONE task file for a sonnet bee
4. Return the task file to me for review
5. DO NOT dispatch the bee yet — wait for my approval

---

**Status:** READY FOR Q33N
