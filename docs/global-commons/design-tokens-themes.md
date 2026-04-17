# Design Tokens — Theme Variants

**Source:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css`
**Last Updated:** 2026-03-17

---

## Overview

DEIA supports **five themes** via CSS custom properties. Themes are applied by setting the `data-theme` attribute on the `.hhp-root` element:

```html
<div class="hhp-root" data-theme="depth">
  <!-- App content -->
</div>
```

**Available themes:**
1. **Default** (no `data-theme` attribute) — Full-color dark purple
2. **Depth** (`data-theme="depth"`) — Deeper blacks, more saturated accents
3. **Light** (`data-theme="light"`) — Light mode with inverted colors
4. **Monochrome** (`data-theme="monochrome"`) — Grayscale (no color)
5. **High Contrast** (`data-theme="high-contrast"`) — Maximum contrast for accessibility

This document describes how each theme modifies the design tokens from the default theme (see [design-tokens.md](design-tokens.md)).

---

## How Themes Work

Themes **override** specific CSS variables while leaving others unchanged. For example:

```css
/* Default theme */
.hhp-root {
  --sd-bg: #0e0a1a;
  --sd-purple: #8b5cf6;
}

/* Depth theme override */
.hhp-root[data-theme="depth"] {
  --sd-bg: #060410;  /* Darker */
  --sd-purple: #a78bfa;  /* More saturated */
}
```

**Result:** When `data-theme="depth"` is applied, the background becomes darker and the purple becomes more saturated. All other tokens (shadows, typography, etc.) remain unchanged unless explicitly overridden.

---

## Theme Comparison Table

**Key differences at a glance:**

| Token | Default | Depth | Light | Monochrome | High Contrast |
|-------|---------|-------|-------|------------|---------------|
| **Background** | `#0e0a1a` (dark purple) | `#060410` (deeper black) | `#f4f2fa` (light lavender) | `#0a0a0a` (pure black) | `#000000` (absolute black) |
| **Primary Accent** | `#8b5cf6` (purple) | `#a78bfa` (saturated purple) | `#6d48d8` (darker purple) | `#cccccc` (light gray) | `#ffff00` (yellow) |
| **Success Color** | `#22c55e` (green) | `#22c55e` (green) | `#16a34a` (darker green) | `#aaaaaa` (gray) | `#00ff88` (bright green) |
| **Warning Color** | `#f59e0b` (orange) | `#f59e0b` (orange) | `#d97706` (darker orange) | `#999999` (gray) | `#ff8800` (bright orange) |
| **Error Color** | `#ef4444` (red) | `#ef4444` (red) | `#dc2626` (darker red) | `#888888` (gray) | `#ff4444` (bright red) |
| **Border** | `rgba(139,92,246,0.35)` (purple tint) | `rgba(139,92,246,0.45)` (more opaque) | `rgba(109,72,216,0.25)` (subtle) | `rgba(200,200,200,0.2)` (gray) | `rgba(255,255,0,0.6)` (yellow) |
| **Text Primary** | `#f0edf6` (near-white) | `#f5f0ff` (whiter) | `#1a1033` (near-black) | `#f0f0f0` (light gray) | `#ffffff` (pure white) |
| **Shadow Intensity** | Medium | Medium | Light | Medium | Heavy |

---

## Depth Theme

**Purpose:** Deeper blacks, more saturated accent colors, enhanced contrast

**Use case:** Users who prefer maximum visual depth and immersion. Good for OLED screens where deep blacks look stunning.

### Key Overrides

| Token | Default Value | Depth Value | Change |
|-------|--------------|-------------|--------|
| `--sd-bg` | `#0e0a1a` | `#060410` | **Darker** background (deeper black) |
| `--sd-surface` | `#1a1428` | `#0e0a1c` | Darker surface |
| `--sd-surface-alt` | `#0f0b1a` | `#080614` | Darker alt surface |
| `--sd-purple` | `#8b5cf6` | `#a78bfa` | **More saturated** purple |
| `--sd-accent` | `#8b5cf6` | `#a78bfa` | More saturated accent |
| `--sd-text-primary` | `#f0edf6` | `#f5f0ff` | **Whiter** text |
| `--sd-border` | `rgba(139,92,246,0.35)` | `rgba(139,92,246,0.45)` | **More opaque** border |
| `--sd-glass-bg` | `rgba(26,20,40,0.85)` | `rgba(14,10,28,0.90)` | More opaque glass |

