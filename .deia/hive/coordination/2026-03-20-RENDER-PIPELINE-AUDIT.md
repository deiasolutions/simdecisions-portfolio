# ShiftCenter Browser Rendering Infrastructure — Audit

**Audited:** `browser/src/`
**Date:** 2026-03-20
**Auditor:** Q33NR

---

## 1. RENDER PIPELINE — EGG to Pixels

### Full Path: Working & Complete

**EGG File → Parsing → Shell Tree → React Components → DOM**

#### Step 1: EGG File Loading
- **Location:** `browser/src/shell/useEggInit.ts`
- **Process:** Resolves EGG ID from URL/hostname → loads `.egg.md` via Vite plugin → parses YAML frontmatter
- **Status:** WORKING

#### Step 2: EGG Parsing to IR
- `browser/src/eggs/parseEggMd.ts` — Markdown → ParsedEgg
- `browser/src/eggs/eggInflater.ts` — ParsedEgg → EggIR (schema translation)
- `browser/src/eggs/fieldTranslator.ts` — Schema v1/v2 → v3 translation
- **Status:** WORKING

#### Step 3: Shell Tree Construction
- **Converter:** `browser/src/shell/eggToShell.ts`
- **Function:** `eggLayoutToShellTree(eggNode: EggLayoutNode): ShellTreeNode`
- **Mapping:** `pane` → AppNode, `split` → SplitNode, `tab-group` → TabbedNode
- **Output:** `BranchesRoot` (4-branch system: layout, float, pinned, spotlight)
- **Status:** WORKING

#### Step 4: React Rendering
- **Root:** `browser/src/App.tsx` → `useEggInit()` → `<Shell initialState={...} />`
- **Shell:** `browser/src/shell/components/Shell.tsx` — `useReducer` + `MessageBus`, renders 4 branches
- **Status:** WORKING

#### Step 5: Recursive Node Rendering
- **Renderer:** `browser/src/shell/components/ShellNodeRenderer.tsx`
- Routes: AppNode → PaneChrome → AppFrame → registry lookup | SplitNode → SplitContainer | TabbedNode → TabbedContainer
- Load states: COLD (not mounted), WARM (invisible/preloading), HOT (visible)
- **Status:** WORKING

#### Step 6: App Registry → Primitives
- **Registry:** `browser/src/shell/components/appRegistry.ts` — `Map<string, AppRenderer>`
- **Registration:** `browser/src/apps/index.ts` — 15+ app types
- **Adapters:** terminal, text-pane, canvas, tree-browser, kanban, progress, sim, etc.
- **Status:** WORKING

---

## 2. LAYOUT SYSTEM

### Split-Pane Tree (Primary)
- **Binary splits:** `SplitContainer.tsx` — horizontal/vertical, ratio 0.0-1.0
- **Triple splits:** `TripleSplitContainer.tsx` — 3-way, two ratios
- **Max depth:** 8 levels
- **Resizable:** `SplitDivider` with drag-to-resize
- **Seamless borders:** `seamless: true` flag
- **Status:** WORKING

### Tab System
- `TabbedContainer.tsx` — reorderable tabs, per-tab close, add tab, notification badges (info/attention/governance)
- **Status:** WORKING

### Float System (Draggable Windows)
- `FloatPaneWrapper.tsx` — `react-draggable` + `react-resizable`, custom x/y/w/h, z-index layering
- **Status:** WORKING

### Pinned System (Slide-Over)
- `PinnedPaneWrapper.tsx` — slide from edges, click-outside/Escape to retract, overlay backdrop
- **Status:** WORKING

### Spotlight System (Full-Screen Overlay)
- `SpotlightOverlay.tsx` — single pane, backdrop dim, Escape to exit
- **Status:** WORKING

### NOT IMPLEMENTED
- **CSS Grid layout** — no grid system
- **Freeform canvas layout** — float panes only, no general drag-anywhere

---

## 3. CSS FOUNDATION

### CSS Variables (--sd-* system)
- **Location:** `browser/src/shell/shell-themes.css`
- **150+ variables** covering:
  - Colors: bg, surface, border, text (primary/secondary/muted), accent, state colors
  - Semantics: purple, green, orange, cyan, red (+ dim/light/hover variants)
  - Glass: bg, blur, shadow
  - Typography: font-sans, font-mono, font-xs/sm/base/md/lg
  - Shadows: sm through 2xl
  - Gradients + glow effects
  - Kanban column colors, priority colors, dev stage colors, mode colors
- **Status:** WORKING — comprehensive design token system

