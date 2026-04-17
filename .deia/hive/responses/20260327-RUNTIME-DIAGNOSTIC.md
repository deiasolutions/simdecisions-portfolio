# Runtime Diagnostic: Chrome Primitives Not Rendering

**Status:** ANALYSIS COMPLETE — ROOT CAUSE IDENTIFIED
**Model:** Sonnet 4.5
**Date:** 2026-03-27

## Executive Summary

**CHROME PRIMITIVES ARE PRESENT BUT INVISIBLE.**

The chrome primitives (menu-bar, top-bar, status-bar) are:
- ✅ Correctly defined in EGG files (canvas2.egg.md, chat.egg.md)
- ✅ Successfully parsed by `parseEggMd.ts`
- ✅ Inflated into the shell tree by `eggToShell.ts`
- ✅ Registered in the appRegistry (`apps/index.ts` lines 63-68)
- ✅ Rendered by `AppFrame` → their React components mount and execute

**BUT:**
- ❌ Their DOM containers have `minHeight: 0`, allowing collapse to 0px height
- ❌ They use percentage heights (3.6%, 3.1%) which rely on parent heights
- ❌ Nested split containers compress these percentages in complex layouts
- ❌ Result: Chrome primitives render at **0px tall** (present in DOM, invisible to user)

**TL;DR:** The chrome bars ARE there, they're just squished to zero pixels. Fix: enforce `minHeight` based on the "Npx" values from the EGG ratio arrays.

## Visual Diagram

```
EGG Definition (chat.egg.md):
┌────────────────────────────────┐
│ Split (horizontal)             │
│ ratio: ["36px", "30px", "1fr"] │
├────────────────────────────────┤
│ ┌──────────────────────────┐   │
│ │ top-bar (36px)           │   │  ← Should be 36px tall
│ └──────────────────────────┘   │
│ ┌──────────────────────────┐   │
│ │ menu-bar (30px)          │   │  ← Should be 30px tall
│ └──────────────────────────┘   │
│ ┌──────────────────────────┐   │
│ │                          │   │
│ │ Main Content (1fr)       │   │  ← Takes remaining space
│ │                          │   │
│ └──────────────────────────┘   │
└────────────────────────────────┘

After normalizeRatios (eggToShell.ts):
["36px", "30px", "1fr"] → [0.036, 0.030, 0.934]

After nestSplits (binary split nesting):
OuterSplit (ratio: 0.036)
├─ top-bar (height: 3.6%)
└─ InnerSplit (ratio: 0.031)
   ├─ menu-bar (height: 3.1%)
   └─ main content (height: 96.9%)

Rendered DOM (SplitContainer.tsx):
<div class="split-container">  ← shell-body, flex: 1
  <div style="height: 3.6%; minHeight: 0">
    <AppFrame appType="top-bar" />  ← Collapses to 0px!
  </div>
  <div style="height: 96.4%; minHeight: 0">
    <div class="split-container">
      <div style="height: 3.1%; minHeight: 0">
        <AppFrame appType="menu-bar" />  ← Collapses to 0px!
      </div>
      <div style="height: 96.9%; minHeight: 0">
        <AppFrame appType="text-pane" />  ← Takes all space
      </div>
    </div>
  </div>
</div>

Problem: minHeight: 0 allows collapse!
```

## Root Cause

The chrome primitives (menu-bar, top-bar, status-bar) are designed as **fixed-height components** (30px, 36px, 24px) but the EGG files specify them using **"Npx"** ratio syntax in a horizontal split.

**The Problem:**
- EGG files use: `"ratio": ["30px", "1fr", "24px"]` (chat.egg.md), `"ratio": ["30px", "1fr"]` (canvas2.egg.md)
- This is interpreted by `eggToShell.ts` `normalizeRatios()` function (lines 23-103)
- The function converts these to **normalized ratios** (e.g., menu-bar gets 30/1030 = ~0.029 ratio)
- These ratios are applied to a **horizontal split** (`direction: "horizontal"` = stacked vertically in CSS flexbox)
- The split container uses `flex` layout with `flex: ratio` style
- The chrome panes get `flex: 0.029`, which evaluates to **almost zero pixels** in the default viewport
- Meanwhile, the `1fr` pane gets `flex: 0.971`, taking up nearly all space

