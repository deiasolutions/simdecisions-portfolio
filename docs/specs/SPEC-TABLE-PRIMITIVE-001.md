# SPEC: Table Primitive (P-13) — AG Grid Community Edition

## Priority
P0

## Backlog
BL-TBD

## Objective
Build the table pane primitive using AG Grid Community Edition (MIT licensed). Renders rows and columns with sort, filter, group, cell editing, and clipboard paste. Registers as appType "table" in the app registry. Integrates with the relay bus for cross-pane communication. Includes SheetJS import for .xlsx/.csv file loading.

## Context
The table primitive is used by 24 of our planned products — more than any other unbuilt primitive. It's the #1 gap in the primitive set. AG Grid Community provides sort, filter, group, column resize, cell editing, copy/paste, and CSV export out of the box.

Files to read first:
- `browser/src/apps/index.ts` — app registry, see how other appTypes are registered
- `browser/src/apps/canvasAdapter.tsx` — example adapter pattern to follow
- `browser/src/primitives/canvas/CanvasApp.tsx` — example primitive wrapper
- `browser/src/infrastructure/relay_bus/` — bus API for publishing/subscribing events
- `browser/package.json` — check if ag-grid-react or ag-grid-community is already a dependency

## Dependencies to Install
```bash
cd browser
npm install ag-grid-community ag-grid-react
npm install xlsx  # SheetJS for spreadsheet import
```

## File Structure
```
browser/src/primitives/table/
├── TableApp.tsx           # AG Grid wrapper component
├── SheetSelector.tsx      # Multi-sheet dropdown (visible only when .xlsx has multiple sheets)
├── table.css              # AG Grid theme override using var(--sd-*)
├── sheetImporter.ts       # .xlsx/.csv → AG Grid row data
├── tableTypes.ts          # TypeScript types for table config
└── __tests__/
    ├── TableApp.test.tsx
    ├── sheetImporter.test.ts
    └── tableAdapter.test.ts

browser/src/apps/
├── tableAdapter.ts        # App registry adapter (follows existing adapter pattern)
```

## Acceptance Criteria

### Core Table Rendering
- [ ] AG Grid Community (v32+ latest stable) renders in a pane with rows and columns
- [ ] Column definitions come from EGG config OR from data shape (auto-detect columns from first row)
- [ ] Default column behavior: resizable, sortable
- [ ] Row data accepts JSON array: `[{ name: "Task A", status: "done", cost: 1.50 }, ...]`
- [ ] Empty state: shows "No data" message with helpful text, not a blank grid
- [ ] Loading state: shows spinner while data loads

### Sorting and Filtering
- [ ] Click column header to sort ascending/descending/none
- [ ] Filter icon on each column header — text filter for strings, number filter for numbers, date filter for dates
- [ ] Multi-column sort (shift+click)
- [ ] Filter bar at top: global text search across all columns

### Cell Editing
- [ ] Double-click a cell to edit (when config.editable: true)
- [ ] Enter confirms edit, Escape cancels
- [ ] Edited cells highlighted with var(--sd-accent) border until saved
- [ ] Read-only mode when config.editable: false (default)

### Column Management
- [ ] Drag column headers to reorder
- [ ] Right-click column header: show/hide columns, auto-size columns, pin left/right
- [ ] Column widths persist for the session (in component state, not localStorage)

### Clipboard
- [ ] Ctrl+C copies selected cells (tab-separated)
- [ ] Ctrl+V pastes from clipboard into grid when config.editable: true (handles Excel copy format)
- [ ] Paste into read-only table: silent ignore (AG Grid handles this natively)
- [ ] Select range of cells by shift+click or click+drag

### Bus Integration
- [ ] On row click: publish `table:row-selected { rowIndex, rowData }` to bus
- [ ] On cell edit: publish `table:cell-changed { rowIndex, colId, oldValue, newValue }` to bus
- [ ] On filter change: publish `table:filter-changed { filterModel }` to bus
- [ ] Listen for `table:load-data { rows, columns? }` — replaces current data
- [ ] Listen for `table:append-row { rowData }` — adds row to bottom
- [ ] Listen for `table:update-row { rowIndex, changes }` — updates specific row
- [ ] Listen for `table:clear` — empties the table

### RTD Subscription (DEFERRED — depends on ADR-RTD-001 implementation)

**RTD = Real-Time Display Value.** Every headless or visible service publishes named metrics to the platform bus. Format: `{service_id, metric_key, value, unit, currency?, timestamp}`. Emitted on state change, not on a timer. Defined in ADR-RTD-001 (2026-03-18). Not yet built in code.

