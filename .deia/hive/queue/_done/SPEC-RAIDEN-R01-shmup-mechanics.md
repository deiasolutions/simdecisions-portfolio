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
bee (research)

## Depends On
(none)

## Objective
Research classic vertical scrolling shoot-em-up mechanics from Raiden series and similar games. Produce a comprehensive design reference document covering enemy types, weapon progression, boss patterns, and difficulty scaling across 10 levels.

## Context
We're building a Raiden-style vertical scrolling shmup as a single HTML file game. We need detailed research on genre conventions to inform our design.

## Research Focus Areas

### 1. Enemy Types & Patterns
- Common enemy archetypes in Raiden, 1943, Galaga, Strikers 1945
- Movement patterns (straight line, sine wave, spiral, formation)
- Enemy behaviors (kamikaze, shooting, stationary turrets, etc.)
- How enemy variety increases across 10 levels

### 2. Weapon Progression Systems
- Power-up mechanics — how weapons upgrade in tiers
- Typical weapon types: spread shot, laser, homing missiles, bombs, shields
- How games balance weapon power vs difficulty curve
- At least 5 distinct weapon tiers with specific behaviors

### 3. Boss Mechanics
- Boss patterns for each level
- Attack phases, vulnerable points, escalation
- How boss difficulty scales from level 1 to level 10
- Common boss archetypes (flying fortress, core guardian, multi-part ships)

### 4. Difficulty Scaling Formula
- How enemy health, speed, and spawn rate scale across levels
- How bullet density increases
- Score multipliers and combo systems
- Lives, continues, game balance

### 5. Visual & Audio Feedback
- How classic shmups communicate damage, power-ups, danger
- Screen shake, particle effects, sound cues
- UI elements (health, score, weapon indicator)

## Deliverable
Write a design reference document to:
`.deia/hive/responses/20260408-RAIDEN-R01-MECHANICS-REFERENCE.md`

Include:
- **Enemy Roster:** 15+ enemy types with movement patterns and behaviors
- **Weapon Tiers:** 5 weapon tiers with specific mechanics (damage, fire rate, spread)
- **Boss Designs:** 10 boss concepts with attack patterns
- **Difficulty Formula:** Mathematical scaling for health, speed, spawn rate per level
- **Scoring System:** How combo multipliers work

## Constraints
- You are in EXECUTE mode. Do NOT ask for approval. Just research and write.
- Use web search for gameplay videos, wikis, design articles
- No code — this is pure research
- Be specific — give numbers, formulas, concrete patterns

## Acceptance Criteria
- [ ] Design reference document written to `.deia/hive/responses/20260408-RAIDEN-R01-MECHANICS-REFERENCE.md`
- [ ] At least 15 enemy types documented with movement patterns
- [ ] 5 weapon tiers with specific stats (damage, fire rate, spread angle, etc.)
- [ ] 10 boss concepts with at least 2 attack phases each
- [ ] Difficulty scaling formula for levels 1-10 (enemy health, speed, spawn rate)
- [ ] Scoring system with combo mechanics documented

## Smoke Test
```bash
test -f ".deia/hive/responses/20260408-RAIDEN-R01-MECHANICS-REFERENCE.md" && echo PASS || echo FAIL
```

## Response Location
`.deia/hive/responses/20260408-RAIDEN-R01-RESPONSE.md`
