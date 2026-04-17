# RAIDEN-110 E2E Test Plan

**Date:** 2026-04-08
**Game Version:** raiden-v1-20260408.html
**Tester:** BEE-SONNET (RAIDEN-110)

---

## Test Scenarios

### 1. Happy Path - Full Game Playthrough

**Objective:** Verify complete game flow from start to victory

**Steps:**
1. Open game in browser (`browser/public/games/raiden-v1-20260408.html`)
2. Verify menu screen displays with game title and instructions
3. Press Space to start game
4. Verify game state transitions to PLAYING
5. Verify player ship appears at bottom center
6. Verify HUD shows: Lives (3), Score (0), Level (1), Weapon Tier (1)
7. Use arrow keys to move player ship
8. Verify ship movement is smooth and stays within bounds
9. Hold Space to fire bullets
10. Verify bullets fire continuously at correct rate
11. Kill enemies as they spawn
12. Verify enemies spawn in waves with different patterns
13. Verify score increases when enemies are killed
14. Verify combo multiplier activates (2x, 3x, 4x, 5x)
15. Collect power-up drops
16. Verify weapon upgrades (Tier 1 → 2 → 3 → 4 → 5)
17. Verify bullet patterns change with each weapon tier:
    - Tier 1: Single forward shot
    - Tier 2: Dual forward shots (spread)
    - Tier 3: Triple shots (wider spread)
    - Tier 4: Quad shots + diagonal
    - Tier 5: Penta shots + homing
18. Verify power-up types work correctly:
    - WEAPON: upgrades weapon tier
    - BOMB: adds bomb (max 9)
    - SHIELD: activates shield (temporary invincibility)
    - LIFE: adds extra life
19. Wait for wave duration (60 seconds)
20. Verify "BOSS INCOMING!" message appears
21. Verify boss spawns with unique design
22. Damage boss with player bullets
23. Verify boss health bar shows damage
24. Verify boss attack patterns change based on health phases:
    - Phase 1 (100%-75%): Basic pattern
    - Phase 2 (75%-50%): Intermediate pattern
    - Phase 3 (50%-25%): Advanced pattern
    - Phase 4 (<25%): Desperation pattern
25. Defeat boss (reduce health to 0)
26. Verify boss explosion and bonus score
27. Verify "LEVEL COMPLETE" message appears
28. Verify transition to Level 2
29. Repeat steps 7-28 for levels 2 through 10
30. Verify difficulty increases each level:
    - More enemies
    - Faster enemies
    - Tougher bosses
    - More aggressive patterns
31. After defeating Level 10 boss, verify victory screen displays
32. Verify final score is shown
33. Verify confetti animation plays
34. If high score achieved, verify initials entry prompt
35. Enter 3 initials (A-Z only)
36. Press Enter to save high score
37. Verify high score is saved to localStorage
38. Press Space to return to menu
39. Verify high scores are displayed on menu screen

**Expected Results:**
- ✓ All game systems work together seamlessly
- ✓ No errors in console
- ✓ Smooth gameplay at 60 FPS
- ✓ All transitions work correctly
- ✓ Victory screen displays after Level 10

**Actual Results:** [TO BE FILLED]

**Status:** [ ] PASS / [ ] FAIL

---

### 2. Death Flow - Player Loses All Lives

**Objective:** Verify game over flow when player dies

**Steps:**
1. Open game and press Space to start
2. Intentionally collide with enemy or enemy bullet
3. Verify player ship flashes (invincibility)
4. Verify life count decreases by 1
5. Verify life icon disappears from HUD
6. Repeat collision 2 more times
7. After 3rd death, verify game state transitions to GAME_OVER
8. Verify "GAME OVER" screen displays
9. Verify final score is shown
10. If high score achieved, verify initials entry
11. Enter initials and press Enter
12. Verify high score is saved
13. Press Space to restart
14. Verify game resets to Level 1 with 3 lives

**Expected Results:**
- ✓ Player invincibility after death (2 seconds)
- ✓ Lives decrease correctly
- ✓ Game over after 3 deaths
- ✓ High score saved if applicable
- ✓ Restart works correctly

