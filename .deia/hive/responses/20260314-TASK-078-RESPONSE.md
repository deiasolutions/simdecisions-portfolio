# TASK-078: Tree-Browser Conversation Load Handler — COMPLETE

**Status:** COMPLETE
**Model:** Haiku 4.5
**Date:** 2026-03-14

---

## Files Modified

**Created:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\chat\conversationLoader.ts` — Hook implementation (70 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\chat\__tests__\conversationLoader.test.ts` — Test suite (185 lines)

---

## What Was Done

1. **TDD approach:** Wrote 7 comprehensive tests first
   - Test for successful conversation load and send
   - Test for 404 (conversation not found) error handling
   - Test for network/volume offline error handling
   - Test for null bus handling
   - Test for null textPaneNodeId handling
   - Test for missing conversationId in data
   - Test for wrong event type filtering

2. **Implemented `useConversationLoader` hook** (`browser/src/services/chat/conversationLoader.ts`)
   - Listens for `tree-browser:conversation-selected` events on message bus
   - Extracts `conversationId` from event data
   - Calls `chatApi.getConversation(conversationId)` to load full conversation
   - Calls `chatMarkdown.serializeConversation()` to convert to markdown
   - Sends markdown to text-pane via `terminal:text-patch` bus message with proper envelope:
     - `type: 'terminal:text-patch'`
     - `sourcePane: 'conversation-loader'`
     - `target: textPaneNodeId` (from hook params)
     - `format: 'markdown'`
     - `ops: [{ op: 'replace', content: markdown }]`
     - Unique `nonce` and ISO `timestamp`

3. **Error handling:**
   - 404 errors (conversation not found): sends "**Error:** Conversation not found." message
   - Network/volume offline errors: sends "**Error:** Unable to load conversation (volume offline or network error)." message
   - Both errors use same bus message format as success case

4. **Edge case handling:**
   - Returns early if bus is null (no subscription created)
   - Returns early if textPaneNodeId is null (no target to send to)
   - Ignores messages without conversationId in data
   - Ignores messages with wrong type (filters on `tree-browser:conversation-selected`)
   - Properly unsubscribes when hook unmounts

5. **Test results:** All 7 tests pass (77ms)

---

## Test Results

**Test file:** `browser/src/services/chat/__tests__/conversationLoader.test.ts`

```
✓ src/services/chat/__tests__/conversationLoader.test.ts (7 tests)
  ✓ should load and send conversation markdown when event is received
  ✓ should send error message when conversation not found (404)
  ✓ should send unavailable message on volume offline/network error
  ✓ should do nothing when bus is null
  ✓ should do nothing when textPaneNodeId is null
  ✓ should ignore messages without conversationId in data
  ✓ should ignore messages with wrong type

Test Files: 1 passed (1)
Tests: 7 passed (7)
Duration: 77ms
```

---

## Build Verification

Command run:
```bash
cd /c/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser && npm test -- src/services/chat/__tests__/conversationLoader.test.ts --run
```

Output:
```
 ✓ src/services/chat/__tests__/conversationLoader.test.ts (7 tests) 77ms

 Test Files  1 passed (1)
      Tests  7 passed (7)
   Start at  08:34:38
   Duration  1.82s
```

All tests pass. No build errors. Hook is ready to wire into EGG apps that have both tree-browser and text-pane components.

---

## Acceptance Criteria

- [x] New service: `browser/src/services/chat/conversationLoader.ts` created
- [x] Export `useConversationLoader(bus, textPaneNodeId)` hook — function exported and works with renderHook
- [x] Subscribe to bus messages filtered by type `tree-browser:conversation-selected`
- [x] Extract conversationId from event data (`message.data.conversationId`)
- [x] Call `chatApi.getConversation(conversationId)`
- [x] Call `chatMarkdown.serializeConversation(conversation)` to get markdown
- [x] Send markdown to text-pane via bus with `terminal:text-patch` type
- [x] Handle 404 errors (conversation not found) — sends error message
- [x] Handle volume offline errors — sends "unavailable" message
- [x] 3+ tests in `browser/src/services/chat/__tests__/conversationLoader.test.ts` — 7 tests written and passing
- [x] Tests written FIRST (TDD) — yes, tests were written before implementation
- [x] All tests pass — yes, 7/7 passing
- [x] Mock chatApi.getConversation and chatMarkdown.serializeConversation using vi.mock() — both mocked
- [x] Mock bus.subscribe and bus.send — both mocked
- [x] Test scenarios:
  - [x] Conversation found — loads and sends markdown to text-pane (test 1)
  - [x] Conversation not found (404) — sends error message (test 2)
  - [x] Volume offline — sends "unavailable" message (test 3)
- [x] No file over 500 lines — conversationLoader.ts: 70 lines, test file: 185 lines
- [x] No stubs — fully implemented loader
- [x] TDD: write tests first — yes, tests written before implementation

---

## Clock / Cost / Carbon

**Implementation Time:** ~15 minutes (reading context, writing tests, implementing hook, verifying)
**Cost:** Minimal — small focused module, no external API calls during development
**Carbon:** <1g CO₂ (local development only)

---

## Issues / Follow-ups

### Next Steps
1. **Wire the hook** into the EGG app that combines tree-browser + text-pane (follow-up task)
   - Example: `browser/src/apps/chatApp.tsx` or similar
   - Call hook in useEffect after both bus and textPaneNodeId are available

2. **Verify in E2E tests:**
   - User clicks conversation in tree-browser
   - Conversation markdown loads in text-pane
   - Error handling works (test with missing conversations, offline volumes)

### Edge Cases Handled
- Bus null: hook does nothing (safe)
- TextPaneNodeId null: hook does nothing (safe)
- Missing conversationId in event: ignored
- Wrong event type: filtered out
- API errors (404 vs network): distinguished and sent as different messages
- Unsubscription: returns cleanup function from useEffect

### Design Notes
- Hook is "dumb" — it just subscribes and forwards to bus
- All business logic delegated to chatApi and chatMarkdown
- Error messages are markdown so they render nicely in text-pane
- Nonce generation is timestamp + Math.random() for replay protection (per bus spec)
- No state management needed — purely side-effect based (useEffect pattern)

### Files Not Modified
- No existing files modified (new module only)
- No index file created (not needed — hook imported directly)
- No package.json changes
- No build config changes

---

**Task complete. Ready for review and wiring into parent EGG app.**
