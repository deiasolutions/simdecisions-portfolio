---
id: RAIDEN-107
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-102, RAIDEN-103, RAIDEN-104]
---
# SPEC-RAIDEN-107: Sound Effects (Web Audio API)

## Priority
P1

## Model Assignment
sonnet

## Role
bee (builder)

## Depends On
- RAIDEN-102 (player ship)
- RAIDEN-103 (enemy system)
- RAIDEN-104 (weapon system)

## Objective
Implement synthesized sound effects using Web Audio API. No external audio files — all sounds procedurally generated. Covers player shoot, enemy explosion, power-up collection, bomb, boss warning, etc.

## Context
Classic arcade games had synthesized beeps and boops. We're recreating that aesthetic with modern Web Audio API.

## Technical Requirements

### Sound System Architecture
- Create AudioContext on first user interaction (browser autoplay policy)
- Sound manager class: `playSound(type, params)`
- Volume control (master volume slider on menu)
- Mute toggle (M key)

### Sound Effects (minimum 8)

1. **Player Shoot:** Short high-pitch beep (440Hz, 50ms)
2. **Enemy Explosion:** Descending noise burst (white noise, pitch drops 1000Hz → 100Hz, 200ms)
3. **Player Hit:** Low harsh buzz (100Hz, 300ms, distorted)
4. **Power-Up Collect:** Rising arpeggio (C-E-G, 100ms each note)
5. **Bomb:** Deep rumble (50Hz, 500ms, tremolo effect)
6. **Boss Warning:** Siren (oscillating 200Hz ↔ 400Hz, 1 second)
7. **Boss Defeat:** Victory jingle (C-E-G-C, 150ms each, ascending)
8. **Game Over:** Descending sad trombone (G-F-E-D, 200ms each)

### Sound Synthesis Techniques
- **Oscillators:** sine, square, sawtooth, triangle waves
- **Envelopes:** ADSR (attack, decay, sustain, release)
- **Filters:** low-pass, high-pass for tone shaping
- **Effects:** tremolo (amplitude modulation), vibrato (frequency modulation)
- **Noise:** white noise for explosions

### Performance Considerations
- Reuse AudioContext (create once, persist)
- Limit concurrent sounds (max 10 simultaneous)
- Stop sounds when game paused

### User Controls
- Master volume slider (0-100%, default 70%)
- Mute toggle (M key, persists to localStorage)
- Volume/mute settings on menu screen

## Deliverable
Update file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\games\raiden-v1-20260408.html`

Add sections:
- `// ===== AUDIO SYSTEM =====`
- `// ===== SOUND EFFECTS =====`

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- No external audio files (everything synthesized)
- Sounds are recognizable and satisfying (test in browser)
- Volume control works and persists

## Acceptance Criteria
- [ ] AudioContext created on first user interaction
- [ ] 8 sound effects implemented (shoot, explosion, hit, power-up, bomb, boss warning, boss defeat, game over)
- [ ] Each sound uses synthesized audio (oscillators, noise, filters)
- [ ] Master volume slider on menu (0-100%)
- [ ] Mute toggle (M key)
- [ ] Volume/mute settings persist to localStorage
- [ ] Sounds stop when game paused
- [ ] Smoke test: play game, hear sounds for all actions

## Smoke Test
```bash
# Manual: Open file in browser
# - Shoot (spacebar) → hear beep
# - Kill enemy → hear explosion
# - Collect power-up → hear arpeggio
# - Use bomb → hear rumble
# - Get hit → hear buzz
# - Boss appears → hear siren
# - Defeat boss → hear victory jingle
# - Die → hear sad trombone
# - Press M → mute (no sounds)
# - Press M again → unmute
# - Adjust volume slider → sounds quieter/louder
```

## Tests
Write inline tests:
- AudioContext creation (not null after user interaction)
- Sound duration (player shoot = 50ms)
- Frequency sweep (explosion descends from 1000Hz to 100Hz)
- Volume scaling (master volume affects all sounds)

## Response Location
`.deia/hive/responses/20260408-RAIDEN-107-RESPONSE.md`
