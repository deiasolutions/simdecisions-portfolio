# TRIAGE ESCALATION: GAMIFICATION-V1

**Date:** 2026-04-10 03:34:28 UTC
**Reason:** 3 requeue attempts (max 3)
**Status:** NEEDS MANUAL REVIEW

## Summary

Spec `SPEC-GAMIFICATION-V1.md` has been requeued 3 times and failed each time.
Automated triage has moved it to `_escalated/` for manual review.

## Triage History

- 2026-04-09T15:50:45.759461Z — requeued (empty output)
- 2026-04-09T15:55:45.818578Z — requeued (empty output)
- 2026-04-10T03:29:28.676531Z — requeued (empty output)

## Next Steps

1. **Review spec file** in `queue/_escalated/SPEC-GAMIFICATION-V1.md`
2. **Diagnose root cause** — why is this spec failing repeatedly?
3. **Options:**
   - Fix spec and move back to backlog/
   - Archive spec if no longer needed
   - Break into smaller specs
   - Escalate to architect (Mr. AI) if systemic issue

## Original Spec

```markdown
## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

# ShiftCenter Gamification Specification

**Spec ID:** SPEC-GAMIFICATION-V1
**Created:** 2026-04-06
**Status:** DRAFT
**Depends On:** SPEC-EVENT-LEDGER-GAMIFICATION
**Related:** SPEC-ML-TRAINING-V1 (Pillar 3)
**Ships With:** V1.0
**Pillar:** 2 of 3 (Core App, **Gamification**, AI Training)

---

## Executive Summary

Gamification keeps the human-in-the-loop engaged. Every action in ShiftCenter — approving tasks, writing docs, reviewing code — earns XP, unlocks badges, and builds progression.

### Core Principle

> To learn is to grow. To grow is to live.
> ABCDG: Always Be Collecting Data for Gamification.

The Event Ledger captures everything. Gamification scores it. What we measure, we improve.

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Event Ledger                                   │
│  Every action emits an event: tasks, wiki edits, reviews, deploys       │
└─────────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         XP Calculator                                    │
│  Event → Scoring Rules → xp_delta                                       │
│  Rules can change. History doesn't. Replay anytime.                     │
└─────────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Badge Engine                                      │
│  Pattern matching on event history                                       │
│  Badges added anytime — history is there                                │
└─────────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      Progression State                                   │
│  user_progression table + progression.md wiki page                      │
│  RTD emission: {metric_key: "xp", value: 4250}                         │
└─────────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Dashboard Widget                                  │
│  XP bar, level, recent badges, streak counter                           │
│  Morning report includes overnight XP earned                            │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Database Schema

### 2.1 User Progression Table

```sql
CREATE TABLE user_progression (
    user_id UUID PRIMARY KEY REFERENCES users(id),
    
    -- Core metrics
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    
    -- Streak tracking
    streak_days INTEGER DEFAULT 0,
    streak_last_date DATE,
    streak_longest INTEGER DEFAULT 0,
    
    -- Badges (array of badge IDs)
    badges JSONB DEFAULT '[]',
    
    -- Stats (lifetime counters)
    stats JSONB DEFAULT '{
        "tasks_approved": 0,
        "tasks_rejected": 0,
        "wiki_pages_created": 0,
        "wiki_pages_edited": 0,
        "notebooks_run": 0,
        "eggs_packed": 0,
        "reviews_completed": 0,
        "specs_written": 0,
        "deploys_completed": 0
    }',
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 2.2 XP Events Table

