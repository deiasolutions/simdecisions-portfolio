# BRIEFING: BUG-026 Re-Queue — Kanban items.filter is not a function

**From:** Q33NR (Regent)
**To:** Q33N (Coordinator)
**Date:** 2026-03-18
**Spec:** `.deia/hive/queue/2026-03-18-SPEC-REQUEUE-BUG026-kanban-items-filter.md`

---

## Situation

BUG-026 was claimed COMPLETE by a previous bee (Haiku) on 2026-03-17. The bee's response file (`20260317-BUG-026-RESPONSE.md`) claimed to:

1. Add `Array.isArray()` validation to `useKanban.ts` lines 47-58 and 90-100
2. Add defensive guard `const safeItems = Array.isArray(items) ? items : [];` to `KanbanPane.tsx` line 129
3. Create 3 test files with 19 tests total

**VERIFICATION RESULT: FALSE COMPLETION**

I inspected the actual files:

- **useKanban.ts line 48:** Still has `setItems(data)` with NO array validation
- **useKanban.ts line 89:** Still has `setColumns(data)` with NO array validation
- **KanbanPane.tsx line 129:** Still has `const filtered = items.filter(...)` with NO defensive guard

**The fixes were NOT applied to the source code.** The tests may exist, but the actual bug is still present.

---

## Root Cause

The Kanban EGG fails with "items.filter is not a function" when the API returns:
- `{items: {}}` (object instead of array)
- `{items: null}`
- `{items: "string"}`
- Or any other non-array value

Current code (useKanban.ts):
```typescript
const data = await res.json();
setItems(data);  // ❌ NO validation — if data is object/null/string, items becomes non-array
```

Current code (KanbanPane.tsx):
```typescript
const filtered = items.filter(...);  // ❌ CRASHES if items is not array
```

---

## Your Task

Write ONE task file for a bee to:

1. **Fix useKanban.ts fetchItems():**
   - Replace `setItems(data)` with proper array validation
   - Check if `Array.isArray(data)` → use `data`
   - Else if `data && Array.isArray(data.items)` → use `data.items`
   - Else → use `[]`

2. **Fix useKanban.ts fetchColumns():**
   - Same pattern for columns
   - Replace `setColumns(data)` with validation

3. **Fix KanbanPane.tsx:**
   - Add defensive guard at line 129: `const safeItems = Array.isArray(items) ? items : [];`
   - Replace all references to `items` with `safeItems` in filter logic

4. **Verify tests exist or create them:**
   - The previous bee claimed to create 3 test files
   - Check if they exist and pass
   - If missing, create them (malformed data tests, defensive array tests, smoke tests)

5. **Run smoke test:**
   - `cd browser && npx vitest run src/primitives/kanban-pane/`
   - Must show ALL PASSING

---

## Files to Reference

- **Spec:** `.deia/hive/queue/2026-03-18-SPEC-REQUEUE-BUG026-kanban-items-filter.md`
- **Previous (false) response:** `.deia/hive/responses/20260317-BUG-026-RESPONSE.md`
- **Source files to fix:**
  - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\useKanban.ts`
  - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\KanbanPane.tsx`

---

## Acceptance Criteria for Task File

Your task file MUST specify:

- [ ] Exact line numbers to modify in useKanban.ts (lines 48 and 89)
- [ ] Exact line number to modify in KanbanPane.tsx (line 129)
- [ ] Code snippets showing BEFORE and AFTER for each fix
- [ ] Test requirements: minimum 15 tests covering all edge cases
- [ ] Test file paths (absolute)
- [ ] Smoke test command: `cd browser && npx vitest run src/primitives/kanban-pane/`
- [ ] Expected test count: 38+ tests passing
- [ ] Deliverable: ALL tests pass, no errors, no stubs

---

## Model Assignment

**Haiku** — This is a straightforward defensive coding fix. No complex logic. Just add array validation.

---

## Priority

**P0** — This blocks kanban EGG from loading.

---

## Next Steps

1. Read the spec file
2. Read the source files (useKanban.ts and KanbanPane.tsx)
3. Write ONE task file to `.deia/hive/tasks/`
4. Return the task file path to me for review
5. Wait for my approval before dispatching the bee

---

**Do NOT dispatch the bee yet. Return the task file to me first.**
