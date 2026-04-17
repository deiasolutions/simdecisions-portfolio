# SPEC-KB-001A: SC Keyboard Primitive — Core Component

## Priority
P2

## Objective
Port `SCKeyboard.jsx` (v3, 525 lines) into the ShiftCenter pane primitive system as `appType: "sc-keyboard"` (P-33). ONE component, orientation-reactive: portrait renders compact layout, landscape renders full 104-key layout. ZERO surface controls — surface is keys + buffer bar, nothing else. No title bar, no drag/resize/rotate, no sliders/dots/toggles.

This wave builds the component, registers it, and gets it rendering inside a pane. Infrastructure wiring (relay_bus, RTD, theme subscription) is Wave B. Gestures and options menu are Wave C.

## Source Material
- `SCKeyboard.jsx` (v3) — the ONLY source file. Port this.
- `SPEC-SC-KEYBOARD-001 v3` — the ONLY spec.
- `DISPATCH-TASK-KB-001` — the ONLY dispatch.

## Files to Read First
- browser/src/apps/terminalAdapter.tsx
  adapter pattern
- browser/src/apps/index.ts
  registerApps centralized registration
- browser/src/shell/components/appRegistry.ts
  registerApp API
- browser/src/shell/constants.ts
  APP_REGISTRY metadata

## Module Structure

All files under `browser/src/primitives/keyboard/`:

1. **SCKeyboard.tsx** — Main component. Single file, both layouts. Orientation detection via `screen.orientation` API + `window.resize` fallback. Portrait renders compact (C_ROWS/C_SYM rows, symbol toggle, shift, backspace, space, return). Landscape renders full 104-key (F_FN, F_NUM, F_Q, F_H, F_S, F_B rows). Owns all state: buffer, shifted, capsActive, symbols, returnLocked, fnHeld, fnLocked, minimized, accentIdx, brightness, soundEnabled, readoutPos, bufferWindow, fRowVisible, flares, orientation, showMenu.

2. **BacklitKey.tsx** — Extracted key renderer. Handles both compact and full key rendering. Cap color always `#0e0f13`. Backlit mode: accent-colored text glow through dark cap. Glass mode: frosted blur background, no glow. Receives brightness, accent, flare value, dark/glass flag.

3. **TrayGlowLayer.tsx** — SVG overlay for per-key LED glow under tray surface. Gaussian blur filter. Renders circles at key positions with brightness + flare-based opacity. Tray color always `#060810`.

4. **ComposeBuffer.tsx** — Buffer bar only. Text + cursor + hidden-character count. No native `<input>` or `<textarea>`. Flow mode: auto-commits words at buffer window boundary. Hold mode: accumulates until explicit submit. Floating submit bubble appears when buffer has content. Buffer window sizes: 8 / 14 / 20 (default 14).

