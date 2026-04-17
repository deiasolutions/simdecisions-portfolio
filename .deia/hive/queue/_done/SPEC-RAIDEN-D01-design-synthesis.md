---
id: RAIDEN-D01
priority: P1
model: sonnet
role: queen
depends_on: [RAIDEN-R01, RAIDEN-R02, RAIDEN-R03]
---
# SPEC-RAIDEN-D01: Design Synthesis and Game Specification

## Priority
P1

## Model Assignment
sonnet

## Role
queen (Q33N — you synthesize research into unified game design)

## Depends On
- RAIDEN-R01 (shmup mechanics research)
- RAIDEN-R02 (mobile controls research)
- RAIDEN-R03 (AI research)

## Objective
Synthesize the three research deliverables into a unified game design document that builders can implement from.

## You are in EXECUTE mode
Write the complete game design document. Do NOT enter plan mode. Do NOT ask for approval. Just synthesize and document.

## Synthesis Tasks

### 1. Consolidate Enemy Roster
- Take the enemy types from RAIDEN-R01 research
- Assign enemies to specific levels (1-10)
- Create spawn patterns for each level
- Define exact stats (HP, speed, score value, attack patterns)

### 2. Finalize Weapon Progression
- Take the weapon tiers from RAIDEN-R01 research
- Define exact upgrade path (when does player get each weapon?)
- Specify drop rates for power-ups
- Define weapon visuals (colors, particle effects)

### 3. Design 10 Boss Fights
- One boss per level
- Define attack patterns, phases, weak points
- Ensure difficulty curve from level 1-10

### 4. Define Visual Style
- CSS-only graphics (no sprites, no images)
- Geometric shapes with glow effects
- Color palette using `var(--sd-*)` CSS variables
- Particle effects for explosions, bullets, power-ups

### 5. Integrate Mobile Controls
- Use recommendations from RAIDEN-R02 research
- Define exact screen layout for mobile vs PC
- Specify touch zones, button sizes, visual feedback

### 6. Specify AI Architecture
- Use recommendations from RAIDEN-R03 research
- Define exact state space, action space, fitness function
- Specify training loop parameters
- Design AI visualization (generation counter, fitness display)

### 7. Create Level Flow Document
- Define what happens in each of the 10 levels
- Enemy waves, spawn timing, boss arrival
- Difficulty pacing, power-up availability
- Level completion criteria

## Deliverables

### File: `.deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md`

