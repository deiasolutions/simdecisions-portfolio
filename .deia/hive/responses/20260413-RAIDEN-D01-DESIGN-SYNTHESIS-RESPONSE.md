# RAIDEN-D01: Design Synthesis and Game Specification -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-13

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\responses\20260413-RAIDEN-D01-GAME-DESIGN-DOC.md` (created)

## What Was Done

Synthesized three research deliverables (RAIDEN-R01, R02, R03) into unified game design document:

- **Section 1:** Game overview with tech stack and target platform specifications
- **Section 2:** Enemy roster finalized - 17 enemy types with exact stats, movement patterns, spawn levels, visual designs
- **Section 3:** Weapon progression - 3 weapon types (Vulcan, Laser, Missiles) with 5 tiers each, plus Bomb and Shield
- **Section 4:** Boss designs - 10 bosses with full phase breakdowns, attack patterns, weak points, rewards
- **Section 5:** Level flow - 10 levels with enemy counts, spawn timing, power-up distribution
- **Section 6:** Difficulty scaling - mathematical formulas for health, speed, spawn rate, bullets, boss HP
- **Section 7:** Scoring system - base values, chain multipliers, medal chaining, grazing, end-of-stage bonuses
- **Section 8:** Visual style guide - CSS color palette, entity rendering, particle effects, screen shake
- **Section 9:** Controls - PC (keyboard/mouse) and mobile (hybrid touch) with sensitivity settings
- **Section 10:** AI specification - NEAT architecture (21-16-4 network), reward function, training loop, hybrid modes
- **Section 11:** Sound design - 6 synthesized SFX + adaptive music system (10 stage themes, 10 boss themes)
- **Section 12:** HUD layout - PC and mobile layouts with game state overlays
- **Section 13:** Performance targets - 60 FPS PC, 30 FPS mobile, 200 max entities
- **Section 14:** File structure - single HTML architecture with all classes outlined
- **Section 15:** Implementation phases - 10 build specs (RAIDEN-101 through RAIDEN-110)
- **Section 16:** Acceptance criteria - 20+ checkpoints for verification
- **Section 17:** Testing plan - unit, integration, performance, E2E, smoke tests

## Tests Run

No code written (design synthesis task). Smoke test spec provided in document:

```bash
test -f ".deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md" && \
grep -q "Enemy Roster (Final)" ".deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md" && \
grep -q "Level Flow (10 Levels)" ".deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md" && \
grep -q "AI Specification (Final)" ".deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md" && \
echo "PASS"
```

Output: **PASS** (all sections present)

## Design Decisions Made

**Enemy Assignment:**
- Levels 1-2: Basic enemies (E01-E05)
- Levels 3-5: Introduce medium enemies (E06-E12)
- Levels 6-10: Add advanced enemies (E13-E17)
- Progressive complexity matches difficulty curve

**Weapon Visual Design:**
- Vulcan: Cyan circles (3-6px) with spread patterns
- Laser: Cyan beams (8-80px width) with glow and piercing
- Missiles: Yellow triangles (6-10px) with white exhaust trails
- All use CSS `var(--sd-*)` variables only

**Boss Progression:**
- Levels 1-3: 2-phase bosses (500-1,000 HP)
- Levels 4-6: 3-phase bosses with mechanics (1,500-2,500 HP)
- Levels 7-9: Complex multi-part bosses (3,000-5,000 HP)
- Level 10: 4-phase final boss (10,000 HP)

**Mobile Controls Decision:**
- Hybrid direct touch (1:1 tracking) + floating anchor fallback
- Bottom 25% screen = movement zone (green thumb zone from R02 research)
- Auto-fire enabled by default (reduces cognitive load)
- 3 sensitivity presets (1×, 1.5×, 2×)
- 88×88px bomb button in right thumb zone
- Haptic feedback on all major events

**AI Architecture Decision:**
- 21 input neurons (vs Flappy Bird's 5) - handles shmup complexity
- 16 hidden neurons (2× input layer, NEAT best practice)
- 4 output neurons (movement left/right, fire, bomb)
- Population 100 (vs Flappy Bird's 50) - more diversity needed
- Fitness balances survival (1.0×) + aggression (10.0× enemy kills) + caution (-50.0× damage)
- 4 hybrid modes for player-AI collaboration

**Sound Design Decision:**
- All Web Audio API synthesis (no audio files)
- 6 core SFX cover all major events
- Adaptive music system: 10 stage themes + 10 boss themes
- Boss music dynamically intensifies as HP drops
- Priority system prevents audio overload (max 32 sounds)

**Performance Budget:**
- Max 200 entities (enemies + bullets + particles)
- Max 200 particles (prioritize recent, cull old)
- Object pooling for bullets/particles (avoid GC)
- Culling for offscreen entities
- 60 FPS PC target, 30 FPS mobile minimum

## Integration Points

**Connects RAIDEN-R01 (Mechanics):**
- All 17 enemy types from R01 research assigned to levels
- All weapon tiers from R01 finalized with exact visuals and stats
- Boss designs from R01 expanded with full phase details
- Difficulty formulas from R01 applied across all 10 levels
- Scoring system from R01 integrated with chain/graze mechanics

**Connects RAIDEN-R02 (Mobile Controls):**
- Hybrid direct touch control scheme (R02 recommendation)
- Bottom 25% touch zone (green thumb zone from R02 research)
- Auto-fire default (R02 finding: reduces cognitive load)
- Haptic feedback patterns (R02 best practices)
- One-handed mode + button size options (R02 accessibility)

**Connects RAIDEN-R03 (AI Architecture):**
- NEAT topology (21-16-4) from R03 spec
- State vector construction (21 inputs) from R03
- Fitness function (7 components) from R03
- Training loop design (background/manual/off) from R03
- Hybrid modes (auto-dodge, auto-fire, co-pilot, takeover) from R03
- Visualization (HUD, fitness graph) from R03

## Ready for Implementation

**10 Build Specs Required (from Section 15):**

1. **RAIDEN-101:** Core engine (canvas, game loop, entity system, collision)
2. **RAIDEN-102:** Player + controls (PC keyboard/mouse, mobile touch)
3. **RAIDEN-103:** Enemy system (17 types, movement patterns, spawning)
4. **RAIDEN-104:** Weapon system (3 weapons × 5 tiers, power-ups, bomb, shield)
5. **RAIDEN-105:** Level progression (wave spawning, difficulty scaling, backgrounds)
6. **RAIDEN-106:** Scoring + UI (chain system, HUD, game states, menus)
7. **RAIDEN-107:** Sound (Web Audio synthesis, 6 SFX, 20 music themes)
8. **RAIDEN-108:** Boss fights (10 bosses, phases, attacks, health bars)
9. **RAIDEN-109:** AI system (NEAT, training loop, visualization, save/load)
10. **RAIDEN-110:** Integration + polish (hybrid modes, optimization, testing)

Each spec will reference sections of this design doc for detailed requirements.

## Completeness Verification

✅ **Enemy Roster:** 17 types, all assigned to levels
✅ **Weapon Progression:** 3 weapons × 5 tiers, fully specified with visuals
✅ **Boss Designs:** 10 bosses with full attack pattern details
✅ **Level Flow:** 10 levels, timing, waves, power-ups documented
✅ **Visual Style:** Colors, shapes, effects all specified (CSS variables only)
✅ **Controls:** PC and mobile controls finalized from R02
✅ **AI Specification:** NEAT architecture complete from R03
✅ **Sound Design:** 6 SFX + 20 music themes documented
✅ **HUD Layout:** PC and mobile layouts specified
✅ **Game States:** Menu, play, pause, game over, level complete enumerated
✅ **Performance Targets:** 60 FPS PC, 30 FPS mobile, 200 max entities
✅ **Implementation Phases:** 10 build specs outlined
✅ **NO TBD, NO PLACEHOLDERS:** All design decisions made

## Blockers

None.

## Next Steps

1. Q88N reviews this design document
2. Q33N creates 10 implementation specs (RAIDEN-101 through RAIDEN-110)
3. BEEs execute specs sequentially (each phase tested before next)
4. Final integration + smoke tests
5. Deploy to `browser/public/games/raiden-v1-20260413.html`

---

**BEE:** BEE-QUEUE-TEMP-SPEC-RAIDEN-D01-design-synthesis
**Objective:** Synthesize research into unified game design
**Result:** Complete design document (17 sections, 2,500+ lines, zero TBD)
