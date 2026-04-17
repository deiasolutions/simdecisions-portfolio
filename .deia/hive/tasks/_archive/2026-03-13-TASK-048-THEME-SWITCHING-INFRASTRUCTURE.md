# TASK-048: Theme Switching Infrastructure

**Date:** 2026-03-13
**Bee Model:** Sonnet
**From:** Q33N
**Parent Briefing:** `.deia/hive/coordination/2026-03-13-BRIEFING-THEME-SWITCHING.md`
**Depends On:** None
**Blocks:** TASK-049 (CSS variable gap fill needs body bg fix)

---

## Objective

Port the platform's theme switching infrastructure into shiftcenter shell. Replace the volumeStorage DI stub with the full implementation from platform, add theme state management to Shell.tsx, wire theme into ShellContext, create ThemePicker component, and apply body background fix.

---

## What Already Exists

| Artifact | File | Lines |
|----------|------|-------|
| 5 theme CSS variable sets | `browser/src/shell/shell-themes.css` | 26-160 |
| `THEMES` constant | `browser/src/shell/constants.ts` | 42-48 |
| `ThemeId` type | `browser/src/shell/constants.ts` | 51 |
| `ShellContextValue` interface | `browser/src/infrastructure/relay_bus/messageBus.ts` | 288-297 |
| volumeStorage DI stub (21 lines) | `browser/src/shell/volumeStorage.ts` | entire file |
| volumeStorage usage | `browser/src/shell/actions/lifecycle.ts` | 159 |

---

## What to Port from Platform

| Artifact | Platform Source | Lines |
|----------|----------------|-------|
| Full volumeStorage impl | `platform/simdecisions-2/src/services/storage/volumeStorage.ts` | 1-136 |
| Theme state + persistence pattern | `platform/simdecisions-2/src/components/shell/HiveHostPanes.jsx` | 112-119 |
| data-theme attribute pattern | `platform/simdecisions-2/src/components/shell/HiveHostPanes.jsx` | 364 |
| Theme in context pattern | `platform/simdecisions-2/src/components/shell/HiveHostPanes.jsx` | 349-350 |
| ThemePicker component (dropdown variant) | `platform/simdecisions-2/src/components/shared/ThemePicker.tsx` | 1-98 |

---

## Implementation Steps (TDD)

### Step 1: Replace volumeStorage stub with full implementation

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\volumeStorage.ts`

**Action:** REPLACE entire file

Port the full implementation from `platform/simdecisions-2/src/services/storage/volumeStorage.ts`.

**Key functions to port:**
- `readVolume<T>(path: string): T | null` — reads from localStorage/sessionStorage by volume path
- `writeVolume<T>(path: string, data: T): void` — writes JSON-serialized data
- `deleteVolume(path: string): void` — removes a volume
- `hasVolume(path: string): boolean` — checks existence
- `listVolumes(prefix: string): string[]` — lists volumes under a prefix
- `migrateKey(oldKey: string, newPath: string): void` — migrates old localStorage key to new volume path

**Path format:** `local://shell/theme` → localStorage key `sd:volume:shell/theme`

**Breaking change:** Remove the old DI pattern (`setVolumeStorage`, `getVolumeStorage`). Export the functions directly.

**File size target:** Under 150 lines

**Tests:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\volumeStorage.test.ts` (NEW)

Test cases (minimum 5):
1. `readVolume` returns null for missing key
2. `readVolume`/`writeVolume` round-trip with object data
3. `deleteVolume` removes key from localStorage
4. `migrateKey` moves old key to new volume path and deletes old key
5. `migrateKey` no-ops if new path already exists (preserves new value)

---

### Step 2: Update volumeStorage exports

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\index.ts`

**Action:** MODIFY

Update exports to match new volumeStorage API:

```typescript
export { readVolume, writeVolume, deleteVolume, hasVolume, listVolumes, migrateKey } from './volumeStorage';
```

Remove old DI exports if present.

---

### Step 3: Update lifecycle.ts volumeStorage usage

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\actions\lifecycle.ts`

**Action:** MODIFY (line 159)

**Current pattern:**
```typescript
getVolumeStorage()?.writeVolume(...)
```

**New pattern:**
```typescript
import { writeVolume } from '../volumeStorage';
// ...
writeVolume(...)
```

Remove optional chaining since function is always available.

---

### Step 4: Add theme state to Shell.tsx

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx`

**Action:** MODIFY

Add imports:
```typescript
import { useState, useCallback } from 'react';
import { readVolume, writeVolume, migrateKey } from '../volumeStorage';
import type { ThemeId } from '../constants';
```

