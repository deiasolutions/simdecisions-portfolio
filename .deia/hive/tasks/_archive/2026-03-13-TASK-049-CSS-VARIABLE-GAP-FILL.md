# TASK-049: CSS Variable Gap Fill

**Date:** 2026-03-13
**Bee Model:** Sonnet
**From:** Q33N
**Parent Briefing:** `.deia/hive/coordination/2026-03-13-BRIEFING-THEME-SWITCHING.md`
**Depends On:** TASK-048 (needs body bg fix in shell-themes.css first)
**Blocks:** None

---

## Objective

Port ~51 missing CSS variables per theme from platform source files to shiftcenter. ShiftCenter's themes currently define ~24 variables each. Platform defines ~90 per theme. Fill the gap to achieve full platform parity.

---

## Current State

| Theme | Current Variables | Target Variables | Gap |
|-------|------------------|------------------|-----|
| full-color (default) | ~24 | ~90 | ~66 |
| depth | ~24 | ~70 | ~46 |
| light | ~24 | ~85 | ~61 |
| monochrome | ~24 | ~85 | ~61 |
| high-contrast | ~24 | ~85 | ~61 |

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css`

**Existing selectors:**
- `.hhp-root` (lines 26-68) — default theme (full-color)
- `.hhp-root[data-theme="depth"]` (lines 70-84)
- `.hhp-root[data-theme="light"]` (lines 86-110)
- `.hhp-root[data-theme="monochrome"]` (lines 112-136)
- `.hhp-root[data-theme="high-contrast"]` (lines 138-160)

---

## Missing Variable Categories

| Category | Variables | Count |
|----------|-----------|-------|
| Extended color variants | `--sd-purple-light`, `--sd-purple-hover`, `--sd-purple-deep`, `--sd-purple-dimmer`, `--sd-purple-dimmest`, `--sd-green-dark`, `--sd-green-dimmer`, `--sd-green-dimmest`, `--sd-orange-bright`, `--sd-orange-dimmer`, `--sd-cyan-dimmer`, `--sd-cyan-dimmest`, `--sd-cyan-border`, `--sd-red-dimmer` | 14 |
| Shadow system | `--sd-shadow-sm`, `--sd-shadow-md`, `--sd-shadow-lg`, `--sd-shadow-xl`, `--sd-shadow-2xl` | 5 |
| Gradients | `--sd-gradient-purple`, `--sd-gradient-green`, `--sd-gradient-orange` | 3 |
| Glow effects | `--sd-purple-glow`, `--sd-green-glow`, `--sd-orange-glow`, `--sd-cyan-glow` | 4 |
| Glass variants | `--sd-glass-bg-light`, `--sd-glass-bg-dark` | 2 |
| Overlay system | `--sd-overlay`, `--sd-overlay-heavy` | 2 |
| Text variants | `--sd-text-secondary-light`, `--sd-text-on-accent` | 2 |
| Dialog/UI helpers | `--sd-bg-secondary`, `--sd-bg-hover`, `--sd-bg-subtle`, `--sd-accent-subtle` | 4 |
| Grid dot | `--sd-grid-dot` | 1 |
| Mode colors | `--mode-design`, `--mode-production`, `--mode-simulate`, `--mode-playback`, `--mode-tabletop`, `--mode-compare`, `--mode-optimize`, `--mode-design-dim`, `--mode-production-dim`, `--mode-simulate-dim`, `--mode-playback-dim`, `--mode-tabletop-dim`, `--mode-compare-dim`, `--mode-optimize-dim` | 14 |
| **Total per theme** | | **~51** |

---

## Platform Source Files

| Theme | Platform Source File | Selector |
|-------|---------------------|----------|
| full-color | `platform/simdecisions-2/src/index.css` | `:root` |
| depth | `platform/simdecisions-2/src/themes/depth.css` | `html[data-theme="depth"]` |
| light | `platform/simdecisions-2/src/styles/themes.css` | `html[data-theme="light"]` (lines 33-139) |
| monochrome | `platform/simdecisions-2/src/styles/themes.css` | `html[data-theme="monochrome"]` (lines 143-245) |
| high-contrast | `platform/simdecisions-2/src/styles/themes.css` | `html[data-theme="high-contrast"]` (lines 249-352) |

**Note:** Platform uses `html[data-theme="..."]` selectors. ShiftCenter uses `.hhp-root[data-theme="..."]` selectors. Keep the shiftcenter convention.

---

## Implementation Steps (TDD)

### Step 1: Read platform source files

**Action:** Read the 5 platform source files to extract exact CSS variable values.

**Files to read:**
1. `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\index.css` (`:root` selector)
2. `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\themes\depth.css` (entire file)
3. `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\styles\themes.css` (lines 33-352)

**Extract:**
- All variables under each category (shadow, gradient, glow, glass, overlay, text, mode colors, etc.)
- Exact rgba/hex values for each theme

---

### Step 2: Write tests for CSS variable presence

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\shell-themes.test.ts` (NEW)

