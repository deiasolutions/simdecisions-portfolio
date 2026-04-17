# SPEC-KB-001C: SC Keyboard — Gestures, Menu & Physical Keyboard

## Priority
P2

## Depends On
- KB-001A (core component)
- KB-001B (bus wiring for RTD emissions)

## Objective
Complete the SC Keyboard by wiring gesture handlers (swipe-to-minimize, long-press/right-click options menu), the options menu with 5 hardware settings, and physical keyboard auto-hide detection. After this wave, the keyboard is feature-complete per SPEC-SC-KEYBOARD-001 v3.

## Source Material
- `SCKeyboard.jsx` (v3) — gesture and menu implementation reference
- `SPEC-SC-KEYBOARD-001 v3` — sections 3 (Gestures), 4 (Long-Press Menu), 11 (Physical Keyboard)
- `DISPATCH-TASK-KB-001` — Gestures, Long-Press Menu, Testing checklist

## Files to Read First
- browser/src/primitives/keyboard/SCKeyboard.tsx
  from Wave A — contains inline minimized/showMenu state to extract into hooks
- browser/src/primitives/keyboard/useKeyboardBus.ts
  from Wave B — bus emission utility for RTD events
- browser/src/shell/types.ts
  ChromeOptions, menu schema

## Scope

### 0. State Migration
Wave A created `minimized` and `showMenu` as inline useState in SCKeyboard.tsx. This wave extracts them:
- `minimized` / `setMinimized` → moves into `useTrayGestures.ts`
- `showMenu` / `setShowMenu` → moves into `useOptionsMenu.ts`
- `swipeStartY` / `longPressRef` → new state in `useTrayGestures.ts`
- SCKeyboard.tsx consumes these hooks instead of inline state. Pill rendering stays in SCKeyboard.tsx, reading `minimized` from the hook.

### 1. Tray Gesture Handler
In the JSX, swipe detection and long-press detection share the same touch lifecycle (onTouchStart/Move/End). They CANNOT be separate hooks — both need the same touch start event. Extract into one unified `useTrayGestures.ts`:
- Touch start: record Y position AND start 600ms long-press timer. Guard: only on tray (check `data-key` attribute — skip if target is a key).
- Touch move: cancel long-press timer on ANY move. If delta Y > 60px downward → minimize to pill.
- Touch end: cancel long-press timer, reset swipe state.
- Long-press fires (600ms, no movement): calls `onLongPress` callback → opens options menu.
- Returns `{ minimized, setMinimized, onTrayTouchStart, onTrayTouchMove, onTrayTouchEnd }`.
- Pill rendering: glass lozenge 100px × 36px, keyboard icon + "kb", tap restores.
- Emit RTD via bus (from Wave B): `keyboard:minimized` on minimize, `keyboard:restored` on restore.

### 2. Long-Press / Right-Click Options Menu
- **Mobile**: long-press (600ms) on tray opens bottom sheet.
- **Desktop**: right-click on tray opens dropdown menu.
- Only triggers on tray area (not on keys).
- Menu contains exactly 5 items:

| Item | Display | Behavior |
|------|---------|----------|
| Readout position | `readout: below` / `above` / `hidden` | Cycles through 3 positions |
| Return lock default | `return lock: on` / `off` | Toggles returnLocked |
| Fn lock default | `Fn lock: on` / `off` | Toggles fnLocked |
| F-row visibility | `F-row: visible` / `hidden` | Toggles fRowVisible (landscape only) |
| Buffer window size | `buffer: 8 chars` / `14 chars` / `20 chars` | Cycles 14 → 20 → 8 → 14 |

- Menu closes on: item tap (after action), "close" link at bottom, tap outside menu.
- Menu renders inside the keyboard's own container (absolute positioned, above tray).
- Menu styling: monospace labels, theme-aware (dark/glass from sd:hhpanes_mode), accent-colored close link.
- **Manifest schema**: Per dispatch ("schema in manifest, HiveHostPanes renders"), the keyboard's appConfig manifest must declare its menu schema so HiveHostPanes can discover the menu items. The keyboard component renders its own menu (as in the JSX), but the schema is also declared in the APP_REGISTRY entry or appConfig for stage-level discovery.

**NOT in this menu** (these are ShiftCenter View/Tools menu items):
- Keyboard on/off
- System keyboard switch
- Orientation lock