**Actual Results:** [TO BE FILLED]

**Status:** [ ] PASS / [ ] FAIL

---

### 3. High Score System

**Objective:** Verify high score persistence and display

**Steps:**
1. Open game in browser
2. Verify menu screen shows "HIGH SCORES" list
3. Play game and achieve a score
4. Die or complete game
5. If score is high enough, verify initials prompt appears
6. Type 3 letters (e.g., "ABC")
7. Verify backspace works to delete letters
8. Press Enter when 3 letters entered
9. Verify high score is saved
10. Return to menu
11. Verify high score appears in list with initials
12. Close browser tab
13. Reopen game
14. Verify high score persists (loaded from localStorage)

**Expected Results:**
- ✓ High scores stored in localStorage
- ✓ High scores persist across sessions
- ✓ Top 5 scores displayed
- ✓ Initials entry works correctly

**Actual Results:** [TO BE FILLED]

**Status:** [ ] PASS / [ ] FAIL

---

### 4. AI Training Mode

**Objective:** Verify NEAT AI training system works

**Steps:**
1. Open game
2. Press 'T' to toggle training mode
3. Verify training indicator appears
4. Watch AI play the game
5. Verify multiple generations run automatically
6. Verify fitness score increases over generations
7. Verify console logs show:
   - Generation number
   - Best fitness
   - Species count
8. Wait for 10+ generations
9. Verify fitness improvement (trend upward)
10. Press 'S' to save best genome
11. Verify console message confirms save
12. Refresh page
13. Press 'T' to toggle training mode
14. Verify best genome is loaded from localStorage
15. Press 'A' to toggle autoplay mode
16. Verify AI controls the player using saved genome
17. Verify player moves, shoots, and dodges automatically
18. Press 'A' again to toggle off autoplay
19. Verify manual control returns

**Expected Results:**
- ✓ AI trains over multiple generations
- ✓ Fitness improves over time
- ✓ Best genome saves to localStorage
- ✓ Best genome loads on page refresh
- ✓ Autoplay mode works with saved genome
- ✓ AI can play the game autonomously

**Actual Results:** [TO BE FILLED]

**Status:** [ ] PASS / [ ] FAIL

---

### 5. Mobile Experience

**Objective:** Verify mobile controls and responsiveness

**Steps (Mobile Device or DevTools Mobile Emulation):**
1. Open game on mobile device or Chrome DevTools → Toggle device toolbar
2. Select mobile viewport (e.g., iPhone 12 Pro)
3. Verify game scales to fit screen
4. Tap screen to start game
5. Verify virtual joystick appears on touch
6. Drag joystick to move player
7. Verify player movement follows joystick input
8. Verify joystick deadzone (small movements ignored)
9. Tap bomb button (bottom right)
10. Verify bomb activates (clears bullets and damages enemies)
11. Verify bomb count decreases
12. Enable device orientation (if available)
13. Press 'M' to toggle tilt mode (or tap tilt toggle button)
14. Tilt device left/right
15. Verify player moves based on tilt angle
16. Tilt device forward/backward
17. Verify player moves up/down
18. Toggle tilt mode off
19. Verify joystick control returns
20. Test haptic feedback (if supported):
    - Fire bullets → short vibration
    - Enemy hit → medium vibration
    - Player hit → long vibration
21. Open game on slow device or throttle CPU in DevTools
22. Verify performance tier detection (low/medium/high)
23. Verify particle count and visual effects adjust to tier
24. Add game to home screen (mobile Safari or Chrome "Add to Home Screen")
25. Verify PWA icon appears
26. Launch from home screen
27. Verify game loads offline (service worker cache)

**Expected Results:**
- ✓ Game scales correctly to mobile viewport
- ✓ Touch joystick works smoothly
- ✓ Deadzone prevents jitter
- ✓ Bomb button works on tap
- ✓ Tilt controls work (if device supports orientation)
- ✓ Haptic feedback works (if device supports)
- ✓ Performance tier detection adjusts quality
- ✓ PWA installable and works offline

