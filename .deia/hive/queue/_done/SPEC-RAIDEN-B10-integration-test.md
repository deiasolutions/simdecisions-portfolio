---
id: RAIDEN-B10
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-B09]
---
# SPEC-RAIDEN-B10: Integration, E2E Testing, and Final Polish

## Priority
P1

## Model Assignment
sonnet

## Role
bee (b33 — you write code and tests)

## Depends On
- RAIDEN-B09 (mobile polish)

## Objective
Final integration: Ensure all systems work together, run comprehensive E2E tests, fix bugs, and deploy.

## You are in EXECUTE mode
Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.

## Design Reference
Read: `.deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md` (entire document for verification)

## Deliverables

### File: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\public\games\raiden-v1-20260413.html`

**Final integration and testing:**

1. **End-to-End Test Plan**
   Run through complete game flow and verify all features:

   **Test 1: Full Playthrough (Manual)**
   - Start game from menu
   - Play through levels 1-10
   - Collect power-ups, upgrade weapons
   - Use bombs
   - Fight all bosses
   - Complete game
   - Check high score persists

   **Test 2: AI Mode**
   - Activate AI mode (A key)
   - Watch AI train for 20 generations
   - AI should reach level 2+ by generation 20
   - Check genome persistence (refresh page, training continues)

   **Test 3: Hybrid Mode**
   - Activate hybrid mode (H key)
   - AI controls movement, player controls shooting
   - See ghost overlay showing AI intent
   - Defeat enemies and progress

   **Test 4: Mobile Experience**
   - Test on actual mobile device (iOS and Android)
   - Virtual joystick works smoothly
   - Bomb button works
   - Fullscreen mode works
   - Haptic feedback works (vibration)
   - Performance: 30fps minimum

   **Test 5: Audio**
   - All 6 sound effects play correctly
   - Mute/unmute works (M key)
   - Sound preference persists
   - Audio works on mobile (after user interaction)

   **Test 6: Scoring and UI**
   - Score increases correctly
   - Combo multiplier builds and resets
   - HUD displays all info (score, level, lives, weapon, bombs)
   - Menu, pause, game over screens work
   - High score persists across sessions

   **Test 7: Edge Cases**
   - Die on boss fight, respawn correctly
   - Pause during boss fight, resume correctly
   - Switch to AI mode mid-game, AI takes over
   - Resize window during game, layout adapts
   - Lose all lives, game over screen appears

2. **Bug Fixes**
   Common issues to check and fix:
   - Collision detection false positives/negatives
   - Entity cleanup (memory leaks from pooling)
   - Boss not spawning (timing issue)
   - AI getting stuck in corners
   - Touch controls not responding (event propagation)
   - Sound crackling (too many concurrent sounds)
   - HUD overlapping game elements
   - Performance drops (too many particles)

3. **Code Cleanup**
   - Remove TEST_MODE flags and debug code
   - Remove console.log statements (or wrap in DEBUG flag)
   - Ensure file is under 500 lines (if over, aggressively minify or modularize)
   - Add code comments for complex sections (AI, collision detection)
   - Consistent code style (indentation, naming)

4. **Final Polish**
   - Tweak difficulty: Is game too hard? Too easy? Adjust enemy HP/spawn rates
   - Tweak visuals: Colors, glow effects, particle counts
   - Tweak audio: Volume levels, sound frequencies
   - Tweak AI: Fitness function weights, mutation rates

5. **Performance Verification**
   - Desktop: 60fps with 50 enemies + 100 bullets + 200 particles
   - Mobile: 30fps with 20 enemies + 50 bullets + 100 particles
   - AI training: 30fps minimum during genome evaluation

6. **Accessibility**
   - Keyboard controls clearly documented (in menu or help screen)
   - Touch controls visible and large enough (44px minimum)
   - High contrast for HUD (readable on light/dark backgrounds)
   - Colorblind mode (optional): Use shapes/icons, not just colors

7. **Documentation (In-Game)**
   - Help screen (H key or button in menu):
     - Controls (keyboard + touch)
     - Weapon tiers explanation
     - Boss patterns tips
     - AI mode explanation
   - Credits screen:
     - "Made with Claude Code"
     - Link to GitHub repo (optional)

## Acceptance Criteria
- [ ] Full playthrough (levels 1-10) completes without errors
- [ ] AI mode trains and improves over 20 generations
- [ ] Hybrid mode works (AI movement + player shooting)
- [ ] Mobile experience smooth (30fps, touch controls work)
- [ ] All 6 sound effects play correctly
- [ ] Scoring, combos, high score persistence work
- [ ] All game states (menu, play, pause, game over) work
- [ ] No console errors during full playthrough
- [ ] Performance targets met (60fps desktop, 30fps mobile)
- [ ] Code cleaned up (no debug logs, no test mode)
- [ ] Help screen documents controls and features
- [ ] File size reasonable (<500 lines preferred, max 1000)

## Tests (Manual E2E)
**Run all 7 test scenarios above.**

**Automated smoke test (run in browser console):**
```javascript
// Smoke test script (paste into console)
console.log("Running smoke tests...");

// Test 1: Canvas exists
if (!document.querySelector('canvas')) {
  console.error("FAIL: Canvas not found");
} else {
  console.log("PASS: Canvas exists");
}

// Test 2: Audio context initialized
if (typeof AudioContext !== 'undefined') {
  console.log("PASS: AudioContext available");
} else {
  console.error("FAIL: AudioContext not available");
}

// Test 3: High score in localStorage
if (localStorage.getItem('raidenHighScore') !== null) {
  console.log("PASS: High score persistence");
} else {
  console.warn("WARN: No high score saved yet");
}

// Test 4: FPS counter (press F to activate, check >30fps)
console.log("MANUAL: Press F to check FPS (should be 30+)");

console.log("Smoke tests complete.");
```

## Smoke Test
```bash
test -f "browser/public/games/raiden-v1-20260413.html" && \
wc -l "browser/public/games/raiden-v1-20260413.html" | awk '{if($1>1000) print "WARN: File over 1000 lines"; else print "PASS: File size OK"}' && \
grep -q "RAIDEN" "browser/public/games/raiden-v1-20260413.html" && \
echo "INTEGRATION COMPLETE"
```

## Response Location
`.deia/hive/responses/20260413-RAIDEN-B10-INTEGRATION-TEST-RESPONSE.md`

## Deployment
After tests pass:
1. File already in `browser/public/games/` (accessible at `/games/raiden-v1-20260413.html`)
2. Add link to game in `browser/public/index.html` or games index page
3. Test in production: Open `http://localhost:5173/games/raiden-v1-20260413.html`

## Notes
- This is the final spec. Game should be 100% playable after this.
- Prioritize fun over perfection (a fun game with minor bugs > a perfect but boring game).
- If file exceeds 1000 lines, aggressively minify (remove whitespace, shorten variable names).
- Once complete, the game is ready for public play and AI learning demos.
