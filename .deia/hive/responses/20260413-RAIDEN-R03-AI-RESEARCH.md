# Self-Learning Shmup AI Research

## 1. Approach: Simple Neural Network + Genetic Algorithm (Not Full NEAT)
**Recommendation:** Fixed-topology neural network with genetic algorithm (same approach as flappy bird AI)

**Rationale:**
- The flappy bird implementation does NOT use full NEAT (NeuroEvolution of Augmenting Topologies) — it uses a fixed-topology neural network evolved via genetic algorithm
- This simpler approach is sufficient for shmup gameplay where state space is well-defined
- Fixed topology (input → hidden → output) trains faster and is easier to debug
- Genetic algorithm handles evolution (crossover, mutation, elitism) effectively
- Full NEAT adds complexity (topology evolution, speciation) that may not be necessary for dodge-and-shoot mechanics
- The flappy bird AI demonstrates this approach works well for similar survival/dodge gameplay

**Why Not Full NEAT:**
- NEAT's topology evolution is valuable when optimal network structure is unknown
- Shmup state space is clear: positions, velocities, threats — we can design the topology upfront
- Simpler implementation = faster iteration, easier visualization, better performance

## 2. State Space Design
**Inputs (what the AI observes):**

### Option A: Position-Based (72 inputs) — RECOMMENDED
- **Player state (4 inputs):**
  - Player X position (normalized 0-1)
  - Player Y position (normalized 0-1)
  - Player X velocity (normalized -1 to 1)
  - Player Y velocity (normalized -1 to 1)

- **Player status (3 inputs):**
  - Current weapon tier (normalized 0-1, 0=base, 1=max power)
  - Current health/lives (normalized 0-1)
  - Bomb availability (0 or 1)

- **Closest 5 enemies (25 inputs):**
  - For each enemy: X pos, Y pos, X velocity, Y velocity, threat level (1=weak, 0.5=medium, 1=boss)
  - If fewer than 5 enemies, pad with zeros

- **Closest 8 bullets (32 inputs):**
  - For each bullet: X pos, Y pos, X velocity, Y velocity
  - If fewer than 8 bullets, pad with zeros

- **Closest 2 power-ups (8 inputs):**
  - For each power-up: X pos, Y pos, type (weapon=1, health=0.5, bomb=0.75), urgency (distance-based)

**Total Input Nodes:** 72

### Option B: Grid-Based (123 inputs) — ALTERNATIVE
- 10x10 grid of screen sectors (100 cells)
- Each cell encodes: enemy density (0-1), bullet density (0-1), power-up presence (0-1)
- Reduces to 100 inputs but loses precise position data
- Additional 23 inputs for player state, weapon tier, health, etc.

**Recommendation:** Use Option A (position-based). Flappy bird uses 5 position-based inputs successfully — shmup needs more but same principle applies.

## 3. Action Space Design
**Outputs (what the AI controls):**

### 4 Output Nodes:
1. **Move X:** Continuous value [-1, 1]
   - -1 = move left at max speed
   - 0 = no horizontal movement
   - 1 = move right at max speed
   - Implementation: `playerVelocityX = output[0] * maxSpeed`

2. **Move Y:** Continuous value [-1, 1]
   - -1 = move up at max speed
   - 0 = no vertical movement
   - 1 = move down at max speed
   - Implementation: `playerVelocityY = output[1] * maxSpeed`

3. **Fire:** Binary decision via threshold
   - Output > 0.5 = fire weapon
   - Output ≤ 0.5 = don't fire
   - Implementation: `if (output[2] > 0.5) player.fire()`

4. **Bomb:** High-threshold binary decision
   - Output > 0.8 = use bomb (rare, emergency action)
   - Output ≤ 0.8 = don't bomb
   - High threshold prevents wasteful bomb usage
   - Implementation: `if (output[3] > 0.8 && player.bombs > 0) player.useBomb()`

**Total Output Nodes:** 4

