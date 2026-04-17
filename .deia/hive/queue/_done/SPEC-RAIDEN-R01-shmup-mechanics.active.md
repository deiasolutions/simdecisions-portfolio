---
id: RAIDEN-R01
priority: P1
model: sonnet
role: bee
depends_on: []
---
# SPEC-RAIDEN-R01: Shmup Mechanics Research

## Priority
P1

## Model Assignment
sonnet

## Role
bee (b33 — you research and document findings)

## Depends On
(none)

## Objective
Research classic vertical scrolling shoot-em-up mechanics from Raiden series and similar games to inform our game design.

## You are in EXECUTE mode
Write all research and documentation. Do NOT enter plan mode. Do NOT ask for approval. Just research and document.

## Research Scope

### 1. Enemy Types and Patterns
Research and document:
- Common enemy archetypes in Raiden/1943/Galaga (scouts, heavies, kamikaze, formations, etc.)
- Attack patterns (straight line, sine wave, figure-8, spiral, diving, etc.)
- Formation behaviors (V-formation, echelon, pincer, swarm)
- Enemy health/hit points progression across difficulty levels
- Specific examples from Raiden I and II

### 2. Weapon Progression Systems
Research and document:
- Weapon tier systems (how many tiers? what differentiates them?)
- Specific weapon types:
  - Single shot variations
  - Spread shot (angles, bullet count)
  - Laser/beam weapons
  - Homing missiles
  - Bombs/screen-clear weapons
  - Shields/defensive power-ups
- Power-up collection mechanics (drop rates, stacking, loss on death)
- Typical progression: what order do players acquire weapons?

### 3. Boss Fight Mechanics
Research and document:
- Boss health scaling (relative to level difficulty)
- Attack pattern phases (how many phases per boss? what triggers phase changes?)
- Weak point mechanics (specific hitboxes vs full-body damage)
- Warning systems (screen shake, music change, warning text)
- Specific boss examples from Raiden that work well

### 4. Difficulty Scaling Formula
Research and document:
- How enemy count increases across 10 levels
- How enemy speed/aggression scales
- How enemy health scales
- How spawn frequency changes
- Early game vs mid-game vs end-game pacing
- Specific difficulty curve recommendations for casual vs hardcore players

### 5. Scoring Systems
Research and document:
- Base score values for enemy types
- Combo multiplier mechanics (how do combos build? how long do they last?)
- Bonus scoring (no-death bonus, time bonus, perfect clear)
- Score display and feedback (floating numbers, screen flash, audio cues)
- High score persistence

## Deliverables

### File: `.deia/hive/responses/20260413-RAIDEN-R01-MECHANICS-RESEARCH.md`

Structure:
```markdown
# Raiden-Style Shmup Mechanics Research

## 1. Enemy Roster (10 types minimum)
| Enemy Type | HP | Speed | Attack Pattern | Spawn Level | Score Value |
|------------|----|----|----------------|-------------|-------------|
| Scout | 1 | fast | straight | 1+ | 100 |
| ... | ... | ... | ... | ... | ... |

## 2. Weapon Progression (5 tiers minimum)
| Tier | Weapon Name | Damage | Fire Rate | Special Effect | Visual |
|------|-------------|--------|-----------|----------------|--------|
| 1 | Single Shot | 1 | 200ms | none | white bullet |
| ... | ... | ... | ... | ... | ... |

## 3. Boss Mechanics (10 bosses, one per level)
| Level | Boss Name | HP | Phases | Attack Patterns | Weak Points |
|-------|-----------|----|----|-----------------|-------------|
| 1 | ... | ... | 2 | straight bullets, dive | center core |
| ... | ... | ... | ... | ... | ... |

## 4. Difficulty Scaling Formula
- **Enemy Count:** level * 8 + base(20)
- **Enemy Speed:** 1.0 + (level * 0.15)
- **Enemy HP:** base_hp * (1 + level * 0.25)
- **Spawn Frequency:** max(500ms - level*30ms, 200ms)

## 5. Scoring System
- **Base Scores:** scout=100, heavy=500, boss=10000
- **Combo Multiplier:** +0.1x per kill within 2 seconds, max 5x
- **Bonus Scoring:** no-death=50000, perfect-level=10000

## 6. Recommended Game Flow (10 levels)
| Level | Theme | Enemy Mix | Boss Type | Difficulty Spike |
|-------|-------|-----------|-----------|------------------|
| 1 | Tutorial | scouts only | simple turret | gentle |
| ... | ... | ... | ... | ... |
```

## Acceptance Criteria
- [ ] At least 10 distinct enemy types documented with stats
- [ ] At least 5 weapon tiers with specific mechanics
- [ ] 10 boss designs with phase mechanics
- [ ] Mathematical difficulty scaling formula provided
- [ ] Scoring system with combo mechanics defined
- [ ] All data tables complete (no TBD, no placeholders)

## Smoke Test
```bash
test -f ".deia/hive/responses/20260413-RAIDEN-R01-MECHANICS-RESEARCH.md" && \
grep -q "Enemy Roster" ".deia/hive/responses/20260413-RAIDEN-R01-MECHANICS-RESEARCH.md" && \
grep -q "Weapon Progression" ".deia/hive/responses/20260413-RAIDEN-R01-MECHANICS-RESEARCH.md" && \
echo "PASS"
```

## Response Location
`.deia/hive/responses/20260413-RAIDEN-R01-MECHANICS-RESEARCH-RESPONSE.md`
