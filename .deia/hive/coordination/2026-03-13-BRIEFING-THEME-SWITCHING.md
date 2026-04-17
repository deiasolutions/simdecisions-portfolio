# BRIEFING: Port Theme Switching from Platform (BL-118)

**Date:** 2026-03-13
**From:** Q33NR
**To:** Q33N
**Model:** Sonnet (for task file authoring)
**Bee model:** Sonnet (significant scope — volumeStorage port, Shell.tsx wiring, ThemePicker, CSS gap fill)

---

## Objective

Port the platform's theme switching system into the shiftcenter shell. The platform already has a working system: `volumeStorage` for persistence, `useState` + `useCallback` in the shell root, `data-theme` attribute on `.hhp-root`, and a `ThemePicker` component. ShiftCenter already has the 5 theme CSS variable sets and the `THEMES` constant but is missing the switching mechanism and ~50 CSS variables per theme that the platform defines.

**This is a two-task job.** TASK-044 = switching infrastructure. TASK-045 = CSS variable gap fill.

---

## What Already Exists in ShiftCenter

| Artifact | File | Status |
|----------|------|--------|
| 5 theme CSS variable sets (~24 vars each) | `browser/src/shell/shell-themes.css:26-160` | DONE |
| `data-theme` attribute selectors | `shell-themes.css:68,85,111,137` | DONE |
| `THEMES` constant (5 entries with id/label/icon) | `browser/src/shell/constants.ts:42-48` | DONE |
| `ThemeId` type | `browser/src/shell/constants.ts:51` | DONE |
| Tests for THEMES constant | `browser/src/shell/__tests__/constants.test.ts:150-180` | DONE |
| Animations using `var(--sd-accent)` | `shell-themes.css:162-211` | DONE |
| `volumeStorage.ts` (DI stub interface) | `browser/src/shell/volumeStorage.ts` | STUB — needs replacement |
| `ShellCtx` with `ShellContextValue` | `browser/src/infrastructure/relay_bus/messageBus.ts:288-297` | DONE — needs theme fields |
| `lifecycle.ts` uses `getVolumeStorage()` | `browser/src/shell/actions/lifecycle.ts:159` | DONE — uses DI pattern |

---

## What Exists in Platform (source of truth for porting)

| Artifact | Platform File | What to Port |
|----------|--------------|-------------|
| Full volumeStorage implementation | `src/services/storage/volumeStorage.ts` (136 lines) | Port entirely |
| Shell theme state + persistence | `src/components/shell/HiveHostPanes.jsx:112-119` | Port pattern to Shell.tsx |
| `data-theme` attribute | `HiveHostPanes.jsx:364` | Port pattern |
| Theme in context | `HiveHostPanes.jsx:349-350` | Add to ShellContextValue |
| ThemePicker component | `src/components/shared/ThemePicker.tsx` (98 lines) | Port dropdown variant, adapt to ShellCtx |
| Default theme full CSS (~90 vars) | `src/index.css` `:root` selector | Port missing vars |
| Depth theme full CSS (~70 vars) | `src/themes/depth.css` | Port missing vars |
| Light/Mono/HC full CSS (~85 vars each) | `src/styles/themes.css` | Port missing vars |

---

## TASK-044: Theme Switching Infrastructure

### 1. Replace volumeStorage stub with real implementation

**File:** `browser/src/shell/volumeStorage.ts`

Replace the current 21-line DI stub with the platform's full implementation. Port from `platform/simdecisions-2/src/services/storage/volumeStorage.ts`.

Key functions to port:
- `readVolume(path)` — reads from localStorage/sessionStorage by volume path
- `writeVolume(path, data)` — writes JSON-serialized data
- `deleteVolume(path)` — removes a volume
- `hasVolume(path)` — checks existence
- `listVolumes(prefix)` — lists volumes under a prefix
- `migrateKey(oldKey, newPath)` — migrates old localStorage key to new volume path

Path format: `local://shell/theme` → localStorage key `sd:volume:shell/theme`

**Breaking change:** The old DI pattern (`setVolumeStorage`/`getVolumeStorage`) is removed. `lifecycle.ts` line 159 currently calls `getVolumeStorage()?.writeVolume(...)` — update it to import `writeVolume` directly.

**Backward compat:** Keep `setVolumeStorage` and `getVolumeStorage` as deprecated re-exports that delegate to the real functions. Or just update the one callsite in `lifecycle.ts`.

