# SPEC-GAMIFY-01: Progression Tables and XP Foundation

## Priority
P1

## Model Assignment
haiku

## Depends On
LEDGER-01

## Intent
Create the database schema for user progression (XP, levels, badges, stats) and implement basic XP calculation from event kinds. This is the foundation layer - storage and calculation only, no event consumption pipeline yet.

## Files to Read First
.deia/BOOT.md
hivenode/main.py

## Acceptance Criteria
- [ ] `user_progression` table created with fields: user_id, xp, level, streak_days, streak_last_date, streak_longest, badges (JSONB), stats (JSONB), created_at, updated_at
- [ ] `xp_events` table created with fields: id, user_id, event_kind, source_event_id, xp_delta, xp_reason, multipliers (JSONB), created_at
- [ ] `badge_definitions` table created with fields: id, name, description, icon, trigger_type, trigger_config (JSONB), rarity, xp_bonus, is_active, created_at
- [ ] `badge_awards` table created with fields: id, user_id, badge_id, earned_at, trigger_event_id, UNIQUE(user_id, badge_id)
- [ ] All tables have proper indexes on user_id, timestamps, and lookup fields
- [ ] Level calculation function implemented using XP thresholds [0, 100, 400, 1000, 2000, 3500, 6000, 10000, 16000, 26000]
- [ ] Base XP lookup table implemented with at least 10 event kinds from spec
- [ ] XP calculation function implemented with multiplier support (first_of_day, streak, time_based)
- [ ] Migration script creates all tables idempotently (safe to run multiple times)
- [ ] At least 5 unit tests for XP calculation with various multipliers
- [ ] At least 3 unit tests for level calculation
- [ ] Schema compatible with both PostgreSQL and SQLite
- [ ] No file over 500 lines
- [ ] All SQL uses SQLAlchemy Core (not ORM)

## Constraints
- This spec implements ONLY schema and calculation functions
- Event consumption pipeline is NOT in scope
- Badge trigger checking is NOT in scope (just table definitions)
- Dashboard widgets are NOT in scope
- Use existing hivenode database patterns
- All file paths absolute
- No stubs - complete implementations
- No git operations

## Smoke Test
After completion:
1. Run migration to create tables
2. Manually insert a user_progression record
3. Call XP calculation function with event_kind="TASK_APPROVED" and verify base_xp=10
4. Call XP calculation with first_of_day multiplier and verify xp_delta=20
5. Calculate level from xp=500 and verify level=2
6. Query all tables to confirm schema matches spec
