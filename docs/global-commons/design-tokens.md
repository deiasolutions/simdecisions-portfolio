# Design Tokens — Default Theme

**Source:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css`
**Last Updated:** 2026-03-17

---

## Overview

**Design tokens** are named CSS variables that define the visual language of DEIA applications. Instead of hardcoding colors, shadows, and typography throughout the codebase, all styles reference tokens like `var(--sd-purple)` or `var(--sd-shadow-md)`.

This approach provides:
- **Consistency:** All components use the same color palette
- **Maintainability:** Changing a token value updates all usages
- **Themability:** Different themes override token values (see [design-tokens-themes.md](design-tokens-themes.md))

This document describes the **default theme** (full-color dark purple). For theme variants, see [design-tokens-themes.md](design-tokens-themes.md).

---

## Color System

### Base Colors

**Purpose:** Core background and surface colors

| Token | Value | Description |
|-------|-------|-------------|
| `--sd-bg` | `#0e0a1a` | Main background color (deep purple-black) |
| `--sd-surface` | `#1a1428` | Surface color for cards, panels, and containers |
| `--sd-surface-alt` | `#0f0b1a` | Alternative surface (slightly darker than main bg) |
| `--sd-surface-hover` | `#1f1930` | Surface color on hover state |

**Usage:**
```css
.card {
  background: var(--sd-surface);
  border: 1px solid var(--sd-border);
}

.card:hover {
  background: var(--sd-surface-hover);
}
```

---

### Border Colors

**Purpose:** Border colors for UI elements

| Token | Value | Description |
|-------|-------|-------------|
| `--sd-border` | `rgba(139,92,246,0.35)` | Default border (purple with transparency) |
| `--sd-border-hover` | `rgba(139,92,246,0.5)` | Border on hover (more opaque) |
| `--sd-border-subtle` | `rgba(139,92,246,0.3)` | Subtle border (less visible) |
| `--sd-border-focus` | `rgba(139,92,246,0.6)` | Border on focus state (most opaque) |
| `--sd-border-muted` | `rgba(139,92,246,0.2)` | Very subtle border (minimal visibility) |

**Usage:**
```css
input {
  border: 1px solid var(--sd-border);
}

input:focus {
  border-color: var(--sd-border-focus);
  box-shadow: 0 0 0 2px var(--sd-accent);
}
```

---

### Primary Accent Colors

**Purpose:** Main accent colors for UI states (success, warning, error, info)

| Token | Value | Description |
|-------|-------|-------------|
| `--sd-purple` | `#8b5cf6` | Primary accent color (purple) |
| `--sd-purple-dim` | `rgba(139,92,246,0.15)` | Dimmed purple (for backgrounds) |
| `--sd-green` | `#22c55e` | Success/positive state color |
| `--sd-green-dim` | `rgba(34,197,94,0.15)` | Dimmed green background |
| `--sd-orange` | `#f59e0b` | Warning/caution color |
| `--sd-orange-dim` | `rgba(245,158,11,0.15)` | Dimmed orange background |
| `--sd-yellow` | `#f59e0b` | Highlight/alert color |
| `--sd-cyan` | `#06b6d4` | Info/secondary accent |
| `--sd-cyan-dim` | `rgba(6,182,212,0.15)` | Dimmed cyan background |
| `--sd-red` | `#ef4444` | Error/danger color |
| `--sd-red-dim` | `rgba(239,68,68,0.1)` | Dimmed red background |

**Usage:**
```css
.success-badge {
  background: var(--sd-green-dim);
  color: var(--sd-green);
  border: 1px solid var(--sd-green);
}

.error-message {
  background: var(--sd-red-dim);
  color: var(--sd-red);
}
```

---

### Text Colors

**Purpose:** Typography hierarchy

| Token | Value | Description |
|-------|-------|-------------|
| `--sd-text-primary` | `#f0edf6` | Primary text color (near-white) |
| `--sd-text-secondary` | `#9a8fb5` | Secondary text (dimmed purple-gray) |
| `--sd-text-muted` | `#6b5f82` | Muted text (low emphasis) |

