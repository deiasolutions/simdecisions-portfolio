# SPEC-EFEMERA-CONN-02: Efemera Connector Primitive

> **Project:** Efemera Connector (12 specs submitted as batch, 2026-03-28)
> Dependencies between specs ensure correct execution order.
> Design doc: `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md`

## Priority
P0

## Depends On
- SPEC-EFEMERA-CONN-01-service-modules
- SPEC-EFEMERA-CONN-05-adapter-cleanup

## Model Assignment
sonnet

## Objective

Create the `efemera-connector` React primitive — a registered appType that renders a two-tab sidebar (Channels + Members) and orchestrates all efemera backend communication via bus events.

## Read First

- `.deia/BOOT.md` — hard rules
- `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md` — full architecture (sections 2, 3, 4)
- `browser/src/apps/sidebarAdapter.tsx` — reference for tabbed sidebar pattern (activity bar + switchable content)
- `browser/src/primitives/tree-browser/TreeBrowser.tsx` — reuse for rendering channel/member lists
- `browser/src/primitives/tree-browser/adapters/channelsAdapter.ts` — `channelToNode()` and `groupChannels()` (exported by CONN-05)
- `browser/src/primitives/tree-browser/adapters/membersAdapter.ts` — `memberToNode()` and `groupMembers()` (exported by CONN-05)
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
import { channelToNode, groupChannels } from '../tree-browser/adapters/channelsAdapter'
import { memberToNode, groupMembers } from '../tree-browser/adapters/membersAdapter'
import { ShellCtx } from '../../infrastructure/relay_bus'
import { useEfemeraConnector } from './useEfemeraConnector'
import type { AppRendererProps } from '../../shell/components/appRegistry'

export function EfemeraConnector({ paneId, isActive, config }: AppRendererProps) {
  const tabs = config.tabs || [
    { id: 'channels', icon: '#', label: 'Channels' },
    { id: 'members', icon: '@', label: 'Members' },
  ]
  const defaultTab = config.defaultTab || 'channels'
  const [activeTab, setActiveTab] = useState(defaultTab)

  const {
    channels, members, activeChannelId,
    selectChannel, loading, error, wsConnected,
  } = useEfemeraConnector({ paneId, config })

  // Convert channels to TreeNodeData using groupChannels()
  // Convert members to TreeNodeData using groupMembers()
  // Render: tab strip + content
  // Channel click: call selectChannel(channelId, channelName)
}
```

**Tab strip CSS:** Use same patterns as sidebarAdapter — horizontal strip at top with icon buttons, active indicator border. Use `var(--sd-*)` variables only.

**Channel list rendering:** Call `groupChannels()` from channelsAdapter for grouped TreeNodeData[].

**Member list rendering:** Call `groupMembers()` from membersAdapter for grouped TreeNodeData[].

**Connection status:** Show a small badge in the tab strip indicating WebSocket connected/disconnected.

### 2. `browser/src/primitives/efemera-connector/useEfemeraConnector.ts` (~250 lines)

Custom hook that wires services to the bus. Derives WS URL from HIVENODE_URL:
```typescript
const wsUrl = HIVENODE_URL.replace(/^http/, 'ws') + '/efemera/ws'
```

All bus events use `target: '*'` (broadcast). Consumers filter by type via `bus.subscribeType()`.

```typescript
export function useEfemeraConnector(options: { paneId: string; config: any }) {
  // On mount: load channels, connect WS, start presence, subscribe bus events, emit efemera:ready
  // selectChannel: emit efemera:channel-changed, fetch history -> emit efemera:messages-loaded, fetch members, switch WS subscription
  // On efemera:message-send: call sendMessage, emit efemera:message-sent + efemera:message-received on success, efemera:error on failure
  // WS onMessage: route by type -> emit efemera:message-received, efemera:typing, efemera:presence-changed
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

## Acceptance Criteria
- [ ] EfemeraConnector renders two tabs (Channels and Members)
- [ ] Default tab is Channels
- [ ] Clicking Members tab switches content
- [ ] Channels list renders grouped nodes (Pinned, Channels, DMs) using groupChannels()
- [ ] Members list renders grouped nodes (Online, Idle, Offline) using groupMembers()
- [ ] Channel click calls selectChannel and emits efemera:channel-changed
- [ ] Connection badge shows connected/disconnected state
- [ ] Loading state shown while fetching
- [ ] On mount: loads channels, connects WS, starts presence
- [ ] selectChannel emits efemera:channel-changed, loads messages, loads members
- [ ] efemera:message-send received -> calls sendMessage, emits efemera:message-sent on success
- [ ] efemera:message-send received -> emits efemera:error on failure
- [ ] WS message received -> emits efemera:message-received
- [ ] WS disconnect -> starts polling fallback
- [ ] Unmount cleans up all services
- [ ] Registered as appType 'efemera-connector' in apps/index.ts
- [ ] CSS uses var(--sd-*) only
- [ ] No file exceeds 500 lines
- [ ] All tests pass

## Smoke Test
- [ ] `npx vitest run browser/src/primitives/efemera-connector/__tests__/EfemeraConnector.test.tsx` — all pass
- [ ] `npx vitest run browser/src/primitives/efemera-connector/__tests__/useEfemeraConnector.test.ts` — all pass
- [ ] `npx vite build` — zero errors

## Constraints
- Reuse `TreeBrowser` component for rendering lists — don't build a custom list
- Reuse `channelToNode()`, `groupChannels()`, `memberToNode()`, `groupMembers()` — don't duplicate rendering logic
- Reference `sidebarAdapter.tsx` for tab UI patterns
- CSS: `var(--sd-*)` only
- No file exceeds 500 lines
- TDD: write tests first

## Response File
20260328-EFEMERA-CONN-02-RESPONSE.md
