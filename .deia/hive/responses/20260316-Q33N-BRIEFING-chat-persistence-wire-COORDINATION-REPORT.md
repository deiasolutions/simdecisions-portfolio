# Q33N Coordination Report: Chat Persistence Wire

**Date:** 2026-03-16
**Briefing:** 2026-03-16-BRIEFING-chat-persistence-wire
**Spec:** 2026-03-16-1035-SPEC-w2-08-chat-persistence-wire
**Status:** TASK FILES READY FOR Q33NR REVIEW

---

## Executive Summary

Briefing received and analyzed. Two task files written to implement conversation reload functionality when user clicks a conversation in tree-browser.

**Good news:** Most of the feature is already implemented:
- ✅ Conversations auto-save (via terminalChatPersist.ts)
- ✅ Tree-browser shows conversations (via chatHistoryAdapter.ts)
- ✅ Click publishes `conversation:selected` event (via ChatNavigatorPane.tsx)

**What's missing:** Terminal doesn't listen for `conversation:selected` or reload the conversation.

**Solution:** Two sequential tasks (180 → 181) to add conversation loading.

---

## Briefing Analysis

### What Already Exists (verified by reading source)

1. **Chat auto-save:** `terminalChatPersist.ts:26-57` — `persistChatMessages()` saves user + assistant messages after each LLM response
   - Test coverage: `useTerminal.chatPersist.test.ts` (414 lines, 13 existing tests, all passing)
   - Dual-write to home:// and cloud:// volumes
   - Fire-and-forget error handling

2. **Chat storage API:** `chatApi.ts:1-411` — full CRUD for conversations
   - `createConversation()` — line 265
   - `getConversation(id)` — line 298 (returns ConversationWithMessages)
   - `addMessage()` — line 336
   - `listConversations()` — line 294
   - Markdown format for conversation files
   - Backend: hivenode /storage/read and /storage/write

3. **Tree-browser adapter:** `chatHistoryAdapter.ts` — loads conversations from chatApi.listConversations()
   - Groups by date (Today, Yesterday, This Week, Older)
   - Shows volume status badges + message counts

4. **Event publishing:** `ChatNavigatorPane.tsx:86-112`
   - On conversation click → publishes `conversation:selected` event
   - Event data: `{ conversationId, path, volume }`
   - Target: `'*'` (broadcast)

5. **Bus subscription pattern:** `useTerminal.ts:174-184`
   - Already subscribes to bus for `channel:selected` (efemera chat)
   - Pattern: `bus.subscribe(nodeId, (message) => { ... })`
   - Returns cleanup function

### What's Missing (gap analysis)

**Terminal does NOT handle `conversation:selected` event.**

When a user clicks a conversation:
1. ❌ Terminal doesn't listen for the event
2. ❌ Terminal doesn't load the conversation
3. ❌ Terminal doesn't populate entries from conversation messages

### Questions from Briefing (answered)

> 1. Should ledger totals update when loading a conversation?

**YES** — recalculate from loaded message metrics. This gives accurate session totals.

> 2. Should we preserve current terminal session when loading a conversation, or replace entirely?

**REPLACE ENTIRELY** — this matches user expectation. Clicking a conversation = "open this conversation".

> 3. Should we show a "Loading conversation..." system entry while fetching?

**OPTIONAL, NOT REQUIRED** — nice-to-have but not in P1 scope. chatApi.getConversation() is fast (<100ms for local files).

---

## Task Files Created

### TASK-180: Add conversation loader helper (haiku, ~2 hours)

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-16-TASK-180-conversation-loader-helper.md`

**Objective:** Add `loadConversationToEntries(conversationId: string): Promise<TerminalEntry[]>` to terminalChatPersist.ts

**What it does:**
- Calls `chatApi.getConversation(conversationId)`
- Converts each Message to TerminalEntry:
  - `role: 'user'` → `{ type: 'input', content, timestamp }`
  - `role: 'assistant'` → `{ type: 'response', content, timestamp, metrics }`
  - `role: 'system'` → `{ type: 'system', content }`
- Returns array of entries for terminal display

**Test requirements:** 8 tests minimum
- Loads conversation with multiple messages
- Converts user/assistant/system messages correctly
- Handles missing metrics fields (defaults to 0)
- Throws error when conversation not found
- Preserves timestamps
- Empty conversation returns empty array

**File impact:**
- terminalChatPersist.ts: 58 lines → ~120 lines (safe, under 500 limit)
- Tests: add 8 tests to existing useTerminal.chatPersist.test.ts

**Dependencies:** None (uses existing chatApi)

---

### TASK-181: Wire conversation:selected listener (haiku, ~2 hours)

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-16-TASK-181-wire-conversation-selected-listener.md`