**Visual effect:**
- **Deeper blacks** create more "pop" for UI elements
- **More saturated purples** make accents stand out
- **Whiter text** improves readability on darker backgrounds

**Example:**

```css
/* Depth theme card */
<div class="hhp-root" data-theme="depth">
  <div class="card">
    <!-- Background: #0e0a1c (much darker than default) -->
    <!-- Border: rgba(139,92,246,0.45) (more visible than default) -->
  </div>
</div>
```

---

## Light Theme

**Purpose:** Inverted color scheme for bright environments

**Use case:** Daytime use, outdoor settings, users who prefer light mode, accessibility requirements.

### Key Overrides

| Token | Default Value | Light Value | Change |
|-------|--------------|-------------|--------|
| `--sd-bg` | `#0e0a1a` (dark) | `#f4f2fa` (light lavender) | **Inverted** to light |
| `--sd-surface` | `#1a1428` (dark) | `#ffffff` (white) | **Pure white** surface |
| `--sd-surface-alt` | `#0f0b1a` (dark) | `#f0edf8` (light lavender) | Light alt surface |
| `--sd-purple` | `#8b5cf6` | `#6d48d8` | **Darker** purple (for contrast on light bg) |
| `--sd-green` | `#22c55e` | `#16a34a` | Darker green |
| `--sd-orange` | `#f59e0b` | `#d97706` | Darker orange |
| `--sd-red` | `#ef4444` | `#dc2626` | Darker red |
| `--sd-text-primary` | `#f0edf6` (light) | `#1a1033` (dark purple-black) | **Inverted** to dark |
| `--sd-text-secondary` | `#9a8fb5` (mid-gray) | `#4a3f6b` (dark gray) | Darker secondary text |
| `--sd-border` | `rgba(139,92,246,0.35)` | `rgba(109,72,216,0.25)` | **Subtler** border |
| `--sd-shadow-sm` | `0 2px 8px rgba(0,0,0,0.3)` | `0 2px 8px rgba(26,20,40,0.08)` | **Lighter** shadow |

**Visual effect:**
- **White backgrounds** reduce eye strain in bright environments
- **Dark text** provides high contrast on light backgrounds
- **Lighter shadows** create subtle depth without overwhelming the UI

**Example:**

```css
/* Light theme button */
<div class="hhp-root" data-theme="light">
  <button class="primary">
    <!-- Background: #6d48d8 (darker purple for contrast) -->
    <!-- Text: #ffffff (white text on dark button) -->
  </button>
</div>
```

---

## Monochrome Theme

**Purpose:** Grayscale palette with no color (for accessibility or preference)

**Use case:** Users with color blindness, users who prefer minimal visual distractions, low-bandwidth displays.

### Key Overrides

| Token | Default Value | Monochrome Value | Change |
|-------|--------------|------------------|--------|
| `--sd-bg` | `#0e0a1a` (purple-black) | `#0a0a0a` (pure black) | **No color** |
| `--sd-surface` | `#1a1428` (purple) | `#141414` (dark gray) | No color |
| `--sd-purple` | `#8b5cf6` (purple) | `#cccccc` (light gray) | **Grayscale** |
| `--sd-green` | `#22c55e` (green) | `#aaaaaa` (mid-gray) | Grayscale |
| `--sd-orange` | `#f59e0b` (orange) | `#999999` (gray) | Grayscale |
| `--sd-red` | `#ef4444` (red) | `#888888` (dark gray) | Grayscale |
| `--sd-cyan` | `#06b6d4` (cyan) | `#bbbbbb` (light gray) | Grayscale |
| `--sd-text-primary` | `#f0edf6` | `#f0f0f0` (light gray) | No color |
| `--sd-border` | `rgba(139,92,246,0.35)` | `rgba(200,200,200,0.2)` | **Gray border** |

