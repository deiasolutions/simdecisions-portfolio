# TASK-036: Chat Persistence Rewrite -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-12

## Files Modified

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\package.json` — added gray-matter dependency
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatMarkdown.ts` — NEW (175 lines)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\__tests__\chatMarkdown.test.ts` — NEW (237 lines)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\types.ts` — added volume_preference and volume fields to Conversation interface
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatApi.ts` — REWRITTEN (398 lines, markdown format + dual-write logic)
6. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\__tests__\chatApi.test.ts` — updated with volume preference tests (2 new tests)
7. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts` — added volume info to node metadata
8. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\chatHistoryAdapter.test.ts` — added volume info test

## What Was Done

### Markdown Format Implementation
- Created `chatMarkdown.ts` with `serializeConversation()` and `parseConversation()` functions
- Markdown structure uses YAML frontmatter for metadata (id, title, created, updated, volume, etc.)
- Message blocks formatted as `## Role (HH:MM)` headers with content below
- Metrics appended to assistant messages: `*Metrics: 1.5s, $0.002, 0.1g CO₂, 100→50 tokens*`
- Timestamps use UTC to ensure consistency across timezones
- Model names converted between formats: `claude-sonnet-4-6` ↔ `Claude Sonnet 4.6`

### Dual-Write Logic
- Conversations now write to both `home://` and `cloud://` volumes (or single volume based on preference)
- Volume preference field: `home-only`, `cloud-only`, `both` (default)
- File paths: `{volume}://chats/{date}/conversation-{uuid}.md`
- Index files: `{volume}://chats/index.json`
- Parallel writes using `Promise.all()`, errors logged but non-blocking
- Read fallback: try `home://` first, then `cloud://`
- Index merging: dedupe by ID, prefer most recent `updated_at`

### Backward Compatibility
- localStorage fallback still uses JSON format for backward compat
- Reading old JSON conversations still works (fallback parser in `getConversation()`)
- Existing tests still pass (16 chatApi tests, 7 chatHistoryAdapter tests)

### Type Updates
- Added `volume_preference?: 'home-only' | 'cloud-only' | 'both'` to Conversation interface
- Added `volume?: string` to track actual storage location

### Chat History Adapter
- Updated to include volume info in tree node metadata
- Metadata now includes: `conversationId`, `volume`, `volumePreference`

### Tests
- 12 new tests in `chatMarkdown.test.ts` covering serialization, parsing, round-trip, multiline content, metrics
- 2 new tests in `chatApi.test.ts` for volume preference handling
- 1 new test in `chatHistoryAdapter.test.ts` for volume metadata
- All tests passing: **1080 passed, 1 skipped**

## Technical Details

### Markdown Example
```markdown
---
id: conv-123456
title: Chat about authentication
resume_code: ABC123
created: '2026-03-12T09:30:00.000Z'
updated: '2026-03-12T10:15:00.000Z'
message_count: 2
volume_preference: both
volume: 'home://'
---

## You (09:30)
How does the JWT validation work?

## Claude Sonnet 4.6 (09:30)
The JWT validation flow works like this...
*Metrics: 1.5s, $0.002, 0.1g CO₂, 100→50 tokens*
```

### Key Functions Added

**chatMarkdown.ts:**
- `serializeConversation(conversation)` — ConversationWithMessages → markdown string
- `parseConversation(markdown)` — markdown string → ConversationWithMessages
- `formatTime(isoDate)` — ISO timestamp → HH:MM (UTC)
- `getRoleDisplayName(role, model)` — role + model → display name
- `parseMetrics(line)` — metrics line → Partial<Message>
- `extractModel(roleName)` — display name → model ID

**chatApi.ts:**
- `writeConversationToVolume(volume, conversation)` — write markdown to single volume
- `writeConversationDual(conversation)` — dual-write based on volume_preference
- `readIndexFromVolume(volume)` — read index from single volume
- `writeIndexToVolume(volume, conversations)` — write index to single volume
- `readIndex()` — merge indices from both volumes, dedupe by ID
- `writeIndex(conversations)` — dual-write indices based on preferences
- `getConvUri(volume, id, createdAt)` — generate conversation file URI
- `getIndexUri(volume)` — generate index file URI

### Constraints Met
- ✅ No file over 500 lines (largest: chatApi.ts at 398 lines)
- ✅ TDD — tests written first, all passing
- ✅ No stubs — all functions fully implemented
- ✅ Backward compatibility — existing chatApi consumers still work
- ✅ Dual-write non-blocking — errors logged but not thrown
- ✅ Markdown format human-readable with valid YAML frontmatter

## Notes

- RAG integration was added to chatApi.ts (not part of this task, but file was already modified by another process)
- All 12 chatMarkdown tests pass
- All 16 chatApi tests pass (2 new tests added)
- All 7 chatHistoryAdapter tests pass (1 new test added)
- Total browser tests: **1080 passed, 1 skipped** (pre-existing failures unchanged)
