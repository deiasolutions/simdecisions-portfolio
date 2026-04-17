# TASK-BUG073: Canvas2 Light Mode Fix

**Bug ID:** BUG-073
**Priority:** P1
**Date:** 2026-03-25
**Model:** Haiku
**Estimated Effort:** Small (1-2 hours)

---

## Objective

Fix the canvas2 EGG so the canvas background responds to light/dark color mode changes. Replace all hardcoded colors with CSS variable tokens.

---

## Problem

On canvas2 EGG, switching to light color mode does not update the canvas background color. The canvas stays dark regardless of theme selection.

**Root Cause:**
1. `FlowCanvas.tsx` line 230 has `colorMode="dark"` hardcoded on the `<ReactFlow>` component
2. Multiple hardcoded rgba() colors in node components and edges
3. `MiniMap` component has hardcoded rgba colors for node/stroke

---

## Context

- **EGG file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas2.egg.md`
- **Theme system:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css`
- **Theme object:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\lib\theme.ts`
- **Light mode selector:** `.hhp-root[data-theme="light"]` (lines 271-370 in shell-themes.css)
- **Dark mode selector:** `.hhp-root` (default, lines 26-168)
- **Project rule:** All CSS must use `var(--sd-*)` tokens. No hex, no rgb(), no named colors.

---

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowCanvas.tsx` — Main canvas wrapper
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css` — Theme variables
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\lib\theme.ts` — Theme object mapping

---

## Deliverables

### 1. Fix FlowCanvas.tsx colorMode

- [ ] Remove hardcoded `colorMode="dark"` on line 230
- [ ] Dynamically read current theme from the DOM or use a useTheme hook
- [ ] Set `colorMode="light"` when `.hhp-root[data-theme="light"]` is active
- [ ] Set `colorMode="dark"` for all other themes (default, depth, monochrome, high-contrast)

**Implementation approach:**
```tsx
const [colorMode, setColorMode] = useState<'light' | 'dark'>('dark');

useEffect(() => {
  const root = document.querySelector('.hhp-root');
  const theme = root?.getAttribute('data-theme');
  setColorMode(theme === 'light' ? 'light' : 'dark');

  // MutationObserver to watch for theme changes
  const observer = new MutationObserver(() => {
    const newTheme = root?.getAttribute('data-theme');
    setColorMode(newTheme === 'light' ? 'light' : 'dark');
  });
  if (root) {
    observer.observe(root, { attributes: true, attributeFilter: ['data-theme'] });
  }
  return () => observer.disconnect();
}, []);

// Then use: colorMode={colorMode}
```

### 2. Fix MiniMap hardcoded colors

- [ ] Replace `"rgba(139,92,246,0.08)"` on line 253 with CSS variable reference
- [ ] Replace `"rgba(139,92,246,0.6)"` on line 254 with CSS variable reference
- [ ] Replace `"rgba(139,92,246,0.25)"` on line 258 with CSS variable reference
- [ ] Replace `"rgba(139,92,246,0.8)"` on line 259 with CSS variable reference

**Use these tokens:**
- `var(--sd-purple-dimmer)` for 0.08 alpha
- `var(--sd-purple-dim)` for 0.15 alpha
- `var(--sd-border)` for 0.25-0.35 alpha
- `var(--sd-purple)` for full opacity

### 3. Fix Background grid color

- [ ] Line 241: Replace `"var(--sd-purple-dim)"` with `var(--sd-grid-dot)` (theme-aware token)

### 4. Fix ContextMenu.tsx hardcoded colors

- [ ] Line 77: Replace `"1px solid rgba(139,92,246,0.2)"` with `var(--sd-border-muted)`
- [ ] Line 81: Replace `"0 8px 32px rgba(0,0,0,0.5)"` with `var(--sd-float-shadow)`
- [ ] Line 92: Replace `"rgba(139,92,246,0.1)"` with `var(--sd-bg-hover)`
- [ ] Line 109-110: Replace rgba purple/red with CSS variables

### 5. Fix broadcast-highlights.css

- [ ] Line 28: Replace `rgba(6, 182, 212, 0.05)` with `var(--sd-cyan-dimmest)`

### 6. Fix CheckpointFlash.tsx

- [ ] Line 117: Replace `rgba(0, 0, 0, 0.2)` with appropriate theme token or keep as-is (shadow opacity)

---

## Test Requirements

### Unit Tests

Create test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\FlowCanvas.theme.test.tsx`

```tsx
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { ReactFlowProvider } from '@xyflow/react';
import FlowCanvas from '../FlowCanvas';