### 3. Physical Keyboard Auto-Hide
Detect physical keyboard connection and auto-hide the on-screen keyboard:
- Listen for keyboard events that indicate physical input (e.g., `keydown` with `isTrusted: true` and no touch event preceding it).
- On detection: minimize keyboard to pill automatically.
- Stage manages reactivation (not this primitive's job) — the keyboard stays as pill until tapped or stage restores it.
- Emit RTD: `keyboard:physical-detected` when auto-hiding.

### 4. Desktop Right-Click Prevention
- `onContextMenu` on tray element: `ev.preventDefault()` + open options menu.
- Keys themselves suppress context menu via `onContextMenu` prevent default (already in Wave A).

## Module Files

1. **useTrayGestures.ts** — Unified tray gesture hook (replaces dispatch's `useSwipeMinimize.ts` — renamed because it handles BOTH swipe-to-minimize AND long-press-to-menu, which share the same touch lifecycle). Returns `{ minimized, setMinimized, onTrayTouchStart, onTrayTouchMove, onTrayTouchEnd }`. Accepts `onLongPress` callback. Internal state: swipeStartY, longPressTimer ref.

2. **useOptionsMenu.ts** (new) — Menu state and actions. Returns `{ showMenu, openMenu, closeMenu, menuItems }`. `openMenu` is passed as `onLongPress` to useTrayGestures. Each menu item: `{ label: string, action: () => void }`. Formats labels from current state (readoutPos, returnLocked, fnLocked, fRowVisible, bufferWindow).

3. **OptionsMenu.tsx** (new) — Presentational component for the menu. Props: `{ items, visible, onClose, dark, accent, border }`. Renders absolute-positioned panel with item list + close link.

4. **usePhysicalKeyboard.ts** (new) — Physical keyboard detection hook. Returns `{ physicalDetected }`. Sets flag on trusted keydown events. Calls `onMinimize` callback (from useTrayGestures) when detected.

## DO NOT
- Add any items to the menu beyond the 5 specified
- Add keyboard lifecycle controls to the menu (on/off is ShiftCenter View/Tools)
- Add orientation lock to the menu (ShiftCenter View settings)
- Build a "settings panel" — the menu is a simple list, not a form
- Use native `<select>`, `<input>`, or `<range>` in the menu
- Add drag/resize/rotate gestures
- Change the swipe threshold (60px) or long-press duration (600ms)

## Deliverables
1. browser/src/primitives/keyboard/useTrayGestures.ts (dispatch calls this useSwipeMinimize.ts — renamed, see Module Files note)
2. browser/src/primitives/keyboard/useOptionsMenu.ts (new)
3. browser/src/primitives/keyboard/OptionsMenu.tsx (new)
4. browser/src/primitives/keyboard/usePhysicalKeyboard.ts (new)
5. Updated: browser/src/primitives/keyboard/SCKeyboard.tsx (migrate inline minimized/showMenu state to hooks, integrate gestures + menu + physical detection)
6. browser/src/primitives/keyboard/__tests__/trayGestures.test.ts
7. browser/src/primitives/keyboard/__tests__/optionsMenu.test.ts
8. browser/src/primitives/keyboard/__tests__/physicalKeyboard.test.ts

## Acceptance Criteria
- [ ] Swipe down (>60px) on tray minimizes keyboard to pill
- [ ] Swipe on key elements does NOT trigger minimize (data-key guard)
- [ ] Tap pill restores full keyboard
- [ ] Long-press (600ms) on tray opens options menu (mobile)
- [ ] Right-click on tray opens options menu (desktop)
- [ ] Long-press on keys does NOT open menu
- [ ] Menu shows exactly 5 items with current state values
- [ ] Readout position cycles: below → above → hidden → below
- [ ] Return lock toggles on/off
- [ ] Fn lock toggles on/off
- [ ] F-row visibility toggles visible/hidden
- [ ] Buffer window cycles: 14 → 20 → 8 → 14
- [ ] Menu closes on item tap, close link, or outside tap
- [ ] Menu does NOT contain keyboard on/off, system keyboard, or orientation lock
- [ ] Physical keyboard detection: trusted keydown auto-minimizes to pill
- [ ] RTD: `keyboard:minimized` emits on minimize (swipe or physical-detect)
- [ ] RTD: `keyboard:restored` emits on restore (pill tap)
- [ ] RTD: `keyboard:physical-detected` emits on physical keyboard auto-hide
- [ ] Desktop context menu suppressed on tray, options menu opens instead
- [ ] Menu schema declared in APP_REGISTRY or appConfig manifest for HiveHostPanes discovery
- [ ] All tests pass (minimum 12 tests)
- [ ] Build passes with `npx vite build`

## Smoke Test
- [ ] `npx vitest run browser/src/primitives/keyboard/__tests__/trayGestures.test.ts` — all tests pass
- [ ] `npx vitest run browser/src/primitives/keyboard/__tests__/optionsMenu.test.ts` — all tests pass
- [ ] `npx vite build` — zero errors

## Response File
20260328-KB-001C-RESPONSE.md
