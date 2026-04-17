---
id: RAIDEN-104
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-102, RAIDEN-103, RAIDEN-R01]
---
# SPEC-RAIDEN-104: Weapon System & Power-Ups

## Priority
P1

## Model Assignment
sonnet

## Role
bee (builder)

## Depends On
- RAIDEN-102 (player ship)
- RAIDEN-103 (enemy system)
- RAIDEN-R01 (mechanics research)

## Objective
Implement the progressive weapon system with 5 weapon tiers and power-up drops. Player collects power-ups to upgrade weapons from basic shot to spread/laser/homing missiles.

## Context
Building on player ship (RAIDEN-102) and enemies (RAIDEN-103). Use weapon tier designs from RAIDEN-R01 research.

## Technical Requirements

### Weapon Tiers (5 minimum)
1. **Tier 0 (Basic):** Single shot straight upward (default)
2. **Tier 1 (Dual Shot):** Two bullets parallel
3. **Tier 2 (Spread):** Three bullets (center + 15° angles)
4. **Tier 3 (Laser):** Continuous beam (high damage, limited width)
5. **Tier 4 (Homing):** Bullets curve toward nearest enemy

Advanced tier (optional):
6. **Tier 5 (Plasma):** Wide spread with piercing bullets

### Power-Up System
- Power-ups drop from destroyed enemies (10% drop rate)
- Power-up types:
  - **Weapon (W):** Upgrade weapon tier (blue cube)
  - **Bomb (B):** Add bomb charge (green cube)
  - **Shield (S):** Temporary invincibility (cyan cube)
  - **1-Up:** Extra life (gold star)
- Power-ups float downward slowly (velocity: 0, 2)
- Player collects by touching (AABB collision)
- Visual feedback: power-up pulses, collection sound

### Bomb System
- Player starts with 3 bombs
- Bomb clears all enemy bullets on screen
- Bomb damages all enemies (50% health)
- Bomb animation: screen flash + expanding circle
- Bomb count displayed (top left, next to lives)

### Shield System
- Shield duration: 5 seconds
- Shield visual: cyan glow around player ship
- Immune to bullets and collisions while active
- Shield timer displayed

### Weapon Indicator
- Show current weapon tier (icon + text, top left)
- Color-coded per tier

## Deliverable
Update file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\games\raiden-v1-20260408.html`

Add sections:
- `// ===== WEAPON TIERS =====`
- `// ===== POWER-UP SYSTEM =====`
- `// ===== BOMB SYSTEM =====`

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- Each weapon tier feels distinct and more powerful
- Power-up drop rate balanced (not too rare, not too common)
- Visual feedback for weapon tier changes

## Acceptance Criteria
- [ ] 5 weapon tiers implemented (Basic, Dual, Spread, Laser, Homing)
- [ ] Player starts with Tier 0 (basic shot)
- [ ] Power-ups drop from enemies (10% rate)
- [ ] Collecting weapon power-up upgrades tier (up to Tier 4)
- [ ] Bomb clears bullets and damages enemies
- [ ] Shield power-up grants 5 seconds invincibility
- [ ] 1-Up power-up adds extra life
- [ ] Weapon indicator displays current tier (top left)
- [ ] Bomb count displayed (top left)
- [ ] Smoke test: collect power-ups, weapon upgrades, use bomb

## Smoke Test
```bash
# Manual: Open file in browser
# - Kill enemies until power-up drops
# - Collect power-up (weapon upgrades from single to dual shot)
# - Collect more power-ups (weapon progresses to spread, laser, homing)
# - Press bomb key (B or Shift) — bullets cleared, enemies damaged
# - Collect shield — player glows cyan, bullets pass through
```

## Tests
Write inline tests:
- Weapon tier progression (tier increases on power-up)
- Bullet spread calculation (spread angle = 15°)
- Homing bullet targeting (finds nearest enemy)
- Laser continuous damage (ticks per frame)
- Bomb clears bullets (all enemy bullets removed)

## Response Location
`.deia/hive/responses/20260408-RAIDEN-104-RESPONSE.md`
