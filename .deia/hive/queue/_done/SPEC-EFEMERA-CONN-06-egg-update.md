# SPEC-EFEMERA-CONN-06: Update Efemera EGG Layout + Permissions

> **Project:** Efemera Connector (12 specs submitted as batch, 2026-03-28)
> Dependencies between specs ensure correct execution order.
> Design doc: `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md`

## Priority
P0

## Depends On
- SPEC-EFEMERA-CONN-03-terminal-relay
- SPEC-EFEMERA-CONN-04-textpane-chat
- SPEC-EFEMERA-CONN-05-adapter-cleanup

## Model Assignment
haiku

## Objective

Update `eggs/efemera.egg.md` to use the new efemera-connector primitive, remove the old tree-browser panes, and update the bus permissions to the new `efemera:*` event namespace.

## Read First

- `.deia/BOOT.md` — hard rules
- `eggs/efemera.egg.md` — the file being modified
- `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md` — section 2.4

## Changes to `eggs/efemera.egg.md`

### Layout Block

**Before:** The left sidebar is a tree-browser with `adapter: "channels"`. Members is a separate tree-browser pane.

**After:** The left sidebar is `efemera-connector`. The separate members pane is removed (connector renders both tabs).

New layout:
```json
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["30px", "1fr"],
  "children": [
    {
      "type": "pane",
      "nodeId": "chrome-menu",
      "appType": "menu-bar",
      "label": "Menu",
      "seamless": true,
      "config": {}
    },
    {
      "type": "split",
      "direction": "vertical",
      "ratio": 0.18,
      "children": [
        {
          "type": "pane",
          "nodeId": "efemera-connector",
          "appType": "efemera-connector",
          "label": "Efemera",
          "chrome": false,
          "config": {
            "tabs": [
              { "id": "channels", "icon": "#", "label": "Channels" },
              { "id": "members", "icon": "@", "label": "Members" }
            ],
            "defaultTab": "channels",
            "pollingIntervalMs": 3000,
            "presenceAutoIdleMs": 300000
          }
        },
        {
          "type": "split",
          "direction": "horizontal",
          "ratio": 0.88,
          "seamless": true,
          "secondChildAuto": true,
          "children": [
            {
              "type": "pane",
              "nodeId": "efemera-messages",
              "appType": "text-pane",
              "label": "Messages",
              "chrome": false,
              "headless": true,
              "config": {
                "format": "markdown",
                "readOnly": true,
                "renderMode": "chat",
                "hideHeader": true
              }
            },
            {
              "type": "pane",
              "nodeId": "efemera-compose",
              "appType": "terminal",
              "label": "Compose",
              "chrome": false,
              "config": {
                "displayMode": "minimal",
                "expandMode": "expand-up",
                "routeTarget": "relay",
                "promptPrefix": ">",
                "brandName": "Efemera",
                "hideStatusBar": true,
                "links": {
                  "to_text": "efemera-messages",
                  "to_connector": "efemera-connector"
                }
              }
            }
          ]
        }
      ]
    }
  ]
}
```

### Permissions Block

Replace old `channel:*` events with new `efemera:*` namespace:

```json
{
  "bus_emit": [
    "efemera:message-send", "efemera:channel-create",
    "efemera:typing-start", "efemera:typing-stop",
    "efemera:channel-changed", "efemera:messages-loaded",
    "efemera:message-received", "efemera:message-sent",
    "efemera:presence-changed", "efemera:typing",
    "efemera:error", "efemera:ready"
  ],
  "bus_receive": [
    "efemera:message-send", "efemera:channel-create",
    "efemera:typing-start", "efemera:typing-stop",
    "efemera:channel-changed", "efemera:messages-loaded",
    "efemera:message-received", "efemera:message-sent",
    "efemera:presence-changed", "efemera:typing",
    "efemera:typing-stop", "efemera:error", "efemera:ready"
  ]
}
```

## Acceptance Criteria
- [ ] EGG parses correctly
- [ ] Layout has efemera-connector pane (not tree-browser) in left sidebar
- [ ] No tree-browser panes with adapter: "channels" or "members"
- [ ] Bus permissions use efemera:* namespace only (no channel:* events)
- [ ] Terminal links reference to_connector (not to_channels)
- [ ] Settings block unchanged
- [ ] Commands block unchanged

## Smoke Test
- [ ] EGG file is valid markdown with valid JSON blocks
- [ ] `npx vite build` — zero errors

## Constraints
- Do NOT modify the commands, settings, away, or startup blocks (unchanged)
- Keep the menu-bar chrome at top
- The `secondChildAuto` pattern for compose bar stays (terminal auto-sizes)

## Response File
20260328-EFEMERA-CONN-06-RESPONSE.md
