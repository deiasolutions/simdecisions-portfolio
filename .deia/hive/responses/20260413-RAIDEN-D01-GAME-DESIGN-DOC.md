# Raiden-Style Shmup: Complete Game Design

## 1. Game Overview
- **Genre:** Vertical scrolling shoot-em-up
- **Target Platform:** Browser (PC + mobile)
- **Target File:** `browser/public/games/raiden-v1-20260413.html`
- **Tech Stack:** Single HTML file, Canvas API, Web Audio API, NEAT for AI
- **Game Structure:** 10 levels, progressive difficulty, boss battles, second loop
- **Target Audience:** Casual to hardcore shmup enthusiasts
- **Session Length:** 3.5-5 minutes per level, 35-50 minutes full game
- **Orientation:** Portrait mode (locked), landscape optional for tablets

---

## 2. Enemy Roster (Final)

All enemies scale with level according to the difficulty formulas in section 6.

| ID | Enemy Type | Movement Pattern | Attack | HP (L1) | Speed (L1) | Score Value | Spawn Levels |
|----|-----------|------------------|--------|---------|------------|-------------|--------------|
| E01 | Straight Diver | Straight down, constant speed | Kamikaze collision only | 1 | 150px/s | 1,000 | 1-10 |
| E02 | Weaving Scout | Sine wave descent (80px amplitude, 2Hz) | Aimed shot every 2s | 1 | 100px/s | 1,000 | 1-10 |
| E03 | Formation Fighter | V-formation, holds, then dives | 3-bullet spread on dive | 2 | 250px/s | 5,000 | 1-10 |
| E04 | Spiral Bomber | Spiral outward from center | Drops bombs while spiraling | 2 | 120°/s | 5,000 | 2-10 |
| E05 | Side Swooper | Arc swoop from left/right edge | Rapid-fire (3/sec) during swoop | 2 | 200px/s | 5,000 | 2-10 |
| E06 | Turret Tank | Descends to mid, stops 5s, continues | 5-way radial burst every 1.5s | 5 | 60px/s | 10,000 | 3-10 |
| E07 | Shielded Carrier | Slow center descent | Spawns 2 Divers every 3s | 10 (5 shield) | 40px/s | 10,000 | 3-10 |
| E08 | Chaser Drone | Tracks player X (0.5s lag) | Aimed shot when aligned | 3 | 180px/s | 5,000 | 4-10 |
| E09 | Ring Shooter | Descends to mid, holds position | 8-way ring every 2s | 4 | 100px/s | 10,000 | 4-10 |
| E10 | Zigzag Interceptor | Sharp 90° turns every 0.8s | Aimed shot at each turn | 2 | 220px/s | 5,000 | 4-10 |
| E11 | Wave Leader | Horizontal sine wave at top | 3-bullet spread every 1.5s | 6 | 180px/s | 10,000 | 5-10 |
| E12 | Kamikaze Accelerator | Pauses 1s, then accelerates | Collision only | 1 | 0→400px/s | 5,000 | 5-10 |
| E13 | Split Bomber | Splits into 2 at mid-screen | Children fire single bullets | 3 (1 per child) | 120px/s | 10,000 | 6-10 |
| E14 | Laser Frigate | Horizontal traverse at top | 140px wide laser for 2s, 3s pause | 12 | 70px/s | 50,000 | 7-10 |
| E15 | Bullet Curtain Generator | Stationary at top-center | 5 aimed bullets/sec | 8 | 0px/s | 50,000 | 8-10 |
| E16 | Escort Fighter | Orbits carriers/bosses (60px radius) | Aimed shot every 2s | 2 | 150px/s | 5,000 | 3-10 |
| E17 | Homing Missile Launcher | Descends at screen edge | 1 homing missile every 4s | 6 | 50px/s | 10,000 | 9-10 |

**Visual Design (CSS-only):**
- **Straight Diver:** Red triangle (10px base, pointing down)
- **Weaving Scout:** Orange diamond (12×12px)
- **Formation Fighter:** Red pentagon (15px diameter)
- **Spiral Bomber:** Pink circle (18px) with rotating trail
- **Side Swooper:** Red chevron (15×10px)
- **Turret Tank:** Dark red square (25×25px) with rotating turret line
- **Shielded Carrier:** Gray rectangle (40×30px) with blue shield glow
- **Chaser Drone:** Yellow circle (12px) with tracking line to player
- **Ring Shooter:** Magenta octagon (20px diameter)
- **Zigzag Interceptor:** Red X-shape (14px)
- **Wave Leader:** Large red star (22px, 5 points)
- **Kamikaze Accelerator:** Bright red circle (8px) with flame trail
- **Split Bomber:** Purple oval (20×15px), splits into 2 circles (10px)
- **Laser Frigate:** Large gray rectangle (60×40px) with cyan laser beam
- **Bullet Curtain:** Dark purple hexagon (30px) with bullet spawn points
- **Escort Fighter:** Small orange triangle (8px)
- **Missile Launcher:** Black rectangle (30×20px) at edge

All enemies use:
- Base color: `var(--sd-danger)` (red spectrum)
- Glow effect: `box-shadow: 0 0 10px currentColor`
- Hit flash: Change to `var(--sd-bg)` for 2 frames on damage

---

## 3. Weapon Progression (Final)

Player collects power-ups by destroying enemies (every 5th enemy drops power-up). Icon cycles through colors every 1.5s.

### Weapon Tiers

#### VULCAN CANNON (Red Power-Up)

