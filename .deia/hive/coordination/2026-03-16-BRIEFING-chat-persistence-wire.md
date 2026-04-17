# BRIEFING: Wire chat persistence save to volume list in tree reload

**Date:** 2026-03-16
**For:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Spec:** `2026-03-16-1035-SPEC-w2-08-chat-persistence-wire`
**Priority:** P1.20
**Model:** sonnet

---

## Objective

Wire the missing piece: when a user clicks a conversation in tree-browser, the terminal should reload that conversation's messages. Currently:
- ✅ Conversations auto-save (via `terminalChatPersist.ts`)
- ✅ Tree-browser lists conversations (via `chatHistoryAdapter.ts`)
- ✅ Clicking publishes `conversation:selected` event (via `ChatNavigatorPane.tsx`)
- ❌ Terminal does NOT listen for `conversation:selected` or reload the conversation

**Goal:** Terminal listens for `conversation:selected` bus events, loads the conversation via `chatApi.getConversation()`, and populates terminal entries with the loaded messages.

---

## Context

### What Already Exists

1. **Chat persistence (auto-save):**
   - `browser/src/primitives/terminal/terminalChatPersist.ts` — helper that calls `chatApi.addMessage()` after each LLM response
   - `browser/src/primitives/terminal/useTerminal.ts:574-582` — already calls `persistChatMessages()` after LLM responses

2. **Chat storage API:**
   - `browser/src/services/terminal/chatApi.ts` — full CRUD for conversations
   - `createConversation()`, `getConversation(id)`, `addMessage()`, `deleteConversation()`, etc.
   - Dual-write to `home://` and `cloud://` volumes
   - Markdown format for conversation files

3. **Tree-browser adapter:**
   - `browser/src/primitives/tree-browser/adapters/chatHistoryAdapter.ts` — loads conversations from `chatApi.listConversations()`
   - Groups by date (Today, Yesterday, This Week, Older)
   - Shows volume status badges

4. **Chat navigator pane:**
   - `browser/src/primitives/tree-browser/ChatNavigatorPane.tsx` — wraps TreeBrowser for conversations
   - On conversation click → publishes `conversation:selected` event with `{ conversationId, path, volume }`

5. **Bus event handling in useTerminal:**
   - `browser/src/primitives/terminal/useTerminal.ts:176-183` — already subscribes to bus events
   - Currently only handles `channel:selected` (for efemera chat)
   - Pattern: `bus.subscribe(nodeId, (message) => { ... })`

### What's Missing

**Terminal does NOT handle `conversation:selected` event.**

When a user clicks a conversation in tree-browser:
1. ChatNavigatorPane publishes `conversation:selected` with `conversationId`
2. Terminal needs to:
   - Call `chatApi.getConversation(conversationId)`
   - Load the conversation's messages
   - Convert messages to `TerminalEntry[]` format
   - Replace current terminal entries with loaded conversation
   - Set `conversationId` state (so new messages append to this conversation)
   - Optionally update ledger totals from message metrics

---

## File Paths (Absolute)

### Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (main terminal hook, ~600 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts` (TerminalEntry types)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatApi.ts` (conversation API)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\types.ts` (Message, Conversation types)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\ChatNavigatorPane.tsx` (event publisher)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts` (bus event types)

### Files to Modify

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (add `conversation:selected` listener)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminalChatPersist.ts` (add conversation loader helper)

### Test Files

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\useTerminal.chatPersist.test.ts` (new test file)

---

## Technical Approach

### 1. Add conversation loader helper to terminalChatPersist.ts

Create `loadConversationToEntries(conversationId: string): Promise<TerminalEntry[]>`:
- Call `chatApi.getConversation(conversationId)`
- Convert each `Message` to a `TerminalEntry`:
  - `role: 'user'` → `{ type: 'input', content: message.content }`
  - `role: 'assistant'` → `{ type: 'response', content: message.content, metrics: { model, clock_ms, cost_usd, carbon_g, ... } }`
- Return array of entries

### 2. Add conversation:selected listener to useTerminal.ts

In the existing `useEffect(() => { bus.subscribe(nodeId, ...) })` block (lines 176-183):
- Add case for `message.type === 'conversation:selected'`
- Call `loadConversationToEntries(message.data.conversationId)`
- `setEntries([{ type: 'banner', content: WELCOME_BANNER }, ...loadedEntries])`
- `setConversationId(message.data.conversationId)`
- Optionally: recalc ledger totals from message metrics

### 3. Test coverage

Write `useTerminal.chatPersist.test.ts`:
- Mock `chatApi.getConversation()`
- Mock `bus.send()` and `bus.subscribe()`
- Test:
  - ✅ Conversation loads when `conversation:selected` event fires
  - ✅ Entries are populated from messages
  - ✅ conversationId state is set
  - ✅ Ledger totals update (if implemented)
  - ✅ Banner is prepended to entries
  - ✅ No crash if conversation not found

---

## Acceptance Criteria (from spec)

- [ ] Conversations save automatically (already done via terminalChatPersist.ts)
- [ ] Tree-browser shows conversation list (already done via chatHistoryAdapter.ts)
- [ ] Clicking conversation reloads it (NEW — this briefing)
- [ ] Tests written and passing

---

## Constraints

- **Max 500 lines per file** — useTerminal.ts is already ~600 lines, so conversation loading logic goes in terminalChatPersist.ts
- **TDD** — write tests first
- **No stubs** — full implementation
- **CSS** — none needed (logic-only change)
- **Heartbeats** — POST to `http://localhost:8420/build/heartbeat` every 3 minutes with task_id `2026-03-16-1035-SPEC-w2-08-chat-persistence-wire`
- **File claims** — claim files before modifying (see spec)

---

## Smoke Test

```bash
cd browser && npx vitest run src/primitives/terminal/__tests__/useTerminal.chatPersist.test.ts
```

No new test failures in existing terminal tests.

---

## Task Breakdown Guidance

Suggested task split (bee-sized):

1. **TASK-180:** Add `loadConversationToEntries()` helper to terminalChatPersist.ts + unit tests
2. **TASK-181:** Wire `conversation:selected` listener in useTerminal.ts + integration test
3. **TASK-182:** E2E smoke test (tree-browser → click conversation → terminal updates)

Or combine into 1-2 tasks if clean separation isn't needed.

---

## Questions for Q33N

1. Should ledger totals update when loading a conversation? (Sum all message metrics?)
2. Should we preserve current terminal session when loading a conversation, or replace entirely?
3. Should we show a "Loading conversation..." system entry while fetching?

**Suggested answers (Q33NR opinion):**
1. Yes — update ledger totals from loaded messages
2. Replace entirely (fresh terminal state)
3. Optional nice-to-have (not required for P1)

---

## Response Required

Q33N: Please read this briefing, read the listed files, write task files, and return them to Q33NR for review before dispatching bees.

---

**End of briefing.**
