# SPEC-EFEMERA-CONN-05: Clean Up Adapters and Dead Code

> **Project:** Efemera Connector (12 specs submitted as batch, 2026-03-28)
> Dependencies between specs ensure correct execution order.
> Design doc: `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md`

## Priority
P0

## Depends On
- SPEC-EFEMERA-CONN-01-service-modules

## Model Assignment
haiku

## Objective

Clean up the old adapter code that the connector replaces. Export `channelToNode()`, `memberToNode()`, and grouping functions as public exports. Strip HTTP calls from channelsAdapter and membersAdapter, remove dead code paths from treeBrowserAdapter, and delete relayPoller.ts. This MUST run before CONN-02 so the connector can import these functions.

## Read First

- `.deia/BOOT.md` — hard rules
- `browser/src/primitives/tree-browser/adapters/channelsAdapter.ts` — modify
- `browser/src/primitives/tree-browser/adapters/membersAdapter.ts` — modify
- `browser/src/apps/treeBrowserAdapter.tsx` — modify
- `browser/src/services/efemera/relayPoller.ts` — delete
- `browser/src/primitives/efemera-connector/types.ts` — re-exports from adapters

## Changes

### 1. `browser/src/primitives/tree-browser/adapters/channelsAdapter.ts`

**Keep:**
- `ChannelData` interface (exported, used by connector's types.ts)
- `channelToNode()` function — **CHANGE TO EXPORTED** (`export function channelToNode`)
- Grouping logic for pinned/channels/DMs (extract to exported function)

**Remove:**
- `getMockChannels()` — mock data no longer needed
- `fetchChannels()` — HTTP call no longer needed
- `loadChannels()` — the async function that called fetchChannels

**Add:**
- `export function groupChannels(channels: ChannelData[]): TreeNodeData[]` — extract the grouping logic from the old `loadChannels()` into a pure function that takes channels and returns grouped TreeNodeData[]

**Result:** File goes from 132 lines to ~70 lines. Pure data transformation, no HTTP, no mocks.

### 2. `browser/src/primitives/tree-browser/adapters/membersAdapter.ts`

**Keep:**
- `MemberData` interface (exported, used by connector's types.ts)
- `memberToNode()` function — **CHANGE TO EXPORTED** (`export function memberToNode`)
- Grouping logic for online/idle/offline (extract to exported function)

**Remove:**
- `getMockMembers()` — mock data no longer needed
- `fetchMembers()` — HTTP call no longer needed
- `loadMembers()` — the async function that called fetchMembers

**Add:**
- `export function groupMembers(members: MemberData[]): TreeNodeData[]` — extract the grouping logic from the old `loadMembers()` into a pure function

**Result:** File goes from 113 lines to ~65 lines. Pure data transformation, no HTTP, no mocks.

### 3. `browser/src/apps/treeBrowserAdapter.tsx`

**Remove:**
- The `channels` adapter path in the load function (~line 74-75)
- The `members` adapter path (~line 76-77)
- The `channels` case in handleSelect (~lines 276-289)
- The imports for `loadChannels` and `loadMembers`
- Remove `'channels'` and `'members'` from `EMPTY_TEXT` map and `AUTO_EXPAND_ADAPTERS` set

**Result:** TreeBrowserAdapter no longer knows about efemera. The connector handles channels and members directly.

### 4. Delete `browser/src/services/efemera/relayPoller.ts`

The polling logic has been absorbed into the connector's messageService (CONN-01). Delete the standalone file.

Also check: is the `browser/src/services/efemera/` directory empty after this? If so, remove it. If other files remain (like hivenodeUrl.ts), leave the directory.

### 5. Update imports

Check all files that import from the deleted/modified modules:
- `relayPoller.ts` — find all imports, should be none after CONN-01 (connector uses messageService)
- `loadChannels` / `loadMembers` — find all imports, remove dead references
- `channelsAdapter` and `membersAdapter` — verify connector imports the new `groupChannels` / `groupMembers` exports

## Acceptance Criteria
- [ ] `channelToNode()` is exported from channelsAdapter.ts
- [ ] `memberToNode()` is exported from membersAdapter.ts
- [ ] `groupChannels()` is exported — takes ChannelData[], returns TreeNodeData[]
- [ ] `groupMembers()` is exported — takes MemberData[], returns TreeNodeData[]
- [ ] `fetchChannels`, `getMockChannels`, `loadChannels` removed from channelsAdapter
- [ ] `fetchMembers`, `getMockMembers`, `loadMembers` removed from membersAdapter
- [ ] `channels` and `members` adapter paths removed from treeBrowserAdapter
- [ ] `relayPoller.ts` deleted
- [ ] No dead imports remain
- [ ] Existing channelsAdapter and membersAdapter tests updated to test pure functions
- [ ] All tests pass

## Smoke Test
- [ ] `npx vitest run browser/src/primitives/tree-browser/` — all pass
- [ ] `npx vitest run browser/src/apps/` — all pass
- [ ] `npx vite build` — zero errors

## Constraints
- Do NOT remove any adapter that's still used (filesystem, palette, properties, branches, etc.)
- Do NOT modify TreeBrowser.tsx — it's a pure presentational component, unchanged
- Keep HIVENODE_URL service file — other code still uses it
- TDD: run existing tests, verify they pass after cleanup

## Response File
20260328-EFEMERA-CONN-05-RESPONSE.md
