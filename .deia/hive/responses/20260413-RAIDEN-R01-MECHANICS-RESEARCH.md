# Raiden-Style Shmup Mechanics Research

## 1. Enemy Roster (10 types minimum)

| Enemy Type | HP | Speed | Attack Pattern | Spawn Level | Score Value | Behavior Notes |
|------------|----|----|----------------|-------------|-------------|----------------|
| Scout Fighter | 1 | 180 px/s | Straight dive | 1+ | 100 | Fast, simple diving attack, appears in groups of 3-5 |
| Formation Bomber | 2 | 120 px/s | V-formation, straight bullets | 2+ | 200 | Enters from top in formation, fires synchronized volleys |
| Weaving Drone | 1 | 150 px/s | Sine wave path | 1+ | 150 | Serpentine horizontal movement, unpredictable |
| Heavy Tank | 5 | 60 px/s | Ground-based, aimed shots | 3+ | 500 | Slow but durable, tracks player position |
| Kamikaze Cruiser | 3 | 200 px/s | Direct suicide dive | 4+ | 300 | Fast dive directly at player, no shooting |
| Turret Emplacement | 8 | 0 px/s | Rotating spread fire | 3+ | 400 | Stationary, 360° rotation, fires 8-way spread |
| Elite Fighter | 4 | 160 px/s | Figure-8 pattern, homing shots | 5+ | 600 | Complex movement, fires tracking bullets |
| Carrier Ship | 15 | 80 px/s | Spawns scouts, aimed fire | 6+ | 1200 | Mid-boss tier, releases 2-4 scouts when damaged |
| Plasma Bomber | 6 | 100 px/s | Spiral pattern, plasma orbs | 7+ | 800 | Releases slow-moving plasma obstacles |
| Command Frigate | 20 | 90 px/s | Multi-phase, laser sweep | 8+ | 2000 | Mini-boss, two attack phases, weak point in center |

## 2. Weapon Progression (5 tiers minimum)

| Tier | Weapon Name | Damage | Fire Rate | Special Effect | Visual | Power-Ups Required |
|------|-------------|--------|-----------|----------------|--------|-------------------|
| 1 | Single Shot | 1 | 200ms | None | White bullet | 0 (default) |
| 2 | Twin Shot | 1 per bullet | 200ms | Two parallel streams | Blue bullets | 1 |
| 3 | Wide Vulcan | 0.8 per bullet | 150ms | 3-way spread (30° angle) | Red bullets | 3 |
| 4 | Vulcan MAX | 0.8 per bullet | 150ms | 5-way spread (45° angle) | Red bullets w/ tracer | 5 |
| 5 | Lightning Laser | 2 per tick | Continuous | Piercing beam | Blue laser beam | 7 |

### Sub-Weapons (Secondary Fire)

| Tier | Weapon Name | Damage | Fire Rate | Special Effect | Visual | Power-Ups Required |
|------|-------------|--------|-----------|----------------|--------|-------------------|
| 1 | Missile | 3 | 1000ms | Forward only | Gray missile | 0 (default) |
| 2 | Homing Missile | 3 | 1000ms | Tracks nearest enemy | Red missile w/ trail | 2 |
| 3 | Cluster Missile | 2 per explosion | 1200ms | Splits into 3 on impact | Orange missile | 4 |
| 4 | Plasma Missile | 5 | 800ms | Area damage (50px radius) | Purple missile | 6 |
| 5 | Nuclear Missile | 8 | 1500ms | Large explosion (150px), clears bullets | Yellow missile | 8 |

### Special Weapons (Limited Use)

| Name | Effect | Cooldown | Acquisition |
|------|--------|----------|-------------|
| Smart Bomb | Screen-clear, 500 damage to all | One-time use | Rare drop (5% from elite enemies) |
| Shield | 3-hit protection | 30 seconds | Power-up drop (10% from carriers) |
| Rapid Fire | 2x fire rate for 10 seconds | 45 seconds | Power-up drop (8% from bombers) |

### Power-Up Collection Mechanics

