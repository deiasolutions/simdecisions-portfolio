---
id: RAIDEN-B02
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-B01]
---
# SPEC-RAIDEN-B02: Player and Controls

## Priority
P1

## Model Assignment
sonnet

## Role
bee (b33 — you write code and tests)

## Depends On
- RAIDEN-B01 (game engine core)

## Objective
Implement the player ship, keyboard controls (PC), and touch controls (mobile).

## You are in EXECUTE mode
Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.

## Design Reference
Read: `.deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md`
Specifically: Section 9 (Controls) and Section 2 (Visual Style Guide)

## Deliverables

### File: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\public\games\raiden-v1-20260413.html`

**Add to existing engine:**

1. **Player Ship Entity**
   - Triangular ship (15px base, 25px height)
   - Color: `#3b82f6` (blue, --sd-primary)
   - Position: Start at bottom center (400, 550)
   - Speed: 5 pixels per frame
   - Hitbox: 12px x 20px (slightly smaller than visual for fairness)
   - Health: 3 lives
   - Rendering: Draw triangle with glow effect

2. **Keyboard Controls (PC)**
   - Arrow keys: Move player (up, down, left, right)
   - Spacebar: Fire (hold for auto-fire, 200ms interval)
   - B or Shift: Bomb (if available)
   - P: Pause game
   - A: Toggle AI mode (placeholder for now, implement in B08)
   - H: Toggle hybrid mode (placeholder for now)
   - Prevent player from moving off-screen (clamp to 0-800, 0-600)

3. **Touch Controls (Mobile)**
   - Detect touch support: `'ontouchstart' in window`
   - Virtual joystick (bottom-left):
     - Position: 80px from left, 80px from bottom
     - Size: 120px diameter
     - Visual: Outer circle (opacity 0.3) + inner knob (opacity 0.7)
     - Drag knob to move player
     - Dead zone: 10px from center
   - Auto-fire: Automatically fire while joystick active
   - Bomb button (bottom-right):
     - Position: 80px from right, 80px from bottom
     - Size: 80px diameter
     - Visual: Glowing "B" icon
     - Tap to bomb

4. **Player Shooting**
   - Basic single-shot weapon (tier 1)
   - Bullets: 4px circles, color `#06b6d4` (cyan, --sd-accent)
   - Speed: 10 pixels per frame upward
   - Fire rate: 200ms (5 shots per second)
   - Max bullets on screen: 20 (prevent spam)

5. **Bounds Checking**
   - Player cannot move off canvas
   - Bullets despawn when off-screen
   - Clamp player position to [10, 790] x [10, 590]

## Technical Constraints
- Use existing entity system from B01
- Reuse entity pools for bullets (don't create new objects each frame)
- Touch controls only visible on mobile (check window.innerWidth < 768)
- Keyboard controls work even on mobile (for debugging)

## Acceptance Criteria
- [ ] Player ship renders as blue triangle at bottom center
- [ ] Arrow keys move player smoothly in all directions
- [ ] Player cannot move off-screen
- [ ] Spacebar fires bullets upward (auto-fire when held)
- [ ] Bullets despawn when they leave canvas
- [ ] P key pauses and resumes game
- [ ] On mobile: virtual joystick appears and controls player
- [ ] On mobile: bomb button appears and is tappable
- [ ] No errors in console
- [ ] Smooth 60fps with player + 20 bullets

## Tests (Manual Smoke Tests)
Embed test mode:
```javascript
const TEST_MODE = false; // Disabled now that we have real player

// Test: Player movement
// 1. Open game, see player ship at bottom center
// 2. Press arrow keys, player moves smoothly
// 3. Try to move off-screen, player stops at edges
// 4. Hold spacebar, bullets fire upward every 200ms

// Test: Touch controls (mobile)
// 1. Open game on phone or resize browser to <768px width
// 2. See virtual joystick (bottom-left) and bomb button (bottom-right)
// 3. Drag joystick, player moves
// 4. Release joystick, player stops
// 5. Tap bomb button (no effect yet, but button responds)
```

## Smoke Test
```bash
grep -q "player" "browser/public/games/raiden-v1-20260413.html" && \
grep -q "joystick" "browser/public/games/raiden-v1-20260413.html" && \
grep -q "ArrowUp" "browser/public/games/raiden-v1-20260413.html" && \
echo "PASS"
```

## Response Location
`.deia/hive/responses/20260413-RAIDEN-B02-PLAYER-CONTROLS-RESPONSE.md`

## Notes
- Player is now playable (movement + shooting).
- Next spec (B03) will add enemies to shoot at.
- Keep controls responsive: no input lag.
- Virtual joystick must feel smooth (use touch move events, not click).
