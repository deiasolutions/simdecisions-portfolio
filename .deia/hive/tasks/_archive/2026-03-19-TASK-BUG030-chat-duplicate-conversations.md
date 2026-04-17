# TASK-BUG030: Fix Chat Duplicate Conversations in Tree Browser

**Model:** sonnet
**Priority:** P0
**Date:** 2026-03-19

## Objective
Add defensive deduplication logic to chatHistoryAdapter to ensure each conversation appears exactly once in the tree, regardless of whether the API returns duplicates.

## Context
The chat tree-browser is showing the same conversation duplicated 40+ times across date groups. While chatApi.ts has deduplication logic (lines 192-213), the adapter must defensively handle cases where:
1. The API deduplication fails or has bugs
2. Multiple sources return the same conversation
3. Race conditions or caching issues cause duplicate data

The adapter currently trusts the API to return deduplicated data. We need to add explicit deduplication in the adapter as a defensive measure.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts` (lines 80-124)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\chatHistoryAdapter.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatApi.ts` (lines 192-214 for context)

## Root Cause Analysis
**Current behavior:**
- Line 82: `const conversations = await listConversations()`
- Line 87-89: Sorts by `updated_at`
- Line 99-103: Groups by date without deduplication
- **Missing:** Explicit deduplication by conversation ID before grouping

**Why duplicates occur:**
- If `listConversations()` returns duplicates (bug in chatApi merge logic)
- If the same conversation exists with different timestamps in home:// and cloud://
- If the Map-based dedup in chatApi fails due to reference equality issues

**The fix:**
Add explicit deduplication by `conv.id` before the grouping step (after sorting, before the loop).

## Deliverables

### Code Changes
- [ ] Add deduplication logic in `chatHistoryAdapter.ts` line ~90 (after sort, before grouping)
- [ ] Use `Map<string, Conversation>` keyed by `conv.id` to deduplicate
- [ ] Prefer most recent `updated_at` when choosing which duplicate to keep
- [ ] Ensure each conversation appears in exactly ONE date group
- [ ] No changes to chatApi (it's not the adapter's responsibility to fix API bugs)

### Test Changes
- [ ] Add test case: "deduplicates conversations when API returns duplicates"
  - Mock API returns same conversation 3 times with slightly different `updated_at`
  - Verify tree shows conversation exactly once
  - Verify it appears in correct date group based on most recent `updated_at`
- [ ] Add test case: "handles conversations with same ID but different volumes"
  - Mock returns same ID from home:// and cloud://
  - Verify only one appears in tree
- [ ] Verify existing 9 tests still pass

## Test Requirements

**Test-Driven Development (TDD):**
1. Write the new test cases FIRST (in `chatHistoryAdapter.test.ts`)
2. Run tests → they MUST fail initially
3. Implement the deduplication logic in `chatHistoryAdapter.ts`
4. Run tests → they MUST pass

**Test Commands:**
```bash
# Run adapter tests only
cd browser && npx vitest run src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts

# Run all tree-browser tests
cd browser && npx vitest run src/primitives/tree-browser/

# Full browser test suite (check for regressions)
cd browser && npx vitest run
```

**Expected Results:**
- All 11 tests pass (9 existing + 2 new)
- No regressions in browser test suite
- Test coverage for duplicate handling

## Implementation Details

### Location of Fix
File: `chatHistoryAdapter.ts`
Line: Insert between line 89 (after sort) and line 91 (before comment "// Group by date")

### Deduplication Algorithm
```typescript
// Deduplicate by conversation ID (defensive - API should do this, but be safe)
const dedupMap = new Map<string, Conversation>();
for (const conv of sorted) {
  const existing = dedupMap.get(conv.id);
  if (!existing || new Date(conv.updated_at) > new Date(existing.updated_at)) {
    dedupMap.set(conv.id, conv);
  }
}
const deduped = Array.from(dedupMap.values());
```

Then change line 99 from `for (const conv of sorted)` to `for (const conv of deduped)`.

### Test Structure (in chatHistoryAdapter.test.ts)
Add after line 305 (after "uses conversation ID for label" test):

```typescript
it('deduplicates conversations when API returns duplicates', async () => {
  // Setup: same conversation returned 3 times with different updated_at
  // Verify: appears exactly once, uses most recent updated_at for grouping
});

it('handles conversations with same ID but different volumes', async () => {
  // Setup: same ID from home:// and cloud://
  // Verify: appears exactly once
});
```

## Constraints
- No file over 500 lines (chatHistoryAdapter.ts currently 125 lines → safe)
- CSS: `var(--sd-*)` only (no CSS changes expected)
- No stubs — full implementation required
- MUST modify adapter source code, not just tests
- Tests MUST be written first (TDD)

## Acceptance Criteria
- [ ] chatHistoryAdapter.ts has explicit deduplication logic by `conv.id`
- [ ] Deduplication happens after sorting, before grouping
- [ ] Each conversation appears exactly once in tree, even if API returns duplicates
- [ ] Two new test cases added and passing
- [ ] All existing tree-browser tests pass (no regressions)
- [ ] Full browser test suite passes (no regressions)
- [ ] No hardcoded colors added
- [ ] No files exceed 500 lines

## Smoke Test Verification
After completing the work:

1. **Unit tests pass:**
   ```bash
   cd browser && npx vitest run src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts
   ```
   Expected: 11/11 tests passing

2. **Tree-browser tests pass:**
   ```bash
   cd browser && npx vitest run src/primitives/tree-browser/
   ```
   Expected: All tests passing

3. **No regressions:**
   ```bash
   cd browser && npx vitest run
   ```
   Expected: Same or higher pass count as baseline

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260319-TASK-BUG030-RESPONSE.md`

The response MUST contain these 8 sections:

1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full absolute paths
3. **What Was Done** — bullet list of concrete changes (not intent, actual code changes)
4. **Test Results** — test files run, pass/fail counts, specific test names
5. **Build Verification** — test output summary showing all tests pass
6. **Acceptance Criteria** — copy from task, mark [x] done or [ ] not done with explanation
7. **Clock / Cost / Carbon** — wall time, estimated USD cost, estimated CO2e
8. **Issues / Follow-ups** — any edge cases, dependencies, recommended next tasks

DO NOT skip any section. All three metrics (Clock / Cost / Carbon) are mandatory.

## Clock / Cost / Carbon Estimates
- **Clock:** ~45 minutes (15 min tests, 15 min implementation, 15 min verification)
- **Cost:** ~$0.15 USD (sonnet, moderate complexity)
- **Carbon:** ~15g CO2e (estimated for compute time)
