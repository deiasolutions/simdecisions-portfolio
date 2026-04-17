---
id: RAIDEN-105
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-103, RAIDEN-R01]
---
# SPEC-RAIDEN-105: Boss Fights & Level System

## Priority
P1

## Model Assignment
sonnet

## Role
bee (builder)

## Depends On
- RAIDEN-103 (enemy system)
- RAIDEN-R01 (mechanics research)

## Objective
Implement the 10-level progression system with boss fights at the end of each level. Each boss has attack patterns, phases, and escalating difficulty.

## Context
Building on enemy system (RAIDEN-103). Use boss designs from RAIDEN-R01 research. Bosses are the climax of each level.

## Technical Requirements

### Level Structure
- 10 levels total
- Each level: 30 seconds of enemy waves → boss fight
- Level counter displayed (top center)
- Level transition: fade to black, "Level X" text, fade in

### Boss System
- Boss appears after wave phase completes
- Boss health bar (horizontal bar at top of screen)
- Boss movement patterns (side-to-side, circular, stationary)
- Attack phases: 2-3 phases per boss (attack pattern changes at 75% health, 50% health, 25% health)

### Boss Designs (10 bosses)
Use simplified versions from RAIDEN-R01 research:

1. **Level 1 Boss:** Large red triangle, slow movement, shoots 3-bullet spread
2. **Level 2 Boss:** Green hexagon, side-to-side, shoots spiral pattern
3. **Level 3 Boss:** Blue diamond, circular movement, shoots aimed shots
4. **Level 4 Boss:** Yellow square, stationary, shoots 8-way burst
5. **Level 5 Boss:** Purple pentagon, erratic movement, shoots homing bullets
6. **Level 6 Boss:** Orange octagon, fast side-to-side, shoots laser beam
7. **Level 7 Boss:** Cyan star, diagonal movement, shoots bullet curtain
8. **Level 8 Boss:** Magenta cross, figure-8 pattern, shoots clustered bombs
9. **Level 9 Boss:** White circle, teleports randomly, shoots radial burst
10. **Level 10 Boss:** Rainbow gradient, all patterns, all attack types (final boss)

### Attack Patterns
- **Spread:** 3-5 bullets in arc
- **Spiral:** Bullets rotate while firing
- **Aimed:** Bullets target player position
- **8-way burst:** Bullets in 8 directions (cardinal + diagonal)
- **Homing:** Bullets curve toward player
- **Laser:** Continuous beam (sweeps across screen)
- **Curtain:** Dense wall of bullets
- **Radial:** Bullets in circle (360°)

### Boss Phases
- Phase 1 (100%-75% health): Basic pattern
- Phase 2 (75%-50% health): Faster, more bullets
- Phase 3 (50%-0% health): Most aggressive, new attack type

### Difficulty Scaling
Use formula from RAIDEN-R01:
- Boss health = 100 + (level * 50) [Level 1 = 150 HP, Level 10 = 600 HP]
- Boss fire rate increases 10% per level
- Bullet speed increases 5% per level

### Boss Defeat
- Boss explodes (large particle burst)
- Score bonus (base 1000 * level)
- Transition to next level (or victory screen if level 10)

## Deliverable
Update file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\games\raiden-v1-20260408.html`

Add sections:
- `// ===== LEVEL SYSTEM =====`
- `// ===== BOSS SYSTEM =====`
- `// ===== BOSS DESIGNS =====`
- `// ===== ATTACK PATTERNS =====`

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- Each boss feels unique (different shape, color, movement, attacks)
- Boss health bar provides clear feedback
- Attack patterns are challenging but fair (player can dodge)

## Acceptance Criteria
- [ ] 10 levels implemented
- [ ] Each level has enemy wave phase (30 sec) then boss fight
- [ ] 10 boss designs implemented (distinct shapes, colors, movements)
- [ ] Each boss has 2-3 attack phases
- [ ] Boss health bar displays at top of screen
- [ ] At least 5 distinct attack patterns implemented
- [ ] Difficulty scales per level (health, fire rate, bullet speed)
- [ ] Boss defeat transitions to next level
- [ ] Victory screen after defeating Level 10 boss
- [ ] Smoke test: reach boss, defeat boss, advance to next level

## Smoke Test
```bash
# Manual: Open file in browser
# - Survive wave phase (30 seconds)
# - Boss appears with health bar
# - Boss attacks with patterns
# - Damage boss (health bar decreases)
# - Boss phases change at 75%, 50% health
# - Defeat boss → level transition → next level starts
```

## Tests
Write inline tests:
- Boss health scaling formula
- Attack pattern generation (spread angle, spiral rotation, aimed targeting)
- Phase transitions (at 75%, 50% health)
- Level progression (current level increments)

## Response Location
`.deia/hive/responses/20260408-RAIDEN-105-RESPONSE.md`
