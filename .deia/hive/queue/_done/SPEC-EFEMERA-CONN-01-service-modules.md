# SPEC-EFEMERA-CONN-01: Efemera Connector Service Modules

> **Project:** Efemera Connector (12 specs submitted as batch, 2026-03-28)
> Dependencies between specs ensure correct execution order.
> Design doc: `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md`

## Priority
P0

## Depends On
- None

## Model Assignment
sonnet

## Objective

Create the data-layer service modules for the efemera connector primitive. These are pure TypeScript classes/functions — no React, no bus, no UI. They handle HTTP/WS communication with hivenode and manage state.

## Read First

- `.deia/BOOT.md` — hard rules
- `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md` — full architecture (sections 2.3, 3, 4)
- `browser/src/primitives/tree-browser/adapters/channelsAdapter.ts` — reuse `ChannelData` interface and `channelToNode()` grouping logic
- `browser/src/primitives/tree-browser/adapters/membersAdapter.ts` — reuse `MemberData` interface and `memberToNode()` grouping logic
- `browser/src/services/efemera/relayPoller.ts` — reuse polling logic (interval, lastTimestamp, setChannel)
- `browser/src/services/hivenodeUrl.ts` — use `HIVENODE_URL` for base URL

## Files to Create

### 1. `browser/src/primitives/efemera-connector/types.ts` (~80 lines)

Shared types. Import and re-export `ChannelData` from channelsAdapter and `MemberData` from membersAdapter — don't duplicate them.

```typescript
// Re-export existing types
export type { ChannelData } from '../tree-browser/adapters/channelsAdapter'
export type { MemberData } from '../tree-browser/adapters/membersAdapter'

// New types
export interface Message { ... }  // id, channel_id, author_id, author_name, content, created_at, version?, reply_to_id?, author_type?, message_type?, metadata_json?
export interface Presence { ... } // user_id, status, last_seen
export interface EfemeraChannelChangedData { channelId: string; channelName: string; type: string }
export interface EfemeraMessageSendData { content: string; replyToId?: string }
export interface EfemeraMessagesLoadedData { channelId: string; messages: Message[] }
export interface EfemeraMessageReceivedData { channelId: string; message: Message }
export interface EfemeraMessageSentData { channelId: string; message: Message }
export interface EfemeraErrorData { code: string; message: string; context?: string }
```

### 2. `browser/src/primitives/efemera-connector/channelService.ts` (~120 lines)

Channel CRUD + caching. Reuse `channelToNode()` from channelsAdapter for node rendering.

```typescript
import { HIVENODE_URL } from '../../services/hivenodeUrl'
import type { ChannelData } from './types'

export class ChannelService {
  private cache: ChannelData[] | null = null

  async loadChannels(force?: boolean): Promise<ChannelData[]>  // GET /efemera/channels, cache result
  async createChannel(name: string, type: 'channel' | 'dm'): Promise<ChannelData>  // POST /efemera/channels
  getChannel(id: string): ChannelData | undefined  // from cache
  invalidateCache(): void
}
```

### 3. `browser/src/primitives/efemera-connector/messageService.ts` (~180 lines)

Message operations + polling fallback. Absorb logic from `relayPoller.ts`.

```typescript
import { HIVENODE_URL } from '../../services/hivenodeUrl'
import type { Message } from './types'

export class MessageService {
  private pollingTimer: ReturnType<typeof setInterval> | null = null
  private lastTimestamp: Map<string, string> = new Map()  // per-channel
  private onNewMessages: ((channelId: string, msgs: Message[]) => void) | null = null

  async loadMessages(channelId: string, since?: string, limit?: number): Promise<Message[]>  // GET
  async sendMessage(channelId: string, content: string, authorId: string, authorName: string, replyToId?: string): Promise<Message>  // POST
  startPolling(channelId: string, intervalMs: number): void  // setInterval, track lastTimestamp
  stopPolling(): void  // clearInterval
  setOnNewMessages(cb: (channelId: string, msgs: Message[]) => void): void
  destroy(): void  // cleanup
}
```

### 4. `browser/src/primitives/efemera-connector/presenceService.ts` (~120 lines)

Presence heartbeat + idle detection.