- Power-up icons appear when specific enemies are destroyed (carriers, elites, command frigates)
- Icons float toward center screen and cycle colors every 0.8 seconds: Red (Vulcan) → Blue (Laser) → Gray (Missile)
- Collecting same weapon type consecutively increases tier (max tier: 8 for Vulcan/Laser, 5 for Missiles)
- **Loss on death:** Player drops 2 tier levels on death (tier 5 → tier 3)
- **Stacking:** Multiple power-ups collected rapidly grant bonus score (100 × tier)

## 3. Boss Mechanics (10 bosses, one per level)

| Level | Boss Name | HP | Phases | Attack Patterns | Weak Points | Phase Triggers |
|-------|-----------|----|----|-----------------|-------------|----------------|
| 1 | Gun Turret | 200 | 2 | P1: Straight bullets; P2: 3-way spread | Center barrel | 50% HP |
| 2 | Twin Cannons | 400 | 2 | P1: Alternating fire; P2: Synchronized spread | Both turrets | Destroy one turret |
| 3 | Armored Tank | 800 | 3 | P1: Forward bullets; P2: Side guns activate; P3: Kamikaze drones | Top hatch, side guns | 66%, 33% HP |
| 4 | Flying Fortress | 1200 | 2 | P1: Rotating lasers; P2: Laser + missile swarm | Core reactor (center) | 40% HP |
| 5 | Carrier Battleship | 1800 | 3 | P1: Fighter spawns; P2: Broadside cannons; P3: Desperation barrage | Bridge, engine pods | 60%, 30% HP |
| 6 | Plasma Core | 2500 | 2 | P1: Slow plasma orbs; P2: Fast plasma rain | Exposed core (appears periodically) | 50% HP |
| 7 | Dual Bomber | 3000 | 3 | P1: Bombing runs; P2: Split pattern; P3: Both units combined attack | Each bomber unit | Destroy one unit, 25% HP |
| 8 | Mega Cruiser | 4000 | 4 | P1: Turret fire; P2: Laser sweep; P3: Missile barrage; P4: All weapons | Front cannons, bridge, engines | 70%, 50%, 25% HP |
| 9 | Command Dreadnought | 5500 | 3 | P1: Formation drones; P2: Beam weapons; P3: Screen-filling bullet hell | Shield generators (4), core | Destroy all shields, 20% HP |
| 10 | Ultimate Weapon | 8000 | 5 | P1: Testing player (slow); P2: Laser grid; P3: Bullet spirals; P4: Combination; P5: Desperation (fast chaos) | Multiple cores (6 total) | Destroy 2 cores per phase |

### Boss Warning System

- **Audio cue:** Warning siren plays 2 seconds before boss entrance
- **Visual warning:** Screen flashes red border + "WARNING" text in center
- **Music change:** Boss theme begins immediately after warning
- **Screen shake:** Light rumble during boss entrance animation (0.5s)

### Weak Point Mechanics

- **Full-body damage:** All bosses take reduced damage (0.5x) on non-weak-point hits
- **Weak point damage:** Weak points take full damage (1.0x) and flash red when hit
- **Destructible components:** Some bosses have parts that can be destroyed separately (turrets, shields)
- **Invulnerability phases:** Bosses are invulnerable during entrance animation and between phases (1-2s transitions)

## 4. Difficulty Scaling Formula

### Enemy Count Progression
```
enemy_count = base_count + (level * scaling_factor)
- Level 1-3: base=20, scaling=8 → 28, 36, 44 enemies
- Level 4-6: base=20, scaling=12 → 68, 80, 92 enemies
- Level 7-10: base=20, scaling=15 → 125, 140, 155, 170 enemies
```

### Enemy Speed Scaling
```
enemy_speed = base_speed × (1.0 + level × 0.15)
- Level 1: 1.0x (base speed)
- Level 5: 1.75x
- Level 10: 2.5x
```

### Enemy Health Scaling
```
enemy_hp = base_hp × (1.0 + level × 0.25)
- Level 1: 1.0x (base HP)
- Level 5: 2.25x
- Level 10: 3.5x
```

