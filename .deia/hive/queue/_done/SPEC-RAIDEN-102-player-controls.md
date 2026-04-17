---
id: RAIDEN-102
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-101, RAIDEN-R02]
---
# SPEC-RAIDEN-102: Player Ship & Controls

## Priority
P1

## Model Assignment
sonnet

## Role
bee (builder)

## Depends On
- RAIDEN-101 (game engine core)
- RAIDEN-R02 (mobile controls research)

## Objective
Implement the player ship with keyboard controls (PC) and touch controls (mobile). Ship should move, fire bullets, and stay within screen bounds.

## Context
Building on the game engine from RAIDEN-101. This adds the playable ship. Controls must feel responsive and match the UX patterns from RAIDEN-R02 research.

## Technical Requirements

### Player Ship
- Extend `Entity` base class
- Sprite: Blue triangle (CSS border trick or canvas path)
- Starting position: bottom center of screen
- Movement speed: configurable (start at 5 pixels/frame)
- Health: 3 lives (visual indicator)
- Invincibility frames after hit (2 seconds, ship flashes)

### Keyboard Controls (PC)
- Arrow keys or WASD: 8-way movement
- Spacebar: fire (auto-fire, hold to shoot continuously)
- Shift or B: bomb (special ability, limited uses)
- Movement feels tight and responsive (no acceleration/deceleration)

### Touch Controls (Mobile)
- Virtual joystick (floating, appears on touch)
  - Touch left half of screen: joystick appears at touch point
  - Drag: ship moves relative to joystick center
  - Release: joystick disappears, ship stops
- Auto-fire: always shooting (no fire button)
- Bomb button: fixed position (bottom right corner, large enough for thumb)
- Visual feedback: joystick renders as two circles, bomb button pulses

### Bullet System (Player)
- Player fires bullets upward (velocity: 0, -10)
- Bullet sprite: small yellow rectangle
- Fire rate: 10 bullets/second (configurable)
- Bullets removed when off-screen
- Use entity pool for bullets (pre-allocate 100)

### Screen Boundaries
- Player clamped to screen edges (cannot move off-screen)
- Leave 10px margin from edges for visual clarity

## Deliverable
Update file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\games\raiden-v1-20260408.html`

Add sections:
- `// ===== PLAYER SHIP =====`
- `// ===== BULLET SYSTEM =====`
- `// ===== CONTROLS (PC) =====`
- `// ===== CONTROLS (MOBILE) =====`

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- Smooth controls (no input lag)
- Touch detection (detect mobile vs PC and switch control scheme)
- Visual feedback for all inputs (joystick visible, bomb button animates)

## Acceptance Criteria
- [ ] Player ship renders at bottom center (blue triangle)
- [ ] Keyboard controls work (arrow keys move ship, spacebar fires)
- [ ] Touch controls work (virtual joystick moves ship, auto-fire active)
- [ ] Bomb button renders and responds to touch
- [ ] Ship clamped to screen boundaries
- [ ] Bullets fire at 10/sec, move upward, removed when off-screen
- [ ] Invincibility frames after hit (ship flashes)
- [ ] Lives counter displayed (top left corner)
- [ ] Smoke test: can move ship around, fire bullets, use bomb

## Smoke Test
```bash
# Manual: Open file in browser
# - Arrow keys move ship
# - Spacebar fires bullets
# - Ship cannot move off-screen
# - Touch left side to move (mobile or simulate touch in devtools)
# - Bomb button visible in bottom right
```

## Tests
Write inline tests:
- Player movement (8 directions)
- Screen boundary clamping
- Bullet firing rate (count bullets spawned per second)
- Touch input mapping (touch position -> ship movement)

## Response Location
`.deia/hive/responses/20260408-RAIDEN-102-RESPONSE.md`
