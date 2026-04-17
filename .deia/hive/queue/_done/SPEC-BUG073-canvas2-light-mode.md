# BUG-073: Canvas2 canvas background doesn't change in light color mode

## Objective
Fix the canvas2 EGG so the canvas background responds to light/dark color mode changes. Currently the canvas stays dark regardless of theme selection. Replace all hardcoded colors with CSS variable tokens.

## Problem Analysis
- On canvas2 EGG, switching to light color mode does not update the canvas background color
- The canvas stays dark regardless of theme selection
- Likely cause: hardcoded colors or missing CSS variable usage in FlowCanvas/drawing-canvas components
- Per project conventions, all CSS must use var(--sd-*) tokens — no hex, no rgb(), no named colors

## Files to Read First
- eggs/canvas2.egg.md
- browser/src/apps/sim/components/flow-designer/FlowCanvas.tsx
- browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx
- browser/src/apps/sim/components/flow-designer/modes/DesignMode.tsx
- browser/src/apps/sim/components/flow-designer/FlowToolbar.tsx
- browser/src/apps/sim/components/flow-designer/ZoomControls.tsx
- browser/src/apps/sim/components/flow-designer/NodePalette.tsx
- browser/src/apps/sim/components/flow-designer/nodes/PhaseNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/ResourceNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/CheckpointNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/SplitNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/JoinNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/QueueNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/CalloutNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/StickyNoteNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/AnnotationRectNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/AnnotationEllipseNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/AnnotationTextNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/AnnotationImageNode.tsx
- browser/src/apps/sim/components/flow-designer/properties/PropertyPanel.tsx
- browser/src/apps/sim/components/flow-designer/useNodeEditing.ts

## Files to Modify
- browser/src/apps/sim/components/flow-designer/FlowCanvas.tsx
- browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx
- browser/src/apps/sim/components/flow-designer/modes/DesignMode.tsx
- browser/src/apps/sim/components/flow-designer/FlowToolbar.tsx
- browser/src/apps/sim/components/flow-designer/ZoomControls.tsx
- browser/src/apps/sim/components/flow-designer/NodePalette.tsx
- browser/src/apps/sim/components/flow-designer/nodes/PhaseNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/ResourceNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/CheckpointNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/SplitNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/JoinNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/QueueNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/CalloutNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/StickyNoteNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/AnnotationRectNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/AnnotationEllipseNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/AnnotationTextNode.tsx
- browser/src/apps/sim/components/flow-designer/nodes/AnnotationImageNode.tsx
- browser/src/apps/sim/components/flow-designer/properties/PropertyPanel.tsx

## Deliverables
- [ ] Canvas background responds to light/dark mode toggle
- [ ] Grid/dot pattern also responds to theme change
- [ ] No hardcoded hex/rgb/named colors — all var(--sd-*) tokens
- [ ] Node shapes remain readable in both themes
- [ ] No regressions in dark mode appearance

## Acceptance Criteria
- [ ] Open http://localhost:5173/?egg=canvas2 and switch to light mode — canvas background changes to light
- [ ] Switch to dark mode — canvas background changes to dark
- [ ] Nodes, edges, and grid remain visible and readable in both modes
- [ ] cd browser && npx vitest run — no test regressions

## Smoke Test
- [ ] cd browser && npx vitest run src/apps/sim/ — all sim tests pass
- [ ] cd browser && npx vitest run — no regressions across full suite

## Constraints
- TDD: write tests for theme-aware styling if feasible
- No file over 500 lines
- No stubs
- CSS: var(--sd-*) only — no hex, no rgb(), no named colors

## Model Assignment
sonnet

## Priority
P1
