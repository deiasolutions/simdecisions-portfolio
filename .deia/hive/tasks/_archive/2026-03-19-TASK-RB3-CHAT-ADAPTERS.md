# RB-3: Chat Adapter Rebuild — BUG030 Empty List + BUG022B Click-to-Place

## YOUR ROLE
You are a BEE. Read `.deia/BOOT.md` for your rules.

## Context
You are on the `browser-recovery` branch. The browser/ directory has been reset to the March 16 baseline (commit ad06402). You are rebuilding features that were lost during a tangled period.

## Objective
Fix two related issues in the chat history adapter:

### Fix A: BUG-030 — Chat Tree Browser Empty
The Chat EGG's tree-browser panel shows date group headers but no conversation items underneath them. The chatHistoryAdapter is returning empty groups.

**What to do:**
1. Read `eggs/chat.egg.md` for EGG config
2. Read `browser/src/primitives/tree-browser/adapters/chatHistoryAdapter.ts`
3. Trace the data flow from adapter to tree-browser rendering
4. Fix adapter to return conversation entries under date groups
5. If no conversations exist, show "No conversations yet" placeholder
6. Add tests for populated and empty conversation lists

### Fix B: BUG-022B — Click-to-Place Chat History Wiring
The canvas click-to-place feature needs the chatHistoryAdapter to properly wire into the bus for component placement events.

**What to do:**
1. Check if chatHistoryAdapter needs to listen for any canvas placement events
2. Wire any missing bus event handlers
3. Verify the adapter exports are correct

## Files You May Modify
- `browser/src/primitives/tree-browser/adapters/chatHistoryAdapter.ts`
- Test files for chatHistoryAdapter

## Files You Must NOT Modify
- Anything in `browser/src/primitives/canvas/` (canvas.css already cherry-picked)
- Anything in `browser/src/shell/`
- Anything in `browser/src/primitives/apps-home/`
- `browser/src/App.tsx`
- `browser/src/infrastructure/relay_bus/types/messages.ts` (already cherry-picked)
- Anything outside `browser/`

## Smoke Test
```bash
cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter
```

## Build Verification
```bash
cd browser && npx vite build
```

## Acceptance Criteria
- [ ] Chat tree-browser shows conversation entries when they exist
- [ ] Date headers group conversations correctly
- [ ] Empty state shows placeholder text
- [ ] Tests pass
- [ ] Build passes

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Response Requirements — MANDATORY
Write response to `.deia/hive/responses/20260319-TASK-RB3-CHAT-ADAPTERS-RESPONSE.md` with all 8 sections per BOOT.md.