**Usage:**
```css
h1 {
  color: var(--sd-text-primary);
}

p {
  color: var(--sd-text-secondary);
}

.caption {
  color: var(--sd-text-muted);
  font-size: var(--sd-font-sm);
}
```

---

### Glass Effects

**Purpose:** Frosted glass/blur effects for modals and overlays

| Token | Value | Description |
|-------|-------|-------------|
| `--sd-glass-bg` | `rgba(26,20,40,0.85)` | Semi-transparent glass background |
| `--sd-glass-bg-heavy` | `rgba(18,14,32,0.95)` | More opaque glass background |
| `--sd-glass-blur` | `blur(12px)` | Backdrop blur amount |

**Usage:**
```css
.modal {
  background: var(--sd-glass-bg);
  backdrop-filter: var(--sd-glass-blur);
  border: 1px solid var(--sd-border);
}
```

---

### Accent & Glow

**Purpose:** Primary accent and glow effects

| Token | Value | Description |
|-------|-------|-------------|
| `--sd-accent` | `#8b5cf6` | Primary accent (same as purple) |
| `--sd-accent-glow` | `rgba(139,92,246,0.4)` | Glow effect around accent elements |

**Usage:**
```css
button.primary {
  background: var(--sd-accent);
  box-shadow: 0 0 20px var(--sd-accent-glow);
}
```

---

### Extended Color Variants

**Purpose:** Additional color shades for specific use cases

| Token | Value | Description |
|-------|-------|-------------|
| `--sd-purple-light` | `#c084fc` | Lighter purple variant |
| `--sd-purple-hover` | `#7c4ee4` | Purple on hover state |
| `--sd-purple-deep` | `#7c3aed` | Deeper purple shade |
| `--sd-purple-dimmer` | `rgba(139, 92, 246, 0.12)` | Very subtle purple background |
| `--sd-purple-dimmest` | `rgba(139, 92, 246, 0.08)` | Extremely subtle purple tint |
| `--sd-green-dark` | `#16a34a` | Darker green variant |
| `--sd-green-dimmer` | `rgba(34, 197, 94, 0.15)` | Subtle green background |
| `--sd-green-dimmest` | `rgba(34, 197, 94, 0.1)` | Very subtle green tint |
| `--sd-orange-bright` | `#fbbf24` | Brighter orange variant |
| `--sd-orange-dimmer` | `rgba(245, 158, 11, 0.2)` | Subtle orange background |
| `--sd-cyan-dimmer` | `rgba(6, 182, 212, 0.2)` | Subtle cyan background |
| `--sd-cyan-dimmest` | `rgba(6, 182, 212, 0.08)` | Very subtle cyan tint |
| `--sd-cyan-border` | `rgba(6, 182, 212, 0.3)` | Cyan border color |
| `--sd-red-dimmer` | `rgba(239, 68, 68, 0.15)` | Subtle red background |
| `--sd-blue` | `#3b82f6` | Blue accent (for canvas nodes) |
| `--sd-blue-dimmest` | `rgba(59, 130, 246, 0.08)` | Very subtle blue tint |
| `--sd-blue-dimmer` | `rgba(59, 130, 246, 0.2)` | Subtle blue background |

---

## Typography

**Purpose:** Font families and sizes

| Token | Value | Description |
|-------|-------|-------------|
| `--sd-font-sans` | `'DM Sans', system-ui, sans-serif` | Sans-serif font stack |
| `--sd-font-mono` | `'JetBrains Mono', 'Fira Code', monospace` | Monospace font stack (for code) |
| `--sd-font-xs` | `10px` | Extra small text |
| `--sd-font-sm` | `11px` | Small text |
| `--sd-font-base` | `12px` | Base text size |
| `--sd-font-md` | `13px` | Medium text |
| `--sd-font-lg` | `16px` | Large text |

**Usage:**
```css
body {
  font-family: var(--sd-font-sans);
  font-size: var(--sd-font-base);
}

code {
  font-family: var(--sd-font-mono);
  font-size: var(--sd-font-sm);
}

h1 {
  font-size: var(--sd-font-lg);
  font-weight: 600;
}
```

---

## Shadow System

**Purpose:** Elevation and depth via box-shadows

