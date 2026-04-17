---
id: FLAPPY-FIX-001
priority: P1
model: sonnet
role: bee
depends_on: []
---
# SPEC-FLAPPY-FIX-001: Fix Flappy Bird AI v2 crash after first death

## Priority
P1

## Model Assignment
sonnet

## Role
bee

## Depends On
None

## Objective
Fix the Flappy Bird AI v2 game which crashes after the first generation of birds all die. The game renders correctly on load and birds start flying, but when all 120 birds die and the game tries to advance to generation 2, it crashes and stops.

## Context
The game is a single HTML file with minified JavaScript. It uses NEAT neuroevolution with 120 birds. The crash occurs in the generation advancement flow: `updAI()` detects all birds dead → calls `nextG()` → `ga.next()` which runs speciation, crossover, mutation → creates new birds → should restart.

The code is heavily minified with single-letter variable names. Read carefully.

Known issues to investigate:
1. The `updAI()` method (line ~124) — check for variable scoping issues, undefined references
2. The `nextG()` method (line ~127) — check `ga.next()` call chain for crashes
3. The `GA.next()` method (line ~92) — speciation, crossover, and mutation — check for edge cases (empty species, division by zero in fitness sharing, etc.)
4. The `Genome.cross()` method (line ~75) — check crossover for missing nodes
5. The `Genome.dist()` method (line ~70) — check distance calculation for edge cases (empty connection lists, Math.max with empty arrays)
6. `Bird.calcFit()` (line ~105) — check for null/undefined genome reference

Common JS pitfalls in this code:
- `Math.max(...[])` returns `-Infinity` which can poison calculations
- Division by zero in fitness sharing when total adjusted fitness is 0
- Species with 0 members after speciation
- Crossover producing genomes with missing node references

## You are in EXECUTE mode
**Debug the crash, fix it, verify the game runs for 50+ generations without crashing. Do NOT enter plan mode. Do NOT ask for approval. Just fix it.**

## Files to Read First
browser/public/games/flappy-bird-ai-v2-20260407.html

## Deliverables

### 1. Identify the crash
- [ ] Open the game in a browser (or read the code carefully)
- [ ] Identify the exact line and cause of the crash after first death
- [ ] Document the root cause

### 2. Fix the crash
- [ ] Fix the root cause so generation advancement works
- [ ] Ensure the fix handles edge cases (empty species, zero fitness, etc.)
- [ ] Do NOT rewrite the game — make minimal targeted fixes

### 3. Verify stability
- [ ] Game runs for 50+ generations without crashing
- [ ] AI birds visibly improve over generations
- [ ] Human mode still works (toggle with M key, spacebar to flap)
- [ ] Speed controls work (1x, 3x, 10x)
- [ ] No console errors

## Test Requirements
- [ ] Load game, let AI run for 50 generations at 10x speed — no crash
- [ ] Switch to human mode, play, switch back to AI — no crash
- [ ] Click restart button — game resets cleanly, runs again
- [ ] Open browser console — no errors

## Constraints
- Single HTML file, no external dependencies
- Minimal changes — fix bugs, don't rewrite
- Keep the minified style (don't expand/reformat the whole file)
- File must work via file:// protocol (no server required)

## Acceptance Criteria
- [ ] Game runs for 50+ generations without crashing at 10x speed
- [ ] Root cause documented in response file
- [ ] Fix is minimal and targeted (not a rewrite)
- [ ] Human mode works after fix
- [ ] No console errors during 50-generation run
- [ ] Response file at `.deia/hive/responses/20260414-FLAPPY-FIX-001-RESPONSE.md`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260414-FLAPPY-FIX-001-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes with line numbers
4. **Test Results** — 50-generation run log, human mode test
5. **Build Verification** — game loads, runs, no console errors
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — any remaining edge cases

DO NOT skip any section.

## Output Location
browser/public/games/flappy-bird-ai-v2-20260407.html
.deia/hive/responses/20260414-FLAPPY-FIX-001-RESPONSE.md

## Smoke Test
- [ ] `test -f browser/public/games/flappy-bird-ai-v2-20260407.html` passes
- [ ] `test -f .deia/hive/responses/20260414-FLAPPY-FIX-001-RESPONSE.md` passes
