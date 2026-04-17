# BRIEFING: Shell Reducer — Swap, Delete, Merge Fixes

**Date:** 2026-03-13
**From:** Q33NR (Regent)
**To:** Q33N (Queen Coordinator)
**Spec:** `docs/specs/2026-03-13-1801-SPEC-shell-swap-delete-merge.md`
**Priority:** P0
**Model Assignment:** Sonnet

---

## Objective

Fix three broken/missing shell reducer operations:
1. **Pane swap without data loss** — currently loses app state/content when swapping
2. **Delete empty cell via FAB** — FAB menu exists but "Delete Cell" option is missing
3. **Contiguous-edge merge on delete** — when a cell is deleted, the neighboring cell with the longest shared border should expand (if empty) or the space becomes empty (if neighbor has content)

---

## Context — Current State Verified

The shell reducer lives at `browser/src/shell/`. It was ported in TASK-008 with 231 passing tests. The reducer delegates layout operations to `browser/src/shell/actions/layout.ts`.

**Files confirmed to exist (with line counts):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts` (203 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\actions\layout.ts` (311 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts` (244 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\utils.ts` (~500 lines, 16 helper functions)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\EmptyPane.tsx` (156 lines — HAS FAB menu)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\reducer.layout.test.ts` (existing tests)

**Directory structure confirmed:**
```
browser/src/shell/
├── __tests__/
│   ├── reducer.layout.test.ts
│   ├── reducer.branch.test.ts
│   ├── reducer.lifecycle.test.ts
│   ├── reducer.test.ts
│   └── ... (other test files)
├── actions/
│   ├── layout.ts
│   ├── branch.ts
│   └── lifecycle.ts
├── components/
│   ├── EmptyPane.tsx
│   ├── PaneContent.tsx
│   ├── ShellNodeRenderer.tsx
│   └── ... (other components)
├── reducer.ts
├── types.ts
├── utils.ts
├── constants.ts
└── ...
```

---

## Verified Bugs (from code review)

### Bug 1: SWAP_CONTENTS loses data (lines 279-297 in actions/layout.ts)
```typescript
case 'SWAP_CONTENTS': {
  const keys = [
    'appType', 'appConfig', 'label', 'audioMuted', 'busMute', 'notification',
    'tabs', 'activeTabIndex', 'type', 'children', 'ratio', 'direction'
  ];
  const extract = (n: any) => Object.fromEntries(keys.filter(k => k in n).map(k => [k, n[k]]));
  let newRoot = replaceNode(state.root, nodeAId, { ...nodeA, ...extract(nodeB) });
  newRoot = replaceNode(newRoot, nodeBId, { ...nodeB, ...extract(nodeA) });
  ...
}
```

**Problem:** This swaps the `appType` and `appConfig` fields, but React remounts the components because the content fields change. This loses:
- Terminal history
- Editor scroll position
- Text content in text-pane
- Any other internal component state

**Root cause:** The swap changes appType/appConfig, which triggers React to see it as a different component type, causing unmount → remount.

**Fix needed:** Swap should only swap the `appType` + `appConfig` fields WITHOUT triggering component remount. React keys on PaneContent containers must remain stable (keyed by node.id). The swap should be seen by React as a content update, not a component change.

### Bug 2: FAB menu missing "Delete Cell" (EmptyPane.tsx lines 41-89)
`EmptyPane.tsx` exists with a FAB menu. Menu has:
- Split options (horizontal, vertical, triple)
- Merge option (conditional, only if parent is split)
- Tab options
- Applet spawn options

**Missing:** "Delete Cell" option

**Current merge logic (lines 62-71):**
```typescript
...(canMerge && parent ? [
  { separator: true, label: '' } as ContextMenuItem,
  {
    icon: '⊟', label: 'Merge Pane',
    action: () => {
      const keep = parent.children[0].id === node.id ? 1 : 0;
      dispatch?.({ type: 'MERGE', splitNodeId: parent.id, keepChild: keep });
    },
  } as ContextMenuItem,
] : []),
```

This only shows "Merge Pane" if the parent is a split. We need a separate "Delete Cell" option that works even when parent is not a split.

### Bug 3: No contiguous-edge merge on delete (actions/layout.ts lines 74-82)
Current `MERGE` action:
```typescript
case 'MERGE': {
  const split = findNode(state.root, action.splitNodeId);
  if (!split || split.type !== 'split') return state;
  return withUndo(
    state,
    replaceNode(state.root, action.splitNodeId, split.children[action.keepChild ?? 0]),
    'Merge pane'
  );
}
```

**Problem:** This only collapses binary splits by picking one child. It does NOT:
- Check neighbor borders
- Use layout positions to determine which neighbor to expand
- Distinguish between empty and occupied neighbors

**Spec requirement:**
- Find the neighbor that shares the longest continuous border (use COMPUTED LAYOUT POSITIONS, not tree parentage)
- If neighbor is EMPTY → expand neighbor to fill deleted space
- If neighbor is APPLET (has content) → deleted space becomes empty, neighbor does NOT expand

**Fix needed:** Add a new action `DELETE_CELL` that:
1. Removes the cell from the tree
2. Checks layout dimensions to find neighbor with longest shared border
3. If neighbor is empty (appType === 'empty') → expand neighbor to fill space
4. If neighbor has content (appType !== 'empty') → replace deleted cell with empty cell

**Implementation note:** The reducer needs access to rendered layout dimensions. Add `layoutDimensions: Record<string, { x: number; y: number; w: number; h: number }>` to ShellState. The renderer (PaneContent or ShellNodeRenderer) updates this field on each layout. The reducer reads it for merge decisions.

---

## Acceptance Criteria (from Spec)

### Fix 1: Swap without data loss
- [ ] When two panes are swapped, the swap changes the `appType` and `config` fields on the pane nodes — it does NOT unmount/remount the DOM components
- [ ] React keys on PaneContent containers do NOT change during swap — only the content reference changes
- [ ] State inside each app (terminal history, editor content, scroll position) is preserved after swap
- [ ] Test: swap terminal and text-pane, verify both retain their content

### Fix 2: Delete empty cell via FAB
- [ ] The FAB menu on empty panes includes a "Delete Cell" option
- [ ] Clicking "Delete Cell" removes the empty pane from the tree
- [ ] The space freed by deletion is handled by the merge rules (Fix 3)
- [ ] Test: create a split with one empty pane, delete it, verify the other pane fills the space

### Fix 3: Contiguous-edge merge on delete
- [ ] When a cell is deleted, check the neighbor that shares the longest continuous border
- [ ] If that neighbor is an EMPTY cell → the empty cell expands to fill the deleted space
- [ ] If that neighbor is an APPLET (has content) → the deleted space becomes an empty cell (neighbor does NOT auto-expand)
- [ ] Merge check uses COMPUTED LAYOUT POSITIONS (actual rendered pixel coordinates), not tree parentage
- [ ] Test: 2x2 grid, delete one empty cell next to another empty cell — the empty neighbor expands
- [ ] Test: 2x2 grid, delete one empty cell next to a terminal — the space becomes empty, terminal doesn't expand
- [ ] Test: vertical split, delete left pane — right pane fills entire width

### General
- [ ] All existing shell reducer tests still pass (0 regressions)
- [ ] 12+ new tests for swap, delete, and merge operations
- [ ] No file over 500 lines

---

## Constraints

1. **Do NOT change existing split/merge actions that work** — only add the new behavior
2. **The merge rule implementation requires rendered layout dimensions** — add `layoutDimensions` field to ShellState. The renderer updates it on each layout. The reducer reads it for merge decisions.
3. **TDD required** — write tests first, then implementation
4. **CSS: `var(--sd-*)` only** — no hex, no rgb(), no named colors
5. **No file over 500 lines** — modularize at 500, hard limit 1,000
6. **All file paths must be absolute** in task files

---

## Task Breakdown (suggested)

You may write 1-3 task files depending on coupling:

**Option A: 3 separate tasks**
- TASK-056: Fix SWAP_CONTENTS to preserve React component state
- TASK-057: Add "Delete Cell" to EmptyPane FAB menu
- TASK-058: Implement contiguous-edge merge logic (includes layoutDimensions)

**Option B: 2 tasks (if delete + merge are tightly coupled)**
- TASK-056: Fix SWAP_CONTENTS
- TASK-057: Delete cell via FAB + contiguous-edge merge (combined)

**Option C: 1 task (if all three are tightly coupled)**
- TASK-056: Shell reducer swap/delete/merge fixes (all three)

Use your judgment based on code coupling and test dependencies.

---

## Smoke Test (from Spec)

- [ ] Load chat.egg.md, split a pane, swap two panes — content preserved in both
- [ ] Create an empty pane via split, delete it via FAB — space is reclaimed correctly

---

## Your Job, Q33N

1. **Read the codebase** (files listed above — absolute paths provided)
2. **Write 1-3 task files** (per breakdown above)
3. **Return task files to Q33NR for review** — DO NOT dispatch bees yet
4. **Include in each task file:**
   - Objective (one sentence)
   - Context (what the bee needs to know)
   - Files to Read First (absolute paths)
   - Deliverables (concrete outputs with checkboxes)
   - Test Requirements (TDD, edge cases, specific scenarios)
   - Constraints (no file over 500 lines, CSS vars only, no stubs)
   - Response file requirement (8 sections — copy from BOOT.md)

5. **Wait for Q33NR approval** before dispatching

---

## Model Assignment

- Swap fix: **Sonnet** (complex React state management)
- FAB delete: **Haiku** (simple UI addition) OR **Sonnet** if combined with merge
- Merge logic: **Sonnet** (complex layout calculation with dimensions)

Spec says **sonnet** — use Sonnet unless you split into subtasks where Haiku is appropriate.

---

## Budget

Check `.deia/config/queue.yml` for max session budget.
Current spec: P0 (high priority)
Use model assignments wisely.

---

**End Briefing**

Q33N, acknowledge receipt and begin investigation.
