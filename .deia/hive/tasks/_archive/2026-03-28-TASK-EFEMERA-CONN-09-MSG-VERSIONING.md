# TASK-EFEMERA-CONN-09: Port Message Versioning + Reply Threading Routes

## Objective
Add API routes for message editing (versioning), reply threading, and message history — porting the endpoint patterns from platform.

## Context
CONN-07 added the schema fields (version, parent_id, reply_to_id, edited_at) and store methods (edit_message, get_message_history, get_replies). This task adds the HTTP routes that expose these capabilities.

Platform had:
- `PUT /api/messages/{id}` — edit message (re-runs moderation, creates new version)
- `GET /api/messages/{id}/history` — get all versions
- `GET /api/messages/{id}/replies` — get thread replies
- `POST /api/messages/` — send with optional reply_to_id

**Depends on:** TASK-EFEMERA-CONN-07 (schema + store methods must exist).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\messages\routes.py` (295 lines — reference implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\store.py` (after CONN-07)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\routes.py` (current routes)

## Deliverables

### 1. Modify `hivenode/efemera/routes.py` OR create `hivenode/efemera/message_routes.py`

If routes.py would exceed 500 lines with additions, split message-specific routes into a new file.

- [ ] Extend `CreateMessageRequest` schema with optional fields: reply_to_id, author_type, message_type, metadata_json, topic_id, topic_name
- [ ] `POST /channels/{channel_id}/messages` — update to pass new fields through to store.create_message()
- [ ] `PUT /channels/{channel_id}/messages/{message_id}` — edit message
  - Only the original sender can edit (compare author_id)
  - Creates new version via store.edit_message()
  - Returns the new version
  - 403 if not the sender
  - 404 if message not found
- [ ] `GET /channels/{channel_id}/messages/{message_id}/history` — get edit history
  - Returns all versions via store.get_message_history()
  - 404 if message not found
- [ ] `GET /channels/{channel_id}/messages/{message_id}/replies` — get thread replies
  - Returns replies via store.get_replies()
  - 404 if parent message not found
- [ ] `GET /channels/{channel_id}/messages` — update to exclude edits and replies (only top-level approved messages)

### 2. Add Pydantic schemas

- [ ] `EditMessageRequest`: content (str, min_length=1, max_length=4000)
- [ ] `MessageResponse`: all message fields including version, reply_to_id, edited_at, author_type, message_type

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing efemera tests still pass
- [ ] New test file: `tests/hivenode/test_efemera_messages_v2.py`

### Test cases required (22+ tests):
**Message creation with new fields:**
- Create message with reply_to_id
- Create message with author_type='bot'
- Create message with metadata_json
- Create message with topic_id and topic_name
- Default values applied when fields omitted

**Message editing:**
- Edit message returns version=2
- Edit message sets parent_id to original
- Edit message sets edited_at
- Multiple edits increment version (1, 2, 3)
- Edit by non-sender returns 403
- Edit non-existent message returns 404
- Edit preserves channel_id and author_id

**Edit history:**
- History returns root + all edits
- History ordered by version ASC
- History for non-existent message returns 404

**Reply threading:**
- Create reply with reply_to_id
- Get replies returns all replies
- Replies ordered by created_at ASC
- Replies for non-existent message returns 404
- Replies not shown in main message list

**Filtering:**
- list_messages excludes edited versions (parent_id IS NOT NULL)
- list_messages excludes replies (reply_to_id IS NOT NULL)
- list_messages only shows approved moderation_status

## Constraints
- No file over 500 lines — if routes.py would exceed, split into message_routes.py
- No stubs
- Keep existing endpoint signatures backward-compatible
- New optional fields on CreateMessageRequest must not break existing callers
- Register any new route files in `hivenode/routes/__init__.py`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-EFEMERA-CONN-09-RESPONSE.md`

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
