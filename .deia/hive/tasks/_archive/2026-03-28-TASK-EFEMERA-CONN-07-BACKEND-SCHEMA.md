# TASK-EFEMERA-CONN-07: Backend Schema Upgrade

## Objective
Extend the efemera SQLite schema to support message versioning, reply threading, moderation fields, author metadata, and channel type enum — ported from the platform implementation.

## Context
The platform efemera has a rich message model with fields for versioning (version, parent_id, edited_at), threading (reply_to_id, topic_id, topic_name), moderation (moderation_status, moderation_reason), author metadata (author_type, message_type, metadata_json), and bridge tracking (provider). The shiftcenter store has none of these. The channel type is limited to 'channel'|'dm' — platform has 11 types.

This task extends the SQLite schema and store methods to support these fields. No new routes — just the data layer.

**No dependencies.** This task can run in parallel with frontend tasks.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\store.py` (224 lines — current store)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\routes.py` (169 lines — current routes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_efemera.py` (existing tests)
- Platform source (for reference — read the assessment):
  - `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\channels\models.py`
  - `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\messages\models.py`

## Deliverables

### 1. Modify `hivenode/efemera/store.py`

**Schema changes (create_efemera_schema):**
- [ ] Expand channels.type CHECK to include: 'channel', 'dm', 'commons', 'humans_only', 'the_buzz', 'announcements', 'approvals', 'moderation_log', 'bugs_admin', 'bok_submissions', 'the_window', 'dev', 'personal'
- [ ] Add channels.description TEXT column (nullable)
- [ ] Add channels.read_only BOOLEAN DEFAULT FALSE column
- [ ] Add messages.version INTEGER DEFAULT 1 column
- [ ] Add messages.parent_id TEXT REFERENCES messages(id) column (nullable — for edit chains)
- [ ] Add messages.reply_to_id TEXT REFERENCES messages(id) column (nullable — for threads)
- [ ] Add messages.edited_at TEXT column (nullable)
- [ ] Add messages.moderation_status TEXT DEFAULT 'approved' CHECK(moderation_status IN ('approved', 'held', 'blocked', 'rejected', 'withdrawn')) column
- [ ] Add messages.moderation_reason TEXT column (nullable)
- [ ] Add messages.provider TEXT column (nullable — 'discord', etc.)
- [ ] Add messages.author_type TEXT DEFAULT 'human' CHECK(author_type IN ('human', 'bot', 'agent', 'system', 'discord')) column
- [ ] Add messages.message_type TEXT DEFAULT 'text' CHECK(message_type IN ('text', 'terminal_output', 'rag_answer', 'system')) column
- [ ] Add messages.metadata_json TEXT column (nullable — JSON blob)
- [ ] Add messages.topic_id TEXT column (nullable)
- [ ] Add messages.topic_name TEXT column (nullable)
- [ ] Add index on messages(reply_to_id) for thread queries
- [ ] Add index on messages(parent_id) for version history queries
- [ ] Add index on messages(moderation_status) for moderation queue

**Store method additions:**
- [ ] `edit_message(message_id, new_content, editor_id) -> Dict` — creates a new message row with parent_id=original.id, version=original.version+1, edited_at=now. Returns the new version.
- [ ] `get_message(message_id) -> Optional[Dict]` — get a single message by ID
- [ ] `get_message_history(message_id) -> List[Dict]` — get all versions: root + all rows where parent_id=message_id, ordered by version ASC
- [ ] `get_replies(message_id, limit=50) -> List[Dict]` — get messages where reply_to_id=message_id, ordered by created_at ASC
- [ ] `list_messages()` — modify to only return top-level messages (parent_id IS NULL AND reply_to_id IS NULL) with moderation_status='approved'
- [ ] `create_message()` — extend signature to accept optional: reply_to_id, author_type, message_type, metadata_json, provider, topic_id, topic_name
- [ ] `list_moderation_queue(status_filter='held', limit=100) -> List[Dict]` — list messages by moderation_status
- [ ] `update_moderation_status(message_id, status, reason=None) -> Optional[Dict]` — update moderation_status and moderation_reason

**Backward compatibility:**
- [ ] Existing API calls that don't provide new fields still work (all new fields have defaults or are nullable)
- [ ] Existing tests still pass without modification

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing efemera tests still pass
- [ ] New test file: `tests/hivenode/test_efemera_schema_v2.py`

### Test cases required (25+ tests):
**Schema:**
- New columns exist in channels and messages tables
- Channel type enum accepts all 11+2 types
- Message defaults: version=1, moderation_status='approved', author_type='human', message_type='text'

**Message versioning:**
- edit_message creates new row with incremented version
- edit_message sets parent_id to original message ID
- edit_message sets edited_at
- get_message_history returns root + all edits ordered by version
- Multiple edits: version increments correctly (1, 2, 3)

**Reply threading:**
- create_message with reply_to_id stores correctly
- get_replies returns all replies to a message
- list_messages excludes replies (reply_to_id IS NULL)
- Reply to a reply (nested threading)

**Moderation:**
- create_message with default moderation_status='approved'
- list_messages excludes non-approved messages
- list_moderation_queue returns held/blocked messages
- update_moderation_status changes status and reason
- update_moderation_status on non-existent message returns None

**Author metadata:**
- create_message with author_type='bot'
- create_message with message_type='system'
- create_message with metadata_json stores and retrieves correctly
- create_message with provider='discord'

**Backward compatibility:**
- Existing create_message calls (without new fields) still work
- Existing list_messages calls still work
- Existing test_efemera.py tests all pass

## Constraints
- No file over 500 lines. If store.py exceeds 500, split into store.py + message_store.py
- No stubs
- SQLite only (no SQLAlchemy — keep raw sqlite3 pattern from existing store)
- All new columns must have defaults or be nullable — schema changes must not break existing data
- Do NOT modify routes.py in this task — new routes come in CONN-09

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-EFEMERA-CONN-07-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
