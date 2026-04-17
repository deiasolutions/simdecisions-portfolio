---
id: RAIDEN-000
priority: P1
model: sonnet
role: queen
depends_on: []
---
# SPEC-RAIDEN-000: Raiden-Style Shoot-Em-Up — Master Coordination Spec

## Priority
P1

## Model Assignment
sonnet

## Role
queen (Q33N coordinator — you decompose this into research, design, and build specs)

## Depends On
(none)

## Acceptance Criteria

- [ ] Research phase completed with genre analysis and AI approach selection
- [ ] Design specs produced for game mechanics, levels, and weapon progression
- [ ] Build specs queued covering all 10 levels, boss fights, and scoring
- [ ] Auto-play AI spec includes neuroevolution or RL approach
- [ ] Playable game deployed to browser/public/games/

## Intent
Coordinate the full build of a Raiden-style vertical scrolling shoot-em-up game. This is NOT a single-builder task. You are the Q33N. Your job is to:

1. **Dispatch research bees** to study the game genre, mechanics, and AI approaches
2. **Run design ideation** based on research findings
3. **Break the build into phased specs** and queue them for bees

The final product is a polished, playable game in `browser/public/games/`.

---

## Game Requirements

### Core Gameplay
- **Genre:** Vertical scrolling shoot-em-up (shmup), inspired by Raiden, 1943, Galaga
- **10 levels** of progressively more difficult enemies
- **Progressive weapon system** — player collects power-ups that upgrade weapons:
  - Start with basic single shot
  - Spread shot, laser, homing missiles, bombs, shields
  - At least 5 distinct weapon tiers
- **Boss fights** — each level ends with a boss that has attack patterns
- **Score system** with combo multiplier

### Controls
- **PC:** Arrow keys to move, spacebar to fire (auto-fire option), bomb key (B or shift)
- **Mobile:** Touch joystick (left side) + auto-fire with manual bomb button (right side), or tilt controls option. Research how modern mobile shmups handle this — use whatever is standard.

### Auto-Play / Self-Learning AI
- **Auto-play mode:** When player is idle or toggles AI mode, the game plays itself
- **Learning AI:** The AI should get better over time using neuroevolution (NEAT) or reinforcement learning
  - AI observes: player position, enemy positions, bullet positions, power-up positions
  - AI outputs: movement direction + fire/bomb decisions
  - AI improves across generations/episodes
  - Visual indicator showing AI generation/skill level
  - Player can watch the AI learn in real-time (like the flappy bird AI)
- **Hybrid mode option:** AI assists the player (auto-dodges bullets, player aims)

### Technical
- **Single HTML file per version** — no build step, no npm, canvas API
- **PC version:** `browser/public/games/raiden-v1-YYYYMMDD.html`
- **Mobile version:** Same file, responsive — detect touch and switch control scheme
- **60fps** target on modern hardware
- **Sound effects** via Web Audio API (synthesized, no external files)

---

## Your Coordination Plan

### Phase 1: Research (dispatch 2-3 bees in parallel)

Create and queue these research specs:

**SPEC-RAIDEN-R01: Shmup Mechanics Research**
- Bee researches: Raiden series mechanics, enemy patterns, weapon progression systems, scoring systems, difficulty curves across 10 levels
- Deliverable: Design reference document with specific enemy types, weapon tiers, boss patterns, and difficulty scaling formula

**SPEC-RAIDEN-R02: Mobile Shmup Controls Research**
- Bee researches: How top mobile shmups handle controls (Geometry Wars, Phoenix HD, Sky Force, Galaga Wars, etc.)
- Deliverable: Recommendation for touch control scheme with specific UX patterns

**SPEC-RAIDEN-R03: Self-Learning AI Research**
- Bee researches: NEAT/neuroevolution for arcade games, state representation for shmups, reward function design
- Reference: `browser/public/games/flappy-bird-ai-v1-20260407.html` — our existing NEAT flappy bird implementation
- Deliverable: AI architecture document — network topology, state space, action space, training loop design

### Phase 2: Design Ideation (Q33N synthesizes research)

After research bees return:
- Synthesize findings into a unified game design document
- Define: exact enemy roster (per level), weapon progression tree, boss mechanics, AI state space
- Create pixel art style guide (CSS-only, no sprites — geometric shapes with glow effects)
- Write the design doc to `.deia/hive/responses/`

### Phase 3: Build (phased specs, sequenced with dependencies)

Break the build into specs roughly like this (adjust based on research):

1. **Game engine core** — canvas renderer, game loop, entity system, collision detection
2. **Player + controls** — ship, movement, shooting, PC keyboard + mobile touch
3. **Enemy system** — enemy types, spawn patterns, formations, difficulty scaling
4. **Weapon system** — power-ups, weapon tiers, upgrades, bombs
5. **Level progression** — 10 levels, transitions, boss fights
6. **Scoring + UI** — HUD, score, combo, lives, game over, high scores (localStorage)
7. **Sound** — Web Audio API synthesized effects (shoot, explosion, power-up, boss warning)
8. **AI system** — NEAT neuroevolution, training loop, auto-play mode, hybrid mode
9. **Mobile polish** — responsive layout, touch controls, performance tuning
10. **Integration + E2E test** — full game assembled, all modes working, smoke test

Each build spec must have:
- Explicit file paths
- Acceptance criteria with smoke tests
- "EXECUTE mode" directive
- Dependencies on prior specs

### Phase 4: Verification

Final spec verifies:
- All 10 levels playable
- Weapons upgrade correctly
- AI learns and improves
- Mobile controls work
- Performance hits 60fps
- Sound effects play

---

## Output

### Research specs go to:
`.deia/hive/queue/backlog/SPEC-RAIDEN-R01-*.md` etc.

### Design doc goes to:
`.deia/hive/responses/20260407-RAIDEN-DESIGN-DOC.md`

### Build specs go to:
`.deia/hive/queue/backlog/SPEC-RAIDEN-1XX-*.md`

### Your coordination response goes to:
`.deia/hive/responses/20260407-RAIDEN-COORDINATION-RESPONSE.md`

---

## Constraints
- You are in EXECUTE mode. Create all research and build specs. Do NOT ask for approval. Queue everything.
- Every spec you create must include: "You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it."
- Target file: `browser/public/games/raiden-v1-20260407.html` (single file, everything inline)
- All research specs use model: sonnet
- All build specs use model: sonnet
- No file over 500 lines — if the game exceeds this, the builder must use aggressive minification or split into modules loaded via inline script tags within the same HTML file
- No external dependencies. No npm. No CDN. Everything self-contained.
- The game must be FUN. This is entertainment, not a tech demo.

## Smoke Test
```bash
test -f ".deia/hive/responses/20260407-RAIDEN-COORDINATION-RESPONSE.md" && echo RESPONSE
ls .deia/hive/queue/backlog/SPEC-RAIDEN-*.md | wc -l
```

## Response Location
`.deia/hive/responses/20260407-RAIDEN-COORDINATION-RESPONSE.md`

## Triage History
- 2026-04-10T03:29:28.747626Z — requeued (empty output)
- 2026-04-12T18:52:40.095926Z — requeued (empty output)
- 2026-04-12T18:57:40.156447Z — requeued (empty output)
