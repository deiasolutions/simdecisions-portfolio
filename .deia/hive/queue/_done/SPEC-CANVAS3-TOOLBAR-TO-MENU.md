# SPEC-CANVAS3-TOOLBAR-TO-MENU

Move save/import/export actions from menu bar toolbar area into the File menu.

## Priority
P2

## Depends On
None

## Model Assignment
sonnet

## Description

FlowDesigner.tsx emits `TOOLBAR_ACTIONS_CHANGED` bus events (lines ~342-361) that cause undo/redo/save/import/export buttons to appear as icon buttons in the menu bar's right-side toolbar area. These should instead be syndicated as items under the **File** menu dropdown.

### Current Behavior
FlowDesigner sends toolbar actions to the bus:
```
actions: [
  { id: "undo", icon: "↩", label: "Undo", shortcut: "Ctrl+Z" },
  { id: "redo", icon: "↪", label: "Redo", shortcut: "Ctrl+Y" },
  { id: "save", icon: "💾", label: "Save", shortcut: "Ctrl+S" },
  { id: "import", icon: "📥", label: "Import" },
  { id: "export", icon: "📤", label: "Export" },
]
```
MenuBarPrimitive renders these as `.menu-bar-action-btn` buttons to the right of the menus.

### Target Behavior
Replace the `TOOLBAR_ACTIONS_CHANGED` emission with `MENU_ITEMS_CHANGED` emission, targeting the `file` menu. The MenuBarPrimitive already supports syndicated menu items via `getSyndicatedGroups('file')`.

### Files

| File | Change |
|------|--------|
| `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx` | Replace `TOOLBAR_ACTIONS_CHANGED` with `MENU_ITEMS_CHANGED` syndicated to `file` menu |

### Syndicated Menu Format
```typescript
{
  type: BUS_MESSAGE_TYPES.MENU_ITEMS_CHANGED,
  data: {
    menus: [{
      targetMenu: 'file',
      groupLabel: 'Diagram',
      items: [
        { id: 'undo', label: 'Undo', shortcut: 'Ctrl+Z', disabled: !canUndo },
        { id: 'redo', label: 'Redo', shortcut: 'Ctrl+Y', disabled: !canRedo },
        { id: 'save', label: 'Save Diagram', shortcut: 'Ctrl+S' },
        { id: 'import', label: 'Import...', shortcut: 'Ctrl+O' },
        { id: 'export', label: 'Export PHASE-IR', shortcut: 'Ctrl+E' },
      ]
    }]
  }
}
```

## Acceptance Criteria
- [ ] No undo/redo/save/import/export buttons appear in the menu bar toolbar area
- [ ] File menu shows a "Diagram" submenu group with undo, redo, save, import, export
- [ ] Clicking menu items triggers the same actions as before (via `MENU_ACTION_INVOKED` bus event)
- [ ] Undo/redo disabled state is reflected in the menu items

## Smoke Test
1. Load canvas3 set
2. Open File menu — see Diagram submenu with all 5 actions
3. No icon buttons visible in the menu bar right side (except user status)
4. Click Save in the File > Diagram submenu — verify it triggers save

## Constraints
- Do not remove keyboard shortcut handling — shortcuts must still work
- Do not change MenuBarPrimitive.tsx — it already handles syndicated menus
- Keep the `MENU_ACTION_INVOKED` handler in FlowDesigner for receiving menu clicks
