# RAIDEN-R03: Self-Learning AI Architecture

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-08

---

## Executive Summary

This document defines the complete AI architecture for a Raiden-style vertical scrolling shoot-em-up (shmup) with self-learning capabilities. The system uses NEAT (NeuroEvolution of Augmenting Topologies) to evolve neural networks that control AI players capable of improving through gameplay experience.

The architecture is based on analysis of the existing Flappy Bird AI implementation at `browser/public/games/flappy-bird-ai-v1-20260407.html` and extended to handle the substantially greater complexity of a shmup environment.

---

## 1. Network Topology

### Input Layer: 21 Neurons

The neural network receives a 21-dimensional state vector representing the game environment:

**Player State (3 inputs):**
1. `player_x`: Player X position normalized to [0, 1] (0 = left edge, 1 = right edge)
2. `player_y`: Player Y position normalized to [0, 1] (0 = top, 1 = bottom)
3. `player_velocity_y`: Vertical velocity normalized to [-1, 1] (if vertical drift exists)

**Nearest Enemy Data (5 inputs):**
4. `enemy1_rel_x`: Relative X position of closest enemy, normalized to [-1, 1]
5. `enemy1_rel_y`: Relative Y position of closest enemy, normalized to [0, 1]
6. `enemy1_type`: Enemy type encoded as categorical value [0, 1] (0 = basic, 0.5 = medium, 1 = boss)
7. `enemy1_health`: Enemy health normalized to [0, 1]
8. `enemy1_distance`: Euclidean distance to enemy, normalized by screen diagonal

**Second Nearest Enemy Data (4 inputs):**
9. `enemy2_rel_x`: Relative X position, normalized to [-1, 1]
10. `enemy2_rel_y`: Relative Y position, normalized to [0, 1]
11. `enemy2_type`: Enemy type [0, 1]
12. `enemy2_distance`: Normalized distance

**Nearest Threat Bullets (4 inputs):**
13. `bullet1_rel_x`: X position relative to player [-1, 1]
14. `bullet1_rel_y`: Y position relative to player [0, 1]
15. `bullet2_rel_x`: Second closest bullet X [-1, 1]
16. `bullet2_rel_y`: Second closest bullet Y [0, 1]

**Nearest Power-Up (2 inputs):**
17. `powerup_rel_x`: X position relative to player [-1, 1]
18. `powerup_rel_y`: Y position relative to player [0, 1]

**Player Status (3 inputs):**
19. `current_weapon_tier`: Weapon level normalized to [0, 1] (0 = base, 1 = max)
20. `bomb_available`: Binary [0, 1] (0 = on cooldown, 1 = ready)
21. `health_remaining`: Health percentage [0, 1]

### Hidden Layer: 16 Neurons (Initial)

NEAT starts with minimal topology and evolves complexity. Initial hidden layer:
- **Size:** 16 neurons (2x input size, per NEAT best practices)
- **Activation:** Sigmoid function: `f(x) = 1 / (1 + e^(-x))`
- **Topology:** Fully connected from input layer initially
- **Evolution:** NEAT adds/removes neurons and connections over generations

### Output Layer: 4 Neurons

The network outputs continuous values in [0, 1] for each action:

1. `move_left`: Movement left intensity [0, 1]
2. `move_right`: Movement right intensity [0, 1]
3. `fire`: Firing decision threshold [0, 1] (fire if > 0.5)
4. `use_bomb`: Bomb usage decision [0, 1] (activate if > 0.8)

**Action Decoding:**
- **Movement:** `final_x_velocity = (move_right - move_left) * max_speed`
  - If both < 0.3, no movement (deadzone)
  - Net movement is difference between left/right signals
- **Fire:** Binary decision with 0.5 threshold (allows continuous fire if network maintains >0.5)
- **Bomb:** High threshold (0.8) to prevent accidental activation

---

## 2. State Representation Details

### Input Vector Construction

