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
bee (b33 — you research and document findings)

## Depends On
(none)

## Objective
Research neuroevolution/reinforcement learning approaches for a self-learning shmup AI, using our existing flappy bird AI as a reference.

## You are in EXECUTE mode
Write all research and documentation. Do NOT enter plan mode. Do NOT ask for approval. Just research and document.

## Research Scope

### 1. Review Existing Implementation
Read and analyze:
- File: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\public\games\flappy-bird-ai-v1-20260407.html`
- Understand: NEAT implementation, genome structure, mutation rates, fitness function, visualization

### 2. NEAT for Shmups
Research and document:
- How to adapt NEAT (NeuroEvolution of Augmenting Topologies) for shoot-em-up games
- State space design: what does the AI observe? (player pos, enemy positions, bullet positions, power-ups)
- Action space design: what can the AI control? (move X, move Y, fire, bomb)
- Network topology: input nodes, hidden layers, output nodes
- Is NEAT overkill? Could a simpler genetic algorithm work?

### 3. Fitness Function Design
Research and document:
- How to reward the AI for good play (survival time, score, enemies killed, power-ups collected, damage taken)
- How to balance exploration vs exploitation
- Early-game vs late-game fitness (should AI learn level-by-level or holistically?)
- Specific fitness formula recommendation

### 4. Training Loop
Research and document:
- Population size (how many AI agents per generation?)
- Generation lifecycle (how long does each generation live? when to evaluate fitness?)
- Mutation rates (connection weights, add node, add connection, enable/disable)
- Selection strategy (elitism, tournament, roulette wheel)
- How to visualize training progress (generation number, best fitness, current high score)

### 5. Real-Time Learning vs Offline Training
Research and document:
- Should the AI train in real-time as the player watches? (like flappy bird AI)
- Or should we pre-train offline and ship a trained model?
- Pros/cons of each approach for a shmup

### 6. Hybrid Mode (AI-Assisted Play)
Research and document:
- How can the AI assist a human player? (auto-dodge bullets, suggest optimal movement)
- Shared control mechanics (player aims, AI moves to avoid bullets)
- UI indicators (show AI suggestion vs player input)

### 7. State Representation
Research and document:
- How many enemies/bullets should the AI observe? (closest 5? all on screen? grid-based representation?)
- Distance metrics (Euclidean vs Manhattan vs grid cells)
- Normalization (how to scale positions to 0-1 range for neural network)
- Temporal information (velocity, trajectory prediction)

## Deliverables

### File: `.deia/hive/responses/20260413-RAIDEN-R03-AI-RESEARCH.md`

Structure:
```markdown
# Self-Learning Shmup AI Research

## 1. Approach: NEAT vs Alternatives
**Recommendation:** NEAT / Simple GA / Q-Learning

**Rationale:** [why this approach fits shmup gameplay best]

**Reference:** Flappy bird AI uses NEAT successfully for similar dodge-and-survive mechanics.

## 2. State Space Design
**Inputs (what the AI observes):**
- Player position (x, y) — normalized to 0-1
- Player velocity (vx, vy) — normalized
- Closest 5 enemies: (x, y, type, hp) — 20 inputs
- Closest 10 bullets: (x, y, vx, vy) — 40 inputs
- Closest 3 power-ups: (x, y, type) — 9 inputs
- Current weapon tier (0-5) — 1 input
- Current health/lives (0-3) — 1 input

**Total Input Nodes:** ~72

**Simplification Options:** Grid-based representation (10x10 grid of enemy/bullet density) reduces to 100 inputs

## 3. Action Space Design
**Outputs (what the AI controls):**
- Move X: [-1, 1] (left/right)
- Move Y: [-1, 1] (up/down)
- Fire: [0, 1] (threshold 0.5 = fire)
- Bomb: [0, 1] (threshold 0.8 = bomb, rare action)

**Total Output Nodes:** 4

