# Raiden-Style Shmup Mechanics Reference
**Research Date:** 2026-04-08
**Purpose:** Design reference for vertical scrolling shoot-em-up game
**Scope:** Enemy types, weapon progression, boss mechanics, difficulty scaling, scoring systems

---

## Table of Contents
1. [Enemy Roster](#enemy-roster)
2. [Weapon Progression System](#weapon-progression-system)
3. [Boss Designs](#boss-designs)
4. [Difficulty Scaling Formula](#difficulty-scaling-formula)
5. [Scoring & Combo System](#scoring--combo-system)
6. [Visual & Audio Feedback](#visual--audio-feedback)
7. [Level Structure & Progression](#level-structure--progression)

---

## Enemy Roster

### Enemy Classification System
Classic shmups use a three-tier system:
- **Small enemies:** 1,000 points
- **Medium enemies:** 10,000 points
- **Large enemies/Bosses:** 100,000+ points

### 15+ Enemy Types with Movement Patterns

#### 1. **Straight Diver**
- **Movement:** Enters from top, moves straight down at constant speed
- **Attack:** No shooting, kamikaze collision
- **Health:** 1 hit
- **Speed:** Medium (150px/s)
- **Spawn:** Common in early waves, groups of 3-5
- **Inspired by:** Galaga Bees

#### 2. **Weaving Scout**
- **Movement:** Sine wave pattern while descending (amplitude: 80px, frequency: 2Hz)
- **Attack:** Fires single aimed shot every 2 seconds
- **Health:** 1 hit
- **Speed:** Slow descent (100px/s)
- **Spawn:** Pairs or trios, mid-level
- **Inspired by:** Galaga Butterflies

#### 3. **Formation Fighter**
- **Movement:** Enters in formation (V-shape or line), holds position briefly, then dives
- **Attack:** Fires 3-bullet spread on dive
- **Health:** 2 hits
- **Speed:** Fast dive (250px/s)
- **Spawn:** Groups of 5-7, arranged geometrically
- **Inspired by:** Galaga entrance patterns

#### 4. **Spiral Bomber**
- **Movement:** Spiral pattern outward from center (increasing radius)
- **Attack:** Drops bombs (slow-moving projectiles) while spiraling
- **Health:** 2 hits
- **Speed:** Medium rotation (120°/s)
- **Spawn:** Solo or pairs from top-center
- **Inspired by:** Classic arcade spiral enemies

#### 5. **Side Swooper**
- **Movement:** Enters from left/right edge, swoops in arc across screen
- **Attack:** Aimed rapid-fire (3 bullets/second) during swoop
- **Health:** 2 hits
- **Speed:** Fast horizontal (200px/s)
- **Spawn:** Singles from alternating sides
- **Inspired by:** Raiden side attackers

#### 6. **Turret Tank**
- **Movement:** Enters from top, slowly descends to mid-screen, stops for 5s, then continues
- **Attack:** Fires 5-way radial burst every 1.5s while stationary
- **Health:** 5 hits
- **Speed:** Slow (60px/s)
- **Spawn:** 1-2 per wave, mid to late game
- **Inspired by:** Ground turret enemies

#### 7. **Shielded Carrier**
- **Movement:** Slow straight descent down center
- **Attack:** No direct attack, spawns 2 Straight Divers every 3 seconds
- **Health:** 10 hits (front shield absorbs 5)
- **Speed:** Very slow (40px/s)
- **Spawn:** 1 per wave, appears levels 3+
- **Inspired by:** Raiden carrier ships

#### 8. **Chaser Drone**
- **Movement:** Tracks player's X-position with slight lag (0.5s delay)
- **Attack:** Single aimed shot when aligned vertically
- **Health:** 3 hits
- **Speed:** Fast horizontal tracking (180px/s), slow descent (80px/s)
- **Spawn:** 2-4 in spread formation
- **Inspired by:** Homing enemy behaviors

#### 9. **Ring Shooter**
- **Movement:** Enters from top-center, descends to mid-screen, holds position
- **Attack:** Fires 8-way ring pattern (45° intervals) every 2 seconds
- **Health:** 4 hits
- **Speed:** Medium descent (100px/s)
- **Spawn:** 1-2, levels 4+
- **Inspired by:** Danmaku radial patterns

#### 10. **Zigzag Interceptor**
- **Movement:** Sharp zigzag pattern (90° turns every 0.8s)
- **Attack:** Fires aimed shot at each turn
- **Health:** 2 hits
- **Speed:** Fast (220px/s)
- **Spawn:** Groups of 3, unpredictable timing
- **Inspired by:** Aggressive pursuit enemies

#### 11. **Wave Formation Leader**
- **Movement:** Horizontal sine wave at top of screen (doesn't descend immediately)
- **Attack:** Fires 3-bullet spread aimed at player every 1.5s
- **Health:** 6 hits
- **Speed:** Fast horizontal (180px/s), no vertical
- **Spawn:** 1 per wave, flanked by Formation Fighters
- **Inspired by:** Galaga Boss Galagas

#### 12. **Kamikaze Accelerator**
- **Movement:** Pauses at top for 1s, then accelerates rapidly toward player's position
- **Attack:** No shooting, pure collision
- **Health:** 1 hit
- **Speed:** Starts at 0, accelerates to 400px/s
- **Spawn:** Singles or pairs, levels 5+
- **Inspired by:** Fast kamikaze attackers

#### 13. **Split Bomber**
- **Movement:** Straight descent, splits into 2 smaller units at mid-screen
- **Attack:** No attack before split; child units fire single bullets
- **Health:** 3 hits (splits at 1 HP remaining), children have 1 HP each
- **Speed:** Medium (120px/s)
- **Spawn:** 1-3, levels 6+
- **Inspired by:** Splitting enemy mechanics

#### 14. **Laser Frigate**
- **Movement:** Enters from side, moves horizontally across top third of screen
- **Attack:** Fires continuous laser beam (140px width) downward for 2s, then pauses 3s
- **Health:** 12 hits
- **Speed:** Slow horizontal (70px/s)
- **Spawn:** 1 per wave, levels 7+
- **Inspired by:** Mid-boss laser enemies

#### 15. **Bullet Curtain Generator**
- **Movement:** Stationary at top-center after entering
- **Attack:** Fires overlapping aimed bullets (5 bullets/s) creating dense patterns
- **Health:** 8 hits
- **Speed:** N/A (stationary)
- **Spawn:** 1, levels 8+
- **Inspired by:** Danmaku pattern generators

#### 16. **Escort Fighter**
- **Movement:** Orbits around Shielded Carrier or boss in circular path (radius: 60px)
- **Attack:** Fires single aimed shot every 2s
- **Health:** 2 hits
- **Speed:** Orbital (150px/s)
- **Spawn:** 2-4 around larger enemies
- **Inspired by:** Support unit patterns

#### 17. **Homing Missile Launcher**
- **Movement:** Descends slowly at screen edge (left or right)
- **Attack:** Launches 1 homing missile every 4s (missile tracks player, speed 100px/s)
- **Health:** 6 hits
- **Speed:** Slow descent (50px/s)
- **Spawn:** 1 per side, levels 9+
- **Inspired by:** Homing projectile mechanics

---

## Weapon Progression System

### Power-Up Collection Mechanic
- **Icon appearance:** Dropped by specific enemies (every 5th enemy destroyed)
- **Icon behavior:** Floats to center of screen, cycles through colors every 1.5s
- **Color cycle:** Red (Vulcan) → Blue (Laser) → Yellow (Missiles) → repeat
- **Collection:** Fly over icon to collect current weapon type
- **Upgrade:** Collecting same weapon type repeatedly upgrades tier (max tier 5)
- **Downgrade prevention:** Taking damage reduces weapon tier by 1 (never below tier 1)

### Weapon Tier Progression

#### **VULCAN CANNON** (Red Power-Up)

**Tier 1: Basic Vulcan**
- Damage: 1 per bullet
- Fire rate: 5 shots/second
- Pattern: 2 parallel bullets (10px apart)
- Spread: 0° (straight ahead)
- Effective range: Close to medium

**Tier 2: Double Vulcan**
- Damage: 1.5 per bullet
- Fire rate: 6 shots/second
- Pattern: 4 parallel bullets (15px apart)
- Spread: 5° per outer bullet
- Effective range: Close to medium-far

**Tier 3: Wide Spread**
- Damage: 2 per bullet
- Fire rate: 7 shots/second
- Pattern: 6 bullets in fan formation
- Spread: 45° total (7.5° intervals)
- Effective range: Wide area coverage

**Tier 4: Rapid Spread**
- Damage: 2.5 per bullet
- Fire rate: 9 shots/second
- Pattern: 8 bullets in fan formation
- Spread: 60° total (8.6° intervals)
- Effective range: Full frontal coverage

**Tier 5: Maximum Vulcan**
- Damage: 3 per bullet
- Fire rate: 12 shots/second
- Pattern: 10 bullets with curved trajectory
- Spread: 80° total arc
- Effective range: Screen-wide coverage
- Special: Bullets have slight homing (5° correction/second)

---

#### **ION LASER** (Blue Power-Up)

**Tier 1: Thin Beam**
- Damage: 2 per frame (continuous)
- Fire rate: Continuous beam
- Pattern: Single beam (8px width)
- Range: Full screen length
- DPS: ~60 damage/second

**Tier 2: Dual Beam**
- Damage: 3 per frame (continuous)
- Fire rate: Continuous beam
- Pattern: 2 parallel beams (20px apart, 10px width each)
- Range: Full screen length
- DPS: ~90 damage/second (per beam)

**Tier 3: Thick Beam**
- Damage: 4 per frame (continuous)
- Fire rate: Continuous beam
- Pattern: Single wide beam (40px width)
- Range: Full screen length
- DPS: ~160 damage/second
- Special: Pierces multiple enemies

**Tier 4: Triple Beam**
- Damage: 4 per frame (continuous)
- Fire rate: Continuous beam
- Pattern: 3 beams (center: 30px, sides: 20px width, angled 15° outward)
- Range: Full screen length
- DPS: ~200 damage/second (all beams)

**Tier 5: Maximum Laser**
- Damage: 6 per frame (continuous)
- Fire rate: Continuous beam
- Pattern: Single massive beam (80px width)
- Range: Full screen length
- DPS: ~360 damage/second
- Special: Pierces all enemies, creates explosion particles on contact

---

#### **HOMING MISSILES** (Yellow Power-Up)

**Tier 1: Basic Missiles**
- Damage: 5 per missile
- Fire rate: 2 missiles/second
- Pattern: Straight launch, tracks nearest enemy after 0.5s
- Tracking: 90°/second turn rate
- Speed: 200px/second
- Count: 1 missile

**Tier 2: Dual Missiles**
- Damage: 7 per missile
- Fire rate: 3 missiles/second
- Pattern: 2 missiles launched simultaneously (angled 10° outward)
- Tracking: 120°/second turn rate
- Speed: 220px/second
- Count: 2 missiles

**Tier 3: Spread Missiles**
- Damage: 8 per missile
- Fire rate: 4 missiles/second
- Pattern: 3 missiles in 30° spread
- Tracking: 150°/second turn rate
- Speed: 240px/second
- Count: 3 missiles
- Special: Each missile tracks different enemy

**Tier 4: Rapid Missiles**
- Damage: 10 per missile
- Fire rate: 6 missiles/second
- Pattern: 4 missiles in rapid succession
- Tracking: 180°/second turn rate
- Speed: 260px/second
- Count: 4 missiles
- Special: Prioritizes low-health enemies

**Tier 5: Maximum Missiles**
- Damage: 15 per missile (20 on direct hit)
- Fire rate: 8 missiles/second
- Pattern: 6 missiles spiraling outward, then homing
- Tracking: 240°/second turn rate
- Speed: 280px/second
- Count: 6 missiles
- Special: Splash damage (30px radius, 5 damage), leaves burning trail

---

#### **SMART BOMB** (Purple Power-Up)

- **Not a primary weapon** — collected separately (max 3 in reserve)
- **Activation:** Press bomb button
- **Effect:**
  - Clears all enemy bullets on screen (instant)
  - Deals 50 damage to all enemies on screen
  - Grants 3 seconds invulnerability
  - Visual: Full-screen flash + expanding shockwave
- **Recharge:** Cannot be refilled during boss fights

---

#### **SHIELD** (Green Power-Up)

- **Duration:** 15 seconds
- **Effect:**
  - Absorbs 1 hit (bullet or collision)
  - Visual: Rotating hexagonal barrier around ship (40px radius)
  - Flashes when 5 seconds remain
- **Does NOT stack** — refreshes duration if collected again

---

## Boss Designs

### Boss Fight Structure
- **Entrance:** Dramatic entry animation (2-3 seconds)
- **Health bar:** Displayed at top of screen
- **Phases:** Each boss has 2-3 attack phases (triggered at 75%, 50%, 25% HP)
- **Vulnerable points:** Some bosses have specific weak spots (2x damage)
- **Music:** Unique boss theme per level (intensifies with each phase)

---

### Level 1 Boss: **Steel Fortress**
**Type:** Flying battleship
**Health:** 500 HP
**Theme:** Introductory boss, predictable patterns

**Phase 1 (100%-50% HP):**
- **Movement:** Stationary at top-center
- **Attack 1:** Fires 3-bullet spread aimed at player every 2 seconds
- **Attack 2:** Side turrets (2) fire single bullets alternating (1 shot/second each)
- **Vulnerable points:** None

**Phase 2 (50%-0% HP):**
- **Movement:** Moves left-right slowly across top of screen
- **Attack 1:** 5-way radial burst from center every 3 seconds
- **Attack 2:** Side turrets fire faster (2 shots/second each)
- **Attack 3:** Drops 2 mines that fall slowly (destroyable, 2 HP each)
- **Vulnerable points:** Center core exposed (2x damage)

**Defeat reward:** 100,000 points + weapon power-up

---

### Level 2 Boss: **Twin Serpents**
**Type:** Dual flying craft connected by energy beam
**Health:** 700 HP (350 HP each)
**Theme:** Split attention, positional awareness

**Phase 1 (100%-60% HP):**
- **Movement:** Both craft mirror each other vertically, oscillate left-right
- **Attack 1:** Each craft fires aimed 3-bullet spread every 2.5s
- **Attack 2:** Energy beam connecting them damages player on contact (50px width)
- **Vulnerable points:** Both craft must be damaged equally (imbalance heals weaker one)

**Phase 2 (60%-30% HP):**
- **Movement:** Craft separate, move independently in sine waves
- **Attack 1:** Each fires 5-way spread aimed at player
- **Attack 2:** Occasionally dash toward player (1 craft at a time, telegraph 1s beforehand)
- **Vulnerable points:** None

**Phase 3 (30%-0% HP):**
- **Movement:** Both craft spiral around screen perimeter
- **Attack 1:** Continuous aimed bullets (4/second per craft)
- **Attack 2:** Drop homing mines (3 HP each, track player slowly)
- **Vulnerable points:** Destroying one craft causes other to go berserk (attack rate doubles)

**Defeat reward:** 150,000 points + shield power-up + bomb

---

### Level 3 Boss: **Orbital Cannon**
**Type:** Stationary orbital platform
**Health:** 1,000 HP
**Theme:** Bullet density, pattern memorization

**Phase 1 (100%-70% HP):**
- **Movement:** Stationary at top-center
- **Attack 1:** 8-way ring pattern (45° intervals) every 2s
- **Attack 2:** Slow-rotating laser beam (120px length, rotates 360° over 8s)
- **Attack 3:** 4 satellite turrets orbit boss (30px radius), each fires aimed bullet every 2s
- **Vulnerable points:** Satellites can be destroyed (20 HP each), reduces attack density

**Phase 2 (70%-40% HP):**
- **Movement:** Stationary
- **Attack 1:** 16-way dense ring pattern every 3s
- **Attack 2:** Laser beam rotates faster (360° over 5s)
- **Attack 3:** Remaining satellites fire 3-bullet spreads
- **Attack 4:** Drops 3 large missiles that track player (destroyable, 10 HP each)
- **Vulnerable points:** Central core briefly opens every 10s (2x damage, 2s window)

**Phase 3 (40%-0% HP):**
- **Movement:** Erratic shaking
- **Attack 1:** Spiraling bullet pattern (bullets spawn from center, spiral outward)
- **Attack 2:** Rapid-fire aimed bullets (8/second)
- **Attack 3:** All satellites respawn if destroyed (infinite respawns)
- **Vulnerable points:** Core permanently exposed (2x damage)

**Defeat reward:** 200,000 points + weapon tier upgrade

---

### Level 4 Boss: **Hydra Carrier**
**Type:** Multi-segmented flying fortress
**Health:** 1,500 HP
**Theme:** Destroy weak points, manage spawn waves

**Phase 1 (100%-65% HP):**
- **Movement:** Slow descent from top to mid-screen, then stops
- **Attack 1:** Front cannons (2) fire 5-bullet spreads every 3s
- **Attack 2:** Spawns 2 Straight Divers from side hatches every 4s
- **Attack 3:** Rear turret fires slow-moving large bullets (20px diameter) every 5s
- **Vulnerable points:** 3 weak points (front cannons + rear turret), 200 HP each

**Phase 2 (65%-30% HP):**
- **Movement:** Moves left-right across screen
- **Attack 1:** Remaining turrets fire faster
- **Attack 2:** Spawns Weaving Scouts + Spiral Bombers every 5s
- **Attack 3:** Core fires 8-way ring pattern every 4s
- **Vulnerable points:** Destroyed turrets remain offline, core exposed (500 HP)

**Phase 3 (30%-0% HP):**
- **Movement:** Erratic zigzag pattern
- **Attack 1:** Fires aimed rapid-fire from all remaining points (12 bullets/second total)
- **Attack 2:** Continuously spawns Kamikaze Accelerators every 2s
- **Attack 3:** Desperation laser sweep (horizontal laser 200px height, sweeps up-down over 4s)
- **Vulnerable points:** Core is only target remaining

**Defeat reward:** 300,000 points + bomb x2 + shield

---

### Level 5 Boss: **Phase Shifter**
**Type:** Dimension-warping craft
**Health:** 2,000 HP
**Theme:** Invincibility phases, timing-based damage windows

**Phase 1 (100%-70% HP):**
- **Movement:** Teleports to random positions every 5s
- **Attack 1:** Fires 12-way ring pattern on teleport arrival
- **Attack 2:** Aimed 5-bullet spread every 2s
- **Attack 3:** Leaves lingering energy mines at teleport departure (3 mines, 5 HP each)
- **Vulnerable points:** Invincible for 2s after each teleport

**Phase 2 (70%-40% HP):**
- **Movement:** Teleports every 3s
- **Attack 1:** 16-way ring pattern on arrival
- **Attack 2:** Fires spiraling bullets during vulnerable phase
- **Attack 3:** Summons 2 "phase echoes" (clones with 100 HP each) that mimic attacks
- **Vulnerable points:** Echoes must be destroyed first, otherwise boss takes 50% reduced damage

**Phase 3 (40%-0% HP):**
- **Movement:** Rapid teleportation (every 2s)
- **Attack 1:** Dense bullet curtain on arrival (30 bullets in random directions)
- **Attack 2:** Continuous aimed rapid-fire (10 bullets/second)
- **Attack 3:** Spawns 4 phase echoes simultaneously
- **Attack 4:** Charges ultimate laser (2s charge, fires massive beam across entire screen, telegraphed)
- **Vulnerable points:** 1-second damage window after each teleport, echoes grant temporary immunity

**Defeat reward:** 500,000 points + weapon tier upgrade + bomb x3

---

### Level 6 Boss: **Living Crystal**
**Type:** Crystalline organic entity
**Health:** 2,500 HP
**Theme:** Regeneration, sustained pressure

**Phase 1 (100%-60% HP):**
- **Movement:** Slow pulsating (expands/contracts 20px every 2s)
- **Attack 1:** Fires slow-moving crystalline shards (8-way) every 3s
- **Attack 2:** Spawns 4 crystal drones that orbit (40 HP each, fire aimed bullets)
- **Attack 3:** Emits shockwave on pulse (expanding ring, 5 damage if hit)
- **Vulnerable points:** Drones must be destroyed or boss regenerates 10 HP/second

**Phase 2 (60%-30% HP):**
- **Movement:** Erratic floating, moves toward player slowly
- **Attack 1:** Rapid shard spray (16-way ring every 2s)
- **Attack 2:** Spawns 6 crystal drones (regenerate after 15s if destroyed)
- **Attack 3:** Fires aimed laser beam from core (2s duration, rotates to track player)
- **Attack 4:** Splits into 3 segments briefly (5s), each fires independently, then recombines
- **Vulnerable points:** Regenerates 5 HP/second if any drones alive

**Phase 3 (30%-0% HP):**
- **Movement:** Aggressive pursuit of player
- **Attack 1:** Continuous bullet spray (20 bullets/second in all directions)
- **Attack 2:** Spawns 8 drones in rapid succession
- **Attack 3:** Desperate laser barrage (3 rotating beams simultaneously)
- **Attack 4:** Periodic screen-wide crystal explosion (telegraphed, must use bomb or shield to survive)
- **Vulnerable points:** Stops regenerating, but drones create shield (blocks 50% damage if >4 alive)

**Defeat reward:** 750,000 points + full weapon tier upgrade + shield + bomb x3

---

### Level 7 Boss: **Sky Fortress Command**
**Type:** Massive aerial fortress with multiple sections
**Health:** 3,000 HP (1,000 HP main core + 6 sections x 250 HP each)
**Theme:** Target prioritization, overwhelming firepower

**Phase 1 (100%-70% HP):**
- **Movement:** Stationary at top of screen (fills 60% of screen width)
- **Attack 1:** 6 turret sections each fire different patterns:
  - Left wing: 5-way spread
  - Right wing: Homing missiles
  - Left flank: 8-way ring
  - Right flank: Aimed rapid-fire
  - Top: Rotating laser
  - Bottom: Mines
- **Attack 2:** Main core fires dense bullet curtain (40 bullets) every 8s
- **Vulnerable points:** Sections can be destroyed individually, reducing attack types

**Phase 2 (70%-40% HP):**
- **Movement:** Slow left-right oscillation
- **Attack 1:** Remaining sections fire twice as fast
- **Attack 2:** Spawns 4 Laser Frigates to escort
- **Attack 3:** Core charges mega-cannon (5s charge, fires line of massive bullets)
- **Vulnerable points:** Core takes reduced damage (50%) until all sections destroyed

**Phase 3 (40%-0% HP):**
- **Movement:** Descends toward player (threatening screen boundary)
- **Attack 1:** Core fires continuous aimed bullet stream (15 bullets/second)
- **Attack 2:** Deploys all remaining attack patterns simultaneously
- **Attack 3:** Periodic screen-shake EMP blast (clears player bullets, no damage)
- **Attack 4:** Self-destruct sequence begins at 10% HP (30-second countdown, fight intensifies)
- **Vulnerable points:** Core fully exposed, but player must balance damage with survival

**Defeat reward:** 1,000,000 points + full health restore + bomb x5 + shield

---

### Level 8 Boss: **Biomechanical Titan**
**Type:** Organic-mechanical hybrid colossus
**Health:** 4,000 HP
**Theme:** Environmental hazards, multi-stage arena fight

**Phase 1 (100%-75% HP):**
- **Movement:** Anchored at top-center, extends mechanical arms across screen
- **Attack 1:** Left arm sweeps horizontally (200px height, telegraphed)
- **Attack 2:** Right arm drops energy bombs (6 per volley)
- **Attack 3:** Core fires 12-way ring pattern every 3s
- **Attack 4:** Spawns Escort Fighters continuously (2 every 5s)
- **Vulnerable points:** Arms can be destroyed (400 HP each), removes corresponding attacks

**Phase 2 (75%-50% HP):**
- **Movement:** Detaches from top, floats to mid-screen
- **Attack 1:** Fires aimed laser beams from eyes (2 beams, each tracks player for 3s)
- **Attack 2:** Summons pillars from bottom of screen (destroyable, 50 HP, block player movement)
- **Attack 3:** Releases toxic clouds that slowly drift (damage over time in cloud)
- **Attack 4:** 16-way dense bullet spiral
- **Vulnerable points:** Eye lasers can be destroyed (200 HP each), exposes head core (2x damage)

**Phase 3 (50%-0% HP):**
- **Movement:** Aggressive flight, charges toward player repeatedly
- **Attack 1:** Continuous bullet spray from all sections (30 bullets/second)
- **Attack 2:** Summons organic tendrils from sides of screen (attack player from flanks)
- **Attack 3:** Ultimate attack: Charges massive beam (8s charge, full-screen vertical beam, instant kill)
  - Telegraph: Screen flashes red, tendrils retract, loud audio cue
  - Counter: Move to safe zone at bottom corners (50px radius) or use bomb
- **Vulnerable points:** Core fully exposed, but attacks are overwhelming

**Defeat reward:** 1,500,000 points + weapon tier max + bomb x7 + shield x2

---

### Level 9 Boss: **Warp Gate Guardian**
**Type:** Inter-dimensional gateway defender
**Health:** 5,000 HP
**Theme:** Reality distortion, unpredictable patterns

**Phase 1 (100%-66% HP):**
- **Movement:** Stationary at center of warp gate (background warps and distorts)
- **Attack 1:** Summons enemy types from previous levels through portals (3 enemies per wave)
- **Attack 2:** Fires 20-way ring pattern with alternating speeds (creates gaps)
- **Attack 3:** Opens mini-warp gates that redirect player bullets (50% chance)
- **Attack 4:** Dimensional shockwave (expanding ring, pushes player backward)
- **Vulnerable points:** None

**Phase 2 (66%-33% HP):**
- **Movement:** Teleports to random screen positions every 4s
- **Attack 1:** Summons mini-bosses from previous levels (reduced HP: 30% of original)
- **Attack 2:** Fires spiraling bullet patterns that curve unexpectedly
- **Attack 3:** Reverses player controls for 3 seconds (telegraphed, yellow screen tint)
- **Attack 4:** Creates "shadow clones" (3 clones, invincible, fire aimed bullets)
- **Vulnerable points:** Clones disappear when boss teleports, prioritize boss damage

**Phase 3 (33%-0% HP):**
- **Movement:** Erratic blinking (appears/disappears rapidly)
- **Attack 1:** Screen-filling bullet curtain (60 bullets per wave, every 5s)
- **Attack 2:** Summons all previous bosses' signature attacks simultaneously
- **Attack 3:** Gravity well (pulls player toward center, must fight against pull)
- **Attack 4:** Final desperation: Reality fracture (screen splits into 4 sections, boss in each, all fire independently)
- **Vulnerable points:** Only one section contains real boss (others are illusions with 1 HP)

**Defeat reward:** 2,500,000 points + full restore + bomb x10 + shield x3 + extra life

---

### Level 10 Boss: **CRYSTAL CORE OMEGA** (Final Boss)
**Type:** Octagonal/crystalline ultimate entity
**Health:** 10,000 HP (4 phases)
**Theme:** Ultimate challenge, mastery of all mechanics

**Phase 1: Awakening (100%-75% HP):**
- **Movement:** Slowly descends from top, stops at center
- **Attack 1:** 24-way ring pattern (every 2s)
- **Attack 2:** Fires 4 rotating laser beams (360° rotation over 6s)
- **Attack 3:** Summons 8 crystal drones (60 HP each, respawn after 20s)
- **Attack 4:** Aimed rapid-fire between ring patterns (8 bullets/second)
- **Vulnerable points:** Drones create shield (boss takes 70% reduced damage if >4 alive)

**Phase 2: Ascension (75%-50% HP):**
- **Movement:** Floats to top third of screen, oscillates left-right
- **Attack 1:** 32-way dense ring pattern with alternating speeds
- **Attack 2:** 6 rotating laser beams (faster rotation: 360° over 4s)
- **Attack 3:** Summons 12 drones + 4 previous level mini-bosses
- **Attack 4:** Fires spiraling bullet pattern (bullets curve inward toward player)
- **Attack 5:** Charges mega-laser (6s charge, sweeps horizontally across screen)
- **Vulnerable points:** Mini-bosses must be destroyed or boss regenerates 20 HP/second

**Phase 3: Transcendence (50%-25% HP):**
- **Movement:** Teleports to random positions every 3s
- **Attack 1:** Screen-filling bullet curtain (80 bullets per wave)
- **Attack 2:** 8 simultaneous rotating lasers
- **Attack 3:** Summons 16 drones + previous bosses' signature attacks
- **Attack 4:** Reality distortion: Screen warps, player movement feels "drunk"
- **Attack 5:** Gravity pulses (alternates push/pull every 2s)
- **Attack 6:** Ultimate beam: 10s charge, full-screen devastating laser (must use bomb or take cover behind invincible pillar that spawns)
- **Vulnerable points:** 0.5s damage window after each teleport

**Phase 4: Oblivion (25%-0% HP):**
- **Movement:** Stationary at center, but screen scrolls erratically (up, down, left, right)
- **Attack 1:** All previous attack patterns simultaneously
- **Attack 2:** Continuous bullet spray (40 bullets/second in all directions)
- **Attack 3:** 12 rotating lasers + periodic sweeping mega-lasers
- **Attack 4:** Summons all enemy types + all mini-bosses concurrently
- **Attack 5:** Screen-wide explosions (telegraphed, safe zones appear as small blue circles)
- **Attack 6:** Final desperation at 5% HP: Self-destruct sequence (45-second timer, fight intensifies exponentially)
- **Vulnerable points:** Core permanently exposed (2x damage), but survival is paramount

**Defeat reward:** 10,000,000 points + GAME CLEAR + second loop unlocked (enemy speed +50%, bullet speed +60%, new attack patterns)

---

## Difficulty Scaling Formula

### Mathematical Progression (Levels 1-10)

#### Enemy Health Scaling
```
Base Health = defined per enemy type (see Enemy Roster)
Scaled Health = Base Health × (1 + (Level - 1) × 0.25)

Examples:
- Straight Diver (1 HP base):
  - Level 1: 1 HP
  - Level 5: 2 HP
  - Level 10: 3.25 HP (rounds to 3)

- Turret Tank (5 HP base):
  - Level 1: 5 HP
  - Level 5: 10 HP
  - Level 10: 16.25 HP (rounds to 16)
```

#### Enemy Speed Scaling
```
Scaled Speed = Base Speed × (1 + (Level - 1) × 0.15)

Examples:
- Straight Diver (150px/s base):
  - Level 1: 150px/s
  - Level 5: 240px/s
  - Level 10: 352.5px/s

- Kamikaze Accelerator (400px/s max):
  - Level 1: 400px/s
  - Level 5: 640px/s
  - Level 10: 940px/s
```

#### Spawn Rate Scaling
```
Base Spawn Interval = 5 seconds (time between enemy waves)
Scaled Spawn Interval = Base Interval / (1 + (Level - 1) × 0.12)

Examples:
- Level 1: 5.0s between waves
- Level 5: 3.52s between waves
- Level 10: 2.31s between waves

Enemies per Wave = Base Count + floor(Level / 2)
- Level 1: 3 enemies
- Level 5: 5 enemies
- Level 10: 8 enemies
```

#### Bullet Speed Scaling
```
Scaled Bullet Speed = Base Speed × (1 + (Level - 1) × 0.18)

Typical Base Speeds:
- Aimed bullets: 180px/s
- Ring patterns: 150px/s
- Slow projectiles: 100px/s

Examples (aimed bullets):
- Level 1: 180px/s
- Level 5: 310px/s
- Level 10: 471px/s
```

#### Bullet Density Scaling
```
Bullets per Pattern = Base Count × (1 + floor((Level - 1) / 2))

Examples (8-way ring base):
- Level 1: 8 bullets
- Level 3: 16 bullets
- Level 5: 24 bullets
- Level 7: 32 bullets
- Level 9: 40 bullets
- Level 10: 40 bullets (caps at level 9)
```

#### Boss Health Scaling
```
Boss Health = Base Boss Health + (Level × 450)

Examples:
- Level 1: 500 + (1 × 450) = 950 HP
- Level 5: 500 + (5 × 450) = 2,750 HP
- Level 10: 500 + (10 × 450) = 5,000 HP
```

### Second Loop (Loop 2) Modifiers
After completing Level 10, game loops with increased difficulty:
- **All enemy health:** ×1.6
- **All enemy speed:** ×1.5
- **All bullet speed:** ×1.7
- **Spawn rate:** ×1.4 (enemies appear 40% faster)
- **New attack patterns:** Bosses gain additional phase 4

### Difficulty Curve Visualization
```
Level | Health | Speed  | Spawn  | Bullets | Boss HP
------|--------|--------|--------|---------|--------
1     | 100%   | 100%   | 5.0s   | 100%    | 950
2     | 125%   | 115%   | 4.46s  | 100%    | 1,400
3     | 150%   | 130%   | 3.98s  | 200%    | 1,850
4     | 175%   | 145%   | 3.57s  | 200%    | 2,300
5     | 200%   | 160%   | 3.20s  | 300%    | 2,750
6     | 225%   | 175%   | 2.88s  | 300%    | 3,200
7     | 250%   | 190%   | 2.60s  | 400%    | 3,650
8     | 275%   | 205%   | 2.35s  | 400%    | 4,100
9     | 300%   | 220%   | 2.13s  | 500%    | 4,550
10    | 325%   | 235%   | 1.94s  | 500%    | 5,000
```

---

## Scoring & Combo System

### Base Point Values

#### Enemies
- **Small enemies (1 hit):** 1,000 points
- **Medium enemies (2-3 hits):** 5,000 points
- **Large enemies (4+ hits):** 10,000 points
- **Mini-bosses:** 50,000 points
- **Stage bosses:** 100,000 points (×level multiplier)

#### Items
- **Bronze medal:** 50 points
- **Silver medal:** 500 points
- **Gold medal:** 5,000 points (appears rarely)
- **Weapon power-up:** 1,000 points
- **Bomb:** 2,000 points
- **Shield:** 3,000 points

### Combo/Chain System

#### Chain Mechanics
**Definition:** Destroying enemies in succession without letting >2 seconds pass between kills

**Chain Multiplier Formula:**
```
Multiplier = 1.0 + (Chain Count × 0.1)
Caps at 5.0x (40 enemies in chain)

Examples:
- 1 enemy: 1.0x
- 10 enemies: 2.0x
- 20 enemies: 3.0x
- 40+ enemies: 5.0x (max)
```

**Chain Display:**
- **Visual:** Chain counter appears above player ship in bright yellow
- **Audio:** Pitch of destruction sound increases with chain length
- **Persistence:** Chain resets if 2 seconds pass without a kill

**Chain Bonus:**
```
Score = Base Enemy Value × Multiplier

Example (Straight Diver, 1,000 base):
- Kill 1: 1,000 × 1.0 = 1,000 points
- Kill 2: 1,000 × 1.1 = 1,100 points
- Kill 3: 1,000 × 1.2 = 1,200 points
- Kill 10: 1,000 × 2.0 = 2,000 points
- Kill 40: 1,000 × 5.0 = 5,000 points
```

### Medal Chaining

**Mechanic:** Medals dropped by destroyed scenery/enemies increase in value when collected consecutively

**Medal Chain Formula:**
```
Medal Value Progression:
1st medal: 50 points
2nd medal: 100 points
3rd medal: 200 points
4th medal: 400 points
5th+ medal: doubles previous value (caps at 10,000)

Progression: 50 → 100 → 200 → 400 → 800 → 1,600 → 3,200 → 6,400 → 10,000 (max)
```

**Chain Break:** Missing a medal (letting it fall off screen) resets next medal to 50 points

**Strategic Note:** Medal chaining rewards precise positioning and risk-taking (collecting medals in dangerous areas)

### Grazing System

**Definition:** Bullets passing within 5px of player hitbox without hitting

**Graze Bonus:**
- **Per bullet grazed:** 10 points
- **Visual feedback:** Small spark effect + "GRAZE" text
- **Audio feedback:** High-pitched ping sound

**Graze Multiplier (Risk/Reward):**
```
Graze Count per Stage:
- 0-49 grazes: No bonus
- 50-99 grazes: 1.2x stage bonus
- 100-199 grazes: 1.5x stage bonus
- 200+ grazes: 2.0x stage bonus
```

**Applied to end-of-stage bonus calculation**

### End-of-Stage Bonuses

**Stage Clear Bonus:**
```
Base Bonus = 50,000 × Level

Multipliers applied:
- No deaths: ×1.5
- No bombs used: ×1.3
- Graze bonus: ×1.2 to ×2.0 (based on graze count)
- Max chain achieved (40+): ×1.2
- All medals collected: ×1.1
- Boss defeated in under 2 minutes: ×1.2

Example (Level 5, no deaths, 100 grazes, max chain):
Base: 250,000
× 1.5 (no deaths) = 375,000
× 1.5 (graze) = 562,500
× 1.2 (max chain) = 675,000
Total Stage Bonus: 675,000 points
```

### Extra Life Thresholds

**Extend System:**
```
1st extend: 50,000 points
2nd extend: 200,000 points
3rd extend: 500,000 points
4th extend: 1,000,000 points
5th+ extend: Every 1,000,000 points thereafter
```

**Starting lives:** 3
**Max lives on screen:** 9 (additional extends stored as "reserve" indicator)

### Score Display & Milestones

**Score Display:**
- **Location:** Top-right corner
- **Format:** Comma-separated (e.g., 1,234,567)
- **Color:** White (default), gold (>1 million), rainbow pulse (>10 million)

**Milestone Fanfares:**
- **100,000:** Small jingle + "GOOD!" text
- **500,000:** Medium fanfare + "GREAT!" text
- **1,000,000:** Large fanfare + "EXCELLENT!" text + screen flash
- **10,000,000:** Epic fanfare + "LEGENDARY!" text + full-screen particle effect

---

## Visual & Audio Feedback

### Visual Feedback Systems

#### Enemy Hit Reactions
**Purpose:** Communicate damage registration and enemy state

1. **Small enemies (1-3 HP):**
   - Flash white on hit (2 frames)
   - Shake 5px horizontally
   - Small spark particles (3-5 particles) at impact point

2. **Medium enemies (4-8 HP):**
   - Flash white + red outline on hit
   - Shake 8px + brief slow-motion (0.1s)
   - Medium explosion particles (8-12 particles)
   - Smoke trail appears at <50% HP

3. **Large enemies/Bosses (9+ HP):**
   - Flash white + damage number popup (shows damage dealt)
   - Screen shake (intensity scales with damage)
   - Large particle burst (15-20 particles)
   - Armor chunks break off at health thresholds (75%, 50%, 25%)
   - Sparking/fire effects at <30% HP

#### Destruction Effects

**Small enemy destruction:**
- **Duration:** 0.3 seconds
- **Visual:** 8-way particle burst (yellow/orange)
- **Audio:** High-pitched explosion
- **Score popup:** Floats upward for 1 second (shows points earned)

**Medium enemy destruction:**
- **Duration:** 0.5 seconds
- **Visual:** 16-way particle burst + shockwave ring
- **Screen shake:** Light (2px)
- **Audio:** Mid-range explosion + metallic clang
- **Score popup:** Larger font, glows

**Large enemy destruction:**
- **Duration:** 1.0 second
- **Visual:** 32-way particle explosion + multiple shockwaves
- **Screen shake:** Heavy (5px)
- **Audio:** Deep explosion + rumble
- **Score popup:** Very large, rainbow shimmer
- **Slow-motion:** Brief time dilation (0.2s at 50% speed)

**Boss destruction:**
- **Duration:** 3.0 seconds
- **Visual:** Multi-stage explosion sequence:
  - Stage 1 (0-1s): Rapid small explosions across boss body
  - Stage 2 (1-2s): Boss flashes white, armor shatters
  - Stage 3 (2-3s): Massive central explosion, screen-filling light flash
- **Screen shake:** Intense (8px, gradually decreasing)
- **Audio:** Layered explosions + dramatic orchestral hit
- **Slow-motion:** 0.5s at 25% speed
- **Score popup:** Huge animated number, cascading bonuses appear
- **Victory fanfare:** Unique music sting

#### Power-Up Effects

**Power-up icon appearance:**
- **Visual:** Icon materializes with spiral particle effect
- **Behavior:** Floats to screen center, pulsates (scale 0.9x-1.1x)
- **Color cycle:** Smooth transition between weapon colors (1.5s cycle time)
- **Glow:** Bright aura (20px radius) to ensure visibility

**Power-up collection:**
- **Visual:** Icon bursts into particles absorbed by player ship
- **Audio:** Pleasant "ding" sound (pitch increases with weapon tier)
- **Player ship flash:** Brief color flash matching weapon type
- **Text popup:** "POWER UP!" (1s duration, fades upward)
- **Weapon indicator update:** HUD element animates to show new tier

#### Damage & Danger Indicators

**Player taking damage:**
- **Visual:** Player ship flashes red + white alternating (5 frames)
- **Invincibility period:** 2 seconds, ship semi-transparent + flashing
- **Screen shake:** Medium (4px)
- **Audio:** Harsh impact sound + alarm beep
- **HUD update:** Life counter decreases with animation

**Player death:**
- **Visual:** Large explosion centered on ship (2-second animation)
- **Screen effect:** Red vignette + slow-motion (0.5s)
- **Particle count:** 50+ particles in all directions
- **Audio:** Loud explosion + descending tone
- **Respawn:** 3-second countdown timer, ship materializes at bottom-center

**Danger warnings:**
- **Boss ultimate attacks:** Screen border flashes red, warning klaxon sound
- **Laser charge:** Glowing charge-up effect at laser source (color intensifies)
- **Missile lock-on:** Red targeting reticle appears over player for 1s before launch
- **Screen boundaries:** Subtle red vignette when player near edge

#### Screen Shake Guidelines

**Purpose:** Communicate impact weight and importance

**Intensity levels:**
- **Light (2px):** Medium enemy destruction, boss taking damage
- **Medium (4-5px):** Player taking damage, large enemy destruction
- **Heavy (6-8px):** Boss destruction, ultimate attacks, smart bomb detonation
- **Extreme (10px):** Final boss phase transitions

**Duration:** 0.1-0.3 seconds (scales with intensity)

**Frequency:** Shake decays over duration (starts fast, slows down)

**Design principle:** "Camera shake is a privilege, not a right" — use sparingly for impact

#### Particle Effects

**Design philosophy:** Particles communicate state, not just decoration

**Particle types:**
1. **Spark particles (enemy hit):** Yellow/white, fast outward velocity, fade quickly (0.2s)
2. **Explosion particles (destruction):** Orange/red/yellow, expand outward then fall, fade over 0.5s
3. **Smoke particles (damaged):** Gray, drift upward slowly, fade over 1s
4. **Laser particles (continuous):** Bright glow, trail effect along beam
5. **Missile trails:** White exhaust, fade behind projectile
6. **Shield particles:** Blue hexagonal shimmer, rotate around ship
7. **Power-up sparkles:** Color-matched to power-up, orbit icon

**Performance:** Max 200 particles on screen (prioritize recent over old)

---

### Audio Feedback Systems

#### Sound Effect Categories

**Player actions:**
- **Vulcan shot:** Rapid "pew-pew" (subtle to avoid repetition fatigue)
- **Laser beam:** Continuous hum (pitch varies with tier)
- **Missile launch:** "Whoosh" + rocket ignition
- **Bomb activation:** Deep "boom" + shockwave whoosh
- **Movement:** Subtle engine hum (barely audible, provides feedback)

**Enemy sounds:**
- **Enemy spawn:** Brief "warp-in" sound
- **Enemy shot:** Varies by enemy type (e.g., turrets have deeper sound)
- **Enemy destroyed:** Explosion (pitch varies by enemy size)
- **Boss roar:** Unique audio signature per boss (on phase transition)

**Impact & feedback:**
- **Hit confirm:** Satisfying "thunk" when bullet connects
- **Graze:** High-pitched "ping" (reward close calls)
- **Medal collect:** Pleasant chime (pitch increases with medal chain)
- **Power-up collect:** Uplifting "ding" + shimmer sound
- **Chain increase:** Rising pitch tone (communicates combo growth)

**Warnings & alerts:**
- **Low health:** Heart-beat pulse sound (when 1 life remaining)
- **Boss warning:** Dramatic siren (3-second pre-boss entrance)
- **Ultimate attack:** Klaxon alarm + charging sound
- **Countdown timer:** Beep every second (faster as time runs out)

#### Music System

**Stage music:**
- **Level 1:** Upbeat, heroic orchestral theme (establishes adventure)
- **Level 2-3:** Electronic/synth hybrid, increasing intensity
- **Level 4-5:** Rock guitar riffs, driving beat
- **Level 6-7:** Techno/industrial, aggressive
- **Level 8-9:** Epic orchestral, high tension
- **Level 10:** Combination of all themes, climactic

**Boss music:**
- **Unique theme per boss** (overrides stage music)
- **Dynamic intensity:** Music layers add as boss HP decreases
- **Phase transitions:** Musical sting + key change
- **Final boss:** 4 distinct musical movements (one per phase)

**Adaptive audio:**
- **During chain:** Percussion layer intensifies
- **Low health:** Music becomes more tense (bass increases)
- **Invincibility:** Music pitch increases slightly (communicates safety)

#### Audio Balancing

**Priority system (max 32 simultaneous sounds):**
1. **Player actions:** Always play (feedback critical)
2. **Warnings/alerts:** High priority (safety critical)
3. **Enemy destruction:** Medium priority (satisfying, but can be culled)
4. **Ambient sounds:** Low priority (first to be dropped under load)

**Volume mixing:**
- **Music:** 70% of max volume (allows SFX to shine)
- **Player SFX:** 90% of max volume (clear feedback)
- **Enemy SFX:** 60% of max volume (present but not overwhelming)
- **Boss SFX:** 100% of max volume (dramatic moments)

---

## Level Structure & Progression

### Stage Duration & Pacing

**Level structure (typical):**
- **Intro section (30s):** Easy enemy waves, allows player to warm up, collect power-ups
- **Main section (90s):** Escalating enemy density, introduces level-specific enemy types
- **Pre-boss section (30s):** Intense wave, mini-boss or elite enemies, last chance for power-ups
- **Boss fight (60-120s):** Major encounter, tests player mastery

**Total level duration:** 3.5-5 minutes (varies by player skill and boss fight length)

### Background Scrolling

**Scroll speed:**
- **Standard levels:** 50px/second (vertical scrolling)
- **Boss encounters:** Scrolling stops when boss appears (static background)
- **Special moments:** Scroll speed increases to 100px/second during intense sequences

**Background themes (communicates setting):**
- **Level 1:** Blue skies, clouds
- **Level 2:** Mountainous terrain
- **Level 3:** Ocean/naval fleet
- **Level 4:** Industrial complex
- **Level 5:** Cityscape at night
- **Level 6:** Crystal caverns
- **Level 7:** Sky fortress
- **Level 8:** Alien biomass
- **Level 9:** Dimensional rift (abstract, warping)
- **Level 10:** Cosmic void (stars, nebulae)

### Enemy Wave Composition

**Wave structure formula:**
```
Wave = Filler Enemies + Feature Enemy + (Optional Mini-Boss)

Filler Enemies: Straight Divers, Weaving Scouts (60% of wave)
Feature Enemy: Level-specific enemy type (30% of wave)
Mini-Boss: Appears every 3rd wave (10% of encounters)
```

**Example Level 5 wave:**
- **Wave 1:** 4 Straight Divers + 2 Zigzag Interceptors
- **Wave 2:** 3 Weaving Scouts + 2 Chaser Drones + 1 Turret Tank
- **Wave 3:** 5 Formation Fighters + 1 Ring Shooter (mini-boss)

### Checkpoint System

**No traditional checkpoints** — arcade-style continues:
- **Continue system:** Player can continue from start of current level (costs 1 credit)
- **Starting continues:** 3 credits
- **Extra credits:** Earned at score milestones (every 5,000,000 points)
- **1CC (1-credit clear):** Beating game on single credit unlocks achievement

### Progression Rewards

**Per-level unlocks:**
- **Level 1 clear:** Unlock Ship Skin 2
- **Level 3 clear:** Unlock Ship Skin 3
- **Level 5 clear:** Unlock Music Player (listen to tracks)
- **Level 7 clear:** Unlock Boss Rush Mode
- **Level 10 clear:** Unlock Second Loop + Ship Skin 4
- **1CC clear:** Unlock Hard Mode (enemies have 2x HP, bullet speed +30%)

---

## Research Sources

### Academic & Design Resources
- [The Anatomy of a Shmup](https://www.gamedeveloper.com/design/the-anatomy-of-a-shmup) — Core design principles
- [(Breaking) The Shmup Dogma](https://www.gamedeveloper.com/design/-breaking-the-shmup-dogma) — Genre innovation analysis
- [Shmup Scoring Systems - Arcade Otaku](https://forum.arcadeotaku.com/viewtopic.php?t=847) — Detailed scoring mechanics
- [SHMUP Creator: Scoring Systems](https://www.shmupcreator.com/doc/?docs=shmupcreator/making-a-game/scoring-systems) — Design documentation
- [SHMUP Creator: Weapons and Bullet Patterns](https://www.shmupcreator.com/doc/?docs=shmupcreator/weapons-and-bullet-patterns) — Pattern theory

### Game-Specific Research
- [Raiden - Shmups Wiki](https://shmups.wiki/library/Raiden) — Raiden series mechanics
- [Raiden IV - Shmups Wiki](https://shmups.wiki/library/Raiden_IV) — Modern Raiden design
- [Strikers 1945 - Shmups Wiki](https://shmups.wiki/library/Strikers_1945) — Boss design patterns
- [Galaga Walkthrough - StrategyWiki](https://strategywiki.org/wiki/Galaga/Walkthrough) — Formation patterns
- [Boghog's Bullet Hell Shmup 101](https://shmups.wiki/library/Boghog's_bullet_hell_shmup_101) — Bullet pattern types

### Specific Mechanics
- [Help: Dodging Strategy - Shmups Wiki](https://shmups.wiki/library/Help:Dodging_strategy) — Player tactics
- [Help: Glossary - Shmups Wiki](https://shmups.wiki/library/Help:Glossary) — Terminology
- [Extra Life - TheAlmightyGuru](http://www.thealmightyguru.com/Wiki/index.php?title=Extra_life) — Extend systems
- [Video-Game Lives - TV Tropes](https://tvtropes.org/pmwiki/pmwiki.php/Main/VideoGameLives) — Life system design
- [Bullet Hell - Wikipedia](https://en.wikipedia.org/wiki/Bullet_hell) — Danmaku overview

### Additional References
- [Raiden (video game) - Wikipedia](https://en.wikipedia.org/wiki/Raiden_(video_game)) — Historical context
- [Vertical Scrolling Shooter - TV Tropes](https://tvtropes.org/pmwiki/pmwiki.php/Main/VerticalScrollingShooter) — Genre conventions
- [Shoot 'em up - Wikipedia](https://en.wikipedia.org/wiki/Shoot_'em_up) — Broad genre overview
- [History of Vertical Shooters - Retros.ae](https://www.retros.ae/blogs/retro-stories/history-of-vertical-shooters) — Genre evolution

---

## Summary

This reference document provides comprehensive design specifications for a Raiden-style vertical scrolling shoot-em-up:

✅ **17 distinct enemy types** with detailed movement patterns and behaviors
✅ **5 weapon tiers** across 3 primary weapon types (Vulcan, Laser, Missiles) + bombs/shields
✅ **10 boss designs** with 2-4 attack phases each, escalating complexity
✅ **Mathematical difficulty scaling** formulas for levels 1-10 (health, speed, spawn rate, bullet density)
✅ **Comprehensive scoring system** with chain multipliers, medal chaining, and grazing mechanics
✅ **Visual & audio feedback** guidelines for maximum player communication
✅ **Level structure** with pacing, wave composition, and progression rewards

**Design Philosophy:**
- **Clarity over complexity:** Every visual/audio element serves player feedback
- **Risk/reward balance:** Grazing, medal chaining, and chain systems reward skillful play
- **Progressive difficulty:** Mathematical scaling ensures smooth difficulty curve across 10 levels
- **Arcade heritage:** Respects genre conventions (Raiden, Galaga, Strikers 1945) while modernizing

**Next Steps for Implementation:**
1. Prototype core movement + shooting mechanics
2. Implement weapon progression system (3 tiers first)
3. Build enemy spawning system with 5 basic enemy types
4. Create Level 1 boss as proof-of-concept
5. Add scoring/combo system
6. Iterate on difficulty scaling with playtesting

**Research Complete:** 2026-04-08