### Theme Switching
- **Mechanism:** `data-theme` attribute on `.hhp-root`
- **5 themes:**
  1. `full-color` (default) — dark purple, #8b5cf6 accent
  2. `depth` — deeper blacks, #a78bfa accent
  3. `light` — light mode, #6d48d8 accent
  4. `monochrome` — grayscale
  5. `high-contrast` — pure black, yellow accent (#ffff00)
- **Switcher:** `ThemePicker.tsx`
- **Persistence:** localStorage via `volumeStorage.ts` (key: `local://shell/theme`)
- **Status:** WORKING

### CSS Reset
- Minimal reset in `shell-themes.css` lines 6-23: margin/padding 0, height/width 100%, box-sizing border-box
- No heavy normalize.css
- **Status:** WORKING

### Fonts
- Primary: `'DM Sans'` (Google Fonts, 400/500/600/700)
- Mono: `'JetBrains Mono'` (Google Fonts, 400/500)
- Sizes: xs (10px), sm (11px), base (12px), md (13px), lg (16px)
- Preconnected in `index.html`
- **Status:** WORKING

### Spacing
- `--sd-shell-status-height: 32px`
- `--sd-shell-tab-height: 36px`
- `--sd-shell-prompt-height: 60px`
- `--sd-shell-divider-width: 5px`
- `--sd-shell-padding: 8px`
- **Status:** WORKING

---

## 4. RESPONSIVE / MOBILE

### Viewport
- `index.html` has `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- **Status:** PRESENT

### Media Queries
- Shell CSS (`shell.css`): `@media (max-width: 768px)` reduces status/tab heights
- Kanban: mobile sheet, card stacking
- Progress: mobile stage view
- Terminal: prompt height adjustments
- Login/Landing pages: responsive grid
- **Status:** PARTIAL — basic adjustments, not comprehensive

### Breakpoint System
- `browser/src/apps/sim/components/flow-designer/responsive/useBreakpoint.ts`
  - mobile: < 768px, tablet: 768-1023px, desktop: >= 1024px
  - Reusable hook, but only used in Sim app
- **Status:** WORKING but isolated to sim

### Touch
- Sim Flow Designer: pinch-to-zoom, pan gestures (`TouchGestures.tsx`)
- Canvas: ReactFlow built-in touch
- Shell-wide: no global touch gestures
- **Status:** PARTIAL

### Mobile Components
- Kanban: `KanbanMobileSheet.tsx` (bottom sheet)
- Progress: `MobileStageView.tsx`
- Sim: `MobileControls.tsx`, `FocusMode.tsx`, `SlideUpPanel.tsx`, `ResponsiveLayout.tsx`
- **Status:** PARTIAL — per-app, not shell-wide

### Overall Assessment
- **Desktop-first design.** Works on desktop, degrades on mobile. Not mobile-optimized.

---

## 5. PRIMITIVES INVENTORY

| Primitive | Location | Status |
|-----------|----------|--------|
| Terminal | `primitives/terminal/` | FULL |
| TextPane | `primitives/text-pane/` | FULL |
| TreeBrowser | `primitives/tree-browser/` | FULL |
| Canvas | `primitives/canvas/` | FULL |
| Kanban | `primitives/kanban-pane/` | FULL |
| Progress | `primitives/progress-pane/` | FULL |
| Settings | `primitives/settings/` | FULL |
| Dashboard | `primitives/dashboard/` | FULL |
| Auth | `primitives/auth/` | FULL |
| AppsHome | `primitives/apps-home/` | FULL |
| DrawingCanvas | `primitives/drawing-canvas/` | FULL |
| Processing | `primitives/processing/` | FULL |

No stubs identified. All registered primitives have complete implementations.

---

## 6. SUMMARY

### EXISTS & WORKING
- Complete EGG-to-pixels pipeline (load → parse → inflate → shell tree → React)
- Flexible layout (splits, tabs, float, pinned, spotlight)
- 5-theme CSS variable system (150+ tokens)
- App registry with 15+ primitives
- 4-branch root (layout, float, pinned, spotlight)
- Load state optimization (COLD/WARM/HOT)
- Message bus + governance/permissions
- Drag-drop between panes (5-zone drop, swap, move)
- Pane chrome (title bar, close, pin, collapse, mute, settings)

### STUBBED
- None identified

### MISSING
- CSS Grid layout (split-tree only)
- Freeform canvas layout
- Comprehensive mobile UX (desktop-first, responsive adjustments only)
- Shell-wide touch gestures
- PWA features (no service worker, no offline, no install prompt)
- Multi-window sync (each tab is independent)

---

**Assessment:** The rendering system is mature and production-ready for desktop web. Mobile optimization and alternative layout modes (grid, freeform) are the main gaps.
