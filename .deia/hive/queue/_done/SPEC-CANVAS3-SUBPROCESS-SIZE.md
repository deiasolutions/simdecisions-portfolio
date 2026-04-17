# SPEC-CANVAS3-SUBPROCESS-SIZE

Increase default subprocess (group) node size on drop to accommodate nested processes.

## Priority
P2

## Depends On
None

## Model Assignment
haiku

## Description

When a SubProcess node is dropped onto the canvas from the palette, it currently spawns at 400×250px. This is too small for a container expected to hold multiple child nodes. Increase the default to approximately 600×400px (w×h) — roughly a 3-wide × 2-tall grid of normal-sized phase nodes with comfortable padding.

### Current values (FlowDesigner.tsx ~line 800)
```typescript
const gw = 400, gh = 250;
```

### Target values
```typescript
const gw = 600, gh = 400;
```

### Child node repositioning
The auto-created Start and End child nodes inside the subprocess also need repositioning for the larger container:
- Start node: `x: 60, y: gh/2 - 30` (was x:40)
- End node: `x: gw - 140, y: gh/2 - 30` (was gw-120)

### Files

| File | Change |
|------|--------|
| `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx` | Change `gw` from 400→600, `gh` from 250→400, adjust child Start/End positions |

## Acceptance Criteria
- [ ] Dropping a SubProcess from the palette creates a 600×400px group node
- [ ] Auto-created Start child node is positioned near left edge with vertical centering
- [ ] Auto-created End child node is positioned near right edge with vertical centering
- [ ] SubProcess is still resizable (NodeResizer min constraints unchanged at 200×140)

## Smoke Test
1. Load canvas3 set
2. Drag SubProcess from palette onto canvas
3. Confirm the group node is noticeably larger than before — roughly 3 normal nodes wide, 2 tall
4. Confirm Start and End child nodes are inside and well-spaced

## Constraints
- Only change `FlowDesigner.tsx` — do not change GroupNode.tsx min resizer constraints
- Keep zIndex: -1 on the group node style
- Do not change any other node type defaults