**Action:** CREATE test suite

Test approach: Parse shell-themes.css and verify presence of expected variables.

**Test cases (minimum 5):**

1. **Default theme defines all expected CSS variable categories**
   - Parse `.hhp-root` selector
   - Assert presence of variables from each category:
     - Extended colors: `--sd-purple-light`, `--sd-green-dark`, etc.
     - Shadows: `--sd-shadow-sm` through `--sd-shadow-2xl`
     - Gradients: `--sd-gradient-purple`, `--sd-gradient-green`, `--sd-gradient-orange`
     - Glows: `--sd-purple-glow`, `--sd-green-glow`, `--sd-orange-glow`, `--sd-cyan-glow`
     - Glass: `--sd-glass-bg-light`, `--sd-glass-bg-dark`
     - Overlays: `--sd-overlay`, `--sd-overlay-heavy`
     - Text: `--sd-text-secondary-light`, `--sd-text-on-accent`
     - Dialog/UI: `--sd-bg-secondary`, `--sd-bg-hover`, `--sd-bg-subtle`, `--sd-accent-subtle`
     - Grid: `--sd-grid-dot`
     - Modes: `--mode-design` through `--mode-optimize-dim` (14 vars)

2. **Each theme override defines shadow variables**
   - For each theme (depth, light, monochrome, high-contrast):
     - Assert presence of `--sd-shadow-sm`, `--sd-shadow-md`, `--sd-shadow-lg`, `--sd-shadow-xl`, `--sd-shadow-2xl`

3. **Each theme override defines gradient variables**
   - For each theme:
     - Assert presence of `--sd-gradient-purple`, `--sd-gradient-green`, `--sd-gradient-orange`

4. **Each theme override defines mode color variables**
   - For each theme:
     - Assert presence of all 14 mode variables

5. **No hardcoded hex in new variable values (regex scan)**
   - Read shell-themes.css
   - Find all new variables added (compare against known existing vars)
   - Assert new vars use rgba() or reference other vars, not hex

**Test implementation approach:**

