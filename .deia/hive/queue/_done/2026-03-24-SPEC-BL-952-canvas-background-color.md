# SPEC-BL-952: Configurable Canvas Background Color

## Priority
P2

## Objective
Allow the canvas background color and pattern to be configured independently from the color scheme/theme. Currently the canvas Background component uses hardcoded `BackgroundVariant.Dots` with `var(--sd-grid-dot)` color. Users should be able to set a custom background color (e.g. white, light gray) regardless of the active theme.

## Files to Read First
- browser/src/primitives/canvas/CanvasApp.tsx
- browser/src/primitives/canvas/canvas.css
- eggs/canvas2.egg.md

## Deliverables
1. Add canvas background config fields to CanvasApp props or pane config: `bgColor`, `bgVariant` (dots/lines/cross/none), `bgGap`, `bgSize`
2. Read background config from EGG pane config and pass to ReactFlow Background component
3. Add a bus message type `canvas:set-background` so the property panel can update background at runtime
4. Default to current behavior (dots, var(--sd-grid-dot)) when no config is provided
5. Tests: at least 3 tests covering custom background color, variant switching, and default fallback

## Acceptance Criteria
- [ ] Canvas background color can be set via EGG pane config (bgColor field)
- [ ] Background variant (dots/lines/cross/none) is configurable
- [ ] Background config is independent of the active color scheme/theme
- [ ] Property panel can change background at runtime via bus message
- [ ] Default behavior unchanged when no background config is provided
- [ ] All CSS uses var(--sd-*) variables for any new styles
- [ ] Tests pass for background customization

## Response File
20260324-TASK-BL-952-RESPONSE.md
