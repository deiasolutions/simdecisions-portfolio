# Mobile Shmup Touch Controls: UX Recommendation Document

**Research Date:** 2026-04-08
**Research Scope:** Mobile vertical scrolling shoot-em-up controls
**Target Platform:** Responsive HTML5 game (PC + Mobile)

---

## Executive Summary

Based on analysis of top mobile shmups including Sky Force Reloaded, Raiden Legacy, DoDonPachi Resurrection, and Phoenix 2, this document recommends a **hybrid direct-touch + floating control scheme** with auto-fire enabled and customizable sensitivity settings. This approach balances accessibility for casual players with precision for hardcore shmup enthusiasts.

---

## 1. Control Schemes in Popular Mobile Shmups

### Sky Force Reloaded
- **Control Method:** Direct swipe-to-move
- **Ship Movement:** 1:1 finger tracking across entire screen
- **Shooting:** Auto-fire (always on)
- **Special Abilities:** Dedicated virtual buttons on screen edges
- **Key Insight:** Smooth, responsive finger tracking with no virtual joystick

**Source:** [Sky Force Reloaded (TouchArcade)](https://toucharcade.com/2009/03/05/sky-force-reloaded-a-great-099-vertical-shoot-em-up/)

### Raiden Legacy
- **Control Modes:** Two modes—"Fast Touch" and "Arcade Touch"
  - Fast Touch: Smooth 1:1 tracking at 120%, 150%, or 200% speed
  - Arcade Touch: Matches original arcade speed and "choppiness"
- **Ship Movement:** Drag anywhere on screen; ship follows 1:1
- **Button Customization:** Fire and bomb buttons are repositionable
- **Key Insight:** Multiple speed modes let players tune responsiveness to preference

**Sources:**
- [Raiden Legacy (App Store)](https://apps.apple.com/us/app/raiden-legacy/id537280156)
- [Raiden Legacy Review (148 Apps)](https://www.148apps.com/raiden-legacy/raiden-legacy-review/)

### DoDonPachi Resurrection
- **Control Method:** Slide controls optimized for index finger
- **Touch Zone:** Bottom 20-25% of screen reserved for movement input
- **Shooting:** Auto-fire enabled by default
- **Mode Switching:** Virtual thumb buttons on screen edges to toggle shot types
- **Key Insight:** Bottom-zone input prevents finger obscuring bullets; highly precise

**Source:** [DoDonPachi Resurrection (App Store)](https://apps.apple.com/us/app/dodonpachi-resurrection-hd/id488666118)

### Phoenix 2
- **Control Method:** Direct touch-and-drag
- **Shooting:** Continuous auto-fire
- **Special Abilities:** Gesture-based (swipe patterns for bombs)
- **Key Insight:** Minimal UI; entire screen is playable area

**Source:** [Best Shoot-Em-Up Games (TouchArcade)](https://toucharcade.com/2022/09/02/best-shoot-em-up-games-iphone-android-list-top-shmups-2022/)

### Geometry Wars (Dual-Stick Reference)
- **Control Method:** Virtual dual-stick (left for movement, right for aim)
- **Shooting:** Automatic when right stick is engaged
- **Key Insight:** Dual-stick works for twin-stick shooters but NOT for vertical shmups

---

## 2. Touch Input Patterns: Analysis

### Direct Touch (Finger Position = Ship Position)
**Pros:**
- No learning curve—intuitive for all players
- Precise 1:1 control
- No UI occlusion from virtual joystick

**Cons:**
- Finger obscures playfield (especially bottom center)
- Requires full-screen drag for edge-to-edge movement
- Hand fatigue on large screens

**Best For:** Vertical shmups with auto-fire

### Floating Virtual Joystick
**Pros:**
- Adapts to where player places finger
- Reduces hand fatigue (no need to reach fixed position)
- Visual feedback shows input direction

**Cons:**
- Takes up screen real estate
- Less precise than direct touch
- Players can lose reference point mid-action

**Best For:** Games where muscle memory isn't critical

**Sources:**
- [Floating vs Fixed Joystick (Medium)](https://medium.com/@yi_zhang1/ui-critique-2-virtual-joystick-of-mobile-games-7fd4b233c066)
- [Virtual Joysticks (Unity Discussions)](https://discussions.unity.com/t/opinions-wanted-why-are-joystick-controls-so-terrible-on-mobile/640042)

### Fixed Virtual Joystick
**Pros:**
- Consistent positioning builds muscle memory
- Competitive players prefer it

**Cons:**
- Players must reach specific screen area
- Finger can miss joystick in intense moments
- No tactile feedback (unlike physical controller)

**Best For:** Competitive or precision-focused games

### Drag-to-Move (Relative Movement)
**Pros:**
- Start drag anywhere—no fixed zone
- Ship moves relative to drag direction
- Minimal finger repositioning

**Cons:**
- Less intuitive than direct touch
- Requires calibration for sensitivity

**Best For:** One-handed play

### Tilt Controls (Accelerometer)
**Pros:**
- Keeps fingers off screen
- Novelty factor

**Cons:**
- Imprecise for bullet-hell dodging
- Fatiguing for long sessions
- Doesn't work when lying down

**Best For:** Casual modes or accessibility option

**Source:** [Tilt-Touch Synergy (York University)](https://www.yorku.ca/mack/ec2017.html)

---

## 3. Auto-Fire vs. Manual Shooting

### Auto-Fire (Recommended for Mobile Shmups)
- **UX Benefit:** Reduces cognitive load—players focus on dodging
- **Implementation:** Continuous fire when finger touches screen
- **Used By:** DoDonPachi, Sky Force, Phoenix 2

**Source:** [Mobile Shooting Controls Guide](https://adroittechstudios.com/how-to-make-mobile-shooting-controls-fun/)

### Manual Fire
- **UX Benefit:** Preserves hardcore arcade feel
- **Implementation:** Dedicated fire button (right thumb)
- **Used By:** Raiden Legacy (optional mode)

### Hybrid Approach (Recommended)
- **Default:** Auto-fire ON
- **Settings Toggle:** Advanced players can enable manual fire
- **Fire Button:** Positioned in right thumb zone (if manual enabled)

### Power-Ups and Abilities
- **Bomb Button:** Large (88×88px minimum), positioned in right thumb zone
- **Visual Feedback:** Highlight on press, vibration on activation
- **Cooldown Indicator:** Circular progress ring around button

---

## 4. Screen Real Estate and Touch Zones

### Thumb Reach Zones (Based on UX Research)

```
┌─────────────────────────────┐
│   🔴 RED ZONE (Hard Reach)  │  ← Top 15% of screen
├─────────────────────────────┤
│                             │
│  🟡 YELLOW ZONE (Stretch)   │  ← Middle 50% of screen
│                             │
├─────────────────────────────┤
│  🟢 GREEN ZONE (Easy Reach) │  ← Bottom 35% of screen
└─────────────────────────────┘
```

**Key Statistics:**
- 75% of mobile touches are made with the thumb
- 67% of users are right-handed
- Minimum touch target: 44×44 CSS pixels
- Recommended touch target: 48×48 CSS pixels
- Minimum spacing between targets: 8px

**Sources:**
- [Thumb Zone UX Guide (Parachute Design)](https://parachutedesign.ca/blog/thumb-zone-ux/)
- [The Thumb Zone (Smashing Magazine)](https://www.smashingmagazine.com/2016/09/the-thumb-zone-designing-for-mobile-users/)
- [Mobile App UX: Thumb Zones (Elaris Software)](https://elaris.software/blog/mobile-ux-thumb-zones-2025/)

### Recommended Touch Zone Layout (Portrait Mode)

```
┌─────────────────────────────┐
│     PLAYFIELD (bullets,     │
│      enemies, ship)         │  ← 75% of screen height
│                             │
│                             │
├─────────────────────────────┤
│  [Movement Touch Zone]      │  ← 25% bottom (green zone)
│  Player taps/drags here     │
│                             │
│  [Bomb]          [Pause]    │  ← Right-side buttons
└─────────────────────────────┘
```

**Dimensions (Based on 375×667px iPhone SE baseline):**
- **Movement Zone:** Full width, bottom 167px (25%)
- **Bomb Button:** 88×88px, positioned at X: 270px, Y: 550px (right thumb zone)
- **Pause Button:** 64×64px, positioned at X: 300px, Y: 20px (top-right)

### Recommended Touch Zone Layout (Landscape Mode)

```
┌──────────────────────────────────────────────┐
│            PLAYFIELD (bullets,               │
│             enemies, ship)                   │
│                                              │
│                         [Bomb]    [Pause]    │ ← Right edge buttons
│                          88×88     64×64     │
│                                              │
│  [Movement Zone]                             │
│  Left 40% of screen                          │
└──────────────────────────────────────────────┘
```

**Dimensions (Based on 667×375px landscape):**
- **Movement Zone:** Left 267px (40%), full height
- **Bomb Button:** 88×88px, positioned at X: 540px, Y: 250px (right thumb)
- **Pause Button:** 64×64px, positioned at X: 590px, Y: 20px (top-right corner)

---

## 5. Accessibility and Comfort

### Hand Fatigue Considerations
- **One-Handed Mode:** Ship control on left OR right (user preference)
- **Two-Handed Mode:** Movement on left, abilities on right (default)
- **Resting Position:** Bottom 25% of screen minimizes arm strain

**Source:** [Mobile Game Ergonomics (OpenAccess CMS)](https://openaccess-api.cms-conferences.org/articles/download/978-1-958651-72-8_0)

### Visual Indicators
- **Touch Zone Highlight:** Semi-transparent overlay (30% opacity) when finger touches
- **Ship Tether Line:** Dotted line from finger to ship (shows 1:1 relationship)
- **Directional Indicator:** Arrow showing current movement direction

### Haptic Feedback Patterns
- **Ship Hit:** Sharp, quick vibration (50ms, strong intensity)
- **Bomb Activation:** Sustained rumble (200ms, medium intensity)
- **Power-Up Collect:** Light pulse (30ms, light intensity)
- **Boss Spawn:** Three quick pulses (100ms each, medium intensity)

**Sources:**
- [Haptic Feedback in Shooter Games (ACM)](https://dl.acm.org/doi/fullHtml/10.1145/3552327.3552333)
- [Mobile Gaming Haptics (Interhaptics)](https://interhaptics.medium.com/mobile-gaming-ux-how-haptic-feedback-can-change-the-game-3ef689f889bc)

---

## 6. Recommended Control Scheme for RAIDEN Clone

### Primary Control Method: **Hybrid Direct Touch + Floating Anchor**

#### How It Works:
1. **Player taps anywhere in bottom 25% of screen**
2. **Ship immediately moves to finger position** (direct touch)
3. **If finger drags outside movement zone**, a floating joystick appears at last valid position
4. **Ship continues to follow finger within screen bounds** (1:1 tracking)
5. **When finger lifts**, ship stops (no momentum)

#### Why This Works:
- Combines **precision of direct touch** with **comfort of floating joystick**
- No fixed position—works for left-handed and right-handed players
- Finger starts in green zone (easy reach), ship follows precisely

### Auto-Fire: **Enabled by Default**
- Continuous fire while finger is on screen
- Optional manual fire mode in settings (hardcore mode)

### Ability Buttons:
- **Bomb:** 88×88px button in right thumb zone
- **Visuals:** Semi-transparent, glowing border, cooldown ring
- **Haptic:** Strong vibration on press

### Sensitivity Settings:
- **Normal (1:1):** Ship position = finger position
- **Fast (1.5:1):** Ship moves 1.5× faster than finger (less drag needed)
- **Turbo (2:1):** Ship moves 2× faster (for edge-to-edge dodging)

---

## 7. Implementation Pattern (Technical)

### Touch Event Handling (JavaScript/TypeScript)

```javascript
// Pseudocode for hybrid direct touch control

let touchActive = false;
let shipPosition = { x: 0, y: 0 };
const MOVEMENT_ZONE_HEIGHT = window.innerHeight * 0.25; // Bottom 25%

// Touch start
canvas.addEventListener('touchstart', (e) => {
  const touch = e.touches[0];
  if (touch.clientY > (window.innerHeight - MOVEMENT_ZONE_HEIGHT)) {
    touchActive = true;
    updateShipPosition(touch.clientX, touch.clientY);
    startAutoFire();
  }
});

// Touch move
canvas.addEventListener('touchmove', (e) => {
  if (!touchActive) return;
  const touch = e.touches[0];
  updateShipPosition(touch.clientX, touch.clientY);
});

// Touch end
canvas.addEventListener('touchend', () => {
  touchActive = false;
  stopAutoFire();
});

// Update ship position (1:1 tracking with screen bounds)
function updateShipPosition(touchX, touchY) {
  // Map touch coordinates to playfield coordinates
  shipPosition.x = clamp(touchX, SHIP_WIDTH / 2, canvas.width - SHIP_WIDTH / 2);
  shipPosition.y = clamp(touchY, SHIP_HEIGHT / 2, canvas.height - SHIP_HEIGHT / 2);

  // Apply sensitivity multiplier (user setting)
  const sensitivity = getUserSensitivity(); // 1.0, 1.5, or 2.0
  shipPosition.x *= sensitivity;
  shipPosition.y *= sensitivity;

  // Smooth movement (lerp for natural feel)
  shipPosition.x = lerp(currentShipX, shipPosition.x, 0.15);
  shipPosition.y = lerp(currentShipY, shipPosition.y, 0.15);
}
```

### Multi-Touch Handling
- **Ignore secondary touches** (prevent accidental inputs)
- **Track first touch only** (primary movement finger)
- **Bomb button** uses separate touch target (doesn't interfere with movement)

### Input Smoothing
- **Lerp (Linear Interpolation):** Smooth ship movement by 15% per frame
- **Prevents jitter** from touch sampling rate variations
- **Formula:** `newPos = currentPos + (targetPos - currentPos) * 0.15`

### Touch Latency Optimization
- **Use `touchstart` immediately** (don't wait for `click` events)
- **Prevent default** to avoid 300ms tap delay: `e.preventDefault()`
- **Passive listeners** for scroll performance: `{ passive: false }`

**Source:** [Mobile UX Design Examples (Eleken)](https://www.eleken.co/blog-posts/mobile-ux-design-examples)

---

## 8. Visual Design: Control Rendering

### Movement Zone Indicator (First-Time User)
- **On first play:** Show semi-transparent overlay highlighting bottom 25%
- **Text:** "Tap and drag here to move your ship"
- **Duration:** Fade out after 3 seconds or first touch

### Virtual Joystick (If Finger Leaves Zone)
- **Visual:** Circular outer ring (120px diameter), inner knob (60px diameter)
- **Color:** Semi-transparent white (40% opacity)
- **Position:** Appears at last valid touch position
- **Fades out** when finger lifts

### Bomb Button
- **Idle State:** Semi-transparent yellow circle (88×88px, 50% opacity)
- **Cooldown State:** Gray with circular progress ring
- **Active State:** Bright yellow glow, 100% opacity
- **Icon:** Bomb sprite centered (48×48px)

### Touch Feedback Ripple
- **On touch:** Expanding circle from touch point (SVG animation)
- **Color:** White with 60% opacity, fades out over 400ms
- **Max radius:** 60px

### Ship Tether Line (Optional Visual Aid)
- **Line from finger to ship:** Dotted, semi-transparent
- **Only shows** when ship position ≠ finger position (during lerp smoothing)
- **Helps players** understand indirect control

---

## 9. Performance Considerations

### Touch Sampling Rate
- Mobile devices: 60-120 Hz touch sampling
- **Recommendation:** Poll touch input every frame (requestAnimationFrame)
- **Avoid:** Throttling or debouncing (adds latency)

### Canvas Optimization
- Use **hardware-accelerated canvas** (translate3d for ship rendering)
- **Batch draw calls** for bullets/enemies
- **Offscreen canvas** for static background layers

### Battery Impact
- Haptic feedback adds ~5-10% battery drain
- **Recommendation:** Make haptics optional in settings
- **Default:** Haptics ON (better UX), with toggle to disable

---

## 10. User Preference Options

### Control Settings Menu
```
┌─────────────────────────────────────┐
│  CONTROL SETTINGS                   │
├─────────────────────────────────────┤
│  [ ] Auto-Fire (ON / OFF)           │
│  [ ] Sensitivity (Normal/Fast/Turbo)│
│  [ ] Haptic Feedback (ON / OFF)     │
│  [ ] Tilt Controls (ON / OFF)       │
│  [ ] Show Touch Zone Hints (ON/OFF) │
│  [ ] Button Size (Small/Med/Large)  │
│  [ ] One-Handed Mode (Left/Right)   │
└─────────────────────────────────────┘
```

### Sensitivity Slider
- **Normal (1.0×):** Default 1:1 tracking
- **Fast (1.5×):** Ship moves 50% faster than finger
- **Turbo (2.0×):** Ship moves 2× faster (for pros)

### Button Size Presets
- **Small:** 64×64px (for large screens, advanced players)
- **Medium:** 88×88px (default, recommended)
- **Large:** 112×112px (for accessibility, older players)

### One-Handed Mode
- **Left-Handed:** Movement zone on left 40%, bomb button on left
- **Right-Handed:** Movement zone on right 40%, bomb button on right
- **Two-Handed (Default):** Full-width movement zone, bomb on right

---

## 11. Portrait vs. Landscape Considerations

### Portrait Mode (Recommended for Vertical Shmup)
- **Playfield:** Vertical scrolling feels natural
- **Movement Zone:** Bottom 25% (green thumb zone)
- **Pros:** Matches classic arcade orientation, one-handed play possible
- **Cons:** Smaller horizontal playfield

### Landscape Mode
- **Playfield:** Wider view, see more enemies
- **Movement Zone:** Left 40% of screen
- **Pros:** More screen real estate, two-handed grip
- **Cons:** Harder to hold for long sessions, finger obscures more

### Recommendation
- **Default:** Portrait mode (lock orientation)
- **Optional:** Landscape support for tablets
- **Auto-rotate:** OFF (prevents accidental orientation changes mid-game)

---

## 12. Fallback Options for Accessibility

### Tilt Toggle
- **When Enabled:** Ship moves based on device tilt (X-axis only)
- **Sensitivity:** Adjustable (low/medium/high)
- **Use Case:** Players with limited dexterity

### Voice Control (Advanced)
- **Commands:** "Left", "Right", "Bomb"
- **Use Case:** Accessibility for motor-impaired players
- **Implementation:** Web Speech API (if supported)

### External Controller Support
- **Gamepad API:** Detect Xbox/PlayStation controllers
- **Mapping:** Left stick = movement, A button = bomb
- **Use Case:** Desktop or tablet with Bluetooth controller

---

## Final Recommendations Summary

### ✅ Recommended Control Scheme
- **Primary Input:** Hybrid direct touch (1:1 tracking) + floating anchor fallback
- **Touch Zone:** Bottom 25% of screen (green thumb zone)
- **Auto-Fire:** Enabled by default, optional manual mode
- **Sensitivity:** 3 presets (Normal 1×, Fast 1.5×, Turbo 2×)
- **Bomb Button:** 88×88px, right thumb zone, haptic feedback
- **Orientation:** Portrait (locked), landscape optional

### ✅ Implementation Priorities
1. **Core touch handling:** Direct touch with lerp smoothing
2. **Auto-fire:** Continuous fire while touching screen
3. **Bomb button:** Large, responsive, with cooldown visual
4. **Haptic feedback:** Ship hit, bomb activation, power-ups
5. **Settings menu:** Sensitivity, haptics toggle, button size

### ✅ Visual Indicators
- Touch zone overlay (first-time users)
- Touch feedback ripple
- Bomb button cooldown ring
- Optional ship tether line

### ✅ Accessibility
- One-handed mode (left/right)
- Adjustable button sizes
- Optional tilt controls
- Haptics toggle (battery saving)

---

## Research Sources

- [Sky Force Reloaded Review (TouchArcade)](https://toucharcade.com/2009/03/05/sky-force-reloaded-a-great-099-vertical-shoot-em-up/)
- [Raiden Legacy (App Store)](https://apps.apple.com/us/app/raiden-legacy/id537280156)
- [DoDonPachi Resurrection (App Store)](https://apps.apple.com/us/app/dodonpachi-resurrection-hd/id488666118)
- [Best Shoot-Em-Up Games (TouchArcade)](https://toucharcade.com/2022/09/02/best-shoot-em-up-games-iphone-android-list-top-shmups-2022/)
- [Thumb Zone UX Guide (Parachute Design)](https://parachutedesign.ca/blog/thumb-zone-ux/)
- [The Thumb Zone (Smashing Magazine)](https://www.smashingmagazine.com/2016/09/the-thumb-zone-designing-for-mobile-users/)
- [Mobile App UX: Thumb Zones (Elaris Software)](https://elaris.software/blog/mobile-ux-thumb-zones-2025/)
- [Virtual Joystick UI Critique (Medium)](https://medium.com/@yi_zhang1/ui-critique-2-virtual-joystick-of-mobile-games-7fd4b233c066)
- [Mobile Shooting Controls Guide](https://adroittechstudios.com/how-to-make-mobile-shooting-controls-fun/)
- [Tilt-Touch Synergy (York University)](https://www.yorku.ca/mack/ec2017.html)
- [Haptic Feedback in Shooters (ACM)](https://dl.acm.org/doi/fullHtml/10.1145/3552327.3552333)
- [Mobile Gaming Haptics (Interhaptics)](https://interhaptics.medium.com/mobile-gaming-ux-how-haptic-feedback-can-change-the-game-3ef689f889bc)
- [Mobile Game Ergonomics (CMS Conferences)](https://openaccess-api.cms-conferences.org/articles/download/978-1-958651-72-8_0)
- [Mobile UX Design Examples (Eleken)](https://www.eleken.co/blog-posts/mobile-ux-design-examples)
- [Floating vs Fixed Joystick Comparison (Unity)](https://discussions.unity.com/t/opinions-wanted-why-are-joystick-controls-so-terrible-on-mobile/640042)

---

**END OF DOCUMENT**
