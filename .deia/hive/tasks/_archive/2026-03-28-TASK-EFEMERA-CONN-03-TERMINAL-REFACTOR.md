# TASK-EFEMERA-CONN-03: Refactor Terminal Relay Mode

## Objective
Remove all efemera HTTP code from useTerminal.ts relay mode. Replace with bus event emission/subscription using the `efemera:*` namespace. After this task, the terminal primitive knows nothing about efemera HTTP endpoints.

## Context
Currently, when `routeTarget === 'relay'`, the terminal:
1. Subscribes to `channel:selected` bus events to track the active channel (lines ~182-194)
2. On Enter: POSTs directly to `/efemera/channels/{id}/messages` (lines ~468-535)
3. Sends `terminal:text-patch` bus events to text-pane with message content
4. Sends `channel:message-sent` bus events

After refactoring, the terminal:
1. Subscribes to `efemera:channel-changed` to track active channel name (for prompt label)
2. On Enter: emits `efemera:message-send` bus event with `{ content }` — connector handles the HTTP POST
3. Subscribes to `efemera:message-sent` to clear input on success
4. Subscribes to `efemera:error` to show inline errors
5. Does NOT import HIVENODE_URL for efemera purposes
6. Does NOT call fetch() for efemera endpoints

**Depends on:** TASK-EFEMERA-CONN-02 (connector must define the bus events).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (FULL FILE — 993 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260328-EFEMERA-CONNECTOR-DESIGN.md` (Section 5.1, Section 3)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\efemera\types.ts` (bus event data interfaces)

## Deliverables

### 1. Modify `browser/src/primitives/terminal/useTerminal.ts`

**REMOVE:**
- [ ] Lines ~182-194: `channel:selected` bus subscription useEffect → replaced by `efemera:channel-changed` subscription
- [ ] Lines ~468-535: Relay mode HTTP POST block (`if (routeTarget === 'relay') { ... }`) → replaced by bus event emission
- [ ] The `channel:message-sent` bus emit in the relay block → connector emits this now
- [ ] The `terminal:text-patch` bus emit in the relay block → connector sends messages to text-pane now
- [ ] The `activeChannelId` state variable → terminal no longer tracks this (connector does)
- [ ] HIVENODE_URL import IF it's only used for efemera relay (check if other routeTargets use it — canvas mode uses it, so the import stays)

**ADD:**
- [ ] New useEffect subscribing to `efemera:channel-changed` via `bus.subscribeType()`: sets `activeChannelName` for prompt display
- [ ] New useEffect subscribing to `efemera:message-sent` via `bus.subscribeType()`: no action needed (input already cleared before emit)
- [ ] New useEffect subscribing to `efemera:error` via `bus.subscribeType()`: adds error entry to terminal
- [ ] Relay mode Enter handler: emit `efemera:message-send` via `bus.send()` with target `'*'` (connector picks up via subscribeType)
- [ ] Entry for relay input: `{ type: 'input', content: text, hidden: true }` (same as before — compose bar input hidden from terminal display)

**KEEP UNCHANGED:**
- All non-relay code paths (shell, ai, ir, canvas modes)
- Command history logic
- Slash command handling
- Tab completion
- Conversation management
- Everything else

**Net result:** ~67 lines removed, ~25 lines added. File stays under 1000 lines.

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing terminal tests still pass
- [ ] New/modified test cases for relay mode behavior

### Test cases required:
- Relay mode Enter emits `efemera:message-send` on bus (not HTTP POST)
- Relay mode without active channel still works (connector handles the error)
- `efemera:channel-changed` subscription updates activeChannelName
- `efemera:error` subscription adds system entry to terminal
- Non-relay modes (shell, ai, ir, canvas) are NOT affected by changes
- No fetch() calls made for efemera endpoints in relay mode

### Where to add tests:
- Check for existing terminal test files first. If tests exist for relay mode, update them. If not, create `browser/src/primitives/terminal/__tests__/terminalRelay.test.ts`.

## Constraints
- No file over 500 lines (useTerminal.ts is currently 993 — this task should reduce it slightly)
- No stubs
- Do NOT modify any other files except useTerminal.ts and test files
- Do NOT change any non-relay code paths — this is a surgical refactor of relay mode only
- The terminal must still work for all other routeTarget values (shell, ai, ir, canvas)
- Keep `activeChannelName` state (still needed for prompt display)
- Remove `activeChannelId` state ONLY if nothing else uses it (check first)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-EFEMERA-CONN-03-RESPONSE.md`

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