| Tier | Damage | Fire Rate | Pattern | Spread | Visual |
|------|--------|-----------|---------|--------|--------|
| 1 | 1 | 5/s | 2 parallel bullets | 0° | Small cyan circles (3px), 10px apart |
| 2 | 1.5 | 6/s | 4 parallel bullets | 5° outer | Cyan circles (4px), 15px apart |
| 3 | 2 | 7/s | 6 fan bullets | 45° total | Cyan circles (5px), 7.5° intervals |
| 4 | 2.5 | 9/s | 8 fan bullets | 60° total | Cyan circles (5px), 8.6° intervals |
| 5 | 3 | 12/s | 10 curved bullets | 80° arc | Cyan circles (6px) with slight homing (5°/s) |

#### ION LASER (Blue Power-Up)

| Tier | Damage | Pattern | Width | Visual | Special |
|------|--------|---------|-------|--------|---------|
| 1 | 2/frame (60 DPS) | Single beam | 8px | Bright cyan line, glow | — |
| 2 | 3/frame (90 DPS each) | Dual beams | 10px each, 20px apart | Cyan beams | — |
| 3 | 4/frame (160 DPS) | Thick beam | 40px | Wide cyan beam | Pierces enemies |
| 4 | 4/frame (200 DPS) | Triple beams | Center 30px, sides 20px (15° angle) | Cyan beams | — |
| 5 | 6/frame (360 DPS) | Massive beam | 80px | Huge cyan beam | Pierces all, explosion particles |

#### HOMING MISSILES (Yellow Power-Up)

| Tier | Damage | Fire Rate | Count | Tracking | Speed | Visual |
|------|--------|-----------|-------|----------|-------|--------|
| 1 | 5 | 2/s | 1 | 90°/s | 200px/s | Yellow triangle (6px) with white trail |
| 2 | 7 | 3/s | 2 (10° spread) | 120°/s | 220px/s | Yellow triangles (7px) |
| 3 | 8 | 4/s | 3 (30° spread) | 150°/s | 240px/s | Yellow triangles (8px), each tracks different enemy |
| 4 | 10 | 6/s | 4 rapid | 180°/s | 260px/s | Yellow triangles (9px), prioritize low-health |
| 5 | 15 (20 direct) | 8/s | 6 spiral | 240°/s | 280px/s | Large yellow triangles (10px), splash 30px radius (5 dmg), burning trail |

#### SMART BOMB (Purple Power-Up)

Not a primary weapon. Max 3 bombs in reserve.

**Effect:**
- Clears all enemy bullets (instant)
- Deals 50 damage to all enemies on screen
- Grants 3 seconds invulnerability (player flashes cyan)
- Visual: Full-screen white flash + expanding cyan shockwave (canvas center, expands to edges over 0.5s)
- Audio: Deep "boom" + whoosh
- Cannot be refilled during boss fights

#### SHIELD (Green Power-Up)

**Duration:** 15 seconds
**Effect:**
- Absorbs 1 hit (bullet or collision)
- Visual: Rotating hexagonal barrier (40px radius) around ship, `var(--sd-primary)` color with 0.6 alpha
- Flashes yellow when 5 seconds remain (1Hz blink)
- Does NOT stack (refreshes duration if collected again)

---

## 4. Boss Designs (10 Bosses)

Each boss appears at end of level. Health bar at top of screen shows boss HP. Music transitions to unique boss theme.

### Boss Summary Table

| Level | Boss Name | HP | Phases | Key Mechanic | Weak Point | Defeat Reward |
|-------|-----------|-----|--------|--------------|------------|---------------|
| 1 | Steel Fortress | 500 | 2 | Predictable patterns | Center core (2× dmg at 50% HP) | 100K pts + weapon power-up |
| 2 | Twin Serpents | 700 | 3 | Split attention, energy beam | Must damage equally | 150K pts + shield + bomb |
| 3 | Orbital Cannon | 1,000 | 3 | Bullet density, satellites | Core opens every 10s (2× dmg) | 200K pts + tier upgrade |
| 4 | Hydra Carrier | 1,500 | 3 | Destroy weak points, spawns | 3 turrets (200 HP each), core (500 HP) | 300K pts + 2 bombs + shield |
| 5 | Phase Shifter | 2,000 | 3 | Teleportation, invincibility phases | 0.5-2s window after teleport | 500K pts + tier upgrade + 3 bombs |
| 6 | Living Crystal | 2,500 | 3 | Regeneration (10 HP/s if drones alive) | Destroy drones first | 750K pts + full tier + shield + 3 bombs |
| 7 | Sky Fortress Command | 3,000 | 3 | Multi-section, target priority | 6 sections (250 HP each) + core (1,000 HP) | 1M pts + full health + 5 bombs + shield |
| 8 | Biomechanical Titan | 4,000 | 3 | Environmental hazards, ultimate beam | Arms (400 HP each), eyes (200 HP each) | 1.5M pts + weapon max + 7 bombs + 2 shields |
| 9 | Warp Gate Guardian | 5,000 | 3 | Reality distortion, summons | Real boss hidden in 4-way split | 2.5M pts + full restore + 10 bombs + 3 shields + extra life |
| 10 | CRYSTAL CORE OMEGA | 10,000 | 4 | All mechanics combined | Drones + mini-bosses shield boss | 10M pts + GAME CLEAR + second loop unlock |

### Boss Phase Details (Abbreviated)

**Level 1 - Steel Fortress:**
- Phase 1 (100-50%): Stationary, 3-bullet spread + side turrets
- Phase 2 (50-0%): Moves left-right, 5-way burst, drops mines, core exposed (2× dmg)

**Level 2 - Twin Serpents:**
- Phase 1 (100-60%): Mirrored vertical oscillation, energy beam damages on contact
- Phase 2 (60-30%): Separate, sine waves, dash attacks (telegraphed)
- Phase 3 (30-0%): Spiral perimeter, continuous aimed bullets, homing mines

