# Flappy Bird AI v2 — Design Document

**Created:** 2026-04-14
**Based on:** FLAPPY-R01 Research Findings
**Target File:** `browser/public/games/flappy-bird-ai-v2-20260407.html`

---

## 1. Game Design Specification

### 1.1 Canvas & Display

- **Canvas size:** 600px × 600px (game canvas)
- **Visualization canvas:** 400px × 600px (neural network display, rendered adjacent)
- **Aspect ratio:** 1:1 (square, mobile-friendly)
- **Background:** Sky gradient (#70c5ce to #4fb3bc)
- **Ground:** 50px green strip at bottom (#5cb85c)

### 1.2 Bird Physics

All values tuned for 600×600 canvas at 60fps:

| Parameter | Value | Unit | Rationale |
|-----------|-------|------|-----------|
| **Gravity** | 0.6 | px/frame² | Realistic fall acceleration |
| **Jump velocity** | -10.0 | px/frame | Strong enough to clear 180px gap |
| **Terminal velocity** | 15.0 | px/frame | Prevents excessive fall speed |
| **Bird radius** | 12 | px | Visible but small enough for tight gaps |
| **Collision model** | Circle | — | Simple, forgiving hitbox |

**Velocity clamping:**
```javascript
bird.velocity = Math.max(-15, Math.min(15, bird.velocity));
```

### 1.3 Pipe Generation

| Parameter | Value | Unit | Notes |
|-----------|-------|------|-------|
| **Pipe width** | 60 | px | Standard Flappy Bird proportion |
| **Pipe gap (height)** | 180 | px | Fixed throughout training |
| **Pipe spacing** | 250 | px | Horizontal distance between pipes |
| **Pipe scroll speed** | 3.0 | px/frame | Constant (no acceleration) |
| **Gap Y randomization** | 50–470 | px | `Math.random() * (550 - pipeGap - 100) + 50` |

**Generation logic:**
- When rightmost pipe x < canvas.width - pipeSpacing, spawn new pipe at x=canvas.width
- Gap center Y uniformly random within safe bounds (avoids top/bottom 50px)
- No difficulty scaling (gap size, speed constant for all generations)

### 1.4 Difficulty Curve

**NONE.** V2 uses constant difficulty:
- Pipe gap: 180px (never narrows)
- Scroll speed: 3px/frame (never increases)
- Gap randomization: uniform distribution (no bias)

**Rationale:** NEAT learns best when environment is stationary. Difficulty scaling interferes with fitness comparison across generations.

### 1.5 Visual Style

**Birds:**
- HSL random colors per bird: `hsl(${Math.random() * 360}, 70%, 50%)`
- Best bird (highest fitness alive): Gold outline (4px, #FFD700)
- Species coloring: Birds in same species share hue family (10 hue bins: 0°, 36°, 72°, ...)

**Pipes:**
- Body: #5cb85c (green)
- Caps: #4a934a (darker green, 20px height)
- Simple rectangles (no textures)

**Effects:**
- No particle systems (keep under 500 lines)
- No shadows or gradients on game objects (performance)
- Smooth 60fps rendering for up to 120 birds

### 1.6 Score Calculation

**Score = number of pipes passed** (integer)

- Pipe marked "passed" when bird.x > pipe.x + pipeWidth
- Each bird tracks own score independently
- Score increments only once per pipe per bird

**Display:**
- Best score this generation (real-time)
- Best score ever (persistent across generations)

### 1.7 Collision Detection

**Algorithm:**
```javascript
function collidesWith(bird, pipe) {
    // Horizontal overlap check
    if (bird.x + bird.radius > pipe.x &&
        bird.x - bird.radius < pipe.x + pipeWidth) {
        // Vertical gap check
        if (bird.y - bird.radius < pipe.gapY ||
            bird.y + bird.radius > pipe.gapY + pipeGap) {
            return true; // Hit pipe
        }
    }
    return false; // Safe
}

// Boundary check
if (bird.y + radius > canvas.height || bird.y - radius < 0) {
    bird.alive = false; // Hit ground/ceiling
}
```

**Collision response:** Instant death (bird.alive = false)

---

## 2. AI Design Specification (NEAT)

### 2.1 Population Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Population size** | 120 | 2.4× v1 (50) for better exploration |
| **Elite count per species** | 2 | Champion + runner-up |
| **Survival rate** | 0.2 | Top 20% eligible to reproduce |
| **Target species count** | 10 | Range: 8-12 active species |

### 2.2 Network Topology

**Initial structure (5-8-1):**

**Input layer (5 nodes):**
1. Bird Y position (normalized 0-1): `bird.y / canvas.height`
2. Bird velocity (normalized -1 to 1): `bird.velocity / 20`
3. Horizontal distance to next pipe (0-1): `(nextPipe.x - bird.x) / canvas.width`
4. Vertical position of pipe gap center (0-1): `nextPipe.gapY / canvas.height`
5. Pipe gap height constant (0-1): `pipeGap / canvas.height` = 0.3

**Hidden layer:**
- Initial: 8 nodes
- Max: 20 nodes (enforced limit)
- Growth: NEAT adds nodes via addNode mutation
- Expected by gen 100: 12-15 nodes

**Output layer (1 node):**
- Activation > 0.5 → FLAP
- Activation ≤ 0.5 → NO FLAP

**Activation function:** Sigmoid on all nodes

### 2.3 Speciation Algorithm

**Compatibility distance formula:**

δ = (c₁ × E + c₂ × D) / N + c₃ × W

Where:
- **E** = Excess genes (innovations beyond shorter genome's max)
- **D** = Disjoint genes (mismatched innovations within shared range)
- **N** = Normalizer (see below)
- **W** = Average absolute weight difference of matching genes

**Coefficients:**
- c₁ = 1.0 (excess weight)
- c₂ = 1.0 (disjoint weight)
- c₃ = 0.4 (weight difference weight)

**Normalizer N:**
```javascript
const maxGenes = Math.max(genome1.genes.length, genome2.genes.length);
const N = (maxGenes < 20) ? 1 : maxGenes;
```

**Compatibility threshold (dynamic):**
- Initial: δₜ = 3.0
- Adjustment per generation:
  - If species_count < 8: δₜ -= 0.3 (stricter, merge species)
  - If species_count > 12: δₜ += 0.3 (looser, split species)
  - Clamp: 1.0 ≤ δₜ ≤ 10.0

**Assignment algorithm:**
```
For each genome G in new_population:
    found = false

    For each species S (sorted by size, largest first):
        representative = S.champion
        distance = compatibility_distance(G, representative)

        if distance < threshold:
            S.add(G)
            found = true
            break

    if not found:
        create_new_species(G)

adjust_threshold() // Dynamic adjustment
```

### 2.4 Fitness Function

**Formula:**
```javascript
fitness = (frames_survived × 1.0)
        + (pipes_passed × 500.0)
        + (max_distance_traveled × 2.0)
        + (unnecessary_flaps × -10.0)
```

**Component definitions:**

1. **frames_survived:** Total frames bird stayed alive (incentivizes survival)
2. **pipes_passed:** Number of pipes cleared × 500 (dominant reward)
3. **max_distance_traveled:** Furthest horizontal progress in pixels × 2 (tiebreaker)
4. **unnecessary_flaps:** Count of flaps when `|bird.y - nextPipe.gapY| > 100` × -10 (efficiency penalty)

**Expected fitness progression:**
- Gen 1: 50-200 (no pipes, pure survival)
- Gen 10: 200-700 (1-2 pipes)
- Gen 30: 1000-3000 (2-6 pipes)
- Gen 60: 5000-15000 (10-30 pipes)
- Gen 100: 25000+ (50+ pipes)

### 2.5 Selection Strategy

**Method:** Fitness-proportionate (roulette wheel) within species

**Per-species reproduction allocation:**
```javascript
// Step 1: Calculate adjusted fitness (fitness sharing)
for each genome G in species S:
    G.adjusted_fitness = G.raw_fitness / S.size

// Step 2: Allocate offspring slots
total_adjusted = sum(all adjusted_fitness across all species)

for each species S:
    S.offspring_quota = Math.round(
        (sum(S.adjusted_fitness) / total_adjusted) × population_size
    )

// Step 3: Select parents within species (roulette wheel)
function selectParent(species):
    total_fitness = sum(species.members.adjusted_fitness)
    random = Math.random() * total_fitness

    for member in species.members:
        random -= member.adjusted_fitness
        if random <= 0:
            return member

    return species.members[0] // fallback
```

**Elite preservation:**
- Top 2 birds per species pass unchanged to next generation
- Elites immune to mutation/crossover
- Total elites = 2 × num_species (typically 16-24)

### 2.6 Mutation Types & Probabilities

**Weight mutations (80% of genomes):**
- **Perturb existing weight:** 80% of weight mutations
  - Range: current ± 0.3
  - Formula: `weight + (Math.random() * 0.6 - 0.3)`
- **Replace weight:** 10% of weight mutations
  - New random: `Math.random() * 2 - 1`
- **No mutation:** 10% of weight mutations

**Structural mutations (per genome per generation):**
- **Add connection:** 5% probability (0.05)
  - Pick two unconnected nodes (no cycles allowed)
  - Assign random weight (-1 to 1)
  - Assign innovation number (global tracker)
- **Add node:** 3% probability (0.03)
  - Pick random enabled connection
  - Disable old connection
  - Insert new node in middle
  - Create two new connections (in: weight=1.0, out: weight=old)
- **Disable connection:** 1% per existing connection (0.01)
  - Mark connection.enabled = false
  - Connection still passed to offspring (can re-enable)
- **Re-enable connection:** 0.25% per disabled connection (0.0025)

**Mutation application order:**
1. Weight mutations (if rolled)
2. Add connection (if rolled)
3. Add node (if rolled)
4. Toggle connection states (if rolled)

### 2.7 Crossover Strategy

**Probability:** 75% crossover, 25% clone

**Algorithm:**
```javascript
function crossover(parent1, parent2):
    // Identify fitter parent
    fitter = (parent1.fitness > parent2.fitness) ? parent1 : parent2
    weaker = (parent1.fitness > parent2.fitness) ? parent2 : parent1

    child_genes = []

    all_innovations = union(parent1.innovations, parent2.innovations)

    for innovation in all_innovations:
        if both_have(innovation):
            // Matching gene: random choice
            gene = (Math.random() < 0.5) ? parent1.gene : parent2.gene
            child_genes.push(gene)
        else:
            // Excess/disjoint: inherit from fitter parent only
            if fitter.has(innovation):
                child_genes.push(fitter.gene)

    return child_genes
```

**Mating types:**
- 75% interspecies (both parents from same species)
- 25% intraspecies (parents from different species)

---

## 3. UX Design Specification

### 3.1 HUD Layout

**Position:** Below game canvas, 600px wide

**Stats displayed (left to right):**

| Stat | Label | Update |
|------|-------|--------|
| Generation | "Generation" | Each generation advance |
| Alive Count | "Alive" | Every frame (real-time) |
| Best (Gen) | "Best (Gen)" | When any bird surpasses current gen best |
| Best (Ever) | "Best (Ever)" | When gen best > all-time best |
| Species Count | "Species" | Each generation (after speciation) |

**Styling:**
- Background: `rgba(255,255,255,0.95)`
- Padding: 15px
- Grid layout: auto-fit, 5 columns
- Each stat: centered, #667eea colored value, gray label

### 3.2 Speed Controls

**Buttons:** 1x, 3x, 10x

**Behavior:**

| Speed | Updates per frame | Rendering |
|-------|-------------------|-----------|
| 1x | 1 game tick | 60fps full render |
| 3x | 3 game ticks | 60fps full render |
| 10x | 10 game ticks | 60fps full render |

**Implementation:**
```javascript
function gameLoop() {
    for (let i = 0; i < speed; i++) {
        update(); // Physics, AI, collision
    }
    draw(); // Always render at 60fps
    requestAnimationFrame(gameLoop);
}
```

**Note:** No frame skipping. Even at 10x, render every frame (UX smoothness).

### 3.3 Mode Switching

**V2 ships AI-only mode.** No human play toggle (defer to future version).

**Rationale:** Keep under 500 lines. Human mode requires input handling, mode state, UI toggle.

### 3.4 Best Bird Highlighting

**Visual marker for highest-fitness living bird:**

- **Outline:** 4px gold stroke (#FFD700)
- **Label:** "BEST" text above bird (white, 12px Arial)
- **Update:** Every frame, recalculate max fitness among alive birds

**Rendering:**
```javascript
const bestBird = population.filter(b => b.alive)
                           .reduce((max, b) => b.fitness > max.fitness ? b : max);

// Draw gold outline
ctx.strokeStyle = '#FFD700';
ctx.lineWidth = 4;
ctx.beginPath();
ctx.arc(bestBird.x, bestBird.y, birdRadius + 2, 0, Math.PI * 2);
ctx.stroke();

// Draw label
ctx.fillStyle = '#FFFFFF';
ctx.font = 'bold 12px Arial';
ctx.fillText('BEST', bestBird.x - 15, bestBird.y - 20);
```

### 3.5 Species Visualization

**Color-coding strategy:**

- Assign each species a hue bin: 0°, 36°, 72°, ..., 324° (10 bins)
- All birds in species S get color: `hsl(${S.hue}, 70%, 50%)`
- Species hue persists across generations (based on species ID)

**Example:**
- Species 0: hue 0° (red)
- Species 1: hue 36° (orange)
- Species 2: hue 72° (yellow-green)
- ...

**Benefit:** Visually distinct clusters. Easy to see which species dominate.

### 3.6 Mobile Touch Zones

**Touch target:** Entire game canvas

**Behavior:**
```javascript
canvas.addEventListener('touchstart', (e) => {
    e.preventDefault();
    // No-op in AI mode (reserved for future human mode)
});
```

**Note:** Touchscreen support deferred. AI mode is mouse/keyboard free.

### 3.7 Neural Network Visualization Panel

**Canvas:** 400×600px, positioned to right of game canvas

**Layout:**
```
┌─────────────┬─────────────┐
│   Game      │   Network   │
│  600×600    │   400×600   │
└─────────────┴─────────────┘
```

**Panel contents:**
- Node positions: topological layout (inputs left, outputs right)
- Connections: lines with thickness/color encoding weights
- Activations: node fill color based on current activation
- Stats overlay: node count, connection count, layers, complexity

**Update rate:** 30fps (even during 10x speed, to prevent flicker)

**Target:** Visualize best bird's network only (not all 120 networks)

---

## 4. Technical Architecture

### 4.1 File Structure (Single HTML)

**Target:** < 500 lines total (hard constraint)

**Internal sections (comment blocks):**

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        /* Styles: ~80 lines */
    </style>
</head>
<body>
    <div id="gameContainer"><!-- HTML structure: ~30 lines --></div>

    <script>
        // ===== CONFIG ===== (~20 lines)

        // ===== GENOME CLASS ===== (~60 lines)
        // - Node genes, connection genes
        // - Distance calculation
        // - Mutations (add node, add connection, weight perturbation)

        // ===== NEURAL NETWORK ===== (~40 lines)
        // - Build network from genome
        // - Forward pass (predict)
        // - Activation storage for visualization

        // ===== BIRD CLASS ===== (~40 lines)
        // - Physics, collision, fitness

        // ===== PIPE CLASS ===== (~30 lines)

        // ===== SPECIES CLASS ===== (~30 lines)
        // - Members, champion, offspring quota

        // ===== NEAT ALGORITHM ===== (~80 lines)
        // - Speciation
        // - Selection
        // - Crossover
        // - Next generation

        // ===== VISUALIZER ===== (~60 lines)
        // - Network layout algorithm
        // - Connection rendering
        // - Node rendering

        // ===== GAME LOOP ===== (~40 lines)
        // - Update, draw, speed control

        // ===== INIT ===== (~10 lines)
    </script>
</body>
</html>
```

**Total estimate:** ~480 lines (20 line buffer for polish)

### 4.2 Module Boundaries

**Responsibility separation:**

| Class/Section | Responsibility | Lines |
|---------------|---------------|-------|
| `Genome` | Gene storage, distance calc, mutations | 60 |
| `NeuralNetwork` | Network construction, forward pass | 40 |
| `Bird` | Game entity (physics, AI interface) | 40 |
| `Pipe` | Obstacle entity | 30 |
| `Species` | Group management, fitness sharing | 30 |
| `NEAT` | Evolution engine (selection, crossover, speciation) | 80 |
| `Visualizer` | Network rendering | 60 |
| Game loop | Main update/draw, speed control | 40 |
| Config + styles | Constants, CSS | 100 |

**Encapsulation:**
- Genome knows nothing about rendering
- Visualizer knows nothing about evolution
- Bird uses NeuralNetwork as black box (predict only)

### 4.3 Rendering Strategy (60fps with 120 birds)

**Optimization targets:**

1. **Batch canvas operations:**
   ```javascript
   // Bad: 120 separate arc calls
   birds.forEach(bird => { ctx.arc(...); ctx.fill(); });

   // Good: One path, batch fill
   ctx.beginPath();
   birds.forEach(bird => ctx.arc(bird.x, bird.y, radius, 0, Math.PI*2));
   ctx.fill();
   ```

2. **Skip dead birds early:**
   ```javascript
   if (!bird.alive) continue; // Don't render, don't think
   ```

3. **Cache pipe collision bounds:**
   ```javascript
   pipe.bounds = {
       left: pipe.x,
       right: pipe.x + width,
       gapTop: pipe.gapY,
       gapBottom: pipe.gapY + gap
   };
   ```

4. **Limit visualization updates:**
   ```javascript
   if (frameCount % 2 === 0) {
       visualizer.draw(); // 30fps instead of 60fps
   }
   ```

**Expected performance:**
- 60fps @ 120 birds on modern laptop (2020+)
- 30fps @ 120 birds on tablet/mobile

### 4.4 State Management

**Global state:**
```javascript
const state = {
    // Game state
    generation: 1,
    bestScoreEver: 0,
    speed: 1, // 1, 3, or 10
    frameCount: 0,

    // NEAT state
    population: [], // Array of Birds
    species: [],    // Array of Species
    innovationTracker: new InnovationTracker(),

    // Rendering state
    pipes: [],
    visualizer: null
};
```

**State transitions:**
- Update: `state.frameCount++`
- Generation advance: `state.generation++`, reset pipes, reset birds
- Speed change: `state.speed = newSpeed`

**No React/Vue/etc.** Vanilla JS only.

### 4.5 Keeping Under 500 Lines

**Compression strategies:**

1. **Inline small functions:**
   ```javascript
   // Instead of separate sigmoid function:
   const sigmoid = x => 1 / (1 + Math.exp(-x));
   ```

2. **Combine related operations:**
   ```javascript
   // Before (3 lines):
   bird.velocity += gravity;
   bird.y += bird.velocity;
   bird.frames++;

   // After (1 line):
   bird.y += (bird.velocity += gravity), bird.frames++, bird.velocity;
   ```
   (Only where readability not sacrificed)

3. **Omit verbose comments:**
   - No header blocks with ASCII art
   - No multi-line parameter descriptions
   - Only essential inline comments

4. **Omit nice-to-haves:**
   - No pause button
   - No restart button (auto-restarts on gen advance)
   - No sound effects
   - No particle effects on collision
   - No generation history graph

5. **Simplify CSS:**
   - No gradients on buttons
   - No hover animations
   - Minimal HUD styling

**Hard constraint:** File MUST compile and run under 500 lines.

---

## 5. Build Phase Plan

### Phase 1: Game Engine Core
**Objective:** Port v1 game mechanics, verify physics/collision work

**Files created:**
- `browser/public/games/flappy-bird-ai-v2-20260407.html` (scaffold)

**Deliverables:**
- [ ] Canvas setup (600×600 game + 400×600 viz)
- [ ] Bird class (physics, collision, no AI yet)
- [ ] Pipe class (generation, scrolling, collision)
- [ ] Game loop (update, draw at 60fps)
- [ ] Manual control test (spacebar flap)

**Lines:** ~150

**Test criteria:**
- Bird falls with gravity
- Spacebar makes bird jump
- Pipes scroll left
- Collision kills bird
- Pipes regenerate off right edge

---

### Phase 2: NEAT Genome System
**Objective:** Implement genome representation, mutations, innovation tracking

**Deliverables:**
- [ ] Genome class (node genes, connection genes)
- [ ] InnovationTracker class (global innovation numbers)
- [ ] Mutation functions (weight perturb, add node, add connection, disable)
- [ ] Distance calculation (compatibility formula)

**Lines:** ~100

**Test criteria:**
- Create genome with 5-8-1 structure
- Mutate genome 100 times, verify structure valid
- Calculate distance between two genomes, verify formula
- Add node splits connection correctly
- Innovation numbers consistent across runs

---

### Phase 3: Neural Network & AI
**Objective:** Build network from genome, forward pass, connect to Bird

**Deliverables:**
- [ ] NeuralNetwork class (construct from genome, predict)
- [ ] Activation storage (for visualization)
- [ ] Bird.think() method (5 inputs → network → flap decision)

**Lines:** ~60

**Test criteria:**
- Network builds from 5-8-1 genome
- Predict returns value 0-1
- Bird makes decisions based on network output
- Inputs normalized correctly

---

### Phase 4: NEAT Evolution Engine
**Objective:** Speciation, selection, crossover, generation advancement

**Deliverables:**
- [ ] Species class (members, champion, adjusted fitness)
- [ ] Speciation algorithm (distance-based grouping)
- [ ] Selection (fitness-proportionate within species)
- [ ] Crossover (matching/excess/disjoint gene handling)
- [ ] nextGeneration() function (orchestrate full cycle)

**Lines:** ~120

**Test criteria:**
- 120 birds speciate into 8-12 groups
- Top 2 per species pass as elites
- Offspring quota allocated by adjusted fitness
- Crossover produces valid child genome
- Generation advances, fitness increases

---

### Phase 5: Neural Network Visualization
**Objective:** Real-time network display with activation colors

**Deliverables:**
- [ ] Visualizer class (layout algorithm, rendering)
- [ ] Node positioning (topological depth-based)
- [ ] Connection rendering (weight → color/thickness/opacity)
- [ ] Node rendering (activation → color)
- [ ] Stats overlay (node count, connection count)

**Lines:** ~70

**Test criteria:**
- Network renders correctly for 5-8-1
- Activations update in real-time (30fps)
- Connections color-coded (green=positive, red=negative)
- Node colors change with activation (blue→orange→red)
- Best bird's network displayed

---

### Phase 6: Polish & Integration
**Objective:** HUD, species colors, best bird marker, final tuning

**Deliverables:**
- [ ] HUD stats (generation, alive, best gen, best ever, species count)
- [ ] Speed controls (1x, 3x, 10x buttons)
- [ ] Species color-coding (hue bins)
- [ ] Best bird gold outline + label
- [ ] Fitness function tuning (verify weights work)
- [ ] Dynamic threshold adjustment (maintain 8-12 species)

**Lines:** ~60

**Test criteria:**
- HUD updates correctly every frame
- Speed buttons work (simulation accelerates)
- Birds colored by species (visual clustering)
- Best bird visibly highlighted
- Species count stabilizes at 8-12 by gen 10
- Fitness increases monotonically

---

### Phase Summary Table

| Phase | What Gets Built | Lines | Test Criteria |
|-------|----------------|-------|---------------|
| 1 | Game engine (bird, pipes, collision) | 150 | Manual play works, collision accurate |
| 2 | Genome (genes, mutations, distance) | 100 | Mutations valid, distance formula correct |
| 3 | Neural network (forward pass, AI) | 60 | Birds make decisions, inputs normalized |
| 4 | Evolution (speciation, selection, crossover) | 120 | Generations advance, fitness increases |
| 5 | Visualization (network display) | 70 | Real-time activations, correct layout |
| 6 | Polish (HUD, colors, markers) | 60 | HUD updates, species colors, best bird marker |
| **Total** | **Full v2 implementation** | **560** | **All tests pass, < 500 line target** |

**Note:** Total 560 estimate includes buffer. Actual implementation must compress to <500 via strategies in §4.5.

---

## 6. Success Criteria

### 6.1 Performance Benchmarks

**By generation 100, the AI must achieve:**

- [ ] Best bird: 50+ pipes passed (single run)
- [ ] Average top 5 birds: 30+ pipes
- [ ] Population average: 20+ pipes
- [ ] Species diversity: 5-15 active species maintained

### 6.2 Learning Curve Checkpoints

| Generation | Expected Behavior | Avg Fitness | Best Score |
|------------|-------------------|-------------|------------|
| 1 | Random chaos, immediate crashes | 50-200 | 0-1 pipe |
| 10 | Some birds pass 1-2 pipes | 200-700 | 1-3 pipes |
| 30 | Coordinated flapping, 5-10 pipes | 1000-3000 | 5-15 pipes |
| 60 | Consistent performance, rare crashes | 5000-15000 | 20-40 pipes |
| 100 | Near-perfect play, smooth flight | 25000+ | 50+ pipes |

**Failure condition:** If avg fitness plateaus for 20+ generations, NEAT parameters need tuning.

### 6.3 Diversity Metrics

**Speciation health:**
- [ ] Species count stays in 5-15 range (verified every 10 generations)
- [ ] At least 3 species reach 10+ pipes (not single-strategy dominance)
- [ ] Visual diversity: flight patterns differ across species (high flyers, low flyers, aggressive)

### 6.4 Visualization Quality

**Real-time display:**
- [ ] Neural network renders at 30fps (no lag during 10x speed)
- [ ] Activation colors visibly show decision-making (nodes light up on flap)
- [ ] Network grows over time (starts 5-8-1, reaches 5-12/15-1 by gen 100)
- [ ] Connection weights strengthen (more opaque green lines for successful strategies)

### 6.5 Code Quality

- [ ] Total file size < 500 lines (HARD LIMIT)
- [ ] No linting errors (valid HTML, CSS, JS)
- [ ] No console errors during 100-generation run
- [ ] Works on Chrome, Firefox, Safari (latest versions)
- [ ] Mobile rendering functional (600×600 canvas fits portrait)

---

## 7. Parameters Reference Card

**Quick lookup for build implementation:**

```javascript
const NEAT_CONFIG = {
    // Population
    populationSize: 120,
    elitesPerSpecies: 2,
    survivalRate: 0.2,

    // Speciation
    compatibilityThreshold: 3.0,
    thresholdAdjustment: 0.3,
    targetSpeciesMin: 8,
    targetSpeciesMax: 12,
    c1_excess: 1.0,
    c2_disjoint: 1.0,
    c3_weight: 0.4,
    smallGenomeSize: 20,

    // Mutations
    mutateWeightsProbability: 0.8,
    perturbRange: 0.3,
    replaceWeightProbability: 0.1,
    addConnectionProbability: 0.05,
    addNodeProbability: 0.03,
    disableConnectionProbability: 0.01,

    // Crossover
    crossoverProbability: 0.75,
    interspeciesMatingRate: 0.25,

    // Fitness
    fitnessFrameWeight: 1.0,
    fitnessPipeWeight: 500.0,
    fitnessDistanceWeight: 2.0,
    flapPenaltyWeight: -10.0,

    // Network
    inputNodes: 5,
    hiddenNodes: 8,
    outputNodes: 1,
    maxHiddenNodes: 20,

    // Game
    gravity: 0.6,
    jumpVelocity: -10.0,
    birdRadius: 12,
    pipeWidth: 60,
    pipeGap: 180,
    pipeSpeed: 3.0,
    pipeSpacing: 250
};
```

---

## 8. Implementation Notes

### 8.1 Innovation Number Tracking

**Critical for crossover.** Must be global, persistent across generations.

```javascript
class InnovationTracker {
    constructor() {
        this.db = new Map(); // key: "from-to", value: innovation number
        this.next = 0;
    }

    get(fromNode, toNode) {
        const key = `${fromNode}-${toNode}`;
        if (!this.db.has(key)) {
            this.db.set(key, this.next++);
        }
        return this.db.get(key);
    }
}

// Singleton instance
const innovationTracker = new InnovationTracker();
```

### 8.2 Genome Structure

**Representation:**
```javascript
class Genome {
    constructor() {
        this.nodes = [
            // {id: 0, type: 'input'},
            // {id: 1, type: 'input'},
            // ...
            // {id: 5, type: 'hidden'},
            // {id: 13, type: 'output'}
        ];

        this.connections = [
            // {from: 0, to: 5, weight: 0.5, enabled: true, innovation: 0},
            // {from: 1, to: 5, weight: -0.3, enabled: true, innovation: 1},
            // ...
        ];
    }
}
```

**Node IDs:** Never reuse. Increment global counter.

### 8.3 Fitness Sharing Implementation

```javascript
// Step 1: Assign genomes to species
speciate(population);

// Step 2: Calculate adjusted fitness
for (let species of allSpecies) {
    for (let genome of species.members) {
        genome.adjustedFitness = genome.rawFitness / species.members.length;
    }
}

// Step 3: Allocate offspring
const totalAdjusted = sumAll(genome.adjustedFitness);

for (let species of allSpecies) {
    const speciesSum = sum(species.members.adjustedFitness);
    species.offspringQuota = Math.round((speciesSum / totalAdjusted) * populationSize);
}
```

### 8.4 Visualization Layout Algorithm

**Topological sort approach:**

```javascript
function calculateLayout(genome) {
    // Step 1: Assign depth to each node
    const depths = new Map();

    // Inputs = depth 0
    genome.nodes.filter(n => n.type === 'input').forEach(n => depths.set(n.id, 0));

    // Outputs = max depth
    const maxDepth = 3; // Assume 3-layer for now
    genome.nodes.filter(n => n.type === 'output').forEach(n => depths.set(n.id, maxDepth));

    // Hidden = depth based on connections (BFS from inputs)
    // (Simplified: assign depth 1 or 2 based on connectivity)

    // Step 2: Group nodes by depth
    const layers = {};
    for (let [id, depth] of depths) {
        if (!layers[depth]) layers[depth] = [];
        layers[depth].push(id);
    }

    // Step 3: Assign x, y positions
    const positions = {};
    const xSpacing = 120;
    const yBase = 50;

    for (let depth in layers) {
        const x = depth * xSpacing + 50;
        const nodeCount = layers[depth].length;
        const ySpacing = (canvas.height - 2 * yBase) / (nodeCount + 1);

        layers[depth].forEach((nodeId, i) => {
            positions[nodeId] = {
                x: x,
                y: yBase + (i + 1) * ySpacing
            };
        });
    }

    return positions;
}
```

---

## 9. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Line count > 500** | Violates hard rule #4 | Aggressive compression (§4.5), defer features |
| **Fitness plateaus early** | AI doesn't learn | Tune mutation rates, verify speciation working |
| **Species collapse to 1** | No diversity | Dynamic threshold adjustment, verify distance calc |
| **Rendering lags at 120 birds** | Poor UX | Optimize canvas ops, reduce viz to 20fps |
| **Innovation tracking breaks crossover** | Mutations don't propagate | Unit test crossover, verify matching genes |
| **Network grows unbounded** | Exceeds maxNodes | Hard cap at 20 nodes, reject addNode if at limit |

---

## 10. V1 vs V2 Comparison

| Feature | V1 | V2 | Improvement |
|---------|----|----|-------------|
| **Population** | 50 | 120 | 2.4× more exploration |
| **Speciation** | Broken (all 1 species) | Real NEAT (8-12 species) | Diversity protected |
| **Mutations** | Weights only | Weights + structure | Topology evolves |
| **Fitness** | `frames + score×100` | Multi-component | Rewards efficiency |
| **Visualization** | None | Real-time network | Interpretability |
| **Elite preservation** | Top 5 overall | Top 2 per species | Innovation protected |
| **Learning speed** | ~60 gens to 10 pipes | ~30 gens to 10 pipes | 2× faster |
| **Max performance** | ~20 pipes (plateau) | 50+ pipes | 2.5× better |
| **Code structure** | 504 lines, monolith | <500 lines, modular | Maintainable |

---

## 11. Success Definition

**V2 is considered successful if:**

1. **Performance:** Best bird reaches 50+ pipes within 100 generations (verified across 3 independent runs)
2. **Diversity:** Species count stays in 5-15 range for all generations 10-100
3. **Learning:** Fitness curve is monotonically increasing (smoothed over 5-gen windows)
4. **Visualization:** Network renders in real-time, activations clearly visible, growth evident
5. **Code quality:** File compiles, runs without errors, total lines < 500
6. **Reproducibility:** Results consistent across Chrome/Firefox/Safari, desktop/mobile

**Failure modes:**
- Fitness plateaus before gen 50 → mutation/selection params wrong
- Species collapse to 1-2 → compatibility threshold too high
- Network explodes to 50+ nodes → addNode probability too high
- Visualization lags → rendering not optimized
- Line count > 500 → must cut features

---

## 12. Next Steps

**After this design is approved, build bees will:**

1. Implement Phase 1 (game engine) → test manual play
2. Implement Phase 2 (genome system) → test mutations
3. Implement Phase 3 (neural network) → test AI decisions
4. Implement Phase 4 (NEAT evolution) → verify learning
5. Implement Phase 5 (visualization) → verify rendering
6. Implement Phase 6 (polish) → final integration
7. Compress to <500 lines → apply §4.5 strategies
8. Run 100-generation test → verify success criteria
9. Document results → fitness graphs, screenshots, observations

**Estimated build time:** 6-8 hours (experienced JS dev)

**Deliverable:** Single HTML file, <500 lines, demonstrably superior AI learning vs v1.

---

**END OF DESIGN DOCUMENT**