## 4. Network Topology
**Initial Structure:**
- Input layer: 72 nodes (or 100 if grid-based)
- Hidden layer: 0 nodes (NEAT starts minimal, evolves complexity)
- Output layer: 4 nodes

**Evolution:**
- NEAT adds hidden nodes and connections as needed
- Mutation rates: add_node=0.03, add_connection=0.05, weight_mutate=0.8

## 5. Fitness Function
**Formula:**
```
fitness = (survival_time * 10)
        + (score * 0.1)
        + (enemies_killed * 50)
        + (power_ups_collected * 100)
        - (damage_taken * 200)
        + (level_reached * 1000)
```

**Rationale:**
- Survival is important but not enough (prevents camping)
- Score rewards aggressive play
- Power-ups encourage strategic collection
- Damage penalty prevents reckless play
- Level progression is most valuable

## 6. Training Loop
**Population Size:** 50 genomes per generation

**Generation Lifecycle:**
- Each genome plays until death or 60 seconds (whichever comes first)
- Fitness evaluated at end of each run
- Top 10 genomes survive (elitism)
- Remaining 40 slots filled by crossover + mutation

**Selection:** Tournament selection (pick 5 random, choose best, repeat)

**Mutation Rates:**
- Weight mutation: 80%
- Add connection: 5%
- Add node: 3%
- Enable/disable connection: 2%

## 7. Real-Time Learning
**Recommendation:** Real-time training (like flappy bird AI)

**Rationale:**
- Watching the AI learn is engaging and educational
- No need for pre-training infrastructure
- Player can toggle AI on/off and see improvement over time

**Visualization:**
- Top-left corner: "AI Generation: 42 | Best Score: 12,450"
- Color-code AI ship (blue = AI, white = player)

## 8. Hybrid Mode
**Recommendation:** Optional AI-assist mode

**Mechanics:**
- AI controls movement (dodge bullets)
- Player controls firing (aim and shoot)
- Toggle with "H" key

**UI:**
- Ghost overlay showing AI's intended movement
- Smoothly blend player input with AI suggestion (weighted average)

## 9. Implementation Notes
**Performance:**
- Run 1 AI genome per frame during training (not all 50 in parallel, too slow)
- Serialize best genome to localStorage after each generation
- Load best genome on page reload

**Code Reuse:**
- Copy NEAT implementation from flappy-bird-ai-v1-20260407.html
- Adapt fitness function and state/action mappings
- Keep visualization patterns (generation counter, fitness graph)

## 10. Testing Strategy
**Validation:**
- AI should survive longer than random movement by generation 10
- AI should reach level 2 by generation 20
- AI should collect power-ups intentionally by generation 30
- AI should beat average human player by generation 50

**Metrics:**
- Track: avg survival time, max score, avg level reached per generation
- Log best genome to console for analysis
```

## Acceptance Criteria
- [ ] AI approach selected (NEAT recommended) with rationale
- [ ] State space fully defined (input nodes, normalization)
- [ ] Action space fully defined (output nodes, thresholds)
- [ ] Fitness function formula provided with weights
- [ ] Training loop parameters specified (population size, mutation rates, selection)
- [ ] Real-time vs offline training decision made
- [ ] Hybrid mode mechanics designed
- [ ] Implementation notes referencing flappy bird AI provided
- [ ] All sections complete (no TBD, no placeholders)

## Smoke Test
```bash
test -f ".deia/hive/responses/20260413-RAIDEN-R03-AI-RESEARCH.md" && \
grep -q "State Space Design" ".deia/hive/responses/20260413-RAIDEN-R03-AI-RESEARCH.md" && \
grep -q "Fitness Function" ".deia/hive/responses/20260413-RAIDEN-R03-AI-RESEARCH.md" && \
grep -q "NEAT" ".deia/hive/responses/20260413-RAIDEN-R03-AI-RESEARCH.md" && \
echo "PASS"
```

## Response Location
`.deia/hive/responses/20260413-RAIDEN-R03-AI-RESEARCH-RESPONSE.md`
