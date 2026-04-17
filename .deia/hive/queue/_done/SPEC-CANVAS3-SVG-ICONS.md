# SPEC-CANVAS3-SVG-ICONS

Replace Unicode/emoji icons in the canvas tool palette with proper SVG icon components.

## Priority
P3

## Depends On
None

## Model Assignment
sonnet

## Description

The canvas tool palette (NodePalette.tsx) and FlowToolbar.tsx use a mix of SVG icon components and Unicode/emoji strings. Several tools still use text icons that render inconsistently across platforms. Replace all remaining non-SVG icons with SVG components matching the existing icon style.

### Icons Already Using SVGs (no change needed)
- Pointer, Select, Lasso, Pan tools
- All alignment actions (AlignLeft, AlignCenter, AlignRight, etc.)
- All distribution/layout actions (DistributeH, DistributeV, AutoLayout*)
- SubProcess node

### Icons Still Using Unicode/Emoji (need replacement)

**Node types in NodePalette.tsx PALETTE_ITEMS:**
| Node | Current Icon | SVG Description |
|------|-------------|-----------------|
| Start | `"▶"` | Right-pointing triangle in circle |
| Task/Process | `"◆"` | Rounded rectangle |
| Decision | `"◇"` | Diamond outline |
| Resource | `"⚙"` | Gear/cog |
| End | `"⏹"` | Square in circle |
| Parallel Split | `"⫘"` | Horizontal bar with down arrows |
| Parallel Join | `"⫗"` | Up arrows with horizontal bar |
| Queue | `"⊟"` | Hourglass or buffer icon |
| Text annotation | `"T"` | Letter T with serifs |
| Rectangle | `"▢"` | Rectangle outline |
| Ellipse | `"○"` | Ellipse outline |
| Line | `"—"` | Diagonal line |
| Sticky Note | `"📝"` | Note with folded corner |
| Image | `"🖼"` | Frame with mountain/sun |
| Callout | `"💬"` | Speech bubble |

### Files

| File | Change |
|------|--------|
| `browser/src/apps/sim/components/flow-designer/icons.ts` | Add 15 new SVG icon components |
| `browser/src/apps/sim/components/flow-designer/NodePalette.tsx` | Replace string icons with SVG component refs |
| `browser/src/apps/sim/components/flow-designer/FlowToolbar.tsx` | Replace any remaining string icons |

## Acceptance Criteria
- [ ] All palette items render SVG icons (no Unicode characters, no emoji)
- [ ] Icons are monochrome, using `currentColor` for stroke/fill
- [ ] Icons render at same size as existing SVG icons (14x14 in toolbar, 16x16 in palette)
- [ ] Icons are visually consistent with existing SVG style (thin stroke, minimal detail)

## Smoke Test
1. Load canvas3 set
2. Open the tool palette — all icons render as clean SVGs
3. Hover/select tools — icons inherit the active/hover color correctly
4. No emoji or Unicode boxes visible in palette

## Constraints
- Add SVG components to existing `icons.ts` file
- Use `currentColor` for all strokes/fills
- Match existing icon style: `strokeWidth="1.5"`, `strokeLinecap="round"`, `strokeLinejoin="round"`
- viewBox should be `"0 0 24 24"` for consistency
