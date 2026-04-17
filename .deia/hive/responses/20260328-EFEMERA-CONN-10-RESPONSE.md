# SPEC-EFEMERA-CONN-10: Message Versioning + Reply Threading -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-03-28

## Files Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\store.py` — added edit_message(), get_message_history(), get_replies(), updated create_message() with reply validation, updated list_messages() to show latest version only
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\message_routes.py` — NEW FILE, 3 routes for edit/history/replies
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` — registered message_routes router
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_efemera_versioning.py` — NEW FILE, 10 tests for edit versioning
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_efemera_threading.py` — NEW FILE, 10 tests for reply threading
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_efemera.py` — updated to use "commons" instead of "general", adjusted assertions for system channels
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_efemera_schema_upgrade.py` — updated to use "commons" instead of "general", fixed duplicate channel ID test

## What Was Done
- **TDD approach:** Wrote 20 tests (10 versioning + 10 threading) before implementation
- **Edit versioning:** edit_message() creates new row with version++, parent_id=root, preserves original author/channel/type/reply_to_id
- **Version history:** get_message_history() returns all versions ordered by version ASC
- **Reply threading:** create_message() validates reply_to_id (exists, same channel), get_replies() returns latest version of each reply
- **list_messages() update:** Now uses CTE to filter to latest version only (COALESCE(parent_id, id) grouping + MAX(version))
- **New routes file:** message_routes.py with 3 endpoints: PUT /messages/{id}, GET /messages/{id}/history, GET /messages/{id}/replies
- **Router registration:** Added to hivenode/routes/__init__.py with prefix='/efemera', tags=['efemera-messages']
- **Test fixes:** Updated existing tests to use "commons" (system channel) instead of "general" (removed in CONN-01), adjusted assertions for system welcome message and system member

## Tests
- **All 114 efemera tests passing** (29 existing + 20 new + 65 from other efemera test files)
- **test_efemera_versioning.py:** 10/10 passing
- **test_efemera_threading.py:** 10/10 passing
- **No regressions:** Fixed test suite for system channel seeding changes from CONN-01

## Acceptance Criteria Met
- [x] edit_message creates new row with version 2
- [x] edit_message twice creates version 3
- [x] get_message_history returns all versions in order
- [x] edit preserves original author_name and channel_id
- [x] edit with invalid message_id raises ValueError
- [x] list_messages shows latest version only (not all edit chain rows)
- [x] create_message with reply_to_id links to parent
- [x] get_replies returns all replies to a message
- [x] reply to nonexistent message raises ValueError
- [x] reply to message in different channel raises ValueError
- [x] replies appear in list_messages (normal messages with reply_to_id set)
- [x] message_routes.py registered in routes/__init__.py
- [x] All tests pass

## Smoke Test
```bash
cd hivenode && python -m pytest tests/hivenode/test_efemera_versioning.py -v  # 10 passed
cd hivenode && python -m pytest tests/hivenode/test_efemera_threading.py -v   # 10 passed
cd hivenode && python -m pytest tests/hivenode/ -k efemera -v                  # 114 passed
```

## Key Design Decisions
1. **Edit chain vs reply chain:** parent_id tracks edit versions, reply_to_id tracks threaded conversations — completely separate
2. **Latest version filter:** list_messages() and get_replies() both use CTE with COALESCE(parent_id, id) grouping to show only latest versions
3. **Preserved fields:** edit_message() preserves author_id, author_name, channel_id, author_type, message_type, reply_to_id, provider, topic_id, topic_name from original
4. **Reply validation:** create_message() validates reply target exists and is in same channel (throws ValueError otherwise)
5. **Routes organization:** New message_routes.py file instead of adding to existing routes.py (follows spec requirement)

## Notes
- Port follows platform logic exactly (lines 202-294 in platform messages/routes.py)
- Threading is flat (one level) — nested replies work but are not recursive
- edit_message() preserves created_at from original (for chronological ordering)
- Version numbering is continuous across entire edit chain (1, 2, 3, ... N)
- Reply threading and edit versioning interact correctly: editing a reply creates new version but preserves reply_to_id