Structure (must include all sections):
```markdown
# Raiden-Style Shmup: Complete Game Design

## 1. Game Overview
- Genre: Vertical scrolling shoot-em-up
- Target Platform: Browser (PC + mobile)
- Target File: browser/public/games/raiden-v1-20260413.html
- Tech: Single HTML file, Canvas API, Web Audio API, NEAT for AI

## 2. Enemy Roster (Final)
[Complete table from R01 research, with level assignments]

## 3. Weapon Progression (Final)
[Complete table from R01 research, with visuals and upgrade path]

## 4. Boss Designs (10 Bosses)
[Complete table from R01 research, one boss per level]

## 5. Level Flow (10 Levels)
| Level | Duration | Enemies | Boss | Power-Ups | Difficulty |
|-------|----------|---------|------|-----------|------------|
| 1 | 60s | 20 scouts | Turret Boss | 2 weapon, 1 bomb | Easy |
| ... | ... | ... | ... | ... | ... |

## 6. Difficulty Scaling (Final Formula)
[Formula from R01 research, validated]

## 7. Scoring System (Final)
[System from R01 research, with specific values]

## 8. Visual Style Guide
**Colors:**
- Player ship: `var(--sd-primary)` (blue)
- Enemy ships: `var(--sd-danger)` (red)
- Bullets (player): `var(--sd-accent)` (cyan)
- Bullets (enemy): `var(--sd-warning)` (orange)
- Power-ups: `var(--sd-success)` (green)
- Explosions: `var(--sd-warning)` to transparent gradient

**Shapes:**
- Player: Triangular ship (15px base, 25px height)
- Enemies: Various polygons (squares, diamonds, pentagons)
- Bullets: Small circles (3-5px)
- Bosses: Large complex shapes (50-100px)

**Effects:**
- Glow: `box-shadow: 0 0 10px currentColor`
- Trails: Fading particles behind moving objects
- Explosions: Expanding circles with particle burst

## 9. Controls (Final)
**PC:**
- Arrow keys: move
- Spacebar: fire (auto-fire option in settings)
- B or Shift: bomb
- P: pause
- A: toggle AI mode
- H: toggle hybrid mode (AI-assist)

**Mobile:**
[Recommendations from R02 research — joystick type, placement, button specs]

**Screen Layout:**
[ASCII diagram or detailed description from R02 research]

## 10. AI Specification (Final)
**Approach:** NEAT neuroevolution

**State Space:** [from R03 research]
**Action Space:** [from R03 research]
**Fitness Function:** [from R03 research]
**Training Loop:** [from R03 research]
**Visualization:** [from R03 research]

## 11. Sound Design
**Web Audio API (synthesized):**
- Player shoot: 200Hz beep, 50ms
- Enemy explosion: White noise burst, 150ms, filtered 100-800Hz
- Power-up collect: Ascending tone 440Hz → 880Hz, 100ms
- Boss warning: Low rumble 80Hz, 500ms loop
- Level complete: Victory jingle (C-E-G-C major chord arpeggio)
- Bomb: Whoosh + explosion (sweep 2000Hz → 100Hz, 300ms)

## 12. HUD Layout
**Top Bar:**
- Left: Score (large font)
- Center: Level indicator
- Right: Lives (ship icons)

**Bottom Bar (PC):**
- Left: Current weapon icon + tier
- Right: Bomb count

**Bottom (Mobile):**
- Left: Virtual joystick
- Right: Bomb button
- Top: Same as PC

## 13. Game States
- MENU: Start screen with "Play" / "AI Mode" / "Settings"
- PLAYING: Active gameplay
- PAUSED: Overlay with "Resume" / "Restart" / "Quit"
- GAME_OVER: Score summary, high score, "Retry" / "Menu"
- LEVEL_COMPLETE: Transition screen, show stats, 3s delay
- AI_TRAINING: Same as PLAYING but with AI visualization overlay

## 14. Performance Targets
- 60fps on desktop (modern browsers)
- 30fps minimum on mobile
- Canvas size: 800x600 (scales to viewport)
- Max entities on screen: 200 (enemies + bullets + particles)

## 15. File Structure (Single HTML)
```html
<!DOCTYPE html>
<html>
<head>
  <style>/* CSS here */</style>
</head>
<body>
  <canvas id="game"></canvas>
  <script>
    // Game engine
    // Entity system
    // Collision detection
    // Rendering
    // Controls (PC + mobile)
    // AI (NEAT)
    // Sound
    // Game loop
  </script>
</body>
</html>
```

## 16. Implementation Phases (for build specs)
1. Game engine core (canvas, loop, entities, collision)
2. Player + controls (PC keyboard, mobile touch)
3. Enemy system (types, patterns, spawning)
4. Weapon system (shooting, power-ups, upgrades)
5. Level progression (waves, bosses, transitions)
6. Scoring + UI (HUD, game states, menus)
7. Sound (Web Audio synthesized effects)
8. AI system (NEAT, training, auto-play, hybrid)
9. Mobile polish (responsive layout, touch tuning, performance)
10. Integration + testing (E2E, smoke tests, deploy)
```

## Acceptance Criteria
- [ ] All enemy types from R01 assigned to levels
- [ ] All weapon tiers from R01 fully specified with visuals
- [ ] 10 boss fights designed with attack patterns
- [ ] Level flow table complete (10 levels, timing, waves)
- [ ] Visual style guide complete (colors, shapes, effects)
- [ ] PC and mobile controls finalized from R02
- [ ] AI specification complete from R03
- [ ] Sound design documented (all 6 sound effects)
- [ ] HUD layout specified for PC and mobile
- [ ] Game states enumerated (menu, play, pause, game over, etc.)
- [ ] Performance targets documented
- [ ] 10 implementation phases outlined for build specs
- [ ] No TBD, no placeholders, all design decisions made

## Smoke Test
```bash
test -f ".deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md" && \
grep -q "Enemy Roster (Final)" ".deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md" && \
grep -q "Level Flow (10 Levels)" ".deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md" && \
grep -q "AI Specification (Final)" ".deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md" && \
echo "PASS"
```

## Response Location
`.deia/hive/responses/20260413-RAIDEN-D01-DESIGN-SYNTHESIS-RESPONSE.md`
