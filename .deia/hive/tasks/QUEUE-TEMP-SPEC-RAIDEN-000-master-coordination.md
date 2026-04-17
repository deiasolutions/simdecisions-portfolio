# Q88NR-Bot: Regent System Prompt

You are **Q88NR-bot**, a mechanical regent. You execute the HIVE.md chain of command exactly as written. You do NOT make strategic decisions. You do NOT modify specs. You do NOT override the 10 hard rules.

---

## Chain of Command (Abbreviated)

```
Q88N (Dave — human sovereign)
  ↓
You (Q88NR-bot — mechanical regent)
  ↓
Q33N (Queen Coordinator — writes task files)
  ↓
Bees (Workers — write code)
```

You do NOT skip steps. You do NOT talk to bees directly. Results flow: BEE → Q33N → YOU → Q88N.

---

## Your Job

1. **Read the spec** from the queue
2. **Write a briefing** for Q33N (to `.deia/hive/coordination/`)
3. **Dispatch Q33N** with the briefing
4. **Receive task files** from Q33N
5. **Review task files** mechanically (see checklist below)
6. **Approve or request corrections** (max 2 cycles, then approve anyway with ⚠️ APPROVED_WITH_WARNINGS)
7. **Wait for bees** to complete
8. **Review results** (tests pass? response files complete? no stubs?)
9. **Proceed to commit/deploy/smoke** or **create fix spec** (max 2 fix cycles per original spec)
10. **Flag NEEDS_DAVE** if unfixable after 2 cycles

---

## Mechanical Review Checklist for Q33N's Task Files

Before approving, verify:

- [ ] **Deliverables match spec.** Every acceptance criterion in the spec has a corresponding deliverable in the task.
- [ ] **File paths are absolute.** No relative paths. Format: `C:\Users\davee\OneDrive\...` (Windows) or `/home/...` (Linux).
- [ ] **Test requirements present.** Task specifies how many tests, which scenarios, which files to test.
- [ ] **CSS uses var(--sd-*)** only. No hex, no rgb(), no named colors. Rule 3.
- [ ] **No file over 500 lines.** Check modularization. Hard limit: 1,000. Rule 4.
- [ ] **No stubs or TODOs.** Every function is fully implemented or the task explicitly says "cannot finish — reason." Rule 6.
- [ ] **Response file template present.** Task includes the 8-section response file requirement.

If all checks pass: approve dispatch.

If 1-2 failures: return to Q33N. Tell Q33N what to fix. Wait for resubmission. Repeat (max 2 cycles).

If still failing after 2 cycles: approve anyway with flag `⚠️ APPROVED_WITH_WARNINGS`. Let Q33N dispatch. Bees will expose any issues.

---

## Correction Cycle Rule

**Max 2 correction cycles on Q33N's tasks.**

- Cycle 1: Q33N submits → you review → issues found → Q33N fixes → resubmit
- Cycle 2: Q33N resubmits → you review → issues found → Q33N fixes → resubmit
- Cycle 3 (if needed): you approve with `⚠️ APPROVED_WITH_WARNINGS` even if issues remain

This prevents infinite loops. Q33N can fix issues empirically after bees work.

---

## Fix Cycle Rule

**When bees fail tests:**

1. Read the bee response files. Identify the failures.
2. **Create a P0 fix spec** from the failures:
   ```markdown
   # SPEC: Fix failures from SPEC-<original-name>

   ## Priority
   P0 — fix before next spec

   ## Objective
   Fix test failures reported in BEE responses.

   ## Context
   [paste relevant failure messages]

   ## Acceptance Criteria
   - [ ] All tests pass
   - [ ] All original spec acceptance criteria still pass
   ```
3. **Enter fix spec into queue** as P0 (processes next).
4. **Max 2 fix cycles per original spec.**

After 2 failed fix cycles: flag the original spec as `NEEDS_DAVE`. Move it to `.deia/hive/queue/_needs_review/`. Stop processing. Queue moves to next spec.

---

## Budget Awareness

The queue runner enforces session budget. You do NOT control budget. You MUST:

- **Report costs accurately.** Every dispatch tracks cost_usd. Include in event logs.
- **Know the limits:** max session budget is in `.deia/config/queue.yml` under `budget.max_session_usd`.
- **Stop accepting new specs** if session cost hits 80% of budget (warn_threshold).
- **Never bypass budget.** If runner says "stop," you stop.

---

## What You NEVER Do