### Spawn Frequency Scaling
```
spawn_interval = max(base_interval - (level × reduction), min_interval)
- Base interval: 500ms
- Reduction per level: 30ms
- Minimum interval: 200ms
- Level 1: 500ms
- Level 5: 350ms
- Level 10: 200ms (capped)
```

### Boss Health Scaling
```
boss_hp = base_boss_hp × (level × 0.8 + 0.2)
- Level 1: 200 HP (1.0x)
- Level 5: 800 HP (4.0x)
- Level 10: 1600 HP (8.0x)
```

### Aggression Scaling

| Level Range | Enemy Aggression | Bullet Speed | Aim Prediction |
|-------------|------------------|--------------|----------------|
| 1-2 | Passive | 1.0x | None |
| 3-4 | Moderate | 1.2x | 0.2s ahead |
| 5-6 | Aggressive | 1.5x | 0.4s ahead |
| 7-8 | Very Aggressive | 1.8x | 0.6s ahead |
| 9-10 | Extreme | 2.0x | 0.8s ahead |

### Difficulty Curve Pacing Recommendations

**Early Game (Levels 1-3): Tutorial Phase**
- Focus: Introduce mechanics gradually
- Enemy density: Low (20-40 enemies)
- Attack patterns: Simple (straight, basic formations)
- Boss complexity: 2 phases maximum
- Player power: Limited (tiers 1-3)

**Mid-Game (Levels 4-6): Ramp-Up Phase**
- Focus: Increase challenge, introduce variety
- Enemy density: Medium (60-90 enemies)
- Attack patterns: Intermediate (sine waves, aimed shots)
- Boss complexity: 3-4 phases
- Player power: Growing (tiers 4-6)

**Late Game (Levels 7-10): Expert Phase**
- Focus: Maximum challenge, bullet hell elements
- Enemy density: High (120-170 enemies)
- Attack patterns: Complex (spirals, bullet curtains, multi-directional)
- Boss complexity: 4-5 phases with desperation attacks
- Player power: Peak (tiers 7-8, multiple sub-weapons)

### Casual vs Hardcore Mode Adjustments

**Casual Mode:**
- Enemy HP: -30%
- Enemy speed: -20%
- Bullet speed: -25%
- Continues: Unlimited
- Power-up drop rate: +50%
- Lives: 5 starting lives

**Hardcore Mode:**
- Enemy HP: +20%
- Enemy speed: +15%
- Bullet speed: +30%
- Continues: None (one credit only)
- Power-up drop rate: -25%
- Lives: 3 starting lives
- Score multiplier: 2.0x all scoring

## 5. Scoring System

### Base Score Values

| Enemy Type | Base Score | Hardcore Multiplier |
|------------|-----------|---------------------|
| Scout Fighter | 100 | 200 |
| Formation Bomber | 200 | 400 |
| Weaving Drone | 150 | 300 |
| Heavy Tank | 500 | 1000 |
| Kamikaze Cruiser | 300 | 600 |
| Turret Emplacement | 400 | 800 |
| Elite Fighter | 600 | 1200 |
| Carrier Ship | 1200 | 2400 |
| Plasma Bomber | 800 | 1600 |
| Command Frigate | 2000 | 4000 |
| Level Boss | 10000 × level | 20000 × level |

### Combo Multiplier System

**Chain Mechanics:**
- Chain starts on first kill
- Chain continues if next kill occurs within **2.0 seconds** of previous kill
- Each kill in chain increases multiplier by **+0.1x**
- **Maximum multiplier: 5.0x** (50 consecutive kills)
- Chain breaks if 2.0s elapses with no kill
- **Visual feedback:**
  - Combo counter appears in top-right corner
  - Counter pulses on each kill
  - Counter color changes: White (1-2x) → Yellow (2-3x) → Orange (3-4x) → Red (4-5x)
  - Chain break shows "CHAIN BROKEN" message

**Formula:**
```
score = base_score × multiplier
multiplier = min(1.0 + (chain_count × 0.1), 5.0)
```