Update `browser/src/shell/index.ts` exports to match new API.

### 2. Add theme state to Shell.tsx

**File:** `browser/src/shell/components/Shell.tsx`

Port the exact pattern from `HiveHostPanes.jsx:112-119`:

```tsx
import { useState, useCallback } from 'react';
import { readVolume, writeVolume, migrateKey } from '../volumeStorage';
import type { ThemeId } from '../constants';

// Inside Shell component:
const [theme, setThemeState] = useState<ThemeId>(() => {
  migrateKey('sd:shell_theme', 'local://shell/theme');
  return (readVolume<string>('local://shell/theme') as ThemeId) || 'full-color';
});

const setTheme = useCallback((value: ThemeId) => {
  setThemeState(value);
  try { writeVolume('local://shell/theme', value); } catch {}
}, []);
```

Apply `data-theme` on `.hhp-root` (line 51):
```tsx
<div className="shell-frame hhp-root" data-testid="shell-frame"
     data-theme={theme === 'full-color' ? undefined : theme}>
```

### 3. Add theme + setTheme to ShellContextValue

**File:** `browser/src/infrastructure/relay_bus/messageBus.ts`

Add to `ShellContextValue` interface (line 288):
```typescript
theme?: string;
setTheme?: (theme: string) => void;
```

In `Shell.tsx`, include in the context value:
```tsx
const ctx = useMemo(() => ({
  bus, dispatch,
  focusedPaneId: state.focusedPaneId,
  maximizedPaneId: state.maximizedPaneId,
  swapPendingId: state.swapPendingId,
  root: state.root,
  theme,
  setTheme,
}), [bus, dispatch, state.focusedPaneId, state.maximizedPaneId, state.swapPendingId, state.root, theme, setTheme]);
```

### 4. Create ThemePicker component

**File:** `browser/src/shell/components/ThemePicker.tsx` (NEW, ~70 lines)

Port the **dropdown variant** from platform's `ThemePicker.tsx`. Adapt:
- Replace `useUIStore` with `useShell()` from relay_bus (reads `theme` and `setTheme` from context)
- Import `THEMES` from `../constants`
- No lucide-react dependency — use the icon characters from THEMES constant instead of `<Palette>`
- Click-outside-to-close pattern (same `useEffect` + `useRef`)
- Dropdown menu with checkmark for active theme

**Styling:** Create `browser/src/shell/components/theme-picker.css` (NEW, ~60 lines)
- Trigger button: 28px, `var(--sd-surface-alt)` bg, `var(--sd-text-secondary)` color
- Menu: `var(--sd-surface)` bg, `var(--sd-border)` border, absolute positioned above trigger
- Active item: checkmark + `var(--sd-accent)` color
- Hover: `var(--sd-surface-hover)` bg
- All CSS vars, no hex

### 5. Render ThemePicker in Shell

**File:** `browser/src/shell/components/Shell.tsx`

Add ThemePicker inside `.shell-frame`, positioned at bottom-right:
```tsx
<ThemePicker />
```

Position via CSS: `position: absolute; bottom: 8px; right: 8px; z-index: 5;`

### 6. Body background fix

**File:** `browser/src/shell/shell-themes.css`

Add `background: var(--sd-bg);` to the `.hhp-root` rule (line 26). Keep the hardcoded `background: #0e0a1a` on body as fallback before React mounts.

---

## TASK-045: CSS Variable Gap Fill

### Objective

ShiftCenter's themes define ~24 CSS variables per theme. Platform defines ~90. Port the missing ~66 variables for all 5 themes from the platform source files.

### Missing Variable Categories

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
| Mode colors | `--mode-design`, `--mode-production`, `--mode-simulate`, `--mode-playback`, `--mode-tabletop`, `--mode-compare`, `--mode-optimize` + dim variants | 14 |
| **Total per theme** | | **~51** |

### Source Files for Values

| Theme | Platform Source |
|-------|---------------|
| full-color (default) | `platform/.../src/index.css` `:root` selector |
| depth | `platform/.../src/themes/depth.css` |
| light | `platform/.../src/styles/themes.css` lines 33-139 |
| monochrome | `platform/.../src/styles/themes.css` lines 143-245 |
| high-contrast | `platform/.../src/styles/themes.css` lines 249-352 |

