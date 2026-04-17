# TASK-077: useTerminal Conversation Persistence Integration

## Objective
Wire useTerminal to call chatApi functions (createConversation, addMessage) to enable dual-write chat persistence to cloud:// and home:// volumes.

## Context
The chat persistence infrastructure exists in `chatApi.ts` (dual-write, localStorage fallback, markdown serialization) but **useTerminal does not call it**. This task wires the hooks so every conversation is automatically persisted.

**What already exists:**
- `chatApi.createConversation()` — creates conversation, returns { id, resume_code, ... }
- `chatApi.addMessage(conversationId, message)` — appends message to conversation, dual-writes to volumes
- `chatMarkdown.ts` — serializes conversations to markdown with YAML frontmatter
- useTerminal already has `conversationId` and `resumeCode` state (lines 97-98)
- useTerminal already calls `createConversation()` on mount (lines 155-167)

**What's missing:**
- `addMessage()` is NEVER called after LLM responses
- Volume preference is not read from user settings
- Error handling for chatApi failures

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (lines 1-718) — current hook implementation
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatApi.ts` — persistence API
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\types.ts` — Message and Conversation types
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\settingsStore.ts` — user settings (check for volume_preference key)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\__tests__\chatApi.test.ts` — existing test patterns

## Deliverables
- [ ] After each LLM response in `useTerminal.handleSubmit()`, call `chatApi.addMessage()` with user message + assistant response
- [ ] Fire-and-forget: use `.catch()` to log errors without blocking the UI
- [ ] Read volume preference from settings store (key: `sd_user_settings.volume_preference` or default to 'both')
- [ ] Pass volume preference to `createConversation(title, volumePreference)`
- [ ] Ensure user messages and assistant messages are both persisted with correct role and metrics
- [ ] If conversationId is null, createConversation before calling addMessage
- [ ] 5 tests in new file: `browser/src/primitives/terminal/__tests__/useTerminal.chatPersist.test.ts`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Mock chatApi functions using vi.mock()
- [ ] Test scenarios:
  - **First message:** createConversation called, addMessage called for user + assistant
  - **Subsequent messages:** only addMessage called (no duplicate createConversation)
  - **chatApi failure:** error logged, terminal still functional (no crash)
  - **Volume preference:** reads from settings, defaults to 'both'
  - **No conversationId:** creates conversation before calling addMessage
- [ ] Minimum 5 tests

## Constraints
- No file over 500 lines (useTerminal.ts is currently 718 lines — extract helper if needed)
- CSS: var(--sd-*) only (no CSS changes expected)
- No stubs — fully implement addMessage calls
- TDD: write tests first

## Implementation Notes

**Where to add the addMessage call:**
- After line 561 (ledger update) in `handleSubmit()`, add:
  ```typescript
  // Persist user message + assistant response
  if (conversationId) {
    chatApi.addMessage(conversationId, {
      role: 'user',
      content: finalText,
    }).catch(err => console.warn('[useTerminal] Failed to persist user message:', err));

    chatApi.addMessage(conversationId, {
      role: 'assistant',
      content: displayContent,
      model: metrics.model,
      clock_ms: metrics.clock_ms,
      cost_usd: metrics.cost_usd,
      carbon_g: metrics.carbon_g,
      input_tokens: metrics.input_tokens,
      output_tokens: metrics.output_tokens,
    }).catch(err => console.warn('[useTerminal] Failed to persist assistant message:', err));
  }
  ```

**Volume preference:**
- Read from `localStorage.getItem('sd_user_settings')`, parse JSON, extract `volume_preference` field
- Default to 'both' if missing
- Pass to createConversation call on line 158

**Edge cases:**
- If chatApi.addMessage() throws (network down, volume offline), log the error but don't crash the terminal
- If conversationId is null when addMessage is needed, call createConversation first

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260314-TASK-077-RESPONSE.md`

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
