---
id: FLAPPY-B03
priority: P2
model: sonnet
role: bee
depends_on: [FLAPPY-B01, FLAPPY-B02]
---
# SPEC-FLAPPY-B03: Training Loop Integration

## Priority
P2

## Model Assignment
sonnet

## Role
bee

## Depends On
- FLAPPY-B01 (game engine core)
- FLAPPY-B02 (NEAT engine)

## Objective
Integrate the game engine with the NEAT engine: multi-bird simulation, AI decision-making, fitness evaluation, generation advancement, and speed controls.

## Context
This is Phase 3 of the Flappy Bird AI v2 build. You are connecting the game to the AI.

The game engine (B01) can run a single bird manually. The NEAT engine (B02) can evolve a population of networks. Now you wire them together so 50 AI-controlled birds play simultaneously and the population evolves over generations.

## You are in EXECUTE mode
**Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.**

## Files to Read First
- `browser/public/games/flappy-b01-engine.js`
  Game engine from Phase 1
- `browser/public/games/flappy-b02-neat.js`
  NEAT engine from Phase 2
- `.deia/hive/responses/20260414-FLAPPY-V2-DESIGN-DOC.md`
  Design document with integration details

## Deliverables

### 1. Multi-Bird Game State
- [ ] Create array of 50 birds (or population size from design doc)
- [ ] Each bird gets its own neural network (from population)
- [ ] All birds share the same pipes (synchronized game state)
- [ ] Track alive count, best bird index

### 2. AI Decision Loop
- [ ] Each frame, for each alive bird:
  - Get next pipe info
  - Normalize inputs (bird Y, velocity, pipe distance, gap Y, gap size)
  - Call `bird.brain.predict(inputs)`
  - Flap if output > 0.5
- [ ] Update all birds
- [ ] Check collisions for all birds
- [ ] Update scores for all birds

### 3. Fitness Evaluation
- [ ] When a bird dies, calculate its fitness: `frames_survived + 100 * pipes_passed` (or per design doc)
- [ ] Store fitness in bird object
- [ ] Track best fitness this generation
- [ ] Track best fitness ever

### 4. Generation Advancement
- [ ] Detect when all birds are dead
- [ ] Pass all bird fitness values to GeneticAlgorithm
- [ ] Call `ga.nextGeneration()`
- [ ] Create new array of birds with new brains from evolved population
- [ ] Reset pipes to starting state
- [ ] Increment generation counter
- [ ] Log generation stats (best score, avg score, species count)

### 5. Speed Controls
- [ ] 1x speed: render every frame (60fps)
- [ ] 3x speed: update 3 times per frame, render every frame
- [ ] 10x speed: update 10 times per frame, skip rendering (update HUD only)
- [ ] UI buttons to switch speed (1x, 3x, 10x)

### 6. Mode Toggle
- [ ] "AI Mode" — 50 birds controlled by NEAT
- [ ] "Human Mode" — 1 bird controlled by spacebar
- [ ] Button to toggle between modes
- [ ] Preserve generation/population state when switching modes

## Test Requirements

Create: `browser/public/games/flappy-b03-test.html` (integration test file)

Test scenarios:
- [ ] 50 birds spawn at generation 1
- [ ] All birds start in same position
- [ ] Birds make different decisions (some flap, some don't)
- [ ] Alive count decreases as birds die
- [ ] Generation advances when all birds die
- [ ] Population size stays at 50 across generations
- [ ] Best score increases over generations (verify at gen 1, 5, 10)
- [ ] Speed controls work (1x, 3x, 10x)
- [ ] At 10x speed, rendering is skipped (verify frame skip)
- [ ] Mode toggle works (switch to human, play manually, switch back to AI)

Run for 20 generations at 10x speed. Document:
- Best score at gen 1, 5, 10, 15, 20
- Species count at gen 1, 5, 10, 15, 20
- Avg score at gen 1, 5, 10, 15, 20

Expected result: best score should increase significantly from gen 1 to gen 20.

## Constraints
- No external dependencies. Vanilla JS only.
- Target ~100 lines for this phase
- Must maintain 60fps at 1x speed with 50 birds
- No stubs — every function fully implemented
- Speed controls must actually speed up training (not just visual)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260414-FLAPPY-B03-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test scenarios, 20-gen training log
5. **Build Verification** — learning curve data (scores at gen 1, 5, 10, 15, 20)
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Output Location
`browser/public/games/flappy-b03-training.js` — training loop code (will integrate into single HTML later)
`browser/public/games/flappy-b03-test.html` — integration test harness
`.deia/hive/responses/20260414-FLAPPY-B03-RESPONSE.md` — response file

## Acceptance Criteria
- [ ] 50 birds spawn at generation 1 with individual neural networks
- [ ] All birds share the same pipe state
- [ ] AI decision loop: each alive bird gets inputs, calls predict, flaps if > 0.5
- [ ] Fitness calculated as frames_survived + 100 * pipes_passed (or per design doc)
- [ ] Generation advances automatically when all birds die
- [ ] Best score increases over 20 generations
- [ ] Speed controls work: 1x (normal), 3x (3 updates/frame), 10x (skip rendering)
- [ ] Mode toggle: AI mode (50 birds) vs Human mode (1 bird, spacebar)
- [ ] Training loop code at `browser/public/games/flappy-b03-training.js`
- [ ] Response file at `.deia/hive/responses/20260414-FLAPPY-B03-RESPONSE.md`

## Smoke Test
- [ ] `test -f browser/public/games/flappy-b03-training.js` passes
- [ ] `test -f browser/public/games/flappy-b03-test.html` passes
- [ ] `test -f .deia/hive/responses/20260414-FLAPPY-B03-RESPONSE.md` passes