**Actual Results:** [TO BE FILLED]

**Status:** [ ] PASS / [ ] FAIL

---

### 6. Settings and Audio

**Objective:** Verify settings menu and audio controls

**Steps:**
1. Open game
2. Press 'M' to open settings menu (or look for settings UI)
3. Adjust master volume slider
4. Play game and verify sound volume changes
5. Toggle mute checkbox
6. Verify all sounds stop
7. Unmute and verify sounds return
8. Adjust joystick sensitivity (if mobile)
9. Test joystick movement
10. Verify sensitivity change affects movement
11. Adjust graphics quality setting
12. Verify particle count changes:
    - Low: fewer particles
    - Medium: moderate particles
    - High: maximum particles
13. Close settings menu
14. Verify settings persist in localStorage
15. Refresh page
16. Open settings menu
17. Verify all settings were saved

**Expected Results:**
- ✓ Volume control works
- ✓ Mute toggle works
- ✓ Joystick sensitivity adjustable
- ✓ Graphics quality adjustable
- ✓ Settings persist across sessions

**Actual Results:** [TO BE FILLED]

**Status:** [ ] PASS / [ ] FAIL

---

## Integration Checklist

### All Systems Integrated

- [ ] Game loop runs all systems:
  - [ ] Player input system
  - [ ] Bullet system
  - [ ] Enemy spawning system
  - [ ] Collision system
  - [ ] Score system
  - [ ] Audio system
  - [ ] Particle system
  - [ ] Boss system
  - [ ] Level progression system
  - [ ] AI system (training and autoplay)
  - [ ] Visual effects system

- [ ] Player controls (keyboard, touch, tilt) all affect the same player entity
- [ ] Enemy spawning respects level progression
- [ ] Weapon upgrades change bullet behavior correctly
- [ ] Boss fights trigger after wave phase
- [ ] Score persists across game states
- [ ] High scores save and load from localStorage
- [ ] Audio plays for all events:
  - [ ] Player shoot
  - [ ] Enemy hit
  - [ ] Player hit
  - [ ] Power-up collect
  - [ ] Bomb activate
  - [ ] Boss warning
  - [ ] Boss defeat
  - [ ] Game over
- [ ] AI can control player without breaking game state
- [ ] Mobile and PC modes both work
- [ ] Game states transition correctly:
  - [ ] MENU → PLAYING
  - [ ] PLAYING → PAUSED → PLAYING
  - [ ] PLAYING → GAME_OVER → MENU
  - [ ] PLAYING → VICTORY → MENU
- [ ] Level transitions work (1 → 2 → ... → 10)
- [ ] Boss phases change based on health
- [ ] Power-ups spawn and apply effects correctly
- [ ] Bombs clear bullets and damage enemies
- [ ] Shield protects player temporarily
- [ ] Lives system works (3 lives, lose life on hit, game over on 0)
- [ ] Combo system works (increases with consecutive kills)
- [ ] Difficulty scaling works (harder enemies each level)

---

## Automated Test Scenarios (Debug Mode)

These tests run automatically when `DEBUG_MODE = true` in the game file.

### Unit Tests (Existing)

1. **Entity pooling** (RAIDEN-101)
   - Pool creates entities
   - Pool reuses deactivated entities
   - Pool tracks active count

2. **Vector math** (RAIDEN-101)
   - Normalize vector
   - Calculate distance
   - Vector operations

3. **Collision detection** (RAIDEN-101)
   - AABB collision
   - Spatial grid optimization

4. **Player controls** (RAIDEN-102)
   - Movement input
   - Shooting input
   - Bounds checking

5. **Enemy AI** (RAIDEN-103)
   - Movement patterns
   - Shooting behavior
   - Targeting

6. **Weapon system** (RAIDEN-104)
   - Weapon tier upgrades
   - Bullet patterns
   - Power-up collection

7. **Boss system** (RAIDEN-105)
   - Boss spawning
   - Phase transitions
   - Health tracking

8. **Game states** (RAIDEN-106)
   - State transitions
   - High score entry
   - Menu/Pause/Game Over

