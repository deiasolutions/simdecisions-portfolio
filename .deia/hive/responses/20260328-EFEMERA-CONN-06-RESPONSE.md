# SPEC-EFEMERA-CONN-06: Update Efemera EGG Layout + Permissions -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-03-28

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\efemera.egg.md`

## What Was Done

1. **Replaced tree-browser panes with efemera-connector primitive:**
   - Removed `efemera-channels` tree-browser pane (lines 39-50)
   - Removed `efemera-members` tree-browser pane (lines 96-108)
   - Added `efemera-connector` pane with two-tab config (Channels + Members)

2. **Updated layout structure:**
   - Added connector config with `tabs`, `defaultTab`, `pollingIntervalMs`, `presenceAutoIdleMs`
   - Kept menu-bar chrome at top (30px)
   - Maintained `secondChildAuto` pattern for compose bar
   - Added `expandMode: "expand-up"` and `hideStatusBar: true` to terminal config

3. **Updated terminal links:**
   - Changed `to_channels: "efemera-channels"` → `to_connector: "efemera-connector"`
   - Kept `to_text: "efemera-messages"` unchanged

4. **Migrated bus permissions to `efemera:*` namespace:**
   - Removed old events: `channel:selected`, `channel:message-sent`, `channel:message-received`, `channel:messages-loaded`, `presence:update`, `terminal:text-patch`
   - Added new events: `efemera:message-send`, `efemera:channel-create`, `efemera:typing-start`, `efemera:typing-stop`, `efemera:channel-changed`, `efemera:messages-loaded`, `efemera:message-received`, `efemera:message-sent`, `efemera:presence-changed`, `efemera:typing`, `efemera:error`, `efemera:ready`

5. **Fixed JSON syntax error:**
   - Removed extra closing brace and bracket in layout block (was causing validation failure)

6. **Preserved unchanged blocks:**
   - `settings`, `commands`, `away`, `startup`, `ui`, `tabs` blocks remain identical
   - Menu-bar chrome configuration unchanged

## Acceptance Criteria Review

- [x] EGG parses correctly — all 8 JSON blocks validated
- [x] Layout has efemera-connector pane (not tree-browser) in left sidebar — lines 39-54
- [x] No tree-browser panes with adapter: "channels" or "members" — removed both
- [x] Bus permissions use efemera:* namespace only (no channel:* events) — lines 197-226
- [x] Terminal links reference to_connector (not to_channels) — line 91
- [x] Settings block unchanged — lines 166-171 (original settings preserved)
- [x] Commands block unchanged — lines 117-163 (all 4 commands preserved)

## Smoke Test Results

- [x] EGG file is valid markdown with valid JSON blocks — Python validation confirmed all 8 blocks valid
- [ ] `npx vite build` — zero errors — **EXPECTED FAIL**: Build error is unrelated to EGG validity (vite looking for index.html, project uses app.html)

## Notes

- The vite build error (`Cannot resolve entry module index.html`) is a known configuration issue unrelated to EGG file validity
- All JSON blocks in the EGG file parse correctly as validated by Python json module
- Layout structure follows the design doc specification exactly (section 2.4)
- Bus permissions include all 12 events from the connector design (section 3.2)
- The connector primitive will be registered in CONN-02 (not yet implemented)
- Terminal and text-pane refactoring (CONN-03, CONN-04) will wire to these new bus events

## Implementation Details

**Layout changes:**
- Connector pane: nodeId `efemera-connector`, appType `efemera-connector`
- Two tabs: Channels (#) and Members (@)
- Config includes polling interval (3000ms) and presence auto-idle (300000ms)
- Terminal now has `expandMode: "expand-up"` and `hideStatusBar: true` for cleaner compose UI

**Bus migration:**
- Clean swap to `efemera:*` namespace (no migration period)
- All events use `target: '*'` pattern (broadcast to all subscribers)
- Terminal emits `efemera:message-send`, listens for `efemera:message-sent`
- Text-pane listens for `efemera:messages-loaded`, `efemera:message-received`
- Connector owns channel state and emits `efemera:channel-changed`

**Next steps:**
- CONN-02 will implement the efemera-connector primitive React component
- CONN-03 will update terminal to use new bus events
- CONN-04 will update text-pane to use new bus events
- After those specs complete, the efemera EGG will be fully functional with the new architecture
