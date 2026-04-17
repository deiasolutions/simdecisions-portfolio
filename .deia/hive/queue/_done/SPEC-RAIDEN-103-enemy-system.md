---
id: RAIDEN-103
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-101, RAIDEN-R01]
---
# SPEC-RAIDEN-103: Enemy System

## Priority
P1

## Model Assignment
sonnet

## Role
bee (builder)

## Depends On
- RAIDEN-101 (game engine core)
- RAIDEN-R01 (mechanics research)

## Objective
Implement the enemy spawn system with at least 5 enemy types, movement patterns, and basic AI. Enemies should spawn according to difficulty curve and be destroyed by player bullets.

## Context
Building on the game engine from RAIDEN-101. Use enemy designs from RAIDEN-R01 research. This spec covers basic enemy behaviors — boss fights come in RAIDEN-105.

## Technical Requirements

### Enemy Types (minimum 5)
1. **Grunt:** Straight line downward, no shooting, low health (1 hit)
2. **Weaver:** Sine wave pattern, shoots occasionally, medium health (2 hits)
3. **Diver:** Kamikaze (homes toward player), no shooting, medium health
4. **Turret:** Stationary (moves down slowly), shoots frequently, high health (3 hits)
5. **Formation:** Spawns in groups of 3-5, moves in formation, shoots in sync

### Movement Patterns
- Straight line (velocity only)
- Sine wave (x oscillates based on time)
- Homing (calculate angle toward player, adjust velocity)
- Formation (follow leader with offset)
- Spiral (angle increases over time)

### Enemy Bullets
- Red circles (contrast with player's yellow bullets)
- Velocity: toward player or straight down (depends on enemy type)
- Use entity pool (pre-allocate 200)

### Spawn System
- Spawn waves at regular intervals (start at 2 seconds, decrease with level)
- Spawn patterns: single, pair, formation, random scatter
- Spawn positions: top edge, random x (or specific x for formations)
- Difficulty scaling: more enemies, faster enemies, higher health (use formula from RAIDEN-R01)

### Collision & Destruction
- Player bullets destroy enemies (reduce health)
- Enemy bullets hit player (reduce lives, invincibility frames)
- Enemies colliding with player (reduce lives)
- Death animation: simple particle burst (4-8 white circles flying outward, fade out)

### Scoring
- Each enemy destroyed: base score (Grunt=10, Weaver=25, Diver=50, Turret=100, Formation=20 each)
- Combo multiplier: consecutive kills within 1 second (1x, 2x, 3x, max 5x)
- Display: score top right, combo multiplier flashes when active

## Deliverable
Update file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\games\raiden-v1-20260408.html`

Add sections:
- `// ===== ENEMY SYSTEM =====`
- `// ===== ENEMY TYPES =====`
- `// ===== SPAWN SYSTEM =====`
- `// ===== SCORING =====`

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- At least 5 enemy types implemented
- Smooth movement patterns (no jitter)
- Death animations for visual feedback
- Combo system encourages aggressive play

## Acceptance Criteria
- [ ] 5 enemy types implemented (Grunt, Weaver, Diver, Turret, Formation)
- [ ] Each enemy type has distinct movement pattern
- [ ] Enemies shoot bullets (Weaver, Turret)
- [ ] Spawn system creates waves at regular intervals
- [ ] Player bullets destroy enemies (health system works)
- [ ] Enemy bullets hit player (lives decrease, invincibility frames activate)
- [ ] Death animation plays when enemy destroyed
- [ ] Score counter increases on kill
- [ ] Combo multiplier activates for consecutive kills
- [ ] Smoke test: enemies spawn, move, shoot, die when hit

## Smoke Test
```bash
# Manual: Open file in browser
# - Enemies spawn from top of screen
# - Shoot enemies with player bullets (they die)
# - Enemies shoot back (red bullets)
# - Getting hit reduces lives
# - Score increases when killing enemies
# - Combo multiplier shows when killing quickly
```

## Tests
Write inline tests:
- Enemy movement patterns (sine wave math, homing angle calculation)
- Collision detection (player bullet hits enemy)
- Health system (enemy takes 2 hits, dies on 3rd)
- Combo timer (resets after 1 second)

## Response Location
`.deia/hive/responses/20260408-RAIDEN-103-RESPONSE.md`