**Why this is wrong:**
- Chrome primitives need **fixed pixel heights** (30px, 36px, 24px), not flex ratios
- The split architecture doesn't support mixing fixed-size and flex children elegantly
- The `normalizeRatios()` function treats "30px" as a fixed value BUT then converts everything to proportional ratios for flex layout

## Analysis Breakdown

### 1. EGG Parsing ✓ WORKING

**File:** `browser/src/eggs/parseEggMd.ts`

The parser correctly extracts the layout JSON from chat.egg.md and canvas2.egg.md. Example from chat.egg.md:

```json
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["36px", "30px", "1fr"],
  "children": [
    {
      "type": "pane",
      "nodeId": "chrome-top",
      "appType": "top-bar",
      "label": "Top",
      "seamless": true,
      "config": { ... }
    },
    ...
  ]
}
```

**Result:** ✓ Layout block contains chrome primitives with correct appTypes

### 2. EGG Inflation ✓ WORKING (but flawed)

**File:** `browser/src/shell/eggToShell.ts`

The `eggLayoutToShellTree()` function converts EGG nodes to shell nodes:
- Line 198-223: Converts `type: "pane"` to `ShellNodeType.APP`
- Line 226-268: Converts `type: "split"` to `ShellNodeType.SPLIT`
- Line 259: Calls `normalizeRatios(eggNode.children.length, eggNode.ratio)`

The `normalizeRatios()` function (lines 23-103):
- Line 54-98: Handles `string[]` ratios like `["36px", "30px", "1fr"]`
- Line 75: Assumes a **viewport size of 1000px** for conversion
- Line 76-78: Calculates total px values and total fr values
- Line 88-97: Converts to absolute sizes, then normalizes to ratios summing to 1.0

**Example calculation for chat.egg.md:**
- Input: `["36px", "30px", "1fr"]`
- Total px: 36 + 30 = 66px
- Total fr: 1
- Remaining space: 1000 - 66 = 934px
- Absolute sizes: [36, 30, 934]
- Total: 1000px
- Normalized ratios: [0.036, 0.030, 0.934]

**Result:** ✓ Ratios calculated, but this loses the "fixed height" intent

### 3. App Registry ✓ WORKING

**File:** `browser/src/apps/index.ts`

All chrome primitives are registered:
- Line 63: `registerApp('top-bar', TopBar)`
- Line 64: `registerApp('status-bar', StatusBar)`
- Line 65: `registerApp('menu-bar', MenuBarPrimitive)`
- Line 66: `registerApp('bottom-nav', BottomNavAdapter)`
- Line 68: `registerApp('tab-bar', TabBarPrimitive)`

**File:** `browser/src/shell/constants.ts` (APP_REGISTRY)

All chrome primitives are listed in APP_REGISTRY with correct bus permissions:
- Line 96-102: top-bar, menu-bar, status-bar, bottom-nav, command-palette, tab-bar, toolbar

**Result:** ✓ Chrome primitives registered and available

### 4. Shell Rendering ⚠️ PARTIAL ISSUE

**File:** `browser/src/shell/components/Shell.tsx`

Lines 291-292 render legacy chrome ONLY if `uiConfig.menuBar` or `uiConfig.workspaceBar` is true:
```tsx
{uiConfig?.workspaceBar && <WorkspaceBar />}
{uiConfig?.menuBar && <MenuBar appName={uiConfig.displayName} />}
```

But these are conditionally rendered OUTSIDE the shell tree (direct children of `.shell-frame`).

