# Mobile Shmup Controls Research

## 1. Recommended Control Scheme
**Primary Recommendation:** Floating joystick + auto-fire + bomb button

**Rationale:**
Modern mobile shmups have converged on auto-fire as the standard to reduce cognitive load and allow players to focus on positioning and dodging. Research shows that while competitive players prefer manual fire for some genres, vertical shmups benefit from auto-fire because the core challenge is dodging bullet patterns, not aiming. Floating joysticks accommodate different hand sizes and grip styles better than fixed joysticks, providing better ergonomics and less UI clutter while maintaining predictable control.

**Layout:**
```
┌─────────────────────────────┐
│  ╔═══╗   SCORE: 12500  ❤❤❤ │ ← Top safe zone (HUD)
│  ║ ⚡ ║   BOMB: ●●○       │
│  ╚═══╝                      │
│                             │
│                             │
│         [Enemy Area]        │
│                             │
│           ✈️                │ ← Player ship (auto-fires)
│        [Bullets]            │
│                             │
│                             │
│   ◉                    ◉    │ ← Bottom safe zone (controls)
│  Joystick            Bomb   │
│  (floating)        (fixed)  │
│  Left 20%          Right 15%│
└─────────────────────────────┘

Portrait orientation
Safe zones: Top 10%, Bottom 15%
Joystick active area: Left 50% of screen
Bomb button: Fixed position bottom-right
```

## 2. Virtual Joystick Specs

- **Type:** Floating (appears where thumb touches, re-centers on release)
- **Position:** Appears anywhere in left 50% of screen below top safe zone
- **Size:** 120px diameter base (15-18% of typical phone screen width)
- **Max Radius:** 60px from center (thumb can drift beyond, output clamped)
- **Dead Zone:** 8px center (13% of radius) to prevent drift
- **Visual Feedback:**
  - Base: Opacity 0.5 default, 0.8 when active
  - Stick: Opacity 0.7 default, 1.0 when active
  - Glow effect on movement (subtle white radial gradient)
  - Disappears 0.3s after touch release
- **Active Area:** Left 50% of screen only (prevents conflict with bomb button)
- **Examples:**
  - Sky Force series uses floating joystick with auto-fire, placing controls where the thumb touches[^1]
  - Research shows floating joysticks are preferred for ergonomics and accommodate different handedness[^2]

