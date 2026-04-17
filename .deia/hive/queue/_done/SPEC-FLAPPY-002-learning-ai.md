---
id: FLAPPY-002
priority: P1
model: sonnet
role: bee
depends_on: []
---
# SPEC-FLAPPY-002: Flappy Bird with Neuroevolution AI

## Priority
P1

## Model Assignment
sonnet

## Depends On
(none)

## Intent
Build a Flappy Bird game with a built-in NEAT-style neuroevolution AI that learns to play in real-time. Population of 50 birds evolves over generations. Single HTML file, no dependencies.

## Acceptance Criteria
- [ ] New file `browser/public/games/flappy-bird-ai-v1-20260407.html`
- [ ] Canvas-based Flappy Bird with pipes, gravity, collision, scoring
- [ ] NEAT neuroevolution in vanilla JS: 50 neural networks controlling 50 birds simultaneously
- [ ] NN inputs: bird_y, bird_velocity, dist_to_pipe, pipe_gap_y, pipe_gap_size (normalized 0-1)
- [ ] NN output: flap probability (sigmoid, flap if > 0.5)
- [ ] Fitness: frames_survived + 100 * pipes_passed
- [ ] Selection: top 20% survive. Mutation: weight perturbation, add connection, add node. Crossover. Elitism top 5.
- [ ] HUD: generation number, alive count, best score this gen, best score all time, species count
- [ ] Speed control buttons: 1x, 3x, 10x
- [ ] Auto-advance generations when all birds die
- [ ] Mobile touch support for manual play mode
- [ ] All code in ONE HTML file, no external dependencies, canvas API only

## Constraints
- Single HTML file. No build step. No npm.
- Vanilla JS neural network from scratch.
- Canvas API only.
- Must run at 60fps with 50 birds on a modern laptop.
- No file over 500 lines.

## Smoke Test
```bash
test -f browser/public/games/flappy-bird-ai-v1-20260407.html && echo EXISTS
```
