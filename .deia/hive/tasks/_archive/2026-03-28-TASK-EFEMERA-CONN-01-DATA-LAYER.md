# TASK-EFEMERA-CONN-01: Create Efemera Connector Data Layer

## Objective
Create the data service modules (types, channelService, messageService, presenceService, memberService) that handle all HTTP communication with hivenode efemera endpoints. No bus wiring — pure data layer.

## Context
The efemera EGG currently has HTTP calls scattered across 4 primitive files (useTerminal.ts, SDEditor.tsx, channelsAdapter.ts, membersAdapter.ts). We are extracting all HTTP communication into a centralized connector service. This task builds the data layer that the orchestrator (CONN-02) will wire to bus events.

Existing relevant code:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\efemera\relayPoller.ts` — existing polling service (97 lines). Its polling logic should be absorbed into messageService.
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\hivenodeUrl.ts` — base URL constant.
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\routes.py` — backend endpoints this code calls.

All backend endpoints are under `/efemera/`:
- `GET /efemera/channels` — list channels
- `POST /efemera/channels` — create channel
- `GET /efemera/channels/{id}` — get channel
- `GET /efemera/channels/{id}/messages` — list messages (supports `?since=` and `?limit=`)
- `POST /efemera/channels/{id}/messages` — send message
- `GET /efemera/channels/{id}/members` — list members
- `POST /efemera/channels/{id}/members` — add member
- `PUT /efemera/presence` — update presence
- `GET /efemera/presence` — get all presence

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\efemera\relayPoller.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\hivenodeUrl.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\channelsAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\membersAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\routes.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260328-EFEMERA-CONNECTOR-DESIGN.md` (Section 4: Module Designs)

## Deliverables

### 1. `browser/src/services/efemera/types.ts` (~80 lines)
- [ ] `Channel` interface: id, name, type, created_by, pinned, created_at, unread_count
- [ ] `Message` interface: id, channel_id, author_id, author_name, content, created_at, version?, reply_to_id?, author_type?, message_type?, moderation_status?
- [ ] `Member` interface: user_id, username, role, status, joined_at?
- [ ] `Presence` interface: user_id, status, last_seen
- [ ] All bus event data interfaces: EfemeraChannelSelectData, EfemeraMessageSendData, EfemeraChannelCreateData, EfemeraChannelsLoadedData, EfemeraChannelChangedData, EfemeraMessagesLoadedData, EfemeraMessageReceivedData, EfemeraMessageSentData, EfemeraMembersLoadedData, EfemeraPresenceChangedData, EfemeraErrorData

### 2. `browser/src/services/efemera/channelService.ts` (~150 lines)
- [ ] `ChannelService` class with constructor taking `{ baseUrl: string }`
- [ ] `loadChannels(force?: boolean): Promise<Channel[]>` — fetches from `/efemera/channels`, caches result, force=true bypasses cache
- [ ] `createChannel(name, type, description?): Promise<Channel>` — POSTs to `/efemera/channels`, invalidates cache
- [ ] `getChannel(channelId): Channel | undefined` — lookup from cache (no HTTP)
- [ ] `invalidateCache(): void` — clears internal cache
- [ ] All HTTP calls use `AbortSignal.timeout(5_000)`
- [ ] All HTTP errors caught and re-thrown with descriptive messages

### 3. `browser/src/services/efemera/messageService.ts` (~200 lines)
- [ ] `MessageService` class with constructor taking `{ baseUrl: string, pollingIntervalMs: number }`
- [ ] `loadMessages(channelId, since?, limit?): Promise<Message[]>` — fetches from `/efemera/channels/{id}/messages`
- [ ] `sendMessage(channelId, content, authorId, authorName, replyToId?): Promise<Message>` — POSTs to `/efemera/channels/{id}/messages`
- [ ] `startPolling(channelId): void` — starts setInterval polling, tracks lastTimestamp
- [ ] `stopPolling(): void` — clears interval, resets state
- [ ] `onNewMessages(callback): void` — registers callback for polling results
- [ ] `setPollingInterval(ms): void` — updates interval, restarts if polling
- [ ] Polling logic: fetches `?since={lastTimestamp}`, calls callback with new messages, updates lastTimestamp
- [ ] Polling silently ignores network errors (same as current relayPoller)
- [ ] All HTTP calls use `AbortSignal.timeout(5_000)`

