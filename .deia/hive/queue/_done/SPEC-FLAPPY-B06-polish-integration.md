---
id: FLAPPY-B06
priority: P2
model: sonnet
role: bee
depends_on: [FLAPPY-B01, FLAPPY-B02, FLAPPY-B03, FLAPPY-B04, FLAPPY-B05]
---
# SPEC-FLAPPY-B06: Polish + Final Integration

## Priority
P2

## Model Assignment
sonnet

## Role
bee

## Depends On
- FLAPPY-B01 (game engine)
- FLAPPY-B02 (NEAT engine)
- FLAPPY-B03 (training loop)
- FLAPPY-B04 (visualization)
- FLAPPY-B05 (controls + mobile)

## Objective
Integrate all phases into a single HTML file, add sound effects and particle effects, and deliver the final polished game.

## Context
This is Phase 6 (final phase) of the Flappy Bird AI v2 build.

You have 5 separate JS files from phases B01-B05:
- `flappy-b01-engine.js` — game engine (~150 lines)
- `flappy-b02-neat.js` — NEAT engine (~200 lines)
- `flappy-b03-training.js` — training loop (~100 lines)
- `flappy-b04-viz.js` — visualization (~100 lines)
- `flappy-b05-controls.js` — controls (~50 lines)

Total: ~600 lines. Target: <500 lines in the final file.

You must:
1. Merge all JS into one file
2. Compress code where possible (remove verbose comments, compact functions)
3. Add sound effects (Web Audio API)
4. Add particle effects (bird flap, bird death, pipe pass)
5. Final polish (CSS, animations, transitions)
6. Deliver as single HTML file: `browser/public/games/flappy-bird-ai-v2-20260407.html`

## You are in EXECUTE mode
**Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.**

## Files to Read First
- `browser/public/games/flappy-b01-engine.js`
- `browser/public/games/flappy-b02-neat.js`
- `browser/public/games/flappy-b03-training.js`
- `browser/public/games/flappy-b04-viz.js`
- `browser/public/games/flappy-b05-controls.js`
- `browser/public/games/flappy-bird-ai-v1-20260407.html`
  Reference v1 for styling inspiration

## Deliverables

### 1. Code Integration
- [ ] Merge all 5 JS files into single `<script>` block
- [ ] Remove duplicate code (constants defined in multiple files)
- [ ] Remove test harnesses and debug logging
- [ ] Compress verbose comments (keep essential ones)
- [ ] Ensure all functions work after merge (no scope conflicts)
- [ ] Target: <500 lines total (HTML + CSS + JS)

### 2. Sound Effects (Web Audio API)
- [ ] Flap sound (synthesized tone, not external file)
- [ ] Death sound (synthesized, low tone)
- [ ] Score sound (synthesized, high tone — plays when passing pipe)
- [ ] Mute button (M key or on-screen button)
- [ ] Sound effects work on mobile (iOS requires user interaction first)

### 3. Particle Effects
- [ ] Bird flap: small particles trail behind bird when flapping
- [ ] Bird death: explosion effect (particles scatter)
- [ ] Pipe pass: sparkle or confetti when bird passes pipe
- [ ] Particles fade out over time (don't clutter screen)

### 4. CSS Polish
- [ ] Gradient background (sky blue to darker blue)
- [ ] HUD: rounded corners, semi-transparent background, shadow
- [ ] Buttons: hover effects, active states, smooth transitions
- [ ] Canvas: border, shadow, rounded corners
- [ ] Responsive: mobile-friendly spacing and font sizes

### 5. Final Verification
- [ ] AI visibly improves over generations (gen 1 terrible, gen 50+ near-perfect)
- [ ] All acceptance criteria from SPEC-FLAPPY-100 met:
  - Playable Flappy Bird game
  - NEAT neuroevolution with 50+ birds
  - HUD with all stats
  - Speed controls (1x, 3x, 10x)
  - Neural network visualization
  - Mobile responsive with touch controls
  - Single HTML file, no external dependencies
- [ ] No console errors
- [ ] Smooth 60fps at 1x speed

### 6. Cleanup
- [ ] Delete temporary test files: `flappy-b01-test.html`, `flappy-b02-test.html`, etc.
- [ ] Delete temporary JS files: `flappy-b01-engine.js`, `flappy-b02-neat.js`, etc.
- [ ] Keep only `flappy-bird-ai-v2-20260407.html`

## Test Requirements

Manual test (comprehensive):
- [ ] Open `browser/public/games/flappy-bird-ai-v2-20260407.html` in browser
- [ ] Verify 50 birds spawn at generation 1
- [ ] Verify birds make decisions (some flap, some don't)
- [ ] Verify birds die on collision
- [ ] Verify generation advances when all birds die
- [ ] Run to generation 20 at 10x speed — verify best score increases significantly
- [ ] Test speed controls (1x, 3x, 10x) — verify speed changes
- [ ] Test mode toggle (AI ↔ Human) — verify manual play works
- [ ] Test keyboard controls (spacebar, R, 1/3/0, M)
- [ ] Test sound effects (flap, death, score) — verify audio plays
- [ ] Test mute button — verify audio stops
- [ ] Test particle effects (flap, death, pass) — verify particles appear
- [ ] Test mobile: open on phone or Chrome DevTools mobile emulation
  - Verify tap to flap works
  - Verify on-screen buttons work
  - Verify layout is responsive
  - Verify no horizontal scroll
- [ ] Verify neural network visualization displays and updates live
- [ ] Verify best bird is highlighted
- [ ] Verify birds are colored by species
- [ ] Verify no console errors
- [ ] Verify file size is <50KB (should be ~20-30KB uncompressed)

Performance test:
- Run for 100 generations at 10x speed
- Verify no memory leaks (check Chrome Task Manager)
- Verify no performance degradation over time
- Document best score at gen 100 (should be very high, 50+ pipes)

## Constraints
- **CRITICAL:** Final file must be <500 lines total (HTML + CSS + JS)
- No external dependencies (no CDN, no external files)
- All sounds synthesized with Web Audio API (no external audio files)
- All effects rendered with Canvas API (no external libraries)
- No stubs — every function fully implemented
- File must work offline (no network requests)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260414-FLAPPY-B06-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — comprehensive manual test, performance test, 100-gen training log
5. **Build Verification** — file size, line count, feature checklist
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Output Location
`browser/public/games/flappy-bird-ai-v2-20260407.html` — final game file
`.deia/hive/responses/20260414-FLAPPY-B06-RESPONSE.md` — response file

## Acceptance Criteria
- [ ] All 5 JS files merged into single `<script>` block in one HTML file
- [ ] Final file at `browser/public/games/flappy-bird-ai-v2-20260407.html`
- [ ] Total line count < 500 (HTML + CSS + JS)
- [ ] Sound effects: flap, death, score (Web Audio API, synthesized)
- [ ] Mute button works
- [ ] Particle effects: flap trail, death explosion, pipe pass sparkle
- [ ] CSS polish: gradient background, rounded HUD, button hover/active states
- [ ] AI visibly improves over generations (gen 1 terrible, gen 50+ near-perfect)
- [ ] No console errors, smooth 60fps, works offline
- [ ] Temporary test/JS files cleaned up
- [ ] Response file at `.deia/hive/responses/20260414-FLAPPY-B06-RESPONSE.md`

## Smoke Test
- [ ] `test -f browser/public/games/flappy-bird-ai-v2-20260407.html` passes
- [ ] Line count of final file is under 500
- [ ] `test ! -f browser/public/games/flappy-b01-test.html` passes (cleanup verified)