describe('FlowCanvas theme responsiveness', () => {
  let root: HTMLElement;

  beforeEach(() => {
    root = document.createElement('div');
    root.className = 'hhp-root';
    document.body.appendChild(root);
  });

  afterEach(() => {
    document.body.removeChild(root);
  });

  it('should use dark mode by default', () => {
    const { container } = render(
      <ReactFlowProvider>
        <FlowCanvas nodes={[]} edges={[]} onNodesChange={vi.fn()} onEdgesChange={vi.fn()} onConnect={vi.fn()} mode="design" />
      </ReactFlowProvider>,
      { container: root }
    );
    const reactFlow = container.querySelector('.react-flow');
    expect(reactFlow).toHaveAttribute('data-color-mode', 'dark');
  });

  it('should use light mode when data-theme="light"', async () => {
    root.setAttribute('data-theme', 'light');
    const { container } = render(
      <ReactFlowProvider>
        <FlowCanvas nodes={[]} edges={[]} onNodesChange={vi.fn()} onEdgesChange={vi.fn()} onConnect={vi.fn()} mode="design" />
      </ReactFlowProvider>,
      { container: root }
    );
    await waitFor(() => {
      const reactFlow = container.querySelector('.react-flow');
      expect(reactFlow).toHaveAttribute('data-color-mode', 'light');
    });
  });

  it('should update colorMode when theme changes', async () => {
    const { container } = render(
      <ReactFlowProvider>
        <FlowCanvas nodes={[]} edges={[]} onNodesChange={vi.fn()} onEdgesChange={vi.fn()} onConnect={vi.fn()} mode="design" />
      </ReactFlowProvider>,
      { container: root }
    );

    // Start dark
    let reactFlow = container.querySelector('.react-flow');
    expect(reactFlow).toHaveAttribute('data-color-mode', 'dark');

    // Switch to light
    root.setAttribute('data-theme', 'light');
    await waitFor(() => {
      reactFlow = container.querySelector('.react-flow');
      expect(reactFlow).toHaveAttribute('data-color-mode', 'light');
    });

    // Switch back to dark
    root.removeAttribute('data-theme');
    await waitFor(() => {
      reactFlow = container.querySelector('.react-flow');
      expect(reactFlow).toHaveAttribute('data-color-mode', 'dark');
    });
  });

  it('should use dark mode for depth theme', async () => {
    root.setAttribute('data-theme', 'depth');
    const { container } = render(
      <ReactFlowProvider>
        <FlowCanvas nodes={[]} edges={[]} onNodesChange={vi.fn()} onEdgesChange={vi.fn()} onConnect={vi.fn()} mode="design" />
      </ReactFlowProvider>,
      { container: root }
    );
    await waitFor(() => {
      const reactFlow = container.querySelector('.react-flow');
      expect(reactFlow).toHaveAttribute('data-color-mode', 'dark');
    });
  });
});
```

- [ ] All tests pass
- [ ] Edge cases: theme attribute missing, theme switches during mount, unmount cleanup

### Manual Smoke Test

- [ ] Open http://localhost:5173/?egg=canvas2
- [ ] Canvas background is dark by default
- [ ] Switch to light mode via settings or ThemeMenu
- [ ] Canvas background changes to light
- [ ] Grid dots change color to match theme
- [ ] MiniMap colors change to match theme
- [ ] Nodes remain visible and readable in both modes
- [ ] Edges remain visible and readable in both modes
- [ ] Switch back to dark mode — canvas background changes to dark

---

## Constraints

1. **TDD:** Write tests first, then implementation (except pure CSS).
2. **No file over 500 lines.** Modularize at 500. Hard limit: 1,000.
3. **NO STUBS.** Every function fully implemented. No `// TODO`, no empty bodies.
4. **CSS: `var(--sd-*)` only.** No hex, no rgb(), no named colors. MANDATORY.
5. **All file paths must be absolute** in response file.

---

## Acceptance Criteria

- [ ] `FlowCanvas.tsx` dynamically reads theme from `.hhp-root[data-theme]`
- [ ] `colorMode` prop on `<ReactFlow>` is dynamic, not hardcoded
- [ ] MiniMap colors use CSS variables, not hardcoded rgba
- [ ] Background grid color uses `var(--sd-grid-dot)`
- [ ] ContextMenu colors use CSS variables
- [ ] broadcast-highlights.css uses CSS variables
- [ ] All hardcoded rgba() colors in canvas2 files are replaced (or documented if kept for shadows)
- [ ] Open http://localhost:5173/?egg=canvas2 and switch to light mode — canvas background changes to light
- [ ] Switch to dark mode — canvas background changes to dark
- [ ] Nodes, edges, and grid remain visible and readable in both modes
- [ ] `cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/FlowCanvas.theme.test.tsx` — all tests pass
- [ ] `cd browser && npx vitest run` — no test regressions

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260325-TASK-BUG073-CANVAS2-LIGHT-MODE-RESPONSE.md`

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

- This is a P1 bug, not a major refactor. Keep scope tight: fix the theme issue, ensure theme switching works, move on.
- Do NOT rewrite the entire canvas system. Only change what's needed for theme responsiveness.
- If you find extensive hardcoded colors in node components (PhaseNode, ResourceNode, etc.), document them in "Issues / Follow-ups" but DO NOT fix them in this task. This task is scoped to FlowCanvas, MiniMap, Background, and ContextMenu only.
- Shadow colors (rgba(0,0,0,...)) can stay as-is if they're pure black shadows — those are theme-agnostic.
- Focus on the main canvas background, grid, and minimap. Do not chase down every rgba() in the entire sim folder.

---

**END OF TASK**