5. **useFnLayer.ts** — Fn key state management. Single tap toggles fnHeld. Double tap (within 250ms) toggles fnLocked. Dispatches Fn actions: F1=BL-, F2=BL+, F3=CLR (accent cycle), F4=SND (sound toggle), F5=POS (readout position cycle), F6=F/H (flow/hold toggle), F7=CMD (command palette). F8-F12 reserved (no-op). Fn+Arrows = Home/End/PgUp/PgDn (per spec section 7 — the JSX doesn't implement this yet, BUILD IT).

6. **useFlare.ts** — 500ms flare decay animation via requestAnimationFrame. Returns `{ flares, fireFlare }`. Manages per-key flare timers via ref.

7. **useClickSound.ts** — Cherry MX Blue clicky synthesis via Web Audio API. Two-oscillator double-bump: first oscillator 4200→1800Hz in 15ms, second 3600→1200Hz starting at 8ms offset. Returns `{ playClick }`. Respects soundEnabled flag.

8. **constants.ts** — Layout arrays (C_ROWS, C_SYM, F_FN, F_NUM, F_Q, F_H, F_S, F_B), ACCENTS array (7 colors with name/rgb/full), FN_ACTIONS map, CAP_COLOR, TRAY_COLOR, FLARE_MS, DEFAULT_BW.

9. **index.ts** — Barrel export.

## Registration

1. **Adapter** — `browser/src/apps/keyboardAdapter.tsx`
   - Accepts `AppRendererProps { paneId, isActive, config }`
   - Extracts ShellCtx for bus (used in Wave B, null-safe now)
   - Renders `<SCKeyboard nodeId={paneId} isActive={isActive} bus={null} />`

2. **apps/index.ts** — Add `registerApp('sc-keyboard', KeyboardAdapter)`

3. **constants.ts APP_REGISTRY** — Add entry:
   ```
   { appType: 'sc-keyboard', label: 'Keyboard', category: 'primitive' }
   ```
   (bus_receive/bus_emit added in Wave B)

## Key Behaviors to Preserve from JSX

- Orientation detection: `screen.orientation.type.startsWith("landscape")` with `window.innerWidth > innerHeight` fallback
- Compact key handler: shift toggles on single letter, symbols mode swaps entire layout, backspace/enter/space special-cased
- Full key handler: shift/caps/fn/meta/esc/backspace/tab/enter/arrow/mod/space all special-cased, dual-symbol rendering (shifted shows secondary label)
- 8OS key: tap = command palette (same as Fn+F7). Hold+key = meta_8os modifier (per spec section 7 — the JSX only handles tap, BUILD the hold-modifier behavior)
- Escape: triggers Escape Protocol (stub as console.log in Wave A, wired to relay_bus in Wave B)
- Return lock: locked = CR (newline into buffer), unlocked = submit. Double-tap return toggles lock (per spec section 7 — the JSX doesn't implement double-tap toggle, BUILD IT).
- Fn+Arrows: Home (Fn+Left), End (Fn+Right), PgUp (Fn+Up), PgDn (Fn+Down) (per spec section 7 — the JSX doesn't implement this, BUILD IT)
- Minimized pill: glass lozenge `100px × 36px`, keyboard icon + "kb", tap restores
- Status line: shows ret=CR|send, CAPS, Fn, HOLD, MUTE
- Buffer display: `\n` → ⏎, `\t` → ⇥, sliding window, hidden count indicator

## DO NOT
- Split into two component files (one component, two layouts)
- Add a title bar
- Add drag, resize, or rotate
- Add any surface controls (sliders, dots, toggles)
- Use native `<input>` or `<textarea>` of any type
- Add media controls to Fn layer
- Add keyboard lifecycle controls (on/off is ShiftCenter View/Tools)
- Add orientation lock (ShiftCenter View settings)
- Change backlight physics (caps always #0e0f13, tray always #060810)
- Build extended layout or macros
- Wire relay_bus or RTD (that's Wave B)
- Build gesture handlers or options menu (that's Wave C)

## Stubs for Later Waves
- `bus` prop accepted but unused (Wave B wires it)
- `minimized` / `showMenu` state exists as inline useState in SCKeyboard.tsx. Wave C will extract these into hooks (useTrayGestures.ts, useOptionsMenu.ts) and refactor SCKeyboard.tsx to consume the hooks. Wave A just needs the state + conditional renders.
- `dark` flag hardcoded `true` with comment `// wired to sd:hhpanes_mode in Wave B`
- Keys include `onContextMenu={(ev) => ev.preventDefault()}` to suppress browser context menu (not a gesture handler — just default prevention). Wave C adds the tray-level onContextMenu that opens the options menu.

## Deliverables
1. browser/src/primitives/keyboard/SCKeyboard.tsx
2. browser/src/primitives/keyboard/BacklitKey.tsx
3. browser/src/primitives/keyboard/TrayGlowLayer.tsx
4. browser/src/primitives/keyboard/ComposeBuffer.tsx
5. browser/src/primitives/keyboard/useFnLayer.ts
6. browser/src/primitives/keyboard/useFlare.ts
7. browser/src/primitives/keyboard/useClickSound.ts
8. browser/src/primitives/keyboard/constants.ts
9. browser/src/primitives/keyboard/index.ts
10. browser/src/apps/keyboardAdapter.tsx
11. browser/src/primitives/keyboard/__tests__/SCKeyboard.test.tsx

## Acceptance Criteria
- [ ] `appType "sc-keyboard"` resolves correctly from app registry
- [ ] Portrait orientation renders compact layout (4 alpha rows + bottom row)
- [ ] Landscape orientation renders full 104-key layout (6 rows with F-row)
- [ ] Orientation change switches layout automatically
- [ ] Surface shows ONLY keys + buffer bar — nothing else visible
- [ ] Compact: symbol toggle swaps alpha ↔ symbol rows
- [ ] Compact: shift capitalizes next letter then auto-releases
- [ ] Full: dual-symbol keys show primary/secondary with shift toggle
- [ ] Full: Fn+F1-F7 dispatch correct actions (brightness, accent, sound, position, flow/hold, cmd)
- [ ] Full: Fn+Arrows map to Home/End/PgUp/PgDn in useFnLayer (bus emission in Wave B)
- [ ] Full: Fn double-tap locks/unlocks
- [ ] Full: CapsLock toggles persistent caps
- [ ] Full: 8OS tap = command palette, 8OS hold+key = meta_8os modifier
- [ ] Full: Escape triggers Escape Protocol (console.log stub, wired in Wave B)
- [ ] Return lock: CR mode inserts newline, send mode submits buffer
- [ ] Return lock: double-tap return toggles lock mode
- [ ] Buffer bar: sliding window, cursor blink, hidden count, no native inputs
- [ ] Flow mode: auto-commits words at buffer window boundary
- [ ] Hold mode: accumulates until explicit submit
- [ ] Minimized pill renders and tap restores
- [ ] Backlit physics: cap #0e0f13, tray glow, 500ms flare decay
- [ ] MX Blue click: audible two-oscillator synthesis, toggleable
- [ ] Status line shows correct indicators
- [ ] All CSS uses var(--sd-*) only — no hex/rgb outside constants.ts backlight values
- [ ] No native `<input>` or `<textarea>` anywhere
- [ ] All tests pass (minimum 15 tests)
- [ ] Build passes with `npx vite build`

## Smoke Test
- [ ] `npx vitest run browser/src/primitives/keyboard/__tests__/SCKeyboard.test.tsx` — all tests pass
- [ ] `npx vite build` — zero errors
- [ ] `grep -r "sc-keyboard" browser/src/apps/` — adapter registered

## Response File
20260328-KB-001A-RESPONSE.md
