---
id: FLAPPY-B01
priority: P2
model: sonnet
role: bee
depends_on: [FLAPPY-D01]
---
# SPEC-FLAPPY-B01: Game Engine Core

## Priority
P2

## Model Assignment
sonnet

## Role
bee

## Depends On
- FLAPPY-D01 (design document)

## Objective
Build the core game engine: canvas setup, bird physics, pipe generation, collision detection, scoring, and game loop.

## Context
This is Phase 1 of the Flappy Bird AI v2 build. You are building the foundation that the NEAT AI will sit on top of.

Read the design document from FLAPPY-D01 for exact parameters (gravity, jump velocity, pipe spacing, gap size, etc.).

## You are in EXECUTE mode
**Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.**

## Files to Read First
- `.deia/hive/responses/20260414-FLAPPY-V2-DESIGN-DOC.md`
  Design document with all parameters
- `browser/public/games/flappy-bird-ai-v1-20260407.html`
  Reference for game mechanics (but use design doc parameters, not v1 values)

## Deliverables

### 1. Canvas Setup
- [ ] HTML structure with canvas element
- [ ] Canvas sized per design doc
- [ ] Context and basic rendering setup

### 2. Bird Class
- [ ] Properties: x, y, velocity, alive, score, frames
- [ ] `update()` — apply gravity, update position, check bounds
- [ ] `flap()` — apply jump velocity
- [ ] `draw()` — render bird as circle with eye
- [ ] `reset()` — reset to starting state

### 3. Pipe Class
- [ ] Properties: x, gapY, passed
- [ ] Constructor generates random gap Y per design doc formula
- [ ] `update()` — move pipe left at specified speed
- [ ] `draw()` — render top and bottom pipe segments
- [ ] `collidesWith(bird)` — accurate collision detection
- [ ] `isOffscreen()` — check if pipe passed left edge

### 4. Game State Management
- [ ] Pipe array with spawning logic (spawn at correct spacing)
- [ ] Pipe cleanup (remove offscreen pipes)
- [ ] Score tracking (increment when bird passes pipe)
- [ ] Game over detection (bird hits pipe/bounds)

### 5. Game Loop
- [ ] `update()` — update all game objects
- [ ] `draw()` — render background, ground, pipes, bird
- [ ] `gameLoop()` — main loop with requestAnimationFrame
- [ ] 60fps target

### 6. Manual Play Mode (for testing)
- [ ] Spacebar to flap
- [ ] Single bird controlled by player
- [ ] Score display
- [ ] Restart on game over (R key)

## Test Requirements

Create: `browser/public/games/flappy-b01-test.html` (temporary test file)

Manual test scenarios:
- [ ] Bird falls with gravity when not flapping
- [ ] Bird jumps when spacebar pressed
- [ ] Pipes spawn at correct spacing
- [ ] Collision detection works (bird dies on pipe hit)
- [ ] Collision detection works (bird dies on ceiling/floor hit)
- [ ] Score increments when passing pipes
- [ ] Game runs at smooth 60fps
- [ ] Pipes scroll smoothly
- [ ] Gap Y randomization creates varied difficulty

Document test results in response file (no automated tests for canvas game).

## Constraints
- No external dependencies. Canvas API only. Vanilla JS.
- Target ~150 lines for this phase
- Use exact parameters from design doc (don't guess)
- No hardcoded colors — use descriptive variable names (will add CSS vars in polish phase)
- Bird physics must feel responsive (not floaty, not brick-like)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260414-FLAPPY-B01-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — manual test scenarios, all results
5. **Build Verification** — does game run? is it playable?
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Output Location
`browser/public/games/flappy-b01-engine.js` — game engine code (will integrate into single HTML later)
`browser/public/games/flappy-b01-test.html` — test harness
`.deia/hive/responses/20260414-FLAPPY-B01-RESPONSE.md` — response file

## Acceptance Criteria
- [ ] Canvas renders with correct dimensions from design doc
- [ ] Bird falls with gravity and responds to flap input
- [ ] Pipes spawn at correct spacing and scroll left
- [ ] Collision detection works for pipes, ceiling, and floor
- [ ] Score increments when bird passes a pipe
- [ ] Game loop runs at 60fps
- [ ] Manual play mode works (spacebar to flap, R to restart)
- [ ] Engine code at `browser/public/games/flappy-b01-engine.js`
- [ ] Response file at `.deia/hive/responses/20260414-FLAPPY-B01-RESPONSE.md`

## Smoke Test
- [ ] `test -f browser/public/games/flappy-b01-engine.js` passes
- [ ] `test -f browser/public/games/flappy-b01-test.html` passes
- [ ] `test -f .deia/hive/responses/20260414-FLAPPY-B01-RESPONSE.md` passes
