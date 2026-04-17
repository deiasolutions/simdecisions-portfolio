---
id: FLAPPY-B04
priority: P2
model: sonnet
role: bee
depends_on: [FLAPPY-B03]
---
# SPEC-FLAPPY-B04: Visualization — HUD, Neural Network Display, Bird Coloring

## Priority
P2

## Model Assignment
sonnet

## Role
bee

## Depends On
- FLAPPY-B03 (training loop integration)

## Objective
Build the visualization layer: HUD with stats, neural network visualization for the best bird, bird coloring by species, and best bird highlighting.

## Context
This is Phase 4 of the Flappy Bird AI v2 build. The game works, the AI learns, now make it VISIBLE and UNDERSTANDABLE.

The user should be able to watch:
- Which birds are alive (color-coded by species)
- Which bird is the best (highlighted)
- What the best bird's brain is doing (live neural network visualization)
- How the population is improving (HUD stats)

## You are in EXECUTE mode
**Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.**

## Files to Read First
- `browser/public/games/flappy-b03-training.js`
  Training loop from Phase 3
- `.deia/hive/responses/20260414-FLAPPY-V2-DESIGN-DOC.md`
  Design document with UX details
- `.deia/hive/responses/20260414-FLAPPY-R01-FINDINGS.md`
  Research findings on neural network visualization

## Deliverables

### 1. HUD Display
- [ ] Generation number
- [ ] Alive count (updates in real-time as birds die)
- [ ] Best score (this generation)
- [ ] Best score (all time)
- [ ] Species count
- [ ] Layout per design doc (grid or horizontal)
- [ ] Style: clean, readable, non-intrusive

### 2. Bird Coloring by Species
- [ ] Assign each species a unique color (HSL palette)
- [ ] Color birds by their species
- [ ] Species colors persist across generations (species 1 always blue, species 2 always red, etc.)
- [ ] Handle species extinction (reuse colors)

### 3. Best Bird Highlighting
- [ ] Identify the bird with highest fitness (or most pipes passed if tied)
- [ ] Highlight with outline, marker, or brighter color
- [ ] Update best bird in real-time (if a different bird takes the lead)

### 4. Neural Network Visualization
- [ ] Draw the best bird's neural network on canvas
- [ ] Layout: input layer (5 nodes) → hidden layer (X nodes) → output layer (1 node)
- [ ] Arrange nodes vertically per layer, layers horizontally
- [ ] Draw connections (lines between nodes)
- [ ] Color nodes by activation level (gradient from inactive to active)
- [ ] Line thickness or color by connection weight (positive vs negative, strong vs weak)
- [ ] Update live every frame (show network activating as bird makes decisions)
- [ ] Position: corner of canvas or separate panel (per design doc)

### 5. Rendering Optimizations
- [ ] At 10x speed, skip bird rendering (update HUD + neural net only)
- [ ] At 1x speed, render everything
- [ ] Ensure 60fps with all visualizations at 1x speed

## Test Requirements

Create: `browser/public/games/flappy-b04-test.html` (visualization test file)

Test scenarios:
- [ ] HUD displays correct values (generation, alive count, scores, species count)
- [ ] HUD updates in real-time as birds die
- [ ] Birds are colored by species (verify by watching multiple species)
- [ ] Best bird is highlighted (verify by watching highlighted bird change if another bird takes lead)
- [ ] Neural network displays 5 input nodes, X hidden nodes, 1 output node (X from design doc)
- [ ] Neural network connections are visible
- [ ] Neural network nodes change color/intensity as network activates
- [ ] Neural network updates live (not frozen)
- [ ] At 10x speed, rendering is skipped but HUD still updates
- [ ] No performance degradation (still 60fps at 1x speed)

Manual test:
- Run for 10 generations at 1x speed
- Watch birds die and HUD update
- Watch best bird highlight move to new leader
- Watch neural network activate (nodes light up when bird decides to flap)

## Constraints
- No external dependencies. Canvas API only. Vanilla JS.
- Target ~100 lines for this phase
- Neural network visualization must be readable (not cluttered)
- Colors must be visually distinct (not 50 shades of blue)
- No stubs — every function fully implemented

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260414-FLAPPY-B04-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test scenarios, manual test observations
5. **Build Verification** — performance check (fps, rendering)
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Output Location
`browser/public/games/flappy-b04-viz.js` — visualization code (will integrate into single HTML later)
`browser/public/games/flappy-b04-test.html` — test harness
`.deia/hive/responses/20260414-FLAPPY-B04-RESPONSE.md` — response file

## Acceptance Criteria
- [ ] HUD displays generation, alive count, best score (gen + all-time), species count
- [ ] HUD updates in real-time as birds die
- [ ] Birds colored by species using distinct HSL colors
- [ ] Best bird highlighted with outline or marker, updates in real-time
- [ ] Neural network visualization: 5 input → X hidden → 1 output nodes displayed
- [ ] Network connections visible with weight-based color/thickness
- [ ] Node colors update live based on activation level
- [ ] At 10x speed, bird rendering skipped but HUD still updates
- [ ] 60fps maintained at 1x speed with all visualizations
- [ ] Visualization code at `browser/public/games/flappy-b04-viz.js`
- [ ] Response file at `.deia/hive/responses/20260414-FLAPPY-B04-RESPONSE.md`

## Smoke Test
- [ ] `test -f browser/public/games/flappy-b04-viz.js` passes
- [ ] `test -f browser/public/games/flappy-b04-test.html` passes
- [ ] `test -f .deia/hive/responses/20260414-FLAPPY-B04-RESPONSE.md` passes