**Level 3 - Orbital Cannon:**
- Phase 1 (100-70%): 8-way ring, rotating laser, 4 orbital satellites (20 HP each)
- Phase 2 (70-40%): 16-way ring, faster laser, 3 homing missiles, core opens every 10s
- Phase 3 (40-0%): Spiraling bullets, rapid aimed fire, satellites respawn infinitely

**Level 4 - Hydra Carrier:**
- Phase 1 (100-65%): 3 weak points (front cannons + rear turret), spawns Divers
- Phase 2 (65-30%): Remaining turrets, spawns Scouts/Bombers, core 8-way ring
- Phase 3 (30-0%): Zigzag, rapid-fire, spawns Kamikazes, desperation laser sweep

**Level 5 - Phase Shifter:**
- Phase 1 (100-70%): Teleports every 5s, 12-way ring on arrival, invincible 2s after teleport
- Phase 2 (70-40%): Teleports every 3s, summons 2 phase echoes (100 HP each)
- Phase 3 (40-0%): Rapid teleport (2s), 30-bullet curtain, 4 echoes, ultimate laser charge

**Level 6 - Living Crystal:**
- Phase 1 (100-60%): Pulsating, 8-way shards, 4 drones (40 HP), regenerates 10 HP/s if drones alive
- Phase 2 (60-30%): 16-way ring, 6 drones (respawn after 15s), tracking laser, splits into 3 segments briefly
- Phase 3 (30-0%): Pursuit mode, 20 bullets/s spray, 8 drones, screen-wide crystal explosion (telegraphed)

**Level 7 - Sky Fortress Command:**
- Phase 1 (100-70%): 6 turret sections (each fires unique pattern), main core fires 40-bullet curtain
- Phase 2 (70-40%): Remaining sections fire 2× faster, spawns 4 Laser Frigates, mega-cannon charge
- Phase 3 (40-0%): Descends toward player, continuous aimed stream, EMP blast, self-destruct at 10%

**Level 8 - Biomechanical Titan:**
- Phase 1 (100-75%): Arms sweep/drop bombs, core 12-way ring, spawns Escort Fighters
- Phase 2 (75-50%): Eye lasers (track player 3s), summons pillars (50 HP), toxic clouds, 16-way spiral
- Phase 3 (50-0%): Charges repeatedly, 30 bullets/s, tendrils from sides, ultimate beam (8s charge, safe zones at bottom corners)

**Level 9 - Warp Gate Guardian:**
- Phase 1 (100-66%): Summons previous enemies, 20-way ring, mini-warp gates redirect bullets
- Phase 2 (66-33%): Teleports every 4s, summons mini-bosses (30% HP), reverses controls 3s, shadow clones
- Phase 3 (33-0%): Erratic blinking, 60-bullet curtain, all previous boss attacks, gravity well, reality fracture (4-way split, 1 real)

**Level 10 - CRYSTAL CORE OMEGA:**
- Phase 1 (100-75%): 24-way ring, 4 rotating lasers, 8 drones (60 HP, respawn 20s), boss takes 70% reduced dmg if >4 drones alive
- Phase 2 (75-50%): 32-way ring, 6 lasers, 12 drones + 4 mini-bosses, regenerates 20 HP/s if mini-bosses alive
- Phase 3 (50-25%): Teleports every 3s, 80-bullet curtain, 8 lasers, 16 drones, reality distortion, gravity pulses, ultimate beam (10s charge)
- Phase 4 (25-0%): Screen scrolls erratically, all previous attacks simultaneously, 40 bullets/s spray, 12 lasers, summons all enemies/bosses, screen-wide explosions (safe zones marked), self-destruct at 5%

---

## 5. Level Flow (10 Levels)

Each level consists of: intro (30s), main section (90s), pre-boss (30s), boss fight (60-120s).

| Level | Duration | Enemy Count | Enemy Types Featured | Boss | Power-Ups | Difficulty Theme |
|-------|----------|-------------|----------------------|------|-----------|------------------|
| 1 | 60s + boss | 20 | E01, E02, E03 | Steel Fortress | 2 weapon, 1 bomb | Tutorial - basic patterns |
| 2 | 75s + boss | 25 | E01-E05 | Twin Serpents | 2 weapon, 1 shield, 1 bomb | Introduce side attacks |
| 3 | 90s + boss | 30 | E01-E07 | Orbital Cannon | 3 weapon, 1 shield, 2 bombs | Dense bullet patterns |
| 4 | 90s + boss | 35 | E01-E08 | Hydra Carrier | 3 weapon, 2 shields, 2 bombs | Multi-target management |
| 5 | 100s + boss | 40 | E01-E12 | Phase Shifter | 4 weapon, 2 shields, 3 bombs | Speed & aggression |
| 6 | 100s + boss | 45 | E01-E13 | Living Crystal | 4 weapon, 3 shields, 3 bombs | Regeneration pressure |
| 7 | 110s + boss | 50 | E01-E14 | Sky Fortress | 5 weapon, 3 shields, 4 bombs | Overwhelming firepower |
| 8 | 110s + boss | 55 | E01-E15 | Biomechanical Titan | 5 weapon, 4 shields, 5 bombs | Environmental hazards |
| 9 | 120s + boss | 60 | E01-E17 | Warp Gate Guardian | 6 weapon, 4 shields, 6 bombs | Reality bending chaos |
| 10 | 120s + boss | 70 | All enemies | CRYSTAL CORE OMEGA | 7 weapon, 5 shields, 7 bombs | Ultimate challenge |

**Wave Composition Formula:**
- 60% filler enemies (E01-E03)
- 30% feature enemies (level-specific)
- 10% mini-bosses (every 3rd wave)

**Spawn Rate Scaling:** See Section 6 for mathematical formula.

