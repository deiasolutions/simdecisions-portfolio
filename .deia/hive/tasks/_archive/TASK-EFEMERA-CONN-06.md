# TASK-EFEMERA-CONN-06: Update Efemera EGG Layout + Permissions

**Priority:** P0
**Depends on:** CONN-03, CONN-04, CONN-05
**Blocks:** None
**Model:** Haiku
**Role:** Bee

## Objective

Update `eggs/efemera.egg.md` to use the new efemera-connector primitive, remove the old tree-browser panes, and update the bus permissions to the new `efemera:*` event namespace.

## Read First

- `.deia/BOOT.md` — hard rules
- `eggs/efemera.egg.md` — the file being modified
- `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md` — section 2.4

## Changes to `eggs/efemera.egg.md`

### Layout Block

**Before:** The left sidebar is a tree-browser with `adapter: "channels"`. Members is a separate tree-browser pane at the bottom.

**After:** The left sidebar is `efemera-connector`. The separate members pane is removed (connector renders both tabs).

Replace the layout `children` structure. The new layout:

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

**Key changes:**
- `efemera-channels` tree-browser → `efemera-connector` primitive
- `efemera-members` tree-browser → removed (connector owns both tabs)
- The 3-way vertical split (channels | main | members) becomes 2-way (connector | main)
- Terminal links: `to_channels` renamed to `to_connector`

### Permissions Block

Replace old `channel:*` events with new `efemera:*` namespace:

```json
{
  "storage": { "localStorage": true, "sessionStorage": true },
  "network": { "allowedDomains": ["localhost", "hivenode.railway.app"] },
  "bus_emit": [
    "efemera:message-send",
    "efemera:channel-create",
    "efemera:typing-start",
    "efemera:typing-stop",
    "efemera:channel-changed",
    "efemera:messages-loaded",
    "efemera:message-received",
    "efemera:message-sent",
    "efemera:presence-changed",
    "efemera:typing",
    "efemera:error",
    "efemera:ready"
  ],
  "bus_receive": [
    "efemera:message-send",
    "efemera:channel-create",
    "efemera:typing-start",
    "efemera:typing-stop",
    "efemera:channel-changed",
    "efemera:messages-loaded",
    "efemera:message-received",
    "efemera:message-sent",
    "efemera:presence-changed",
    "efemera:typing",
    "efemera:typing-stop",
    "efemera:error",
    "efemera:ready"
  ]
}
```

### Settings Block

Keep existing settings — they're already correct:
```json
{
  "pollingInterval": 3000,
  "notificationSound": true,
  "presenceAutoIdle": 300000
}
```

## Tests

- Verify EGG parses correctly (if an EGG parser test exists)
- Manual: load efemera EGG in browser, verify layout renders correctly
- The connector primitive should render in the left sidebar
- Text-pane should render in the main area
- Terminal compose bar should render at the bottom

## Constraints

- Do NOT modify the commands, settings, away, or startup blocks (unchanged)
- Keep the menu-bar chrome at top
- The `secondChildAuto` pattern for compose bar stays (terminal auto-sizes)
