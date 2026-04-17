---
id: RAIDEN-109
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-102, RAIDEN-R02]
---
# SPEC-RAIDEN-109: Mobile Polish & Performance

## Priority
P1

## Model Assignment
sonnet

## Role
bee (builder)

## Depends On
- RAIDEN-102 (player controls — touch already implemented)
- RAIDEN-R02 (mobile controls research)

## Objective
Polish the mobile experience: responsive layout, touch control refinements, performance tuning for 60fps on mobile, tilt controls option.

## Context
Touch controls were implemented in RAIDEN-102, but need polish based on RAIDEN-R02 research. This spec optimizes for mobile performance and adds optional tilt controls.

## Technical Requirements

### Responsive Layout
- Detect screen size (portrait vs landscape)
- Portrait mode: game canvas scales vertically, UI adjusts
- Landscape mode: game canvas scales horizontally
- Touch zones adapt to screen size (larger buttons on phones, smaller on tablets)

### Touch Control Refinements
Based on RAIDEN-R02 research:
- **Joystick sensitivity:** Configurable (low/medium/high in settings)
- **Joystick deadzone:** Small deadzone to prevent drift
- **Joystick visual feedback:** Smooth interpolation (not instant snap)
- **Bomb button size:** Larger on phones (80px), smaller on tablets (60px)
- **Haptic feedback:** Vibrate on shoot, hit, bomb (if supported)

### Tilt Controls (Optional)
- Toggle tilt mode in settings
- Use DeviceOrientationEvent (gamma = left/right, beta = up/down)
- Tilt sensitivity configurable (low/medium/high)
- Calibrate button (sets current orientation as neutral)
- Visual indicator: tilt mode active

### Performance Tuning
Target: 60fps on iPhone 12 / Pixel 5 equivalent

Optimizations:
- Reduce particle count on mobile (10 vs 50 on PC)
- Lower entity pool sizes (fewer bullets/enemies active)
- Simplify rendering (no glow effects on low-end devices)
- Detect device performance tier (use `navigator.hardwareConcurrency`)
- Auto-adjust quality settings (low/medium/high)

### Settings Menu
- Volume slider
- Mute toggle
- Control scheme: Touch Joystick / Tilt Controls
- Joystick sensitivity: Low / Medium / High
- Tilt sensitivity: Low / Medium / High
- Graphics quality: Low / Medium / High (auto-detected)

### PWA Features (Progressive Web App)
- Add manifest.json (metadata for "Add to Home Screen")
- Icon set (192x192, 512x512 — simple colored shapes, inline SVG converted to data URLs)
- Fullscreen mode on launch (standalone display mode)
- Offline support (service worker caches HTML file)

## Deliverable
Update file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\games\raiden-v1-20260408.html`

Add sections:
- `// ===== MOBILE POLISH =====`
- `// ===== TILT CONTROLS =====`
- `// ===== PERFORMANCE TUNING =====`
- `// ===== SETTINGS MENU =====`
- `// ===== PWA FEATURES =====`

Also create inline (within HTML file):
- Service worker script (in separate `<script>` tag)
- Manifest JSON (in `<script type="application/json">` tag)

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- 60fps on mid-range mobile devices (2020+)
- Controls feel responsive (no input lag)
- Tilt controls are smooth (not jittery)

## Acceptance Criteria
- [ ] Responsive layout (portrait and landscape modes)
- [ ] Touch joystick sensitivity configurable
- [ ] Joystick deadzone prevents drift
- [ ] Bomb button size adapts to screen size
- [ ] Haptic feedback on shoot/hit/bomb (if supported)
- [ ] Tilt controls implemented (toggle in settings)
- [ ] Tilt calibration button
- [ ] Performance tuning (60fps on mobile)
- [ ] Quality settings (low/medium/high, auto-detected)
- [ ] Settings menu (volume, mute, controls, quality)
- [ ] PWA manifest and service worker
- [ ] "Add to Home Screen" works on iOS/Android
- [ ] Smoke test: play on mobile, 60fps, controls responsive

## Smoke Test
```bash
# Manual: Open on mobile device (or Chrome DevTools device emulation)
# - Touch joystick works (move ship smoothly)
# - Bomb button tappable (not too small)
# - Switch to tilt mode → tilt device → ship moves
# - Calibrate tilt → works from new neutral position
# - Check FPS counter (should be ~60)
# - Add to home screen → launch → fullscreen mode
# - Airplane mode → game still loads (cached)
```

## Tests
Write inline tests:
- Joystick deadzone (input < threshold = no movement)
- Tilt angle mapping (gamma 0-45° = movement 0-1)
- Performance tier detection (low/medium/high based on hardwareConcurrency)
- Service worker caching (fetch event returns cached HTML)

## Response Location
`.deia/hive/responses/20260408-RAIDEN-109-RESPONSE.md`
