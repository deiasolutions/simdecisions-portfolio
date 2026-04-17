# Q33N: BUG-030 (RE-QUEUE) — Task File Ready for Review

**Date:** 2026-03-18
**From:** Q33N (Queen Coordinator)
**To:** Q33NR (Queen Regent)
**Bot ID:** QUEEN-2026-03-18-BRIEFING-BUG030-REQ

---

## Summary

I've analyzed the BUG-030 re-queue briefing and created one task file for a sonnet bee to fix the failing chatHistoryAdapter tests.

**Task file created:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-18-TASK-BUG030B-fix-chat-history-tests.md`

---

## Analysis

### What's Actually Wrong

The briefing was accurate. The previous bee (BUG-030) correctly added `'chat-history'` to AUTO_EXPAND_ADAPTERS in treeBrowserAdapter.tsx (line 39). This was the right fix for the expand behavior.

However, the bee also wrote 9 tests with **incorrect mock expectations** that don't match the real API contract:

1. **Dynamic IDs:** Tests use hardcoded `'conv-1'` but chatApi.generateId() produces `'conv-${timestamp}-${random6chars}'`
2. **Volume defaults:** Tests expect `volume: 'cloud://'` but API defaults to `'home://'`
3. **Preference defaults:** Tests expect `volumePreference: 'cloud-only'` but API defaults to `'both'`
4. **Badge status:** Tests expect `'🟢'` (online) but mocked volumeStatus returns `'offline'` → `'🔴'`

### What's Correct (No Changes Needed)

- `chatHistoryAdapter.ts` — Implementation is correct
- `treeBrowserAdapter.tsx` — AUTO_EXPAND_ADAPTERS fix is correct
- `chatApi.ts` — API contract is correct

### What Needs Fixing

- `chatHistoryAdapter.test.ts` — Test mock expectations must match reality

---

## Task File Details

**TASK-BUG030B** instructs the bee to:

1. Use dynamic pattern matching for conversationId (regex, not hardcoded 'conv-1')
2. Fix mock data to use correct defaults: `volume: 'home://'`, `volume_preference: 'both'`
3. Fix badge expectations to match mocked volumeStatus behavior
4. Do NOT modify adapter source code (it's correct)
5. Run tests to verify all 9 pass
6. Verify no regressions in full tree-browser suite

**Model:** sonnet (test fixing requires understanding API contracts)
**Priority:** P0
**Estimated time:** 15-20 minutes

---

## Test Commands in Task File

```bash
# Specific test file
cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts

# Full tree-browser suite
cd browser && npx vitest run src/primitives/tree-browser/
```

---

## Acceptance Criteria

All criteria from the spec are captured in the task file:
- [ ] Chat tree-browser shows conversation entries when they exist
- [ ] Date headers group conversations correctly
- [ ] Empty state shows placeholder text
- [ ] Tests pass
- [ ] No regressions in tree-browser tests

---

## Files Referenced

Task file includes absolute paths for all files bee needs to read:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\chatHistoryAdapter.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatApi.ts`

---

## Ready for Q33NR Review

The task file is ready for your review. Please check:
- [ ] Deliverables are concrete and testable
- [ ] Test requirements are clear
- [ ] No stubs will be created
- [ ] Constraints are enforced
- [ ] Response file format is mandated
- [ ] Acceptance criteria match spec

Once approved, I will dispatch the bee.

---

**Q33N (Coordinator)**
2026-03-18
