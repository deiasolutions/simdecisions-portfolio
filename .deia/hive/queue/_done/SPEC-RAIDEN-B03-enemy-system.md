---
id: RAIDEN-B03
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-B02]
---
# SPEC-RAIDEN-B03: Enemy System

## Priority
P1

## Model Assignment
sonnet

## Role
bee (b33 — you write code and tests)

## Depends On
- RAIDEN-B02 (player and controls)

## Objective
Implement enemy types, spawn patterns, formations, and enemy shooting.

## You are in EXECUTE mode
Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.

## Design Reference
Read: `.deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md`
Specifically: Section 2 (Enemy Roster), Section 5 (Level Flow), Section 4 (Difficulty Scaling)

## Deliverables

### File: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\public\games\raiden-v1-20260413.html`

**Add to existing engine:**

1. **Enemy Types (Implement at least 5 types)**
   - **Scout:** 1 HP, fast, straight down, score 100
   - **Heavy:** 3 HP, slow, straight down, shoots occasionally, score 500
   - **Kamikaze:** 1 HP, very fast, dives toward player, score 200
   - **Weaver:** 2 HP, medium speed, sine wave pattern, score 300
   - **Formation:** 1 HP, moves in V-formation with 4 others, score 150

   **Visuals (from design doc):**
   - Scout: Small red square (10x10)
   - Heavy: Large red diamond (20x20)
   - Kamikaze: Red triangle pointing down (12x15)
   - Weaver: Red pentagon (15x15)
   - Formation: Small red circles (8x8)

2. **Enemy Spawning**
   - Spawn enemies from top of screen
   - Random X position (with padding from edges)
   - Spawn rate: 1 enemy per second initially, increases with level
   - Wave system: Spawn enemies in waves (e.g., 5 scouts, pause 2s, 3 heavies, pause 3s)

3. **Enemy Movement Patterns**
   - **Straight:** Move straight down at constant speed
   - **Sine Wave:** Horizontal sine wave while moving down
   - **Dive:** Move toward player position when spawned
   - **Formation:** Maintain offset from formation leader

4. **Enemy Shooting**
   - Heavy and Weaver types shoot bullets downward
   - Enemy bullets: 5px red circles, speed 5 pixels/frame
   - Fire rate: 1 bullet per 2 seconds (random offset per enemy)
   - Bullets despawn when off-screen

5. **Collision Handling**
   - Player bullets hit enemies: Reduce enemy HP, destroy bullet
   - Enemy bullets hit player: Reduce player lives, destroy bullet, invincibility for 2s
   - Player hits enemy (collision): Reduce player lives, destroy enemy, invincibility for 2s

6. **Enemy Destruction**
   - When enemy HP reaches 0: Add score, spawn particle explosion, remove enemy
   - When enemy leaves bottom of screen: Remove enemy (no score)

7. **Particle Effects**
   - Explosion: 10 particles radiating outward, fade over 30 frames
   - Color: Orange to transparent

## Technical Constraints
- Max 50 enemies on screen at once (cap for performance)
- Reuse enemy entities from pool (no `new` in game loop)
- Enemy patterns defined as functions: `straightPattern(enemy, dt)`, `sinePattern(enemy, dt)`
- Use design doc's difficulty scaling formula for spawn rate and HP

## Acceptance Criteria
- [ ] At least 5 enemy types render with correct visuals
- [ ] Enemies spawn from top at regular intervals
- [ ] Enemies follow movement patterns (straight, sine, dive, formation)
- [ ] Heavy and Weaver enemies shoot bullets downward
- [ ] Player bullets destroy enemies (damage based on HP)
- [ ] Enemy bullets damage player (lives decrease)
- [ ] Explosions spawn particles when enemy destroyed
- [ ] Score increases when enemy killed
- [ ] No errors in console
- [ ] 60fps with 20 enemies + 50 bullets

## Tests (Manual Smoke Tests)
```javascript
// Test: Enemy spawning
// 1. Start game, enemies spawn from top every second
// 2. See different enemy types (scouts, heavies, weavers)
// 3. Enemies move in different patterns (straight, sine wave)

// Test: Shooting
// 1. Shoot at enemies with player bullets
// 2. Enemies lose HP and explode when HP = 0
// 3. See explosion particles
// 4. Score increases

// Test: Enemy bullets
// 1. Heavy/Weaver enemies shoot bullets downward
// 2. Get hit by enemy bullet, lose 1 life
// 3. Player gets 2 seconds invincibility (blink effect)

// Test: Collisions
// 1. Fly into an enemy, lose 1 life
// 2. Enemy destroyed, player gets invincibility

// Test: Performance
// 1. Let game run until 20+ enemies on screen
// 2. Still 60fps (check with F key FPS counter)
```

## Smoke Test
```bash
grep -q "enemy" "browser/public/games/raiden-v1-20260413.html" && \
grep -q "explosion" "browser/public/games/raiden-v1-20260413.html" && \
grep -q "spawn" "browser/public/games/raiden-v1-20260413.html" && \
echo "PASS"
```

## Response Location
`.deia/hive/responses/20260413-RAIDEN-B03-ENEMY-SYSTEM-RESPONSE.md`

## Notes
- Game is now playable (player vs enemies).
- Next spec (B04) adds weapon power-ups.
- Enemy difficulty will scale with levels (implemented in B05).
- Keep enemy patterns interesting but fair (player can dodge).