---

## 6. Difficulty Scaling (Final Formula)

### Formulas

**Enemy Health:**
```
Scaled Health = Base Health × (1 + (Level - 1) × 0.25)
```

**Enemy Speed:**
```
Scaled Speed = Base Speed × (1 + (Level - 1) × 0.15)
```

**Spawn Rate:**
```
Spawn Interval = 5s / (1 + (Level - 1) × 0.12)
Enemies per Wave = 3 + floor(Level / 2)
```

**Bullet Speed:**
```
Scaled Bullet Speed = Base Speed × (1 + (Level - 1) × 0.18)
```

**Bullet Density:**
```
Bullets per Pattern = Base Count × (1 + floor((Level - 1) / 2))
```

**Boss Health:**
```
Boss Health = 500 + (Level × 450)
```

### Difficulty Curve Table

| Level | Health | Speed | Spawn Interval | Bullets | Boss HP |
|-------|--------|-------|----------------|---------|---------|
| 1 | 100% | 100% | 5.0s | 100% | 950 |
| 2 | 125% | 115% | 4.46s | 100% | 1,400 |
| 3 | 150% | 130% | 3.98s | 200% | 1,850 |
| 4 | 175% | 145% | 3.57s | 200% | 2,300 |
| 5 | 200% | 160% | 3.20s | 300% | 2,750 |
| 6 | 225% | 175% | 2.88s | 300% | 3,200 |
| 7 | 250% | 190% | 2.60s | 400% | 3,650 |
| 8 | 275% | 205% | 2.35s | 400% | 4,100 |
| 9 | 300% | 220% | 2.13s | 500% | 4,550 |
| 10 | 325% | 235% | 1.94s | 500% | 5,000 |

### Second Loop Modifiers (After Level 10 Clear)

- Enemy health: ×1.6
- Enemy speed: ×1.5
- Bullet speed: ×1.7
- Spawn rate: ×1.4 (40% faster spawns)
- Bosses gain phase 4
- Reward: 10M points + achievement + Ship Skin 4

---

## 7. Scoring System (Final)

### Base Point Values

**Enemies:**
- Small (1 hit): 1,000 points
- Medium (2-3 hits): 5,000 points
- Large (4+ hits): 10,000 points
- Mini-bosses: 50,000 points
- Stage bosses: 100,000 × level multiplier

**Items:**
- Bronze medal: 50 points
- Silver medal: 500 points
- Gold medal (rare): 5,000 points
- Weapon power-up: 1,000 points
- Bomb: 2,000 points
- Shield: 3,000 points

### Chain System

**Chain Multiplier:**
```
Multiplier = 1.0 + (Chain Count × 0.1)
Max: 5.0× at 40 enemies
```

**Chain Persistence:** 2 seconds without kill resets chain

**Example:**
- Kill 1: 1,000 × 1.0 = 1,000
- Kill 10: 1,000 × 2.0 = 2,000
- Kill 40: 1,000 × 5.0 = 5,000

**Visual Feedback:**
- Chain counter appears above player in bright yellow
- Audio pitch increases with chain length
- Chain breaks: red "CHAIN BREAK" text

### Medal Chaining

**Medal Value Progression:**
```
50 → 100 → 200 → 400 → 800 → 1,600 → 3,200 → 6,400 → 10,000 (max)
```

Missing a medal resets to 50 points.

### Grazing System

**Graze Definition:** Bullet passes within 5px of player hitbox without hitting

**Graze Bonus:**
- Per bullet: 10 points
- Visual: Small spark + "GRAZE" text
- Audio: High-pitched ping

**Graze Multiplier (end-of-stage):**
- 0-49 grazes: 1.0×
- 50-99 grazes: 1.2×
- 100-199 grazes: 1.5×
- 200+ grazes: 2.0×

### End-of-Stage Bonuses

**Base Bonus:** 50,000 × Level

**Multipliers:**
- No deaths: ×1.5
- No bombs used: ×1.3
- Graze bonus: ×1.2 to ×2.0
- Max chain (40+): ×1.2
- All medals collected: ×1.1
- Boss defeated in <2 min: ×1.2

**Example (Level 5, no deaths, 100 grazes, max chain):**
```
Base: 250,000
× 1.5 (no deaths) = 375,000
× 1.5 (graze) = 562,500
× 1.2 (max chain) = 675,000
Total: 675,000 points
```

### Extra Life Thresholds

```
1st extend: 50,000 points
2nd extend: 200,000 points
3rd extend: 500,000 points
4th extend: 1,000,000 points
5th+ extend: Every 1,000,000 points
```

Starting lives: 3
Max lives on screen: 9 (additional as "reserve" indicator)

---

## 8. Visual Style Guide

All graphics rendered with CSS/Canvas primitives. No sprite images.

### Color Palette

**CSS Variables (MUST USE):**
```css
--sd-primary: #4A90E2 (blue - player ship)
--sd-accent: #00FFFF (cyan - player bullets/lasers)
--sd-danger: #FF4444 (red - enemies)
--sd-warning: #FFA500 (orange - enemy bullets)
--sd-success: #44FF44 (green - power-ups)
--sd-bg: #0A0A1A (dark blue-black background)
--sd-text: #FFFFFF (white text)
```

### Entity Rendering

**Player Ship:**
- Shape: Triangular (15px base, 25px height), points upward
- Color: `var(--sd-primary)`
- Glow: `box-shadow: 0 0 10px var(--sd-primary)`
- Hit flash: White flash (5 frames) + invincibility flicker (2s)
- Death: 50+ particle explosion, red vignette, slow-motion

