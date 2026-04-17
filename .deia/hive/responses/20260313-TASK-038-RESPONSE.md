# TASK-038: Tree-Browser Conversation Navigator -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-13

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\ChatNavigatorPane.tsx` [CREATE]
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts` [MODIFY]
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts` [MODIFY]
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\conversationNavigator.test.tsx` [CREATE]

## What Was Done

- **ChatNavigatorPane component (261 lines):**
  - Wraps TreeBrowser with chat-history adapter
  - Loads conversation list from chatApi on mount
  - Auto-expands date group nodes (Today, Yesterday, This Week, Older)
  - Publishes `conversation:selected` message when user clicks a conversation
  - Subscribes to `conversation:created` and `conversation:deleted` events
  - Auto-refreshes tree when conversations created or deleted
  - Auto-selects newly created conversations

- **Volume sync badges:**
  - Fetches sync status from `/sync/status` hivenode route
  - Maps sync status to badge type:
    - Synced → green `✓` (success)
    - Pending → yellow `⬆` (warning)
    - Conflict → yellow `⚠` (warning)
    - Offline → red `✗` (default)
  - Falls back to message count badges if sync status unavailable
  - Badge application is recursive through tree groups

- **Conversation actions:**
  - New button in header — calls `createConversation()`, publishes `conversation:created` event
  - Delete button in header — disabled unless conversation selected
  - Delete shows confirmation dialog before deletion
  - Publishes `conversation:deleted` event after successful deletion

- **Message types added:**
  - `ConversationSelectedData` — { conversationId, path, volume }
  - `ConversationCreatedData` — { conversationId }
  - `ConversationDeletedData` — { conversationId }
  - `ConversationActionData` — { conversationId, action }

- **chatHistoryAdapter enhancement:**
  - Added `created_at` to conversation node metadata
  - Required for path construction: `{volume}://chats/{date}/conversation-{id}.md`

- **Test suite (12 tests, all passing):**
  - Selection handler: publishes message with correct data, ignores group nodes
  - Tree refresh: responds to created/deleted events, auto-selects new conversations
  - Volume badges: shows correct badge for sync status, falls back to message count
  - Conversation actions: creates and deletes conversations, shows confirmation

## Tests

All 12 tests pass:
- ✅ ChatNavigatorPane - Selection Handler (3/3)
- ✅ ChatNavigatorPane - Tree Refresh (3/3)
- ✅ ChatNavigatorPane - Volume Badges (4/4)
- ✅ ChatNavigatorPane - Conversation Actions (2/2)

## Technical Notes

- Component avoids circular dependencies in useCallback by inlining logic in `loadTree()`
- Uses `setTimeout(fn, 0)` for auto-selection after create to wait for state updates
- TreeBrowser auto-expands all group nodes via `expandedIds` prop
- Graceful degradation: sync badges optional, message count fallback
- No stubs — all functions fully implemented

## Acceptance Criteria

1. ✅ Clicking a conversation in tree publishes `conversation:selected` message
2. ✅ Terminal can subscribe to `conversation:selected` and load conversation
3. ✅ Tree refreshes automatically when conversations created/deleted
4. ✅ Volume badges show sync status (green/yellow/red)
5. ✅ New conversation action creates conversation, selects it
6. ✅ Delete conversation action shows confirmation, deletes conversation
7. ✅ All tests pass (12/12)
8. ✅ No console errors or warnings
