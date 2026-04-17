# TASK-EFEMERA-CONN-04: Refactor Text-Pane Chat Mode

## Objective
Remove all efemera HTTP code from SDEditor.tsx. Replace with bus event subscriptions using the `efemera:*` namespace. After this task, the text-pane primitive knows nothing about efemera HTTP endpoints.

## Context
Currently, SDEditor.tsx in chat mode:
1. On `channel:selected` bus event: fetches messages from `/efemera/channels/{id}/messages` directly (lines ~369-398)
2. On `channel:message-received` bus event: appends message content (lines ~401-410)

After refactoring:
1. On `efemera:messages-loaded`: replaces content with full message history (connector fetched it)
2. On `efemera:message-received`: appends single new message
3. On `efemera:channel-changed`: clears content, shows loading state
4. On `efemera:typing` / `efemera:typing-stop`: shows/hides typing indicator
5. Does NOT import HIVENODE_URL for efemera purposes
6. Does NOT call fetch() for efemera endpoints

**Depends on:** TASK-EFEMERA-CONN-02 (connector must define the bus events).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx` (FULL FILE — 810 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260328-EFEMERA-CONNECTOR-DESIGN.md` (Section 5.2, Section 3)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\efemera\types.ts` (bus event data interfaces)

## Deliverables

### 1. Modify `browser/src/primitives/text-pane/SDEditor.tsx`

**REMOVE:**
- [ ] Lines ~369-398: `channel:selected` handler that fetches from `/efemera/channels/{id}/messages` → connector does this now
- [ ] Lines ~401-410: `channel:message-received` handler that appends content → replaced by `efemera:message-received`
- [ ] HIVENODE_URL import IF it's only used for efemera (check — it's also used for file:selected storage fetch, so the import likely stays)

**ADD:**
- [ ] In the bus subscription useEffect, add handler for `efemera:channel-changed`: clear content, set label to `#channelName`, show loading state
- [ ] In the bus subscription useEffect, add handler for `efemera:messages-loaded`: render full message history using the same format (bold author + content)
- [ ] In the bus subscription useEffect, add handler for `efemera:message-received`: append single message (same format as current channel:message-received handler)
- [ ] In the bus subscription useEffect, add handler for `efemera:typing`: set typing indicator state
- [ ] In the bus subscription useEffect, add handler for `efemera:typing-stop`: clear typing indicator state

**KEEP UNCHANGED:**
- All non-efemera bus handlers (terminal:text-patch, file:selected, terminal:targeting, etc.)
- All mode logic (document, raw, code, diff, process-intake, chat)
- Co-Author functionality
- Menu bar and header rendering
- Content persistence
- Everything else

**Net result:** ~42 lines removed, ~30 lines added. File stays well under 1000 lines.

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing text-pane tests still pass
- [ ] New/modified test cases for efemera event handling

### Test cases required:
- `efemera:channel-changed` in chat mode: clears content, updates label
- `efemera:messages-loaded` in chat mode: renders full message list
- `efemera:message-received` in chat mode: appends single message
- `efemera:typing` in chat mode: sets typing indicator
- `efemera:typing-stop` in chat mode: clears typing indicator
- Non-chat modes ignore efemera events
- `terminal:text-patch` handler still works (not broken by changes)
- `file:selected` handler still works (not broken by changes)

### Where to add tests:
- Check for existing SDEditor test files first. If tests for chat mode bus handling exist, update them. If not, create `browser/src/primitives/text-pane/__tests__/sdEditorEfemera.test.tsx`.

## Constraints
- No file over 500 lines (SDEditor.tsx is currently 810 — this task should reduce it slightly)
- No stubs
- Do NOT modify any other files except SDEditor.tsx and test files
- Do NOT change any non-chat-mode code paths
- Do NOT change how `terminal:text-patch` works — that's used by AI chat mode too
- Keep the existing bus subscription pattern (single subscribe to paneContext.nodeId)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-EFEMERA-CONN-04-RESPONSE.md`

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