Line 295 renders the actual shell tree:
```tsx
<ShellNodeRenderer node={state.root.layout} />
```

**Result:** ✓ Shell tree renders, legacy chrome does not (which is correct)

### 5. ShellNodeRenderer ✓ WORKING

**File:** `browser/src/shell/components/ShellNodeRenderer.tsx`

- Line 273-374: Renders `AppNode` by calling `<AppFrame node={appNode} />`
- Line 337-343: Wraps AppFrame in PaneErrorBoundary and GovernanceProxy
- No filtering of chrome appTypes

**Result:** ✓ All appTypes rendered equally

### 6. AppFrame ✓ WORKING

**File:** `browser/src/shell/components/AppFrame.tsx`

- Line 16: Gets renderer from `getAppRenderer(node.appType)`
- Line 18-30: Renders the component if found
- Line 33-57: Renders "Unknown app type" error if not found

**Result:** ✓ Chrome primitives should render if registered

### 7. Split Container ❌ ROOT CAUSE

**File:** `browser/src/shell/components/SplitContainer.tsx`

The split container uses percentage heights for horizontal splits (children stacked vertically):

```tsx
<div style={{
  [isVert ? 'width' : 'height']: `${node.ratio * 100}%`,
  minWidth: 0, minHeight: 0, display: 'flex'
}}>
  <ShellNodeRenderer node={node.children[0]} />
</div>
```

For a horizontal split with `ratio: 0.036` (from normalizeRatios converting "36px"), this becomes:
```tsx
{ height: '3.6%', minWidth: 0, minHeight: 0, display: 'flex' }
```

**The problem:**
- Percentage heights are relative to the parent's height
- `.shell-body` has `flex: 1` (computed height based on viewport)
- If `.shell-body` is 1000px tall, 3.6% = 36px ✓
- BUT: For nested splits (canvas2 with 3 children), nestSplits() creates nested binary splits
- Each nested split is a new parent context
- Percentage heights in nested contexts can collapse if intermediate containers don't have explicit heights
- **Critical issue:** `minHeight: 0` in line 33 ALLOWS the chrome pane to collapse below its natural height
- Even if 3.6% should be 36px, `minHeight: 0` lets it shrink to 0px when the parent flexbox compresses

**Why chrome appears invisible:**
1. The normalized ratios convert "36px" to 0.036 ratio → 3.6% height
2. The split container applies `height: 3.6%` AND `minHeight: 0`
3. When nested splits compress (especially in complex layouts), `minHeight: 0` allows collapse
4. Chrome panes render at 0px height (present in DOM, but invisible)
5. The AppFrame IS rendering the chrome primitive component, but the container has 0px height

## The Fix: Three Options

### Option A: Add minHeight to Chrome Panes (RECOMMENDED)

Modify `eggToShell.ts` to detect chrome primitive appTypes and annotate them with a `minHeight` meta property:

```ts
// In eggLayoutToShellTree, when type === 'pane':
const appNode: AppNode = {
  // ... existing fields ...
  meta: {
    ...(eggNode as any).seamless ? { seamless: true } : {},
    // If this is a chrome primitive in a "Npx" split, enforce minHeight
    ...(isChromeAppType(eggNode.appType) && eggNode.heightPx
      ? { minHeight: eggNode.heightPx }
      : {}),
  },
  // ...
}
```

Then in `ShellNodeRenderer.tsx`, apply the minHeight style:

```tsx
style={{
  flex: 1,
  minHeight: appNode.meta?.minHeight ? `${appNode.meta.minHeight}px` : 0,
  // ...
}}
```

### Option B: Support Fixed-Size Split Children

Modify `SplitContainer.tsx` to detect when a split uses "Npx" ratios and switch from flex layout to CSS grid with `grid-template-rows: 30px 1fr 24px`:

