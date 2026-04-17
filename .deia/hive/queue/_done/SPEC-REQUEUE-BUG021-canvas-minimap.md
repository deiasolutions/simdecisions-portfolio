# BUG-021 (RE-QUEUE): Canvas minimap formatting broken

## Priority
P1

## Background
The canvas minimap has weird formatting — doesn't look like the platform version. Previous bee (haiku) claimed to verify but the issue persists at runtime.

## Problem
The canvas minimap either doesn't exist or has broken styling compared to the platform repo (`platform/simdecisions-2`). No minimap component exists in `browser/src/primitives/canvas/controls/` — only ZoomControls.

## What Needs to Happen
1. Check platform repo for the minimap implementation: `platform/simdecisions-2/src/components/canvas/` or similar
2. Check if React Flow's built-in `<MiniMap>` component is being used in CanvasApp.tsx
3. If minimap exists but is unstyled, port the CSS from platform
4. If minimap doesn't exist, add React Flow's `<MiniMap>` with proper styling
5. Ensure minimap matches the platform look: correct background, node colors, viewport indicator

## Files to Read First
- `browser/src/primitives/canvas/CanvasApp.tsx` (check for MiniMap import/usage)
- `browser/src/primitives/canvas/canvas.css` (existing canvas styles)
- `platform/simdecisions-2/src/components/canvas/` (reference implementation if accessible)
- React Flow MiniMap docs for configuration options

## Deliverables
- [ ] Canvas has a working minimap
- [ ] Minimap styling matches platform aesthetic (no white zones, proper background)
- [ ] Minimap uses CSS variables (var(--sd-*)) for all colors
- [ ] Tests for minimap rendering
- [ ] No regressions in canvas tests

## Smoke Test
```bash
cd browser && npx vitest run --reporter=verbose src/primitives/canvas/
cd browser && npx vitest run
```

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
sonnet