### 4. `browser/src/services/efemera/presenceService.ts` (~120 lines)
- [ ] `PresenceService` class with constructor taking `{ baseUrl, userId, idleThresholdMs, heartbeatIntervalMs }`
- [ ] `start(): void` — starts heartbeat interval + idle detection listeners
- [ ] `stop(): void` — clears intervals, removes event listeners, sends offline status
- [ ] `setStatus(status): Promise<void>` — PUTs to `/efemera/presence`
- [ ] `onStatusChange(callback): void` — registers callback for status changes
- [ ] `getStatus(): string` — returns current status
- [ ] Idle detection: listens for mousemove, keydown, mousedown. After idleThresholdMs of inactivity, status -> 'idle'. On activity after idle: status -> 'online'.
- [ ] Heartbeat: sends PUT at heartbeatIntervalMs intervals with current status

### 5. `browser/src/services/efemera/memberService.ts` (~80 lines)
- [ ] `MemberService` class with constructor taking `{ baseUrl: string }`
- [ ] `loadMembers(channelId): Promise<Member[]>` — fetches from `/efemera/channels/{id}/members`
- [ ] HTTP errors caught and re-thrown with descriptive messages
- [ ] `AbortSignal.timeout(5_000)` on all fetches

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Test files:
  - `browser/src/services/efemera/__tests__/channelService.test.ts` (8+ tests)
  - `browser/src/services/efemera/__tests__/messageService.test.ts` (12+ tests)
  - `browser/src/services/efemera/__tests__/presenceService.test.ts` (10+ tests)
  - `browser/src/services/efemera/__tests__/memberService.test.ts` (5+ tests)

### Test cases required:
**channelService:**
- loadChannels fetches from correct URL
- loadChannels returns cached data on second call
- loadChannels(force=true) bypasses cache
- createChannel POSTs correctly and invalidates cache
- getChannel returns from cache
- HTTP 500 throws descriptive error
- Network timeout throws descriptive error
- Empty channel list handled

**messageService:**
- loadMessages fetches from correct URL
- loadMessages with since parameter adds query param
- sendMessage POSTs correctly
- startPolling creates interval
- stopPolling clears interval
- Polling calls callback with new messages
- Polling updates lastTimestamp
- Polling ignores network errors
- Channel switch stops old poll and starts new one
- sendMessage with replyToId included in body
- setPollingInterval restarts polling
- Double startPolling is idempotent

**presenceService:**
- start begins heartbeat
- stop clears heartbeat and sends offline
- Idle detection triggers after threshold
- Activity after idle resets to online
- setStatus PUTs to correct URL
- onStatusChange callback fires on transitions
- getStatus returns current status
- Multiple start calls are idempotent
- stop removes window event listeners
- Heartbeat interval fires at configured time

**memberService:**
- loadMembers fetches from correct URL
- loadMembers with empty response returns empty array
- HTTP 500 throws descriptive error
- Network timeout throws descriptive error
- channelId is URL-encoded

### Test approach:
- Mock `fetch` globally (vi.fn())
- Use `vi.useFakeTimers()` for polling and heartbeat tests
- No real backend needed

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (no CSS in this task)
- No stubs — every method fully implemented
- Import HIVENODE_URL from `../../services/hivenodeUrl` (or accept baseUrl in constructor)
- Do NOT import or use MessageBus — that's CONN-02's job
- Do NOT modify any existing files — this task creates new files only

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-EFEMERA-CONN-01-RESPONSE.md`

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