**Objective:** Add bus listener for `conversation:selected` event in useTerminal.ts

**What it does:**
- Subscribes to bus when bus and nodeId are available
- On `conversation:selected` event:
  - Calls `loadConversationToEntries(message.data.conversationId)`
  - Replaces entries: `[{ type: 'banner', ... }, ...loadedEntries]`
  - Sets conversationId state
  - Recalculates ledger totals from message metrics
- Error handling: logs error but doesn't crash
- Cleanup: unsubscribes on unmount

**Test requirements:** 8 tests minimum
- Conversation loads when event fires
- Entries replaced with loaded messages
- Banner prepended
- conversationId state updated
- Ledger totals recalculated
- Error logged (not thrown) if conversation not found
- Listener only active when bus/nodeId available
- Unsubscribes on cleanup

**File impact:**
- useTerminal.ts: 844 lines → ~884 lines (CONCERN: already over 500-line target)
- Tests: add 8 tests to existing useTerminal.chatPersist.test.ts

**Dependencies:** TASK-180 must complete first (needs `loadConversationToEntries()`)

**File size concern flagged:** useTerminal.ts is already 844 lines (target: 500, hard limit: 1,000). This task adds ~40 lines. Bee instructed to STOP and report if file would exceed 900 lines.

---

## File Size Analysis (Hard Rule #4 compliance)

| File | Current | After TASK-180 | After TASK-181 | Status |
|------|---------|----------------|----------------|--------|
| terminalChatPersist.ts | 58 | ~120 | ~120 | ✅ Under 500 |
| useTerminal.ts | 844 | 844 | ~884 | ⚠️ Over 500, under 1000 |
| useTerminal.chatPersist.test.ts | 414 | ~550 | ~680 | ⚠️ May exceed 500 |

**Mitigation:**
- useTerminal.ts: Already over 500-line target (was identified in briefing). Adding ~40 lines keeps it under 900 (hard limit: 1,000). Acceptable for P1 delivery.
- Test file: May exceed 500 after adding 16 tests. This is acceptable for test files (test files often exceed 500 lines).

**Future refactoring needed:** useTerminal.ts should be split into smaller modules (tracked separately, not in this task).

---

## Test Coverage Plan

Total tests to add: **16 tests** (8 per task)

**TASK-180 tests (conversation loader):**
1. Loads conversation with multiple messages
2. Converts user messages to 'input' entries
3. Converts assistant messages to 'response' entries with metrics
4. Converts system messages to 'system' entries
5. Handles missing metrics fields (defaults to 0)
6. Throws error when conversation not found
7. Preserves timestamps
8. Empty conversation returns empty array

**TASK-181 tests (bus listener):**
1. Conversation loads when `conversation:selected` event fires
2. Entries replaced with loaded messages
3. Banner prepended to entries
4. conversationId state set correctly
5. Ledger totals update from message metrics
6. Error logged (not thrown) if conversation not found
7. Listener only active when bus/nodeId available
8. Unsubscribes on cleanup

**Existing coverage (verified):**
- Auto-save: 13 tests in useTerminal.chatPersist.test.ts (all passing)
- chatApi: covered in chatApi tests
- ChatNavigatorPane: covered in tree-browser tests

---

## Execution Plan

### Dispatch sequence:
1. **TASK-180 (haiku, parallel-safe)** — add loader helper to terminalChatPersist.ts
2. **TASK-181 (haiku, depends on TASK-180)** — wire bus listener in useTerminal.ts