```sql
CREATE TABLE xp_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    user_id UUID REFERENCES users(id),
    
    -- Event reference
    event_kind VARCHAR(100) NOT NULL,
    source_event_id UUID,                  -- Links to Event Ledger
    source_id UUID,                        -- task_id, page_id, etc.
    
    -- XP calculation
    xp_delta INTEGER NOT NULL,
    xp_reason VARCHAR(255),                -- Human-readable explanation
    
    -- Multipliers applied
    multipliers JSONB DEFAULT '{}',        -- {"streak": 1.5, "first_of_day": 2.0}
    
    -- Timestamp
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_xp_events_user ON xp_events(user_id);
CREATE INDEX idx_xp_events_time ON xp_events(created_at DESC);
CREATE INDEX idx_xp_events_kind ON xp_events(event_kind);
```

### 2.3 Badges Table

```sql
CREATE TABLE badge_definitions (
    id VARCHAR(50) PRIMARY KEY,            -- 'first_blood', 'streak_7', etc.
    
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    icon VARCHAR(50),                      -- emoji or icon name
    
    -- Trigger definition
    trigger_type VARCHAR(50) NOT NULL,     -- 'event_count', 'streak', 'pattern', 'manual'
    trigger_config JSONB NOT NULL,         -- Type-specific config
    
    -- Rarity
    rarity VARCHAR(20) DEFAULT 'common',   -- common, uncommon, rare, epic, legendary
    xp_bonus INTEGER DEFAULT 0,            -- One-time XP award on earn
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE badge_awards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    user_id UUID REFERENCES users(id),
    badge_id VARCHAR(50) REFERENCES badge_definitions(id),
    
    -- Context
    earned_at TIMESTAMPTZ DEFAULT NOW(),
    trigger_event_id UUID,                 -- Event that triggered the badge
    
    UNIQUE(user_id, badge_id)
);

CREATE INDEX idx_badge_awards_user ON badge_awards(user_id);
```

---

## 3. XP Scoring Rules

### 3.1 Base XP Values

| Event Kind | Base XP | Notes |
|------------|---------|-------|
| **Tasks** | | |
| TASK_APPROVED | +10 | Approved a queued task |
| TASK_REJECTED | +5 | Rejected with feedback |
| TASK_COMPLETED | +25 | Task finished successfully |
| TASK_DISPATCHED | +2 | Sent task to queue |
| **Wiki** | | |
| PAGE_CREATED | +15 | New wiki page |
| PAGE_UPDATED | +5 | Edited existing page |
| PAGE_LINKED | +5 | Per new inbound link |
| **Notebooks** | | |
| NOTEBOOK_RUN | +2 | Executed cell(s) |
| NOTEBOOK_EXPORTED | +10 | Generated export |
| **Eggs** | | |
| EGG_PACKED | +25 | Created an egg |
| EGG_INFLATED | +5 | Extracted an egg |
| **Reviews** | | |
| REVIEW_COMPLETED | +15 | Finished code review |
| BUG_CAUGHT | +50 | Found bug before deploy |
| **Specs** | | |
| SPEC_WRITTEN | +30 | New spec document |
| SPEC_SHIPPED | +100 | Spec → deployed |
| **Deploys** | | |
| DEPLOY_COMPLETED | +20 | Successful deployment |
| ROLLBACK_EXECUTED | +10 | Quick recovery |
| **Efficiency** | | |
| UNDER_BUDGET_CLOCK | +15 | Task under time estimate |
| UNDER_BUDGET_COIN | +15 | Task under cost estimate |
| UNDER_BUDGET_CARBON | +15 | Task under carbon estimate |

### 3.2 Multipliers

| Condition | Multiplier | Stacks |
|-----------|------------|--------|
| First action of the day | 2.0x | No |
| Streak active (3+ days) | 1.25x | Yes |
| Streak active (7+ days) | 1.5x | Yes |
| Streak active (30+ days) | 2.0x | Yes |
| Night shift (10pm-6am) | 1.25x | Yes |
| Weekend | 1.1x | Yes |

### 3.3 XP Calculation

