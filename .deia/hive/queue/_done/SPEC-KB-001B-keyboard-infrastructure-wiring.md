# SPEC-KB-001B: SC Keyboard — Infrastructure Wiring

## Priority
P2

## Depends On
- KB-001A (core component must exist and render)

## Objective
Wire the SC Keyboard primitive into ShiftCenter infrastructure: relay_bus keystroke emission, RTD emissions per ADR-RTD-001, theme subscription (accent/mode/font/a11y), and glass/backlit automatic switching from `sd:hhpanes_mode`. After this wave, every keypress emits a bus event, the keyboard tracks its own telemetry, and the visual mode follows the stage theme — no toggles.

## Source Material
- `SCKeyboard.jsx` (v3) — reference implementation
- `SPEC-SC-KEYBOARD-001 v3` — sections 8 (Backlight), 10 (Sound), 12 (Theme)
- `DISPATCH-TASK-KB-001` — "Wire to Infrastructure" section

## Files to Read First
- browser/src/infrastructure/relay_bus/MessageBus.ts
  bus API, emit/subscribe
- browser/src/infrastructure/relay_bus/types/messages.ts
  BusMessage types
- browser/src/shell/types.ts
  AppNode, shell dispatch actions
- browser/src/primitives/terminal/useTerminal.ts
  bus usage pattern in existing primitive

## Scope

### 1. relay_bus Keystroke Emission
Every keypress (compact and full) emits to relay_bus:
```typescript
bus.emit({
  type: 'keystroke',
  source: nodeId,
  payload: {
    key: string,          // the character or key name
    modifiers: {
      shift: boolean,
      ctrl: boolean,
      alt: boolean,
      fn: boolean,
      meta_8os: boolean,
    },
    timestamp: number,    // Date.now()
  }
})
```
- Fn-layer actions emit as `{ type: 'keystroke', payload: { key: 'fn:bl_down', ... } }`
- Submit emits `{ type: 'buffer:submit', source: nodeId, payload: { text: string } }`
- Bus is received via adapter prop, null-safe (no crash if bus unavailable)

### 2. RTD Emissions (per ADR-RTD-001)
Emit on state change, not on timer:
- `keyboard:orientation-changed` — when layout switches portrait ↔ landscape
- `keyboard:fn-locked` / `keyboard:fn-unlocked` — Fn lock toggles
- `keyboard:sound-toggled` — sound on/off
- `keyboard:brightness-changed` — brightness level after Fn+F1/F2
- `keyboard:accent-changed` — accent color after Fn+F3

NOTE: `keyboard:minimized` / `keyboard:restored` RTD events are deferred to Wave C, where the swipe gesture and minimized state hook are built. Wave B provides the bus emission utility that Wave C calls.

### 3. Theme Subscription
Subscribe to ShiftCenter theme system:
- **Accent color**: override local accent from theme when theme provides one (Fn+F3 cycles local override, theme reset restores theme accent)
- **Mode (dark/light)**: `sd:hhpanes_mode` determines glass vs backlit. `dark = true` → backlit (glow, dark caps). `dark = false` → glass (frosted blur, no glow). NO toggle — automatic.
- **Font**: respect `var(--font-mono)` and `var(--font-sans)` from theme
- **A11y**: if high-contrast mode, force maximum brightness, disable glow blur, use solid accent borders

### 4. Remove Hardcoded `dark = true`
Replace with theme-derived value:
```typescript
// Before (v3 JSX stub):
const dark = true; // wired to sd:hhpanes_mode in production

// After:
const dark = themeMode === 'dark'; // from sd:hhpanes_mode subscription
```
Glass rendering (non-dark path) already exists in the JSX — `BacklitKey` and `renderFullKeyEl` both have glass branches.

### 5. Update APP_REGISTRY
Add bus patterns to the `sc-keyboard` entry in constants.ts:
```typescript
{
  appType: 'sc-keyboard',
  label: 'Keyboard',
  category: 'primitive',
  bus_emit: ['keystroke', 'buffer:submit', 'keyboard:*'],
  bus_receive: ['keyboard:config-changed'],
}
```

### 6. Remove All Mocks
Per dispatch: "Remove all mocks (receiving pane, LLM, fake bus)."
- Replace `console.log("[8OS] command palette")` with real `bus.emit({ type: 'command_palette:open' })`
- Replace `console.log("[ESC]")` with real `bus.emit({ type: 'escape_protocol', source: nodeId })`
- No console.log stubs should remain for key actions after this wave

### 7. Update Adapter
Wire bus from ShellCtx into the keyboard component:
```typescript
export function KeyboardAdapter({ paneId, isActive, config }: AppRendererProps) {
  const ctx = useContext(ShellCtx);
  const bus = ctx?.bus || null;
  return <SCKeyboard nodeId={paneId} isActive={isActive} bus={bus} />;
}
```

## DO NOT
- Add any surface controls for theme switching (automatic only)
- Add a brightness slider (Fn+F1/F2 only)
- Add an accent picker UI (Fn+F3 cycle only)
- Change the keystroke emission format after it's defined here
- Add bus subscriptions for receiving keystrokes (this primitive emits only)
- Build the options menu (Wave C)
- Build gesture handlers (Wave C)

## Deliverables
1. browser/src/primitives/keyboard/useKeyboardBus.ts (new — bus emission hook)
2. browser/src/primitives/keyboard/useKeyboardTheme.ts (new — theme subscription hook)
3. Updated: browser/src/primitives/keyboard/SCKeyboard.tsx (wire bus + theme)
4. Updated: browser/src/apps/keyboardAdapter.tsx (pass bus)
5. Updated: browser/src/shell/constants.ts (APP_REGISTRY bus patterns)
6. browser/src/primitives/keyboard/__tests__/keyboardBus.test.ts
7. browser/src/primitives/keyboard/__tests__/keyboardTheme.test.ts

## Acceptance Criteria
- [ ] Every keypress emits a `keystroke` event on relay_bus with correct key + modifiers
- [ ] Buffer submit emits `buffer:submit` with buffer text
- [ ] Fn-layer actions emit as `fn:action_id` keystroke events
- [ ] RTD events fire on state change (orientation, fn-lock, sound, brightness, accent)
- [ ] RTD events do NOT fire on timer — only on change
- [ ] Theme accent overrides local accent (Fn+F3 cycles local, theme reset restores)
- [ ] `sd:hhpanes_mode = dark` → backlit rendering (glow, dark caps)
- [ ] `sd:hhpanes_mode = light` → glass rendering (frosted blur, no glow)
- [ ] No toggle for dark/glass anywhere in the component
- [ ] High contrast mode: max brightness, no blur, solid borders
- [ ] Font variables respected (--font-mono, --font-sans)
- [ ] All console.log stubs from Wave A replaced with real bus emissions
- [ ] 8OS command palette fires `command_palette:open` on bus
- [ ] Escape fires `escape_protocol` on bus
- [ ] Bus null-safe: component renders and functions without bus
- [ ] All tests pass (minimum 10 tests)
- [ ] Build passes with `npx vite build`

## Smoke Test
- [ ] `npx vitest run browser/src/primitives/keyboard/__tests__/keyboardBus.test.ts` — all tests pass
- [ ] `npx vitest run browser/src/primitives/keyboard/__tests__/keyboardTheme.test.ts` — all tests pass
- [ ] `npx vite build` — zero errors

## Response File
20260328-KB-001B-RESPONSE.md