9. **Audio synthesis** (RAIDEN-107)
   - Sound generation
   - Volume control
   - Mute toggle

10. **NEAT AI** (RAIDEN-108)
    - Neural network forward pass
    - Genome mutation
    - Species tracking
    - Training progression

11. **Mobile controls** (RAIDEN-109)
    - Joystick deadzone
    - Tilt angle mapping
    - Performance tier detection

### Integration Tests (New - To Add)

1. **Spawn enemy → shoot it → dies → score increases**
   ```javascript
   const enemy = enemySystem.spawn(ENEMY_TYPES.GRUNT, 100, 100);
   const bullet = bulletSystem.firePlayerBullet(100, 120);
   // Wait for collision
   collisionSystem.update();
   assert(enemy.health <= 0, 'Enemy should be dead');
   assert(scoreSystem.score > 0, 'Score should increase');
   ```

2. **Collect power-up → weapon tier increases → bullet pattern changes**
   ```javascript
   const initialTier = bulletSystem.weaponTier;
   const powerup = powerUpSystem.spawn(POWERUP_TYPES.WEAPON, 100, 100);
   player.x = 100; player.y = 100;
   collisionSystem.update();
   assert(bulletSystem.weaponTier === initialTier + 1, 'Weapon tier should increase');
   const bulletCount = bulletSystem.firePlayerBullet(100, 100).length;
   assert(bulletCount > 1, 'Higher tier should fire more bullets');
   ```

3. **Boss spawns at correct time → takes damage → phases change → dies → level advances**
   ```javascript
   levelTimer = LEVEL_CONFIG.WAVE_DURATION;
   update(0.1);
   assert(boss !== null, 'Boss should spawn after wave duration');
   assert(boss.data.currentPhase.healthPercent === 100, 'Boss should start in phase 1');
   boss.takeDamage(boss.maxHealth * 0.3);
   update(0.1);
   assert(boss.data.currentPhase.healthPercent < 100, 'Boss should transition phase');
   boss.takeDamage(boss.health);
   update(0.1);
   assert(currentLevel === 2, 'Level should advance after boss defeat');
   ```

4. **AI state → network forward pass → action outputs → player moves**
   ```javascript
   const ai = new AIPlayer(player, entityPools);
   const initialX = player.x;
   const initialY = player.y;
   ai.think(0.1);
   assert(player.x !== initialX || player.y !== initialY, 'AI should move player');
   ```

---

## Performance Verification

### Target Metrics

- **FPS:** 60 (minimum 50)
- **Memory:** Stable (no leaks)
- **Frame time:** <16.67ms (60 FPS)
- **Entity count:** Up to 250 active entities
- **Particle count:** Up to 150 particles

### Test Procedure

1. Open game in Chrome
2. Open DevTools → Performance tab
3. Click Record
4. Play game for 5 minutes (all levels or until death)
5. Stop recording
6. Analyze:
   - FPS graph (should stay above 50 FPS)
   - Memory graph (should be stable, no upward trend)
   - Frame timings (should stay below 16.67ms)
   - Scripting time (should be minimal)
   - Rendering time (should be consistent)
7. Open DevTools → Memory tab
8. Take heap snapshot before game start
9. Play game for 5 minutes
10. Take heap snapshot after game
11. Compare snapshots:
    - Look for detached DOM nodes (should be none)
    - Look for increased object counts (entity pools should be stable)
    - Look for memory leaks (listeners, intervals, timeouts)

### Performance Report Template

```
## Performance Test Results

**Date:** 2026-04-08
**Browser:** Chrome [version]
**Device:** [CPU, GPU, RAM]

### FPS Over 5 Minutes
- Average: X FPS
- Minimum: Y FPS
- Maximum: Z FPS
- Dropped frames: N

### Memory Usage
- Start: X MB
- End: Y MB
- Delta: Z MB
- Trend: [stable / increasing / decreasing]

### Frame Timing
- Average frame time: X ms
- P95 frame time: Y ms
- P99 frame time: Z ms

### Bottlenecks Identified
1. [None] or [List bottlenecks]

### Recommendations
1. [None] or [List optimizations]
```