**Example:**
- Kill 1: Scout (100) × 1.0 = 100 points
- Kill 2: Scout (100) × 1.1 = 110 points (within 2s)
- Kill 3: Bomber (200) × 1.2 = 240 points
- Kill 4: Tank (500) × 1.3 = 650 points
- **Total: 1,100 points** (4-chain)

### Bonus Scoring

| Bonus Type | Condition | Score Award | Notes |
|------------|-----------|-------------|-------|
| No-Death Bonus | Complete level without dying | 50,000 | Per level |
| Perfect Clear | Destroy all enemies in level | 10,000 | Per level |
| Boss Speed Kill | Defeat boss in under 30s | 5,000 × level | Rewards aggression |
| Max Chain | Achieve 50+ chain | 25,000 | One-time per level |
| Full Power | Reach max weapon tier | 5,000 | One-time per level |
| Grazing Bonus | Bullet passes within 10px of player | 50 | Per bullet, encourages risk |
| 1-UP Threshold | Every 500,000 points | Extra life | Recurring |

### Score Display and Feedback

**Floating Numbers:**
- Appear at enemy death location
- Float upward for 1.0s then fade
- Size scales with score value (100pt = 12px font, 10000pt = 24px font)
- Color matches combo multiplier tier

**Screen Flash:**
- Subtle white flash (0.1s) on chain milestones (10, 25, 50 chain)
- Gold flash (0.2s) on bonus awards (no-death, perfect clear)

**Audio Cues:**
- Rising pitch "ding" sound for each chain kill (pitch increases with multiplier)
- Special "fanfare" sound for bonus awards
- "Maximum" voice sample when hitting 5.0x multiplier

### High Score Persistence

**Leaderboard Structure:**
- **Global High Score:** Single highest score across all playthroughs
- **Per-Level Records:** Best score for each of 10 levels
- **Speed Run Times:** Fastest clear time per level
- **Hardcore Leaderboard:** Separate rankings for hardcore mode

**Data Stored:**
```json
{
  "global_high_score": 9999999,
  "player_initials": "ACE",
  "date_achieved": "2026-04-13",
  "mode": "hardcore",
  "level_records": [
    {"level": 1, "score": 125000, "time": "2:34", "no_death": true},
    ...
  ]
}
```

**Display:**
- High score shown on title screen
- "NEW RECORD" banner when player beats previous high score
- End-of-level score breakdown showing: base score, combo bonus, level bonus, total

## 6. Recommended Game Flow (10 levels)

| Level | Theme | Enemy Mix | Boss Type | Difficulty Spike | Duration | Visual Theme |
|-------|-------|-----------|-----------|------------------|----------|--------------|
| 1 | Training Grounds | 80% scouts, 20% bombers | Simple gun turret | Gentle (tutorial) | 2 min | Blue sky, clouds |
| 2 | Coastal Assault | 60% scouts, 30% bombers, 10% drones | Twin cannons | Low (pattern intro) | 2.5 min | Ocean, beach |
| 3 | Urban Warfare | 40% scouts, 30% tanks, 20% turrets, 10% drones | Armored tank | Medium (first wall) | 3 min | City ruins |
| 4 | Sky Fortress | 50% bombers, 30% elites, 20% drones | Flying fortress | Medium-high (laser intro) | 3.5 min | High altitude, sunset |
| 5 | Naval Blockade | 30% scouts, 40% carriers, 20% elites, 10% kamikazes | Carrier battleship | High (mid-game peak) | 4 min | Stormy ocean |
| 6 | Energy Facility | 20% scouts, 30% plasma bombers, 30% turrets, 20% elites | Plasma core | High (new mechanics) | 4 min | Industrial, electric |
| 7 | Dual Strike | 40% bombers, 30% kamikazes, 20% elites, 10% carriers | Dual bomber | Very high (coordination test) | 4.5 min | Mountain range |
| 8 | Command Bridge | 20% scouts, 30% elites, 30% frigates, 20% plasma | Mega cruiser | Very high (gauntlet) | 5 min | Space station |
| 9 | Final Approach | 10% scouts, 30% carriers, 40% frigates, 20% elites | Command dreadnought | Extreme (bullet hell) | 5.5 min | Deep space |
| 10 | Ultimate Showdown | 20% all enemy types (mixed chaos) | Ultimate weapon | Maximum (final test) | 6 min | Cosmic void |

