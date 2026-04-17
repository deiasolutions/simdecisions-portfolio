# TASK-038: Tree-Browser Conversation Navigator

**Role:** BEE (coder)
**Model:** Sonnet
**Parent:** SPEC-HIVENODE-E2E-001 Wave 4
**Spec sections:** 8.1–8.3
**Date:** 2026-03-12
**Estimated tests:** ~12

---

## Objective

Wire the tree-browser primitive as a conversation navigator pane. When the user clicks a conversation in the tree, load it into the chat terminal. Add volume badges showing sync status, and wire conversation actions (new, delete).

**This is browser-only TypeScript work. No backend changes.**

---

## What Already Exists

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx` — complete component with `onSelect`, `onExpand`, `onCollapse`, keyboard nav
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts` — `loadChatHistory()` returns `TreeNodeData[]` grouped by date
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatApi.ts` — `listConversations()`, `getConversation(id)`, `createConversation()`, `deleteConversation(id)`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\messageBus.ts` — `send()`, `subscribe()`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\types.ts` — `TreeBrowserPaneConfig` with adapter type `'chat-history'`

---

## What to Build

### 1. Conversation Selection Handler

**File:** New file or extend existing adapter
**Path:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts`

When user selects a conversation in the tree:

1. Extract `conversationId` from `TreeNodeData.meta.conversationId`
2. Publish `conversation:selected` message on relay bus:
   ```typescript
   {
     type: 'conversation:selected',
     sourcePane: '<tree-browser-pane-id>',
     target: '*',  // Broadcast
     data: {
       conversationId: string,
       path: string,  // e.g., "home://chats/2026-03-12/conversation-abc123.md"
       volume: 'home://' | 'cloud://',
     }
   }
   ```
3. The terminal/chat pane subscribes to this message type
4. On receipt, terminal calls `getConversation(id)` to load messages
5. Display loaded conversation in the terminal output

**Message type definition:**

Add to `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts`:

```typescript
export interface ConversationSelectedData {
  conversationId: string;
  path: string;
  volume: string;
}
```

### 2. Tree-Browser Pane Integration

**File:** New component or extend existing
**Path:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\ChatNavigatorPane.tsx`

Create a pane component that wraps TreeBrowser:

1. Use `TreeBrowserPaneConfig` with `adapter: 'chat-history'`
2. Call `loadChatHistory()` on mount
3. Call `loadChatHistory()` on conversation create/delete (subscribe to bus events):
   - `conversation:created` → refresh tree, select new conversation
   - `conversation:deleted` → refresh tree, clear selection if deleted
4. Pass `onSelect` handler that publishes `conversation:selected` message
5. Wire keyboard nav, search, expand/collapse through TreeBrowser props

**Props:**

```typescript
interface ChatNavigatorPaneProps {
  paneId: string;        // For relay bus messages
  selectedId?: string;   // Current conversation ID
}
```

### 3. Volume Badges (Section 8.3)

**File:** Extend `chatHistoryAdapter.ts`

Show sync status on conversations:

- **Online/synced** (green) — volume is online, file synced to cloud
- **Sync in progress** (yellow) — currently syncing
- **Conflict** (red) — sync conflict detected
- **Pending upload** (blue) — changes pending sync
- **Offline** (red) — volume offline

**Implementation:**

1. Read volume status from hivenode `/sync/status` route (built in Wave 3)
2. Call `fetch('http://localhost:8420/sync/status')` to get sync state
3. Map sync state to badge type:
   ```typescript
   {
     text: 'Synced',
     type: 'success'  // or 'warning', 'default', 'active'
   }
   ```
4. Set `TreeNodeData.badge` based on sync status
5. Fall back to message count badge if sync status unavailable

**Badge mapping:**

- Synced → `{ text: '✓', type: 'success' }`
- Pending → `{ text: '⬆', type: 'warning' }`
- Conflict → `{ text: '⚠', type: 'warning' }`
- Offline → `{ text: '✗', type: 'default' }`

### 4. Conversation Actions

**File:** Extend `ChatNavigatorPane.tsx`

Right-click or action menu on conversations:

1. **New conversation:**
   - Button in tree header or keyboard shortcut (`Ctrl+N`)
   - Calls `createConversation()`
   - Publishes `conversation:created` bus event
   - Refreshes tree
   - Selects new conversation (publishes `conversation:selected`)

2. **Delete conversation:**
   - Action in `TreeNodeData.actions[]`:
     ```typescript
     {
       id: 'delete',
       label: 'Delete Conversation',
       icon: '🗑',
       danger: true
     }
     ```
   - Confirmation modal: "Delete this conversation? This cannot be undone."
   - Calls `deleteConversation(id)`
   - Publishes `conversation:deleted` bus event with `{ conversationId }`
   - Refreshes tree

**Wire through `TreeNodeAction` interface:**

- TreeBrowser supports `node.actions[]` array
- On action click, publish `conversation:action` bus event:
  ```typescript
  {
    type: 'conversation:action',
    data: {
      conversationId: string,
      action: 'delete' | 'rename' | 'export'
    }
  }
  ```

---

## File Structure

```
browser/src/primitives/tree-browser/
├── adapters/
│   └── chatHistoryAdapter.ts           [MODIFY] Add sync badges, action handlers
├── ChatNavigatorPane.tsx               [CREATE] Wrapper pane component
└── __tests__/
    └── conversationNavigator.test.ts   [CREATE] Test suite

