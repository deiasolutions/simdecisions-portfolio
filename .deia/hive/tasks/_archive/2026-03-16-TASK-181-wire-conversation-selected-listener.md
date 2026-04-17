# TASK-181: Wire conversation:selected listener in useTerminal

## Objective
Add bus listener for `conversation:selected` event in useTerminal.ts that loads the clicked conversation and replaces terminal entries with the conversation's messages.

## Context

**Dependency: TASK-180 must complete first** — this task uses `loadConversationToEntries()` from terminalChatPersist.ts.

When a user clicks a conversation in tree-browser:
1. ChatNavigatorPane publishes `conversation:selected` event with `{ conversationId, path, volume }`
2. Terminal needs to listen for this event
3. Load the conversation using `loadConversationToEntries(conversationId)`
4. Replace current entries with: `[{ type: 'banner', content: WELCOME_BANNER }, ...loadedEntries]`
5. Set `conversationId` state so new messages append to this conversation
6. Update ledger totals from loaded message metrics

### Existing pattern (channel:selected for efemera chat):

```typescript
// useTerminal.ts lines 174-184
useEffect(() => {
  if (routeTarget !== 'relay' || !bus || !nodeId) return;
  const unsubscribe = bus.subscribe(nodeId, (message: any) => {
    if (message.type === 'channel:selected' && message.data) {
      setActiveChannelId(message.data.channelId);
      setActiveChannelName(message.data.channelName);
    }
  });
  return unsubscribe;
}, [routeTarget, bus, nodeId]);
```

We need to add a similar listener for `conversation:selected` but NOT restricted to `routeTarget === 'relay'` — it should work for all route targets.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (844 lines — add listener here)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminalChatPersist.ts` (after TASK-180 completes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts` (100 lines — ConversationSelectedData type)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\ChatNavigatorPane.tsx` (216 lines — event publisher)

## Deliverables

- [ ] Add new `useEffect` block in useTerminal.ts for conversation loading
- [ ] Listener subscribes to bus when `bus` and `nodeId` are available (no routeTarget restriction)
- [ ] On `message.type === 'conversation:selected'`:
  - [ ] Call `loadConversationToEntries(message.data.conversationId)`
  - [ ] Replace entries: `setEntries([{ type: 'banner', content: WELCOME_BANNER }, ...loadedEntries])`
  - [ ] Set conversation state: `setConversationId(message.data.conversationId)`
  - [ ] Update ledger totals from message metrics
- [ ] Error handling: log error but don't crash if conversation load fails
- [ ] Return cleanup function to unsubscribe

## Implementation Details

### Ledger calculation from loaded messages:

```typescript
// Recalculate ledger totals from loaded entries
const newLedger: SessionLedger = {
  total_clock_ms: 0,
  total_cost_usd: 0,
  total_carbon_g: 0,
  total_input_tokens: 0,
  total_output_tokens: 0,
  message_count: 0,
};

for (const entry of loadedEntries) {
  if (entry.type === 'response' && entry.metrics) {
    newLedger.total_clock_ms += entry.metrics.clock_ms;
    newLedger.total_cost_usd += entry.metrics.cost_usd;
    newLedger.total_carbon_g += entry.metrics.carbon_g;
    newLedger.total_input_tokens += entry.metrics.input_tokens;
    newLedger.total_output_tokens += entry.metrics.output_tokens;
    newLedger.message_count += 1;
  }
}

setLedger(newLedger);
```

### Suggested code location:

Add the new useEffect block after the existing channel:selected listener (after line 184).

## Test Requirements

Add tests to `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\useTerminal.chatPersist.test.ts`:

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - ✅ Conversation loads when `conversation:selected` event fires
  - ✅ Entries are replaced with loaded messages
  - ✅ Banner is prepended to entries
  - ✅ conversationId state is set correctly
  - ✅ Ledger totals update from message metrics
  - ✅ Error logged (not thrown) if conversation not found
  - ✅ Listener only active when bus and nodeId are available
  - ✅ Unsubscribes on cleanup

Test count target: **8 tests minimum**

## Constraints

- No file over 500 lines (useTerminal.ts is 844 lines — ALREADY OVER LIMIT)
  - **This task should NOT increase file size significantly** (add ~40 lines max)
  - If file would exceed 900 lines, STOP and report to Q33N
- CSS: var(--sd-*) only (no CSS in this task)
- No stubs — full implementation
- Follow existing bus subscription pattern (see channel:selected listener)
- Fire-and-forget error handling (log errors, don't crash)

## Acceptance Criteria

- [ ] Bus listener for `conversation:selected` added
- [ ] Listener loads conversation and replaces entries
- [ ] Banner prepended to loaded entries
- [ ] conversationId state updated
- [ ] Ledger totals recalculated from loaded messages
- [ ] Error handling: logs error but doesn't crash
- [ ] Cleanup: unsubscribes on unmount
- [ ] 8+ tests written and passing
- [ ] No new test failures in existing terminal tests
- [ ] File stays under 900 lines total

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-181-RESPONSE.md`

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

## File Claims

Before modifying any file, claim it:
```bash
curl -X POST http://localhost:8420/build/claim \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-181", "files": ["browser/src/primitives/terminal/useTerminal.ts", "browser/src/primitives/terminal/__tests__/useTerminal.chatPersist.test.ts"]}'
```

Release when done:
```bash
curl -X POST http://localhost:8420/build/release \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-181", "files": ["browser/src/primitives/terminal/useTerminal.ts"]}'
```

## Heartbeats

POST to `http://localhost:8420/build/heartbeat` every 3 minutes:
```json
{
  "task_id": "TASK-181",
  "status": "running",
  "model": "haiku",
  "message": "Wiring conversation loader"
}
```

Final heartbeat on completion:
```json
{
  "task_id": "TASK-181",
  "status": "complete",
  "model": "haiku",
  "message": "8 tests passing, listener wired"
}
```

## Dependency Note

**WAIT FOR TASK-180 TO COMPLETE** before starting this task. You need `loadConversationToEntries()` from terminalChatPersist.ts.