Build the bus subscriber infrastructure now — the subscribe config, time window, and ring buffer — but wire it to regular bus events, not RTD-specific ones. When RTD lands, the subscription code works unchanged (it's just listening for bus messages with a metric_key field). For smoke testing, use build monitor heartbeat events as the test producer.

- [ ] Config option `subscribe: [{ metric_key: "RTD:cost_coin" }]` — table auto-appends rows as matching bus events arrive
- [ ] Each matching event becomes a row: `{ timestamp, metric_key, value, unit }`
- [ ] Auto-scroll to bottom when new rows arrive (when config.autoScroll: true)

### Sheet Import (.xlsx / .csv)
- [ ] `sheetImporter.ts` uses SheetJS to parse uploaded files
- [ ] Accepts .xlsx, .xls, .csv, .tsv
- [ ] Auto-detects column headers from first row
- [ ] Handles multiple sheets in .xlsx — SheetSelector.tsx renders dropdown inside table pane, above the grid, below pane chrome title bar. Only visible when loaded file has multiple sheets.
- [ ] Import triggered by:
  - Bus message: `table:import-file { fileContent, fileName }` (base64 or ArrayBuffer)
  - Drag-and-drop: user drags .xlsx onto the table pane
  - Terminal command: `//table import <filename>` — terminal routes via bus addressing to table pane's nodeId (uses existing envelope router pattern, same as to_explorer/to_ir/to_simulator)
- [ ] After import: columns auto-sized, data rendered, row count shown in pane chrome status slot

### Sheet Export
- [ ] Export button in table header (or terminal command `//table export`)
- [ ] Export current view (with filters applied) to .csv
- [ ] Downloads via browser download API

### AG Grid Theme Override
- [ ] ALL AG Grid colors overridden with var(--sd-*) variables
- [ ] No AG Grid default theme colors visible — fully integrated with ShiftCenter dark theme
- [ ] Specific overrides needed:
  ```css
  .ag-theme-custom {
    --ag-background-color: var(--sd-surface);
    --ag-header-background-color: var(--sd-surface-secondary);
    --ag-header-foreground-color: var(--sd-text-primary);
    --ag-foreground-color: var(--sd-text-primary);
    --ag-row-hover-color: var(--sd-hover);
    --ag-selected-row-background-color: var(--sd-accent-muted);
    --ag-range-selection-border-color: var(--sd-accent);
    --ag-border-color: var(--sd-border);
    --ag-font-family: var(--sd-font-mono);
    --ag-font-size: var(--sd-font-size-sm);
  }
  ```
- [ ] No hardcoded hex, rgb, or named colors anywhere in table.css

### App Registry
- [ ] Register `appType: "table"` in `browser/src/apps/index.ts`
- [ ] Adapter at `browser/src/apps/tableAdapter.ts` — follows same pattern as canvasAdapter, terminalAdapter
- [ ] Accepts config from EGG:
  ```yaml
  - type: app
    appType: table
    config:
      editable: false
      autoScroll: false
      columns:
        - field: name
          headerName: Name
          width: 200
        - field: status
          headerName: Status
          width: 100
        - field: cost
          headerName: Cost ($)
          width: 100
          type: numericColumn
      subscribe:
        - metric_key: "RTD:cost_coin"
  ```

### Status Display
- [ ] Table publishes status info (row count, selected count, filter active) to the existing pane chrome status slot — do NOT add a second status bar
- [ ] Uses whatever pattern other primitives use for their status text (bus message or callback to PaneChrome)
- [ ] Uses var(--sd-text-secondary) for status text

## EGG Example
```yaml
# A simple data viewer EGG
egg: data-viewer
layout:
  type: split
  direction: horizontal
  ratio: [25, 75]
  children:
    - type: app
      appType: tree-browser
      config:
        adapter: filesystem
    - type: app
      appType: table
      config:
        editable: true
```

## Smoke Test
- [ ] Load an EGG with appType: table — grid renders with empty state
- [ ] Send `table:load-data` via bus with 10 rows — data appears
- [ ] Click column header — sorts
- [ ] Double-click cell (editable mode) — edit works
- [ ] Copy cells from Excel, paste into grid — data appears
- [ ] Drag .xlsx file onto table — data imports
- [ ] Type `//table export` in terminal — .csv downloads
- [ ] Subscribe to bus events with metric_key — rows auto-append (use build monitor heartbeats as test producer)

## Model Assignment
sonnet

## Constraints
- AG Grid COMMUNITY edition only (v32+ latest stable) — do not use any module that requires a license key. If Community v32+ includes basic row grouping, use it.
- Community features that ARE available and should work: client-side sorting, filtering, cell editing, column reordering, copy/paste, CSV export, custom cell renderers.
- No file over 500 lines. If TableApp.tsx grows large, split into sub-components.
- All colors via var(--sd-*). Zero hardcoded colors.
- SheetJS (xlsx package) must be imported dynamically — it's ~1MB. Don't load it until user actually imports a file.

## Test Requirements
- 8+ tests for TableApp (render, load data, sort, filter, edit, bus events)
- 4+ tests for sheetImporter (xlsx parse, csv parse, multi-sheet, error handling)
- 3+ tests for tableAdapter (registration, config parsing, bus wiring)
- Total: 15+ tests minimum