## 4. Network Topology
**Initial Structure:**
- **Input layer:** 72 nodes
- **Hidden layer:** 16 nodes (double the flappy bird's 8 nodes, scales with input complexity)
- **Output layer:** 4 nodes
- **Activation:** Sigmoid (0-1 range, same as flappy bird)

**Why Fixed Topology:**
- Clear input/output requirements → no need for topology evolution
- Easier to debug ("which inputs affect which outputs?")
- Faster training (no structural mutation overhead)
- Flappy bird proves 5→8→1 works; 72→16→4 is proportional scaling

**Weight Initialization:**
- Random uniform distribution [-1, 1] (same as flappy bird)
- Biases initialized randomly [-1, 1]

## 5. Fitness Function
**Formula:**
```javascript
fitness = (survivalTime * 10)           // Base survival reward
        + (score * 0.1)                  // Points from gameplay
        + (enemiesKilled * 50)           // Encourage aggression
        + (powerUpsCollected * 100)      // Strategic collection
        - (damageTaken * 200)            // Penalty for taking hits
        + (levelReached * 1000)          // Major milestone reward
        + (accuracy * 500)               // shots hit / shots fired (prevents spam)
```

**Rationale:**
- **Survival (10x):** Core metric, but not dominant (prevents passive camping)
- **Score (0.1x):** Gameplay points are already factored into other metrics, low weight prevents double-counting
- **Enemies killed (50x):** Encourages aggressive play, strategic targeting
- **Power-ups (100x):** High value encourages collection (weapon upgrades = better performance)
- **Damage penalty (-200x):** Strong penalty discourages reckless play
- **Level reached (1000x):** Major milestone, most valuable metric (level 2 = instant 1000 fitness)
- **Accuracy (500x):** Rewards efficient shooting, prevents mindless spam

**Comparison to Flappy Bird:**
- Flappy bird: `fitness = frames + score * 100` (simple survival + pipes passed)
- Shmup: More complex multi-objective balancing (survive + kill + collect + dodge)

## 6. Training Loop
**Population Size:** 50 genomes per generation (same as flappy bird)

**Generation Lifecycle:**
- Each genome plays until death OR 60 seconds (timeout prevents infinite survival with no progress)
- Fitness evaluated at end of each run
- All genomes play simultaneously (parallel simulation, draw all 50 ships on screen)
- Generation ends when all genomes die OR all reach 60-second timeout

**Selection Strategy: Roulette Wheel (Fitness-Proportionate)**
- Total fitness = sum of all genome fitnesses
- Each genome's selection probability = its fitness / total fitness
- Higher fitness = higher probability of being selected as parent
- Allows weaker genomes a chance (genetic diversity)

**Elitism:**
- Top 5 genomes (10% of population) survive unchanged to next generation
- Prevents losing best solutions
- Same as flappy bird's `CONFIG.eliteCount = 5`

**Reproduction:**
- Remaining 45 slots filled by crossover + mutation
- Crossover: Randomly blend parent1 and parent2 weights (gene-by-gene 50/50 coin flip)
- Mutation applied to all children after crossover

**Mutation Rates:**
- **Weight perturbation:** 80% chance per weight
  - 50% chance: small adjustment `weight += random(-0.2, 0.2)`
  - 50% chance: complete replacement `weight = random(-1, 1)`
- **Bias mutation:** Same 80% rate as weights
- **No topology mutation** (fixed structure)

**Implementation (pseudocode from flappy bird pattern):**
```javascript
nextGeneration() {
    // 1. Calculate fitness for all genomes
    population.forEach(genome => genome.calculateFitness());

    // 2. Sort by fitness
    const sorted = [...population].sort((a, b) => b.fitness - a.fitness);

    // 3. Elitism: top 5 survive
    const elite = sorted.slice(0, 5).map(g => g.clone());

    // 4. Survivors pool (top 20% for mating)
    const survivors = sorted.slice(0, 10);

    // 5. Fill remaining 45 slots
    const newPopulation = [...elite];
    while (newPopulation.length < 50) {
        const parent1 = selectParent(survivors); // roulette wheel
        const parent2 = selectParent(survivors);
        const child = parent1.crossover(parent2);
        child.mutate(0.1); // 10% mutation rate (applies to 80% of weights)
        newPopulation.push(child);
    }

    // 6. Reset all genomes for new generation
    population = newPopulation;
    population.forEach(genome => genome.reset());
}
```

## 7. Real-Time Training
**Recommendation:** Real-time training (watch AI learn live)

**Rationale:**
- Flappy bird AI's most engaging feature is watching 50 birds learn simultaneously
- Educational: user sees evolution in action
- No pre-training infrastructure needed
- Debuggable: user can see when AI gets stuck on bad strategy

**Visualization:**
- Show all 50 AI ships simultaneously (color-coded by fitness)
- Best genome highlighted (brighter color, slightly larger)
- HUD displays:
  - Generation number
  - Alive count (50 → 0 as genomes die)
  - Best score this generation
  - Best score ever
  - Current speed multiplier (1x, 3x, 10x for faster training)

**Performance Optimization:**
- Speed controls: 1x (real-time), 3x, 10x (same as flappy bird)
- At 10x: run 10 update cycles per frame, draw once per frame
- This accelerates training without requiring background processing

**Persistence:**
- Save best genome to localStorage after each generation
- On page reload, load best genome and continue from that generation
- Format: JSON serialization of weights/biases

## 8. Hybrid Mode (AI-Assisted Play)
**Recommendation:** Optional AI-assist mode (toggle with "A" key)

**Mode A: Full AI Control**
- AI controls movement and firing
- Player watches (spectator mode)
- Use best genome from training
- Toggle to player control at any time

**Mode B: Movement Assist (RECOMMENDED)**
- AI controls movement only (dodge bullets, collect power-ups)
- Player controls firing (aim and shoot)
- Blended control:
  ```javascript
  playerX = lerp(aiSuggestedX, playerInputX, 0.3) // 70% AI, 30% player
  playerY = lerp(aiSuggestedY, playerInputY, 0.3)
  ```
- Player can override AI by holding keys strongly

**UI Indicators:**
- Ghost overlay: translucent ship showing AI's intended position (0.3 opacity)
- Blue tint on player ship when AI-assist active
- HUD label: "AI ASSIST: ON" in top-right corner

**Use Case:**
- Beginner players learning bullet patterns
- Accessibility feature for players with motor impairments
- "Safety net" mode for difficult sections

## 9. Implementation Notes

### Code Reuse from Flappy Bird AI
**Directly reusable:**
- `NeuralNetwork` class: `predict()`, `sigmoid()`, `clone()`, `mutate()`, `crossover()` (lines 135-222)
- `GeneticAlgorithm` class: `nextGeneration()`, `selectParent()` (lines 339-403)
- Speed controls: 1x/3x/10x buttons (lines 477-493)
- HUD display pattern: generation, alive count, best scores (lines 82-103, 461-465)

**Requires adaptation:**
- Input size: 5 → 72 nodes
- Hidden size: 8 → 16 nodes (proportional scaling)
- Output size: 1 → 4 nodes
- `think()` method: flappy bird detects next pipe, shmup needs nearest threats (lines 274-292)
- Fitness calculation: simple `frames + score * 100` → multi-objective formula (line 295)

**Performance:**
- Flappy bird runs 50 birds at 60fps with no lag
- Shmup has more sprites (enemies, bullets) but same principle
- Use object pooling for bullets/enemies (reuse objects, don't GC churn)
- Limit max bullets/enemies rendered (cull offscreen)

**Training Visualization:**
- Color-code ships by fitness rank (best = green, worst = red, gradient in between)
- Draw ships at 50% opacity when multiple overlap (prevents visual clutter)
- Show fitness values only for top 3 genomes (avoid HUD spam)

### localStorage Schema
```javascript
const checkpoint = {
    generation: 42,
    bestScoreEver: 12450,
    bestGenome: {
        weightsIH: [[...], [...]],  // 72x16 matrix
        weightsHO: [[...], [...]],  // 16x4 matrix
        biasH: [...],               // 16 values
        biasO: [...]                // 4 values
    }
};
localStorage.setItem('shmupAI_checkpoint', JSON.stringify(checkpoint));
```

**Load on startup:**
```javascript
const saved = localStorage.getItem('shmupAI_checkpoint');
if (saved) {
    const checkpoint = JSON.parse(saved);
    generation = checkpoint.generation;
    bestScoreEver = checkpoint.bestScoreEver;
    // Restore best genome to population[0]
    population[0].brain.weightsIH = checkpoint.bestGenome.weightsIH;
    // ... etc
}
```

## 10. Testing Strategy

### Training Validation Milestones
**Generation 5:**
- [ ] AI survives longer than random movement (avg >10 seconds vs <5 seconds random)
- [ ] At least 1 genome reaches score >100

**Generation 10:**
- [ ] AI intentionally dodges bullets (watches velocity vectors, moves away)
- [ ] Avg survival time >20 seconds
- [ ] Best genome reaches score >500

**Generation 20:**
- [ ] AI reaches level 2 (at least 1 genome per generation)
- [ ] AI collects power-ups intentionally (moves toward them when safe)
- [ ] Avg accuracy >30% (shots hit / shots fired)

**Generation 30:**
- [ ] AI prioritizes targets (shoots weak enemies first, avoids boss until powered up)
- [ ] Uses bombs strategically (emergency situations only, not randomly)
- [ ] Best genome reaches score >2000

**Generation 50:**
- [ ] AI beats average human player (score >5000)
- [ ] Avg survival time >60 seconds
- [ ] Fitness plateau detected (improvement <5% per 10 generations)

### Metrics to Track
**Per Generation:**
- Avg survival time (should increase monotonically)
- Max score (best genome's score)
- Avg accuracy (shots hit / shots fired)
- Avg level reached (should progress from 1.0 → 1.5 → 2.0+)
- Elite genome fitness (top 5 avg, should increase)

**Log to console:**
```javascript
console.log(`Gen ${generation}: Best=${bestScore}, Avg Survival=${avgSurvival.toFixed(1)}s, Accuracy=${(avgAccuracy*100).toFixed(1)}%`);
```

**Early stopping criteria:**
- If best score doesn't improve for 50 generations, increase mutation rate to 0.15 (escape local optimum)
- If still no improvement after 100 generations, plateau reached (AI has learned limit of fixed topology)

### Debugging Tools
**Genome inspector (console command):**
```javascript
window.inspectBestGenome = () => {
    const best = population.reduce((a, b) => a.fitness > b.fitness ? a : b);
    console.log('Best Genome:', {
        fitness: best.fitness,
        score: best.score,
        survival: best.frames / 60,
        weightsIH: best.brain.weightsIH,
        weightsHO: best.brain.weightsHO
    });
};
```

**Input visualization (what does AI see?):**
- Draw lines from player to tracked enemies/bullets
- Highlight which inputs are >0.5 (significant threats)
- Show neural network activation (input → hidden → output) in side panel

## 11. Alternative Approaches Considered

### Q-Learning (Reinforcement Learning)
**Not recommended because:**
- Requires discrete state space (hard to discretize continuous shmup positions)
- Q-table size explodes with 72-dimensional state space
- Deep Q-Learning (DQN) requires replay buffer, target network, complex training loop
- Genetic algorithm is simpler and sufficient for this use case

### Full NEAT
**Not recommended because:**
- Topology evolution adds complexity without clear benefit
- Shmup state/action space is well-defined (no need to discover network structure)
- Speciation overhead slows training
- Harder to debug ("why did the network add this connection?")

### Behavior Trees
**Not recommended because:**
- Requires manual rule-writing (not self-learning)
- Brittle against new enemy patterns
- Good for enemy AI, not for learning player AI

### Imitation Learning
**Not recommended because:**
- Requires expert human gameplay data (recording player inputs)
- AI limited by human skill ceiling
- No self-improvement beyond mimicry

## 12. Future Enhancements (Post-V1)

### Transfer Learning
- Train AI on level 1, transfer weights to level 2 starting population
- Speeds up learning for new levels (doesn't start from scratch)

### Curriculum Learning
- Start training with slow bullets, gradually increase speed
- Start with few enemies, gradually increase density
- AI learns fundamentals before facing full difficulty

### Multi-Objective Optimization
- Separate fitness functions for different playstyles (aggressive, defensive, speed-run)
- Evolve multiple specialist genomes, let player choose playstyle

### Ensemble AI
- Run top 5 genomes in parallel, average their outputs
- More robust than single genome (less prone to edge-case failures)

## 13. Expected Training Time

**Hardware assumptions:**
- Modern browser (Chrome/Firefox)
- 60 FPS target
- 50 genomes per generation

**Timeline:**
- **Generation 1-10:** ~5 minutes (genomes die quickly, fast turnover)
- **Generation 10-30:** ~15 minutes (genomes survive longer, slower generations)
- **Generation 30-50:** ~20 minutes (most genomes reach timeout, slow generations)

**Total to "good" AI:** ~40 minutes real-time (10x speed → 4 minutes perceived)

**User patience:**
- 1x speed: engaging to watch for ~10 minutes
- 3x speed: comfortable for ~20 minutes
- 10x speed: use for overnight training (wake up to gen 500+)

## 14. Code Structure Recommendations

### File Organization
```
raiden-ai-v1.html
├── HTML structure (canvas, HUD, controls)
├── Styles (embedded, no external CSS)
├── NeuralNetwork class (~100 lines, copy from flappy bird)
├── Genome class (~150 lines, player ship + brain)
├── GeneticAlgorithm class (~100 lines, copy from flappy bird)
├── Game entities (Enemy, Bullet, PowerUp classes ~50 lines each)
├── Game loop (update, draw, collision ~200 lines)
├── AI training loop (think, fitness calculation ~100 lines)
└── Controls (buttons, localStorage ~50 lines)
```

**Total estimated size:** ~800 lines (similar to flappy bird's 505 lines, scaled for complexity)

### Modularization Strategy
- Keep single-file HTML for easy deployment (no build step)
- Use ES6 classes for clarity
- Separate concerns: game logic vs AI training vs rendering
- Comment sections clearly (same pattern as flappy bird)

## 15. Final Recommendation Summary

**Approach:** Fixed-topology neural network (72→16→4) evolved via genetic algorithm

**Training:** Real-time, 50 genomes/generation, roulette wheel selection, 10% elitism

**Fitness:** Multi-objective (survival + kills + collection - damage + levels + accuracy)

**Visualization:** Live training display, 1x/3x/10x speed, localStorage checkpoints

**Hybrid Mode:** Optional AI-assist (AI moves, player shoots) with ghost overlay

**Code Reuse:** Copy neural network and genetic algorithm from flappy bird, adapt state/action spaces

**Timeline:** ~40 minutes to trained AI (4 minutes perceived at 10x speed)

**This approach balances complexity (sophisticated enough to handle shmup gameplay) with simplicity (easier to implement and debug than full NEAT or Q-learning).**