```python
def calculate_xp(event: Event, user: UserProgression) -> XPEvent:
    base_xp = XP_TABLE.get(event.kind, 0)
    
    multipliers = {}
    total_multiplier = 1.0
    
    # First action of day
    if is_first_action_today(user, event.timestamp):
        multipliers['first_of_day'] = 2.0
        total_multiplier *= 2.0
    
    # Streak bonus
    if user.streak_days >= 30:
        multipliers['streak_30'] = 2.0
        total_multiplier *= 2.0
    elif user.streak_days >= 7:
        multipliers['streak_7'] = 1.5
        total_multiplier *= 1.5
    elif user.streak_days >= 3:
        multipliers['streak_3'] = 1.25
        total_multiplier *= 1.25
    
    # Time-based
    hour = event.timestamp.hour
    if hour >= 22 or hour < 6:
        multipliers['night_owl'] = 1.25
        total_multiplier *= 1.25
    
    if event.timestamp.weekday() >= 5:
        multipliers['weekend'] = 1.1
        total_multiplier *= 1.1
    
    xp_delta = int(base_xp * total_multiplier)
    
    return XPEvent(
        user_id=user.user_id,
        event_kind=event.kind,
        source_event_id=event.id,
        xp_delta=xp_delta,
        multipliers=multipliers
    )
```

---

## 4. Level System

### 4.1 Level Thresholds

| Level | XP Required | Title | Cumulative |
|-------|-------------|-------|------------|
| 1 | 0 | Drone | 0 |
| 2 | 100 | Worker | 100 |
| 3 | 300 | Builder | 400 |
| 4 | 600 | Architect | 1,000 |
| 5 | 1,000 | Engineer | 2,000 |
| 6 | 1,500 | Artisan | 3,500 |
| 7 | 2,500 | Master | 6,000 |
| 8 | 4,000 | Queen's Hand | 10,000 |
| 9 | 6,000 | Hive Lord | 16,000 |
| 10 | 10,000 | Sovereign | 26,000 |

### 4.2 Level Calculation

```python
LEVEL_THRESHOLDS = [0, 100, 400, 1000, 2000, 3500, 6000, 10000, 16000, 26000]

def calculate_level(xp: int) -> int:
    for level, threshold in enumerate(LEVEL_THRESHOLDS):
        if xp < threshold:
            return level
    return len(LEVEL_THRESHOLDS)

def xp_to_next_level(xp: int) -> int:
    level = calculate_level(xp)
    if level >= len(LEVEL_THRESHOLDS):
        return 0
    return LEVEL_THRESHOLDS[level] - xp
```

---

## 5. Badge System

### 5.1 Starter Badges

| Badge ID | Name | Trigger | Rarity | XP Bonus |
|----------|------|---------|--------|----------|
| `first_blood` | First Blood | First task approved | Common | +25 |
| `hello_wiki` | Hello Wiki | First wiki page created | Common | +25 |
| `notebook_curious` | Notebook Curious | First notebook run | Common | +15 |

### 5.2 Streak Badges

| Badge ID | Name | Trigger | Rarity | XP Bonus |
|----------|------|---------|--------|----------|
| `streak_3` | Warming Up | 3-day streak | Common | +25 |
| `streak_7` | On Fire | 7-day streak | Uncommon | +50 |
| `streak_14` | Dedicated | 14-day streak | Rare | +100 |
| `streak_30` | Unstoppable | 30-day streak | Epic | +250 |
| `streak_100` | Legendary | 100-day streak | Legendary | +1000 |

### 5.3 Volume Badges

| Badge ID | Name | Trigger | Rarity | XP Bonus |
|----------|------|---------|--------|----------|
| `tasks_10` | Task Tackler | 10 tasks approved | Common | +25 |
| `tasks_50` | Task Master | 50 tasks approved | Uncommon | +75 |
| `tasks_100` | Task Lord | 100 tasks approved | Rare | +150 |
| `wiki_10` | Doc Writer | 10 wiki pages | Uncommon | +50 |
| `wiki_50` | Knowledge Keeper | 50 wiki pages | Rare | +150 |
| `backlinks_10` | Graph Weaver | Page with 10+ backlinks | Rare | +100 |

