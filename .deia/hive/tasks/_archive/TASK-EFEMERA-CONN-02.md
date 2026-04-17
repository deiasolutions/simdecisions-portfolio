# TASK-EFEMERA-CONN-02: Efemera Connector Primitive

**Priority:** P0
**Depends on:** CONN-01, CONN-05
**Blocks:** CONN-03, CONN-04, CONN-06
**Model:** Sonnet
**Role:** Bee

## Objective

Create the `efemera-connector` React primitive — a registered appType that renders a two-tab sidebar (Channels + Members) and orchestrates all efemera backend communication via bus events.

## Read First

- `.deia/BOOT.md` — hard rules
- `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md` — full architecture (sections 2, 3, 4)
- `browser/src/apps/sidebarAdapter.tsx` — reference for tabbed sidebar pattern (activity bar + switchable content)
- `browser/src/primitives/tree-browser/TreeBrowser.tsx` — reuse for rendering channel/member lists
- `browser/src/primitives/tree-browser/adapters/channelsAdapter.ts` — `channelToNode()` and grouping logic
- `browser/src/primitives/tree-browser/adapters/membersAdapter.ts` — `memberToNode()` and grouping logic
- `browser/src/infrastructure/relay_bus/` — MessageBus API (subscribe, subscribeType, send)
- `browser/src/apps/index.ts` — app registration pattern
- `browser/src/primitives/efemera-connector/` — service modules from CONN-01

## Files to Create

### 1. `browser/src/primitives/efemera-connector/EfemeraConnector.tsx` (~200 lines)

The main React component. Registered as `appType: "efemera-connector"`.

**Structure:**
```tsx
import { useState, useEffect, useContext, useCallback } from 'react'
import { TreeBrowser } from '../tree-browser'
import type { TreeNodeData } from '../tree-browser'
import { channelToNode } from '../tree-browser/adapters/channelsAdapter'
import { memberToNode } from '../tree-browser/adapters/membersAdapter'
import { ShellCtx } from '../../infrastructure/relay_bus'
import { useEfemeraConnector } from './useEfemeraConnector'
import type { AppRendererProps } from '../../shell/components/appRegistry'

export function EfemeraConnector({ paneId, isActive, config }: AppRendererProps) {
  // Config from EGG
  const tabs = config.tabs || [
    { id: 'channels', icon: '#', label: 'Channels' },
    { id: 'members', icon: '@', label: 'Members' },
  ]
  const defaultTab = config.defaultTab || 'channels'

  // Tab state
  const [activeTab, setActiveTab] = useState(defaultTab)

  // Connector hook — wires services to bus
  const {
    channels, members, activeChannelId,
    selectChannel, loading, error, wsConnected,
  } = useEfemeraConnector({ paneId, config })

  // Convert channels to TreeNodeData using existing channelToNode + grouping
  // Convert members to TreeNodeData using existing memberToNode + grouping

  // Render: tab strip + content
  // Tab strip: two icon buttons (# and @), styled like sidebarAdapter's ActivityBarButton
  // Content: TreeBrowser with the appropriate nodes[]
  // Channel click: call selectChannel(channelId, channelName)
}
```

**Tab strip CSS:** Use same patterns as sidebarAdapter — horizontal strip at top with icon buttons, active indicator border. Use `var(--sd-*)` variables only.

**Channel list rendering:** Call `channelToNode()` from channelsAdapter for each channel, then group into Pinned/Channels/DMs sections (reuse the grouping logic from `loadChannels()` in channelsAdapter.ts).

**Member list rendering:** Call `memberToNode()` from membersAdapter for each member, then group into Online/Idle/Offline sections (reuse the grouping logic from `loadMembers()` in membersAdapter.ts).

**Connection status:** Show a small badge in the tab strip (like the existing `.terminal-efemera-badge` pattern in terminal.css) indicating WebSocket connected/disconnected.

### 2. `browser/src/primitives/efemera-connector/useEfemeraConnector.ts` (~250 lines)

Custom hook that wires services to the bus.

```typescript
export function useEfemeraConnector(options: { paneId: string; config: any }) {
  // State
  const [channels, setChannels] = useState<ChannelData[]>([])
  const [members, setMembers] = useState<MemberData[]>([])
  const [activeChannelId, setActiveChannelId] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [wsConnected, setWsConnected] = useState(false)

  // Instantiate services (useRef to persist across renders)
  // channelService, messageService, presenceService, memberService, wsTransport

  // On mount:
  //   1. Load channels via channelService
  //   2. Connect WebSocket via wsTransport
  //   3. Start presence heartbeat
  //   4. Subscribe to bus events: efemera:message-send, efemera:typing-start, etc.
  //   5. Emit efemera:ready

  // selectChannel(channelId, channelName):
  //   1. Set activeChannelId
  //   2. Emit efemera:channel-changed via bus
  //   3. Fetch message history → emit efemera:messages-loaded
  //   4. Fetch members → update local state
  //   5. Switch WS channel subscription
  //   6. Start polling fallback if WS unavailable

  // On efemera:message-send from bus:
  //   1. Call messageService.sendMessage()
  //   2. On success: emit efemera:message-sent + efemera:message-received
  //   3. On error: emit efemera:error

  // WS onMessage handler:
  //   Route by type: 'message' → emit efemera:message-received
  //                  'typing' → emit efemera:typing
  //                  'presence' → emit efemera:presence-changed, update members

  // On unmount: stop polling, disconnect WS, stop presence, unsubscribe bus

  return { channels, members, activeChannelId, selectChannel, loading, error, wsConnected }
}
```

### 3. `browser/src/primitives/efemera-connector/efemera-connector.css` (~100 lines)

Styles for the connector. Tab strip, connection badge, active states. All `var(--sd-*)`.

### 4. Register in `browser/src/apps/index.ts`

Add:
```typescript
import { EfemeraConnector } from '../primitives/efemera-connector'
registerApp('efemera-connector', EfemeraConnector)
```

## Tests to Create

### `browser/src/primitives/efemera-connector/__tests__/EfemeraConnector.test.tsx`
- Renders two tabs (Channels and Members)
- Default tab is Channels
- Clicking Members tab switches content
- Channels list renders grouped nodes (Pinned, Channels, DMs)
- Members list renders grouped nodes (Online, Idle, Offline)
- Channel click calls selectChannel
- Connection badge shows connected/disconnected state
- Loading state shown while fetching

### `browser/src/primitives/efemera-connector/__tests__/useEfemeraConnector.test.ts`
- On mount: loads channels, connects WS, starts presence
- selectChannel: emits efemera:channel-changed, loads messages, loads members
- efemera:message-send: calls sendMessage, emits efemera:message-sent on success
- efemera:message-send: emits efemera:error on failure
- WS message received: emits efemera:message-received
- WS disconnect: starts polling fallback
- Unmount: cleans up all services

## Constraints

- Reuse `TreeBrowser` component for rendering lists — don't build a custom list
- Reuse `channelToNode()` and `memberToNode()` — don't duplicate rendering logic
- Reference `sidebarAdapter.tsx` for tab UI patterns
- CSS: `var(--sd-*)` only
- No file exceeds 500 lines
- TDD: write tests first