| Token | Value | Description |
|-------|-------|-------------|
| `--sd-shadow-sm` | `0 2px 8px rgba(0, 0, 0, 0.3)` | Small shadow (subtle elevation) |
| `--sd-shadow-md` | `0 4px 16px rgba(0, 0, 0, 0.3)` | Medium shadow (moderate elevation) |
| `--sd-shadow-lg` | `0 8px 24px rgba(0, 0, 0, 0.3)` | Large shadow (high elevation) |
| `--sd-shadow-xl` | `0 8px 32px rgba(0, 0, 0, 0.4)` | Extra large shadow (very high elevation) |
| `--sd-shadow-2xl` | `0 24px 64px rgba(0, 0, 0, 0.6)` | Massive shadow (floating modals) |

**Usage:**
```css
.card {
  box-shadow: var(--sd-shadow-md);
}

.modal {
  box-shadow: var(--sd-shadow-2xl);
}
```

---

## Gradients

**Purpose:** Linear gradients for buttons and highlights

| Token | Value | Description |
|-------|-------|-------------|
| `--sd-gradient-purple` | `linear-gradient(135deg, var(--sd-purple), var(--sd-purple-deep))` | Purple gradient |
| `--sd-gradient-green` | `linear-gradient(135deg, var(--sd-green), var(--sd-green-dark))` | Green gradient |
| `--sd-gradient-orange` | `linear-gradient(135deg, var(--sd-orange), var(--sd-orange-bright))` | Orange gradient |

**Usage:**
```css
button.primary {
  background: var(--sd-gradient-purple);
}

.success-indicator {
  background: var(--sd-gradient-green);
}
```

---

## Glow Effects

**Purpose:** Box-shadow glows for interactive elements

| Token | Value | Description |
|-------|-------|-------------|
| `--sd-purple-glow` | `0 0 20px rgba(139, 92, 246, 0.3)` | Purple glow |
| `--sd-green-glow` | `0 0 20px rgba(34, 197, 94, 0.3)` | Green glow |
| `--sd-orange-glow` | `0 0 20px rgba(245, 158, 11, 0.3)` | Orange glow |
| `--sd-cyan-glow` | `0 0 20px rgba(6, 182, 212, 0.3)` | Cyan glow |

**Usage:**
```css
button:hover {
  box-shadow: var(--sd-purple-glow);
}
```

---

## Kanban Column Colors

**Purpose:** Color coding for kanban board columns

| Token | Value | Description |
|-------|-------|-------------|
| `--sd-col-icebox` | `#6b7a8d` | Icebox column (gray-blue) |
| `--sd-col-backlog` | `#e89b3f` | Backlog column (orange) |
| `--sd-col-in-progress` | `#4a90d9` | In Progress column (blue) |
| `--sd-col-review` | `#a07cdc` | Review column (purple) |
| `--sd-col-done` | `#3fb8a9` | Done column (teal) |

**Usage:**
```css
.kanban-column[data-status="in-progress"] {
  border-top: 3px solid var(--sd-col-in-progress);
}
```

---

## Priority Colors

**Purpose:** Color coding for task priorities (P0-P3)

| Token | Value | Description |
|-------|-------|-------------|
| `--sd-pri-p0` | `var(--sd-red)` | P0 (critical) — red |
| `--sd-pri-p1` | `var(--sd-orange)` | P1 (high) — orange |
| `--sd-pri-p2` | `var(--sd-cyan)` | P2 (medium) — cyan |
| `--sd-pri-p3` | `var(--sd-text-muted)` | P3 (low) — muted gray |
| `--sd-pri-p0-bg` | `#2b1225` | P0 background (dark red) |
| `--sd-pri-p1-bg` | `#2b2011` | P1 background (dark orange) |
| `--sd-pri-p2-bg` | `#11192b` | P2 background (dark blue) |
| `--sd-pri-p3-bg` | `#1a1e2b` | P3 background (dark gray) |

**Usage:**
```css
.task[data-priority="p0"] {
  background: var(--sd-pri-p0-bg);
  border-left: 3px solid var(--sd-pri-p0);
}
```

---

## Dev Cycle Stage Colors

**Purpose:** Color coding for development stages (spec, IR, validation, build, test)

