---
id: RAIDEN-B05
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-B04]
---
# SPEC-RAIDEN-B05: Level Progression and Boss Fights

## Priority
P1

## Model Assignment
sonnet

## Role
bee (b33 — you write code and tests)

## Depends On
- RAIDEN-B04 (weapon system)

## Objective
Implement 10 levels with difficulty scaling, boss fights, and level transitions.

## You are in EXECUTE mode
Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.

## Design Reference
Read: `.deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md`
Specifically: Section 4 (Boss Designs), Section 5 (Level Flow), Section 6 (Difficulty Scaling)

## Deliverables

### File: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\public\games\raiden-v1-20260413.html`

**Add to existing engine:**

1. **Level System**
   - Track current level (1-10)
   - Display level number in HUD (top-center: "Level 1")
   - Each level lasts 60 seconds or until boss defeated
   - After boss defeated: Transition to next level

2. **Difficulty Scaling (from design doc)**
   - **Enemy count:** `level * 8 + 20` (Level 1: 28 enemies, Level 10: 100 enemies)
   - **Enemy speed:** `1.0 + (level * 0.15)` multiplier
   - **Enemy HP:** `base_hp * (1 + level * 0.25)` (Scout L1: 1 HP, Scout L10: 3 HP)
   - **Spawn frequency:** `max(500ms - level*30ms, 200ms)` (L1: 500ms, L10: 200ms)

3. **Boss Fights (10 Bosses, one per level)**
   Implement at least 3 distinct boss types, reuse with variations:

   **Boss Type 1: Turret (Levels 1, 4, 7)**
   - Large red rectangle (100x60) at top-center
   - HP: 50 * level
   - Attack: Shoots 3 bullets downward every 1 second
   - Movement: Slides left-right slowly

   **Boss Type 2: Circler (Levels 2, 5, 8)**
   - Large red hexagon (80x80) at top-center
   - HP: 60 * level
   - Attack: Shoots 8 bullets radially (360° spread) every 1.5 seconds
   - Movement: Circles around top third of screen

   **Boss Type 3: Diver (Levels 3, 6, 9)**
   - Large red diamond (70x70) at top-center
   - HP: 70 * level
   - Attack: Dives toward player position, shoots 5-bullet spread while diving
   - Movement: Dive → return to top → repeat

   **Final Boss (Level 10):**
   - Huge red pentagon (150x150) at top-center
   - HP: 1000
   - Phases:
     - Phase 1 (100% - 66% HP): Turret attack (5 bullets every 0.5s)
     - Phase 2 (66% - 33% HP): Radial attack (12 bullets every 1s)
     - Phase 3 (33% - 0% HP): Dive + radial combined
   - Movement: Erratic, fast left-right

4. **Boss Spawn Logic**
   - After 60 seconds of normal enemies: Clear screen, spawn boss
   - OR after enemy count threshold reached
   - Boss warning: Screen shake + text "WARNING: BOSS INCOMING" for 2 seconds
   - Music change (optional, or just low rumble sound)

5. **Boss Defeat**
   - When boss HP = 0: Big explosion (50 particles), award 10,000 points
   - Level complete screen: "LEVEL X COMPLETE!" overlay for 3 seconds
   - Transition to next level (reset enemy spawn, increase difficulty)

6. **Level Transitions**
   - Fade out current level
   - Show "LEVEL X" text for 2 seconds
   - Fade in new level
   - Reset: Enemy positions, bullets, but NOT player weapon tier or lives

7. **Game Completion**
   - After defeating Level 10 boss: "GAME COMPLETE!" screen
   - Show final score, total time, accuracy stats
   - "Play Again" button

## Technical Constraints
- Bosses are special entities (type: BOSS) with unique rendering and AI
- Boss attack patterns: Define as state machines (IDLE, ATTACK, MOVE, DIVE)
- Difficulty scaling: Apply multipliers to enemy stats based on current level
- Level state persists (score, lives, weapon tier carry over)

## Acceptance Criteria
- [ ] 10 levels with increasing difficulty
- [ ] At least 3 distinct boss types implemented
- [ ] Bosses spawn after 60 seconds or enemy threshold
- [ ] Boss warning displays before boss spawn
- [ ] Bosses have attack patterns (shoot bullets, move, dive)
- [ ] Defeating boss transitions to next level
- [ ] Level number displayed in HUD
- [ ] Final boss (level 10) has 3 phases
- [ ] Game completion screen after level 10
- [ ] No errors in console
- [ ] 60fps during boss fights

## Tests (Manual Smoke Tests)
```javascript
// Test: Level progression
// 1. Play through level 1 (60 seconds or defeat boss)
// 2. Boss spawns, see warning text
// 3. Defeat boss, see "LEVEL 1 COMPLETE"
// 4. Transition to level 2
// 5. Notice enemies spawn faster and have more HP

// Test: Boss fights
// 1. Fight Turret boss (level 1): Shoots 3 bullets, slides left-right
// 2. Fight Circler boss (level 2): Shoots radial pattern
// 3. Fight Diver boss (level 3): Dives toward player

// Test: Final boss
// 1. Skip to level 10 (use cheat code or debug mode)
// 2. Final boss has 1000 HP
// 3. Observe 3 attack phases as HP decreases
// 4. Defeat final boss, see "GAME COMPLETE" screen

// Test: Difficulty scaling
// 1. Compare level 1 vs level 5: More enemies, faster spawn, higher HP
// 2. Check enemy stats match difficulty formula
```

## Smoke Test
```bash
grep -q "boss" "browser/public/games/raiden-v1-20260413.html" && \
grep -q "level" "browser/public/games/raiden-v1-20260413.html" && \
grep -q "WARNING" "browser/public/games/raiden-v1-20260413.html" && \
echo "PASS"
```

## Response Location
`.deia/hive/responses/20260413-RAIDEN-B05-LEVEL-PROGRESSION-RESPONSE.md`

## Notes
- Game is now complete in terms of core loop (10 levels, bosses, progression).
- Next specs add polish: scoring (B06), sound (B07), AI (B08), mobile (B09), integration (B10).
- Boss fights should be challenging but fair (clear attack telegraphs).