### File to Modify

**`browser/src/shell/shell-themes.css`** — Add the missing variables to each theme's existing selector block. Do NOT duplicate selectors. Add variables into the existing `.hhp-root` and `.hhp-root[data-theme="..."]` blocks.

Note: ShiftCenter uses `.hhp-root[data-theme]` selectors, platform uses `html[data-theme]` selectors. Keep the shiftcenter convention.

Note: Some existing values in shiftcenter differ slightly from platform (e.g., border opacity values). **Keep the existing shiftcenter values for variables that already exist.** Only ADD the missing ones.

---

## Files Reference

| File | Action | Task |
|------|--------|------|
| `browser/src/shell/volumeStorage.ts` | REPLACE (stub → full impl) | TASK-044 |
| `browser/src/shell/components/Shell.tsx` | MODIFY (add theme state, data-theme, ThemePicker) | TASK-044 |
| `browser/src/infrastructure/relay_bus/messageBus.ts` | MODIFY (add theme/setTheme to ShellContextValue) | TASK-044 |
| `browser/src/shell/components/ThemePicker.tsx` | NEW (~70 lines) | TASK-044 |
| `browser/src/shell/components/theme-picker.css` | NEW (~60 lines) | TASK-044 |
| `browser/src/shell/shell-themes.css` | MODIFY (add bg to .hhp-root) | TASK-044 |
| `browser/src/shell/shell-themes.css` | MODIFY (add ~51 vars × 5 themes) | TASK-045 |
| `browser/src/shell/actions/lifecycle.ts` | MODIFY (update volumeStorage import) | TASK-044 |
| `browser/src/shell/index.ts` | MODIFY (update volumeStorage exports) | TASK-044 |

---

## Test Requirements

### TASK-044 Tests (12 minimum)

| # | Test | File |
|---|------|------|
| 1 | `readVolume` returns null for missing key | volumeStorage.test.ts |
| 2 | `readVolume`/`writeVolume` round-trip | volumeStorage.test.ts |
| 3 | `deleteVolume` removes key | volumeStorage.test.ts |
| 4 | `migrateKey` moves old key to new volume path | volumeStorage.test.ts |
| 5 | `migrateKey` no-ops if new path exists | volumeStorage.test.ts |
| 6 | Shell renders with default theme (no data-theme attribute) | Shell.test.tsx |
| 7 | Shell applies data-theme attribute when theme is not full-color | Shell.test.tsx |
| 8 | Theme persists to volumeStorage on change | Shell.test.tsx |
| 9 | Theme loads from volumeStorage on mount | Shell.test.tsx |
| 10 | Invalid volumeStorage value falls back to full-color | Shell.test.tsx |
| 11 | ThemePicker renders 5 theme buttons | ThemePicker.test.tsx |
| 12 | ThemePicker highlights active theme | ThemePicker.test.tsx |
| 13 | ThemePicker calls setTheme on click | ThemePicker.test.tsx |
| 14 | ThemePicker closes dropdown on click outside | ThemePicker.test.tsx |

### TASK-045 Tests (5 minimum)

| # | Test | File |
|---|------|------|
| 1 | Default theme defines all expected CSS variable categories | shell-themes.test.ts |
| 2 | Each theme override defines shadow variables | shell-themes.test.ts |
| 3 | Each theme override defines gradient variables | shell-themes.test.ts |
| 4 | Each theme override defines mode color variables | shell-themes.test.ts |
| 5 | No hardcoded hex in new variable values (regex scan) | shell-themes.test.ts |

---

## Constraints

- CSS: `var(--sd-*)` only in new code. No hex (existing body fallback is fine).
- No file over 500 lines.
- TDD.
- No stubs.
- `ThemePicker.tsx` under 80 lines.
- `volumeStorage.ts` under 150 lines.
- `shell-themes.css` will grow significantly with gap fill — keep under 500 lines.
- Port exact platform values. Do not invent new values.

---

## Task IDs

- **TASK-044** — Theme switching infrastructure (volumeStorage, Shell.tsx, ShellCtx, ThemePicker, body bg)
- **TASK-045** — CSS variable gap fill (port ~51 missing vars × 5 themes from platform)

TASK-045 depends on TASK-044 (needs the body bg fix in shell-themes.css from TASK-044 first).

---

**End of briefing. Q33N: write two task files and return for review.**
