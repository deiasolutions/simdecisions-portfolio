---
id: RAIDEN-110
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-101, RAIDEN-102, RAIDEN-103, RAIDEN-104, RAIDEN-105, RAIDEN-106, RAIDEN-107, RAIDEN-108, RAIDEN-109]
---
# SPEC-RAIDEN-110: Integration & E2E Testing

## Priority
P1

## Model Assignment
sonnet

## Role
bee (builder)

## Depends On
All prior specs (RAIDEN-101 through RAIDEN-109)

## Objective
Perform full integration testing, smoke tests, and E2E verification of the complete game. Fix any integration bugs, ensure all features work together, verify performance targets.

## Context
This is the final spec. The game should be complete. This spec verifies everything works, fixes integration issues, and adds a comprehensive E2E test suite.

## Technical Requirements

### Integration Checklist
Verify all systems integrate correctly:
- [ ] Game loop runs all systems (player, enemies, bullets, collisions, AI, audio, rendering)
- [ ] Player controls (keyboard, touch, tilt) all affect the same player entity
- [ ] Enemy spawning respects level progression
- [ ] Weapon upgrades change bullet behavior correctly
- [ ] Boss fights trigger after wave phase
- [ ] Score persists across game states
- [ ] High scores save and load from localStorage
- [ ] Audio plays for all events
- [ ] AI can control player without breaking game state
- [ ] Mobile and PC modes both work

### E2E Test Scenarios (Manual)
Write a test plan document covering:

1. **Happy Path:**
   - Start game → kill enemies → collect power-ups → upgrade weapon → defeat boss → advance to next level → repeat to level 10 → victory screen

2. **Death Flow:**
   - Start game → lose all lives → game over screen → retry

3. **High Score:**
   - Start game → get high score → enter initials → see score on menu

4. **AI Training:**
   - Toggle training mode → watch generations evolve → fitness increases → save best genome → reload page → genome persists

5. **Mobile:**
   - Open on mobile → touch joystick works → bomb button works → tilt mode works → haptic feedback works → add to home screen works

6. **Settings:**
   - Adjust volume → sounds quieter
   - Mute → no sounds
   - Change joystick sensitivity → movement changes
   - Change graphics quality → particle count changes

### Automated Tests (Inline)
Add debug mode tests (toggle with `?debug=1` in URL):
- Unit tests (already in prior specs)
- Integration tests:
  - Spawn enemy → shoot it → dies → score increases
  - Collect power-up → weapon tier increases → bullet pattern changes
  - Boss spawns at correct time → takes damage → phases change → dies → level advances
  - AI state → network forward pass → action outputs → player moves

### Performance Verification
- Run game for 5 minutes (all levels)
- Verify FPS stays above 50 (target 60)
- Verify memory usage stable (no leaks)
- Use Chrome DevTools Performance tab (record session, analyze)

### Bug Fixes
If integration bugs found:
- Document in response file
- Fix bugs
- Re-run tests

### Final Polish
- Ensure no console errors
- Ensure no visual glitches
- Ensure all text is readable (contrast, font size)
- Ensure game is fun (playtest!)

## Deliverable
1. **Test Plan Document:**
   `.deia/hive/responses/20260408-RAIDEN-110-TEST-PLAN.md`
   - E2E test scenarios
   - Expected results
   - Actual results (pass/fail)

2. **Updated Game File:**
   `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\games\raiden-v1-20260408.html`
   - All integration bugs fixed
   - Debug mode tests pass

3. **Performance Report:**
   `.deia/hive/responses/20260408-RAIDEN-110-PERFORMANCE.md`
   - FPS over 5 minute session
   - Memory usage graph
   - Bottlenecks identified (if any)

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- All tests must pass before marking complete
- If critical bugs found, fix them (within scope of this spec)
- If bugs are out of scope, document in response and flag for follow-up spec

## Acceptance Criteria
- [ ] Integration checklist 100% verified
- [ ] E2E test plan written and executed (all scenarios pass)
- [ ] Automated tests run in debug mode (all pass)
- [ ] Performance verified (60fps target met)
- [ ] No console errors
- [ ] Game is playable start-to-finish (Level 1 → Level 10 → Victory)
- [ ] Mobile and PC both tested
- [ ] AI training works and improves
- [ ] All prior spec acceptance criteria still pass (regression check)

## Smoke Test
```bash
# Manual: Full game playthrough
# 1. Open browser → menu screen
# 2. Press Space → game starts
# 3. Play through Level 1 → defeat boss
# 4. Advance to Level 2
# 5. Collect power-ups → weapon upgrades
# 6. Use bomb → clears bullets
# 7. Die → game over → see score
# 8. Press T → AI trains → fitness improves
# 9. Press A → AI plays game
# 10. Test on mobile (touch controls)
# 11. Check FPS (should be 60)
```

## Tests
Run all inline tests from prior specs:
- RAIDEN-101: Entity pooling, collision detection
- RAIDEN-102: Player controls, bullet firing
- RAIDEN-103: Enemy movement, spawning
- RAIDEN-104: Weapon tiers, power-ups
- RAIDEN-105: Boss phases, level progression
- RAIDEN-106: Game states, high scores
- RAIDEN-107: Audio synthesis
- RAIDEN-108: NEAT training, AI control
- RAIDEN-109: Mobile performance, tilt controls

All tests must pass.

## Response Location
`.deia/hive/responses/20260408-RAIDEN-110-RESPONSE.md`
