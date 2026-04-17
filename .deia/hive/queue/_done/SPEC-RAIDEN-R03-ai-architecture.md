---
id: RAIDEN-R03
priority: P1
model: sonnet
role: bee
depends_on: []
---
# SPEC-RAIDEN-R03: Self-Learning AI Research

## Priority
P1

## Model Assignment
sonnet

## Role
bee (research)

## Depends On
(none)

## Objective
Research neuroevolution and reinforcement learning approaches for arcade game AI. Produce an AI architecture document covering network topology, state representation, action space, reward function, and training loop design for a vertical scrolling shmup.

## Context
We're building a Raiden-style shmup with a self-learning AI that can auto-play the game and improve over time. We have an existing NEAT implementation in `browser/public/games/flappy-bird-ai-v1-20260407.html` as a reference. We need to design the AI system for a much more complex game.

## Research Focus Areas

### 1. NEAT/Neuroevolution for Arcade Games
- How NEAT (NeuroEvolution of Augmenting Topologies) works for real-time games
- Fitness function design for shmups (survival time vs score vs enemies killed)
- Population size, mutation rates, speciation parameters
- Training speed vs quality tradeoffs

### 2. State Space Design
- What should the AI observe?
  - Player position, velocity
  - Enemy positions, types, health
  - Bullet positions (player + enemy)
  - Power-up positions
  - Screen boundaries
  - Current weapon tier
- How to represent this state efficiently (vector encoding, normalization)
- How to handle variable numbers of enemies/bullets (fixed grid sampling vs attention)

### 3. Action Space Design
- What outputs does the AI need?
  - Movement direction (8-way, or continuous X/Y)
  - Fire decision (continuous fire vs when to shoot)
  - Bomb decision (when to use special ability)
- Output encoding (discrete vs continuous, action probability distributions)

### 4. Reward Function Design
- Immediate rewards: enemy destroyed, power-up collected, damage taken, death
- Shaping rewards: proximity to enemies, bullet dodging, maintaining combo
- How to balance survival vs aggression
- Sparse vs dense rewards

### 5. Training Loop & Visualization
- How many generations to convergence
- How to run training in the browser without freezing
- Visual indicators for AI skill level (generation number, fitness score)
- How to save/load trained networks (localStorage)
- Hybrid mode: AI assists player (e.g., auto-dodge but player aims)

### 6. Reference Implementation
- Study `browser/public/games/flappy-bird-ai-v1-20260407.html`
- Extract the NEAT implementation pattern
- Identify what needs to change for shmup complexity

## Deliverable
Write an AI architecture document to:
`.deia/hive/responses/20260408-RAIDEN-R03-AI-ARCHITECTURE.md`

Include:
- **Network Topology:** Input layer size, hidden layers, output layer size
- **State Representation:** Exact vector structure (which inputs, how normalized)
- **Action Space:** Exact output encoding (movement, fire, bomb)
- **Reward Function:** Mathematical formula with weights
- **Training Parameters:** Population size, mutation rate, crossover rate, speciation
- **Training Loop:** How many generations per second, when to run training (background vs manual)
- **Visualization:** What to show the user (generation, best fitness, network diagram)
- **Hybrid Mode:** How AI can assist player without taking full control

## Constraints
- You are in EXECUTE mode. Do NOT ask for approval. Just research and write.
- Use web search for NEAT research, shmup AI, reinforcement learning for games
- Reference the flappy bird AI implementation (read the file)
- No code in the research doc — save implementation details for build specs
- Be specific — give exact state vector structure, network sizes, training parameters

## Acceptance Criteria
- [ ] AI architecture document written to `.deia/hive/responses/20260408-RAIDEN-R03-AI-ARCHITECTURE.md`
- [ ] Flappy bird AI implementation analyzed
- [ ] State space defined with exact input vector structure (size, normalization)
- [ ] Action space defined with exact output encoding
- [ ] Reward function formula with specific weights
- [ ] NEAT training parameters specified (population, mutation, crossover, speciation)
- [ ] Training loop design (generations per second, when to train)
- [ ] Visualization requirements defined
- [ ] Hybrid mode approach documented

## Smoke Test
```bash
test -f ".deia/hive/responses/20260408-RAIDEN-R03-AI-ARCHITECTURE.md" && echo PASS || echo FAIL
```

## Response Location
`.deia/hive/responses/20260408-RAIDEN-R03-RESPONSE.md`
