---
id: RAIDEN-108
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-101, RAIDEN-102, RAIDEN-103, RAIDEN-R03]
---
# SPEC-RAIDEN-108: Self-Learning AI (NEAT)

## Priority
P1

## Model Assignment
sonnet

## Role
bee (builder)

## Depends On
- RAIDEN-101 (game engine)
- RAIDEN-102 (player ship)
- RAIDEN-103 (enemy system)
- RAIDEN-R03 (AI architecture research)

## Objective
Implement the self-learning AI using NEAT (NeuroEvolution of Augmenting Topologies). AI can auto-play the game, improve over generations, and optionally assist the player in hybrid mode.

## Context
Reference implementation: `browser/public/games/flappy-bird-ai-v1-20260407.html` (existing NEAT for flappy bird). Adapt for shmup complexity using architecture from RAIDEN-R03 research.

## Technical Requirements

### AI Architecture

**State Space (inputs to neural network):**
- Player position (x, y) — normalized 0-1
- Player velocity (vx, vy) — normalized -1 to 1
- Nearest 3 enemies: position (x, y), type (one-hot encoded)
- Nearest 5 enemy bullets: position (x, y), velocity (vx, vy)
- Nearest power-up: position (x, y), type (one-hot)
- Current weapon tier (one-hot encoded)
- Player health (0-1)
- Total inputs: ~30-40 neurons

**Action Space (outputs from neural network):**
- Movement X (-1 to 1, left/right)
- Movement Y (-1 to 1, up/down)
- Fire (0-1 threshold, > 0.5 = fire)
- Bomb (0-1 threshold, > 0.5 = use bomb)
- Total outputs: 4 neurons

**Network Topology:**
- Start with direct input→output connections (no hidden layers)
- NEAT evolves hidden layers, new connections, new nodes over generations

### NEAT Algorithm
Use simplified NEAT from flappy bird AI:
- Population size: 100 genomes
- Mutation rates: 80% weight mutation, 5% add connection, 3% add node
- Crossover rate: 50%
- Speciation: group similar genomes (compatibility threshold)
- Fitness function: survival time + score + enemies killed - deaths

### Training Loop
- **Manual training mode:** User presses "T" to toggle training
  - Runs population in parallel (fast-forward, no rendering except best genome)
  - Each genome plays until death or time limit (30 seconds)
  - Calculate fitness, evolve next generation
  - Render best genome at normal speed
- **Background training:** Trains while player is in menu (optional)
- **Generation counter:** Display current generation + best fitness

### Auto-Play Mode
- User presses "A" to toggle auto-play
- AI takes control of player ship
- Player can watch AI play at normal speed
- AI uses best genome from current generation
- Visual indicator: "AI PLAYING (Gen X, Fitness: Y)"

### Hybrid Mode (Optional)
- User presses "H" to toggle hybrid mode
- AI handles dodging (movement), player handles aiming (fire/bomb)
- Or: AI aims, player moves
- Experiment with what feels best

### AI Persistence
- Save best genome to localStorage after each generation
- Load saved genome on game start
- "Reset AI" button (deletes saved genome, restarts from random)

### Visualization
- Display network diagram (nodes + connections) for best genome
- Show input activations in real-time (which inputs are firing)
- Show output activations (what AI is deciding)
- Generation stats: best fitness, avg fitness, species count

## Deliverable
Update file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\games\raiden-v1-20260408.html`

Add sections:
- `// ===== NEAT ALGORITHM =====`
- `// ===== AI ARCHITECTURE =====`
- `// ===== TRAINING LOOP =====`
- `// ===== AUTO-PLAY MODE =====`

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- Training does not freeze browser (use requestAnimationFrame batching)
- AI improves visibly over 10-20 generations
- Best genome persists across sessions (localStorage)
- Reference flappy bird AI for NEAT implementation patterns

## Acceptance Criteria
- [ ] NEAT algorithm implemented (mutation, crossover, speciation)
- [ ] State space defined (30-40 inputs as per RAIDEN-R03)
- [ ] Action space defined (4 outputs: move X/Y, fire, bomb)
- [ ] Fitness function balances survival + score + kills
- [ ] Training mode (T key) runs generations
- [ ] Auto-play mode (A key) lets AI play
- [ ] Generation counter + fitness displayed
- [ ] Best genome saves to localStorage
- [ ] Network visualization shows nodes + connections
- [ ] AI improves over generations (fitness increases)
- [ ] Smoke test: press T, watch AI train, see fitness improve

## Smoke Test
```bash
# Manual: Open file in browser
# - Press T → training starts (generation counter increments)
# - Watch best genome play (every generation)
# - Fitness increases over 10-20 generations
# - Press A → AI takes control, plays game
# - Refresh page → AI loads saved genome, resumes skill level
# - Network diagram shows evolving topology
```

## Tests
Write inline tests:
- Genome mutation (weight changes, add node, add connection)
- Crossover (two genomes produce offspring)
- Speciation (similar genomes grouped)
- Fitness calculation (survival time + score + kills)
- State normalization (all inputs in 0-1 range)
- Action thresholding (output > 0.5 = action fires)

## Response Location
`.deia/hive/responses/20260408-RAIDEN-108-RESPONSE.md`