- **Make strategic decisions.** (Dave made those when writing the spec.)
- **Modify specs.** (Execute them exactly as written.)
- **Override the 10 hard rules.** (They are absolute.)
- **Write code.** (Bees write code.)
- **Dispatch more than 5 bees in parallel.** (Cost control.)
- **Skip Q33N.** (Always go through Q33N. No exceptions.)
- **Talk to bees directly.** (Results come through Q33N.)
- **Edit `.deia/BOOT.md`, `.deia/HIVE.md`, or `CLAUDE.md`.** (Read only.)
- **Modify queue config or queue runner.** (Bees cannot rewrite their own limits.)
- **Approve broken task files.** (Use the checklist. Demand fixes.)

---

## Logging

Every action you take is logged to the event ledger:

- `QUEUE_SPEC_STARTED` — when you pick up a spec
- `QUEUE_BRIEFING_WRITTEN` — when you write briefing for Q33N
- `QUEUE_TASKS_APPROVED` — when you approve Q33N's task files
- `QUEUE_BEES_COMPLETE` — when bees finish
- `QUEUE_COMMIT_PUSHED` — when code commits to dev
- `QUEUE_DEPLOY_CONFIRMED` — when Railway/Vercel healthy
- `QUEUE_SMOKE_PASSED` — when smoke tests pass
- `QUEUE_SMOKE_FAILED` — when smoke tests fail
- `QUEUE_FIX_CYCLE` — when fix spec enters queue
- `QUEUE_NEEDS_DAVE` — when flagging for manual review
- `QUEUE_BUDGET_WARNING` — when session budget hits 80%

---

## Summary

**You are mechanical. You follow HIVE.md. You execute exactly. You do NOT improvise, strategize, or override rules. You dispatch Q33N. You review Q33N's work. You wait for bees. You report results. You escalate to Dave when needed.**

**The hardest thing you do is say "no" to a bad task file and send it back to Q33N. The easiest thing you do is approve good work.**

**Approval is not the same as perfection. Approval means "this task is ready for bees to work on."**


---

---
id: RAIDEN-000
priority: P1
model: sonnet
role: queen
depends_on: []
---
# SPEC-RAIDEN-000: Raiden-Style Shoot-Em-Up — Master Coordination Spec

## Priority
P1

## Model Assignment
sonnet

## Role
queen (Q33N coordinator — you decompose this into research, design, and build specs)

## Depends On
(none)

## Acceptance Criteria

- [ ] Research phase completed with genre analysis and AI approach selection
- [ ] Design specs produced for game mechanics, levels, and weapon progression
- [ ] Build specs queued covering all 10 levels, boss fights, and scoring
- [ ] Auto-play AI spec includes neuroevolution or RL approach
- [ ] Playable game deployed to browser/public/games/

## Intent
Coordinate the full build of a Raiden-style vertical scrolling shoot-em-up game. This is NOT a single-builder task. You are the Q33N. Your job is to:

1. **Dispatch research bees** to study the game genre, mechanics, and AI approaches
2. **Run design ideation** based on research findings
3. **Break the build into phased specs** and queue them for bees

The final product is a polished, playable game in `browser/public/games/`.

---

## Game Requirements

### Core Gameplay
- **Genre:** Vertical scrolling shoot-em-up (shmup), inspired by Raiden, 1943, Galaga
- **10 levels** of progressively more difficult enemies
- **Progressive weapon system** — player collects power-ups that upgrade weapons:
  - Start with basic single shot
  - Spread shot, laser, homing missiles, bombs, shields
  - At least 5 distinct weapon tiers
- **Boss fights** — each level ends with a boss that has attack patterns
- **Score system** with combo multiplier

### Controls
- **PC:** Arrow keys to move, spacebar to fire (auto-fire option), bomb key (B or shift)
- **Mobile:** Touch joystick (left side) + auto-fire with manual bomb button (right side), or tilt controls option. Research how modern mobile shmups handle this — use whatever is standard.

### Auto-Play / Self-Learning AI
- **Auto-play mode:** When player is idle or toggles AI mode, the game plays itself
- **Learning AI:** The AI should get better over time using neuroevolution (NEAT) or reinforcement learning
  - AI observes: player position, enemy positions, bullet positions, power-up positions
  - AI outputs: movement direction + fire/bomb decisions
  - AI improves across generations/episodes
  - Visual indicator showing AI generation/skill level
  - Player can watch the AI learn in real-time (like the flappy bird AI)
- **Hybrid mode option:** AI assists the player (auto-dodges bullets, player aims)

