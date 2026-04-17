# BRIEFING: BL-952 — Configurable Canvas Background Color

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-24
**Priority:** P2
**Model:** Haiku (simple feature addition)

---

## Objective

Enable canvas background color and pattern to be configurable independently from the color scheme/theme. Currently hardcoded to dots with `var(--sd-grid-dot)` at line 563 of CanvasApp.tsx.

---

## Context

The spec says:
- **Current state:** `<Background variant={BackgroundVariant.Dots} gap={20} size={2} color="var(--sd-grid-dot)" />` (CanvasApp.tsx:563)
- **Desired state:** Users can configure background color, variant (dots/lines/cross/none), gap, and size independently of theme
- **Use case:** White or light gray background for certain diagrams regardless of active theme

---

## Files to Read First

- `browser/src/primitives/canvas/CanvasApp.tsx` (line 563 — Background component, line 58-61 — CanvasAppProps)
- `eggs/canvas2.egg.md` (config section lines 64-79 — pane config for canvas-editor)
- `browser/src/primitives/canvas/canvas.css` (background-related styles if any)

---

## Requirements from Spec

1. Add canvas background config fields to CanvasApp props or pane config: `bgColor`, `bgVariant`, `bgGap`, `bgSize`
2. Read background config from EGG pane config and pass to ReactFlow Background component
3. Add a bus message type `canvas:set-background` so the property panel can update background at runtime
4. Default to current behavior (dots, var(--sd-grid-dot)) when no config is provided
5. Tests: at least 3 tests covering custom background color, variant switching, and default fallback

---

## Acceptance Criteria (from spec)

- [ ] Canvas background color can be set via EGG pane config (bgColor field)
- [ ] Background variant (dots/lines/cross/none) is configurable
- [ ] Background config is independent of the active color scheme/theme
- [ ] Property panel can change background at runtime via bus message
- [ ] Default behavior unchanged when no background config is provided
- [ ] All CSS uses var(--sd-*) variables for any new styles
- [ ] Tests pass for background customization

---

## Constraints

- **Rule 3:** All CSS must use var(--sd-*) variables only. No hex, no rgb(), no named colors.
- **Rule 4:** No file over 500 lines. CanvasApp.tsx is currently 592 lines — already over limit. You may need to recommend splitting this file.
- **Rule 5:** TDD. Tests first.
- **Rule 6:** No stubs. Full implementation.

---

## Technical Guidance

### Recommended approach:

1. **Extend CanvasAppProps** to include optional background config:
   ```typescript
   export interface CanvasAppProps {
     nodeId?: string | null;
     bus?: MessageBus | null;
     background?: {
       variant?: 'dots' | 'lines' | 'cross' | 'none';
       color?: string;
       gap?: number;
       size?: number;
     };
   }
   ```

2. **Read config from EGG pane** via `config.background` in canvas2.egg.md (pane config for canvas-editor)

3. **Add bus subscription** in CanvasInner useEffect to handle `canvas:set-background` message type

4. **Default values:**
   ```typescript
   const bgVariant = background?.variant ?? BackgroundVariant.Dots;
   const bgColor = background?.color ?? 'var(--sd-grid-dot)';
   const bgGap = background?.gap ?? 20;
   const bgSize = background?.size ?? 2;
   ```

5. **Bus permissions:** Add `canvas:set-background` to eggs/canvas2.egg.md permissions section (both bus_emit and bus_receive)

6. **File size warning:** CanvasApp.tsx is 592 lines — already violates Rule 4 (max 500 lines). Consider extracting bus subscription logic or node type mapping to separate modules.

---

## Test Requirements

Minimum 3 tests in `browser/src/primitives/canvas/__tests__/canvas-background.test.tsx`:

1. **Custom background color:** Render CanvasApp with `background={{ color: 'var(--sd-surface)' }}` and verify Background component receives it
2. **Variant switching:** Test dots/lines/cross/none variants are passed through correctly
3. **Default fallback:** Render CanvasApp with no background config and verify default (dots, var(--sd-grid-dot), gap=20, size=2)

Optional bonus tests:
- Bus message `canvas:set-background` updates background at runtime
- Gap and size customization

---

## Deliverables

Write a single task file for a bee to execute:
- Task file name: `2026-03-24-TASK-BL-952-CANVAS-BACKGROUND.md`
- Target model: Haiku
- Target role: bee
- Include all acceptance criteria from spec
- Include 8-section response file requirement

---

## Notes

- This is a P2 (low priority) feature. Keep implementation simple.
- Background color must remain a CSS variable reference, not a hardcoded color.
- If CanvasApp.tsx needs refactoring due to file size, that's a separate task — do NOT combine it with this feature.

---

**END BRIEFING**