```javascript
function getStateVector(player, enemies, bullets, powerups) {
    const state = new Array(21).fill(0);

    // Player state (normalized to canvas dimensions)
    state[0] = player.x / CANVAS_WIDTH;
    state[1] = player.y / CANVAS_HEIGHT;
    state[2] = player.velocityY / MAX_VELOCITY;

    // Sort enemies by distance
    const sortedEnemies = enemies
        .map(e => ({
            enemy: e,
            dist: Math.hypot(e.x - player.x, e.y - player.y)
        }))
        .sort((a, b) => a.dist - b.dist);

    // Nearest enemy
    if (sortedEnemies.length > 0) {
        const e1 = sortedEnemies[0];
        state[3] = (e1.enemy.x - player.x) / CANVAS_WIDTH;
        state[4] = (e1.enemy.y - player.y) / CANVAS_HEIGHT;
        state[5] = encodeEnemyType(e1.enemy.type);
        state[6] = e1.enemy.health / e1.enemy.maxHealth;
        state[7] = e1.dist / Math.hypot(CANVAS_WIDTH, CANVAS_HEIGHT);
    }

    // Second nearest enemy
    if (sortedEnemies.length > 1) {
        const e2 = sortedEnemies[1];
        state[8] = (e2.enemy.x - player.x) / CANVAS_WIDTH;
        state[9] = (e2.enemy.y - player.y) / CANVAS_HEIGHT;
        state[10] = encodeEnemyType(e2.enemy.type);
        state[11] = e2.dist / Math.hypot(CANVAS_WIDTH, CANVAS_HEIGHT);
    }

    // Nearest threat bullets (enemy bullets heading toward player)
    const threatBullets = bullets
        .filter(b => b.isEnemy && b.y < player.y + 100) // Only bullets ahead
        .map(b => ({
            bullet: b,
            dist: Math.hypot(b.x - player.x, b.y - player.y)
        }))
        .sort((a, b) => a.dist - b.dist);

    if (threatBullets.length > 0) {
        state[12] = (threatBullets[0].bullet.x - player.x) / CANVAS_WIDTH;
        state[13] = (threatBullets[0].bullet.y - player.y) / CANVAS_HEIGHT;
    }

    if (threatBullets.length > 1) {
        state[14] = (threatBullets[1].bullet.x - player.x) / CANVAS_WIDTH;
        state[15] = (threatBullets[1].bullet.y - player.y) / CANVAS_HEIGHT;
    }

    // Nearest power-up
    const nearestPowerup = powerups
        .map(p => ({
            powerup: p,
            dist: Math.hypot(p.x - player.x, p.y - player.y)
        }))
        .sort((a, b) => a.dist - b.dist)[0];

    if (nearestPowerup) {
        state[16] = (nearestPowerup.powerup.x - player.x) / CANVAS_WIDTH;
        state[17] = (nearestPowerup.powerup.y - player.y) / CANVAS_HEIGHT;
    }

    // Player status
    state[18] = player.weaponTier / MAX_WEAPON_TIER;
    state[19] = player.bombReady ? 1 : 0;
    state[20] = player.health / player.maxHealth;

    return state;
}

function encodeEnemyType(type) {
    const typeMap = { 'basic': 0, 'medium': 0.5, 'heavy': 0.75, 'boss': 1 };
    return typeMap[type] || 0;
}
```

### Normalization Rationale

All inputs are normalized to prevent any single feature from dominating the network training:
- **Position data:** Normalized to canvas dimensions (0-1 range)
- **Relative positions:** Allow negative values for left/above positions (-1 to 1)
- **Distances:** Normalized by screen diagonal to bound [0, 1]
- **Binary states:** Already in [0, 1]
- **Categorical data:** Encoded as ordered continuous values [0, 1]

---

## 3. Action Space Design

### Movement Control

**8-Way Movement Simulation:**
- Network outputs continuous left/right signals
- Game already provides vertical auto-scroll
- Player can strafe left/right based on network output
- Deadzone (0.3) prevents jitter from neutral network outputs

**Movement Formula:**
```javascript
function decodeMovement(outputs) {
    const moveLeft = outputs[0];
    const moveRight = outputs[1];

    // Deadzone to prevent micro-adjustments
    const leftActive = moveLeft > 0.3;
    const rightActive = moveRight > 0.3;

    if (!leftActive && !rightActive) return 0;

    // Net movement is difference
    const netMove = moveRight - moveLeft;
    return netMove * PLAYER_MAX_SPEED;
}
```