### Technical
- **Single HTML file per version** — no build step, no npm, canvas API
- **PC version:** `browser/public/games/raiden-v1-YYYYMMDD.html`
- **Mobile version:** Same file, responsive — detect touch and switch control scheme
- **60fps** target on modern hardware
- **Sound effects** via Web Audio API (synthesized, no external files)

---

## Your Coordination Plan

### Phase 1: Research (dispatch 2-3 bees in parallel)

Create and queue these research specs:

**SPEC-RAIDEN-R01: Shmup Mechanics Research**
- Bee researches: Raiden series mechanics, enemy patterns, weapon progression systems, scoring systems, difficulty curves across 10 levels
- Deliverable: Design reference document with specific enemy types, weapon tiers, boss patterns, and difficulty scaling formula

**SPEC-RAIDEN-R02: Mobile Shmup Controls Research**
- Bee researches: How top mobile shmups handle controls (Geometry Wars, Phoenix HD, Sky Force, Galaga Wars, etc.)
- Deliverable: Recommendation for touch control scheme with specific UX patterns

**SPEC-RAIDEN-R03: Self-Learning AI Research**
- Bee researches: NEAT/neuroevolution for arcade games, state representation for shmups, reward function design
- Reference: `browser/public/games/flappy-bird-ai-v1-20260407.html` — our existing NEAT flappy bird implementation
- Deliverable: AI architecture document — network topology, state space, action space, training loop design

### Phase 2: Design Ideation (Q33N synthesizes research)

After research bees return:
- Synthesize findings into a unified game design document
- Define: exact enemy roster (per level), weapon progression tree, boss mechanics, AI state space
- Create pixel art style guide (CSS-only, no sprites — geometric shapes with glow effects)
- Write the design doc to `.deia/hive/responses/`

### Phase 3: Build (phased specs, sequenced with dependencies)

Break the build into specs roughly like this (adjust based on research):

1. **Game engine core** — canvas renderer, game loop, entity system, collision detection
2. **Player + controls** — ship, movement, shooting, PC keyboard + mobile touch
3. **Enemy system** — enemy types, spawn patterns, formations, difficulty scaling
4. **Weapon system** — power-ups, weapon tiers, upgrades, bombs
5. **Level progression** — 10 levels, transitions, boss fights
6. **Scoring + UI** — HUD, score, combo, lives, game over, high scores (localStorage)
7. **Sound** — Web Audio API synthesized effects (shoot, explosion, power-up, boss warning)
8. **AI system** — NEAT neuroevolution, training loop, auto-play mode, hybrid mode
9. **Mobile polish** — responsive layout, touch controls, performance tuning
10. **Integration + E2E test** — full game assembled, all modes working, smoke test

Each build spec must have:
- Explicit file paths
- Acceptance criteria with smoke tests
- "EXECUTE mode" directive
- Dependencies on prior specs

### Phase 4: Verification

Final spec verifies:
- All 10 levels playable
- Weapons upgrade correctly
- AI learns and improves
- Mobile controls work
- Performance hits 60fps
- Sound effects play

---

## Output

### Research specs go to:
`.deia/hive/queue/backlog/SPEC-RAIDEN-R01-*.md` etc.

### Design doc goes to:
`.deia/hive/responses/20260407-RAIDEN-DESIGN-DOC.md`

### Build specs go to:
`.deia/hive/queue/backlog/SPEC-RAIDEN-1XX-*.md`

### Your coordination response goes to:
`.deia/hive/responses/20260407-RAIDEN-COORDINATION-RESPONSE.md`

---

## Constraints
- You are in EXECUTE mode. Create all research and build specs. Do NOT ask for approval. Queue everything.
- Every spec you create must include: "You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it."
- Target file: `browser/public/games/raiden-v1-20260407.html` (single file, everything inline)
- All research specs use model: sonnet
- All build specs use model: sonnet
- No file over 500 lines — if the game exceeds this, the builder must use aggressive minification or split into modules loaded via inline script tags within the same HTML file
- No external dependencies. No npm. No CDN. Everything self-contained.
- The game must be FUN. This is entertainment, not a tech demo.

## Smoke Test
```bash
test -f ".deia/hive/responses/20260407-RAIDEN-COORDINATION-RESPONSE.md" && echo RESPONSE
ls .deia/hive/queue/backlog/SPEC-RAIDEN-*.md | wc -l
```

## Response Location
`.deia/hive/responses/20260407-RAIDEN-COORDINATION-RESPONSE.md`

## Triage History
- 2026-04-10T03:29:28.747626Z — requeued (empty output)
- 2026-04-12T18:52:40.095926Z — requeued (empty output)
- 2026-04-12T18:57:40.156447Z — requeued (empty output)
