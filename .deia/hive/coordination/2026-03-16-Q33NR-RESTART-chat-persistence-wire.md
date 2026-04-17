# Q33NR RESTART BRIEFING: Complete Chat Persistence Wire

**Date:** 2026-03-16
**Restart Attempt:** 1/2
**Original Spec:** QUEUE-TEMP-2026-03-16-1035-SPEC-w2-08-chat-persistence-wire
**Previous Bot:** REGENT-QUEUE-TEMP-2026-03-16-1035-SPE (timed out)

---

## Situation

Previous queen timed out after dispatching bees for tree-browser features (drag/drop, file selection). However, the **original spec was about chat persistence**, not tree browser features.

## What Was Completed

✅ **TASK-180: conversation-loader-helper**
- Function `loadConversationToEntries()` exists in terminalChatPersist.ts (lines 78-114)
- Converts Message objects to TerminalEntry objects
- Tests passing (17 tests in useTerminal.chatPersist.test.ts)

✅ **Tree browser work** (unrelated to chat persistence, but completed):
- TreeNodeRow drag data transfer
- file:selected bus events

## What Remains

❌ **TASK-181: Wire conversation:selected listener**
- useTerminal.ts does NOT have a `conversation:selected` listener
- When user clicks conversation in tree-browser, terminal doesn't reload it
- Original task file exists: `.deia/hive/tasks/2026-03-16-TASK-181-wire-conversation-selected-listener.md`

## Spec Acceptance Criteria Status

- [x] Conversations save automatically (already working)
- [x] Tree-browser shows conversation list (already working)
- [ ] **Clicking conversation reloads it** ← MISSING
- [x] Tests written and passing (for completed parts)

---

## Your Task

Review the existing TASK-181 file and dispatch a bee to complete it:

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-16-TASK-181-wire-conversation-selected-listener.md`

**What it needs to do:**
1. Add `useEffect` block in useTerminal.ts
2. Subscribe to bus for `conversation:selected` events
3. Call `loadConversationToEntries(conversationId)` when event fires
4. Replace terminal entries with loaded conversation
5. Update conversationId state
6. Recalculate ledger totals

**Expected changes:**
- useTerminal.ts: +40 lines (currently 844 lines, will be ~884)
- Tests: +8 tests in useTerminal.chatPersist.test.ts

**Constraints:**
- File must stay under 900 lines (hard limit 1000)
- TDD: tests first
- No stubs

---

## Dispatch Command

```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-16-TASK-181-wire-conversation-selected-listener.md \
  --model haiku --role bee --inject-boot --timeout 1200
```

---

## Success Criteria

After bee completes:
1. useTerminal.ts has conversation:selected listener
2. Clicking conversation in tree-browser reloads terminal
3. All tests pass (including 8 new tests)
4. Spec acceptance criteria all met
5. Response file written with all 8 sections

---

**Q33NR (Restart Queen)**
Bot ID: REGENT-QUEUE-TEMP-2026-03-16-1035-SPE (restart attempt 1)
