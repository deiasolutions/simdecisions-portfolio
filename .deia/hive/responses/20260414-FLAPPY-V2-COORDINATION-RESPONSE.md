# SPEC-FLAPPY-100: Self-Learning Flappy Bird v2 — Master Coordination -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-14
**Role:** Q33N (Coordinator)

## Files Modified

### Specs Created (Queue Backlog)
- `.deia/hive/queue/backlog/SPEC-FLAPPY-R01-shmup-mechanics.md` — Research spec: V1 audit + NEAT improvements research
- `.deia/hive/queue/backlog/SPEC-FLAPPY-D01-design-synthesis.md` — Design spec: Q33N synthesizes research into design doc
- `.deia/hive/queue/backlog/SPEC-FLAPPY-B01-engine-core.md` — Build spec: Game engine (bird, pipes, collision, scoring)
- `.deia/hive/queue/backlog/SPEC-FLAPPY-B02-neat-engine.md` — Build spec: NEAT engine (genome, network, mutation, speciation)
- `.deia/hive/queue/backlog/SPEC-FLAPPY-B03-training-loop.md` — Build spec: Training loop integration (multi-bird, AI, fitness, gen advancement)
- `.deia/hive/queue/backlog/SPEC-FLAPPY-B04-visualization.md` — Build spec: Visualization (HUD, neural net viz, bird coloring)
- `.deia/hive/queue/backlog/SPEC-FLAPPY-B05-controls-mobile.md` — Build spec: Controls + mobile responsiveness
- `.deia/hive/queue/backlog/SPEC-FLAPPY-B06-polish-integration.md` — Build spec: Final polish + integration into single HTML

### Coordination Response
- `.deia/hive/responses/20260414-FLAPPY-V2-COORDINATION-RESPONSE.md` — This file

## What Was Done

### V1 Analysis
Read the existing v1 Flappy Bird AI implementation (504 lines). Identified:
- **Working:** Basic NEAT with 50 birds, speed controls, HUD, genetic algorithm
- **Broken:** Trivial speciation (line 389 just groups all birds together, no real species distance calculation)
- **Missing:** Neural network visualization, best bird highlighting, mode toggle, sophisticated speciation

### Project Breakdown
Created a 3-phase coordination plan:

**Phase 1: Research (1 bee)**
- SPEC-FLAPPY-R01: Audit v1, research NEAT best practices, design neural network visualization approach
- Deliverable: Research findings document with specific recommendations

**Phase 2: Design (Q33N synthesis)**
- SPEC-FLAPPY-D01: Q33N synthesizes research into comprehensive design doc
- Deliverable: Game design, AI design (exact NEAT parameters), UX design, technical architecture, build phase plan

**Phase 3: Build (6 phased bee specs)**
1. **B01 — Game Engine Core** (~150 lines): Bird physics, pipe generation, collision, scoring, manual play mode
2. **B02 — NEAT Engine** (~200 lines): Genome, neural network, mutation, crossover, speciation (real species distance algorithm)
3. **B03 — Training Loop** (~100 lines): Multi-bird simulation, AI decision-making, fitness evaluation, generation advancement, speed controls
4. **B04 — Visualization** (~100 lines): HUD, neural network live display, bird coloring by species, best bird highlighting
5. **B05 — Controls + Mobile** (~50 lines): Keyboard (spacebar, R, 1/3/0, M), touch, on-screen buttons, responsive layout
6. **B06 — Polish + Integration** (compression to <500 lines): Merge all phases, add sound effects (Web Audio), particle effects, final polish

### Spec Design Principles

Every build spec includes:
- **EXECUTE mode directive** — "You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it."
- **Absolute file paths** — All paths specified as absolute paths
- **Test requirements** — Manual test scenarios (canvas game, no automated tests), validation criteria
- **8-section response file** — All bees must write standard response files
- **Constraints** — Line count targets, no external dependencies, no hardcoded colors, no stubs
- **Smoke tests** — Bash commands to verify deliverables

### Dependencies
```
R01 (research)
 ↓
D01 (design synthesis by Q33N)
 ↓
B01 (game engine) ──┐
                    ├──→ B03 (training loop) ──→ B04 (viz) ──→ B05 (controls) ──┐
B02 (NEAT engine) ──┘                                                           ├──→ B06 (final)
                                                                                 ┘
```

Sequential execution required for dependency chain. Parallel possible for B01 + B02 (independent components).

## Test Results

This is a coordination task. No code tests.

**Validation:**
- [x] All 8 specs created and written to `.deia/hive/queue/backlog/`
- [x] Dependencies correctly specified (R01 → D01 → B01/B02 → B03 → B04 → B05 → B06)
- [x] Every build spec has EXECUTE mode directive
- [x] Every spec has absolute file paths, test requirements, 8-section response template
- [x] Total expected code: ~600 lines pre-compression, <500 lines final (within constraint)
- [x] Research spec focuses on NEAT improvements and neural net viz (addresses v1 weaknesses)
- [x] Design spec is Q33N work (not dispatched to bee)
- [x] Final deliverable: single HTML file at `browser/public/games/flappy-bird-ai-v2-20260407.html`

## Build Verification

**Specs queued:** 8 total
```bash
ls .deia/hive/queue/backlog/SPEC-FLAPPY-*.md | wc -l
# Expected output: 8
```

**Coordination response written:**
```bash
test -f ".deia/hive/responses/20260414-FLAPPY-V2-COORDINATION-RESPONSE.md" && echo RESPONSE
# Expected output: RESPONSE
```

## Acceptance Criteria

From SPEC-FLAPPY-100:

- [x] **Specs created:** Research (R01), Design (D01), Build (B01-B06) — 8 total
- [x] **Execution plan:** Phased build with clear dependencies
- [x] **Target deliverable:** `browser/public/games/flappy-bird-ai-v2-20260407.html` (single file, <500 lines)
- [x] **EXECUTE mode:** All build specs include "Do NOT enter plan mode. Do NOT ask for approval. Just build it."
- [x] **Features covered:**
  - Playable Flappy Bird game (B01)
  - NEAT neuroevolution with 50+ birds (B02, B03)
  - AI visibly improves over generations (B03 — fitness tuning, B02 — proper speciation)
  - HUD with all stats (B04)
  - Speed controls 1x/3x/10x (B03)
  - Neural network visualization (B04)
  - Mobile responsive + touch controls (B05)
  - Single HTML, no external dependencies (B06)
- [x] **Constraints enforced:**
  - No file over 500 lines (B06 compresses to <500)
  - No external dependencies (all specs specify "Canvas API only, Vanilla JS")
  - V1 audit included (R01)

## Clock / Cost / Carbon

**Clock:** 18 minutes (spec writing)
**Cost:** ~$0.15 USD (Sonnet for coordination)
**Carbon:** ~0.02 kg CO2e (estimated)

## Issues / Follow-ups

### Next Steps (for Q33NR or Queue Runner)

1. **Dispatch R01** — Research bee to audit v1 and research NEAT improvements
2. **Wait for R01 completion** — Findings document becomes input for D01
3. **Q33N executes D01** — Q33N reads research, synthesizes design doc (Q33N does this work, not dispatched to bee)
4. **Dispatch B01 + B02 in parallel** — Game engine and NEAT engine are independent
5. **Sequential dispatch B03 → B04 → B05 → B06** — Each phase depends on previous
6. **Verify final deliverable** — Test `flappy-bird-ai-v2-20260407.html` against all acceptance criteria from SPEC-FLAPPY-100

### Known Challenges

**Line count constraint:** Target <500 lines total. Pre-compression estimate is ~600 lines. B06 must:
- Remove verbose comments
- Compact functions (arrow functions, ternary operators)
- Remove debug logging
- Consolidate duplicate code
- If still over 500: consider reducing neural network viz complexity or removing less critical features

**Speciation algorithm:** V1 has no real speciation (line 389 trivial). R01 must research and recommend a proper compatibility distance formula. B02 must implement it correctly.

**Mobile audio:** iOS requires user interaction before playing audio. B06 must handle this (play silent sound on first touch to initialize Web Audio context).

**Performance:** 50 birds at 60fps is demanding. B01/B03 must optimize rendering (skip dead birds, use efficient collision detection). B04 must optimize neural net viz (skip at 10x speed).

**Testing:** No automated tests for canvas game. All testing is manual. Bees must document test results thoroughly in response files.

### Potential Optimizations (if line count becomes issue in B06)

1. **Remove particle effects** — Save ~30 lines
2. **Simplify neural net viz** — Show network diagram but skip live activation display — Save ~20 lines
3. **Remove sound effects** — Save ~40 lines
4. **Remove human play mode** — AI-only — Save ~20 lines

Total potential savings: ~110 lines. Should be enough to hit <500 target.

### Research Focus for R01

Critical questions for R01 to answer:
1. **Speciation distance formula:** What formula for calculating genome compatibility distance? (NEAT paper uses δ = c1*E/N + c2*D/N + c3*W where E=excess genes, D=disjoint genes, W=avg weight diff)
2. **Distance threshold:** What threshold for same species vs new species? (NEAT paper uses δ_t = 3.0)
3. **Hidden layer size:** 5 inputs, how many hidden nodes? (v1 uses 8, is that optimal? Should it be 6? 10?)
4. **Mutation rates:** Weight perturbation (v1 uses 0.1), add connection (not in v1), add node (not in v1)
5. **Fitness function weights:** frames_survived + 100*pipes_passed (is 100 the right multiplier? Should it be 50? 200?)
6. **Neural net viz:** What's the clearest way to show 5-8-1 network on canvas? Vertical arrangement? Horizontal? Diagonal?

R01 must provide **specific numeric values** for all parameters, not ranges or "tune as needed."

## Deliverables Summary

| Spec ID | Type | Model | Role | Depends On | Deliverable |
|---------|------|-------|------|------------|-------------|
| FLAPPY-R01 | Research | sonnet | bee | — | Research findings doc |
| FLAPPY-D01 | Design | sonnet | queen | R01 | Design doc (Q33N work) |
| FLAPPY-B01 | Build | sonnet | bee | D01 | Game engine JS |
| FLAPPY-B02 | Build | sonnet | bee | D01 | NEAT engine JS |
| FLAPPY-B03 | Build | sonnet | bee | B01, B02 | Training loop JS |
| FLAPPY-B04 | Build | sonnet | bee | B03 | Visualization JS |
| FLAPPY-B05 | Build | sonnet | bee | B04 | Controls JS |
| FLAPPY-B06 | Build | sonnet | bee | B01-B05 | Final HTML (single file) |

**Final output:** `browser/public/games/flappy-bird-ai-v2-20260407.html`

---

## Coordination Complete

All specs written and queued in `.deia/hive/queue/backlog/`. Ready for dispatch by Q33NR or queue runner.

The build is structured, dependencies are clear, and all constraints are enforced at the spec level. Bees have clear instructions and test requirements. The design will be data-driven (research findings → design doc → build specs).

**Estimated total cost for full build:** ~$2-3 USD (1 research bee, 1 Q33N design session, 6 build bees)
**Estimated total time:** ~4-6 hours (sequential execution) or ~2-3 hours (with parallelization of B01+B02)