Add state inside Shell component (port exact pattern from HiveHostPanes.jsx:112-119):
```typescript
const [theme, setThemeState] = useState<ThemeId>(() => {
  migrateKey('sd:shell_theme', 'local://shell/theme');
  return (readVolume<string>('local://shell/theme') as ThemeId) || 'full-color';
});

const setTheme = useCallback((value: ThemeId) => {
  setThemeState(value);
  try { writeVolume('local://shell/theme', value); } catch {}
}, []);
```

Apply `data-theme` attribute on `.hhp-root` div (currently line ~51):
```typescript
<div className="shell-frame hhp-root" data-testid="shell-frame"
     data-theme={theme === 'full-color' ? undefined : theme}>
```

**Tests:** Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\Shell.test.tsx`

Add test cases (minimum 5):
1. Shell renders with default theme (no data-theme attribute when theme is 'full-color')
2. Shell applies data-theme="depth" when theme is 'depth'
3. Theme persists to volumeStorage when setTheme is called
4. Theme loads from volumeStorage on mount (mock readVolume to return 'monochrome')
5. Invalid volumeStorage value falls back to 'full-color'

---

### Step 5: Add theme/setTheme to ShellContextValue

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\messageBus.ts`

**Action:** MODIFY (ShellContextValue interface, line ~288)

Add fields:
```typescript
export interface ShellContextValue {
  bus: MessageBus;
  dispatch: (action: ShellAction) => void;
  focusedPaneId?: string;
  maximizedPaneId?: string;
  swapPendingId?: string;
  root?: PaneNode;
  theme?: string;
  setTheme?: (theme: string) => void;
}
```

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx`

**Action:** MODIFY (context value creation)

Include theme and setTheme in the context value:
```typescript
const ctx = useMemo(() => ({
  bus,
  dispatch,
  focusedPaneId: state.focusedPaneId,
  maximizedPaneId: state.maximizedPaneId,
  swapPendingId: state.swapPendingId,
  root: state.root,
  theme,
  setTheme,
}), [bus, dispatch, state.focusedPaneId, state.maximizedPaneId, state.swapPendingId, state.root, theme, setTheme]);
```

---

### Step 6: Create ThemePicker component

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ThemePicker.tsx` (NEW)

**Action:** CREATE (~70 lines)

Port the **dropdown variant** from `platform/simdecisions-2/src/components/shared/ThemePicker.tsx`.

**Adaptations:**
- Replace `useUIStore` with `useShell()` from `../../infrastructure/relay_bus/messageBus`
- Import `THEMES` from `../constants`
- No lucide-react dependency — use the icon character from THEMES constant instead of `<Palette>` icon
- Keep click-outside-to-close pattern (`useEffect` + `useRef`)
- Dropdown menu with checkmark (✓) for active theme

**Structure:**
```typescript
import { useState, useRef, useEffect } from 'react';
import { useShell } from '../../infrastructure/relay_bus/messageBus';
import { THEMES } from '../constants';
import './theme-picker.css';

export function ThemePicker() {
  const { theme, setTheme } = useShell();
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Click-outside-to-close
  useEffect(() => {
    if (!isOpen) return;
    const handleClick = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [isOpen]);

  return (
    <div className="theme-picker" ref={menuRef}>
      <button
        className="theme-picker-trigger"
        onClick={() => setIsOpen(!isOpen)}
        title="Change theme"
      >
        {THEMES.find(t => t.id === theme)?.icon || '🎨'}
      </button>
      {isOpen && (
        <div className="theme-picker-menu">
          {THEMES.map(t => (
            <button
              key={t.id}
              className={`theme-picker-item ${theme === t.id ? 'active' : ''}`}
              onClick={() => {
                setTheme?.(t.id);
                setIsOpen(false);
              }}
            >
              <span className="theme-picker-icon">{t.icon}</span>
              <span className="theme-picker-label">{t.label}</span>
              {theme === t.id && <span className="theme-picker-check">✓</span>}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
```

**File size target:** Under 80 lines

**Tests:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\ThemePicker.test.tsx` (NEW)

Test cases (minimum 4):
1. ThemePicker renders trigger button with current theme icon
2. ThemePicker renders 5 theme buttons when menu is open
3. ThemePicker highlights active theme with checkmark
4. ThemePicker calls setTheme on click and closes menu
5. ThemePicker closes dropdown when clicking outside

---

### Step 7: Create ThemePicker styles

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\theme-picker.css` (NEW)

**Action:** CREATE (~60 lines)