### 5.4 Skill Badges

| Badge ID | Name | Trigger | Rarity | XP Bonus |
|----------|------|---------|--------|----------|
| `bug_hunter` | Bug Hunter | First bug caught in review | Uncommon | +75 |
| `bug_slayer` | Bug Slayer | 10 bugs caught | Rare | +200 |
| `ship_it` | Ship It | Spec → deployed in <48h | Rare | +150 |
| `speed_demon` | Speed Demon | 5 tasks under time budget | Uncommon | +75 |
| `budget_hawk` | Budget Hawk | Week under budget (all 3 currencies) | Rare | +200 |

### 5.5 Time Badges

| Badge ID | Name | Trigger | Rarity | XP Bonus |
|----------|------|---------|--------|----------|
| `night_owl` | Night Owl | Task approved after midnight | Common | +15 |
| `early_bird` | Early Bird | Task approved before 6am | Common | +15 |
| `weekend_warrior` | Weekend Warrior | 10 weekend actions | Uncommon | +50 |

### 5.6 Badge Trigger Config

```yaml
# Example badge definitions

first_blood:
  name: "First Blood"
  description: "Approved your first task"
  icon: "🩸"
  trigger_type: event_count
  trigger_config:
    event_kind: TASK_APPROVED
    count: 1
  rarity: common
  xp_bonus: 25

streak_7:
  name: "On Fire"
  description: "Maintained a 7-day streak"
  icon: "🔥"
  trigger_type: streak
  trigger_config:
    days: 7
  rarity: uncommon
  xp_bonus: 50

bug_hunter:
  name: "Bug Hunter"
  description: "Caught a bug before it shipped"
  icon: "🐛"
  trigger_type: event_count
  trigger_config:
    event_kind: BUG_CAUGHT
    count: 1
  rarity: uncommon
  xp_bonus: 75

backlinks_10:
  name: "Graph Weaver"
  description: "Created a wiki page with 10+ inbound links"
  icon: "🕸️"
  trigger_type: wiki_metric
  trigger_config:
    metric: backlink_count
    threshold: 10
  rarity: rare
  xp_bonus: 100
```

---

## 6. Four Factors: ρ-π-σ-τ Profile

### 6.1 The Four Factors

Every user has a Four-Vector profile that describes *how* they work:

| Factor | Symbol | What It Measures |
|--------|--------|------------------|
| **Rho (ρ)** | ρ | **Reliability** — Consistency, follow-through, streak maintenance |
| **Pi (π)** | π | **Productivity** — Output volume, task completion, artifacts created |
| **Sigma (σ)** | σ | **Sophistication** — Complexity handled, architecture decisions, edge cases |
| **Tau (τ)** | τ | **Teaching** — Knowledge shared, docs written, others helped |

### 6.2 Factor Scoring

| Event Pattern | ρ | π | σ | τ |
|---------------|---|---|---|---|
| Streak maintained | +3 | | | |
| Consecutive days active | +2 | | | |
| Task completed on time | +1 | | | |
| Task completed | | +2 | | |
| Page created | | +2 | | |
| Artifact shipped | | +3 | | |
| ADR written | | | +4 | |
| Complex spec completed | | | +5 | |
| Edge case handled | | | +3 | |
| Wiki page with 5+ backlinks | | | | +4 |
| Tutorial/runbook created | | | | +3 |
| Doc helps another user | | | | +5 |

### 6.3 Factor Schema

