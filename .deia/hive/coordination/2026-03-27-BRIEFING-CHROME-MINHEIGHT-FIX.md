# BRIEFING: Fix Chrome Primitive Height Collapse

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-27
**Priority:** P0

## Context

Chrome primitives (menu-bar, top-bar, status-bar) are in the DOM but render at 0px height. The runtime diagnostic identified the root cause: `normalizeRatios()` in `eggToShell.ts` converts `"30px"` to flex ratio ~0.03, and `SplitContainer.tsx` applies `minHeight: 0` to all split children, allowing chrome panes to collapse.

The fix: detect "Npx" ratio values during inflation, inject `minHeight` into AppNode meta, and apply it in the renderer.

## Your Mission

**Implement the minHeight fix for chrome pane collapse. Write tests first (TDD).**

### 1. Update the AppNode type

**File:** `browser/src/shell/types.ts`

Add `minHeight?: number` to the `AppNode.meta` type definition. Find the meta interface and add the field.

### 2. Modify eggToShell.ts — inject minHeight from "Npx" ratios

**File:** `browser/src/shell/eggToShell.ts`

In the `eggLayoutToShellTree()` function, when processing a `type: "split"` node:

1. Check if `ratio` is a string array (e.g., `["30px", "1fr", "24px"]`)
2. For each child that is a pane, check if its corresponding ratio entry matches `/^(\d+)px$/`
3. If so, inject `minHeight: N` into the child's `meta` object

This must happen BEFORE `nestSplits()` is called, because nestSplits restructures the tree.

**Important:** Apply minHeight to ALL panes with "Npx" ratios, not just chrome appTypes. Any pane declared with a pixel height should respect it.

### 3. Modify SplitContainer.tsx — apply minHeight from meta

**File:** `browser/src/shell/components/SplitContainer.tsx`

When rendering split children, if a child node has `meta.minHeight`, apply it as a CSS `minHeight` style instead of `0`.

Look for where `minHeight: 0` is set on child containers and change it to read from the node's meta.

### 4. Modify ShellNodeRenderer.tsx — apply minHeight on AppNode containers

**File:** `browser/src/shell/components/ShellNodeRenderer.tsx`

In the HOT, WARM, and COLD rendering blocks for AppNode, change `minHeight: 0` to `minHeight: appNode.meta?.minHeight ? appNode.meta.minHeight + 'px' : 0`.

### 5. Write tests

**File:** `browser/src/shell/__tests__/chromeMinHeight.test.ts` (new file)

Write tests that verify:

a) `eggLayoutToShellTree()` injects `minHeight: 30` for a pane with ratio `"30px"`
b) `eggLayoutToShellTree()` injects `minHeight: 24` for a pane with ratio `"24px"`
c) `eggLayoutToShellTree()` does NOT inject minHeight for a pane with ratio `"1fr"`
d) `normalizeRatios()` still produces correct flex ratios (existing behavior unchanged)
e) For canvas2.egg.md layout: menu-bar gets `minHeight: 30`, status-bar gets `minHeight: 24`
f) For chat.egg.md layout: top-bar gets `minHeight: 36`, menu-bar gets `minHeight: 30`

Also write a render test that verifies:
g) A SplitContainer with a chrome pane child applies `min-height: 30px` to its container div

### 6. Run existing tests

Run `npx vitest run` from `browser/` to ensure no regressions. Fix any failures.

### 7. Verify with canvas2 and chat eggs

After the code change, manually verify by reading the code path:
- Load canvas2.egg.md → menu-bar should get minHeight: 30, status-bar should get minHeight: 24
- Load chat.egg.md → top-bar should get minHeight: 36, menu-bar should get minHeight: 30

## Files to Modify

1. `browser/src/shell/types.ts` — add `minHeight?: number` to AppNode meta
2. `browser/src/shell/eggToShell.ts` — inject minHeight from "Npx" ratio values
3. `browser/src/shell/components/SplitContainer.tsx` — apply minHeight from child node meta
4. `browser/src/shell/components/ShellNodeRenderer.tsx` — apply minHeight on AppNode containers
5. `browser/src/shell/__tests__/chromeMinHeight.test.ts` — NEW test file

## Files to Read First

- `browser/src/shell/eggToShell.ts` — understand normalizeRatios() and eggLayoutToShellTree()
- `browser/src/shell/types.ts` — understand AppNode and meta types
- `browser/src/shell/components/SplitContainer.tsx` — understand split rendering
- `browser/src/shell/components/ShellNodeRenderer.tsx` — understand AppNode rendering
- `.deia/hive/responses/20260327-RUNTIME-DIAGNOSTIC.md` — full root cause analysis

## Constraints

- TDD: write tests first, then implement
- Do NOT change EGG file format or syntax
- Do NOT change normalizeRatios() ratio output — just add minHeight meta alongside
- Do NOT remove `minHeight: 0` globally — only override it when meta.minHeight is present
- Keep changes minimal. This is a surgical fix.
- 500 line max per file

## Deliverable

Write response to: `.deia/hive/responses/20260327-CHROME-MINHEIGHT-FIX.md`

Include:
1. Test results (all tests passing)
2. Files modified with line numbers
3. Before/after behavior description
4. Any issues encountered

## Model Assignment

Sonnet — focused code change, TDD, 5 files.