**Visual effect:**
- **All colors removed** (only shades of gray)
- **Visual hierarchy maintained** via brightness differences
- **No semantic color coding** (no red = error, green = success)

**Example:**

```css
/* Monochrome theme status badge */
<div class="hhp-root" data-theme="monochrome">
  <span class="status-badge success">
    <!-- Background: rgba(200,200,200,0.1) (light gray) -->
    <!-- Color: #aaaaaa (mid-gray) -->
    <!-- No green — relies on text/icon to convey "success" -->
  </span>
</div>
```

**Accessibility note:**
Monochrome theme **removes color-based information**. Ensure your UI conveys meaning via:
- Text labels ("Success", "Error", "Warning")
- Icons (✓ checkmark, ✗ cross, ⚠ warning triangle)
- Position/layout (errors at top, success at bottom)

---

## High Contrast Theme

**Purpose:** Maximum contrast for accessibility (WCAG AAA compliance)

**Use case:** Users with low vision, screen readers, accessibility requirements, testing for WCAG compliance.

### Key Overrides

| Token | Default Value | High Contrast Value | Change |
|-------|--------------|---------------------|--------|
| `--sd-bg` | `#0e0a1a` | `#000000` (absolute black) | **Maximum contrast** |
| `--sd-surface` | `#1a1428` | `#0a0a0a` (near-black) | Very dark |
| `--sd-purple` | `#8b5cf6` | `#ffff00` (bright yellow) | **High visibility** |
| `--sd-green` | `#22c55e` | `#00ff88` (bright green) | Maximum visibility |
| `--sd-orange` | `#f59e0b` | `#ff8800` (bright orange) | Maximum visibility |
| `--sd-red` | `#ef4444` | `#ff4444` (bright red) | Maximum visibility |
| `--sd-cyan` | `#06b6d4` | `#00ffff` (bright cyan) | Maximum visibility |
| `--sd-text-primary` | `#f0edf6` | `#ffffff` (pure white) | **Maximum contrast** |
| `--sd-border` | `rgba(139,92,246,0.35)` | `rgba(255,255,0,0.6)` | **Bright yellow border** |
| `--sd-border-focus` | `rgba(139,92,246,0.6)` | `#ffff00` (solid yellow) | Maximum focus visibility |
| `--sd-shadow-sm` | `0 2px 8px rgba(0,0,0,0.3)` | `0 2px 8px rgba(0,0,0,0.5)` | **Heavier shadows** |

