---
id: RAIDEN-B06
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-B05]
---
# SPEC-RAIDEN-B06: Scoring System and UI Polish

## Priority
P1

## Model Assignment
sonnet

## Role
bee (b33 — you write code and tests)

## Depends On
- RAIDEN-B05 (level progression)

## Objective
Implement scoring system with combos, HUD polish, menus, and game over screen.

## You are in EXECUTE mode
Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.

## Design Reference
Read: `.deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md`
Specifically: Section 7 (Scoring System), Section 12 (HUD Layout), Section 13 (Game States)

## Deliverables

### File: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\public\games\raiden-v1-20260413.html`

**Add to existing engine:**

1. **Scoring System**
   - **Base Scores (from design doc):**
     - Scout: 100
     - Heavy: 500
     - Weaver: 300
     - Kamikaze: 200
     - Formation: 150
     - Boss: 10,000
   - **Combo Multiplier:**
     - Kill enemy within 2 seconds of last kill: +0.1x multiplier
     - Max multiplier: 5x
     - Combo resets after 2 seconds of no kills
     - Display: "x2.5 COMBO!" next to score
   - **Bonus Scoring:**
     - No-death bonus (per level): +5,000
     - Perfect level (no hits taken): +10,000
     - Level completion: +1,000 * level

2. **HUD Layout (from design doc Section 12)**
   - **Top Bar:**
     - Top-left: Score (large font, e.g., "Score: 12,450")
     - Top-center: Level (e.g., "Level 3")
     - Top-right: Lives (ship icons, e.g., "♥ ♥ ♥" or ship sprites)
   - **Bottom Bar (PC):**
     - Bottom-left: Weapon tier (e.g., "Weapon: T3")
     - Bottom-right: Bomb count (e.g., "Bombs: 2")
   - **Bottom (Mobile):**
     - Virtual joystick and bomb button (already implemented in B02)
     - Weapon/bomb info overlaid on top bar

3. **Menu Screen (Game State: MENU)**
   - Title: "RAIDEN-STYLE SHMUP"
   - Buttons:
     - "PLAY" — Start game
     - "AI MODE" — Watch AI play (placeholder, implement in B08)
     - "SETTINGS" — Toggle auto-fire, sound (optional)
   - High score display: "High Score: 45,670" (from localStorage)
   - Visual: Stars background (animated particles), pulsing title

4. **Pause Screen (Game State: PAUSED)**
   - Semi-transparent overlay
   - Text: "PAUSED"
   - Buttons: "Resume", "Restart", "Quit to Menu"
   - Press P again to resume

5. **Game Over Screen (Game State: GAME_OVER)**
   - Text: "GAME OVER"
   - Final score display: "Final Score: 23,890"
   - High score: "High Score: 45,670" (update if new high score)
   - Stats:
     - Total time played
     - Enemies killed
     - Accuracy (shots hit / shots fired)
     - Max combo
   - Buttons: "Retry", "Menu"

6. **High Score Persistence**
   - Save to localStorage: `localStorage.setItem('raidenHighScore', score)`
   - Load on game start: `localStorage.getItem('raidenHighScore') || 0`
   - Display on menu and game over screens

7. **Floating Score Text**
   - When enemy killed: Display "+100" or "+500 x2.5" above enemy position
   - Fade out and float upward over 1 second
   - Color: Yellow for normal score, gold for combo score

## Technical Constraints
- HUD renders on top of game canvas (use separate canvas layer or overlay div)
- Menu/pause/game over screens: Draw directly on canvas with semi-transparent background
- Combo timer: Track last kill timestamp, check `Date.now() - lastKill < 2000`
- High score: JSON.parse/stringify if storing complex data (e.g., {score, date, level})

## Acceptance Criteria
- [ ] Score increases when enemies killed (base score * combo multiplier)
- [ ] Combo multiplier builds with rapid kills (max 5x)
- [ ] Combo display shows current multiplier
- [ ] HUD displays score, level, lives, weapon, bombs
- [ ] Menu screen with "PLAY", "AI MODE", "SETTINGS"
- [ ] Pause screen with "Resume", "Restart", "Quit"
- [ ] Game over screen with final score, stats, high score
- [ ] High score persists across sessions (localStorage)
- [ ] Floating score text appears when enemy killed
- [ ] No errors in console
- [ ] Clean, readable UI (good contrast, legible fonts)

## Tests (Manual Smoke Tests)
```javascript
// Test: Scoring
// 1. Kill enemies, see score increase (100, 500, etc.)
// 2. Kill enemies rapidly, see combo multiplier increase (x1.5, x2.0, ...)
// 3. Wait 2 seconds, combo resets to x1.0

// Test: HUD
// 1. Check top bar: Score, Level, Lives all visible
// 2. Check bottom bar: Weapon tier, Bomb count visible
// 3. Resize to mobile, check HUD still readable

// Test: Menu
// 1. Load game, see menu screen with title and buttons
// 2. Click "PLAY", game starts
// 3. Click "AI MODE" (placeholder, no effect yet)

// Test: Pause
// 1. Press P during game, see pause overlay
// 2. Click "Resume", game continues
// 3. Click "Restart", game restarts from level 1

// Test: Game Over
// 1. Die (lose all lives), see game over screen
// 2. Check final score, stats (time, enemies killed, accuracy)
// 3. If new high score, see "NEW HIGH SCORE!" message
// 4. Click "Retry", restart game

// Test: High Score Persistence
// 1. Get high score (e.g., 10,000)
// 2. Refresh page
// 3. See high score still displayed on menu (loaded from localStorage)
```

## Smoke Test
```bash
grep -q "score" "browser/public/games/raiden-v1-20260413.html" && \
grep -q "combo" "browser/public/games/raiden-v1-20260413.html" && \
grep -q "localStorage" "browser/public/games/raiden-v1-20260413.html" && \
echo "PASS"
```

## Response Location
`.deia/hive/responses/20260413-RAIDEN-B06-SCORING-UI-RESPONSE.md`

## Notes
- Game now has full UI and scoring system.
- Next spec (B07) adds sound effects.
- Make sure HUD is readable on both PC and mobile.
- Combo system adds skill ceiling (rewards aggressive play).
