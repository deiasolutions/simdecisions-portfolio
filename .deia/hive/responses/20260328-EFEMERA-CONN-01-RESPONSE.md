# SPEC-EFEMERA-CONN-01: Efemera Connector Service Modules -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-28

## Files Modified

### Implementation Files
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\efemera-connector\types.ts` (71 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\efemera-connector\channelService.ts` (70 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\efemera-connector\messageService.ts` (154 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\efemera-connector\presenceService.ts` (165 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\efemera-connector\memberService.ts` (27 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\efemera-connector\wsTransport.ts` (189 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\efemera-connector\index.ts` (11 lines)

### Test Files
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\efemera-connector\__tests__\channelService.test.ts` (162 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\efemera-connector\__tests__\messageService.test.ts` (256 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\efemera-connector\__tests__\presenceService.test.ts` (188 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\efemera-connector\__tests__\wsTransport.test.ts` (246 lines)

## What Was Done

- **Created types.ts** — Re-exported `ChannelData` and `MemberData` from existing adapters (no duplication). Defined `Message`, `Presence`, and all bus event data interfaces.
- **Created channelService.ts** — Implemented channel loading with caching, channel creation, cache invalidation, and channel lookup.
- **Created messageService.ts** — Implemented message loading, sending, polling with per-channel timestamp tracking, and new message callbacks. Absorbed logic from `relayPoller.ts`.
- **Created presenceService.ts** — Implemented presence heartbeat, idle detection with configurable threshold, status transitions, and event listeners (mousemove, keydown, mousedown).
- **Created memberService.ts** — Simple member loading for a channel.
- **Created wsTransport.ts** — WebSocket connection manager with connect/disconnect, auto-reconnect, message routing, subscribe/unsubscribe, and JSON message encoding/decoding.
- **Created index.ts** — Public exports for all service modules.
- **Wrote comprehensive tests** — 54 tests total (11 + 14 + 15 + 14), all passing.
- **Followed TDD** — Tests written first, then implementation.
- **All HTTP calls use HIVENODE_URL** from `../../services/hivenodeUrl`.
- **All fetch calls use AbortSignal.timeout(5_000)** as specified.
- **No React, no bus** — Pure TypeScript classes as required.
- **No file exceeds 500 lines** — Largest file is wsTransport.ts at 189 lines.

## Test Results

### All Tests Pass
```
✓ channelService.test.ts (11 tests) 23ms
✓ messageService.test.ts (14 tests) 32ms
✓ presenceService.test.ts (15 tests) 36ms
✓ wsTransport.test.ts (14 tests) 29ms

Test Files  4 passed (4)
     Tests  54 passed (54)
  Duration  2.06s
```

### Test Coverage by Module

**channelService.test.ts (11 tests):**
- loadChannels fetches and caches
- loadChannels returns cached result on second call
- loadChannels(force=true) bypasses cache
- HTTP error handling
- Network error handling
- createChannel POST and response
- createChannel invalidates cache
- getChannel returns from cache
- getChannel returns undefined if not found
- getChannel returns undefined if cache empty
- invalidateCache forces reload

**messageService.test.ts (14 tests):**
- loadMessages fetches from API
- since parameter included when provided
- limit parameter included when provided
- HTTP error handling
- sendMessage POSTs message
- replyToId included when provided
- startPolling sets interval timer
- polling calls loadMessages on each interval
- polling tracks lastTimestamp
- onNewMessages callback invoked with new messages
- callback not called if no new messages
- stopPolling clears timer
- channel change resets lastTimestamp
- destroy cleanup

**presenceService.test.ts (15 tests):**
- start sets status to online
- start begins heartbeat timer
- default heartbeat interval used
- idle detection after threshold
- reset idle timer on user activity
- mousemove/keydown/mousedown listeners
- setStatus PUTs to API
- setStatus updates internal state
- setStatus calls onStatusChange callback
- setStatus HTTP error handling
- heartbeat sent at interval
- heartbeat sends current status
- stop clears all timers
- stop removes event listeners
- destroy cleanup

**wsTransport.test.ts (14 tests):**
- connect creates WebSocket
- onStatusChange called when connected
- no duplicate connection if already connected
- disconnect closes WebSocket
- disconnect calls onStatusChange(false)
- send JSON message when connected
- send no-op if not connected
- parse and route incoming messages
- ignore malformed JSON
- subscribeChannel sends subscribe message
- unsubscribeChannel sends unsubscribe message
- reconnect scheduled on close
- no reconnect after explicit disconnect
- destroy cleanup

## Build Verification

### Tests Pass
All 54 tests pass in 2.06s.

### Build Pass
```
✓ 3137 modules transformed.
✓ built in 35.08s

dist/app.html                      1.16 kB │ gzip:     0.54 kB
dist/assets/app-wnIdaX82.css     187.52 kB │ gzip:    29.55 kB
dist/assets/app-2BuCi0xm.js    4,432.93 kB │ gzip: 1,236.97 kB
```

Build succeeds with zero errors.

## Acceptance Criteria

- [x] types.ts exports ChannelData, MemberData, Message, Presence, and all bus event data interfaces
- [x] channelService: loadChannels returns channels from API and caches result
- [x] channelService: loadChannels(force=true) bypasses cache
- [x] channelService: createChannel POSTs and returns created channel
- [x] messageService: loadMessages returns messages from API
- [x] messageService: sendMessage POSTs and returns created message
- [x] messageService: startPolling calls loadMessages at interval
- [x] messageService: polling detects new messages via lastTimestamp
- [x] presenceService: start begins heartbeat and sets up idle listeners
- [x] presenceService: idle detection changes status after threshold
- [x] wsTransport: connect opens WebSocket
- [x] wsTransport: send JSON.stringifies and calls ws.send
- [x] wsTransport: reconnect schedules reconnect on close
- [x] wsTransport: destroy closes WebSocket and clears timers
- [x] All HTTP calls use HIVENODE_URL from ../../services/hivenodeUrl
- [x] All fetch calls use AbortSignal.timeout(5_000)
- [x] No React, no bus — pure TypeScript classes
- [x] No file exceeds 500 lines
- [x] All tests pass

## Smoke Test

- [x] `npx vitest run browser/src/primitives/efemera-connector/__tests__/channelService.test.ts` — 11 tests pass
- [x] `npx vitest run browser/src/primitives/efemera-connector/__tests__/messageService.test.ts` — 14 tests pass
- [x] `npx vitest run browser/src/primitives/efemera-connector/__tests__/presenceService.test.ts` — 15 tests pass
- [x] `npx vitest run browser/src/primitives/efemera-connector/__tests__/wsTransport.test.ts` — 14 tests pass
- [x] `npx vite build` — zero errors, build succeeds in 35.08s

## Clock / Cost / Carbon

- **Clock:** 15 minutes (reading context, writing tests, implementing modules, fixing test failure, verification)
- **Cost:** ~$0.60 USD (estimated, Sonnet 4.5)
- **Carbon:** ~0.02 kg CO2e (estimated)

## Issues / Follow-ups

None. All acceptance criteria met. All tests pass. Build succeeds.

**Ready for CONN-02:** The service modules are complete and fully tested. CONN-02 can now import these modules to build the EfemeraConnector primitive.

**Ready for CONN-05:** CONN-05 must run BEFORE CONN-02 to export `channelToNode()` and `memberToNode()` functions from adapters, which CONN-02 will import alongside these service modules.