**Enemy Ships:**
- Base color: `var(--sd-danger)` (see Enemy Roster for specific shapes)
- Glow: `box-shadow: 0 0 10px currentColor`
- Hit flash: White flash (2 frames)
- Destruction: Particle burst (count scales with enemy size), score popup floats upward

**Bullets:**
- Player bullets: Small cyan circles (3-6px), `var(--sd-accent)`
- Enemy bullets: Small orange/red circles (4-5px), `var(--sd-warning)`
- Lasers: Solid lines with gradient glow, `var(--sd-accent)` for player
- Missiles: Triangular (6-10px) with white exhaust trail

**Power-Ups:**
- Icon: Pulsating circle (20px diameter)
- Color cycle: Red → Blue → Yellow → repeat (1.5s cycle)
- Glow: `box-shadow: 0 0 20px currentColor`
- Collection: Burst into particles absorbed by player ship

**Explosions:**
- Small: 8-way particle burst, yellow/orange
- Medium: 16-way burst + shockwave ring, screen shake 2px
- Large: 32-way burst + multiple shockwaves, screen shake 5px, slow-motion 0.2s
- Boss: 3-stage explosion sequence (3s), screen shake 8px, dramatic orchestral hit

### Particle Effects

**Types:**
1. **Spark (hit):** Yellow/white, fast outward, fade 0.2s
2. **Explosion:** Orange/red/yellow gradient, expand + fall, fade 0.5s
3. **Smoke (damaged):** Gray, drift upward, fade 1s
4. **Laser trail:** Bright glow along beam path
5. **Missile exhaust:** White trail, fade behind projectile
6. **Shield:** Blue hexagonal shimmer, rotate around ship
7. **Power-up sparkle:** Color-matched, orbit icon

**Performance:** Max 200 particles (prioritize recent)

### Screen Shake Guidelines

- Light (2px): Medium enemy destruction
- Medium (4-5px): Player damage, large enemy
- Heavy (6-8px): Boss destruction, smart bomb
- Extreme (10px): Final boss phase transitions

**Duration:** 0.1-0.3s, decay over time

---

## 9. Controls (Final)

### PC Controls

**Keyboard:**
- Arrow keys: Move ship (8-way movement, diagonal possible)
- Spacebar: Fire (hold for continuous, or toggle auto-fire in settings)
- B or Shift: Bomb
- P: Pause
- A: Toggle AI mode
- H: Toggle hybrid mode (AI-assist)
- M: Mute/unmute
- Escape: Return to menu

**Mouse (Alternative):**
- Move cursor: Ship follows cursor position (1:1 tracking)
- Left click: Fire
- Right click: Bomb
- Middle click: Pause

### Mobile Controls

**Primary: Hybrid Direct Touch + Floating Anchor**

**Portrait Mode (Default):**
```
┌─────────────────────────────┐
│     PLAYFIELD (bullets,     │
│      enemies, ship)         │  ← 75% of screen height
│                             │
│                             │
├─────────────────────────────┤
│  [Movement Touch Zone]      │  ← 25% bottom (green thumb zone)
│  Player taps/drags here     │
│                             │
│  [Bomb: 88×88px]  [Pause]   │  ← Right-side buttons
└─────────────────────────────┘
```

**Touch Behavior:**
1. Player taps anywhere in bottom 25% of screen
2. Ship moves to finger position (1:1 tracking)
3. Auto-fire enabled while touching
4. Bomb button: 88×88px in right thumb zone

**Landscape Mode (Optional):**
```
┌──────────────────────────────────────────────┐
│            PLAYFIELD (bullets,               │
│             enemies, ship)                   │
│                                              │
│                         [Bomb]    [Pause]    │ ← Right edge
│                          88×88     64×64     │
│                                              │
│  [Movement Zone]                             │
│  Left 40%                                    │
└──────────────────────────────────────────────┘
```

**Sensitivity Settings:**
- Normal (1.0×): 1:1 finger tracking (default)
- Fast (1.5×): Ship moves 50% faster than finger
- Turbo (2.0×): Ship moves 2× faster (for edge-to-edge dodging)

**Haptic Feedback:**
- Ship hit: Sharp vibration (50ms, strong)
- Bomb activation: Sustained rumble (200ms, medium)
- Power-up collect: Light pulse (30ms)
- Boss spawn: Three quick pulses (100ms each)

**Accessibility Options:**
- One-handed mode (left/right)
- Button size: Small (64px) / Medium (88px) / Large (112px)
- Tilt controls toggle
- Haptics on/off

---

## 10. AI Specification (Final)

Based on NEAT (NeuroEvolution of Augmenting Topologies). Self-learning AI improves through gameplay.

### Network Architecture

**Input Layer: 21 Neurons**
1. `player_x` (normalized [0,1])
2. `player_y` (normalized [0,1])
3. `player_velocity_y` (normalized [-1,1])
4-8. Nearest enemy: `rel_x`, `rel_y`, `type`, `health`, `distance`
9-12. 2nd nearest enemy: `rel_x`, `rel_y`, `type`, `distance`
13-16. Nearest 2 threat bullets: `rel_x`, `rel_y` (each)
17-18. Nearest power-up: `rel_x`, `rel_y`
19-21. Player status: `weapon_tier`, `bomb_available`, `health`

**Hidden Layer: 16 Neurons (Initial)**
- Sigmoid activation: `f(x) = 1 / (1 + e^(-x))`
- NEAT evolves topology (adds/removes neurons/connections)

**Output Layer: 4 Neurons**
1. `move_left` [0,1]
2. `move_right` [0,1]
3. `fire` [0,1] (fire if >0.5)
4. `use_bomb` [0,1] (bomb if >0.8)

**Movement decoding:**
```
final_x_velocity = (move_right - move_left) × max_speed
Deadzone: if both <0.3, no movement
```