```typescript
import { HIVENODE_URL } from '../../services/hivenodeUrl'

export class PresenceService {
  private status: 'online' | 'idle' | 'offline' = 'online'
  private heartbeatTimer: ReturnType<typeof setInterval> | null = null
  private idleTimer: ReturnType<typeof setTimeout> | null = null
  private onStatusChange: ((status: string) => void) | null = null

  start(userId: string, idleThresholdMs: number, heartbeatIntervalMs?: number): void
  stop(): void
  setStatus(status: 'online' | 'idle' | 'offline'): Promise<void>  // PUT /efemera/presence
  getStatus(): string
  setOnStatusChange(cb: (status: string) => void): void
  private resetIdleTimer(): void  // on mousemove/keydown/mousedown
  private goIdle(): void
  destroy(): void
}
```

### 5. `browser/src/primitives/efemera-connector/memberService.ts` (~80 lines)

Member list fetch. Reuse `memberToNode()` from membersAdapter for node rendering.

```typescript
import { HIVENODE_URL } from '../../services/hivenodeUrl'
import type { MemberData } from './types'

export class MemberService {
  async loadMembers(channelId: string): Promise<MemberData[]>  // GET /efemera/channels/{id}/members
}
```

### 6. `browser/src/primitives/efemera-connector/wsTransport.ts` (~150 lines)

WebSocket connection manager. Ported from platform's ws.py connection pattern but as a browser client.

**WS URL derivation:** The connector hook (CONN-02) derives the URL from `HIVENODE_URL`:
```typescript
const wsUrl = HIVENODE_URL.replace(/^http/, 'ws') + '/efemera/ws'
```
The wsTransport itself takes the full URL as a constructor param — it doesn't import HIVENODE_URL directly.

```typescript
export interface WsTransportOptions {
  url: string  // ws://localhost:8000/efemera/ws or wss://...
  onMessage: (type: string, data: any) => void
  onStatusChange: (connected: boolean) => void
  reconnectIntervalMs?: number  // default 3000
}

export class WsTransport {
  private ws: WebSocket | null = null
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null
  private connected: boolean = false

  connect(): void
  disconnect(): void
  send(type: string, data: any): void  // JSON.stringify and ws.send
  subscribeChannel(channelId: string): void  // send { type: 'subscribe', channelId }
  unsubscribeChannel(channelId: string): void
  isConnected(): boolean
  private handleOpen(): void
  private handleClose(): void  // trigger reconnect
  private handleMessage(event: MessageEvent): void  // parse JSON, route to onMessage
  private scheduleReconnect(): void
  destroy(): void
}
```

### 7. `browser/src/primitives/efemera-connector/index.ts` (~10 lines)

Public exports.

## Acceptance Criteria
- [ ] types.ts exports ChannelData, MemberData, Message, Presence, and all bus event data interfaces
- [ ] channelService: loadChannels returns channels from API and caches result
- [ ] channelService: loadChannels(force=true) bypasses cache
- [ ] channelService: createChannel POSTs and returns created channel
- [ ] messageService: loadMessages returns messages from API
- [ ] messageService: sendMessage POSTs and returns created message
- [ ] messageService: startPolling calls loadMessages at interval
- [ ] messageService: polling detects new messages via lastTimestamp
- [ ] presenceService: start begins heartbeat and sets up idle listeners
- [ ] presenceService: idle detection changes status after threshold
- [ ] wsTransport: connect opens WebSocket
- [ ] wsTransport: send JSON.stringifies and calls ws.send
- [ ] wsTransport: reconnect schedules reconnect on close
- [ ] wsTransport: destroy closes WebSocket and clears timers
- [ ] All HTTP calls use HIVENODE_URL from ../../services/hivenodeUrl
- [ ] All fetch calls use AbortSignal.timeout(5_000)
- [ ] No React, no bus — pure TypeScript classes
- [ ] No file exceeds 500 lines
- [ ] All tests pass

## Smoke Test
- [ ] `npx vitest run browser/src/primitives/efemera-connector/__tests__/channelService.test.ts` — all pass
- [ ] `npx vitest run browser/src/primitives/efemera-connector/__tests__/messageService.test.ts` — all pass
- [ ] `npx vitest run browser/src/primitives/efemera-connector/__tests__/presenceService.test.ts` — all pass
- [ ] `npx vitest run browser/src/primitives/efemera-connector/__tests__/wsTransport.test.ts` — all pass
- [ ] `npx vite build` — zero errors

## Constraints
- All HTTP calls use `HIVENODE_URL` from `../../services/hivenodeUrl`
- All fetch calls use `AbortSignal.timeout(5_000)` (match existing pattern)
- No React. No bus. Pure TypeScript classes.
- No file exceeds 500 lines
- TDD: write tests first, then implementation

## Response File
20260328-EFEMERA-CONN-01-RESPONSE.md
