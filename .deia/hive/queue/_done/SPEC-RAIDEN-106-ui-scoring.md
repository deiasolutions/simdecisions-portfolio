---
id: RAIDEN-106
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-103, RAIDEN-104]
---
# SPEC-RAIDEN-106: UI, Scoring & Game States

## Priority
P1

## Model Assignment
sonnet

## Role
bee (builder)

## Depends On
- RAIDEN-103 (enemy system with basic scoring)
- RAIDEN-104 (weapon system)

## Objective
Polish the UI with HUD elements, implement game states (menu, playing, paused, game over, victory), high score system with localStorage persistence.

## Context
Building on existing scoring from RAIDEN-103. Add full game state management and persistent high scores.

## Technical Requirements

### Game States
- **MENU:** Title screen, "Press Space to Start", high score display
- **PLAYING:** Active gameplay
- **PAUSED:** Pause overlay (press P to pause/unpause)
- **GAME_OVER:** Death screen, final score, "Press Space to Retry"
- **VICTORY:** Victory screen (after Level 10 boss), final score, confetti animation

### HUD (during PLAYING state)
Top left:
- Lives counter (heart icons or "Lives: X")
- Bomb counter ("Bombs: X")
- Weapon tier indicator ("Weapon: Tier X" with icon)

Top center:
- Level counter ("Level X")

Top right:
- Score ("Score: XXXXX")
- Combo multiplier ("Combo: Xx" — only when active)

Bottom:
- Boss health bar (when boss active)
- Shield timer (when shield active)

### High Score System
- Track top 5 high scores in localStorage
- High score entry: initials (3 letters) + score
- Display high scores on menu screen
- New high score prompts for initials (simple text input)

### Pause System
- Press P to pause/unpause
- Pause overlay: semi-transparent black, "PAUSED" text, "Press P to Resume"
- Game loop stops (entities freeze)

### Game Over
- Trigger when lives reach 0
- Fade to game over screen
- Show final score
- If new high score: prompt for initials
- "Press Space to Retry" restarts from Level 1

### Victory Screen
- Trigger when Level 10 boss defeated
- Confetti particle animation
- Show final score + total time
- If new high score: prompt for initials
- "Press Space to Play Again"

### Visual Polish
- Screen shake on player hit (2 frames, 5px offset)
- Particle effects: explosions (enemy death), power-up collection sparkle
- Text animations: score popup on enemy kill, combo multiplier pulse

## Deliverable
Update file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\games\raiden-v1-20260408.html`

Add sections:
- `// ===== GAME STATES =====`
- `// ===== HUD =====`
- `// ===== HIGH SCORES =====`
- `// ===== VISUAL EFFECTS =====`

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- HUD does not obscure gameplay
- High scores persist across sessions (localStorage)
- Victory screen feels celebratory (confetti, positive feedback)

## Acceptance Criteria
- [ ] 5 game states implemented (MENU, PLAYING, PAUSED, GAME_OVER, VICTORY)
- [ ] Menu screen displays title and high scores
- [ ] HUD shows lives, bombs, weapon, level, score, combo
- [ ] Pause works (P key, game freezes, overlay shown)
- [ ] Game over triggers on death, shows final score
- [ ] Victory screen triggers after Level 10 boss
- [ ] High scores saved to localStorage (top 5)
- [ ] New high score prompts for initials
- [ ] Screen shake on player hit
- [ ] Particle effects for explosions and power-up collection
- [ ] Smoke test: play game, die, see game over, retry, see menu

## Smoke Test
```bash
# Manual: Open file in browser
# - Menu screen shows with high scores
# - Press Space → game starts
# - HUD visible (lives, score, level, weapon)
# - Press P → game pauses
# - Die (lose all lives) → game over screen
# - Defeat Level 10 boss → victory screen
# - High score saves, appears on menu after retry
```

## Tests
Write inline tests:
- Game state transitions (MENU → PLAYING → GAME_OVER)
- High score sorting (top 5 descending)
- localStorage persistence (save/load high scores)
- Pause state (entities stop moving)

## Response Location
`.deia/hive/responses/20260408-RAIDEN-106-RESPONSE.md`