```typescript
import { readFileSync } from 'fs';
import { resolve } from 'path';

describe('shell-themes.css', () => {
  const cssPath = resolve(__dirname, '../shell-themes.css');
  const cssContent = readFileSync(cssPath, 'utf-8');

  const parseSelector = (selector: string): Map<string, string> => {
    const regex = new RegExp(`${selector}\\s*\\{([^}]+)\\}`, 's');
    const match = cssContent.match(regex);
    if (!match) return new Map();

    const vars = new Map<string, string>();
    const varRegex = /--([\w-]+):\s*([^;]+);/g;
    let varMatch;
    while ((varMatch = varRegex.exec(match[1])) !== null) {
      vars.set(`--${varMatch[1]}`, varMatch[2].trim());
    }
    return vars;
  };

  describe('default theme (full-color)', () => {
    const vars = parseSelector('.hhp-root');

    it('defines extended color variants', () => {
      expect(vars.has('--sd-purple-light')).toBe(true);
      expect(vars.has('--sd-purple-hover')).toBe(true);
      expect(vars.has('--sd-purple-deep')).toBe(true);
      expect(vars.has('--sd-purple-dimmer')).toBe(true);
      expect(vars.has('--sd-purple-dimmest')).toBe(true);
      expect(vars.has('--sd-green-dark')).toBe(true);
      expect(vars.has('--sd-green-dimmer')).toBe(true);
      expect(vars.has('--sd-green-dimmest')).toBe(true);
      expect(vars.has('--sd-orange-bright')).toBe(true);
      expect(vars.has('--sd-orange-dimmer')).toBe(true);
      expect(vars.has('--sd-cyan-dimmer')).toBe(true);
      expect(vars.has('--sd-cyan-dimmest')).toBe(true);
      expect(vars.has('--sd-cyan-border')).toBe(true);
      expect(vars.has('--sd-red-dimmer')).toBe(true);
    });

    it('defines shadow system', () => {
      expect(vars.has('--sd-shadow-sm')).toBe(true);
      expect(vars.has('--sd-shadow-md')).toBe(true);
      expect(vars.has('--sd-shadow-lg')).toBe(true);
      expect(vars.has('--sd-shadow-xl')).toBe(true);
      expect(vars.has('--sd-shadow-2xl')).toBe(true);
    });

    it('defines gradients', () => {
      expect(vars.has('--sd-gradient-purple')).toBe(true);
      expect(vars.has('--sd-gradient-green')).toBe(true);
      expect(vars.has('--sd-gradient-orange')).toBe(true);
    });

    it('defines glow effects', () => {
      expect(vars.has('--sd-purple-glow')).toBe(true);
      expect(vars.has('--sd-green-glow')).toBe(true);
      expect(vars.has('--sd-orange-glow')).toBe(true);
      expect(vars.has('--sd-cyan-glow')).toBe(true);
    });

    it('defines glass variants', () => {
      expect(vars.has('--sd-glass-bg-light')).toBe(true);
      expect(vars.has('--sd-glass-bg-dark')).toBe(true);
    });

    it('defines overlay system', () => {
      expect(vars.has('--sd-overlay')).toBe(true);
      expect(vars.has('--sd-overlay-heavy')).toBe(true);
    });

    it('defines text variants', () => {
      expect(vars.has('--sd-text-secondary-light')).toBe(true);
      expect(vars.has('--sd-text-on-accent')).toBe(true);
    });

    it('defines dialog/UI helpers', () => {
      expect(vars.has('--sd-bg-secondary')).toBe(true);
      expect(vars.has('--sd-bg-hover')).toBe(true);
      expect(vars.has('--sd-bg-subtle')).toBe(true);
      expect(vars.has('--sd-accent-subtle')).toBe(true);
    });

    it('defines grid dot', () => {
      expect(vars.has('--sd-grid-dot')).toBe(true);
    });

    it('defines mode colors', () => {
      const modeVars = [
        '--mode-design', '--mode-production', '--mode-simulate', '--mode-playback',
        '--mode-tabletop', '--mode-compare', '--mode-optimize',
        '--mode-design-dim', '--mode-production-dim', '--mode-simulate-dim',
        '--mode-playback-dim', '--mode-tabletop-dim', '--mode-compare-dim', '--mode-optimize-dim'
      ];
      modeVars.forEach(v => expect(vars.has(v)).toBe(true));
    });
  });

  const themes = ['depth', 'light', 'monochrome', 'high-contrast'];

  themes.forEach(theme => {
    describe(`${theme} theme`, () => {
      const vars = parseSelector(`.hhp-root\\[data-theme="${theme}"\\]`);

      it('defines shadow system', () => {
        expect(vars.has('--sd-shadow-sm')).toBe(true);
        expect(vars.has('--sd-shadow-md')).toBe(true);
        expect(vars.has('--sd-shadow-lg')).toBe(true);
        expect(vars.has('--sd-shadow-xl')).toBe(true);
        expect(vars.has('--sd-shadow-2xl')).toBe(true);
      });

      it('defines gradients', () => {
        expect(vars.has('--sd-gradient-purple')).toBe(true);
        expect(vars.has('--sd-gradient-green')).toBe(true);
        expect(vars.has('--sd-gradient-orange')).toBe(true);
      });

      it('defines mode colors', () => {
        const modeVars = [
          '--mode-design', '--mode-production', '--mode-simulate', '--mode-playback',
          '--mode-tabletop', '--mode-compare', '--mode-optimize',
          '--mode-design-dim', '--mode-production-dim', '--mode-simulate-dim',
          '--mode-playback-dim', '--mode-tabletop-dim', '--mode-compare-dim', '--mode-optimize-dim'
        ];
        modeVars.forEach(v => expect(vars.has(v)).toBe(true));
      });
    });
  });
});
```

**Total tests:** ~35 (1 default theme × 10 categories + 4 themes × 3 key categories each)

---

