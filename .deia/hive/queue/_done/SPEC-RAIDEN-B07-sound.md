---
id: RAIDEN-B07
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-B06]
---
# SPEC-RAIDEN-B07: Sound Effects

## Priority
P1

## Model Assignment
sonnet

## Role
bee (b33 — you write code and tests)

## Depends On
- RAIDEN-B06 (scoring and UI)

## Objective
Implement synthesized sound effects using Web Audio API.

## You are in EXECUTE mode
Write all code and tests. Do NOT enter plan mode. DO NOT ask for approval. Just build it.

## Design Reference
Read: `.deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md`
Specifically: Section 11 (Sound Design)

## Deliverables

### File: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\public\games\raiden-v1-20260413.html`

**Add to existing engine:**

1. **Web Audio API Setup**
   - Create AudioContext on first user interaction (click/touch, required by browsers)
   - Initialize on "PLAY" button click or first keypress
   - Handle browser autoplay policy

2. **Sound Effects (from design doc Section 11)**

   **Player Shoot:**
   - Frequency: 200Hz
   - Type: Square wave
   - Duration: 50ms
   - Volume: 0.1

   **Enemy Explosion:**
   - Type: White noise
   - Duration: 150ms
   - Filter: Band-pass 100-800Hz
   - Volume: 0.2

   **Power-Up Collect:**
   - Frequency: 440Hz → 880Hz (ascending)
   - Type: Sine wave
   - Duration: 100ms
   - Volume: 0.15

   **Boss Warning:**
   - Frequency: 80Hz
   - Type: Sawtooth wave
   - Duration: 500ms (looped)
   - Volume: 0.3

   **Level Complete:**
   - Notes: C-E-G-C (major chord arpeggio: 261Hz, 329Hz, 392Hz, 523Hz)
   - Type: Sine wave
   - Duration: 100ms per note (400ms total)
   - Volume: 0.2

   **Bomb:**
   - Sweep: 2000Hz → 100Hz (downward)
   - Type: Sawtooth wave
   - Duration: 300ms
   - Volume: 0.4

3. **Sound Trigger Integration**
   - Player shoots: Play shoot sound
   - Enemy destroyed: Play explosion sound
   - Power-up collected: Play power-up sound
   - Boss spawns: Play boss warning sound (loop until boss defeated)
   - Level complete: Play victory jingle
   - Bomb activated: Play bomb sound

4. **Sound Settings**
   - Mute/unmute toggle (M key)
   - Volume slider in settings menu (0-100%)
   - Save sound preference to localStorage

5. **Performance Optimization**
   - Reuse oscillators and buffers (don't create new AudioContext nodes every sound)
   - Limit concurrent sounds (max 10 at once, skip oldest)
   - Clean up disconnected nodes

## Technical Constraints
- No external audio files (all synthesized with Web Audio API)
- Use OscillatorNode for tones, AudioBufferSourceNode for noise
- Handle mobile browsers (iOS requires user interaction before audio)
- Keep volume low (don't blast user's ears)

## Acceptance Criteria
- [ ] 6 sound effects implemented (shoot, explosion, power-up, boss warning, level complete, bomb)
- [ ] Sounds play at appropriate game events
- [ ] M key toggles mute/unmute
- [ ] Sound preference persists (localStorage)
- [ ] Boss warning loops while boss is active
- [ ] No errors in console
- [ ] Sounds work on both PC and mobile

## Tests (Manual Smoke Tests)
```javascript
// Test: Player shoot
// 1. Fire weapon, hear 200Hz beep (50ms)

// Test: Enemy explosion
// 1. Destroy enemy, hear noise burst (150ms)

// Test: Power-up
// 1. Collect power-up, hear ascending tone (440→880Hz)

// Test: Boss warning
// 1. Boss spawns, hear low rumble (80Hz loop)
// 2. Defeat boss, rumble stops

// Test: Level complete
// 1. Complete level, hear victory jingle (C-E-G-C arpeggio)

// Test: Bomb
// 1. Activate bomb, hear whoosh/explosion (2000→100Hz sweep)

// Test: Mute
// 1. Press M key, all sounds muted
// 2. Press M again, sounds resume
// 3. Refresh page, mute setting persists

// Test: Mobile
// 1. Open game on mobile, tap screen to initialize audio
// 2. All sounds work on mobile
```

## Smoke Test
```bash
grep -q "AudioContext" "browser/public/games/raiden-v1-20260413.html" && \
grep -q "oscillator" "browser/public/games/raiden-v1-20260413.html" && \
grep -q "playSound" "browser/public/games/raiden-v1-20260413.html" && \
echo "PASS"
```

## Response Location
`.deia/hive/responses/20260413-RAIDEN-B07-SOUND-RESPONSE.md`

## Notes
- Sound adds immersion and feedback.
- Keep volumes balanced (not too loud, not too quiet).
- Next spec (B08) implements the AI system (biggest feature).
- Test on both PC and mobile (iOS audio requires user interaction).