### Reward Function

```
Fitness =
    (survival_time × 1.0) +
    (score × 0.5) +
    (enemies_killed × 10.0) +
    (damage_taken × -50.0) +
    (powerups_collected × 5.0) +
    (bomb_efficiency × 3.0) +
    (proximity_penalty × -0.1)
```

**Component Breakdown:**
- **Survival time:** Measured in frames, baseline goal
- **Score:** Game score, secondary to survival
- **Enemies killed:** High weight (10.0) encourages aggression
- **Damage taken:** Strong penalty (-50.0) enforces caution
- **Power-ups:** Positive (5.0) for upgrades
- **Bomb efficiency:** `(enemies_killed_by_bomb / bombs_used) × 3.0` if bombs_used > 0
- **Proximity penalty:** `-0.1 × edge_frames` (frames at x<50 or x>width-50), encourages center positioning

### NEAT Parameters

```javascript
populationSize: 100
eliteCount: 10 (top 10% preserved)
survivalRate: 0.25 (top 25% breeding pool)
mutationRate: 0.10
addNodeRate: 0.03
addConnectionRate: 0.05
crossoverRate: 0.75
compatibilityThreshold: 3.0 (speciation)
```

### Training Loop

**Modes:**
1. **Background Training:** Uses `requestIdleCallback()`, ~10 gen/hour
2. **Manual Training:** User clicks "Train Generation" button
3. **Off:** Training paused, user plays with best AI

**Speed Multiplier:**
- 1×: Real-time (60 FPS)
- 3×: Fast (180 updates/sec)
- 10×: Ultra-fast (600 updates/sec, no rendering)
- Max: Headless (~2000 updates/sec)

**Convergence Estimates:**
- 10-20 gen: Basic competence (survives 30s)
- 50-100 gen: Good performance (completes level 1)
- 200-500 gen: Expert play (high scores, strategic bombs)
- Training time (10× speed): ~2-5 hours to expert

### Visualization

**HUD Display:**
```
Generation:        247
Alive:            42 / 100
Best (Gen):       1,245.3
Best (Ever):      2,891.7
Avg Fitness:        687.2
Species:            7
Training Speed:     10×
Gen/Hour:          ~120
```

**AI Player Visual:**
- Semi-transparent (0.7 alpha)
- Distinct color per network (hue from ID)
- Best performer highlighted with glow
- Fitness graph: Line chart showing best/avg over generations

**Network Visualization (Optional):**
- Small diagram in corner
- Neurons light up during activation
- Shows active connections

### Hybrid Modes

**1. Auto-Dodge:**
- AI controls movement
- Player controls fire/bombs

**2. Auto-Fire:**
- Player controls movement
- AI controls firing

**3. Co-Pilot:**
- AI displays suggestions (arrows, "BOMB NOW" text)
- Player retains full control

**4. Takeover:**
- AI plays automatically
- Player can press button to override

**Save/Load:**
- Best network autosaved to `localStorage` every 5 generations
- JSON export/import for sharing trained AIs

---

## 11. Sound Design

All sounds synthesized with Web Audio API (no audio files).

### Sound Effects

| Event | Frequency | Duration | Filter | Description |
|-------|-----------|----------|--------|-------------|
| Player shoot | 200Hz beep | 50ms | — | Subtle "pew" (rapid, not fatiguing) |
| Enemy explosion (small) | White noise | 150ms | 100-800Hz bandpass | High-pitched pop |
| Enemy explosion (large) | White noise | 300ms | 50-500Hz bandpass | Deep boom |
| Power-up collect | 440→880Hz sweep | 100ms | — | Ascending pleasant tone |
| Boss warning | 80Hz rumble | 500ms loop | — | Low threatening sound |
| Level complete | C-E-G-C arpeggio | 800ms | — | Victory jingle (major chord) |
| Bomb | 2000→100Hz sweep | 300ms | — | Whoosh + explosion |
| Player hit | Harsh impact | 100ms | White noise burst | Alarm beep |
| Graze | 1200Hz ping | 30ms | — | High-pitched reward |
| Boss roar | Custom per boss | 500ms | — | Unique signature on phase change |

### Music System

**Stage Music (Looping):**
- Level 1: Upbeat orchestral (heroic theme)
- Levels 2-3: Electronic/synth hybrid
- Levels 4-5: Rock guitar riffs
- Levels 6-7: Techno/industrial
- Levels 8-9: Epic orchestral (high tension)
- Level 10: Combination of all themes (climactic)

**Boss Music:**
- Unique theme per boss (overrides stage music)
- Dynamic intensity: layers add as boss HP decreases
- Phase transitions: Musical sting + key change
- Final boss: 4 distinct movements (one per phase)

**Adaptive Audio:**
- During chain: Percussion layer intensifies
- Low health: Bass increases (tense)
- Invincibility: Pitch +5% (communicates safety)

**Audio Balancing:**
- Music: 70% max volume
- Player SFX: 90% max volume
- Enemy SFX: 60% max volume
- Boss SFX: 100% max volume

**Priority System (max 32 simultaneous sounds):**
1. Player actions (always play)
2. Warnings/alerts (high priority)
3. Enemy destruction (medium)
4. Ambient (low, first to cull)

---

## 12. HUD Layout

### Top Bar (PC + Mobile)

```
┌────────────────────────────────────────┐
│ SCORE: 1,234,567   LVL 5   ♥♥♥○○○○○○  │
└────────────────────────────────────────┘
```

- **Left:** Score (large font, gold if >1M, rainbow pulse if >10M)
- **Center:** Level indicator
- **Right:** Lives (ship icons, filled = alive, empty = lost)

### Bottom Bar (PC Only)

```
│ [Weapon Icon] Tier 3          Bombs: 3 │
```

