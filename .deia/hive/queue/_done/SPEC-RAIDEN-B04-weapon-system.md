---
id: RAIDEN-B04
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-B03]
---
# SPEC-RAIDEN-B04: Weapon System and Power-Ups

## Priority
P1

## Model Assignment
sonnet

## Role
bee (b33 — you write code and tests)

## Depends On
- RAIDEN-B03 (enemy system)

## Objective
Implement weapon upgrades, power-ups, and bomb mechanics.

## You are in EXECUTE mode
Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.

## Design Reference
Read: `.deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md`
Specifically: Section 3 (Weapon Progression)

## Deliverables

### File: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\public\games\raiden-v1-20260413.html`

**Add to existing engine:**

1. **Weapon Tiers (Implement at least 5 tiers from design doc)**
   - **Tier 1 (Single Shot):** One bullet straight up (already implemented in B02)
   - **Tier 2 (Double Shot):** Two bullets parallel (left and right offset)
   - **Tier 3 (Spread Shot):** Three bullets (center, 15° left, 15° right)
   - **Tier 4 (Spread + Fast):** Five bullets spread (0°, ±15°, ±30°), faster fire rate (150ms)
   - **Tier 5 (Laser):** Continuous beam upward (30px width, screen height), damages all enemies in path

   **Damage Values:**
   - Tier 1-4 bullets: 1 damage each
   - Tier 5 laser: 0.5 damage per frame (30 damage per second at 60fps)

2. **Power-Up Drops**
   - Enemies drop power-ups on death (10% chance)
   - Power-up types:
     - **Weapon Upgrade (W):** Green circle with "W", upgrades weapon tier
     - **Bomb (B):** Yellow circle with "B", adds 1 bomb to inventory
     - **Life (L):** Blue circle with "L", adds 1 life (rare, 2% drop rate)
   - Power-ups fall slowly downward (2 pixels/frame)
   - Despawn after 10 seconds or when off-screen

3. **Weapon Upgrade Logic**
   - Player starts at tier 1
   - Collect "W" power-up: Upgrade to next tier (max tier 5)
   - Weapon tier persists across levels
   - Weapon tier resets to tier 1 on death (lose all upgrades)

4. **Bomb Mechanics**
   - Player starts with 3 bombs
   - Press B or Shift: Activate bomb (if available)
   - Bomb effect:
     - Clear all enemy bullets on screen
     - Damage all enemies on screen (5 damage each)
     - Screen flash (white overlay, fade out over 15 frames)
     - Sound effect (synthesized explosion)
   - Cooldown: 1 second (prevent spam)

5. **HUD Display**
   - Top-right: Bomb count (e.g., "Bombs: 3")
   - Bottom-left: Current weapon tier (e.g., "Weapon: Tier 3")
   - Color: White text with black outline

6. **Visual Effects**
   - Tier 5 laser: Glowing cyan beam with particle trail
   - Bomb explosion: Radial white flash + expanding circle

## Technical Constraints
- Weapon firing logic: Check current tier, spawn bullets accordingly
- Laser (tier 5) does not spawn bullet entities, instead draws rectangle and checks collision every frame
- Power-ups use entity pool (same as enemies/bullets)
- Bomb screen flash: Use canvas globalAlpha or overlay div

## Acceptance Criteria
- [ ] 5 weapon tiers implemented with distinct visuals
- [ ] Weapon upgrades when collecting "W" power-up
- [ ] Weapon tier displayed in HUD
- [ ] Bombs clear enemy bullets and damage enemies
- [ ] Bomb count displayed in HUD
- [ ] Bombs have 1-second cooldown
- [ ] Power-ups drop from enemies (10% chance)
- [ ] Power-ups despawn after 10 seconds
- [ ] No errors in console
- [ ] 60fps with tier 5 laser active

## Tests (Manual Smoke Tests)
```javascript
// Test: Weapon upgrades
// 1. Shoot enemies, collect "W" power-ups
// 2. See weapon tier increase (1 → 2 → 3 → 4 → 5)
// 3. Observe different bullet patterns for each tier
// 4. Tier 5 laser: See glowing beam, enemies take damage

// Test: Bombs
// 1. Press B key (or tap bomb button on mobile)
// 2. Screen flashes white
// 3. All enemy bullets disappear
// 4. All enemies take 5 damage
// 5. Bomb count decreases (Bombs: 3 → 2)

// Test: Power-up drops
// 1. Kill enemies, see power-ups drop occasionally (10%)
// 2. Collect power-ups, see effects (weapon upgrade, bomb added, life added)
// 3. If power-up not collected, it despawns after 10 seconds

// Test: Death penalty
// 1. Upgrade weapon to tier 5
// 2. Die (get hit 3 times)
// 3. Respawn at tier 1 (weapon reset)
```

## Smoke Test
```bash
grep -q "weapon" "browser/public/games/raiden-v1-20260413.html" && \
grep -q "bomb" "browser/public/games/raiden-v1-20260413.html" && \
grep -q "powerup" "browser/public/games/raiden-v1-20260413.html" && \
echo "PASS"
```

## Response Location
`.deia/hive/responses/20260413-RAIDEN-B04-WEAPON-SYSTEM-RESPONSE.md`

## Notes
- Weapon upgrades add strategic depth.
- Bombs are powerful but limited (use wisely).
- Next spec (B05) adds level progression and bosses.
- Laser (tier 5) is the most powerful but also the most complex to render.
