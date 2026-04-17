---
egg: efemera
version: 1.0.0
schema_version: 3
displayName: Efemera
description: Real-time messaging — channels, DMs, presence. Relay-first layout with channel sidebar, chat bubbles, and compose bar.
author: daaaave-atx
favicon: /icons/efemera.svg
defaultRoute: /efemera
license: MIT
_stub: false
auth: required
---

# Efemera EGG

Real-time messaging app built on ShiftCenter primitives. Channels, DMs, presence indicators, message history.

Layout: top-bar (36px) + menu-bar (30px) + main split (1fr) + status-bar (24px).

```layout
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["36px", "30px", "1fr", "24px"],
  "children": [
    {
      "type": "pane",
      "nodeId": "chrome-top",
      "appType": "top-bar",
      "label": "Top",
      "seamless": true,
      "config": {
        "appName": "Efemera",
        "showKebab": true,
        "showAvatar": true
      }
    },
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
      "ratio": 0.15,
      "children": [
        {
          "type": "pane",
          "nodeId": "efemera-channels",
          "appType": "efemera-connector",
          "label": "Channels",
          "chrome": false,
          "config": {
            "view": "channels",
            "pollingIntervalMs": 3000,
            "presenceAutoIdleMs": 300000
          }
        },
        {
          "type": "split",
          "direction": "vertical",
          "ratio": 0.82,
          "children": [
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
                      "to_connector": "efemera-channels"
                    }
                  }
                }
              ]
            },
            {
              "type": "pane",
              "nodeId": "efemera-members",
              "appType": "efemera-connector",
              "label": "Friends",
              "chrome": false,
              "config": {
                "view": "members"
              }
            }
          ]
        }
      ]
    },
    {
      "type": "pane",
      "nodeId": "chrome-status",
      "appType": "status-bar",
      "label": "Status",
      "seamless": true,
      "config": {
        "currencies": ["clock", "coin", "carbon"],
        "showConnection": true
      }
    }
  ],
  "slideover": [
    {
      "type": "pane",
      "nodeId": "settings-panel",
      "appType": "settings",
      "label": "Settings",
      "chrome": false,
      "config": {},
      "slideoverMeta": {
        "edge": "left",
        "width": "400px",
        "trigger": "settings",
        "dockable": false,
        "defaultDocked": false,
        "minDockWidth": 768
      }
    }
  ]
}
```

```ui
{
  "chromeMode": "auto",
  "commandPalette": true,
  "akk": true
}
```

```tabs
[
  { "id": "tab-efemera", "eggId": "efemera", "label": "Efemera", "active": true }
]
```

```commands
[
  {
    "id": "efemera.new-channel",
    "label": "New Channel",
    "category": "app",
    "defaultShortcut": "Ctrl+Shift+N",
    "scope": "egg",
    "icon": "#",
    "description": "Create a new channel.",
    "tags": ["channel", "new", "create"],
    "handler": "efemera.newChannel"
  },
  {
    "id": "efemera.new-dm",
    "label": "New Message",
    "category": "app",
    "defaultShortcut": "Ctrl+N",
    "scope": "egg",
    "icon": "@",
    "description": "Start a new direct message.",
    "tags": ["dm", "direct", "message", "new"],
    "handler": "efemera.newDM"
  },
  {
    "id": "efemera.members",
    "label": "Toggle Members",
    "category": "view",
    "defaultShortcut": "Ctrl+Shift+M",
    "scope": "egg",
    "icon": "👤",
    "description": "Show or hide the members panel.",
    "tags": ["members", "users", "presence", "panel"],
    "handler": "efemera.toggleMembers"
  },
  {
    "id": "efemera.search",
    "label": "Search Messages",
    "category": "app",
    "defaultShortcut": "Ctrl+F",
    "scope": "egg",
    "icon": "🔍",
    "description": "Search messages in the current channel.",
    "tags": ["search", "find", "messages"],
    "handler": "efemera.searchMessages"
  }
]
```

```settings
{
  "pollingInterval": 3000,
  "notificationSound": true,
  "presenceAutoIdle": 300000
}
```

```away
{
  "idleThresholdMs": 300000,
  "blackoutDelayMs": 600000,
  "message": "Away from keyboard",
  "showFavicon": false,
  "welcomeBack": false
}
```

```startup
{
  "sessionRestore": true,
  "sessionRestoreScope": "perUser",
  "restoreOrder": "sessionFirst",
  "defaultDocuments": []
}
```

```permissions
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
    "efemera:ready",
    "efemera:connection-status"
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
    "efemera:ready",
    "efemera:connection-status"
  ]
}
```
