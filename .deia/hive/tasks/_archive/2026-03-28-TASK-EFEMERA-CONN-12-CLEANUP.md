# TASK-EFEMERA-CONN-12: Update Bus Types + Clean Up Old Events

## Objective
Add the new `efemera:*` bus event types to the relay_bus type system. Remove the old `channel:*` event types. Clean up any remaining references to the old event namespace.

## Context
The connector (CONN-02) uses new bus events with the `efemera:*` namespace. The old `channel:selected`, `channel:message-sent`, `channel:message-received`, `channel:messages-loaded` events are now deprecated. The bus type definitions in `relay_bus/types/messages.ts` and `relay_bus/constants.ts` need to be updated.

**Depends on:** TASK-EFEMERA-CONN-03, CONN-04, CONN-05 (all primitives must be migrated to new events before old ones are removed).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts` (bus message type definitions)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\constants.ts` (bus message type constants)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\index.ts` (public exports)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\efemera\types.ts` (new event data interfaces, created by CONN-01)

## Deliverables

### 1. Modify `browser/src/infrastructure/relay_bus/types/messages.ts`

- [ ] Add new interfaces for efemera bus events (or re-export from services/efemera/types.ts):
  - EfemeraChannelSelectData
  - EfemeraMessageSendData
  - EfemeraChannelCreateData
  - EfemeraChannelsLoadedData
  - EfemeraChannelChangedData
  - EfemeraMessagesLoadedData
  - EfemeraMessageReceivedData
  - EfemeraMessageSentData
  - EfemeraMembersLoadedData
  - EfemeraPresenceChangedData
  - EfemeraErrorData
- [ ] Remove old interfaces: ChannelSelectedData, ChannelMessageData, ChannelMessagesLoadedData (if no other code references them)
- [ ] Update isValidMessageEnvelope if it references old types

### 2. Modify `browser/src/infrastructure/relay_bus/constants.ts`

- [ ] Add new constants:
  ```typescript
  EFEMERA_CHANNEL_SELECT: 'efemera:channel-select',
  EFEMERA_MESSAGE_SEND: 'efemera:message-send',
  EFEMERA_CHANNEL_CREATE: 'efemera:channel-create',
  EFEMERA_PRESENCE_UPDATE: 'efemera:presence-update',
  EFEMERA_TYPING_START: 'efemera:typing-start',
  EFEMERA_TYPING_STOP: 'efemera:typing-stop',
  EFEMERA_CHANNELS_LOADED: 'efemera:channels-loaded',
  EFEMERA_CHANNEL_CHANGED: 'efemera:channel-changed',
  EFEMERA_MESSAGES_LOADED: 'efemera:messages-loaded',
  EFEMERA_MESSAGE_RECEIVED: 'efemera:message-received',
  EFEMERA_MESSAGE_SENT: 'efemera:message-sent',
  EFEMERA_MEMBERS_LOADED: 'efemera:members-loaded',
  EFEMERA_PRESENCE_CHANGED: 'efemera:presence-changed',
  EFEMERA_TYPING: 'efemera:typing',
  EFEMERA_ERROR: 'efemera:error',
  EFEMERA_READY: 'efemera:ready',
  ```
- [ ] Remove old constants: CHANNEL_SELECTED, CHANNEL_MESSAGE_SENT, CHANNEL_MESSAGE_RECEIVED, CHANNEL_MESSAGES_LOADED (if safe)

### 3. Update `browser/src/infrastructure/relay_bus/index.ts`

- [ ] Export new type interfaces
- [ ] Remove exports for deleted old types

### 4. Search and clean up all remaining references

- [ ] grep for `channel:selected` (old event name) in all .ts/.tsx files — ensure none remain (except comments)
- [ ] grep for `channel:message-sent` — ensure none remain
- [ ] grep for `channel:message-received` — ensure none remain
- [ ] grep for `channel:messages-loaded` — ensure none remain
- [ ] grep for `presence:update` (old name) — ensure migrated to `efemera:presence-update`
- [ ] Remove any dead imports of RelayPoller
- [ ] Remove `browser/src/services/efemera/relayPoller.ts` if not already deleted by CONN-06

## Test Requirements
- [ ] All existing bus tests still pass
- [ ] All browser tests still pass (no broken imports)
- [ ] Verify with `npx vitest run` — zero failures

### Test approach:
- This is primarily a cleanup task. No new logic = minimal new tests.
- Run full test suite to verify nothing breaks from type/constant changes.
- If any test references old event names, update them.

## Constraints
- No file over 500 lines
- No stubs
- Do NOT remove old types/constants if ANY non-test code still references them — check thoroughly first
- If backward compatibility is needed, mark old types as `@deprecated` with JSDoc rather than deleting
- Do NOT modify the MessageBus class itself — only types and constants

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-EFEMERA-CONN-12-RESPONSE.md`

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