**Requirements:**
- All colors via CSS variables (`var(--sd-*)`)
- Trigger button: 28px × 28px, `var(--sd-surface-alt)` bg, `var(--sd-text-secondary)` color
- Menu: `var(--sd-surface)` bg, `var(--sd-border)` 1px border, absolute positioned above trigger
- Menu items: hover `var(--sd-surface-hover)` bg
- Active item: checkmark + `var(--sd-accent)` color
- Z-index: 100 (menu)

**Example structure:**
```css
.theme-picker {
  position: relative;
}

.theme-picker-trigger {
  width: 28px;
  height: 28px;
  background: var(--sd-surface-alt);
  color: var(--sd-text-secondary);
  border: 1px solid var(--sd-border);
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.theme-picker-trigger:hover {
  background: var(--sd-surface-hover);
}

.theme-picker-menu {
  position: absolute;
  bottom: 100%;
  right: 0;
  margin-bottom: 4px;
  background: var(--sd-surface);
  border: 1px solid var(--sd-border);
  border-radius: 6px;
  box-shadow: var(--sd-shadow-lg);
  z-index: 100;
  min-width: 160px;
}

.theme-picker-item {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 8px 12px;
  background: none;
  border: none;
  color: var(--sd-text-primary);
  cursor: pointer;
  text-align: left;
}

.theme-picker-item:hover {
  background: var(--sd-surface-hover);
}

.theme-picker-item.active {
  color: var(--sd-accent);
}

.theme-picker-check {
  margin-left: auto;
  color: var(--sd-accent);
}
```

**File size target:** Under 100 lines

---

### Step 8: Render ThemePicker in Shell

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx`

**Action:** MODIFY

Import ThemePicker:
```typescript
import { ThemePicker } from './ThemePicker';
```

Add inside `.shell-frame` div (before closing tag):
```typescript
<div className="shell-frame hhp-root" data-testid="shell-frame" data-theme={theme === 'full-color' ? undefined : theme}>
  {/* existing content */}
  <ThemePicker />
</div>
```

Add positioning CSS to shell.css or inline style:
```css
.shell-frame .theme-picker {
  position: absolute;
  bottom: 8px;
  right: 8px;
  z-index: 5;
}
```

---

### Step 9: Body background fix

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css`

**Action:** MODIFY (line ~26)

Add `background: var(--sd-bg);` to the `.hhp-root` rule:

```css
.hhp-root {
  background: var(--sd-bg);
  color: var(--sd-text-primary);
  /* ... existing vars ... */
}
```

Keep the hardcoded `background: #0e0a1a` on `body` as fallback before React mounts.

---

## Files Modified

| File | Action | Lines Changed |
|------|--------|---------------|
| `browser/src/shell/volumeStorage.ts` | REPLACE | ~130 |
| `browser/src/shell/index.ts` | MODIFY | ~5 |
| `browser/src/shell/actions/lifecycle.ts` | MODIFY | ~3 |
| `browser/src/shell/components/Shell.tsx` | MODIFY | ~20 |
| `browser/src/infrastructure/relay_bus/messageBus.ts` | MODIFY | ~2 |
| `browser/src/shell/components/ThemePicker.tsx` | CREATE | ~70 |
| `browser/src/shell/components/theme-picker.css` | CREATE | ~60 |
| `browser/src/shell/shell-themes.css` | MODIFY | ~1 |

---

## Test Files

| File | Action | Tests |
|------|--------|-------|
| `browser/src/shell/__tests__/volumeStorage.test.ts` | CREATE | 5 |
| `browser/src/shell/components/__tests__/Shell.test.tsx` | MODIFY | +5 |
| `browser/src/shell/components/__tests__/ThemePicker.test.tsx` | CREATE | 5 |

**Total new tests:** 15

---

## Constraints

- CSS: `var(--sd-*)` only. No hex, rgb(), or named colors in new code.
- ThemePicker.tsx under 80 lines.
- volumeStorage.ts under 150 lines.
- theme-picker.css under 100 lines.
- TDD: Write tests first, then implementation.
- No stubs: All functions fully implemented.
- Port exact platform patterns — do not invent new approaches.

---

## Definition of Done

- [ ] volumeStorage.ts replaced with full implementation (5 functions exported)
- [ ] lifecycle.ts updated to use new volumeStorage API
- [ ] Shell.tsx has theme state + persistence + data-theme attribute
- [ ] ShellContextValue has theme and setTheme fields
- [ ] ThemePicker component renders and changes theme
- [ ] ThemePicker CSS uses only CSS variables
- [ ] Body background fix applied to .hhp-root
- [ ] All 15 tests pass
- [ ] Manual test: theme persists across page reload
- [ ] Manual test: ThemePicker dropdown opens/closes correctly
- [ ] Manual test: clicking theme changes CSS variables visibly

---

**End of task file. Ready for dispatch to BEE-SONNET.**