### Firing Control

**Continuous Fire with Threshold:**
```javascript
function shouldFire(outputs) {
    return outputs[2] > 0.5; // Binary decision
}
```

Network learns:
- Fire constantly against enemies (output stays > 0.5)
- Conserve ammo if weapon has cooldown (output drops < 0.5)
- Context-aware: fires more when enemies nearby

### Bomb Usage

**High-Threshold Activation:**
```javascript
function shouldUseBomb(outputs, bombAvailable) {
    return bombAvailable && outputs[3] > 0.8;
}
```

High threshold (0.8) prevents:
- Accidental activation from noise
- Wasteful early-game bomb usage
- Network must "strongly decide" to bomb (high conviction required)

Strategic bomb usage:
- Against boss enemies (enemy_type = 1.0)
- When health is low (health_remaining < 0.3)
- When surrounded by bullets (multiple threat bullets present)

---

## 4. Reward Function

### Formula

```
Fitness =
    (survival_time * 1.0) +
    (score * 0.5) +
    (enemies_killed * 10.0) +
    (damage_taken * -50.0) +
    (powerups_collected * 5.0) +
    (bomb_efficiency * 3.0) +
    (proximity_penalty * -0.1)
```

### Component Breakdown

**1. Survival Time (weight: 1.0)**
- Measured in frames
- Encourages staying alive as primary goal
- Raw frame count incentivizes defensive play

**2. Score (weight: 0.5)**
- Game's internal scoring system
- Secondary to survival (lower weight)
- Prevents score-chasing at expense of survival

**3. Enemies Killed (weight: 10.0)**
- High weight encourages aggressive play
- Balances survival incentive
- Rewards proactive enemy destruction

**4. Damage Taken (weight: -50.0)**
- Strong negative penalty
- Each hit penalized heavily
- Encourages bullet dodging and safe positioning

**5. Power-ups Collected (weight: 5.0)**
- Positive reinforcement for collecting upgrades
- Encourages exploration of screen area
- Weapon tier improvements aid survival

**6. Bomb Efficiency (weight: 3.0)**
- Calculated as: `(enemies_killed_by_bomb / bombs_used)` if bombs_used > 0, else 0
- Rewards strategic bomb usage
- Punishes wasteful bomb spam

**7. Proximity Penalty (weight: -0.1)**
- Small penalty for hugging screen edges
- Formula: `edge_frames * -0.1` where edge_frames counts frames spent at x < 50 or x > width-50
- Encourages central positioning for better dodging options
- Low weight: doesn't override survival priority

### Reward Shaping

**Sparse vs Dense:**
This hybrid approach combines:
- **Sparse rewards:** enemies_killed, powerups_collected (discrete events)
- **Dense rewards:** survival_time, proximity_penalty (continuous feedback)

Dense rewards prevent "reward desert" where network wanders aimlessly. Survival time provides constant feedback signal.

**Balancing Aggression vs Survival:**
- Survival time baseline ensures network values staying alive
- High enemy kill weight (10x vs 1x survival) pushes toward engagement
- Damage penalty (-50x) enforces caution
- Net effect: aggressive but careful play

---

## 5. NEAT Training Parameters

### Population Parameters

```javascript
const NEAT_CONFIG = {
    populationSize: 100,        // Population of neural networks per generation
    eliteCount: 10,             // Top 10% preserved unchanged
    survivalRate: 0.25,         // Top 25% used as breeding pool

    // Mutation rates
    mutationRate: 0.10,         // 10% chance per weight to mutate
    addNodeRate: 0.03,          // 3% chance to add hidden neuron
    addConnectionRate: 0.05,    // 5% chance to add connection
    removeConnectionRate: 0.02, // 2% chance to remove connection

    // Crossover
    crossoverRate: 0.75,        // 75% of offspring from crossover, 25% from mutation-only

    // Speciation
    compatibilityThreshold: 3.0, // Distance threshold for same species
    c1: 1.0,                    // Excess gene coefficient
    c2: 1.0,                    // Disjoint gene coefficient
    c3: 0.4,                    // Weight difference coefficient

    // Mutation magnitudes
    perturbationRate: 0.90,     // 90% small adjustments, 10% full replacement
    perturbationPower: 0.2,     // ±20% adjustment to weights

    // Activation functions
    activationDefault: 'sigmoid',
    activationMutationRate: 0.0 // Don't change activation functions
};
```

