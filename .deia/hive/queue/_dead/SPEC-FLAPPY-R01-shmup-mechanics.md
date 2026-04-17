---
id: FLAPPY-R01
priority: P2
model: sonnet
role: bee
depends_on: []
---
# SPEC-FLAPPY-R01: V1 Audit + NEAT Improvements Research

## Priority
P2

## Model Assignment
sonnet

## Role
bee

## Depends On
(none)

## Objective
Audit the existing v1 Flappy Bird AI and research optimal NEAT parameters and neural network visualization techniques for v2.

## Context
The v1 implementation exists at `browser/public/games/flappy-bird-ai-v1-20260407.html` (504 lines). It has basic NEAT neuroevolution with 50 birds but the speciation system is trivial (line 389 just groups all birds together). The AI does learn but could be better tuned.

V2 needs:
- Real speciation to protect innovation
- Better mutation/crossover parameters
- Live neural network visualization for the best bird
- Visibly better learning curve (gen 1 terrible → gen 50+ near-perfect)

## You are in EXECUTE mode
**Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.**

## Files to Read First
- `browser/public/games/flappy-bird-ai-v1-20260407.html`
  Read thoroughly to understand current implementation

## Deliverables

### 1. V1 Audit Report
- [ ] Does the v1 AI actually learn? Document learning curve observations
- [ ] What's broken? (speciation, mutation rates, fitness function, etc.)
- [ ] What works well? (game mechanics, rendering, controls)
- [ ] Specific file locations and line numbers of issues

### 2. NEAT Best Practices Research
- [ ] Optimal population size for this problem (canvas-based Flappy Bird)
- [ ] Mutation rates: weight perturbation vs structural mutations (add node/connection)
- [ ] Speciation: distance threshold formula, compatibility distance calculation
- [ ] Crossover strategy: uniform vs single-point
- [ ] Elite preservation count
- [ ] Fitness function tuning (frames_survived weight vs pipes_passed weight)

### 3. Neural Network Visualization Research
- [ ] How to visualize a 5-8-1 network (input-hidden-output) on canvas
- [ ] Live activation display (color nodes by activation level)
- [ ] Connection weight visualization (line thickness or color)
- [ ] Layout algorithms for clean network display
- [ ] How to animate the network during gameplay

### 4. Recommendations Document
- [ ] Exact NEAT parameters for v2 (all numeric values specified)
- [ ] Speciation algorithm with distance formula
- [ ] Network topology recommendations (5 inputs, how many hidden layers/nodes, 1 output)
- [ ] Training schedule (how many generations, what success looks like)
- [ ] Neural network visualization approach with pseudo-code or algorithm description

## Test Requirements
This is a research task. No code tests required.

Validation:
- [ ] Findings document is clear and actionable
- [ ] All numeric parameters are specified (not "tune as needed")
- [ ] Speciation algorithm is mathematically defined
- [ ] Visualization approach has enough detail to implement

## Constraints
- No external dependencies. All research must be implementable with vanilla JS and Canvas API.
- All parameters must be specific numeric values, not ranges or "tune to taste"
- Focus on what makes the AI visibly improve over generations

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260414-FLAPPY-R01-RESPONSE.md`

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
`.deia/hive/responses/20260414-FLAPPY-R01-FINDINGS.md` — research findings document
`.deia/hive/responses/20260414-FLAPPY-R01-RESPONSE.md` — standard bee response file

## Smoke Test
```bash
test -f ".deia/hive/responses/20260414-FLAPPY-R01-FINDINGS.md" && echo FINDINGS
test -f ".deia/hive/responses/20260414-FLAPPY-R01-RESPONSE.md" && echo RESPONSE
```
