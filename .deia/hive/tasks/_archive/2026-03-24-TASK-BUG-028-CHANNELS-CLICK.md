# TASK-BUG-028: Wire Efemera Channel Click to Bus Event

## Objective

Wire channel click events in `treeBrowserAdapter.tsx` to emit `channel:selected` bus events. A regression test already exists and is failing — you need to implement the missing bus emission logic.

## Context — WORK ALREADY DONE

✅ **Already implemented (DO NOT modify):**
- `channelsAdapter.ts` — fetches channels from `/efemera/channels`
- `membersAdapter.ts` — fetches members
- `relayPoller.ts` — polls for new messages
- Text-pane has `channel:selected` subscription handlers
- Terminal has `routeTarget: 'relay'` support
- Regression test created: `BUG-028-regression.test.tsx` (1 test failing)

❌ **What's MISSING (your job):**
- `treeBrowserAdapter.tsx` does NOT emit `channel:selected` bus event when a channel is clicked
- The test expects `bus.send()` to be called with:
  ```typescript
  {
    type: 'channel:selected',
    target: '*',  // Broadcast
    sourcePane: paneId,
    nonce: '...',
    timestamp: '...',
    data: {
      channelId: 'general',
      channelName: 'general',
      type: 'channel' | 'dm'
    }
  }
  ```

## Files to Read First

**Read the TEST FILE to understand expected behavior:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\BUG-028-regression.test.tsx`

**Read the implementation:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx` (wire click → bus.send())
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\channelsAdapter.ts` (channel data structure)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx` (look for `channel:selected` subscription)

## Deliverables

- [ ] `treeBrowserAdapter.tsx` emits `channel:selected` bus event when:
  - Adapter is `'channels'`
  - User clicks a channel item (channel or DM)
  - Event includes: `channelId`, `channelName`, `type` ('channel' or 'dm')
- [ ] Event is broadcast (`target: '*'`)
- [ ] Event includes `nonce` and `timestamp` (standard bus envelope)
- [ ] Event includes `sourcePane: paneId`
- [ ] Non-channel adapters (explorer, properties, etc.) do NOT send `channel:selected` events
- [ ] Regression test passes (1 test)
- [ ] No existing tests broken

## Test Requirements

- [ ] Existing regression test MUST pass: `BUG-028-regression.test.tsx` (currently 0/1 passing)
- [ ] Edge cases already covered in test:
  - Clicking channel fires event
  - Clicking DM fires event with type='dm'
  - Clicking different channels sends separate events
  - Non-channel adapters do NOT fire channel:selected
  - Event includes nonce and timestamp
- [ ] No new tests required — just make existing test pass

## Constraints

- No file over 500 lines
- CSS: `var(--sd-*)` only — no hardcoded colors
- No stubs — fully implement all functions
- Do NOT modify channelsAdapter.ts — it's correct
- Do NOT modify the test file — it's correct
- ONLY modify treeBrowserAdapter.tsx to wire click → bus.send()

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260324-TASK-BUG-028-RESPONSE.md`

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

## Bug Details (from inventory)

- **ID:** BUG-028
- **Severity:** P0
- **Component:** efemera
- **Title:** Efemera channels not wired: clicking channels does nothing
- **Status:** OPEN
- **Description:** Clicking a channel in the tree-browser (channels adapter) does not emit `channel:selected` bus event, so text-pane never receives the event and chat doesn't load

## Implementation Hint

Look for the `handleNodeClick` function in `treeBrowserAdapter.tsx`. You need to:

1. Check if `config.adapter === 'channels'`
2. Extract channel data from the clicked node (`node.id`, `node.label`, `node.data.type`)
3. Call `bus.send()` with the event structure shown in the test
4. Use `crypto.randomUUID()` for nonce, `new Date().toISOString()` for timestamp

The test shows the exact event structure expected.