### Parameter Rationale

**Population Size: 100**
- Larger than Flappy Bird's 50 (shmup is more complex)
- Balances diversity with computation speed
- Research suggests 100-200 optimal for game AI
- Based on: [NEAT-Python documentation](https://neat-python.readthedocs.io/en/latest/neat_overview.html)

**Elite Count: 10**
- Top 10% preserved without modification
- Ensures best solutions persist across generations
- Prevents fitness regression

**Survival Rate: 25%**
- Top quartile used for breeding
- Stricter than Flappy Bird's 20% (higher selection pressure)
- Faster convergence on complex strategies

**Mutation Rate: 10%**
- Standard NEAT parameter
- Each weight has 10% chance of mutation per generation
- Based on: [MDPI research on GA parameters](https://www.mdpi.com/2078-2489/10/12/390)

**Add Node/Connection Rates (3%/5%)**
- Allows topology evolution
- Conservative rates prevent bloat
- Network grows gradually in complexity

**Crossover Rate: 75%**
- High crossover encourages trait combination
- 25% mutation-only preserves exploration
- Based on: [Genetic Algorithm tuning best practices](https://www.woodruff.dev/day-31-best-practices-for-tuning-genetic-algorithm-parameters/)

**Speciation**
- Protects innovation by grouping similar networks
- Prevents dominant species from eliminating all diversity
- Compatibility threshold 3.0 is NEAT standard

---

## 6. Training Loop Design

### Training Architecture

```javascript
class TrainingManager {
    constructor() {
        this.generation = 1;
        this.population = this.initializePopulation(100);
        this.speed = 1; // Training speed multiplier
        this.autosaveInterval = 5; // Save every 5 generations
        this.trainingMode = 'background'; // 'background' | 'manual' | 'off'
    }

    initializePopulation(size) {
        return Array(size).fill(0).map(() => ({
            network: new NeuralNetwork(),
            fitness: 0,
            alive: true,
            game: new GameInstance() // Each AI gets own game instance
        }));
    }

    update() {
        // Update all alive AIs
        this.population.forEach(individual => {
            if (!individual.alive) return;

            const state = individual.game.getStateVector();
            const outputs = individual.network.predict(state);

            individual.game.applyActions(outputs);
            individual.game.update();

            if (individual.game.isGameOver()) {
                individual.alive = false;
                individual.fitness = this.calculateFitness(individual.game);
            }
        });

        // Check if generation complete
        if (this.population.every(ind => !ind.alive)) {
            this.nextGeneration();
        }
    }

    nextGeneration() {
        // Sort by fitness
        this.population.sort((a, b) => b.fitness - a.fitness);

        // Log best performer
        console.log(`Gen ${this.generation}: Best fitness = ${this.population[0].fitness}`);

        // Evolve new population
        this.population = this.evolvePopulation(this.population);

        this.generation++;

        // Autosave
        if (this.generation % this.autosaveInterval === 0) {
            this.saveBestNetwork();
        }
    }

    calculateFitness(game) {
        return (
            game.survivalTime * 1.0 +
            game.score * 0.5 +
            game.enemiesKilled * 10.0 +
            game.damageTaken * -50.0 +
            game.powerupsCollected * 5.0 +
            (game.bombsUsed > 0 ? game.enemiesKilledByBomb / game.bombsUsed : 0) * 3.0 +
            game.edgeFrames * -0.1
        );
    }
}
```

### Training Speed Control

**Speed Multiplier:**
- **1x:** Real-time (60 FPS), user watches training
- **3x:** Fast training (180 updates/sec), still visible
- **10x:** Ultra-fast (600 updates/sec), blur of activity
- **Max:** Headless mode, no rendering, ~2000 updates/sec

**Implementation:**
```javascript
function gameLoop() {
    const updatesPerFrame = trainingManager.speed;

    for (let i = 0; i < updatesPerFrame; i++) {
        trainingManager.update();
    }

    // Only render at display refresh rate
    if (trainingManager.speed <= 10) {
        render(); // Skip rendering in ultra-fast mode
    }

    requestAnimationFrame(gameLoop);
}
```

### Training Modes

**1. Background Training (Default)**
- Runs continuously while user does other tasks
- Uses `requestIdleCallback()` to avoid blocking UI
- Slow but steady improvement
- ~10 generations/hour

**2. Manual Training**
- User clicks "Train Generation" button
- Runs one full generation per click
- User controls pacing
- Good for testing/debugging

**3. Off**
- Training paused
- User can play with best AI
- Useful for evaluation

### Convergence Expectations

Based on Flappy Bird AI and NEAT research:
- **Generations to basic competence:** 10-20 (survives 30+ seconds)
- **Generations to good performance:** 50-100 (completes level 1)
- **Generations to expert play:** 200-500 (high scores, strategic bomb use)
- **Training time (10x speed):** ~2-5 hours to expert level

---

## 7. Visualization

### HUD Display

```javascript
const hudElements = {
    generation: {
        label: 'Generation',
        value: () => trainingManager.generation,
        format: 'integer'
    },
    aliveCount: {
        label: 'Alive',
        value: () => trainingManager.population.filter(p => p.alive).length,
        format: 'integer'
    },
    bestFitness: {
        label: 'Best (Gen)',
        value: () => Math.max(...trainingManager.population.map(p => p.fitness)),
        format: 'float'
    },
    bestEver: {
        label: 'Best (Ever)',
        value: () => trainingManager.bestFitnessEver,
        format: 'float'
    },
    speciesCount: {
        label: 'Species',
        value: () => trainingManager.getSpeciesCount(),
        format: 'integer'
    },
    avgFitness: {
        label: 'Avg Fitness',
        value: () => trainingManager.population.reduce((sum, p) => sum + p.fitness, 0) / trainingManager.population.length,
        format: 'float'
    }
};
```

### Visual Indicators

**AI Player Visual Distinction:**
- AI players rendered semi-transparent (0.7 alpha)
- Distinct color per neural network (hue based on network ID)
- Best performer highlighted with glow effect
- Human player (if in hybrid mode) rendered opaque

**Network Visualization (Optional):**
- Small network diagram in corner
- Shows active connections during decision-making
- Neurons light up proportional to activation
- Helpful for understanding AI decision process

**Fitness Graph:**
- Line chart showing best/average fitness over generations
- X-axis: generation number
- Y-axis: fitness score
- Two lines: best fitness (blue), average fitness (gray)
- Updates in real-time

### Performance Metrics Display

```
╔════════════════════════════════════════╗
║  NEAT Training Dashboard               ║
╠════════════════════════════════════════╣
║  Generation:        247                ║
║  Alive:            42 / 100            ║
║  Best (Gen):       1,245.3             ║
║  Best (Ever):      2,891.7             ║
║  Avg Fitness:        687.2             ║
║  Species:            7                 ║
║  Training Speed:     10x               ║
║  Gen/Hour:          ~120               ║
╚════════════════════════════════════════╝
```

---

## 8. Hybrid Mode: AI-Assisted Gameplay

### Assisted Modes

**1. Auto-Dodge Mode**
- AI controls movement only
- Player controls firing and bombs
- AI focuses on bullet avoidance (high weight on damage_taken penalty)
- Player handles strategic decisions

**2. Auto-Fire Mode**
- Player controls movement
- AI controls firing timing
- AI learns optimal firing patterns
- Player handles positioning

**3. Co-Pilot Mode**
- AI suggests actions via visual overlays
- Player retains full control
- Arrow indicators show AI's recommended movement
- "BOMB NOW" indicator when AI would bomb
- Useful for learning from AI

**4. Takeover Mode**
- AI plays automatically
- Player can press button to temporarily override
- Useful for difficult sections or farming
- Player intervention counted separately from AI score

### Implementation

```javascript
class HybridController {
    constructor(mode) {
        this.mode = mode; // 'auto-dodge' | 'auto-fire' | 'co-pilot' | 'takeover'
        this.aiNetwork = loadBestNetwork();
        this.playerOverride = false;
    }

    update(gameState, playerInputs) {
        const aiState = gameState.getStateVector();
        const aiOutputs = this.aiNetwork.predict(aiState);

        switch (this.mode) {
            case 'auto-dodge':
                return {
                    movement: decodeMovement(aiOutputs),
                    fire: playerInputs.fire,
                    bomb: playerInputs.bomb
                };

            case 'auto-fire':
                return {
                    movement: playerInputs.movement,
                    fire: aiOutputs[2] > 0.5,
                    bomb: playerInputs.bomb
                };

            case 'co-pilot':
                // AI doesn't control, just displays suggestions
                this.displaySuggestions(aiOutputs);
                return playerInputs;

            case 'takeover':
                if (this.playerOverride) {
                    return playerInputs;
                } else {
                    return {
                        movement: decodeMovement(aiOutputs),
                        fire: aiOutputs[2] > 0.5,
                        bomb: aiOutputs[3] > 0.8
                    };
                }
        }
    }

    displaySuggestions(outputs) {
        // Draw arrows showing AI's recommended movement
        const moveDir = outputs[1] - outputs[0]; // right - left
        if (Math.abs(moveDir) > 0.3) {
            drawArrow(player.x, player.y, moveDir > 0 ? 'right' : 'left');
        }

        // Show bomb suggestion
        if (outputs[3] > 0.8) {
            drawText(player.x, player.y - 40, "BOMB!", 'red');
        }
    }
}
```

### Save/Load Networks

**LocalStorage Persistence:**
```javascript
function saveBestNetwork() {
    const best = trainingManager.population[0];
    const serialized = {
        generation: trainingManager.generation,
        fitness: best.fitness,
        weightsIH: best.network.weightsIH,
        weightsHO: best.network.weightsHO,
        biasH: best.network.biasH,
        biasO: best.network.biasO,
        timestamp: Date.now()
    };

    localStorage.setItem('raiden_ai_best', JSON.stringify(serialized));
}

function loadBestNetwork() {
    const saved = localStorage.getItem('raiden_ai_best');
    if (!saved) return null;

    const data = JSON.parse(saved);
    const network = new NeuralNetwork();
    network.weightsIH = data.weightsIH;
    network.weightsHO = data.weightsHO;
    network.biasH = data.biasH;
    network.biasO = data.biasO;

    return network;
}
```

**Export/Import:**
- Download button exports network as JSON file
- Upload button imports trained network
- Allows sharing trained AIs between users
- Useful for showcasing expert AI behavior

---

## 9. Reference Implementation Analysis

### Flappy Bird AI (`browser/public/games/flappy-bird-ai-v1-20260407.html`)

**Key Patterns Extracted:**

1. **Simple State Space (5 inputs):**
   - Bird Y position (normalized)
   - Bird velocity (normalized)
   - Next pipe X distance (normalized)
   - Next pipe gap Y position (normalized)
   - Pipe gap size (constant, normalized)

2. **Minimal Network (5-8-1):**
   - 5 inputs, 8 hidden neurons, 1 output
   - Sigmoid activation throughout
   - Single output for "jump" decision (threshold 0.5)

3. **Fitness Function:**
   ```javascript
   fitness = frames + (score * 100)
   ```
   - Survival time (frames) + bonus for passing pipes
   - Simple but effective

4. **Population Management:**
   - 50 population size
   - 5 elite preserved (10%)
   - 20% survival rate for breeding
   - 10% mutation rate

5. **Training Speed:**
   - 1x, 3x, 10x multipliers via game loop updates per frame
   - No rendering at 10x for max speed

6. **Visual Design:**
   - Each bird colored uniquely (`hsl(${Math.random() * 360}, 70%, 50%)`)
   - HUD shows: generation, alive count, best gen, best ever, species count
   - Clean UI with stat cards

### Adaptations for Shmup

**Increased Complexity:**
- State space: 5 → 21 inputs (4.2x larger)
- Hidden neurons: 8 → 16 (2x larger)
- Outputs: 1 → 4 (4x larger)
- Population: 50 → 100 (2x larger)

**Multi-Output Actions:**
- Flappy Bird: single binary decision (jump/no jump)
- Shmup: continuous movement + fire threshold + bomb threshold
- Requires more sophisticated action decoding

**Dynamic Environment:**
- Flappy Bird: deterministic pipe placement
- Shmup: variable enemy patterns, bullets, power-ups
- Requires tracking multiple entities simultaneously

**Strategic Decisions:**
- Flappy Bird: purely reactive (dodge pipe)
- Shmup: proactive (when to bomb, when to collect power-ups)
- Needs higher-level planning capabilities

---

## 10. Implementation Roadmap

### Phase 1: Core Neural Network (Spec R101)
- Implement `NeuralNetwork` class with NEAT topology
- Sigmoid activation, weight matrices, bias vectors
- `predict(inputs)` → outputs
- `clone()`, `mutate(rate)`, `crossover(partner)` methods

### Phase 2: State Vector Construction (Spec R101)
- Implement `getStateVector()` function
- Enemy/bullet/power-up sorting by distance
- Normalization helpers
- Enemy type encoding

### Phase 3: Genetic Algorithm (Spec R101)
- Implement `GeneticAlgorithm` class
- Population initialization
- Fitness calculation (full formula)
- Selection, crossover, mutation, elitism
- Speciation (optional, can defer to later)

### Phase 4: Training Loop Integration (Spec R102)
- Integrate NEAT with game loop
- Multiple game instances per generation
- Speed multiplier (1x/3x/10x)
- Generation cycling

### Phase 5: Visualization (Spec R102)
- HUD elements (generation, alive, fitness, etc.)
- Color-coded AI players
- Fitness graph over time

### Phase 6: Persistence (Spec R102)
- LocalStorage save/load
- JSON export/import
- Best network autosave every 5 generations

### Phase 7: Hybrid Modes (Spec R103)
- Auto-dodge mode
- Auto-fire mode
- Co-pilot mode
- Player override controls

---

## 11. Testing Strategy

### Unit Tests
- `NeuralNetwork.predict()` output range [0, 1]
- State vector normalization (all values in expected ranges)
- Fitness calculation (correct formula application)
- Mutation doesn't corrupt network structure

### Integration Tests
- Full generation cycle completes without crashes
- Population diversity maintained (not all identical networks)
- Fitness improves over generations
- Best network preserved across generations

### Performance Tests
- 100 population at 10x speed maintains 60 FPS
- Memory doesn't leak over 100+ generations
- LocalStorage save/load under 100ms

### Regression Tests
- Trained network performs consistently on same level
- Loading saved network reproduces behavior
- Hybrid modes correctly blend AI + player inputs

---

## 12. Known Limitations & Future Enhancements

### Current Limitations

1. **Fixed Enemy Count:**
   - State vector only tracks 2 nearest enemies
   - Doesn't scale to massive bullet hell scenarios
   - Mitigation: Focus on nearest threats (most relevant)

2. **No Memory:**
   - Network is feedforward only (no recurrence)
   - Can't remember past actions or learn patterns over time
   - Mitigation: State vector includes velocity (proxy for recent movement)

3. **No Boss-Specific Strategies:**
   - Single network for all enemy types
   - Doesn't specialize for boss patterns
   - Mitigation: Enemy type input allows network to differentiate

4. **Collision Prediction:**
   - Network doesn't explicitly predict bullet trajectories
   - Reactive rather than predictive
   - Mitigation: Including bullet positions gives enough signal for dodging

### Future Enhancements

**1. Recurrent Networks (LSTM/GRU):**
- Add memory to track temporal patterns
- Learn enemy attack cycles
- Anticipate boss phase transitions

**2. Attention Mechanism:**
- Dynamic focus on most threatening bullets
- Handle variable-length enemy/bullet lists
- More robust to screen clutter

**3. Curriculum Learning:**
- Start training on easy levels
- Gradually increase difficulty as network improves
- Faster convergence to expert play

**4. Multi-Objective Fitness:**
- Separate fitness scores for survival, aggression, efficiency
- Pareto frontier optimization
- Diverse AI strategies (defensive vs aggressive)

**5. Transfer Learning:**
- Train base network on generic shmup skills
- Fine-tune for specific levels/bosses
- Faster adaptation to new content

---

## 13. Conclusion

This AI architecture provides a complete blueprint for implementing self-learning AI in the Raiden-style shmup. The design balances:

- **Simplicity:** Builds on proven Flappy Bird NEAT pattern
- **Scalability:** Extends to handle shmup complexity (21 inputs, 4 outputs)
- **Usability:** Hybrid modes allow player-AI collaboration
- **Performance:** Training loop optimized for browser execution

The network topology (21-16-4) is intentionally conservative, allowing NEAT to evolve complexity as needed. The reward function balances survival and aggression, encouraging skilled play without excessive risk-taking.

Training is designed for background execution, with progress visualized in real-time. Players can observe AI improvement over generations, test hybrid modes, and export/share trained networks.

Implementation follows a phased approach, with each phase testable independently. The architecture is extensible, with clear paths for future enhancements (recurrence, attention, curriculum learning).

**Next Steps:** Proceed to implementation specs RAIDEN-R101 (AI core), R102 (training loop), R103 (hybrid modes).

---

## Sources

### NEAT & Neuroevolution Research
- [Real-Time Neuroevolution in the NERO Video Game](https://nn.cs.utexas.edu/downloads/papers/stanley.ieeetec05.pdf)
- [A Neuroevolution Approach to General Atari Game Playing](https://www.cs.utexas.edu/~mhauskn/papers/atari.pdf)
- [Neuroevolution in Games: State of the Art and Open Challenges](https://arxiv.org/pdf/1410.7326)
- [NEAT Overview — NEAT-Python Documentation](https://neat-python.readthedocs.io/en/latest/neat_overview.html)

### Genetic Algorithm Parameters
- [Best Practices for Tuning Genetic Algorithm Parameters](https://www.woodruff.dev/day-31-best-practices-for-tuning-genetic-algorithm-parameters/)
- [Choosing Mutation and Crossover Ratios for Genetic Algorithms](https://www.mdpi.com/2078-2489/10/12/390)

### Reinforcement Learning & Game AI
- [Reinforcement Learning Agent for a 2D Shooter Game](https://arxiv.org/html/2509.15042v1)
- [Comprehensive Overview of Reward Engineering and Shaping in RL](https://arxiv.org/html/2408.10215v1)
- [Time-Based Reward Shaping in Real-Time Strategy Games](https://www.researchgate.net/publication/221435646_Time-Based_Reward_Shaping_in_Real-Time_Strategy_Games)

### Bullet Hell & Neural Networks
- [RL Bullet Hell Environment (GitHub)](https://github.com/michael-pacheco/deep-learning-bullet-hell-environment)
- [Training Neural Network for Bullet Hell Games](https://proit.org/post/162113)
- [Artificial Intelligent Player for Bullet Hell Games Based on DQN](https://www.researchgate.net/publication/379883917_Artificial_Intelligent_Player_for_Bullet_Hell_Games_Based_on_Deep_Q-Networks)

### Hybrid AI Systems
- [NVIDIA ACE Autonomous Game Characters](https://www.nvidia.com/en-us/geforce/news/nvidia-ace-autonomous-ai-companions-pubg-naraka-bladepoint/)
- [NVIDIA's Autonomous AI Characters in Popular Games](https://80.lv/articles/nvidia-s-autonomous-ai-characters-are-coming-to-popular-games)
- [How AI Agents in Video Games Transform Gaming](https://inworld.ai/blog/ai-agents-in-video-games-current-and-future-state)

---

**Document Version:** 1.0
**Author:** BEE-QUEUE-TEMP-SPEC-RAIDEN-R03-ai-
**Last Updated:** 2026-04-08
