# TASK-EFEMERA-CONN-02: Create Efemera Connector Orchestrator

## Objective
Create the EfemeraConnector class that orchestrates all efemera sub-services (channelService, messageService, presenceService, memberService) and wires them to the MessageBus via the `efemera:*` event namespace.

## Context
CONN-01 created the data layer (HTTP services). This task builds the orchestrator that:
1. Subscribes to bus events from primitives (efemera:channel-select, efemera:message-send, etc.)
2. Calls the appropriate data service method
3. Emits result bus events back to primitives (efemera:channels-loaded, efemera:message-received, etc.)
4. Manages lifecycle (start/stop)

The connector is the ONLY code that bridges bus events to HTTP services. Primitives never call services directly.

**Depends on:** TASK-EFEMERA-CONN-01 (data layer must exist).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260328-EFEMERA-CONNECTOR-DESIGN.md` (Sections 3, 4.1, 6, 7)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\efemera\types.ts` (created by CONN-01)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\efemera\channelService.ts` (created by CONN-01)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\efemera\messageService.ts` (created by CONN-01)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\efemera\presenceService.ts` (created by CONN-01)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\efemera\memberService.ts` (created by CONN-01)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\messageBus.ts` (bus API)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts` (message types)

## Deliverables

### 1. `browser/src/services/efemera/EfemeraConnector.ts` (~180 lines)

**Constructor:**
- [ ] Accepts `EfemeraConnectorOptions`: bus (MessageBus), paneIds ({ channels, messages, compose, members }), userId?, displayName?, pollingIntervalMs? (default 3000), presenceAutoIdleMs? (default 300000)
- [ ] Instantiates all 4 sub-services internally

**start() method:**
- [ ] Subscribe to `efemera:channel-select` via `bus.subscribeType()` → calls handleChannelSelect
- [ ] Subscribe to `efemera:message-send` via `bus.subscribeType()` → calls handleMessageSend
- [ ] Subscribe to `efemera:channel-create` via `bus.subscribeType()` → calls handleChannelCreate
- [ ] Subscribe to `efemera:presence-update` via `bus.subscribeType()` → calls handlePresenceUpdate
- [ ] Call `channelService.loadChannels()` → emit `efemera:channels-loaded` to broadcast
- [ ] Register `messageService.onNewMessages()` callback → emit `efemera:message-received` to messages pane
- [ ] Start `presenceService` with `onStatusChange` callback → emit `efemera:presence-changed`
- [ ] Emit `efemera:ready` broadcast
- [ ] Store all unsubscribe functions for cleanup

**stop() method:**
- [ ] Call all stored unsubscribe functions
- [ ] Call `messageService.stopPolling()`
- [ ] Call `presenceService.stop()`
- [ ] Clear internal state (activeChannelId, etc.)

**handleChannelSelect(data):**
- [ ] Set activeChannelId
- [ ] Emit `efemera:channel-changed` broadcast with channelId, channelName
- [ ] Stop current polling
- [ ] Call `messageService.loadMessages(channelId)` → emit `efemera:messages-loaded` to messages pane
- [ ] Start polling for new channel
- [ ] Call `memberService.loadMembers(channelId)` → emit `efemera:members-loaded` to members pane
- [ ] On error: emit `efemera:error` broadcast

**handleMessageSend(data):**
- [ ] Validate activeChannelId exists, emit error if not
- [ ] Call `messageService.sendMessage(activeChannelId, data.content, userId, displayName, data.replyToId?)`
- [ ] On success: emit `efemera:message-sent` to compose pane AND `efemera:message-received` to messages pane
- [ ] On error: emit `efemera:error` broadcast

**handleChannelCreate(data):**
- [ ] Call `channelService.createChannel(data.name, data.type, data.description?)`
- [ ] On success: reload channels → emit `efemera:channels-loaded` broadcast
- [ ] On error: emit `efemera:error` broadcast

**handlePresenceUpdate(data):**
- [ ] Call `presenceService.setStatus(data.status)`
- [ ] On error: silently ignore (presence is best-effort)

**getActiveChannelId():**
- [ ] Returns current activeChannelId or null

**Bus emit helper method:**
- [ ] Private `emit(type, target, data)` method that constructs a proper MessageEnvelope with sourcePane='efemera-connector', nonce, timestamp
- [ ] Uses `bus.send()` for targeted delivery, `bus.send()` with target='*' for broadcast

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Test file: `browser/src/services/efemera/__tests__/EfemeraConnector.test.ts` (15+ tests)

### Test cases required:
**Lifecycle:**
- start() subscribes to all required bus event types
- start() loads channels and emits efemera:channels-loaded
- start() emits efemera:ready
- stop() unsubscribes all listeners
- stop() stops polling
- stop() stops presence heartbeat
- Double start() is safe (idempotent or throws)

**Channel select flow:**
- handleChannelSelect emits efemera:channel-changed
- handleChannelSelect loads messages and emits efemera:messages-loaded
- handleChannelSelect loads members and emits efemera:members-loaded
- handleChannelSelect stops old polling and starts new
- handleChannelSelect error emits efemera:error

**Message send flow:**
- handleMessageSend calls messageService.sendMessage with correct args
- handleMessageSend emits efemera:message-sent on success
- handleMessageSend emits efemera:message-received on success (for chat display)
- handleMessageSend emits efemera:error when no active channel
- handleMessageSend emits efemera:error on HTTP failure

**Polling flow:**
- New messages from polling trigger efemera:message-received
- Polling messages target the messages pane nodeId

**Channel create flow:**
- handleChannelCreate calls channelService.createChannel
- handleChannelCreate reloads and emits efemera:channels-loaded on success

### Test approach:
- Mock MessageBus: record `send()` calls, provide `subscribeType()` that captures handlers
- Mock all 4 sub-services (vi.fn() their methods)
- Verify bus events emitted with correct type, target, and data
- Use `vi.useFakeTimers()` where needed

## Constraints
- No file over 500 lines
- No stubs — every method fully implemented
- The connector is a plain class, NOT a React hook or component
- The connector does NOT create or render any DOM
- Import MessageBus type from `../../infrastructure/relay_bus`
- sourcePane for connector-emitted events: use a constant like `'efemera-connector'`
- All bus events use the `efemera:*` namespace

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-EFEMERA-CONN-02-RESPONSE.md`

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