### Pacing Notes

**Level Design Philosophy:**
- **Levels 1-2:** Breathing room between waves (3-5s gaps)
- **Levels 3-5:** Moderate pressure (2-3s gaps)
- **Levels 6-8:** Constant pressure (1-2s gaps)
- **Levels 9-10:** Relentless assault (0.5-1s gaps)

**Power Curve Alignment:**
- Player should reach tier 3-4 weapons by level 3
- Tier 5-6 weapons by level 6
- Max tier (8) achievable by level 8 (if skilled)
- Levels 9-10 assume player has max weapons

**Checkpoint System:**
- Checkpoint every 60 seconds within a level
- Death returns player to last checkpoint
- Boss fights have checkpoint immediately before boss warning

---

## Research Sources

This research compiled information from the following sources:

### Raiden Series Mechanics
- [Raiden Wiki - Raiden IV](https://raiden.fandom.com/wiki/Raiden_IV)
- [Raiden Wiki - Main Series](https://raiden.fandom.com/wiki/Raiden)
- [Shmups Wiki - Raiden](https://shmups.wiki/library/Raiden)
- [Shmups Wiki - Raiden II](https://shmups.wiki/library/Raiden_II)
- [StrategyWiki - Raiden Power-ups](https://strategywiki.org/wiki/Raiden/Power-ups)

### Boss Mechanics and Patterns
- [Indie Retro News - ChromaBlast](https://www.indieretronews.com/2026/03/chromablast-cute-vertical-scrolling.html)
- [Chaotik Blog - Shoot'em Up Mechanics](https://chaotik.co.za/shootem-up-mechanics/)
- [Wikipedia - Shoot 'em up](https://en.wikipedia.org/wiki/Shoot_'em_up)
- [Shmups Wiki - Glossary](https://shmups.wiki/library/Help:Glossary)

### Scoring Systems
- [SHMUP Creator - Scoring Systems](https://www.shmupcreator.com/doc/?docs=shmupcreator/making-a-game/scoring-systems)
- [Arcade Otaku Forum - Scoring Discussion](https://forum.arcadeotaku.com/viewtopic.php?t=847)
- [Fat Pug Studio - Scoring System Design](https://www.fatpugstudio.com/dev-log/scoring-system-design/)
- [AzorMX Gaming - Blazing Star Analysis](https://www.azormx.com/azormx/greatest-shmup-of-them-all/the-search-for-the-greatest-shmup-episode-21-blazing-star/)

### General Shmup Design
- [TV Tropes - Raiden NOVA](https://tvtropes.org/pmwiki/pmwiki.php/VideoGame/RaidenNova)
- [Slant - Best Vertical Shmups 2026](https://www.slant.co/topics/16498/~vertically-scrolling-shoot-em-up-games-on-pc)

---

## Implementation Recommendations

### Priority 1: Core Loop (MVP)
1. Implement basic enemy types (scouts, bombers, drones)
2. Implement tier 1-3 weapons (single, twin, vulcan)
3. Implement first 3 levels with simple bosses
4. Basic scoring (no combos yet)

### Priority 2: Progression Systems
1. Full weapon progression (tiers 1-8)
2. Power-up collection and cycling
3. Combo multiplier system
4. All 10 enemy types

### Priority 3: Boss Battles
1. Multi-phase boss system
2. Weak point mechanics
3. Boss warning system
4. All 10 bosses

### Priority 4: Polish
1. Difficulty scaling implementation
2. Bonus scoring (no-death, perfect clear, etc.)
3. High score persistence
4. Audio/visual feedback (screen flash, floating numbers)

### Priority 5: Replayability
1. Hardcore mode
2. Leaderboards
3. Speed run timers
4. Grazing mechanics
