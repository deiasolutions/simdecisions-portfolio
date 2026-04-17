# TASK-BL-952: Canvas Background — Configurable Color and Variant

## Objective

Enable canvas background color and pattern to be configurable independently from the color scheme/theme. Currently hardcoded at `CanvasApp.tsx:563`. Users should be able to set background variant (dots/lines/cross/none), color, gap, and size via EGG pane config and runtime bus messages.

---

## Context

**Current state:**
- `<Background variant={BackgroundVariant.Dots} gap={20} size={2} color="var(--sd-grid-dot)" />` hardcoded in CanvasApp.tsx line 563
- CanvasAppProps only accepts `nodeId` and `bus`
- No background config in canvas2.egg.md pane config for canvas-editor
- No bus message handler for runtime background updates

**Design requirement:**
- Background must be independently configurable from theme/color scheme
- Useful for diagrams that need light backgrounds regardless of dark theme
- All color values must be CSS variables (`var(--sd-*)`)

**File size warning:**
- CanvasApp.tsx is 592 lines (violates Rule 4: max 500). Task implementer must NOT make it worse. If refactoring needed, flag it as a follow-up task.

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas2.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\canvas.css`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\canvasTypes.ts` (if exists, for type definitions)

---

## Deliverables

- [ ] Extend `CanvasAppProps` to include optional `background` config object
- [ ] Read background config from pane `config.background` in EGG
- [ ] Pass background props to ReactFlow `<Background>` component
- [ ] Add bus subscription to handle `canvas:set-background` messages at runtime
- [ ] Update `canvas2.egg.md` pane config with default background settings (optional fields)
- [ ] Update bus permissions in canvas2.egg.md to include `canvas:set-background` in both `bus_emit` and `bus_receive`
- [ ] Write 3+ tests covering: custom background color, variant switching, default fallback
- [ ] All CSS uses `var(--sd-*)` variables only
- [ ] No file exceeds 500 lines (CanvasApp.tsx already at 592 — do NOT make it worse)

---

## Test Requirements

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\canvas-background.test.tsx`

Write tests FIRST (TDD):

1. **Custom background color test**
   - Render `<CanvasApp background={{ color: 'var(--sd-surface)' }} />`
   - Assert `<Background color="var(--sd-surface)" ... />` appears in DOM
   - Verify other props use defaults (variant=dots, gap=20, size=2)

2. **Variant switching test**
   - Test all 4 variants: dots, lines, cross, none
   - For each variant, render with `background={{ variant: '<variant>' }}`
   - Assert `<Background variant={BackgroundVariant.<Variant>} />` rendered correctly

3. **Default fallback test**
   - Render `<CanvasApp />` (no background prop)
   - Assert Background component has defaults: variant=dots, color=var(--sd-grid-dot), gap=20, size=2

**Optional bonus tests** (if time):
- Bus message `canvas:set-background` updates background at runtime (state change)
- Gap and size customization (gap=30, size=3)
- Null/undefined background handling

---

## Technical Guidance

### Step 1: Extend CanvasAppProps

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

### Step 2: Read from EGG config

In `CanvasApp` or wrapper, read `config.background` from pane config and pass to `CanvasInner`:

```typescript
// Example (actual integration depends on how config flows to CanvasApp):
const { background } = config || {};
return <CanvasInner nodeId={nodeId} bus={bus} background={background} />;
```

### Step 3: Use in Background component

In `CanvasInner` render, replace hardcoded Background:

```typescript
const bgVariant = background?.variant ?? BackgroundVariant.Dots;
const bgColor = background?.color ?? 'var(--sd-grid-dot)';
const bgGap = background?.gap ?? 20;
const bgSize = background?.size ?? 2;

// In ReactFlow JSX:
<Background
  variant={bgVariant}
  gap={bgGap}
  size={bgSize}
  color={bgColor}
/>
```

### Step 4: Add bus handler (optional, for runtime updates)

In `CanvasInner` useEffect (alongside existing bus handlers), add:

```typescript
} else if (msg.type === 'canvas:set-background' && msg.data) {
  // Update background state from bus message
  // This requires adding state hook: const [background, setBackground] = useState(...)
  const newBg = msg.data as { variant?: string; color?: string; gap?: number; size?: number };
  setBackground(prev => ({ ...prev, ...newBg }));
}
```

**Decision:** Runtime bus update is OPTIONAL. If it complicates CanvasApp further (already 592 lines), flag as follow-up task. Default behavior (read from EGG config) is sufficient for P2 feature.

### Step 5: Update canvas2.egg.md

In pane config for `canvas-editor` (lines 70-78), add optional background config:

```json
"config": {
  "defaultMode": "design",
  "zoomEnable": true,
  "gridSnap": true,
  "background": {
    "variant": "dots",
    "color": "var(--sd-grid-dot)",
    "gap": 20,
    "size": 2
  },
  "links": {
    "from_palette": "canvas-sidebar",
    "to_properties": "canvas-sidebar"
  }
}
```

Update permissions section (lines 242-265) to add `canvas:set-background`:

```json
"bus_emit": [
  ..., "canvas:set-background"
],
"bus_receive": [
  ..., "canvas:set-background"
]
```

### Step 6: CSS

No new CSS needed. Existing `canvas.css` is compliant with var(--sd-*) only.

---

## Constraints

- **Rule 3:** All CSS must use `var(--sd-*)` variables only. No hex, rgb(), or named colors.
- **Rule 4:** No file over 500 lines. CanvasApp.tsx is already 592. Do NOT add more than 20-30 lines of code. If this requires refactoring CanvasApp (extracting bus handlers, etc.), recommend it as a follow-up task and stay focused on the background feature.
- **Rule 5:** TDD. Write tests first.
- **Rule 6:** No stubs. Full implementation.
- **Rule 8:** All file paths must be absolute.

---

## Acceptance Criteria (from spec)

- [ ] Canvas background color can be set via EGG pane config (`bgColor` or `background.color` field)
- [ ] Background variant (dots/lines/cross/none) is configurable
- [ ] Background config is independent of the active color scheme/theme
- [ ] Property panel can change background at runtime via bus message (OPTIONAL — can defer to follow-up)
- [ ] Default behavior unchanged when no background config is provided
- [ ] All CSS uses `var(--sd-*)` variables for any new styles
- [ ] Tests pass for background customization (3+ tests)
- [ ] No file exceeds 500 lines (do not make CanvasApp.tsx worse)

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260324-TASK-BL-952-CANVAS-BACKGROUND-RESPONSE.md`

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

- P2 priority. Keep it simple.
- Background color MUST remain a CSS variable reference, never hardcoded.
- If runtime bus update proves complex (due to file size), skip it. The static EGG config approach is sufficient.
- Check if CanvasApp needs refactoring. If yes, that's a separate task — do NOT combine it.
