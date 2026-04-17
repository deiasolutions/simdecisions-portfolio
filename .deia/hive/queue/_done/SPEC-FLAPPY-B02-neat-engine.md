---
id: FLAPPY-B02
priority: P2
model: sonnet
role: bee
depends_on: [FLAPPY-B01]
---
# SPEC-FLAPPY-B02: NEAT Engine Implementation

## Priority
P2

## Model Assignment
sonnet

## Role
bee

## Depends On
- FLAPPY-B01 (game engine core)

## Objective
Build the NEAT neuroevolution engine: genome, neural network, population, mutation, crossover, and speciation.

## Context
This is Phase 2 of the Flappy Bird AI v2 build. You are building the AI brain that will control the birds.

Read the design document from FLAPPY-D01 for exact NEAT parameters (mutation rates, speciation distance, network topology, etc.).

The neural network takes 5 inputs:
1. Bird Y position (normalized 0-1)
2. Bird velocity (normalized)
3. Distance to next pipe (normalized)
4. Next pipe gap Y (normalized)
5. Pipe gap size (normalized)

Output: flap probability (sigmoid, flap if > 0.5)

## You are in EXECUTE mode
**Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.**

## Files to Read First
- `.deia/hive/responses/20260414-FLAPPY-V2-DESIGN-DOC.md`
  Design document with NEAT parameters
- `.deia/hive/responses/20260414-FLAPPY-R01-FINDINGS.md`
  Research findings on NEAT best practices
- `browser/public/games/flappy-bird-ai-v1-20260407.html`
  Reference v1 NEAT implementation (but use design doc parameters, not v1 values)

## Deliverables

### 1. NeuralNetwork Class
- [ ] Constructor: initialize weights, biases for 5-X-1 topology (X from design doc)
- [ ] `predict(inputs)` — forward pass, return output
- [ ] `sigmoid(x)` — activation function
- [ ] `clone()` — deep copy network
- [ ] `mutate(rate)` — weight perturbation, structural mutations
- [ ] `crossover(partner)` — uniform crossover to create child network

### 2. Genome Class (if design recommends separate genome abstraction)
- [ ] Encode network structure (nodes, connections, weights)
- [ ] Innovation numbers for connections (NEAT standard)
- [ ] `distance(other)` — calculate compatibility distance for speciation
- [ ] Structural mutation: add node, add connection
- [ ] Serialize/deserialize for debugging

### 3. Species Class
- [ ] Properties: members (genome indices), representative, stagnation counter
- [ ] `addMember(genomeIndex)` — add genome to species
- [ ] `calculateSharedFitness()` — fitness sharing
- [ ] `selectRepresentative()` — choose new representative for next generation
- [ ] `isStagnant(threshold)` — check if species hasn't improved

### 4. GeneticAlgorithm Class
- [ ] Constructor: create initial random population
- [ ] `nextGeneration()` — selection, crossover, mutation, speciation
- [ ] `selectParent(survivors)` — fitness-proportionate selection
- [ ] `speciate()` — assign genomes to species using distance threshold
- [ ] `calculateFitness()` — fitness = frames_survived + 100 * pipes_passed (or per design doc)
- [ ] `sortByFitness()` — rank population
- [ ] Elite preservation (top N genomes carry over unchanged)

### 5. Speciation Algorithm
- [ ] Implement compatibility distance formula from design doc
- [ ] Distance threshold (from design doc)
- [ ] Assign each genome to species (or create new species)
- [ ] Remove empty species
- [ ] Adjust species fitness sharing

## Test Requirements

Create: `browser/public/games/flappy-b02-test.html` (temporary test file)

Test scenarios:
- [ ] Neural network forward pass produces output in [0, 1]
- [ ] Clone produces identical network (same weights)
- [ ] Mutate changes weights (verify network output differs after mutation)
- [ ] Crossover produces child with mix of parent weights
- [ ] Speciation groups similar genomes (create 2 very different networks, verify different species)
- [ ] Speciation groups similar genomes (create 2 similar networks, verify same species)
- [ ] Elite preservation works (top N genomes survive unchanged)
- [ ] Population evolves over generations (fitness increases)

Create test harness that:
- Initializes population
- Runs 10 generations
- Logs average fitness per generation (should trend upward)
- Logs species count per generation
- Verifies no NaN values in weights/biases

Document test results in response file.

## Constraints
- No external dependencies. Vanilla JS only.
- Target ~200 lines for this phase
- Use exact parameters from design doc (mutation rates, speciation threshold, etc.)
- All networks must use the same 5-X-1 topology (X from design doc)
- No stubs — every function fully implemented

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260414-FLAPPY-B02-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test scenarios, all results
5. **Build Verification** — test output, fitness trends
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Output Location
`browser/public/games/flappy-b02-neat.js` — NEAT engine code (will integrate into single HTML later)
`browser/public/games/flappy-b02-test.html` — test harness
`.deia/hive/responses/20260414-FLAPPY-B02-RESPONSE.md` — response file

## Acceptance Criteria
- [ ] NeuralNetwork class: forward pass produces output in [0, 1]
- [ ] Clone produces identical network with same weights
- [ ] Mutation changes weights (output differs after mutation)
- [ ] Crossover produces child with mix of parent weights
- [ ] Speciation groups similar genomes together, separates different ones
- [ ] Elite preservation: top N genomes survive unchanged
- [ ] Population fitness increases over 10 test generations
- [ ] No NaN values in weights/biases
- [ ] NEAT engine code at `browser/public/games/flappy-b02-neat.js`
- [ ] Response file at `.deia/hive/responses/20260414-FLAPPY-B02-RESPONSE.md`

## Smoke Test
- [ ] `test -f browser/public/games/flappy-b02-neat.js` passes
- [ ] `test -f browser/public/games/flappy-b02-test.html` passes
- [ ] `test -f .deia/hive/responses/20260414-FLAPPY-B02-RESPONSE.md` passes
