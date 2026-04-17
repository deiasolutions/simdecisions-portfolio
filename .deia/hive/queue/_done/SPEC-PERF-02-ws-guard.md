# SPEC: Guard WebSocket Connections on Vercel (Non-Localhost)

## Priority
P0

## Objective
Prevent WebSocket connection attempts on Vercel-hosted domains (efemera.live, shiftcenter.com, etc.) where Vercel's route proxy does not support WebSocket upgrades. The WS transport currently tries to connect, fails immediately, and retries 10 times with exponential backoff — creating 10 failed WebSocket objects over ~5 minutes.

## Context
Vercel's `routes` in vercel.json proxy HTTP requests to Railway but do NOT support WebSocket protocol upgrades. The WS URL `wss://efemera.live/relay/ws` will always fail. The WsTransport class retries 10 times, each creating a WebSocket that immediately errors. This wastes resources and triggers Firefox's performance warning.

The fix should detect non-localhost environments and skip WS entirely, falling back to polling from the start. In the future, a direct Railway WS URL could be used for production WS, but that's out of scope here.

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\efemera-connector\wsTransport.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\efemera-connector\useEfemeraConnector.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\hivenodeUrl.ts

## Acceptance Criteria
- [ ] Add a function `isWebSocketSupported(): boolean` in wsTransport.ts that returns false when `window.location.hostname !== 'localhost'` (Vercel can't proxy WS)
- [ ] In useEfemeraConnector.ts, skip WsTransport creation entirely when `isWebSocketSupported()` returns false — set wsTransport to null
- [ ] When wsTransport is null, the connector should immediately set wsConnected=false and rely on polling fallback when a channel is selected
- [ ] Export the function so tests can use it
- [ ] Tests written FIRST (TDD)
- [ ] All existing tests still pass: `cd browser && npx vitest run src/primitives/efemera-connector`
- [ ] Add test: isWebSocketSupported returns true on localhost
- [ ] Add test: isWebSocketSupported returns false on efemera.live
- [ ] Add test: WsTransport is not created when isWebSocketSupported returns false

## Smoke Test
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run src/primitives/efemera-connector

## Model Assignment
haiku

## Depends On
(none)

## Constraints
- No file over 500 lines
- No stubs
- TDD — tests first
- Do NOT remove WsTransport class or its reconnection logic — just guard instantiation
- Write response to: .deia/hive/responses/20260401-SPEC-PERF-02-RESPONSE.md
