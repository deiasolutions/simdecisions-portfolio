# TASK-RB3: Chat Adapter Rebuild — COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-19

## Files Modified

1. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/tree-browser/adapters/chatHistoryAdapter.ts`
2. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/apps/treeBrowserAdapter.tsx`
3. `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/apps/__tests__/treeBrowserAdapter.chatHistory.test.tsx`

## What Was Done

**Fix A: BUG-030 — Chat Tree Browser Empty (Resolved)**
- Added deduplication logic to `loadChatHistory()` in chatHistoryAdapter.ts
- Deduplicate by conversation ID, keeping most recent `updated_at` when duplicates exist
- Added `chat-history` to `AUTO_EXPAND_ADAPTERS` set in treeBrowserAdapter.tsx
- Date group headers now auto-expand on initial load to show conversation items
- Fixed integration test timing issue in treeBrowserAdapter.chatHistory.test.tsx
- Changed test to properly wait for auto-expansion before asserting row count

**Fix B: BUG-022B — Click-to-Place Chat History Wiring (Resolved)**
- Added `conversation:selected` bus event broadcast in treeBrowserAdapter.tsx
- Event fires when user clicks on a conversation node (not date group headers)
- Sends conversation metadata: conversationId, path, volume
- Follows same pattern as channels adapter (`channel:selected`) and filesystem adapter (`file:selected`)

## Tests

**All tests passing:**
- `chatHistoryAdapter.test.ts`: 11/11 passing ✅
- `treeBrowserAdapter.chatHistory.test.tsx`: 4/4 passing ✅

**Test coverage:**
- Empty conversation list returns empty array
- Conversations grouped by date (Today, Yesterday, This Week, Older)
- Sorting by updated_at (newest first)
- Volume status badges included
- Long title truncation
- Null title fallback to conversation ID
- Error handling returns empty array
- Metadata included in tree nodes
- Zero message conversations handled
- **Deduplication** when API returns duplicate conversation IDs
- Cross-volume deduplication (same ID from home:// and cloud://)
- Auto-expand date groups on initial load
- Empty state display when no conversations
- No empty date headers shown
- Conversations immediately visible (groups expanded)

## Build Verification

**Vite build:** ✅ PASSING
- 3,019 modules transformed
- Build time: 28.00s
- No errors

## Implementation Details

### Deduplication Strategy
```typescript
// Deduplicate by ID (keep most recent updated_at)
const deduped = new Map<string, Conversation>();
for (const conv of conversations) {
  const existing = deduped.get(conv.id);
  if (!existing || new Date(conv.updated_at) > new Date(existing.updated_at)) {
    deduped.set(conv.id, conv);
  }
}
```

### Auto-Expand Configuration
```typescript
const AUTO_EXPAND_ADAPTERS = new Set(['chat-history', 'channels', 'members', 'palette', 'bus'])
```

### Bus Event Payload
```typescript
{
  type: 'conversation:selected',
  sourcePane: paneId,
  target: '*',
  nonce: `${Date.now()}-${Math.random()}`,
  timestamp: new Date().toISOString(),
  data: {
    conversationId: node.meta.conversationId,
    path: `chats/${node.meta.created_at}/${node.meta.conversationId}.md`,
    volume: node.meta.volume || 'home://',
  }
}
```

## Acceptance Criteria

- [x] Chat tree-browser shows conversation entries when they exist
- [x] Date headers group conversations correctly
- [x] Empty state shows "No conversations yet" placeholder
- [x] Tests pass (15/15)
- [x] Build passes
- [x] No file over 500 lines
- [x] CSS: var(--sd-*) only (no CSS changes made)
- [x] No stubs

## Notes

- BUG-022B canvas click-to-place feature was already complete per Q33NR report (2026-03-19)
- The task description conflated canvas component placement with chat conversation selection
- Added `conversation:selected` bus event for chat history, which is the correct wiring for this adapter
- The actual canvas palette click-to-place was implemented on 2026-03-17 and has 10/10 passing tests
- All changes follow existing patterns from channels and filesystem adapters