```sql
CREATE TABLE user_factors (
    user_id UUID PRIMARY KEY REFERENCES users(id),
    
    -- ρ-π-σ-τ Profile (raw scores)
    factor_rho INTEGER DEFAULT 0,
    factor_pi INTEGER DEFAULT 0,
    factor_sigma INTEGER DEFAULT 0,
    factor_tau INTEGER DEFAULT 0,
    
    -- Normalized (0-100 scale)
    rho_normalized INTEGER GENERATED ALWAYS AS (
        LEAST(100, factor_rho / 10)
    ) STORED,
    pi_normalized INTEGER GENERATED ALWAYS AS (
        LEAST(100, factor_pi / 10)
    ) STORED,
    sigma_normalized INTEGER GENERATED ALWAYS AS (
        LEAST(100, factor_sigma / 10)
    ) STORED,
    tau_normalized INTEGER GENERATED ALWAYS AS (
        LEAST(100, factor_tau / 10)
    ) STORED,
    
    -- Derived
    primary_factor VARCHAR(10) GENERATED ALWAYS AS (
        CASE GREATEST(factor_rho, factor_pi, factor_sigma, factor_tau)
            WHEN factor_rho THEN 'rho'
            WHEN factor_pi THEN 'pi'
            WHEN factor_sigma THEN 'sigma'
            WHEN factor_tau THEN 'tau'
        END
    ) STORED,
    
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 6.4 Factor Visualization

```
         τ (Teaching)
            ▲
            │
     ╭──────┼──────╮
    ╱       │       ╲
   ╱        │        ╲
ρ ◄─────────┼─────────► π
(Reliable)  │         (Productive)
   ╲        │        ╱
    ╲       │       ╱
     ╰──────┼──────╯
            │
            ▼
         σ (Sophisticated)