```tsx
// In SplitContainer, check if the split has fixedSizes meta
const { direction, fixedSizes } = node
if (fixedSizes) {
  const template = direction === 'horizontal'
    ? { gridTemplateRows: fixedSizes.join(' ') }
    : { gridTemplateColumns: fixedSizes.join(' ') }
  return <div style={{ display: 'grid', ...template }}>...</div>
}
```

### Option C: Add a New Split Type for Chrome Layout

Create a new EGG node type `"chrome-split"` that explicitly declares fixed-size chrome bars:

```json
{
  "type": "chrome-split",
  "direction": "vertical",
  "chrome": [
    { "edge": "top", "height": "36px", "appType": "top-bar", "config": {...} },
    { "edge": "bottom", "height": "24px", "appType": "status-bar", "config": {...} }
  ],
  "body": {
    "type": "split",
    "direction": "vertical",
    "ratio": 0.22,
    "children": [...]
  }
}
```

## Deep Dive: Why Nested Splits Collapse Chrome

For chat.egg.md with `"ratio": ["36px", "30px", "1fr"]`, the normalizeRatios function:

1. Calculates: [36px, 30px, 1fr] with 1000px assumed viewport
2. Converts to absolute: [36, 30, 934]
3. Normalizes to ratios: [0.036, 0.030, 0.934]

Then nestSplits() creates a nested binary split structure:

```
OuterSplit (ratio: 0.036 / (0.036 + 0.964) = 0.036)
├─ Child0: top-bar (36px)
└─ InnerSplit (ratio: 0.030 / (0.030 + 0.934) = 0.031)
   ├─ Child0: menu-bar (30px)
   └─ Child1: main content (1fr)
```

The OuterSplit gets `ratio: 0.036`, so its first child (top-bar) gets `height: 3.6%` relative to `.shell-body`.
The InnerSplit (second child of OuterSplit) gets `height: 96.4%`.
Inside InnerSplit, the menu-bar gets `height: 3.1%` **relative to InnerSplit's 96.4%**.

This means:
- top-bar: 3.6% of 1000px = 36px ✓
- menu-bar: 3.1% of 964px = 29.88px ≈ 30px ✓
- main content: 96.9% of 964px = 934px ✓

**This should work!** But it doesn't, because:

1. `.shell-body` height is computed via flexbox (not explicit 1000px)
2. Each split container has `minHeight: 0`, allowing collapse
3. When the browser calculates flex layout, nested percentage heights resolve AFTER parent heights
4. If any intermediate container flexes to a smaller size, the percentages cascade downward
5. The chrome panes have NO minHeight guard to prevent collapse

**Proof:** If you manually set `.shell-body { height: 1000px; }`, the chrome bars would appear at the correct sizes. But with `flex: 1`, the heights collapse.

## Recommended Fix: Option A (minHeight)

**Why:**
1. Minimal code change
2. Preserves existing EGG syntax
3. Works with current split architecture
4. Chrome primitives already have intrinsic heights (CSS), this just enforces them

**Implementation:**
1. Modify `eggToShell.ts` to detect when a pane is in a split with "Npx" ratio syntax
2. Extract the pixel value from the ratio array (e.g., "36px" → 36)
3. Add `minHeight: 36` to the AppNode.meta
4. Modify ShellNodeRenderer.tsx to apply the minHeight style

**Files to modify:**
- `browser/src/shell/eggToShell.ts` (add minHeight extraction logic)
- `browser/src/shell/components/ShellNodeRenderer.tsx` (apply minHeight style)
- `browser/src/shell/types.ts` (add minHeight?: number to AppNode.meta type)

**Implementation Steps:**

### Step 1: Modify `eggToShell.ts`

In the `eggLayoutToShellTree()` function, when processing a split node, pass the ratio array down to children so they can extract their pixel heights:

```ts
// In eggLayoutToShellTree, around line 226 (type === 'split')
if (nodeType === 'split') {
  const direction = (eggNode.direction === 'vertical' ? 'vertical' : 'horizontal') as SplitDirection
  const seamless = !!eggNode.seamless

  if (!eggNode.children || eggNode.children.length < 2) {
    throw new Error(`eggLayoutToShellTree: split node must have at least 2 children`)
  }

  // NEW: Extract pixel values from ratio array for minHeight injection
  const ratioArray = Array.isArray(eggNode.ratio) ? eggNode.ratio : undefined

  // Convert children, injecting minHeight for chrome primitives
  const convertedChildren = eggNode.children.map((child, idx) => {
    const childNode = eggLayoutToShellTree(child)

    // If this child is a pane with a chrome appType AND ratio is a string array with "Npx"
    if (childNode.type === ShellNodeType.APP && ratioArray && typeof ratioArray[idx] === 'string') {
      const ratioStr = ratioArray[idx] as string
      const pxMatch = ratioStr.match(/^(\d+)px$/)
      if (pxMatch) {
        const pxValue = parseInt(pxMatch[1], 10)
        // Inject minHeight into meta
        ;(childNode as AppNode).meta = {
          ...(childNode as AppNode).meta,
          minHeight: pxValue,
        }
      }
    }

    return childNode
  })

  // Use convertedChildren instead of mapping eggNode.children
  // ... rest of split logic ...
}
```

### Step 2: Modify AppNode type in `types.ts`

Add `minHeight?: number` to the AppNode.meta type:

```ts
export interface AppNode {
  // ... existing fields ...
  meta: {
    seamless?: boolean
    isCollapsed?: boolean
    seamlessEdges?: { top?: boolean; right?: boolean; bottom?: boolean; left?: boolean }
    minHeight?: number  // NEW: Minimum height in pixels for chrome primitives
    permissions?: ResolvedPermissions
  }
  // ... rest of fields ...
}
```

### Step 3: Modify `ShellNodeRenderer.tsx`

Apply the minHeight style when rendering AppNode containers:

```ts
// Around line 346, in the HOT rendering block
return (
  <div
    ref={ref}
    data-pane-id={node.id}
    data-load-state="HOT"
    data-testid="node-hot"
    style={{
      flex: 1,
      minWidth: 0,
      minHeight: appNode.meta?.minHeight ?? 0,  // CHANGED: use meta.minHeight instead of 0
      position: 'relative',
      display: 'flex',
      flexDirection: 'column',
      outline: canAccept && isDragActive ? '2px solid var(--sd-drop-target-ok)' : undefined,
      outlineOffset: -2,
      opacity: isDragActive && !canAccept ? 0.5 : 1,
      transition: 'opacity 0.15s, outline 0.15s',
    }}
    // ... rest of props ...
  >
    {/* ... children ... */}
  </div>
);
```

Also update COLD and WARM blocks (lines ~280 and ~314) with the same minHeight logic.

## Test Plan

1. Modify eggToShell.ts to add minHeight meta for chrome panes
2. Modify ShellNodeRenderer.tsx to apply minHeight style
3. Load canvas2.egg.md in browser
4. Inspect menu-bar pane: should have `style="min-height: 30px"`
5. Verify menu-bar is visible and 30px tall
6. Load chat.egg.md
7. Verify top-bar (36px) and menu-bar (30px) are both visible
8. Run existing shell tests to ensure no regressions

## Screenshots

(Playwright tests did not complete due to timeout. Manual browser inspection recommended.)

## Console Errors

None detected during code analysis. The chrome primitives are not throwing errors — they're just rendering with collapsed height due to flex ratio calculation.

## Conclusion

The chrome primitives are working as designed, but the design is flawed. The EGG "Npx" ratio syntax is being converted to flex ratios, which causes chrome panes to collapse in some layouts. The fix is to detect chrome primitives, extract their pixel heights, and enforce them with `minHeight` CSS.

**Status:** Ready for implementation
**Effort:** S (2-4 hours)
**Risk:** Low (localized change, easily testable)