browser/src/infrastructure/relay_bus/types/
└── messages.ts                         [MODIFY] Add ConversationSelectedData

browser/src/services/terminal/
└── chatApi.ts                          [READ ONLY] Reference for API calls
```

---

## Tests

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\conversationNavigator.test.ts`

**Coverage (~12 tests):**

1. **Selection handler:**
   - ✓ Selecting conversation publishes `conversation:selected` message
   - ✓ Message includes correct conversationId, path, volume
   - ✓ Selecting date group node does nothing (no message)

2. **Tree refresh:**
   - ✓ Tree refreshes on `conversation:created` event
   - ✓ Tree refreshes on `conversation:deleted` event
   - ✓ New conversation is auto-selected after creation

3. **Volume badges:**
   - ✓ Synced conversation shows green badge
   - ✓ Pending conversation shows yellow badge
   - ✓ Offline conversation shows red badge
   - ✓ Falls back to message count if sync status unavailable

4. **Conversation actions:**
   - ✓ New conversation action creates conversation, refreshes tree
   - ✓ Delete action shows confirmation, deletes conversation, refreshes tree

**Test utilities:**

- Mock `chatApi` functions with `vi.mock()`
- Mock `messageBus.send()` and `messageBus.subscribe()`
- Mock fetch for `/sync/status` endpoint
- Use `@testing-library/react` for component rendering

---

## Acceptance Criteria

1. ✅ Clicking a conversation in tree publishes `conversation:selected` message
2. ✅ Terminal subscribes to `conversation:selected` and loads conversation
3. ✅ Tree refreshes automatically when conversations created/deleted
4. ✅ Volume badges show sync status (green/yellow/red)
5. ✅ New conversation action creates conversation, selects it
6. ✅ Delete conversation action shows confirmation, deletes conversation
7. ✅ All tests pass (12/12)
8. ✅ No console errors or warnings

---

## Constraints

- No file over 500 lines
- TDD — tests first
- No stubs — every function fully implemented
- Relay bus messages must use existing `MessageEnvelope` format
- Badge types must use existing `TreeBadge` type (`'default' | 'active' | 'success' | 'warning'`)
- Graceful degradation if hivenode `/sync/status` unavailable

---

## Dependencies

**Required before start:**
- Tree-browser primitive (already built)
- Chat API (already built)
- Relay bus (already built)
- Sync status route (built in Wave 3)

**Blocks:**
- None (independent task)

---

## Notes

- This is the final piece connecting tree-browser to chat terminal
- Volume badges are optional enhancement — implement if time allows, otherwise use message count badges
- Conversation actions can be minimal (just delete) — other actions (rename, export, archive) can be added later
- Focus on core selection + refresh flow first, then add bells and whistles