### Step 3: Add missing variables to default theme (.hhp-root)

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css`

**Action:** MODIFY (add variables to `.hhp-root` selector, lines 26-68)

**Source:** Extract values from `platform/simdecisions-2/src/index.css` `:root` selector

Add the following categories (insert after existing variables, before closing `}`):

```css
.hhp-root {
  /* Existing ~24 variables */
  --sd-bg: #0e0a1a;
  --sd-surface: rgba(30, 20, 50, 0.95);
  /* ... existing vars ... */

  /* Extended color variants */
  --sd-purple-light: [value from platform];
  --sd-purple-hover: [value from platform];
  --sd-purple-deep: [value from platform];
  --sd-purple-dimmer: [value from platform];
  --sd-purple-dimmest: [value from platform];
  --sd-green-dark: [value from platform];
  --sd-green-dimmer: [value from platform];
  --sd-green-dimmest: [value from platform];
  --sd-orange-bright: [value from platform];
  --sd-orange-dimmer: [value from platform];
  --sd-cyan-dimmer: [value from platform];
  --sd-cyan-dimmest: [value from platform];
  --sd-cyan-border: [value from platform];
  --sd-red-dimmer: [value from platform];

  /* Shadow system */
  --sd-shadow-sm: [value from platform];
  --sd-shadow-md: [value from platform];
  --sd-shadow-lg: [value from platform];
  --sd-shadow-xl: [value from platform];
  --sd-shadow-2xl: [value from platform];

  /* Gradients */
  --sd-gradient-purple: [value from platform];
  --sd-gradient-green: [value from platform];
  --sd-gradient-orange: [value from platform];

  /* Glow effects */
  --sd-purple-glow: [value from platform];
  --sd-green-glow: [value from platform];
  --sd-orange-glow: [value from platform];
  --sd-cyan-glow: [value from platform];

  /* Glass variants */
  --sd-glass-bg-light: [value from platform];
  --sd-glass-bg-dark: [value from platform];

  /* Overlay system */
  --sd-overlay: [value from platform];
  --sd-overlay-heavy: [value from platform];

  /* Text variants */
  --sd-text-secondary-light: [value from platform];
  --sd-text-on-accent: [value from platform];

  /* Dialog/UI helpers */
  --sd-bg-secondary: [value from platform];
  --sd-bg-hover: [value from platform];
  --sd-bg-subtle: [value from platform];
  --sd-accent-subtle: [value from platform];

  /* Grid dot */
  --sd-grid-dot: [value from platform];

  /* Mode colors */
  --mode-design: [value from platform];
  --mode-production: [value from platform];
  --mode-simulate: [value from platform];
  --mode-playback: [value from platform];
  --mode-tabletop: [value from platform];
  --mode-compare: [value from platform];
  --mode-optimize: [value from platform];
  --mode-design-dim: [value from platform];
  --mode-production-dim: [value from platform];
  --mode-simulate-dim: [value from platform];
  --mode-playback-dim: [value from platform];
  --mode-tabletop-dim: [value from platform];
  --mode-compare-dim: [value from platform];
  --mode-optimize-dim: [value from platform];
}
```

**Important:** Keep existing shiftcenter values for variables that already exist. Only ADD the missing ones.

---

### Step 4: Add missing variables to depth theme

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css`

**Action:** MODIFY (add variables to `.hhp-root[data-theme="depth"]` selector, lines 70-84)

**Source:** Extract values from `platform/simdecisions-2/src/themes/depth.css`

Add all 51 variable categories (same structure as default theme, but with depth-specific values).

---

### Step 5: Add missing variables to light theme

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css`

**Action:** MODIFY (add variables to `.hhp-root[data-theme="light"]` selector, lines 86-110)

**Source:** Extract values from `platform/simdecisions-2/src/styles/themes.css` lines 33-139

Add all 51 variable categories.

---

### Step 6: Add missing variables to monochrome theme

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css`

**Action:** MODIFY (add variables to `.hhp-root[data-theme="monochrome"]` selector, lines 112-136)

**Source:** Extract values from `platform/simdecisions-2/src/styles/themes.css` lines 143-245

Add all 51 variable categories.

---

### Step 7: Add missing variables to high-contrast theme

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css`

**Action:** MODIFY (add variables to `.hhp-root[data-theme="high-contrast"]` selector, lines 138-160)

**Source:** Extract values from `platform/simdecisions-2/src/styles/themes.css` lines 249-352

Add all 51 variable categories.

---

## Files Modified

| File | Action | Lines Added |
|------|--------|-------------|
| `browser/src/shell/shell-themes.css` | MODIFY | ~255 (51 vars × 5 themes) |

---

## Test Files

| File | Action | Tests |
|------|--------|-------|
| `browser/src/shell/__tests__/shell-themes.test.ts` | CREATE | ~35 |

---

## Constraints

- **Port exact platform values.** Do not invent new values.
- **Keep existing shiftcenter values** for variables that already exist (e.g., `--sd-border` opacity may differ). Only ADD missing vars.
- **CSS: `var(--sd-*)` only.** No hex in new code. Existing hardcoded values on body/hhp-root for `--sd-bg` are grandfathered.
- **File size:** shell-themes.css will grow significantly. Target under 500 lines total.
- **TDD:** Write tests first (Step 2), then add variables (Steps 3-7).
- **No stubs:** All variables must have real values ported from platform.

---

## Definition of Done

- [ ] All 35 tests pass
- [ ] Default theme has all 51 missing variables
- [ ] Depth theme has all 51 missing variables
- [ ] Light theme has all 51 missing variables
- [ ] Monochrome theme has all 51 missing variables
- [ ] High-contrast theme has all 51 missing variables
- [ ] No hardcoded hex in new variable values (all rgba or var references)
- [ ] shell-themes.css under 500 lines
- [ ] Manual test: shadow variables visible in browser DevTools
- [ ] Manual test: mode color variables present in each theme

---

**End of task file. Ready for dispatch to BEE-SONNET.**