You: ρ 78 | π 62 | σ 45 | τ 31
```

Diamond/radar chart. Shape = identity. Shape = data for ML models.

### 6.5 Factors Feed ML

Per SPEC-ML-TRAINING-V1, every model can use factors as features:

```python
{
    "rho": 78,
    "pi": 62,
    "sigma": 45,
    "tau": 31,
    "primary_factor": "rho",
    "factor_balance": 0.72,      # Specialist vs generalist
    "factor_velocity": 2.3       # Growth rate
}
```

---

## 7. Path Map System

### 7.1 Path Map Concept

Visual progression like Duolingo. Users see:
- Completed nodes behind them (filled)
- Current position (glowing)
- Visible-but-locked nodes ahead (grayed)
- Hidden nodes (fog of war until prerequisites met)

### 7.2 Skill Nodes

```sql
CREATE TABLE skill_nodes (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    
    -- Position in path
    path_id VARCHAR(50),                -- 'builder', 'operator', 'architect'
    position_x INTEGER,
    position_y INTEGER,
    
    -- Unlock requirements
    requirements JSONB DEFAULT '{}',    -- {"xp": 500, "badges": ["first_blood"]}
    
    -- What it grants
    grants JSONB DEFAULT '{}',          -- {"feature": "parallel_dispatch", "xp_bonus": 50}
    
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE user_skills (
    user_id UUID REFERENCES users(id),
    skill_id VARCHAR(50) REFERENCES skill_nodes(id),
    
    unlocked_at TIMESTAMPTZ DEFAULT NOW(),
    times_used INTEGER DEFAULT 0,
    
    PRIMARY KEY (user_id, skill_id)
);
```

### 7.3 Example Path Structure

```
[Start]
   │
   ▼
[First Task] ──────────────────────┐
   │                               │
   ▼                               ▼
[Wiki Basics] ──► [Notebook 101]  [Review Basics]
   │                    │              │
   ▼                    ▼              ▼
[Wikilinks]        [Export Code]   [Bug Hunter] 🔓
   │                    │              │
   ▼                    ▼              ▼
[Backlinks]        [Egg Packing]   [QA Master]
   │                    │              │
   └────────┬───────────┘              │
            ▼                          │
      [Knowledge Architect] ◄──────────┘
            │
            ▼
      [Hive Lord]
```

### 7.4 Path Responds to ρ-π-σ-τ

Your Four-Vector shapes what glows:

- High-ρ users see streak-related nodes brightest
- High-π users see volume achievements emphasized
- High-σ users see architecture/complexity nodes
- High-τ users see teaching/documentation nodes

The map responds to who you are, not just what you've done.

### 7.5 Skill Discovery Events

```json
{
  "kind": "SKILL_UNLOCKED",
  "context": {
    "skill_id": "egg_packing",
    "skill_name": "Egg Packing",
    "requirements_met": {
      "wiki_pages": 5,
      "notebooks": 3
    },
    "grants": {
      "feature": "egg_pack_command",
      "xp_bonus": 50
    }
  }
}
```

### 7.6 Path Map Component

```
primitives/gamification/
├── PathMap.tsx              # Main path visualization
├── PathNode.tsx             # Individual skill node
├── PathEdge.tsx             # Connection between nodes
├── SkillUnlock.tsx          # Unlock animation/modal
└── PathProgress.tsx         # "You are here" indicator
```

---

## 8. Progression Wiki Page

Auto-generated at `.wiki/meta/progression.md`:

```markdown
---
title: Progression
page_type: meta
auto_generated: true
last_updated: 2026-04-06T14:30:00Z
---

# Progression

## Current Status

**Level:** 5 — Engineer
**XP:** 2,450 / 3,500 (70% to Artisan)
**Streak:** 12 days 🔥

## Recent XP

| Date | Event | XP |
|------|-------|-----|
| Today | TASK_APPROVED × 3 | +60 |
| Today | PAGE_CREATED | +30 (2x first of day) |
| Yesterday | SPEC_SHIPPED | +100 |
| Yesterday | REVIEW_COMPLETED × 2 | +30 |

## Badges Earned

- 🩸 **First Blood** — 2026-03-01
- 📝 **Hello Wiki** — 2026-03-02
- 🔥 **On Fire** (7-day streak) — 2026-03-08
- 🛠️ **Task Tackler** (10 tasks) — 2026-03-15
- 🚀 **Ship It** (<48h spec→deploy) — 2026-04-01

## Stats

- Tasks approved: 47
- Wiki pages created: 12
- Notebooks run: 28
- Specs written: 5
- Bugs caught: 2

## Next Goals

- [ ] Reach Level 6 (1,050 XP needed)
- [ ] Earn "Dedicated" badge (2 more streak days)
- [ ] Earn "Doc Writer" badge (8 more wiki pages)
```

---

## 9. Dashboard Widget

### 7.1 Component Structure

```
primitives/gamification/
├── ProgressionWidget.tsx       # Main dashboard widget
├── XPBar.tsx                   # Progress bar to next level
├── BadgeDisplay.tsx            # Badge grid/list
├── StreakCounter.tsx           # Current streak display
├── RecentXP.tsx                # Recent XP events
└── hooks/
    ├── useProgression.ts
    └── useBadges.ts
```

### 7.2 Widget Display

```
┌─────────────────────────────────────────┐
│  Level 5 — Engineer                     │
│  ████████████████░░░░░░░░  2,450 / 3,500│
│                                         │
│  🔥 12-day streak                       │
│                                         │
│  Recent: +60 XP today                   │
│                                         │
│  Badges: 🩸 📝 🔥 🛠️ 🚀               │
└─────────────────────────────────────────┘
```

### 7.3 RTD Emissions

```json
{
  "service_id": "gamification",
  "metric_key": "xp",
  "value": 2450,
  "unit": "points",
  "timestamp": "2026-04-06T14:30:00Z"
}

{
  "service_id": "gamification",
  "metric_key": "level",
  "value": 5,
  "unit": "level",
  "timestamp": "2026-04-06T14:30:00Z"
}

{
  "service_id": "gamification",
  "metric_key": "streak",
  "value": 12,
  "unit": "days",
  "timestamp": "2026-04-06T14:30:00Z"
}
```

---

## 10. Morning Report Integration

The morning report (per factory spec) includes gamification summary:

```markdown
## Overnight Gamification

**XP Earned:** +245
**New Level:** No (2,450 / 3,500)
**Streak:** 12 days (maintained ✓)

**Badges Unlocked:**
- None overnight

**Leaderboard Position:** #1 (you're alone, but still winning)
```

---

## 11. API Endpoints

```
GET    /api/gamification/progression          # Current state
GET    /api/gamification/xp-history           # Recent XP events
GET    /api/gamification/badges               # All badges + earned status
GET    /api/gamification/leaderboard          # Multi-user (future)
POST   /api/gamification/recalculate          # Replay all events (admin)
```

---

## 12. Event Processing

### 10.1 Event Consumer

```python
class GamificationConsumer:
    """
    Consumes events from Event Ledger, calculates XP, awards badges.
    """
    
    async def process_event(self, event: LedgerEvent):
        # 1. Calculate XP
        xp_event = self.xp_calculator.calculate(event)
        
        if xp_event.xp_delta > 0:
            # 2. Record XP event
            await self.db.insert(xp_event)
            
            # 3. Update progression
            await self.update_progression(event.actor_id, xp_event)
            
            # 4. Check badges
            new_badges = await self.badge_engine.check(event.actor_id)
            for badge in new_badges:
                await self.award_badge(event.actor_id, badge)
            
            # 5. Emit RTD
            await self.emit_rtd(event.actor_id)
            
            # 6. Update progression.md
            await self.update_wiki_page(event.actor_id)
```

### 10.2 Streak Management

```python
async def update_streak(self, user_id: UUID, event_date: date):
    prog = await self.get_progression(user_id)
    
    if prog.streak_last_date == event_date:
        # Already logged today
        return
    
    if prog.streak_last_date == event_date - timedelta(days=1):
        # Consecutive day — extend streak
        prog.streak_days += 1
        prog.streak_longest = max(prog.streak_longest, prog.streak_days)
    else:
        # Streak broken — reset
        prog.streak_days = 1
    
    prog.streak_last_date = event_date
    await self.save_progression(prog)
```

---

## 13. Acceptance Criteria

### 11.1 XP System

- [ ] Events from ledger calculate XP correctly
- [ ] Multipliers apply (streak, first-of-day, time-based)
- [ ] XP events stored with full context
- [ ] Progression updates in real-time

### 11.2 Levels

- [ ] Level calculated from XP thresholds
- [ ] Level-up emits notification
- [ ] Progress bar shows XP to next level

### 11.3 Badges

- [ ] Badge definitions stored in database
- [ ] Badges awarded on trigger match
- [ ] Badge award is one-time (no duplicates)
- [ ] XP bonus applied on badge earn

### 11.4 Streaks

- [ ] Streak increments on consecutive days
- [ ] Streak resets after missed day
- [ ] Longest streak tracked
- [ ] Streak badges awarded at thresholds

### 11.5 Display

- [ ] Dashboard widget shows current state
- [ ] RTD emissions on state change
- [ ] progression.md auto-updated
- [ ] Morning report includes gamification

---

## 14. Future Enhancements (V2+)

- **Leaderboards** — Multi-user competition (when ShiftCenter has teams)
- **Challenges** — Time-limited objectives with bonus XP
- **Unlocks** — Features gated by progression (e.g., "Level 5 unlocks Opus")
- **Cosmetics** — Custom themes, avatars based on level/badges
- **Seasons** — Quarterly resets with prestige tracking

---

**Spec Version:** 1.0
**Author:** Q88N × Claude
**Review Required:** Ideation on badges continues; spec covers structure

## Triage History
- 2026-04-09T15:50:45.759461Z — requeued (empty output)
- 2026-04-09T15:55:45.818578Z — requeued (empty output)
- 2026-04-10T03:29:28.676531Z — requeued (empty output)

```

---

**Automated escalation by triage daemon**
