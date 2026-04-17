# SPEC: Canvas2 palette toolbar — wrapping grid layout + overflow scroll

## Priority
P1

## Objective
Change the NodePalette embedded mode from a single-column vertical list to a wrapping icon grid, and ensure overflow scrolls. Also fix all hardcoded rgba() colors in this file.

## Context
When NodePalette renders in embedded mode (inside sidebar adapter for canvas2), all 18 items stack in a single column. The sidebar panel is ~240px wide but each button is 40px — massive wasted space. Items that overflow the pane are not visible.

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\NodePalette.tsx
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\lib\theme.ts

## What to Change

1. Embedded style (line 270-273): Change from flexDirection column to flexWrap wrap with row direction. Add alignContent flex-start and overflowY auto.

2. Hardcoded colors — fix all CSS violations in NodePalette.tsx:
   - Line 209: rgba(139,92,246,0.3) border colors
   - Line 210: rgba(139,92,246,0.15) and rgba(139,92,246,0.1) backgrounds
   - Line 226: rgba(139,92,246,0.2) tooltip border
   - Line 229: rgba(0,0,0,0.3) box-shadow
   - Line 265: rgba(0,0,0,0.4) floating shadow
   - Line 286: rgba(139,92,246,0.1) divider
   - All must become var(--sd-*) CSS variables

3. Dividers in embedded mode — add full-width separator between sections (tools, process nodes, annotations) using width 100% flex items.

## Acceptance Criteria
- [ ] Embedded palette renders as a wrapping grid (flex-wrap)
- [ ] Overflow scrolls vertically
- [ ] Zero hardcoded rgba() colors — all use var(--sd-*) CSS variables
- [ ] Floating mode (non-embedded) still works as before (single column)
- [ ] Drag-and-drop still works from grid items
- [ ] Tooltips still appear on hover
- [ ] Tests pass

## Model Assignment
haiku

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only — no hex, no rgb(), no named colors
- No stubs
- TDD