- **Left:** Current weapon icon + tier
- **Right:** Bomb count

### Mobile HUD

- **Top:** Same as PC
- **Bottom:** Virtual joystick (left) + Bomb button (right)
- **Pause:** Top-right corner (64×64px)

### Game State Overlays

**Menu:**
- "Play" / "AI Mode" / "Settings" buttons
- High score display
- Ship skin selector

**Paused:**
- Semi-transparent overlay
- "Resume" / "Restart" / "Quit" buttons

**Game Over:**
- Score summary
- High score comparison
- "Retry" / "Menu" buttons

**Level Complete:**
- 3-second transition screen
- Stats: enemies killed, grazes, accuracy, time
- Stage bonus breakdown

**AI Training:**
- Same as PLAYING but with AI visualization overlay (HUD from section 10)

---

## 13. Performance Targets

- **Desktop (PC):** 60 FPS minimum, modern browsers
- **Mobile:** 30 FPS minimum, 60 FPS target on recent devices
- **Canvas Size:** 800×600 (scales to viewport, maintains aspect ratio)
- **Max Entities:** 200 simultaneous (enemies + bullets + particles)
- **Max Particles:** 200 (prioritize recent over old)
- **Memory:** <100 MB heap, no leaks over 100+ generations of AI training
- **LocalStorage:** <5 MB for saved networks

**Optimization Techniques:**
- Hardware-accelerated canvas (`translate3d` for ship rendering)
- Batch draw calls for bullets/enemies
- Offscreen canvas for static background layers
- Object pooling for bullets/particles (avoid GC churn)
- Culling: Don't render entities outside viewport

---

## 14. File Structure (Single HTML)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Raiden-Style Shmup v1</title>
  <style>
    /* CSS variables */
    :root {
      --sd-primary: #4A90E2;
      --sd-accent: #00FFFF;
      --sd-danger: #FF4444;
      --sd-warning: #FFA500;
      --sd-success: #44FF44;
      --sd-bg: #0A0A1A;
      --sd-text: #FFFFFF;
    }

    /* Layout styles */
    body { margin: 0; padding: 0; background: var(--sd-bg); }
    canvas { display: block; margin: 0 auto; }
    /* HUD styles */
    /* Button styles */
    /* Mobile touch zone styles */
  </style>
</head>
<body>
  <canvas id="game"></canvas>
  <div id="hud">
    <!-- HUD elements here -->
  </div>

  <script>
    // === CONSTANTS ===
    const CANVAS_WIDTH = 800;
    const CANVAS_HEIGHT = 600;
    const FPS = 60;

    // === CLASSES ===
    class NeuralNetwork { /* NEAT implementation */ }
    class GeneticAlgorithm { /* Evolution logic */ }
    class GameEngine { /* Core game loop */ }
    class Entity { /* Base entity class */ }
    class Player extends Entity { /* Player ship */ }
    class Enemy extends Entity { /* Enemy types */ }
    class Bullet { /* Bullet projectiles */ }
    class PowerUp { /* Power-up items */ }
    class Boss extends Enemy { /* Boss encounters */ }
    class ParticleSystem { /* Explosions, effects */ }
    class SoundEngine { /* Web Audio synthesis */ }
    class CollisionDetector { /* Hit detection */ }
    class LevelManager { /* Wave spawning */ }
    class ScoreManager { /* Scoring, combos */ }
    class ControlManager { /* Input handling */ }
    class HUDRenderer { /* UI rendering */ }
    class TrainingManager { /* AI training loop */ }

    // === GAME INITIALIZATION ===
    const canvas = document.getElementById('game');
    const ctx = canvas.getContext('2d');
    const game = new GameEngine();

    // === GAME LOOP ===
    function gameLoop(timestamp) {
      game.update();
      game.render();
      requestAnimationFrame(gameLoop);
    }

    // === START ===
    requestAnimationFrame(gameLoop);
  </script>