[^1]: [Sky Force Reloaded Gameplay](https://sky-force-reloaded-2016.fandom.com/wiki/Game_Play)
[^2]: [Best Virtual Joystick Design](https://medium.com/@renatocassino/i-built-the-best-virtual-joystick-for-phaserjs-then-went-to-bed-ab4ac09d1265)

## 3. Fire Control Decision

- **Auto-Fire:** YES
- **Rationale:**
  - Auto-fire is standard in modern mobile shmups (Sky Force, Phoenix HD)[^3]
  - Research shows auto-fire helps players focus on movement and dodging rather than button management[^4]
  - In vertical shmups, the challenge is positioning and pattern recognition, not aiming accuracy
  - Reduces finger fatigue on touchscreens (no constant tapping)
  - Frees up screen real estate (no fire button needed)
  - For advanced players: could offer optional manual fire toggle in settings, but default to auto-fire

[^3]: [Sky Force Touch Controls](https://toucharcade.com/2014/07/01/sky-force-2014-review/)
[^4]: [Auto-Fire Best Practices](https://www.epicgames.com/fortnite/en-US/news/getting-started---fortnite-for-mobile)

## 4. Bomb Button Specs

- **Position:** Bottom-right corner, 15% from right edge, 12% from bottom edge
- **Size:** 80px diameter (larger than standard 48dp minimum for accessibility)[^5]
- **Touch Target:** 96px diameter (expanded invisible touch area)
- **Visual:**
  - Circular button with glowing bomb icon (⚡ or 💣)
  - Cooldown overlay: radial fill showing recharge progress
  - Stock counter: small badge showing remaining bombs (●●○ = 2/3)
  - Pulse animation when available
  - Dim to 40% opacity when depleted
- **Feedback:**
  - Screen shake (8px, 0.2s duration)
  - White flash overlay (0.1s)
  - Haptic vibration (if supported, 100ms strong)
  - Sound effect
- **Placement Rationale:**
  - Bottom-right prevents accidental activation while using left joystick
  - Positioned in safe zone away from system gesture areas
  - Research shows bombs should be less accessible than primary fire to prevent accidental use[^6]

[^5]: [Material Design Touch Targets](https://support.google.com/accessibility/android/answer/7101858)
[^6]: [Shmup Button Layout Discussion](https://shmups.system11.org/viewtopic.php?t=37081)

## 5. Orientation & Layout

- **Orientation:** Portrait (vertical orientation)
- **Rationale:**
  - Vertical shmups have traditionally used portrait orientation due to genre conventions and gameplay area requirements[^7]
  - 73% of top 100 mobile games use portrait orientation[^8]
  - Portrait allows full vertical scrolling space for enemy patterns
  - Better one-handed playability for casual sessions
  - Natural fit for vertical shoot-em-up gameplay (enemies descend from top)
- **HUD Layout:**
  - **Top Bar (10% of screen):** Score (left), Lives (right), Current Weapon/Power (center icon)
  - **Mid-Screen:** Minimal - only critical alerts (low health warning, powerup notifications as brief toasts)
  - **Bottom (15% of screen):** Control zone - joystick (left), bomb button (right)
  - **Safe Zones:**
    - Top: 10% reserved for notches/camera cutouts
    - Bottom: 15% reserved for gesture navigation areas
    - Sides: 5% padding to avoid rounded corners[^9]

[^7]: [Portrait Orientation for Vertical Shmups](https://en.wikipedia.org/wiki/Page_orientation)
[^8]: [App Store Orientation Statistics](https://www.storemaven.com/academy/app-store-gallery-orientation/)
[^9]: [Mobile Safe Areas Best Practices](https://cursa.app/en/page/mobile-screen-resolution-aspect-ratios-and-safe-areas)

## 6. Alternative: Tilt Controls

- **Viable:** YES (as optional setting)
- **Pros:**
  - No screen occlusion from virtual controls[^10]
  - More immersive "flight simulation" feel
  - Some players find it more engaging and challenging[^11]
  - No loss of tactile feedback compared to virtual joystick (proprioception compensates)
- **Cons:**
  - Significantly impairs precision aiming/dodging in tight bullet patterns[^10]
  - Requires calibration on app start
  - Uncomfortable in public settings (holding phone at angles)
  - Not viable for stationary play (lying down, phone on desk)
  - Lower player preference in competitive scenarios[^11]
  - Difficult to fine-tune for micro-movements
- **Recommendation:**
  - Include as **optional toggle** in settings menu
  - Default to virtual joystick
  - If implemented, use **tilt for movement only**, keep bomb button as touch
  - Provide sensitivity slider and calibration button
  - Add option for horizontal-only tilt (ignore vertical axis) for more comfortable play

[^10]: [Tilt vs Touch Performance Research](https://www.yorku.ca/mack/ec2017.html)
[^11]: [Tilt Control Study](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=3bd4ec7d6f548afc1c2f0d8377631142a997aa8b)

## 7. Performance Targets

- **Frame Rate:**
  - **Target:** 60fps (critical for smooth bullet dodging and responsive controls)
  - **Minimum:** 30fps on low-end devices (graceful degradation)
  - **Implementation:** Use requestAnimationFrame with delta time for frame-independent movement[^12]
- **Input Latency:**
  - **Target:** <16ms (one frame at 60fps, touch to visual response)
  - **Critical:** Touch events must be processed immediately, no debouncing
  - **Joystick:** Update player position every frame based on current touch state
- **Rendering:**
  - **Primary:** Canvas 2D with hardware acceleration
  - **Rationale:** Canvas 2D provides 60fps on mid-range devices with proper optimization[^13]
  - **Optimization Techniques:**
    - Offscreen canvas caching for static sprites (player ship, enemies, bullets)
    - Batch rendering for particles and bullets
    - GPU-accelerated drawImage operations
    - Limit expensive operations (text rendering, gradients) to cached elements[^14]
  - **WebGL:** Only if advanced particle effects or shader effects are critical (increases complexity and battery drain)
- **Battery Considerations:**
  - Limit particle effects on mobile (max 100 particles on screen)
  - Use sprite sheets to reduce draw calls
  - Pause rendering when app is backgrounded
  - Reduce frame rate to 30fps after 2 minutes of inactivity (battery saver mode)

[^12]: [HTML5 Canvas 60fps Optimization](https://dev.to/gamh5games/optimizing-html5-action-games-for-mobile-devices-19ce)
[^13]: [Canvas Performance Best Practices](https://docs.bswen.com/blog/2026-02-21-canvas-performance-optimization/)
[^14]: [Offscreen Canvas Caching](https://tnodes.medium.com/optimizing-my-javascript-canvas-game-pt-1-61de2ac51334)

## 8. Accessibility

- **Button Size:**
  - Minimum visible size: 80px diameter (bomb button)
  - Minimum touch target: 96px diameter (expanded invisible hit area)
  - Exceeds Material Design minimum of 48dp[^15]
  - Joystick base: 120px diameter (well above minimum)
- **Contrast:**
  - Controls must have 4.5:1 contrast ratio against game background
  - Use semi-transparent dark overlay behind controls if needed
  - White outlines on joystick and bomb button
  - High visibility against typical space/sky backgrounds
- **Customization:**
  - Settings option to scale UI (80%, 100%, 120%, 140%)
  - Opacity slider for joystick (30%-80% range)
  - Option to swap joystick/bomb button sides (left-handed mode)
  - Color-blind mode: Use icons/shapes, not just color for health/powerups
- **Haptic Feedback:**
  - Vibration on bomb activation (100ms strong pulse)
  - Light vibration on taking damage (50ms)
  - Settings toggle to disable vibration (battery/preference)
  - Use Web Vibration API where supported
- **Visual Feedback:**
  - Joystick movement shows directional response
  - Bomb button pulsates when ready
  - Screen flash on bomb activation
  - Damage indication: red screen edge vignette (color-blind safe)
- **Settings Persistence:**
  - Save all control preferences to localStorage
  - Reset to defaults button in settings
  - Tutorial on first launch showing control layout

[^15]: [Touch Target Accessibility Guidelines](https://support.google.com/accessibility/android/answer/7101858)

---

## Additional Research Notes

### Industry Examples
- **Sky Force Reloaded:** Uses floating touch controls with auto-fire, minimalist HUD, portrait orientation[^1]
- **Phoenix HD:** Similar control scheme, emphasizes visual clarity and minimal UI obstruction
- **Geometry Wars mobile:** Uses dual-stick shooter pattern (left stick move, right stick aim), but this is more suited to twin-stick shooters than vertical shmups

### Control Scheme Variations Considered
1. **Single floating joystick + auto-fire + bomb button** (RECOMMENDED)
2. **Dual-stick (move + aim):** Rejected - adds complexity, no aiming needed in vertical shmup
3. **Tap-to-move:** Rejected - poor precision for dodging tight bullet patterns
4. **Swipe gestures:** Rejected - occludes view, less precise than joystick

### Future Enhancements
- Bluetooth controller support (map joystick to D-pad/left stick, bomb to A/B button)
- Customizable button positions (drag-and-drop UI editor)
- Gesture shortcuts (swipe up = bomb, double-tap = pause)
- Training mode with on-screen control hints

---

## Sources

- [Sky Force Reloaded Gameplay Documentation](https://sky-force-reloaded-2016.fandom.com/wiki/Game_Play)
- [Best Virtual Joystick Design for PhaserJS](https://medium.com/@renatocassino/i-built-the-best-virtual-joystick-for-phaserjs-then-went-to-bed-ab4ac09d1265)
- [Sky Force 2014 Review - TouchArcade](https://toucharcade.com/2014/07/01/sky-force-2014-review/)
- [Fortnite Mobile Auto-Fire Guide](https://www.epicgames.com/fortnite/en-US/news/getting-started---fortnite-for-mobile)
- [Material Design Touch Target Guidelines](https://support.google.com/accessibility/android/answer/7101858)
- [Shmup Button Layout Discussion](https://shmups.system11.org/viewtopic.php?t=37081)
- [Portrait Orientation in Gaming - Wikipedia](https://en.wikipedia.org/wiki/Page_orientation)
- [App Store Gallery Orientation Best Practices](https://www.storemaven.com/academy/app-store-gallery-orientation/)
- [Mobile Safe Areas and Screen Resolution](https://cursa.app/en/page/mobile-screen-resolution-aspect-ratios-and-safe-areas)
- [Tilt-Touch Synergy Research](https://www.yorku.ca/mack/ec2017.html)
- [Performance of Tilt and Touch in Mobile Games (PDF)](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=3bd4ec7d6f548afc1c2f0d8377631142a997aa8b)
- [Optimizing HTML5 Action Games for Mobile](https://dev.to/gamh5games/optimizing-html5-action-games-for-mobile-devices-19ce)
- [Canvas Performance Optimization Guide](https://docs.bswen.com/blog/2026-02-21-canvas-performance-optimization/)
- [JavaScript Canvas Game Optimization](https://tnodes.medium.com/optimizing-my-javascript-canvas-game-pt-1-61de2ac51334)
- [Touch Target Accessibility for Android](https://support.google.com/accessibility/android/answer/7101858)
- [Mobile Game HUD Layout - Game UI Database](https://www.gameuidatabase.com/index.php?scrn=147)
- [Touch Control Design for Mobile Games](https://mobilefreetoplay.com/control-mechanics/)
- [Virtual Joystick UI Critique](https://medium.com/@yi_zhang1/ui-critique-2-virtual-joystick-of-mobile-games-7fd4b233c066)
