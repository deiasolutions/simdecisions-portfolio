---
id: FLAPPY-D01
priority: P2
model: sonnet
role: queen
depends_on: [FLAPPY-R01]
---
# SPEC-FLAPPY-D01: V2 Design Synthesis

## Priority
P2

## Model Assignment
sonnet

## Role
queen (Q33N — coordinator, NOT bee)

## Depends On
- FLAPPY-R01 (research findings)

## Objective
Synthesize the research findings from FLAPPY-R01 into a comprehensive design document for Flappy Bird AI v2.

## Context
After FLAPPY-R01 completes, you will have:
- V1 audit report (what's broken, what works)
- NEAT parameter recommendations
- Neural network visualization approach
- Speciation algorithm

Your job: synthesize this into a concrete design document that build bees can follow.

## You are in COORDINATE mode
You are Q33N. You read research findings, synthesize them into a design, and write the design doc. You do NOT write code. You do NOT dispatch bees for this task — this is YOUR work.

## Files to Read First
- `.deia/hive/responses/20260414-FLAPPY-R01-FINDINGS.md`
  Research findings from FLAPPY-R01
- `browser/public/games/flappy-bird-ai-v1-20260407.html`
  Reference the v1 implementation

## Deliverables

### 1. Game Design Section
- [ ] Canvas size and aspect ratio
- [ ] Bird physics (gravity, jump velocity, terminal velocity)
- [ ] Pipe generation algorithm (spacing, gap size, gap Y randomization)
- [ ] Difficulty curve (does pipe gap narrow over time? does speed increase?)
- [ ] Visual style (colors, shapes, effects)
- [ ] Score calculation
- [ ] Collision detection approach

### 2. AI Design Section
- [ ] Exact NEAT parameters (population size, elite count, survival rate, mutation rate, crossover rate)
- [ ] Network topology (5 inputs → X hidden nodes → 1 output, specify X)
- [ ] Speciation algorithm with distance formula and threshold
- [ ] Fitness function formula (exact weights for frames vs pipes)
- [ ] Selection strategy (roulette wheel, tournament, rank-based)
- [ ] Mutation types and probabilities (weight perturbation, add connection, add node)
- [ ] Crossover strategy (uniform, single-point, or other)
- [ ] Training schedule (how many generations to "good", expected learning curve)

### 3. UX Design Section
- [ ] HUD layout (generation, alive count, best score gen, best score ever, species count)
- [ ] Speed controls (1x, 3x, 10x) — how do they work? Skip rendering at 10x?
- [ ] Mode switching (human play vs AI mode) — how to toggle?
- [ ] Best bird highlighting (color, outline, or marker)
- [ ] Species visualization (color-code birds by species)
- [ ] Mobile touch zones (tap to flap, buttons for speed/restart)
- [ ] Neural network visualization panel (where on screen, how big, what info shown)

### 4. Technical Architecture
- [ ] File structure within the single HTML (sections: styles, game engine, NEAT engine, UI, main loop)
- [ ] Module boundaries (what functions belong where)
- [ ] Rendering strategy (60fps with 50 birds, how to optimize)
- [ ] State management (game state, generation state, UI state)
- [ ] How to keep under 500 lines (what to compress, what to omit)

### 5. Build Phase Plan
Break the build into logical phases:
- Phase 1: Game engine (bird, pipes, collision, scoring)
- Phase 2: NEAT engine (genome, network, mutation, crossover, speciation)
- Phase 3: Training loop (population, generation advancement, fitness)
- Phase 4: Visualization (HUD, neural network display, bird coloring)
- Phase 5: Controls + mobile (keyboard, touch, mode toggle)
- Phase 6: Polish + integration (sound, effects, final assembly)

For each phase, specify:
- What gets built
- What file(s) get created/modified
- How many lines of code expected
- Test criteria

## Test Requirements
This is a design task. No code tests required.

Validation:
- [ ] Design document is complete and actionable
- [ ] All numeric parameters are specified
- [ ] Build phases are clear and non-overlapping
- [ ] Total expected code size is under 500 lines

## Constraints
- Target file: `browser/public/games/flappy-bird-ai-v2-20260407.html` (single file)
- No external dependencies. Canvas API only. Vanilla JS.
- No file over 500 lines — design must fit this constraint
- AI must visibly improve over generations (gen 1 terrible, gen 50+ near-perfect)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260414-FLAPPY-D01-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Output Location
`.deia/hive/responses/20260414-FLAPPY-V2-DESIGN-DOC.md` — the design document
`.deia/hive/responses/20260414-FLAPPY-D01-RESPONSE.md` — standard response file

## Acceptance Criteria
- [ ] Design document at `.deia/hive/responses/20260414-FLAPPY-V2-DESIGN-DOC.md` exists and is complete
- [ ] All NEAT parameters are numerically specified (population size, mutation rates, etc.)
- [ ] Game physics parameters are numerically specified (gravity, jump velocity, etc.)
- [ ] Build phases are clearly defined with non-overlapping scope
- [ ] Total expected code size fits under 500 lines
- [ ] Response file at `.deia/hive/responses/20260414-FLAPPY-D01-RESPONSE.md` exists

## Smoke Test
- [ ] `test -f .deia/hive/responses/20260414-FLAPPY-V2-DESIGN-DOC.md` passes
- [ ] `test -f .deia/hive/responses/20260414-FLAPPY-D01-RESPONSE.md` passes
