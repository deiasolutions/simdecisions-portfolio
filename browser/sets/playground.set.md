---
egg: playground
version: 1.0.0
schema_version: 3
displayName: "Playground"
description: "Shell playground — test splits, merges, tabs, drag, swap, and pane chrome"
author: "DEIA Solutions"
defaultRoute: /playground
auth: required
---

# Playground EGG

Test environment for shell pane management. Single pane — use the hamburger menu to split, merge, flip, swap, and resize.

Layout: terminal pane (1fr) + status-bar (24px).

## Layout

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
        "appName": "Playground",
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
      "type": "pane",
      "nodeId": "pg-main",
      "appType": "terminal",
      "label": "Playground",
      "config": {
        "promptPrefix": "hive>",
        "statusBarCurrencies": ["clock", "coin", "carbon"]
      }
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

## UI

```ui
{
  "chromeMode": "auto",
  "commandPalette": true,
  "akk": true
}
```

## Commands

```commands
[]
```

## Startup

```startup
{
  "sessionRestore": false,
  "defaultDocuments": []
}
```

## Permissions

```permissions
{
  "llm": {
    "providers": ["anthropic"],
    "requireApiKey": true,
    "allowBYOK": true
  },
  "storage": {
    "localStorage": true
  }
}
```
