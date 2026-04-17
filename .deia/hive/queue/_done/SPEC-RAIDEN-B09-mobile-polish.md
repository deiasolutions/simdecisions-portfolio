---
id: RAIDEN-B09
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-B08]
---
# SPEC-RAIDEN-B09: Mobile Polish and Performance Tuning

## Priority
P1

## Model Assignment
sonnet

## Role
bee (b33 — you write code and tests)

## Depends On
- RAIDEN-B08 (AI system)

## Objective
Optimize for mobile devices: responsive layout, touch controls refinement, performance tuning, and battery efficiency.

## You are in EXECUTE mode
Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.

## Design Reference
Read:
- `.deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md` (Section 9: Controls, Section 14: Performance Targets)
- `.deia/hive/responses/20260413-RAIDEN-R02-MOBILE-CONTROLS-RESEARCH.md` (mobile UX best practices)

## Deliverables

### File: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\public\games\raiden-v1-20260413.html`

**Polish and optimize:**

1. **Responsive Layout**
   - Detect screen size: `window.innerWidth < 768` = mobile
   - Canvas scaling: Maintain 4:3 aspect ratio, fit to viewport
   - Orientation: Portrait mode (vertical shmup works best in portrait)
   - Orientation lock suggestion: Show message "Rotate device to portrait" if landscape on mobile

2. **Touch Controls Refinement (from R02 research)**
   - Virtual joystick (bottom-left):
     - Fixed position (not floating)
     - Size: 120px diameter (15% of screen width)
     - Dead zone: 10px
     - Visual feedback: Glow when active, opacity 0.6 → 1.0
     - Smooth movement: Interpolate player velocity based on joystick distance from center
   - Bomb button (bottom-right):
     - Size: 80px diameter
     - Glowing red icon
     - Cooldown overlay (gray out when on cooldown)
   - Prevent page scroll when touching game area: `event.preventDefault()` on touch events

3. **HUD Adjustments for Mobile**
   - Top bar: Compress score, level, lives into smaller font (fit on narrow screen)
   - Bottom bar: Weapon/bomb info in top corners (don't overlap with virtual controls)
   - Safe zones: Don't render game entities under virtual controls (player can't see them)

4. **Performance Optimization**
   - Target: 60fps on desktop, 30fps minimum on mobile
   - Entity pooling: Reuse objects, avoid `new` in game loop
   - Particle limits: Max 100 particles on mobile (vs 200 on desktop)
   - Sprite batching: Group draw calls by color (reduce canvas state changes)
   - Reduce physics precision on mobile: Skip collision checks for distant entities

5. **Battery Efficiency**
   - Detect mobile: Use lower framerate (30fps) when battery < 20% (Battery API if available)
   - Reduce particle effects on low-end devices (detect performance, disable glow if FPS < 30)
   - Pause game when tab loses focus: `document.addEventListener('visibilitychange', ...)`

6. **Haptic Feedback (Mobile)**
   - Vibrate on hit: `navigator.vibrate(100)` when player takes damage
   - Vibrate on bomb: `navigator.vibrate(200)` when bomb activated
   - Vibrate on level complete: `navigator.vibrate([100, 50, 100])` (pattern)
   - Settings toggle: Enable/disable vibration

7. **Fullscreen Mode (Mobile)**
   - Button in menu: "Fullscreen" (request fullscreen on tap)
   - Use Fullscreen API: `canvas.requestFullscreen()`
   - Exit fullscreen: Double-tap canvas or back button

8. **Device Testing**
   - Test on: Chrome mobile, Safari iOS, Firefox Android
   - Ensure touch events work (not just mouse events)
   - Check performance on mid-range device (not just flagship)

## Technical Constraints
- Use `window.devicePixelRatio` for crisp rendering on Retina displays
- Touch event polyfill: Handle both touch and mouse events (for hybrid devices)
- Graceful degradation: If Battery API not supported, skip battery optimization
- Fullscreen API: Check `document.fullscreenEnabled` before requesting

## Acceptance Criteria
- [ ] Game scales correctly on mobile (portrait mode, 4:3 aspect)
- [ ] Virtual joystick works smoothly (no lag, no stuttering)
- [ ] Bomb button works on tap
- [ ] HUD readable on small screens (compressed but legible)
- [ ] 30fps minimum on mid-range mobile device
- [ ] Particle count reduced on mobile (100 max)
- [ ] Haptic feedback on hit, bomb, level complete
- [ ] Fullscreen mode works (button in menu)
- [ ] Game pauses when tab loses focus
- [ ] No page scroll when touching game area
- [ ] No errors in console on mobile browsers

## Tests (Manual Smoke Tests)
**Desktop tests:**
```javascript
// 1. Resize browser to <768px width, see mobile layout
// 2. Virtual joystick and bomb button appear
// 3. Use mouse to drag joystick, player moves
```

**Mobile tests (test on actual device):**
```javascript
// 1. Open game on phone (Chrome/Safari)
// 2. See virtual joystick (bottom-left) and bomb button (bottom-right)
// 3. Drag joystick, player moves smoothly (no lag)
// 4. Tap bomb button, bomb activates
// 5. Take damage, phone vibrates (if vibration enabled in settings)
// 6. Complete level, phone vibrates (pattern)
// 7. Tap fullscreen button, game goes fullscreen
// 8. Check FPS (should be 30+ on mid-range device)
// 9. Switch tabs, game pauses automatically
// 10. Touch game area, page doesn't scroll
```

## Smoke Test
```bash
grep -q "joystick" "browser/public/games/raiden-v1-20260413.html" && \
grep -q "vibrate" "browser/public/games/raiden-v1-20260413.html" && \
grep -q "requestFullscreen" "browser/public/games/raiden-v1-20260413.html" && \
echo "PASS"
```

## Response Location
`.deia/hive/responses/20260413-RAIDEN-B09-MOBILE-POLISH-RESPONSE.md`

## Notes
- Mobile is a first-class platform (not an afterthought).
- Touch controls must feel responsive (users are very sensitive to lag).
- Performance on mid-range devices is critical (don't optimize only for flagships).
- Next spec (B10) is final integration and E2E testing.
