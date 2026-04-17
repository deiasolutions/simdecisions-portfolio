# SPEC-EFEMERA-CONN-03: Refactor Terminal Relay Mode

> **Project:** Efemera Connector (12 specs submitted as batch, 2026-03-28)
> Dependencies between specs ensure correct execution order.
> Design doc: `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md`

## Priority
P0

## Depends On
- SPEC-EFEMERA-CONN-02-connector-primitive

## Model Assignment
sonnet

## Objective

Remove all efemera HTTP code from the terminal's relay mode. The terminal should only communicate with efemera through `efemera:*` bus events — it never calls fetch() for efemera endpoints. Add proper loading state management.

## Read First

- `.deia/BOOT.md` — hard rules
- `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md` — section 5.1
- `browser/src/primitives/terminal/useTerminal.ts` — the file being modified
  - Lines 182-194: `channel:selected` bus subscription (REMOVE)
  - Lines 468-535: Relay mode HTTP POST + bus emissions (REMOVE)
- `browser/src/primitives/efemera-connector/types.ts` — bus event data shapes

## Changes to `browser/src/primitives/terminal/useTerminal.ts`

### REMOVE

1. **Lines 182-194** — `channel:selected` subscription effect
2. **Lines 468-535** — Relay mode block in `handleSubmit` (HTTP POST + bus emissions)

### ADD

1. **New effect — subscribe to `efemera:channel-changed`:**
   ```typescript
   useEffect(() => {
     if (routeTarget !== 'relay' || !bus) return;
     return bus.subscribeType('efemera:channel-changed', (msg: any) => {
       setActiveChannelId(msg.data.channelId);
       setActiveChannelName(msg.data.channelName);
       setEntries(prev => prev.filter(e => e.type !== 'system'));
     });
   }, [routeTarget, bus]);
   ```

2. **New effect — subscribe to `efemera:message-sent`:**
   ```typescript
   useEffect(() => {
     if (routeTarget !== 'relay' || !bus) return;
     return bus.subscribeType('efemera:message-sent', () => {
       setLoading(false);  // Delivery confirmed
     });
   }, [routeTarget, bus]);
   ```

3. **New effect — subscribe to `efemera:error`:**
   ```typescript
   useEffect(() => {
     if (routeTarget !== 'relay' || !bus) return;
     return bus.subscribeType('efemera:error', (msg: any) => {
       setLoading(false);  // Stop loading on error
       const { message: errMsg, context } = msg.data || {};
       setEntries(prev => [...prev, {
         type: 'system',
         content: `Error: ${errMsg || 'Unknown error'}`,
         level: 'error',
       }]);
     });
   }, [routeTarget, bus]);
   ```

4. **Replace relay mode block in `handleSubmit`:**
   ```typescript
   if (routeTarget === 'relay') {
     if (!activeChannelId) {
       setEntries(prev => [...prev,
         { type: 'input', content: text, hidden: true },
         { type: 'system', content: 'Select a channel first.' },
       ]);
       return;
     }
     setEntries(prev => [...prev, { type: 'input', content: text, hidden: true }]);
     setLoading(true);
     if (bus && nodeId) {
       bus.send({
         type: 'efemera:message-send',
         sourcePane: nodeId,
         target: '*',
         nonce: `${Date.now()}-${Math.random()}`,
         timestamp: new Date().toISOString(),
         data: { content: text },
       });
     }
     return;
   }
   ```

### Also remove
- The `HIVENODE_URL` import if no other code in useTerminal uses it (check first — IR mode and canvas mode may still use it)
- The `channel:message-sent` bus event emission (connector handles this now)
- The `terminal:text-patch` emission for relay mode (connector emits `efemera:message-received` to text-pane directly)

## Acceptance Criteria
- [ ] Relay mode emits `efemera:message-send` on Enter (not HTTP POST)
- [ ] Relay mode sets loading=true when sending
- [ ] Relay mode sets loading=false on `efemera:message-sent`
- [ ] Relay mode sets loading=false on `efemera:error`
- [ ] Relay mode subscribes to `efemera:channel-changed` (not `channel:selected`)
- [ ] Relay mode shows error from `efemera:error` bus event
- [ ] Relay mode without active channel shows "Select a channel first"
- [ ] IR mode, canvas mode, standard LLM mode all unchanged
- [ ] activeChannelId and activeChannelName state still work for prompt display
- [ ] All tests pass

## Smoke Test
- [ ] `npx vitest run browser/src/primitives/terminal/` — all pass
- [ ] `npx vite build` — zero errors

## Constraints
- Do NOT touch IR mode, canvas mode, or standard LLM mode — only relay mode
- Keep `activeChannelId` and `activeChannelName` state — they're still used for prompt display
- The terminal still needs `bus.send()` — just the event types change
- TDD: verify existing relay tests still pass or update them

## Response File
20260328-EFEMERA-CONN-03-RESPONSE.md
