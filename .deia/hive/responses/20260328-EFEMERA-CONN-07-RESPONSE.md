# SPEC-EFEMERA-CONN-07: Backend Schema Upgrade -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-28

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\store.py` (322 lines, +74 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\routes.py` (227 lines, +58 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_efemera_schema_upgrade.py` (385 lines, new file)

## What Was Done

**Schema Extensions:**
- Extended `channels` table with `description` (TEXT), `read_only` (BOOLEAN)
- Extended channel type enum from 2 to 13 types: added commons, announcements, the_buzz, the_window, dev, personal, moderation_log, bugs_admin, approvals, humans_only, bok_submissions
- Extended `messages` table with 13 new columns:
  - `version` (INTEGER, default 1)
  - `parent_id` (TEXT, for edit chains)
  - `reply_to_id` (TEXT, for threading)
  - `edited_at` (TEXT)
  - `author_type` (TEXT, enum: human/bot/agent/system, default 'human')
  - `message_type` (TEXT, enum: text/terminal_output/rag_answer/system, default 'text')
  - `moderation_status` (TEXT, enum: approved/held/blocked, default 'approved')
  - `moderation_reason` (TEXT)
  - `provider` (TEXT)
  - `metadata_json` (TEXT)
  - `topic_id` (TEXT)
  - `topic_name` (TEXT)

**Migration System:**
- Added `_migrate_schema()` method to EfemeraStore.__init__()
- Idempotent ALTER TABLE ADD COLUMN for all new columns
- Safe to run multiple times (catches OperationalError for existing columns)
- All new columns have defaults — backward compatible with existing data

**Store Methods Updated:**
- `create_channel()` — added optional params: `description`, `read_only`, `channel_id`
- `create_message()` — added optional params: `author_type`, `message_type`, `reply_to_id`, `moderation_status`, `moderation_reason`, `metadata_json`
- `get_message(message_id)` — new method, returns single message by ID
- `remove_member(channel_id, user_id)` — new method, removes member from channel

**Routes Updated:**
- Extended `CreateChannelRequest` schema with `description`, `read_only`, and 13-type pattern
- Extended `CreateMessageRequest` schema with `author_type`, `message_type`, `reply_to_id`, `metadata_json`
- Added `JoinChannelRequest` and `LeaveChannelRequest` schemas
- Added `POST /channels/{id}/join` endpoint
- Added `POST /channels/{id}/leave` endpoint
- Updated `create_channel` route to pass new params to store
- Updated `create_message` route to pass new params to store

**Tests:**
- Created comprehensive test file: `test_efemera_schema_upgrade.py` (385 lines, 21 tests)
- Tests cover:
  - Migration idempotency (run twice, no errors)
  - Channel creation with explicit channel_id
  - Channel creation with description and read_only
  - All 13 extended channel types accepted
  - Invalid channel type rejected
  - Message creation with author_type, message_type, reply_to_id, moderation_status, metadata_json
  - Message defaults (human, text, approved, version=1)
  - get_message() retrieval
  - Backward compatibility (existing data gets default values)
  - Join/leave channel endpoints
  - API validation for extended fields

## Tests

**New tests:** 21 tests, all passing
**Existing tests:** 29 tests, all passing
**Total efemera tests:** 50 tests, 0 failures

```
pytest tests/hivenode/test_efemera_schema_upgrade.py -v
======================== 21 passed, 1 warning in 0.90s ========================

pytest tests/hivenode/test_efemera.py -v
======================== 29 passed, 1 warning in 2.63s ========================

pytest tests/hivenode/test_efemera*.py -v
======================== 50 passed, 1 warning in 2.55s ========================
```

## Smoke Test

All smoke tests pass:
- Migration runs idempotently on existing database
- All existing tests pass (backward compatibility confirmed)
- New columns appear in schema after migration
- Channel type validation works for all 13 types
- Message creation with extended fields works
- Join/leave endpoints functional

## Line Counts

- `store.py`: 322 lines (under 500 ✓)
- `routes.py`: 227 lines (under 500 ✓)

## Dependencies

None — this spec is dependency-free.

## Blocks

- SPEC-EFEMERA-CONN-01 (service modules) — blocked on this schema upgrade
- SPEC-EFEMERA-CONN-02 (connector primitive) — blocked on this schema upgrade
- SPEC-EFEMERA-CONN-03 (terminal relay) — blocked on this schema upgrade
- SPEC-EFEMERA-CONN-04 (text-pane chat) — blocked on this schema upgrade

## Notes

**Design decisions:**
1. **Idempotent migration** — `_migrate_schema()` uses try/except to handle existing columns. Safe to run multiple times during development.
2. **Backward compatibility** — All new columns have defaults. Existing code that doesn't pass new params continues to work.
3. **Schema-first approach** — Extended schema matches platform's full feature set (versioning, threading, moderation, metadata). Frontend will use these fields in CONN-10 (message history/replies).
4. **channel_id param** — Allows system channel seeding with explicit IDs (e.g., "bugs-admin", "the-buzz"). Without it, UUID is generated.
5. **reply_to_id vs parent_id** — Separate fields: `reply_to_id` for thread replies (UI), `parent_id` for edit versioning chains (history). CONN-10 will implement edit history.

**What's NOT in this spec:**
- `edit_message()` — deferred to CONN-10
- `get_message_history()` — deferred to CONN-10
- `get_replies()` — deferred to CONN-10
- System channel auto-seeding — deferred to CONN-09 (initial data seed)
- RBAC permission checks — deferred to future spec (out of CONN batch scope)
- Moderation pipeline — deferred to future spec (Phase 3 in assessment doc)

**Verification:**
- Ran migration on clean DB — all columns created
- Ran migration on existing DB — all columns added via ALTER TABLE
- Ran migration twice on same DB — no errors (idempotent)
- All acceptance criteria met ✓
