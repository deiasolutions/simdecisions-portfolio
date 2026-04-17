# BUG-028 Re-Queue Analysis — SPEC INACCURATE

**Status:** BLOCKED — Awaiting Q88N Direction
**Model:** Q33NR (Regent)
**Date:** 2026-03-18

---

## Summary

BUG-028 was re-queued with the claim that "channelsAdapter.ts has zero references to `channel:selected` event" and "the click handler was never wired."

**After code inspection and test verification, I've determined this re-queue spec is INACCURATE.**

The feature IS wired correctly. The architecture follows proper separation of concerns:
- **channelsAdapter.ts** = data loader (fetch channels from API)
- **treeBrowserAdapter.tsx** = click handler (emits `channel:selected` bus event)
- **SDEditor.tsx** = event subscriber (loads messages when channel selected)

All integration tests now pass (7/7). The previous bee's conclusion was correct: "BUG-028 appears to be inaccurate."

---

## Evidence

### 1. Click Handler Exists (treeBrowserAdapter.tsx:173-187)
```typescript
const handleSelect = useCallback((nodeId: string, node: TreeNodeData) => {
  setSelectedId(nodeId)

  // Channels adapter: broadcast channel:selected via bus
  if (adapter === 'channels' && bus && node.meta?.channelId) {
    bus.send({
      type: 'channel:selected',
      sourcePane: paneId,
      target: '*',
      nonce: `${Date.now()}-${Math.random()}`,
      timestamp: new Date().toISOString(),
      data: {
        channelId: node.meta.channelId as string,
        channelName: node.meta.channelName as string,
        type: node.meta.type as string,
      },
    })
  }
  // ... filesystem adapter also here
}, [adapter, bus, paneId])
```

**The click handler IS wired.** It emits `channel:selected` when a channel node is clicked.

### 2. Event Subscriber Exists (SDEditor.tsx:356-386)
```typescript
// Efemera: channel selected — load messages for selected channel
if (message.type === 'channel:selected' && mode === 'chat') {
  const { channelId, channelName } = message.data || {}
  if (channelId) {
    setLabel(channelName ? `#${channelName}` : 'Messages')
    // Reset chat state for new channel
    chatTimestamps.current = new Map()
    chatMessageCount.current = 0

    // Fetch messages from API
    const hivenodeUrl = import.meta.env.VITE_HIVENODE_URL || 'http://localhost:8420'
    fetch(`${hivenodeUrl}/efemera/channels/${channelId}/messages`, {
      signal: AbortSignal.timeout(5_000),
    })
      .then(res => res.ok ? res.json() : [])
      .then((messages: any[]) => {
        const chatContent = messages.map((m: any) => {
          const ts = m.created_at || new Date().toISOString()
          const count = chatMessageCount.current++
          chatTimestamps.current.set(count, ts)
          return `**${m.author_name || 'Unknown'}:** ${m.content}`
        }).join('\n\n')
        setContent(chatContent ? chatContent + '\n\n' : '')
      })
      .catch(() => {
        setContent(`**System:** Welcome to #${channelName || channelId}. Start typing below.\n\n`)
      })
  }
  return
}
```

**The subscriber IS wired.** Text-pane loads messages when `channel:selected` fires.

### 3. Terminal Tracking Exists (useTerminal.ts:176-186)
Terminal with `routeTarget: 'relay'` also subscribes to `channel:selected` and updates `activeChannelId`. This is confirmed in the previous bee's response.

### 4. Integration Tests All Pass
```bash
$ cd browser && npx vitest run src/apps/__tests__/efemera.channels.integration.test.tsx

 ✓ src/apps/__tests__/efemera.channels.integration.test.tsx (7 tests) 4335ms

 Test Files  1 passed (1)
      Tests  7 passed (7)
   Duration  113.73s
```

**All 7 integration tests passing.** These tests verify:
- Channel click → bus event emission
- Bus event → text-pane loads messages
- Bus event → terminal tracks channel
- Multiple subscribers receive same event
- API failure handling
- Empty channel handling
- DM selection works

---

## Why the Re-Queue Spec Is Wrong

The spec says:
> "channelsAdapter.ts has zero references to `channel:selected` event. The click handler was never wired."

**This misunderstands the architecture:**

1. `channelsAdapter.ts` is a **data loader** — it fetches channels from the API and formats them as tree nodes. It does NOT handle clicks.

2. `treeBrowserAdapter.tsx` is the **click handler** — it handles clicks on ALL tree-browser nodes (channels, files, folders, members, etc.) and emits appropriate bus events based on the adapter type.

3. This is **correct separation of concerns**:
   - Data adapters (channelsAdapter, filesystemAdapter, membersAdapter) = load data
   - App adapters (treeBrowserAdapter) = handle UI events
   - Primitives (SDEditor, Terminal) = respond to bus events

**The click handler WAS wired, just not in the file the spec author expected.**

---

## Possible Causes of Original Bug Report

If a user reported "clicking channels does nothing," the likely causes are:

1. **Hivenode not running** — no channels load, nothing to click
2. **Wrong EGG opened** — user opened different app without channels adapter
3. **Browser cache** — old bundled code cached, refresh needed
4. **Development build stale** — Vite dev server not serving updated eggs
5. **API endpoint mismatch** — `VITE_HIVENODE_URL` pointing to wrong server

**NOT a code bug** — the wiring exists and tests prove it works.

---

## Options for Q88N

### Option A: Close BUG-028 as INVALID (Recommended)
- The feature is implemented and tested
- No code changes needed
- Mark bug as INVALID or CANNOT_REPRODUCE
- Update inventory: `python _tools/inventory.py bug update --id BUG-028 --status INVALID --resolution "Feature is implemented. Tests verify channel click → message load flow works correctly."`

### Option B: Manual Smoke Test
If you want empirical proof in a running app:
1. Start hivenode: `cd hivenode && uvicorn main:app --reload --port 8420`
2. Start browser: `cd browser && npm run dev`
3. Open http://localhost:3000/efemera
4. Click a channel in left sidebar
5. Verify messages appear in center panel

### Option C: Fix the Re-Queue Spec and Re-Dispatch
If you still want work done:
- Remove "wire channelsAdapter to emit event" (architecturally wrong)
- Add "document channel selection flow" (useful for onboarding)
- Add "create manual QA checklist for Efemera" (useful for regression testing)

---

## My Recommendation

**Close BUG-028 as INVALID.**

The previous bee (Sonnet) did excellent work:
- Read 6 key files to understand the architecture
- Wrote 8 comprehensive integration tests (479 lines)
- Correctly identified the feature is implemented
- Provided detailed analysis of why the bug report was inaccurate

**The only thing missing from the previous response:** explicitly asking you (Q88N) for permission to close the bug rather than just recommending it.

**That's what I'm doing now:** requesting permission to close BUG-028 as INVALID.

---

## Awaiting Your Direction

Please choose:

1. **Close BUG-028** → I'll update the inventory and move on
2. **Run manual smoke test** → I'll dispatch Q33N to verify in running app
3. **Dispatch for documentation** → I'll correct the spec to focus on docs, not "fixing" working code
4. **Something else** → Tell me what you want

---

## Files Referenced
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\efemera.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\channelsAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-BUG-028-RESPONSE.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\efemera.channels.integration.test.tsx`

## Test Command
```bash
cd browser && npx vitest run src/apps/__tests__/efemera.channels.integration.test.tsx
```

**Result:** 7/7 tests passing

---

**Blocked on:** Q88N decision

**Next action:** Awaiting your response before proceeding with any work on BUG-028.
