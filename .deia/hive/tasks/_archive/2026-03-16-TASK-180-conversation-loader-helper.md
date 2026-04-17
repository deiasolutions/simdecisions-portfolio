# TASK-180: Add conversation loader helper to terminalChatPersist

## Objective
Add `loadConversationToEntries()` helper function to `terminalChatPersist.ts` that loads a conversation from chatApi and converts messages to TerminalEntry format.

## Context

Currently terminalChatPersist.ts only handles saving messages (via `persistChatMessages()`). We need the reverse operation: loading a conversation and converting its messages back to terminal entries.

When a user clicks a conversation in tree-browser, the terminal needs to:
1. Call `chatApi.getConversation(conversationId)`
2. Convert each Message to a TerminalEntry
3. Return the array of entries for terminal display

### Message → TerminalEntry conversion rules:

**Message with role: 'user':**
```typescript
{
  type: 'input',
  content: message.content,
  timestamp: message.created_at
}
```

**Message with role: 'assistant':**
```typescript
{
  type: 'response',
  content: message.content,
  timestamp: message.created_at,
  metrics: {
    model: message.model || 'unknown',
    clock_ms: message.clock_ms || 0,
    cost_usd: message.cost_usd || 0,
    carbon_g: message.carbon_g || 0,
    input_tokens: message.input_tokens || 0,
    output_tokens: message.output_tokens || 0,
  }
}
```

**Message with role: 'system':**
```typescript
{
  type: 'system',
  content: message.content
}
```

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminalChatPersist.ts` (58 lines — add new function here)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatApi.ts` (411 lines — getConversation API)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\types.ts` (109 lines — Message, Conversation types)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts` (100 lines — TerminalEntry types)

## Deliverables

- [ ] Add `loadConversationToEntries(conversationId: string): Promise<TerminalEntry[]>` to terminalChatPersist.ts
- [ ] Function calls `chatApi.getConversation(conversationId)`
- [ ] Function converts each message to appropriate TerminalEntry type
- [ ] Function handles missing metrics fields gracefully (default to 0)
- [ ] Function throws error if conversation not found
- [ ] Export the new function from terminalChatPersist.ts

## Test Requirements

Add tests to `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\useTerminal.chatPersist.test.ts`:

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - ✅ Loads conversation with multiple messages
  - ✅ Converts user messages to 'input' entries
  - ✅ Converts assistant messages to 'response' entries with metrics
  - ✅ Converts system messages to 'system' entries
  - ✅ Handles missing metrics fields (defaults to 0)
  - ✅ Throws error when conversation not found
  - ✅ Preserves timestamps
  - ✅ Empty conversation returns empty array

Test count target: **8 tests minimum**

## Constraints

- No file over 500 lines (terminalChatPersist.ts is 58 lines, safe to add ~50 lines)
- CSS: var(--sd-*) only (no CSS in this task)
- No stubs — full implementation
- Use existing chatApi functions (don't reimplement storage logic)
- Fire-and-forget error handling pattern (log errors, don't crash)

## Acceptance Criteria

- [ ] `loadConversationToEntries()` function added and exported
- [ ] Function converts all message types correctly
- [ ] Function handles missing metrics gracefully
- [ ] 8+ tests written and passing
- [ ] No new test failures in existing terminal tests
- [ ] File stays under 150 lines total

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-180-RESPONSE.md`

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
  -d '{"task_id": "TASK-180", "files": ["browser/src/primitives/terminal/terminalChatPersist.ts", "browser/src/primitives/terminal/__tests__/useTerminal.chatPersist.test.ts"]}'
```

Release when done:
```bash
curl -X POST http://localhost:8420/build/release \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-180", "files": ["browser/src/primitives/terminal/terminalChatPersist.ts"]}'
```

## Heartbeats

POST to `http://localhost:8420/build/heartbeat` every 3 minutes:
```json
{
  "task_id": "TASK-180",
  "status": "running",
  "model": "haiku",
  "message": "Converting messages to entries"
}
```

Final heartbeat on completion:
```json
{
  "task_id": "TASK-180",
  "status": "complete",
  "model": "haiku",
  "message": "8 tests passing"
}
```
