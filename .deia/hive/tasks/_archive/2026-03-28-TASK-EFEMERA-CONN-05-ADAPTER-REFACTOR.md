# TASK-EFEMERA-CONN-05: Refactor Tree-Browser Adapters

## Objective
Remove all direct HTTP calls from channelsAdapter.ts and membersAdapter.ts. Refactor them to receive data from the efemera connector via bus events, transforming connector data into TreeNodeData format.

## Context
Currently:
- `channelsAdapter.ts` calls `fetch(HIVENODE_URL + '/efemera/channels')` directly and has mock fallback data
- `membersAdapter.ts` calls `fetch(HIVENODE_URL + '/efemera/channels/{id}/members')` directly and has mock fallback data

After refactoring:
- The connector emits `efemera:channels-loaded` with `{ channels: Channel[] }` — the adapter transforms this into TreeNodeData[]
- The connector emits `efemera:members-loaded` with `{ channelId, members: Member[] }` — the adapter transforms this into TreeNodeData[]
- Adapters become pure data transformers: Channel[] → TreeNodeData[] and Member[] → TreeNodeData[]
- No HTTP calls in adapters
- No mock data in adapters (connector provides real data; mock data lives in tests only)

**Depends on:** TASK-EFEMERA-CONN-02 (connector must emit the events).

**Note:** The tree-browser primitive currently calls `loadChannels()` or `loadMembers()` as an async function during mount. After this refactor, the adapter's load function should subscribe to the bus event and resolve when data arrives. This means the adapter's `loadChannels()` / `loadMembers()` may need to return a Promise that resolves when the connector emits data, OR the tree-browser needs to support a "push" model where data arrives asynchronously via bus. Read the tree-browser primitive to determine the best approach.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\channelsAdapter.ts` (132 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\membersAdapter.ts` (113 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx` (the primitive — understand how it calls adapters)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\types.ts` (TreeNodeData type)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260328-EFEMERA-CONNECTOR-DESIGN.md` (Section 5.3)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\efemera\types.ts` (Channel, Member interfaces)

## Deliverables

### 1. Modify `browser/src/primitives/tree-browser/adapters/channelsAdapter.ts`

- [ ] Remove `fetchChannels()` function (HTTP call)
- [ ] Remove `getMockChannels()` function (mock data)
- [ ] Remove HIVENODE_URL import
- [ ] Keep `channelToNode()` function (Channel → TreeNodeData transform) — make it accept the Channel type from `services/efemera/types.ts`
- [ ] Keep the grouping logic (pinned/regular/dms sections)
- [ ] Export a `transformChannels(channels: Channel[]): TreeNodeData[]` function that takes Channel[] and returns grouped TreeNodeData[]
- [ ] The existing `loadChannels()` export must still work for backward compatibility during migration — it can be refactored to call `transformChannels()` with data from the connector

### 2. Modify `browser/src/primitives/tree-browser/adapters/membersAdapter.ts`

- [ ] Remove `fetchMembers()` function (HTTP call)
- [ ] Remove `getMockMembers()` function (mock data)
- [ ] Remove HIVENODE_URL import
- [ ] Keep `memberToNode()` function (Member → TreeNodeData transform)
- [ ] Keep the grouping logic (online/idle/offline sections)
- [ ] Export a `transformMembers(members: Member[]): TreeNodeData[]` function that takes Member[] and returns grouped TreeNodeData[]
- [ ] The existing `loadMembers()` export must still work for backward compatibility

### 3. Ensure tree-browser integration works

- [ ] Read TreeBrowser.tsx to understand how adapters are called
- [ ] If tree-browser uses a "pull" model (calls adapter.loadX() on mount), ensure the refactored adapter still supports this pattern
- [ ] If tree-browser supports bus-driven data refresh, wire that up
- [ ] The click handler in tree-browser should emit `efemera:channel-select` (check if this is already wired or needs adding)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing adapter tests still pass
- [ ] New tests for transform functions

### Test cases required:
**channelsAdapter:**
- transformChannels with empty array returns empty array
- transformChannels groups pinned channels into "Pinned" section
- transformChannels groups regular channels into "Channels" section
- transformChannels groups DMs into "Direct Messages" section
- transformChannels handles mixed pinned + regular + DMs
- channelToNode sets correct icon (# for channel, @ for DM)
- channelToNode includes badge for unread_count > 0
- channelToNode includes channelId and channelName in meta

**membersAdapter:**
- transformMembers with empty array returns empty array
- transformMembers groups by online/idle/offline with counts
- memberToNode sets correct status icon
- memberToNode includes badge for owner/admin roles
- memberToNode includes userId, role, status in meta

### Where to add tests:
- Check `browser/src/apps/__tests__/efemera.channels.integration.test.tsx` — update if it tests adapter HTTP calls
- Create `browser/src/primitives/tree-browser/adapters/__tests__/channelsAdapter.test.ts` if needed
- Create `browser/src/primitives/tree-browser/adapters/__tests__/membersAdapter.test.ts` if needed

## Constraints
- No file over 500 lines
- No stubs
- Keep backward compatibility: `loadChannels()` and `loadMembers()` exports must still exist and work (they may internally delegate to transform functions or be shimmed)
- Do NOT modify TreeBrowser.tsx in this task (unless absolutely necessary for bus event wiring — document why)
- Import Channel and Member types from `../../../services/efemera/types`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-EFEMERA-CONN-05-RESPONSE.md`

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
