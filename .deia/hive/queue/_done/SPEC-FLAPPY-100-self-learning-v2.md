---
id: FLAPPY-100
priority: P1
model: sonnet
role: queen
depends_on: []
---
# SPEC-FLAPPY-100: Self-Learning Flappy Bird v2 — Master Coordination Spec

## Priority
P1

## Model Assignment
sonnet

## Role
queen (Q33N coordinator — dispatch research, design, and build bees)

## Depends On
(none)

## Acceptance Criteria

- [ ] Playable Flappy Bird game at browser/public/games/flappy-bird-ai-v2-*.html
- [ ] NEAT neuroevolution with 50+ simultaneous birds
- [ ] AI visibly improves over generations (gen 1 terrible, gen 50+ near-perfect)
- [ ] HUD with generation count, alive count, best scores, species count
- [ ] Speed controls (1x, 3x, 10x)
- [ ] Neural network visualization for best bird
- [ ] Mobile responsive with touch controls
- [ ] Single HTML file, no external dependencies

## Intent
Coordinate the build of a new self-learning Flappy Bird game. This is a Q33N + bees effort. Research first, then design, then build.

An existing v1 is at `browser/public/games/flappy-bird-ai-v1-20260407.html` (504 lines, NEAT neuroevolution). This is a fresh build — study v1 for lessons learned, then build something better.

---

## Game Requirements

### Core Gameplay
- Classic Flappy Bird mechanics — bird with gravity, tap/spacebar to flap, scrolling pipes with random gaps
- Score = pipes passed
- Game over on collision with pipe or ground/ceiling
- Smooth 60fps, polished feel

### Self-Learning AI
- **NEAT neuroevolution** — population of 50+ birds learning simultaneously
- All birds visible on screen at once, color-coded by species
- Best bird highlighted
- AI inputs: bird_y, bird_velocity, dist_to_next_pipe, pipe_gap_y, pipe_gap_size (normalized 0-1)
- AI output: flap probability (sigmoid, flap if > 0.5)
- Fitness: frames_survived + 100 * pipes_passed
- Selection: top 20% survive, mutation (weight perturbation, add connection, add node), crossover, elitism top 5
- Species grouping to protect innovation
- **The AI must visibly improve** — generation 1 should be terrible, generation 10+ should be competent, generation 50+ should be near-perfect

### Display
- HUD: generation #, alive count, best score (this gen), best score (all time), species count
- Speed controls: 1x, 3x, 10x (skip rendering for fast training)
- Auto-advance to next generation when all birds die
- Neural network visualization for the best bird (nodes + connections, live activation display)

### Controls
- **PC:** Spacebar to flap in manual mode, R to restart evolution, 1/3/0 for speed
- **Mobile:** Tap to flap, on-screen buttons for speed and restart
- Toggle between human play and AI mode

### Technical
- Single HTML file: `browser/public/games/flappy-bird-ai-v2-20260407.html`
- Canvas API only, no external dependencies
- All NEAT code written from scratch in vanilla JS
- Mobile responsive

---

## Your Coordination Plan

### Phase 1: Research (1 bee)

**SPEC-FLAPPY-R01: V1 Audit + NEAT Improvements Research**
- Read `browser/public/games/flappy-bird-ai-v1-20260407.html` thoroughly
- Assess: does the v1 AI actually learn? What's broken, what works?
- Research NEAT best practices for this problem: optimal population size, mutation rates, speciation thresholds
- Research: neural network visualization approaches (live node activation display)
- Deliverable: Findings doc with specific recommendations for v2 architecture

### Phase 2: Design (Q33N synthesizes research into a design doc)

- Game design: pipe generation, difficulty curve, visual style
- AI design: exact NEAT parameters, network topology, training schedule
- UX design: HUD layout, speed controls, mode switching, mobile touch zones
- Write to `.deia/hive/responses/`

### Phase 3: Build (phased specs)

Break into roughly:
1. **Game engine** — canvas, game loop, bird physics, pipe generation, collision, scoring
2. **NEAT engine** — genome, neural network, population, mutation, crossover, speciation, selection
3. **Training loop** — multi-bird simulation, fitness evaluation, generation advancement, speed control
4. **Visualization** — HUD, neural network display, bird coloring by species, best bird highlight
5. **Controls + mobile** — keyboard, touch, mode toggle, responsive layout
6. **Polish + integration** — sound effects (Web Audio), particle effects, smooth transitions, final assembly

Each build spec must include the EXECUTE mode directive.

### Phase 4: Verification

- AI visibly improves over generations
- All controls work (PC + mobile)
- Speed controls work
- Neural network visualization is live
- 60fps with 50 birds

---

## Output

- Research specs: `.deia/hive/queue/backlog/SPEC-FLAPPY-R01-*.md`
- Design doc: `.deia/hive/responses/20260407-FLAPPY-V2-DESIGN-DOC.md`
- Build specs: `.deia/hive/queue/backlog/SPEC-FLAPPY-1XX-*.md`
- Coordination response: `.deia/hive/responses/20260407-FLAPPY-V2-COORDINATION-RESPONSE.md`

## Constraints
- You are in EXECUTE mode. Create all research and build specs. Do NOT ask for approval. Queue everything.
- Every sub-spec must include: "You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it."
- Target file: `browser/public/games/flappy-bird-ai-v2-20260407.html`
- No file over 500 lines — use tight code, no verbose comments
- No external dependencies. Canvas API only. Vanilla JS.
- The game must be FUN TO WATCH. Seeing 50 birds flail and gradually learn is the entertainment.

## Smoke Test
```bash
test -f ".deia/hive/responses/20260407-FLAPPY-V2-COORDINATION-RESPONSE.md" && echo RESPONSE
ls .deia/hive/queue/backlog/SPEC-FLAPPY-*.md | wc -l
```

## Response Location
`.deia/hive/responses/20260407-FLAPPY-V2-COORDINATION-RESPONSE.md`

## Triage History
- 2026-04-09T15:50:45.754461Z — requeued (empty output)
- 2026-04-09T15:55:45.815579Z — requeued (empty output)
- 2026-04-10T05:41:49.965579Z — requeued (empty output)
