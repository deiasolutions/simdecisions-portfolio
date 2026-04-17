---
id: RAIDEN-R02
priority: P1
model: sonnet
role: bee
depends_on: []
---
# SPEC-RAIDEN-R02: Mobile Shmup Controls Research

## Priority
P1

## Model Assignment
sonnet

## Role
bee (b33 — you research and document findings)

## Depends On
(none)

## Objective
Research how top mobile shoot-em-up games handle touch controls and recommend the best UX pattern for our game.

## You are in EXECUTE mode
Write all research and documentation. Do NOT enter plan mode. Do NOT ask for approval. Just research and document.

## Research Scope

### 1. Virtual Joystick Patterns
Research and document:
- Fixed vs floating joystick (which is better for shmups?)
- Joystick size and dead zone recommendations
- Visual feedback (opacity, glow, vibration)
- Left-hand vs right-hand placement
- Examples: Sky Force, Phoenix HD, Geometry Wars mobile

### 2. Auto-Fire vs Manual Fire
Research and document:
- Do modern mobile shmups use auto-fire by default?
- If manual fire: where is the fire button? How big?
- Dual-stick shooter pattern (left stick move, right stick aim) vs single stick + auto-fire
- Player preference data if available

### 3. Special Weapon / Bomb Controls
Research and document:
- Where do mobile shmups place the bomb button?
- Tap vs hold mechanics
- Cooldown indicators
- Examples from top games

### 4. Tilt Controls (Optional)
Research and document:
- Are tilt controls viable for shmups?
- Pros/cons vs virtual joystick
- Calibration requirements
- Player adoption rates

### 5. UI Layout for Mobile
Research and document:
- How to fit HUD (score, lives, weapon indicator) on small screens
- Portrait vs landscape mode (which is standard for vertical shmups?)
- Safe zones for touch controls (avoid covering gameplay)
- Pause/menu button placement

### 6. Performance Considerations
Research and document:
- Touch input latency expectations (max acceptable lag)
- Frame rate targets for mobile (30fps vs 60fps)
- Canvas rendering vs WebGL for mobile browsers
- Battery drain concerns

## Deliverables

### File: `.deia/hive/responses/20260413-RAIDEN-R02-MOBILE-CONTROLS-RESEARCH.md`

Structure:
```markdown
# Mobile Shmup Controls Research

## 1. Recommended Control Scheme
**Primary Recommendation:** [Fixed/Floating] joystick + auto-fire + bomb button

**Rationale:** [why this works best for vertical shmups]

**Layout:**
```
[ASCII diagram of screen layout showing joystick, bomb button, HUD placement]
```

## 2. Virtual Joystick Specs
- **Type:** Fixed / Floating
- **Position:** Bottom-left, 20% from edge
- **Size:** 120px diameter (15% of screen width)
- **Dead Zone:** 10px center
- **Visual Feedback:** Opacity 0.6 default, 1.0 when active, glow on movement
- **Examples:** Sky Force uses [details], Phoenix HD uses [details]

## 3. Fire Control Decision
- **Auto-Fire:** YES / NO
- **Fire Button (if manual):** [position, size]
- **Rationale:** [player preference data, genre standards]

## 4. Bomb Button Specs
- **Position:** Bottom-right corner
- **Size:** 80px diameter
- **Visual:** Glowing icon, cooldown overlay
- **Feedback:** Screen shake + flash on activation

## 5. Orientation & Layout
- **Orientation:** Portrait / Landscape
- **Rationale:** [why this fits vertical shmups better]
- **HUD Layout:** Top bar (score, lives), bottom (controls), minimal mid-screen

## 6. Alternative: Tilt Controls
- **Viable:** YES / NO
- **Pros:** [list]
- **Cons:** [list]
- **Recommendation:** Include as optional toggle in settings

## 7. Performance Targets
- **Frame Rate:** 60fps (degrade to 30fps on low-end devices)
- **Input Latency:** <16ms (one frame at 60fps)
- **Rendering:** Canvas 2D (WebGL if battery allows)

## 8. Accessibility
- **Button Size:** Minimum 44px (Apple HIG guideline)
- **Contrast:** High visibility against game background
- **Haptic Feedback:** Vibration on fire, bomb, hit (if supported)
```

## Acceptance Criteria
- [ ] Specific control scheme recommended with rationale
- [ ] Joystick specs defined (type, size, position, visual feedback)
- [ ] Fire control decision made (auto-fire vs manual) with justification
- [ ] Bomb button placement and design specified
- [ ] Screen layout diagram provided (ASCII or description)
- [ ] Performance targets documented
- [ ] All sections complete (no TBD, no placeholders)

## Smoke Test
```bash
test -f ".deia/hive/responses/20260413-RAIDEN-R02-MOBILE-CONTROLS-RESEARCH.md" && \
grep -q "Recommended Control Scheme" ".deia/hive/responses/20260413-RAIDEN-R02-MOBILE-CONTROLS-RESEARCH.md" && \
grep -q "Virtual Joystick Specs" ".deia/hive/responses/20260413-RAIDEN-R02-MOBILE-CONTROLS-RESEARCH.md" && \
echo "PASS"
```

## Response Location
`.deia/hive/responses/20260413-RAIDEN-R02-MOBILE-CONTROLS-RESEARCH-RESPONSE.md`