**Visual effect:**
- **Absolute black backgrounds** (#000000)
- **Pure white text** (#ffffff)
- **Bright, saturated colors** (yellow, cyan, bright green)
- **Heavy borders and shadows** for maximum element separation

**Example:**

```css
/* High contrast theme button */
<div class="hhp-root" data-theme="high-contrast">
  <button class="primary" tabindex="0">
    <!-- Background: #ffff00 (bright yellow) -->
    <!-- Text: #000000 (black text on yellow button) -->
    <!-- Focus border: solid #ffff00 (very visible) -->
  </button>
</div>
```

**Accessibility note:**
High contrast theme meets **WCAG AAA** contrast ratios (7:1 minimum). All interactive elements have:
- Clear focus states (bright yellow outline)
- High color contrast (white text on black, black text on yellow)
- Heavy borders for element separation

---

## Theme Switching

### Programmatic Switching

```typescript
// Get root element
const root = document.querySelector('.hhp-root');

// Switch to depth theme
root.setAttribute('data-theme', 'depth');

// Switch to light theme
root.setAttribute('data-theme', 'light');

// Switch back to default theme
root.removeAttribute('data-theme');
```

### User Preference Detection

```typescript
// Detect system theme preference
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
const prefersHighContrast = window.matchMedia('(prefers-contrast: high)').matches;

// Apply theme based on system preference
if (prefersHighContrast) {
  root.setAttribute('data-theme', 'high-contrast');
} else if (prefersDark) {
  root.setAttribute('data-theme', 'depth');
} else {
  root.setAttribute('data-theme', 'light');
}
```

### Theme Persistence

```typescript
// Save theme to localStorage
function setTheme(theme: string) {
  root.setAttribute('data-theme', theme);
  localStorage.setItem('sd_user_theme', theme);
}

// Load theme from localStorage on page load
const savedTheme = localStorage.getItem('sd_user_theme');
if (savedTheme) {
  root.setAttribute('data-theme', savedTheme);
}
```

---

## Theme-Specific Adjustments

Some components may need **per-theme adjustments** beyond variable overrides:

### Example: Canvas Grid Dots

```css
/* Default theme: purple grid dots */
.hhp-root {
  --sd-grid-dot: rgba(139, 92, 246, 0.35);
}

/* Depth theme: dimmer purple dots */
.hhp-root[data-theme="depth"] {
  --sd-grid-dot: rgba(180, 155, 110, 0.25);
}

/* Light theme: subtle purple dots */
.hhp-root[data-theme="light"] {
  --sd-grid-dot: rgba(139, 92, 246, 0.35);
}

/* Monochrome theme: gray dots */
.hhp-root[data-theme="monochrome"] {
  --sd-grid-dot: rgba(192, 192, 192, 0.35);
}

/* High contrast theme: bright dots */
.hhp-root[data-theme="high-contrast"] {
  --sd-grid-dot: rgba(167, 139, 250, 0.35);
}
```

### Example: Mode Colors

Mode colors (design, production, simulate, etc.) also change per theme:

**Default theme:** Full color (purple = design, green = production, blue = simulate)

**Depth theme:** Uses alternate accent colors (gold/amber for design mode instead of purple)

**Monochrome theme:** All modes are shades of gray (design = light gray, production = mid-gray, etc.)

**High contrast theme:** Bright, saturated mode colors (bright purple, bright yellow, bright cyan)

---

## Best Practices

### 1. Always Use Variables

**Bad:**
```css
.button {
  background: #8b5cf6;  /* Hardcoded purple */
}
```

**Good:**
```css
.button {
  background: var(--sd-purple);  /* Uses theme variable */
}
```

**Why:** Hardcoded values don't update when themes change. Always use CSS variables.

---

### 2. Test All Themes

Before shipping a component, verify it looks correct in **all five themes**. Common issues:

- Text becomes unreadable in light theme (dark text on dark background)
- Borders disappear in monochrome theme (relied on color for visibility)
- Focus states are invisible in high contrast theme (insufficient contrast)

**Testing checklist:**
- ✅ Default theme
- ✅ Depth theme (check darker backgrounds)
- ✅ Light theme (check inverted colors)
- ✅ Monochrome theme (check no-color fallbacks)
- ✅ High contrast theme (check accessibility)

---

### 3. Don't Rely on Color Alone

**Bad:**
```html
<span style="color: var(--sd-green);">Success</span>
<span style="color: var(--sd-red);">Error</span>
```

In monochrome theme, both will be shades of gray — indistinguishable.

**Good:**
```html
<span class="status-success">✓ Success</span>
<span class="status-error">✗ Error</span>
```

Include **text or icons** to convey meaning, not just color.

---

### 4. Use Semantic Tokens

**Bad:**
```css
.error-message {
  color: #ef4444;  /* Hardcoded red */
}
```

**Good:**
```css
.error-message {
  color: var(--sd-red);  /* Semantic token */
}
```

**Why:** Semantic tokens (like `--sd-red` for errors) adapt across themes. Hardcoded values don't.

---

## Next Steps

- **Review default theme:** See [design-tokens.md](design-tokens.md) for full token documentation
- **Read the source:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css`
- **Test themes:** Try switching themes in the browser devtools by setting `data-theme` attribute

---

**Version:** 1.0.0
**Last Updated:** 2026-03-17
**Source:** `shell-themes.css` (lines 185-686)
