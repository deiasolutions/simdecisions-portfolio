# TASK-BL-956-B: FAB Dynamic EGG Discovery

## Objective
Replace EmptyPane FAB's hardcoded `APP_REGISTRY` array with dynamic EGG discovery from the populated EGG registry, and add a 3-choice prompt dialog when users select full app EGGs.

## Context

**Current state:** `EmptyPane.tsx` filters `APP_REGISTRY` (hardcoded array of 6 apps) and uses `window.confirm()` for single-pane mode.

**What needs to change:**
1. Query `getEggRegistry()` to get all available EGGs
2. Derive category from EGG layout structure:
   - **category='app'**: Multi-pane layouts (type='split' at root or nested splits)
   - **category='applet'**: Single-pane multi-primitive bundles (type='pane' with complex config)
   - **category='primitive'**: Single primitives (type='pane' with simple config)
3. When user clicks an app (category='app'), show a custom dialog with 3 choices:
   - **This pane** — dispatch `SPAWN_APP` with the app's primary appType
   - **Full screen** — navigate to EGG URL (`?egg=<eggId>`)
   - **New tab** — dispatch `ADD_TAB` then `SPAWN_APP`
4. Applets and primitives spawn directly via `SPAWN_APP` (no prompt)

**Category derivation logic:**
```typescript
function deriveCategory(egg: EggIR): AppCategory {
  const layout = egg.layout as EggLayoutNode

  // Multi-pane splits → app
  if (layout.type === 'split') return 'app'
  if (layout.type === 'tab-group') return 'app'

  // Single pane with appType → check if it's a multi-primitive bundle
  if (layout.type === 'pane') {
    // If appType is 'kanban', 'apps-home' → applet
    // If appType is 'terminal', 'text-pane', 'tree-browser' → primitive
    // Use APP_REGISTRY as fallback metadata
    const metadata = APP_REGISTRY.find(r => r.appType === layout.appType)
    return metadata?.category ?? 'primitive'
  }

  return 'primitive'
}
```

**Primary appType extraction:**
For apps with split layouts, extract the first `appType` found in the tree:
```typescript
function extractPrimaryAppType(layout: EggLayoutNode): string {
  if (layout.appType) return layout.appType
  if (layout.children?.[0]) return extractPrimaryAppType(layout.children[0])
  return 'unknown'
}
```

**Dialog component (create new file):**
`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\AppLoadDialog.tsx`

Design:
- Modal overlay with semi-transparent background
- Centered dialog box (300px wide)
- Title: "Load {displayName}?"
- Subtitle: "Choose how to open this app"
- Three buttons vertically stacked:
  1. "This pane" — loads into current pane
  2. "Full screen" — replaces entire layout
  3. "New tab" — adds to a new tab
- Close button (X) in top-right
- Escape key closes dialog
- Render via portal to `.hhp-root`
- CSS variables only

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\EmptyPane.tsx` (current FAB implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\constants.ts` (APP_REGISTRY)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\index.ts` (EGG registry)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\types.ts` (EggIR, EggLayoutNode)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts` (SPAWN_APP, ADD_TAB actions)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ContextMenu.tsx` (portal pattern reference)

## Deliverables
- [ ] New file: `AppLoadDialog.tsx` component (dialog UI)
- [ ] New file: `eggCategoryDeriver.ts` utility (category derivation logic)
- [ ] Modified: `EmptyPane.tsx` — replace APP_REGISTRY filter with EGG registry query
- [ ] Function: `deriveCategory(egg: EggIR): AppCategory`
- [ ] Function: `extractPrimaryAppType(layout: EggLayoutNode): string`
- [ ] Dialog shows displayName from EGG frontmatter
- [ ] "This pane" button dispatches `SPAWN_APP` with correct appType
- [ ] "Full screen" button navigates to `?egg=<eggId>`
- [ ] "New tab" button dispatches `ADD_TAB` then `SPAWN_APP`
- [ ] Dialog closes on Escape key
- [ ] Dialog renders via portal to `.hhp-root`
- [ ] Applets/primitives still spawn directly without prompt
- [ ] Keep APP_REGISTRY as fallback for category metadata

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  1. FAB menu shows all 20 EGGs from registry (not just hardcoded 6)
  2. Clicking an app (split layout) shows 3-choice dialog
  3. Dialog displays correct displayName from EGG frontmatter
  4. "This pane" button dispatches SPAWN_APP with primary appType
  5. "Full screen" button navigates to correct EGG URL
  6. "New tab" button dispatches ADD_TAB then SPAWN_APP
  7. Clicking an applet spawns directly without dialog
  8. Clicking a primitive spawns directly without dialog
  9. Dialog closes on Escape key
  10. Dialog renders via portal to `.hhp-root`
  11. Category derivation: split layout → 'app'
  12. Category derivation: single pane → 'primitive' or 'applet' from fallback
  13. Primary appType extraction: nested split → first appType in tree

**Minimum 13 tests required.**

## File Size Planning
- `EmptyPane.tsx`: currently 206 lines, will grow by ~50 lines (dialog state, EGG query) → **~256 lines** ✓
- `AppLoadDialog.tsx`: new file, ~120 lines (dialog UI + styling) ✓
- `eggCategoryDeriver.ts`: new file, ~60 lines (category logic + appType extraction) ✓

All files under 500 line limit.

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only — NO hardcoded colors
- No stubs — fully implement all logic
- Dialog must use portal pattern (`.hhp-root` target)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260325-TASK-BL-956-B-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
