---
id: RAIDEN-B08
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-B07, RAIDEN-R03]
---
# SPEC-RAIDEN-B08: AI System (NEAT Neuroevolution)

## Priority
P1

## Model Assignment
sonnet

## Role
bee (b33 — you write code and tests)

## Depends On
- RAIDEN-B07 (sound effects)
- RAIDEN-R03 (AI research — for architecture specs)

## Objective
Implement NEAT neuroevolution AI that learns to play the game, with auto-play and hybrid modes.

## You are in EXECUTE mode
Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.

## Design Reference
Read:
- `.deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md` (Section 10: AI Specification)
- `.deia/hive/responses/20260413-RAIDEN-R03-AI-RESEARCH.md` (full AI architecture)
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\public\games\flappy-bird-ai-v1-20260407.html` (NEAT reference implementation)

## Deliverables

### File: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\public\games\raiden-v1-20260413.html`

**Add to existing engine:**

1. **NEAT Implementation (copy and adapt from flappy-bird-ai)**
   - Genome class: Genes (connections), nodes, fitness
   - Species class: Group similar genomes, shared fitness
   - Population class: Manage 50 genomes, crossover, mutation
   - Neural network: Forward propagation (inputs → hidden → outputs)
   - Mutation: Add node (3%), add connection (5%), mutate weight (80%)
   - Crossover: Combine two parent genomes, inherit from fitter parent

2. **State Space (from AI research doc)**
   **Inputs to neural network (normalized 0-1):**
   - Player X position (0-800 → 0-1)
   - Player Y position (0-600 → 0-1)
   - Player velocity X, Y (normalized)
   - Closest 5 enemies: X, Y, type (5 * 3 = 15 inputs)
   - Closest 10 bullets: X, Y, velocity X, Y (10 * 4 = 40 inputs)
   - Closest 3 power-ups: X, Y, type (3 * 3 = 9 inputs)
   - Current weapon tier (0-5 → 0-1)
   - Current health (0-3 → 0-1)

   **Total: ~72 input nodes**

3. **Action Space (from AI research doc)**
   **Outputs from neural network:**
   - Move X: -1 to 1 (left/right)
   - Move Y: -1 to 1 (up/down)
   - Fire: 0-1 (threshold 0.5 = fire, but we have auto-fire, so ignore)
   - Bomb: 0-1 (threshold 0.8 = bomb, rare action)

   **Total: 4 output nodes**

4. **Fitness Function (from AI research doc)**
   ```javascript
   fitness = (survival_time * 10)
           + (score * 0.1)
           + (enemies_killed * 50)
           + (power_ups_collected * 100)
           - (damage_taken * 200)
           + (level_reached * 1000)
   ```

5. **Training Loop**
   - Population size: 50 genomes
   - Each genome plays until death or 60 seconds
   - Evaluate fitness at end of run
   - Top 10 genomes survive (elitism)
   - Remaining 40 slots: Tournament selection + crossover + mutation
   - Run one genome at a time (not parallel, to avoid slowdown)

6. **Auto-Play Mode**
   - Press A key to toggle AI mode
   - AI takes control of player ship
   - Player can watch AI play
   - Display AI generation and best score in top-right corner

7. **Hybrid Mode (AI-Assisted)**
   - Press H key to toggle hybrid mode
   - AI controls movement (dodge bullets)
   - Player controls firing (shoot and bomb manually, disable auto-fire)
   - Ghost overlay shows AI's intended movement (semi-transparent)

8. **AI Visualization**
   - Top-right corner: "AI Gen: 42 | Best: 12,450"
   - Color-code AI ship: Blue tint when AI active
   - Fitness graph (optional): Small line chart showing fitness over generations

9. **Genome Persistence**
   - Save best genome to localStorage after each generation
   - Load best genome on page reload (continue training)
   - Export/import genome (copy JSON to clipboard for sharing)

## Technical Constraints
- Copy NEAT code from flappy-bird-ai-v1-20260407.html (genome, species, network)
- Adapt state/action mappings for shmup (different inputs/outputs than flappy bird)
- Run training in background: One genome per frame, doesn't block rendering
- Performance: AI should not drop framerate below 30fps during training

## Acceptance Criteria
- [ ] NEAT neuroevolution implemented (genome, species, population)
- [ ] 72 input nodes (player state + enemies + bullets + power-ups)
- [ ] 4 output nodes (move X, move Y, fire, bomb)
- [ ] Fitness function rewards survival, score, kills, power-ups
- [ ] Population of 50 genomes trains over generations
- [ ] Auto-play mode: AI controls player (A key toggle)
- [ ] Hybrid mode: AI moves, player shoots (H key toggle)
- [ ] AI generation and best score displayed
- [ ] Best genome persists to localStorage
- [ ] AI improves over time (survives longer by generation 20+)
- [ ] No errors in console
- [ ] 30fps minimum during AI training

## Tests (Manual Smoke Tests)
```javascript
// Test: AI training
// 1. Press A to activate AI mode
// 2. AI plays game, dies, respawns as next genome
// 3. See generation counter increment (Gen: 1 → 2 → 3 ...)
// 4. By generation 10, AI survives longer than random movement
// 5. By generation 20, AI reaches level 2+

// Test: Fitness function
// 1. AI that survives longer has higher fitness
// 2. AI that collects power-ups has higher fitness
// 3. AI that avoids damage has higher fitness

// Test: Auto-play mode
// 1. Press A, AI takes control
// 2. Player ship moves autonomously (dodges bullets, shoots enemies)
// 3. Press A again, player regains control

// Test: Hybrid mode
// 1. Press H, AI controls movement
// 2. Player must manually shoot (spacebar) and bomb (B)
// 3. See ghost overlay showing AI's intended path
// 4. Press H again, back to normal

// Test: Genome persistence
// 1. Train AI for 10 generations
// 2. Refresh page
// 3. AI resumes training from generation 11 (loaded from localStorage)

// Test: Performance
// 1. During AI training, check FPS (press F)
// 2. Should be at least 30fps even with 50 genomes in population
```

## Smoke Test
```bash
grep -q "NEAT" "browser/public/games/raiden-v1-20260413.html" && \
grep -q "genome" "browser/public/games/raiden-v1-20260413.html" && \
grep -q "fitness" "browser/public/games/raiden-v1-20260413.html" && \
grep -q "neural" "browser/public/games/raiden-v1-20260413.html" && \
echo "PASS"
```

## Response Location
`.deia/hive/responses/20260413-RAIDEN-B08-AI-SYSTEM-RESPONSE.md`

## Notes
- This is the most complex spec (AI system is non-trivial).
- Copy heavily from flappy-bird-ai reference implementation.
- State space design is critical (what AI observes affects learning).
- Fitness function tuning may require iteration (adjust weights empirically).
- Next spec (B09) polishes mobile experience.
- AI should be fun to watch (like flappy bird AI learning to fly).