| Token | Value | Description |
|-------|-------|-------------|
| `--sd-stage-spec` | `#4a90d9` | Specification stage (blue) |
| `--sd-stage-ir` | `#a07cdc` | Intermediate representation stage (purple) |
| `--sd-stage-val` | `#e89b3f` | Validation stage (orange) |
| `--sd-stage-build` | `#3fb8a9` | Build stage (teal) |
| `--sd-stage-test` | `#22c55e` | Test stage (green) |

**Usage:**
```css
.stage-indicator[data-stage="build"] {
  background: var(--sd-stage-build);
}
```

---

## Mode Colors

**Purpose:** Color coding for simulation modes

| Token | Value | Description |
|-------|-------|-------------|
| `--mode-design` | `#8b5cf6` | Design mode (purple) |
| `--mode-production` | `#22c55e` | Production mode (green) |
| `--mode-simulate` | `#3b82f6` | Simulate mode (blue) |
| `--mode-playback` | `#06b6d4` | Playback mode (cyan) |
| `--mode-tabletop` | `#f59e0b` | Tabletop mode (orange) |
| `--mode-compare` | `#eab308` | Compare mode (yellow) |
| `--mode-optimize` | `#ef4444` | Optimize mode (red) |

Each mode also has a `-dim` variant (e.g., `--mode-design-dim: #a78bfa`) for dimmed backgrounds.

**Usage:**
```css
.mode-badge[data-mode="production"] {
  background: var(--mode-production-dim);
  color: var(--mode-production);
}
```

---

## Overlay System

**Purpose:** Dark overlays for modals and dialogs

| Token | Value | Description |
|-------|-------|-------------|
| `--sd-overlay` | `rgba(0, 0, 0, 0.5)` | Default overlay (50% black) |
| `--sd-overlay-heavy` | `rgba(0, 0, 0, 0.6)` | Heavier overlay (60% black) |
| `--sd-overlay-bg` | `rgba(0,0,0,0.7)` | Modal overlay background |
| `--sd-spotlight-backdrop` | `rgba(0,0,0,0.75)` | Spotlight mode backdrop |
| `--sd-spotlight-shadow` | `0 16px 64px rgba(0,0,0,0.8)` | Spotlight mode shadow |

**Usage:**
```css
.modal-backdrop {
  background: var(--sd-overlay);
}
```

---

## Helper Tokens

**Purpose:** Miscellaneous UI helpers

| Token | Value | Description |
|-------|-------|-------------|
| `--sd-float-shadow` | `0 8px 32px rgba(0,0,0,0.4)` | Shadow for floating elements |
| `--sd-grid-dot` | `rgba(139, 92, 246, 0.35)` | Color for canvas grid dots |
| `--sd-bg-secondary` | `rgba(20, 16, 32, 0.8)` | Secondary background |
| `--sd-bg-hover` | `rgba(139, 92, 246, 0.08)` | Hover background tint |
| `--sd-bg-subtle` | `rgba(139, 92, 246, 0.05)` | Very subtle background tint |
| `--sd-accent-subtle` | `rgba(139, 92, 246, 0.1)` | Subtle accent background |
| `--sd-text-on-accent` | `#ffffff` | Text color on accent backgrounds |

---

## Usage Patterns

**Button:** `background: var(--sd-accent)`, `color: var(--sd-text-on-accent)`, `box-shadow: var(--sd-shadow-sm)`, hover adds `var(--sd-purple-glow)`

**Card:** `background: var(--sd-surface)`, `border: var(--sd-border)`, `box-shadow: var(--sd-shadow-md)`, hover uses `var(--sd-surface-hover)`

**Modal:** Backdrop uses `var(--sd-overlay)` + `backdrop-filter: var(--sd-glass-blur)`, content uses `var(--sd-glass-bg-heavy)` + `var(--sd-shadow-2xl)`

---

## Next Steps

- **Explore theme variants:** See [design-tokens-themes.md](design-tokens-themes.md) for depth, light, monochrome, and high-contrast themes
- **Read the source:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css`

---

**Version:** 1.0.0
**Last Updated:** 2026-03-17
**Source:** `shell-themes.css` (lines 26-183)
