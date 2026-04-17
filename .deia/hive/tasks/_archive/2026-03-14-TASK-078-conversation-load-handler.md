# TASK-078: Tree-Browser Conversation Load Handler

## Objective
Build a bus subscriber that listens for `tree-browser:conversation-selected` events, loads the conversation from chatApi, and sends the markdown content to the text-pane via `terminal:text-patch`.

## Context
When a user clicks a conversation in the tree-browser, the adapter publishes a `tree-browser:conversation-selected` bus event with the conversationId. This task implements the handler that:
1. Receives the event
2. Calls `chatApi.getConversation(conversationId)`
3. Serializes the conversation to markdown (via `chatMarkdown.serializeConversation()`)
4. Sends the markdown to the text-pane via `terminal:text-patch` bus message

**What already exists:**
- chatHistoryAdapter publishes conversation nodes with `conversationId` in meta (line 69)
- chatApi.getConversation() returns ConversationWithMessages
- chatMarkdown.serializeConversation() converts to markdown
- Bus infrastructure supports `terminal:text-patch` messages (used in useTerminal.ts line 406)

**What's missing:**
- No bus subscriber for `tree-browser:conversation-selected`
- No service to handle conversation loading and routing to text-pane

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts` — conversation node structure
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (lines 169-179) — bus subscription pattern (channel:selected)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatApi.ts` — getConversation API
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatMarkdown.ts` — serializeConversation function
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` (lines 466-472) — conversation load flow

## Deliverables
- [ ] New service: `browser/src/services/chat/conversationLoader.ts`
- [ ] Export `useConversationLoader(bus, textPaneNodeId)` hook
- [ ] Subscribe to bus messages filtered by type `tree-browser:conversation-selected`
- [ ] Extract conversationId from event data (`message.data.conversationId`)
- [ ] Call `chatApi.getConversation(conversationId)`
- [ ] Call `chatMarkdown.serializeConversation(conversation)` to get markdown
- [ ] Send markdown to text-pane via bus:
  ```typescript
  bus.send({
    type: 'terminal:text-patch',
    sourcePane: 'conversation-loader',
    target: textPaneNodeId,
    nonce: `${Date.now()}-${Math.random()}`,
    timestamp: new Date().toISOString(),
    data: {
      format: 'markdown',
      ops: [{ op: 'replace', content: markdown }],
    },
  });
  ```
- [ ] Handle 404 errors (conversation not found) — send error message to text-pane
- [ ] Handle volume offline errors — send "Volume offline, conversation unavailable" to text-pane
- [ ] 3 tests in `browser/src/services/chat/__tests__/conversationLoader.test.ts`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Mock chatApi.getConversation and chatMarkdown.serializeConversation using vi.mock()
- [ ] Mock bus.subscribe and bus.send
- [ ] Test scenarios:
  - **Conversation found:** loads and sends markdown to text-pane
  - **Conversation not found (404):** sends error message to text-pane
  - **Volume offline:** sends "unavailable" message to text-pane
- [ ] Minimum 3 tests

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (no CSS in this task)
- No stubs — fully implement loader
- TDD: write tests first

## Implementation Notes

**Hook signature:**
```typescript
export function useConversationLoader(
  bus: MessageBus | null,
  textPaneNodeId: string | null
) {
  useEffect(() => {
    if (!bus || !textPaneNodeId) return;

    const unsubscribe = bus.subscribe('*', async (message: any) => {
      if (message.type !== 'tree-browser:conversation-selected') return;

      const conversationId = message.data?.conversationId;
      if (!conversationId) return;

      try {
        const conversation = await getConversation(conversationId);
        const markdown = serializeConversation(conversation);

        bus.send({
          type: 'terminal:text-patch',
          sourcePane: 'conversation-loader',
          target: textPaneNodeId,
          nonce: `${Date.now()}-${Math.random()}`,
          timestamp: new Date().toISOString(),
          data: {
            format: 'markdown',
            ops: [{ op: 'replace', content: markdown }],
          },
        });
      } catch (error: any) {
        const errorMsg = error.message?.includes('not found')
          ? '**Error:** Conversation not found.'
          : '**Error:** Unable to load conversation (volume offline or network error).';

        bus.send({
          type: 'terminal:text-patch',
          sourcePane: 'conversation-loader',
          target: textPaneNodeId,
          nonce: `${Date.now()}-${Math.random()}`,
          timestamp: new Date().toISOString(),
          data: {
            format: 'markdown',
            ops: [{ op: 'replace', content: errorMsg }],
          },
        });
      }
    });

    return unsubscribe;
  }, [bus, textPaneNodeId]);
}
```

**Where to wire it:**
- This hook should be called in the EGG app that has both tree-browser (for chat history) and text-pane
- Example: `browser/src/apps/chatApp.tsx` (if exists) or wherever the chat EGG is initialized
- For now, create the service — wiring will be done in a follow-up task

**Edge cases:**
- If textPaneNodeId is null, do nothing (no target to send to)
- If conversationId is missing from event data, ignore the message
- If getConversation throws 404, show friendly error
- If getConversation throws network error, show "volume offline" message

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260314-TASK-078-RESPONSE.md`

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
