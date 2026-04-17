# TASK-056: Shell Swap Fix — Preserve State on Swap

**Date:** 2026-03-13
**Priority:** P0
**Model:** Sonnet
**Spec:** 2026-03-13-1801-SPEC-shell-swap-delete-merge.md
**Parent Briefing:** 2026-03-13-BRIEFING-shell-swap-delete-merge.md

---

## Objective

Fix pane swap to preserve component state (terminal history, editor content, scroll position) by swapping ONLY the app content fields, NOT the node IDs that React uses as keys.

---

## Problem

Current SWAP_CONTENTS implementation (layout.ts:279-296) extracts and swaps these fields:
```typescript
const keys = [
  'appType', 'appConfig', 'label', 'audioMuted', 'busMute', 'notification',
  'tabs', 'activeTabIndex', 'type', 'children', 'ratio', 'direction'
];
```

This likely causes React to remount the components because it swaps structural fields like `type`, `children`, etc. When components remount, all internal state is lost.

---

## Solution

The swap should ONLY exchange the "content" of app panes — the fields that determine WHAT is displayed, not WHERE or HOW:

**Fields to swap (app content):**
- `appType` — what app is running
- `appConfig` — app configuration
- `label` — pane label
- `audioMuted`, `busMute`, `notification` — UI state
- `appState` — dynamic app state (if present)

**Fields to NEVER swap (structure/identity):**
- `id` — React key, must stay stable
- `type` — node type (app/split/tabbed)
- `children`, `ratio`, `direction` — split/tab structure
- `loadState`, `sizeStates`, etc. — lifecycle state

**Key insight:** React uses `paneId` (which comes from `node.id`) as the component key. If the ID stays the same but only the content changes, React will NOT unmount/remount the component — it will just update props.

---

## Files to Modify

1. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\actions\layout.ts`**
   - Update SWAP_CONTENTS case (lines 279-296)
   - Change extracted fields to ONLY app content fields
   - Add comment explaining the React key preservation strategy

---

## Implementation Steps

### Step 1: Write tests FIRST (TDD)

Create test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\reducer.swap.test.ts`

Write 6+ tests:

```typescript
describe('SWAP_CONTENTS - State Preservation', () => {
  it('swaps appType and appConfig between two panes', () => {
    // Setup: 2-pane split with terminal and text-pane
    // Action: swap them
    // Assert: appTypes and configs are swapped
  });

  it('preserves node IDs during swap', () => {
    // Setup: 2-pane split, note both IDs
    // Action: swap
    // Assert: IDs are unchanged (critical for React key stability)
  });

  it('swaps label between panes', () => {
    // Setup: pane A label "Terminal", pane B label "Editor"
    // Action: swap
    // Assert: labels swapped
  });

  it('swaps audioMuted, busMute, notification', () => {
    // Setup: pane A muted, pane B unmuted
    // Action: swap
    // Assert: mute states swapped
  });

  it('swaps appState if present', () => {
    // Setup: pane A with appState={foo: 1}, pane B with appState={bar: 2}
    // Action: swap
    // Assert: appState swapped
  });

  it('does NOT swap structural fields (type, children, ratio)', () => {
    // Setup: swap an app node with a split node (should reject or no-op)
    // OR: verify type/children/ratio never change during swap
  });

  it('does NOT swap if either pane is locked', () => {
    // Setup: pane A locked=true
    // Action: attempt swap
    // Assert: state unchanged
  });

  it('clears swapPendingId after swap', () => {
    // Setup: state with swapPendingId set
    // Action: swap
    // Assert: swapPendingId is null
  });

  it('adds swap to undo stack with descriptive label', () => {
    // Setup: 2-pane split
    // Action: swap
    // Assert: past.length increased, label includes both pane labels
  });
});
```

Run tests, verify they fail.

### Step 2: Fix the swap logic

Edit `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\actions\layout.ts`:

**Replace lines 279-296** with:

```typescript
case 'SWAP_CONTENTS': {
  const { nodeAId, nodeBId } = action;
  if (!nodeAId || !nodeBId || nodeAId === nodeBId) return state;
  if (isLocked(state.root, nodeAId, nodeBId)) return state;

  const nodeA = findNode(state.root, nodeAId);
  const nodeB = findNode(state.root, nodeBId);
  if (!nodeA || !nodeB) return state;

  // Only swap app nodes (can't swap splits/tabs/etc)
  if (nodeA.type !== 'app' || nodeB.type !== 'app') return state;

  // Swap ONLY content fields — preserve IDs so React doesn't remount
  // React uses node.id as the component key. If we keep IDs stable,
  // components stay mounted and preserve their internal state.
  const contentFields = [
    'appType', 'appConfig', 'label',
    'audioMuted', 'busMute', 'notification',
    'appState'  // dynamic state (optional)
  ];

  const extractContent = (n: any) =>
    Object.fromEntries(contentFields.filter(k => k in n).map(k => [k, n[k]]));

  let newRoot = replaceNode(state.root, nodeAId, { ...nodeA, ...extractContent(nodeB) });
  newRoot = replaceNode(newRoot, nodeBId, { ...nodeB, ...extractContent(nodeA) });

  return {
    ...withUndo(state, newRoot, `Swap ${(nodeA as any).label || nodeAId} ↔ ${(nodeB as any).label || nodeBId}`),
    swapPendingId: null
  };
}
```

### Step 3: Verify React key preservation

Check `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneContent.tsx` to confirm `paneId` prop is derived from `node.id`.

Check `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx` or wherever PaneContent is rendered — verify it passes `node.id` as the React `key` prop.

If keys are NOT currently stable, add a comment in the response file noting this and recommend a follow-up task.

### Step 4: Run tests

```bash
cd browser
npx vitest run src/shell/__tests__/reducer.swap.test.ts
```

All 9 tests must pass.

### Step 5: Run full shell test suite

```bash
cd browser
npx vitest run src/shell/__tests__/
```

Ensure 0 regressions (all existing 231 tests still pass).

---

## Acceptance Criteria

- [ ] SWAP_CONTENTS only swaps content fields (appType, appConfig, label, audioMuted, busMute, notification, appState)
- [ ] Node IDs are NEVER swapped (preserves React keys)
- [ ] Structural fields (type, children, ratio, direction) are NEVER swapped
- [ ] Only app nodes can be swapped (reject splits/tabs)
- [ ] Locked panes cannot be swapped
- [ ] swapPendingId is cleared after swap
- [ ] Swap action adds to undo stack with descriptive label
- [ ] 9+ new tests in reducer.swap.test.ts, all passing
- [ ] All existing shell tests still pass (0 regressions)

---

## Constraints

- **TDD:** Write tests first, then implementation
- **NO STUBS:** Every function fully implemented
- **File size limit:** 500 lines (modularize if needed)
- **NO HARDCODED COLORS:** Only CSS variables

---

## Files Created/Modified

**Created:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\reducer.swap.test.ts`

**Modified:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\actions\layout.ts`

---

## Testing

```bash
# Run swap tests
cd browser
npx vitest run src/shell/__tests__/reducer.swap.test.ts

# Run full shell suite
npx vitest run src/shell/__tests__/

# Expected: 9+ new tests passing, 231 existing tests still passing (240+ total)
```

---

## Notes

- The key insight is that React component state is tied to the component instance, which is tied to the React `key` prop. If we swap node IDs, React thinks it's a different component and remounts it (losing state). If we keep IDs stable and only swap content, React updates the existing component in place.
- Terminal history, editor content, scroll position, etc. are all internal component state that survives prop updates but NOT unmounts.
- If PaneContent is currently NOT using node.id as the key, this fix may require a small change to ShellNodeRenderer to ensure keys are stable.

---

## Response File

When done, write: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260313-TASK-056-RESPONSE.md`

Use the 8-section mandatory format from BOOT.md.
