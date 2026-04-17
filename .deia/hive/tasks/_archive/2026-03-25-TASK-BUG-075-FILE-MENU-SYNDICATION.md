# TASK-BUG-075: Move save/import/export from toolbar to File menu

## Objective

Split FlowDesigner's toolbar action syndication so only undo/redo remain as toolbar icons. Move save/import/export to the File menu via `menu:items-changed` bus event. Update MenuBar to render syndicated File menu items using the same pattern as Edit/View menus.

## Context

Canvas toolbar currently publishes 5 actions via `toolbar:actions-changed`: undo, redo, save, import, export. The file operations (save/import/export) belong in the File menu, not the toolbar. The toolbar should only show history operations (undo/redo).

MenuBar already supports syndicated menu groups for Edit and View menus. The same pattern needs to be applied to the File menu. FlowDesigner already listens for `menu:action-invoked` and handles all 5 actions (lines 442-494), so no changes are needed to the listener — only to what gets published where.

### Current Implementation

**FlowDesigner.tsx lines 338-356:**
- Publishes 5 toolbar actions (undo, redo, save, import, export)
- All 5 appear as toolbar buttons

**FlowDesigner.tsx lines 358-372:**
- Listens for `toolbar:action-invoked`
- Handles undo, redo, save, import, export

**FlowDesigner.tsx lines 442-494:**
- Listens for `menu:action-invoked`
- Handles canvas-*, edit-*, canvas-mode-* actions (NOT save/import/export yet)

**MenuBar.tsx lines 268-314:**
- File menu dropdown with New Tab, Close Tab, Settings
- NO syndicated groups rendering (unlike Edit/View menus)

### Required Changes

**FlowDesigner.tsx (lines 338-356):**
1. Split toolbar emission: only undo/redo actions
2. Add new menu emission: save/import/export targeting 'file' menu
3. Both emissions should check `hasSidebarPalette` guard
4. Menu emission should be in separate useEffect after toolbar emission

**FlowDesigner.tsx (lines 442-494):**
1. Add cases for "save", "import", "export" to the menu listener switch statement
2. Call `fileOpsRef.current?.save()`, `fileOpsRef.current?.load()`, `fileOpsRef.current?.exportFlow()`

**MenuBar.tsx (lines 268-314):**
1. After the Settings button (line 311), add syndicated groups rendering
2. Use `getSyndicatedGroups('file')` with .map() pattern
3. Follow exact same pattern as Edit menu (lines 344-377) or View menu (lines 467-500)

### Expected Behavior After Fix

**When canvas pane is focused:**
- Toolbar: Undo (↩) | Redo (↪) only
- File menu:
  - New Tab ▶
  - Close Tab
  - Settings
  - ─── (divider before syndicated groups)
  - Flow ▶ (syndicated submenu)
    - Save Flow (Ctrl+S)
    - Import Flow
    - Export Flow

**When canvas pane is NOT focused:**
- Toolbar: empty
- File menu: only default items (New Tab, Close Tab, Settings)

### Bus Event Types

These types already exist in `browser/src/shell/types.ts`:

```typescript
interface SyndicatedMenuGroup {
  targetMenu: string;        // 'file' | 'edit' | 'view' | 'tools'
  groupLabel: string;        // 'Flow'
  items: SyndicatedMenuItem[];
}

interface SyndicatedMenuItem {
  id: string;               // 'save' | 'import' | 'export'
  label: string;            // 'Save Flow' | 'Import Flow' | 'Export Flow'
  shortcut?: string;        // 'Ctrl+S' for save
  disabled?: boolean;
  checked?: boolean;
  separator?: boolean;
}
```

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx` (lines 338-372 toolbar/menu publish, lines 442-494 menu listener)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\MenuBar.tsx` (lines 268-314 File menu, lines 344-377 Edit menu pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\FlowToolbar.test.tsx` (test patterns)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\MenuBar.test.tsx` (test patterns)

## Deliverables

- [ ] FlowDesigner toolbar emission contains ONLY undo/redo (2 actions)
- [ ] FlowDesigner menu emission contains save/import/export targeting 'file' (1 group, 3 items)
- [ ] FlowDesigner menu listener handles save/import/export action IDs
- [ ] MenuBar File menu renders syndicated groups after Settings button
- [ ] MenuBar File menu divider appears before syndicated groups (when present)
- [ ] Tests updated: FlowDesigner toolbar/menu syndication tests (NEW test file recommended)
- [ ] Tests updated: MenuBar File menu syndication tests (extend existing MenuBar.test.tsx)
- [ ] All existing tests still pass (no regressions)

## Test Requirements

### FlowDesigner Tests

Create new test file: `browser/src/apps/sim/components/flow-designer/__tests__/FlowDesigner.syndication.test.tsx`

**Test cases (minimum 8):**
1. Toolbar emission contains 2 actions (undo, redo) when hasSidebarPalette=false
2. Toolbar emission includes disabled state for undo/redo based on canUndo/canRedo
3. Menu emission contains 1 group with targetMenu='file'
4. Menu emission group has groupLabel='Flow' and 3 items (save, import, export)
5. Menu emission includes shortcut 'Ctrl+S' for save action
6. Menu emission does NOT fire when hasSidebarPalette=true (sidebar layout)
7. Menu listener handles 'save' action by calling fileOpsRef.current.save()
8. Menu listener handles 'import' and 'export' actions correctly

**Test structure:**
- Use @testing-library/react (same as MenuBar tests)
- Mock bus.send and bus.subscribe
- Render FlowDesigner with minimal props
- Verify bus.send calls for toolbar and menu emissions
- Simulate menu:action-invoked messages and verify fileOpsRef calls

### MenuBar Tests

Extend `browser/src/shell/components/__tests__\MenuBar.test.tsx`

**Test cases (minimum 4):**
1. File menu renders syndicated groups when syndicatedMenus contains targetMenu='file'
2. File menu shows divider before syndicated groups
3. Clicking syndicated File menu item emits menu:action-invoked with correct actionId
4. File menu does NOT show syndicated groups when syndicatedMenus is empty

**Test structure:**
- Add new describe block: "File menu syndication"
- Mock bus to inject menu:items-changed with file-targeted groups
- Verify rendering of syndicated submenus
- Verify menu:action-invoked emission on click

### Smoke Tests

```bash
cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/FlowDesigner.syndication.test.tsx
cd browser && npx vitest run src/shell/components/__tests__/MenuBar.test.tsx
cd browser && npx vitest run src/apps/sim/ -- all sim tests pass
cd browser && npx vitest run src/shell/ -- all shell tests pass
cd browser && npx vitest run -- no regressions
```

## Acceptance Criteria

- [ ] Toolbar area only shows undo/redo icons when canvas is focused
- [ ] File menu shows Save Flow, Import Flow, Export Flow when canvas is focused
- [ ] Clicking File > Flow > Save Flow triggers save action
- [ ] Clicking File > Flow > Import Flow triggers import action
- [ ] Clicking File > Flow > Export Flow triggers export action
- [ ] Undo/Redo still work from toolbar buttons
- [ ] Tests updated and all passing (minimum 12 new tests total)
- [ ] Build passes with no regressions

## Constraints

- TDD: Write tests FIRST, then implementation
- No file over 500 lines (FlowDesigner is currently ~800 lines — verify changes don't make it worse)
- CSS: var(--sd-*) only (no CSS changes needed for this task)
- No stubs — all functions fully implemented
- Menu syndication must use the EXACT same pattern as Edit menu (lines 344-377 in MenuBar.tsx)
- FlowDesigner menu emission must follow the EXACT same structure as lines 379-440 (View/Edit/Tools menus)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260325-TASK-BUG-075-RESPONSE.md`

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

## Notes

- This is a simple refactoring — no new features, just moving existing actions from one syndication channel to another
- The bus event types already exist (SyndicatedMenuGroup, SyndicatedMenuItem)
- The MenuBar already knows how to render syndicated groups (see Edit/View menus)
- FlowDesigner already listens for menu:action-invoked, just needs save/import/export cases added
- The only NEW code is: splitting the toolbar emission, adding menu emission, adding File menu rendering in MenuBar
- FlowDesigner.tsx is currently 800+ lines — this is a bug fix, not a refactor, so don't modularize it in this task
