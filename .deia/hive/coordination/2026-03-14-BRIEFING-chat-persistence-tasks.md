# BRIEFING: Chat Persistence — Write 3 Task Files

**Date:** 2026-03-14
**Parent Spec:** QUEUE-TEMP-2026-03-14-0402-SPEC-chat-persistence.md
**Survey:** 20260314-Q33N-CHAT-PERSISTENCE-SURVEY.md
**Approval:** 20260314-Q88NR-CHAT-PERSISTENCE-APPROVAL.md
**Model:** sonnet
**Role:** Q33N

---

## Objective

Write 3 task files to complete the remaining 40% of chat persistence:

1. **TASK-1:** useTerminal integration with chatApi
2. **TASK-2:** Bus handler for conversation loading
3. **TASK-3:** Volume status badges

---

## Context

Your survey identified that chat persistence infrastructure is 60% implemented but NOT wired end-to-end. Q88NR has approved your recommendation to proceed with 3 focused task files.

---

## Pre-Task Research Required

Before writing task files, complete these reads:

1. **Verify markdown format:**
   - Read `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatMarkdown.ts`
   - Confirm it matches SPEC-HIVENODE-E2E-001 Section 7.2 format

2. **Count existing tests:**
   - Search for `**/*chatApi*.test.*` and `**/*chatHistory*.test.*`
   - Count how many tests exist
   - Determine how many new tests needed to reach 15+ total

3. **Check bus handler patterns:**
   - Search codebase for `tree-browser:.*-selected` patterns
   - Find examples to guide TASK-2 implementation

4. **Check volume status route:**
   - Verify if `/node/discover` route exists in hivenode (SPEC Section 9.3)
   - If not, TASK-3 must specify stubbing or alternative approach

---

## Task File Requirements

Each task file MUST include:

### Header
```markdown
# TASK-XXX: [Title]

## Objective
[One sentence: what the bee must deliver]

## Context
[What the bee needs to know. Include relevant file paths, schema details, interface contracts.]
```

### Files to Read First
- List 3-5 files with **absolute paths** (Windows format: `C:\Users\davee\...`)
- Include line number references where relevant

### Deliverables
- [ ] Concrete, testable outputs
- [ ] Each deliverable maps to an acceptance criterion from the spec

### Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases: [list specific scenarios — offline volume, error handling, etc.]
- [ ] Specify exact test count for this task

### Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (if any UI changes)
- No stubs in production code
- TDD: tests first

### Response Requirements — MANDATORY
```
When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-<TASK-ID>-RESPONSE.md`

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
```

---

## TASK-1 Outline: useTerminal Integration

**Files to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts`

**Deliverables:**
- Add conversationId state tracking
- Call chatApi.createConversation() on first message
- Call chatApi.addMessage() after each LLM response (fire-and-forget)
- Handle errors gracefully (log, don't crash)
- Volume preference from user settings or default to 'both'

**Edge cases:**
- First message in session
- Subsequent messages
- chatApi failure (network down, volume offline)
- localStorage fallback mode

**Tests:** 5 minimum

---

## TASK-2 Outline: Conversation Load Handler

**New file or existing hook?**
- Determine if handler should be in treeBrowserAdapter or a new bus service
- If new service: `browser/src/services/chat/conversationLoader.ts`

**Deliverables:**
- Subscribe to `tree-browser:conversation-selected` bus event
- Extract conversationId from event data
- Call chatApi.getConversation(id)
- Send markdown content to text-pane via `terminal:text-patch`
- Handle missing conversations (404 error)

**Edge cases:**
- Conversation not found
- Volume offline
- Text-pane not linked in EGG config

**Tests:** 3 minimum

---

## TASK-3 Outline: Volume Status Badges

**Files to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts`
- (New) `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\volumes\volumeStatus.ts`

**Deliverables:**
- Implement getVolumeStatus(volume) helper
- Call hivenode `/node/discover` or similar route to check online/offline
- Update chatHistoryAdapter to add status badge to each conversation node
- Badge values: 'online' | 'syncing' | 'conflict' | 'offline'
- Use CSS variables for badge colors

**Edge cases:**
- Volume offline (grey badge)
- Volume syncing (blue spinner badge)
- Conflict (yellow ! badge)
- Hivenode unreachable (assume offline)

**Tests:** 4 minimum

---

## File Naming Convention

```
.deia/hive/tasks/2026-03-14-TASK-XXX-<short-name>.md
```

Examples:
- `2026-03-14-TASK-077-useterminal-chat-persist.md`
- `2026-03-14-TASK-078-conversation-load-handler.md`
- `2026-03-14-TASK-079-volume-status-badges.md`

---

## What to Return to Q88NR

1. **3 task files** written to `.deia/hive/tasks/`
2. **Summary message** listing:
   - Task IDs
   - Effort estimates
   - Total test count
   - Any blockers or assumptions

**DO NOT dispatch bees yet.** Return task files for Q88NR review first.

---

## Q33N: You are cleared to proceed. Write the 3 task files.