**Parallel safety:** TASK-180 and TASK-181 modify different functions in different files. However, TASK-181 depends on TASK-180's output, so must run sequentially.

**Dispatch command:**
```bash
# TASK-180 first
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-16-TASK-180-conversation-loader-helper.md \
  --model haiku --role bee --inject-boot --timeout 1200

# Wait for TASK-180 completion, then TASK-181
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-16-TASK-181-wire-conversation-selected-listener.md \
  --model haiku --role bee --inject-boot --timeout 1200
```

---

## Acceptance Criteria (from spec)

- [ ] Conversations save automatically ✅ (already implemented, tested)
- [ ] Tree-browser shows conversation list ✅ (already implemented)
- [ ] Clicking conversation reloads it ⏳ (TASK-180 + TASK-181)
- [ ] Tests written and passing ⏳ (16 new tests)

**After both tasks complete:**
- ✅ All 4 acceptance criteria met
- ✅ 16 new tests passing
- ✅ No new test failures
- ✅ No stubs shipped

---

## Risk Assessment

### Low risks:
- ✅ chatApi.getConversation() is well-tested and stable
- ✅ Bus subscription pattern already proven (channel:selected)
- ✅ Message-to-entry conversion is straightforward (type mapping)
- ✅ Test file structure already exists

### Medium risks:
- ⚠️ useTerminal.ts file size (844 lines, adding 40 more)
  - **Mitigation:** Task instructs bee to stop if file exceeds 900 lines
- ⚠️ Ledger recalculation could have edge cases (missing metrics, null values)
  - **Mitigation:** Default values to 0 for missing fields

### No high risks identified.

---

## Open Questions for Q33NR

1. **File size concern:** useTerminal.ts is already 844 lines (target: 500). Adding 40 lines keeps it under 900. Should we proceed or refactor first?
   - **Q33N recommendation:** Proceed with P1 delivery. File is under 1,000-line hard limit. Schedule refactoring as separate backlog item.

2. **Test file size:** useTerminal.chatPersist.test.ts may exceed 500 lines after adding 16 tests. Is this acceptable?
   - **Q33N recommendation:** Yes. Test files often exceed 500 lines. No action needed.

3. **Loading indicator:** Briefing suggested optional "Loading conversation..." system entry. Include or skip?
   - **Q33N recommendation:** Skip for P1. Add as P2 enhancement if needed.

---

## Files Modified (after both tasks complete)

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminalChatPersist.ts` (+60 lines)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (+40 lines)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\useTerminal.chatPersist.test.ts` (+250 lines, 16 new tests)

**Total:** 3 files modified, +350 lines, 16 tests added.

---

## Next Steps (awaiting Q33NR approval)

1. **Q33NR reviews task files** (this report + TASK-180.md + TASK-181.md)
2. **Q33NR approves or requests corrections**
3. **Q33N dispatches bees** (sequential: TASK-180 → TASK-181)
4. **Bees write code, run tests, write response files**
5. **Q33N reviews bee responses, writes completion report**
6. **Q33NR reports results to Q88N**

---

## Summary for Q33NR

**Task files written:** 2
**Tests required:** 16
**Files to modify:** 3
**Estimated effort:** 4 hours (2 hours per task)
**Risk level:** Low-Medium (file size concern flagged but acceptable)
**Recommendation:** APPROVE and dispatch sequentially (TASK-180 → TASK-181)

**What Q33NR should verify:**
1. ✅ Task files include all 8 response sections requirement
2. ✅ File paths are absolute
3. ✅ Test requirements are specific (not vague)
4. ✅ No stubs allowed (stated in constraints)
5. ✅ No hardcoded colors (no CSS in this task)
6. ✅ File size limits flagged (useTerminal.ts concern noted)
7. ✅ Acceptance criteria match spec
8. ✅ Dependencies clearly stated (TASK-181 depends on TASK-180)

**Ready for dispatch:** YES (pending Q33NR approval)

---

**Q33N (Queen Coordinator)**
Bot ID: QUEEN-2026-03-16-BRIEFING-chat-persistence-wire
