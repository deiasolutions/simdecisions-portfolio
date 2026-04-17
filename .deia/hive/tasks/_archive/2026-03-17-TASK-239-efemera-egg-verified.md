# TASK-239: Efemera EGG Verified

## Objective

Verify that the Efemera EGG (`eggs/efemera.egg.md`) renders correctly in the browser with all components working: channels sidebar, messages pane, compose terminal, and members list. Fix any layout, data loading, or bus event issues found.

## Context

Efemera is a real-time messaging app built on ShiftCenter's pane system. Backend and frontend are implemented. The EGG file defines a 4-pane layout:

- **Left pane (18%)**: tree-browser with channels adapter → displays channels/DMs
- **Center-top pane (75%)**: text-pane in `renderMode: "chat"` → displays message bubbles
- **Center-bottom pane (25%)**: terminal with `routeTarget: "relay"` → compose bar for sending messages
- **Right pane (15%)**: tree-browser with members adapter → displays members grouped by presence (online/idle/offline)

The layout uses `"seamless": true` between messages and compose panes (no visible border).

**Backend:**
- Store: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\store.py` (SQLite: channels, messages, members, presence)
- Routes: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\routes.py` (8 API endpoints under /efemera/)
- Default channels: "general", "random", "announcements" (seeded on first use)

**Frontend:**
- Channels adapter: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\channelsAdapter.ts`
- Members adapter: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\membersAdapter.ts`
- Relay poller: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\efemera\relayPoller.ts`

**Bus events (defined in EGG permissions):**
- Emit: `channel:selected`, `channel:message-sent`, `channel:messages-loaded`, `presence:update`
- Receive: `channel:selected`, `channel:message-sent`, `channel:message-received`, `channel:messages-loaded`, `presence:update`, `terminal:text-patch`

**Expected behavior:**
1. Selecting a channel in left tree-browser → emits `channel:selected` → messages pane loads messages → compose terminal activates for that channel
2. Typing a message in compose terminal → submits to `/efemera/channels/{id}/messages` → message appears in chat bubbles
3. Relay poller polls for new messages (3 second interval) → emits `channel:message-received` → messages pane appends new bubbles
4. Members pane shows users grouped by online/idle/offline status with badges for owner/admin roles

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\efemera.egg.md` — layout definition
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\store.py` — backend data store
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\routes.py` — API endpoints
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\channelsAdapter.ts` — channels tree adapter
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\membersAdapter.ts` — members tree adapter
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\efemera\relayPoller.ts` — message polling service
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\TextPane.tsx` — text pane component (check chat renderMode)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\Terminal.tsx` — terminal component (check routeTarget relay)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx` — tree browser component (check adapter loading)

## Deliverables

- [ ] Manual verification: Load `?egg=efemera` in browser and verify:
  - All 4 panes render correctly per EGG layout spec
  - Channels tree displays default channels (general, random, announcements) grouped into "Pinned" and "Channels" sections
  - Clicking a channel → messages pane loads messages for that channel
  - Compose terminal accepts input and sends messages via relay
  - Members tree displays mock members grouped by Online/Idle/Offline
  - Seamless border between messages and compose panes (no visible divider)
  - Bus events fire correctly: `channel:selected`, `channel:message-sent`, `channel:message-received`
  - Relay poller polls for new messages (check browser console logs or network tab)

- [ ] Fix any issues found during verification:
  - Layout rendering problems (pane ratios, seamless borders)
  - Adapter loading failures (channels, members)
  - Bus event wiring issues (selection, message flow)
  - Terminal relay target not working
  - Text-pane chat renderMode not rendering bubbles
  - CSS variable usage (no hardcoded colors)

- [ ] Add automated tests for any gaps found:
  - Adapter data loading and transformation
  - Bus event emission/reception
  - Relay poller behavior
  - Terminal relay target submission

- [ ] Run existing tests to verify no regressions:
  - `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run`

- [ ] Document verification results:
  - Checklist of verified behaviors
  - Screenshots or descriptions of any issues found and fixed
  - Test results summary

## Test Requirements

- [ ] TDD: Write tests FIRST for any new functionality or bug fixes
- [ ] All existing tests must pass (no regressions)
- [ ] Edge cases to test:
  - Empty channel list (no channels returned from API)
  - Empty messages list (new channel with no messages)
  - Empty members list (channel with no members)
  - API timeout/failure → fallback to mock data (already implemented in adapters)
  - Selecting different channels → messages pane updates correctly
  - Sending a message → appears immediately in chat bubbles
  - Multiple messages in quick succession → all rendered as bubbles
  - Presence status changes → members list updates

## Constraints

- **Rule 3:** NO HARDCODED COLORS. Only CSS variables (`var(--sd-*)`). Check all styles added/modified.
- **Rule 4:** No file over 500 lines. If any file approaches this limit, modularize.
- **Rule 6:** NO STUBS. Every function must be fully implemented. Do not ship placeholder code.
- **Rule 8:** All file paths must be absolute in documentation and response file.
- **Rule 10:** NO GIT OPERATIONS. Do not commit, push, or modify git state.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-239-RESPONSE.md`

The response MUST contain these 8 sections:

1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full absolute paths
3. **What Was Done** — bullet list of concrete changes (not intent)
4. **Test Results** — test files run, pass/fail counts, specific test names if new tests added
5. **Build Verification** — summary of test run output, last 5 lines of test command
6. **Acceptance Criteria** — copy from task deliverables above, mark [x] done or [ ] not done with explanation
7. **Clock / Cost / Carbon** — all three metrics, never omit any
8. **Issues / Follow-ups** — edge cases discovered, dependencies, recommended next tasks

DO NOT skip any section.

## Notes

- The memory file confirms Efemera backend has **29 tests passing** (store + API), and frontend has **7 tests passing** (channelsAdapter)
- Verify that the terminal `routeTarget: "relay"` is implemented correctly in Terminal.tsx — this may need integration work
- Verify that text-pane `renderMode: "chat"` renders message bubbles correctly — chatRenderer.tsx was recently updated (TASK-229)
- Check browser console for any bus event errors or adapter loading failures
- If manual testing reveals issues, write automated tests to prevent regression
- The EGG file specifies `seamless: true` for the horizontal split — verify this renders without a visible border
