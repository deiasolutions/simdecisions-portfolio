# TASK-PALETTE-WRAP-GRID: Convert Canvas2 Palette to Wrapping Grid Layout

**Model:** haiku
**Priority:** P1
**Complexity:** S (Simple — CSS layout fix + color violations)

---

## Objective

Convert NodePalette's embedded mode from a single-column vertical list to a wrapping icon grid layout with overflow scroll, and fix all hardcoded rgba() color violations by replacing them with var(--sd-*) CSS variables.

---

## Context

When NodePalette renders in embedded mode (inside sidebar adapter for canvas2), all 18 items stack in a single column. The sidebar panel is ~240px wide but each button is 40px — massive wasted space. Items that overflow the pane are not visible.

Current embedded style (lines 270-273) uses `flexDirection: 'column'`, which stacks items vertically in a single column. This wastes horizontal space and causes overflow visibility issues.

Additionally, the file contains multiple hardcoded rgba() color values that violate Rule 3 (NO HARDCODED COLORS). All colors must use CSS variables from `shell-themes.css`.

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\NodePalette.tsx` (293 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\lib\theme.ts` (40 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css` (671 lines)

---

## What Needs to Change

### 1. Embedded Style Layout (lines ~270-273)

**Current:**
```typescript
const embeddedStyle: React.CSSProperties = {
  display: "flex", flexDirection: "column", gap: 2,
  padding: 8, height: "100%", overflowY: "auto",
};
```

**Change to:**
```typescript
const embeddedStyle: React.CSSProperties = {
  display: "flex",
  flexDirection: "row",
  flexWrap: "wrap",
  alignContent: "flex-start",
  gap: 2,
  padding: 8,
  height: "100%",
  overflowY: "auto",
};
```

### 2. Hardcoded Color Violations

Fix ALL rgba() colors in NodePalette.tsx using the CSS variable mappings below:

**Line 209 (borders):**
- `rgba(139,92,246,0.3)` → `var(--sd-border-subtle)`
- `rgba(139,92,246,0.15)` → `var(--sd-purple-dimmer)` (or `var(--sd-border-muted)`)

**Line 210 (backgrounds):**
- `rgba(139,92,246,0.15)` → `var(--sd-purple-dimmer)`
- `rgba(139,92,246,0.1)` → `var(--sd-accent-subtle)`

**Line 226 (tooltip border):**
- `rgba(139,92,246,0.2)` → `var(--sd-border-muted)`

**Line 229 (box-shadow):**
- `rgba(0,0,0,0.3)` → `var(--sd-shadow-md)` (use the shadow variable directly, not rgba)

**Line 265 (floating shadow):**
- `rgba(0,0,0,0.4)` → `var(--sd-shadow-xl)` (use the shadow variable directly, not rgba)

**Line 286 (divider):**
- `rgba(139,92,246,0.1)` → `var(--sd-accent-subtle)`

**CSS Variable Reference (from shell-themes.css):**
```css
--sd-border:           rgba(139,92,246,0.35);
--sd-border-hover:     rgba(139,92,246,0.5);
--sd-border-subtle:    rgba(139,92,246,0.3);
--sd-border-focus:     rgba(139,92,246,0.6);
--sd-border-muted:     rgba(139,92,246,0.2);
--sd-purple-dimmer:    rgba(139, 92, 246, 0.12);
--sd-purple-dimmest:   rgba(139, 92, 246, 0.08);
--sd-accent-subtle:    rgba(139, 92, 246, 0.1);
--sd-shadow-sm:        0 2px 8px rgba(0, 0, 0, 0.3);
--sd-shadow-md:        0 4px 16px rgba(0, 0, 0, 0.3);
--sd-shadow-lg:        0 8px 24px rgba(0, 0, 0, 0.3);
--sd-shadow-xl:        0 8px 32px rgba(0, 0, 0, 0.4);
```

### 3. Dividers in Embedded Mode

Add full-width separator dividers between sections (tools, process nodes, annotations) in embedded mode. Use `width: '100%'` flex items with proper CSS variable colors.

**Example divider in embedded mode:**
```tsx
{embedded && DIVIDER_AFTER.includes(i) && (
  <div style={{
    width: '100%',
    height: 1,
    background: 'var(--sd-border-muted)',
    margin: '4px 0'
  }} />
)}
```

---

## Deliverables

- [ ] Modified `NodePalette.tsx` with wrapping grid layout for embedded mode
- [ ] All hardcoded rgba() colors replaced with var(--sd-*) CSS variables
- [ ] Dividers render as full-width separators in embedded mode
- [ ] Floating mode (non-embedded) still works as before (single column)
- [ ] Regression tests written and passing for all changes
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\NodePalette.grid.test.tsx`

---

## Test Requirements

### Tests to Write (TDD — write tests FIRST)

1. **Embedded mode renders wrapping grid**
   - Render NodePalette with `embedded={true}`
   - Verify container style has `flexDirection: 'row'` and `flexWrap: 'wrap'`
   - Verify container has `overflowY: 'auto'`

2. **Floating mode still renders single column**
   - Render NodePalette with `embedded={false}` (or omit prop)
   - Verify container style has `flexDirection: 'column'`
   - Verify no `flexWrap` style

3. **No hardcoded colors in output**
   - Render NodePalette (both embedded and floating)
   - Query all rendered elements
   - Verify NO inline styles contain rgba() values
   - Verify all color values use var(--sd-*) format

4. **Drag-drop still works**
   - Render NodePalette
   - Simulate dragStart event on a node item
   - Verify dataTransfer contains JSON payload with paletteItem data

5. **Tooltips still appear on hover**
   - Render NodePalette
   - Simulate mouseEnter on a button
   - Verify tooltip div is rendered with label text

6. **Dividers render full-width in embedded mode**
   - Render NodePalette with `embedded={true}`
   - Verify dividers have `width: '100%'` style
   - Verify dividers use `var(--sd-border-muted)` or similar CSS variable

7. **Tool buttons still work**
   - Render NodePalette with `onToolChange` callback
   - Click on "Select" tool button
   - Verify callback called with "select"

---

## Acceptance Criteria

- [ ] Embedded palette renders as a wrapping grid (flexDirection: row, flexWrap: wrap)
- [ ] Overflow scrolls vertically (overflowY: auto)
- [ ] Zero hardcoded rgba() colors — all use var(--sd-*) CSS variables
- [ ] Floating mode (non-embedded) still works as before (single column)
- [ ] Drag-and-drop still works from grid items
- [ ] Tooltips still appear on hover
- [ ] Dividers render full-width in embedded mode
- [ ] All tests pass (7 tests minimum)
- [ ] No file exceeds 500 lines (NodePalette.tsx is currently 293 lines)

---

## Constraints

- **No file over 500 lines** — modularize if needed (Rule 4)
- **CSS: var(--sd-*) only** — no hex, no rgb(), no rgba(), no named colors (Rule 3)
- **No stubs** — every function fully implemented (Rule 6)
- **TDD** — write tests first, then implementation (Rule 5)
- **No git operations** — read-only access to git (Rule 10)

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-PALETTE-WRAP-GRID-RESPONSE.md`

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

---

## Notes

- This is a straightforward CSS fix. No architectural changes.
- The palette already has embedded/floating mode logic — we're just changing the flex layout for embedded mode.
- Color variable mappings follow existing patterns in shell-themes.css.
- If wrapping causes spacing issues, use gap property instead of margins.
- The test file should be co-located with the component in `__tests__/` subdirectory.
- Use vitest for testing (React frontend testing framework).

---

## Test Command

```bash
cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/NodePalette.grid.test.tsx
```

---

**END OF TASK FILE**