</body>
</html>
```

**Sections:**
1. **Constants:** Canvas size, FPS, game config
2. **Classes:** All game systems (20+ classes)
3. **Initialization:** Create game instance
4. **Game Loop:** `requestAnimationFrame` at 60 FPS
5. **AI Training:** Integrated with game loop (optional mode)

**File Size Target:** <500 KB (minified, single HTML file)

---

## 15. Implementation Phases (for Build Specs)

**Phase 1: Core Engine (RAIDEN-101)**
- Canvas setup, game loop, `requestAnimationFrame`
- Entity system: base class, position, velocity, collision bounds
- Collision detection (circle-circle, circle-rect)
- Rendering pipeline
- Input handling (keyboard, mouse, touch)

**Phase 2: Player + Controls (RAIDEN-102)**
- Player ship movement (8-way, bounded to screen)
- PC keyboard controls (arrow keys, spacebar, B)
- Mobile touch controls (hybrid direct + floating anchor)
- Auto-fire toggle
- Death/respawn logic

**Phase 3: Enemy System (RAIDEN-103)**
- Enemy base class with movement patterns
- Implement 17 enemy types (E01-E17)
- Enemy spawning system (waves, timing)
- Enemy AI (movement patterns, attack patterns)
- Enemy destruction (particles, score popup)

**Phase 4: Weapon System (RAIDEN-104)**
- Vulcan, Laser, Missiles (5 tiers each)
- Bullet firing (rate, pattern, spread)
- Power-up drops (every 5th enemy)
- Power-up collection (color cycle, weapon upgrade)
- Bomb system (clear bullets, damage, invincibility)
- Shield system (15s duration, 1 hit absorption)

**Phase 5: Level Progression (RAIDEN-105)**
- LevelManager: wave composition, spawn timing
- Difficulty scaling (formulas from section 6)
- Background scrolling (50px/s vertical)
- 10 level backgrounds (CSS gradients/shapes)
- Level transitions (3s summary screen)
- Stage clear bonus calculation

**Phase 6: Scoring + UI (RAIDEN-106)**
- Score system (base values, chain, medals, grazing)
- HUD rendering (score, level, lives, weapon, bombs)
- Game states (menu, playing, paused, game over, level complete)
- Settings menu (sensitivity, haptics, button size, auto-fire)

**Phase 7: Sound (RAIDEN-107)**
- Web Audio API setup (AudioContext, OscillatorNode, GainNode)
- 6 synthesized SFX (shoot, explosion, power-up, boss warning, level complete, bomb)
- Stage music (looping, 10 themes)
- Boss music (unique per boss, dynamic intensity)
- Audio balancing (priority system, volume mixing)

**Phase 8: Boss Fights (RAIDEN-108)**
- Boss base class (health bar, phase system)
- 10 boss implementations (attacks, phases, weak points)
- Boss entrance animation (2-3s dramatic entry)
- Boss music integration
- Boss defeat rewards

**Phase 9: AI System (RAIDEN-109)**
- NeuralNetwork class (21-16-4 topology, sigmoid)
- GeneticAlgorithm class (selection, crossover, mutation, elitism)
- State vector construction (21 inputs)
- Fitness calculation (7-component formula)
- Training loop (background, manual, off modes)
- Speed multiplier (1×, 3×, 10×, max)
- AI visualization (HUD, fitness graph, color-coded players)

**Phase 10: Integration + Polish (RAIDEN-110)**
- Hybrid AI modes (auto-dodge, auto-fire, co-pilot, takeover)
- Save/load networks (localStorage, JSON export/import)
- Mobile responsive layout (portrait/landscape)
- Performance optimization (object pooling, culling)
- E2E testing (10 levels, AI convergence, mobile touch)
- Smoke tests (deploy to `browser/public/games/`)
- Final polish (particle effects, screen shake tuning)

---

## 16. Acceptance Criteria (for Q88N Verification)

- [ ] All 17 enemy types implemented with correct movement patterns
- [ ] All 3 weapon types with 5 tiers each, fully functional
- [ ] Bomb + shield power-ups working correctly
- [ ] 10 boss fights with 2-4 phases each, attack patterns match spec
- [ ] Level flow table complete (spawn timing, enemy counts)
- [ ] Difficulty scaling formulas applied correctly (health, speed, spawn rate, bullets)
- [ ] Scoring system complete (chain, medals, grazing, bonuses)
- [ ] HUD shows score, level, lives, weapon tier, bomb count
- [ ] PC controls (keyboard + mouse) fully functional
- [ ] Mobile controls (touch + haptics) fully functional
- [ ] 6 sound effects synthesized (no audio files)
- [ ] Stage music + boss music implemented
- [ ] AI training loop functional (100 population, NEAT evolution)
- [ ] AI visualization (generation counter, fitness display, graph)
- [ ] Hybrid modes (4 types) working correctly
- [ ] Save/load AI networks to localStorage
- [ ] Performance targets met (60 FPS PC, 30 FPS mobile)
- [ ] All colors use `var(--sd-*)` CSS variables (NO HARDCODED COLORS)
- [ ] Single HTML file, <500 KB minified
- [ ] No TBD, no placeholders, all design decisions finalized

---

## 17. Testing Plan

### Unit Tests
- Collision detection (circle-circle, circle-rect)
- State vector normalization (all values in [0,1] or [-1,1])
- Fitness calculation (correct formula)
- Difficulty scaling (health, speed match formulas)
- Weapon damage (correct values per tier)

### Integration Tests
- Full level playthrough (level 1-10)
- Boss fights (all 10 bosses, all phases)
- AI training (100 generations, fitness improves)
- Power-up collection (weapon upgrades correctly)
- Chain system (multiplier calculates correctly)

### Performance Tests
- 60 FPS maintained with 200 entities
- No memory leaks over 100+ AI generations
- Mobile 30 FPS minimum on mid-range devices
- LocalStorage save/load <100ms

### E2E Tests
- PC keyboard playthrough (complete level 1)
- Mobile touch playthrough (complete level 1)
- AI training to convergence (50 gen minimum)
- Hybrid mode (auto-dodge completes level 1)

### Smoke Tests
```bash
# File exists
test -f "browser/public/games/raiden-v1-20260413.html"

# File size <500 KB
FILE_SIZE=$(stat -c%s "browser/public/games/raiden-v1-20260413.html")
test $FILE_SIZE -lt 512000

# No hardcoded colors (grep for hex/rgb)
! grep -E '#[0-9A-Fa-f]{3,6}|rgb\(|rgba\(' "browser/public/games/raiden-v1-20260413.html"

# Contains NEAT implementation
grep -q "class NeuralNetwork" "browser/public/games/raiden-v1-20260413.html"

# Contains all 17 enemy types
grep -q "E01.*Straight Diver" "browser/public/games/raiden-v1-20260413.html"
# ... (test for E02-E17)

# Contains all 10 bosses
grep -q "Steel Fortress" "browser/public/games/raiden-v1-20260413.html"
# ... (test for all 10 boss names)
```

---

## Design Document Complete

**Status:** ALL SECTIONS FINALIZED
**No TBD, no placeholders**
**Ready for implementation specs**

Next steps:
1. Q88N reviews this design doc
2. Q33N creates 10 implementation specs (RAIDEN-101 through RAIDEN-110)
3. BEEs execute implementation specs in order
4. Each phase tested before proceeding to next
5. Final integration test + smoke test
6. Deploy to `browser/public/games/raiden-v1-20260413.html`