---

## Regression Check

Verify all prior spec acceptance criteria still pass:

### RAIDEN-101 (Game Engine)
- [ ] Entity pooling works
- [ ] Spatial grid collision detection works
- [ ] 60 FPS maintained

### RAIDEN-102 (Player Controls)
- [ ] Keyboard controls work
- [ ] Player stays within bounds
- [ ] Shooting works
- [ ] Lives system works

### RAIDEN-103 (Enemy System)
- [ ] 5 enemy types spawn
- [ ] Movement patterns work
- [ ] Enemies shoot at player
- [ ] Enemies die when hit

### RAIDEN-104 (Weapon System)
- [ ] 5 weapon tiers work
- [ ] Power-ups spawn
- [ ] Weapon upgrades change bullet pattern
- [ ] Max weapon tier is 5

### RAIDEN-105 (Boss System)
- [ ] Boss spawns after wave
- [ ] Boss has health bar
- [ ] Boss phases change based on health
- [ ] Boss defeat triggers level advance

### RAIDEN-106 (UI & Scoring)
- [ ] HUD shows lives, score, level
- [ ] Menu screen works
- [ ] Pause screen works
- [ ] Game over screen works
- [ ] Victory screen works
- [ ] High score entry works

### RAIDEN-107 (Audio)
- [ ] All sounds synthesized (no external files)
- [ ] Volume control works
- [ ] Mute works

### RAIDEN-108 (AI System)
- [ ] NEAT training works
- [ ] AI improves over generations
- [ ] Autoplay mode works
- [ ] Genome save/load works

### RAIDEN-109 (Mobile Polish)
- [ ] Touch joystick works
- [ ] Bomb button works
- [ ] Tilt controls work (if supported)
- [ ] Performance tier detection works
- [ ] PWA installable

---

## Test Execution Log

### Manual Tests

| Test ID | Test Name | Date | Status | Notes |
|---------|-----------|------|--------|-------|
| 1 | Happy Path | [DATE] | [ ] PASS / [ ] FAIL | [notes] |
| 2 | Death Flow | [DATE] | [ ] PASS / [ ] FAIL | [notes] |
| 3 | High Score | [DATE] | [ ] PASS / [ ] FAIL | [notes] |
| 4 | AI Training | [DATE] | [ ] PASS / [ ] FAIL | [notes] |
| 5 | Mobile Experience | [DATE] | [ ] PASS / [ ] FAIL | [notes] |
| 6 | Settings & Audio | [DATE] | [ ] PASS / [ ] FAIL | [notes] |

### Automated Tests

| Test Suite | Date | Status | Failed Tests |
|------------|------|--------|--------------|
| Unit Tests (All Specs) | [DATE] | [ ] PASS / [ ] FAIL | [list] |
| Integration Tests (New) | [DATE] | [ ] PASS / [ ] FAIL | [list] |

### Performance Tests

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| FPS (average) | 60 | [X] | [ ] PASS / [ ] FAIL |
| FPS (minimum) | 50 | [X] | [ ] PASS / [ ] FAIL |
| Memory (stable) | Yes | [Yes/No] | [ ] PASS / [ ] FAIL |
| Frame time (P95) | <16.67ms | [X]ms | [ ] PASS / [ ] FAIL |

---

## Summary

**Total Tests:** 6 manual + 15 automated = 21 tests
**Tests Passed:** [X]
**Tests Failed:** [Y]
**Overall Status:** [ ] ALL PASS / [ ] SOME FAILED

**Critical Issues Found:** [None] or [List]
**Non-Critical Issues Found:** [None] or [List]
**Performance Issues:** [None] or [List]

**Game Ready for Release:** [ ] YES / [ ] NO (pending fixes)

---

## Next Steps

1. Execute all manual tests → fill in actual results
2. Run automated tests → verify all pass
3. Run performance tests → verify 60 FPS target
4. Fix any integration bugs found
5. Verify fixes with regression tests
6. Update game file with any fixes
7. Write final performance report
8. Write final response file
