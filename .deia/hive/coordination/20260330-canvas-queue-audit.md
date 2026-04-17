# Canvas Queue Audit — Last 21 Days (2026-03-09 → 2026-03-30)

## Active (3)

| Spec | Priority | Model | Status |
|------|----------|-------|--------|
| SPEC-CANVAS3-KEBAB-ALIGN | P2 | haiku | In queue (Gate 0 fixed — was missing `- [ ]` checkbox format) |
| SPEC-CANVAS3-SVG-ICONS | P3 | sonnet | In queue (Gate 0 fixed) |
| SPEC-CANVAS3-TOOLBAR-TO-MENU | P2 | sonnet | In queue (Gate 0 fixed) |

## Done / CLEAN (26)

| Spec | Priority | Date | Summary |
|------|----------|------|---------|
| 2026-03-14-0200-SPEC-canvas-app | P0 | 03-13 | ReactFlow Canvas EGG — initial build |
| 2026-03-15-1016-SPEC-w1-06-canvas-node-types | P0 | 03-15 | Canvas node types |
| 2026-03-15-1036-SPEC-w1-07-canvas-animation | P0 | 03-15 | Canvas animation |
| 2026-03-15-1124-SPEC-w1-08-canvas-lasso-zoom | P0 | 03-15 | Canvas lasso + zoom controls |
| 2026-03-15-1206-SPEC-w1-09-canvas-tests | P0 | 03-15 | Canvas test suite (65 passing) |
| 2026-03-15-1519-SPEC-w1-15-canvas-chatbot-dialect | P0 | 03-15 | Canvas chatbot dialect |
| 2026-03-15-1536-SPEC-w2-02-canvas-chatbot-wire | P0 | 03-15 | Canvas chatbot bus wiring |
| 2026-03-15-1558-SPEC-w2-03-properties-canvas-wire | P0 | 03-15 | Properties panel canvas wire |
| 2026-03-15-2310-SPEC-rebuild-R11-canvas-route-target | P0 | 03-15 | Canvas route target fix |
| 2026-03-16-1022-SPEC-w2-05-des-canvas-visual | P0 | 03-16 | DES canvas visual styling |
| 2026-03-16-1042-SPEC-w2-09-canvas-palette-dnd | P0 | 03-16 | Canvas palette drag-and-drop |
| 2026-03-16-1501-SPEC-w2-03-properties-canvas-wire | P0 | 03-16 | Properties canvas wire (requeue) |
| 2026-03-16-1502-SPEC-w2-09-palette-drag-fix | P0 | 03-16 | Palette drag fix |
| 2026-03-16-SPEC-TASK-237-canvas-egg-verified | P1 | 03-16 | canvas.egg.md verified (W4) |
| 2026-03-17-SPEC-TASK-BUG018-canvas-ir-wrong-pane | P0 | 03-17 | Canvas IR response appears in wrong pane |
| 2026-03-17-SPEC-TASK-BUG019-canvas-drag-captured-by-stage | P0 | 03-17 | Canvas drag captured by Stage |
| 2026-03-17-SPEC-TASK-BUG020-canvas-ir-terminal-hides-response | P0 | 03-17 | Canvas IR terminal hides response |
| 2026-03-17-SPEC-TASK-BUG021-canvas-minimap-white-zone | P0 | 03-17 | Canvas minimap white zone |
| 2026-03-17-SPEC-TASK-BUG022-canvas-components-panel-plain | P0 | 03-17 | Canvas components panel plain text |
| 2026-03-18-SPEC-TASK-BUG037-palette-click-to-add-broken | P0 | 03-18 | Palette click-to-add broken |
| 2026-03-18-SPEC-TASK-FIX-BUG022B-palette-click-dispatch | P0 | 03-18 | Palette click dispatch fix |
| 2026-03-18-SPEC-REQUEUE-BUG022B-canvas-click-to-place | P0 | 03-18 | Canvas click-to-place requeue |
| 2026-03-18-1937-SPEC-fix-REQUEUE-BUG022B-canvas-click-to-place | P0 | 03-18 | Canvas click-to-place fix cycle |
| SPEC-REQUEUE-BUG021-canvas-minimap | P0 | 03-19 | Canvas minimap requeue |
| 2026-03-24-SPEC-BL-952-canvas-background-color | P2 | 03-25 | Configurable canvas background color |
| 2026-03-24-SPEC-BUG-071-canvas-pointer-resize | P1 | 03-25 | Canvas pointer/select tool + node resize |
| 2026-03-24-SPEC-BUG-canvas2-ir-not-reaching-canvas | P1 | 03-27 | Canvas2 IR not reaching canvas |
| 2026-03-24-SPEC-canvas2-palette-wrap | P1 | 03-25 | Canvas2 palette toolbar wrapping grid |
| SPEC-BUG073-canvas2-light-mode | P1 | 03-25 | Canvas2 background doesn't change in light mode |
| SPEC-CANVAS3-CHAT-TERMINAL | P1 | 03-30 | Canvas3 third pane → terminal |

## On Hold (2)

| Spec | Priority | Blocked By | Summary |
|------|----------|------------|---------|
| 2026-03-17-SPEC-TASK-BUG023-canvas-components-no-collapse | P0 | BUG-022 | Palette doesn't collapse to icon-only mode |
| 2026-03-18-SPEC-TASK-BUG038-drag-to-canvas-still-broken | P0 | — | Drag from palette to canvas still not working |

## Staging (2)

| Spec | Priority | Chain | Summary |
|------|----------|-------|---------|
| 2026-03-18-SPEC-STAGING-BUG019-canvas-drag-isolation | P0 | Canvas chain 2/3 | Canvas drag captured by Stage (staging) |
| 2026-03-18-SPEC-STAGING-BUG018-canvas-ir-wrong-pane | P0 | Canvas chain 3/3 | Canvas IR wrong pane (staging) |

## Dead / Superseded (4)

| Spec | Priority | Summary |
|------|----------|---------|
| 2026-03-15-1745-SPEC-rebuild-06-terminal-canvas | P0 | Terminal canvas rebuild — superseded |
| 2026-03-15-2103-SPEC-w2-05-des-canvas-visual | P0 | DES canvas visual — superseded |
| 2026-03-15-2103-SPEC-w2-09-canvas-palette-dnd | P0 | Canvas palette DnD — superseded |
| 2026-03-16-1608-SPEC-fix-w2-09-canvas-palette-dnd | P0 | Canvas palette DnD fix — superseded |

## Stuck / Didn't Go Through

These are the specs that hit problems:

1. **BUG-023 (palette collapse)** — on hold, blocked by BUG-022 completion
2. **BUG-038 (drag to canvas)** — on hold, no clear dependency but still stuck
3. **BUG-019 + BUG-018 staging copies** — sitting in `_staging/` since 03-18, never promoted
4. **CANVAS3 batch (kebab, SVG icons, toolbar-to-menu)** — bounced twice to `_needs_review` due to Gate 0 rejection (acceptance criteria used `- item` instead of `- [ ] item`)

## Totals

| Status | Count |
|--------|-------|
| Active/queued | 3 |
| Done (CLEAN) | 30 |
| On hold | 2 |
| Staging | 2 |
| Dead | 4 |
| **Total** | **41** |
