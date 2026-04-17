# TASK-079: Volume Status Badges for Chat History

## Objective
Add volume status badges (online, syncing, conflict, offline) to conversation nodes in the chat history tree-browser adapter.

## Context
Each conversation is stored on one or more volumes (home://, cloud://, work://). The tree-browser should display a badge showing the volume's status: online (green), syncing (blue spinner), conflict (yellow warning), or offline (grey).

**What already exists:**
- chatHistoryAdapter returns conversation nodes with `volume` and `volumePreference` in meta (lines 84-88)
- hivenode `/node/discover` route returns list of nodes with status (last_seen timestamp)
- Badge type system in tree-browser (type: 'default' | 'success' | 'warning' | 'error')

**What's missing:**
- No volume status checking logic
- No status badges on conversation nodes
- No periodic polling of `/node/discover` to update status

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts` — conversation node structure
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_node_routes.py` (lines 86-114) — /node/discover route contract
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` (lines 474-484) — volume badge spec
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\types.ts` — TreeNode badge types
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\node\client.py` (lines 1-50) — node announcement client pattern

## Deliverables
- [ ] New service: `browser/src/services/volumes/volumeStatus.ts`
- [ ] Export `getVolumeStatus(volume: string): Promise<VolumeStatus>` function
- [ ] Call hivenode `/node/discover` to check if volume's node is online (last_seen < 5 minutes ago)
- [ ] Return status: 'online' | 'syncing' | 'conflict' | 'offline'
- [ ] Update `chatHistoryAdapter.ts` to call `getVolumeStatus()` for each conversation's volume
- [ ] Add status badge to conversation nodes based on volume status:
  - **online:** `{ text: '🟢', type: 'success' }`
  - **syncing:** `{ text: '🔄', type: 'default' }`
  - **conflict:** `{ text: '⚠️', type: 'warning' }`
  - **offline:** `{ text: '🔴', type: 'error' }`
- [ ] Show message count badge alongside status badge (both badges on same node)
- [ ] Handle hivenode unreachable (assume all volumes offline)
- [ ] 4 tests in `browser/src/services/volumes/__tests__/volumeStatus.test.ts`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Mock fetch for `/node/discover` route using vi.mock()
- [ ] Test scenarios:
  - **Node online (last_seen < 5 min ago):** returns 'online'
  - **Node offline (last_seen > 5 min ago):** returns 'offline'
  - **Node not found in discover response:** returns 'offline'
  - **Hivenode unreachable (fetch error):** returns 'offline'
- [ ] Minimum 4 tests

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (no CSS in this task)
- No stubs — fully implement status checking
- TDD: write tests first

## Implementation Notes

**Volume name to node mapping:**
- `home://` → node with volume "home" in `/node/discover` response
- `cloud://` → cloud hivenode (always online if `/node/discover` responds)
- `work://` → node with volume "work"

**getVolumeStatus implementation:**
```typescript
export type VolumeStatus = 'online' | 'syncing' | 'conflict' | 'offline';

const HIVENODE_URL = import.meta.env.VITE_HIVENODE_URL || 'http://localhost:8420';

export async function getVolumeStatus(volume: string): Promise<VolumeStatus> {
  try {
    const volumeName = volume.replace('://', ''); // 'home://' → 'home'

    // Cloud is always online if we can reach hivenode
    if (volumeName === 'cloud') {
      return 'online';
    }

    const response = await fetch(`${HIVENODE_URL}/node/discover`, {
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) {
      return 'offline';
    }

    const data = await response.json();
    const nodes = data.nodes || [];
    const node = nodes.find((n: any) => n.volumes?.includes(volumeName));

    if (!node) {
      return 'offline';
    }

    // Check last_seen timestamp (offline if > 5 minutes ago)
    const lastSeen = new Date(node.last_seen);
    const now = new Date();
    const minutesAgo = (now.getTime() - lastSeen.getTime()) / 60000;

    if (minutesAgo > 5) {
      return 'offline';
    }

    // TODO: Check for sync/conflict status when those features are implemented
    return 'online';
  } catch (error) {
    console.warn('[volumeStatus] Failed to check volume status:', error);
    return 'offline';
  }
}
```

**chatHistoryAdapter changes:**
- Add async status check before returning nodes
- Update badge to show both status + message count:
  ```typescript
  const status = await getVolumeStatus(conv.volume || 'home://');
  const statusBadge = {
    online: { text: '🟢', type: 'success' },
    syncing: { text: '🔄', type: 'default' },
    conflict: { text: '⚠️', type: 'warning' },
    offline: { text: '🔴', type: 'error' },
  }[status];

  badge: {
    text: `${statusBadge.text} ${conv.message_count || 0}`,
    type: statusBadge.type,
  }
  ```

**Performance consideration:**
- Calling `/node/discover` for every conversation is expensive
- Cache the discover response for 60 seconds
- Use a single fetch, then map all conversations to their status

**Caching strategy:**
```typescript
let discoverCache: { nodes: any[]; timestamp: number } | null = null;

async function getNodeList(): Promise<any[]> {
  const now = Date.now();
  if (discoverCache && (now - discoverCache.timestamp) < 60000) {
    return discoverCache.nodes;
  }

  const response = await fetch(`${HIVENODE_URL}/node/discover`);
  const data = await response.json();
  discoverCache = { nodes: data.nodes || [], timestamp: now };
  return discoverCache.nodes;
}
```

**Edge cases:**
- If `/node/discover` returns 401 (requires JWT), assume offline (local mode)
- If volume is 'both' (dual-write), show status of primary volume (home)
- If conversation has no volume field, default to 'home://'

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260314-TASK-079-RESPONSE.md`

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
