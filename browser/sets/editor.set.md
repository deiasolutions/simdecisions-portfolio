---
egg: editor
version: 1.0.0
schema_version: 3
displayName: "Editor"
description: "SDEditor text-pane with file explorer, terminal, and all 6 render modes — document, raw, code, diff, chat, process-intake"
author: "DEIA Solutions"
defaultRoute: /editor
auth: required
---

# Editor EGG

Full-featured text editor powered by the SDEditor primitive. Supports all 6 render modes: document, raw, code, diff, chat, and process-intake. Cycle modes with Cmd+Shift+M or the View menu dropdown.

Layout: top-bar (36px) + menu-bar (30px) + main split (1fr) + status-bar (24px).
Main split: sidebar (20%) | editor (1fr) + terminal below.

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
        "appName": "Editor",
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
      "ratio": 0.20,
      "children": [
        {
          "type": "pane",
          "appType": "sidebar",
          "nodeId": "editor-sidebar",
          "label": "Sidebar",
          "chrome": false,
          "config": {
            "panels": [
              { "id": "explorer", "icon": "\ud83d\udcc1", "label": "Explorer", "appType": "file-explorer" }
            ],
            "footerPanels": [
              { "id": "settings", "icon": "\u2699", "label": "Settings" }
            ],
            "defaultPanel": "explorer",
            "activityBarWidth": 48,
            "panelWidth": 240,
            "adapter": "filesystem"
          }
        },
        {
          "type": "split",
          "direction": "horizontal",
          "ratio": 0.70,
          "children": [
            {
              "type": "pane",
              "appType": "text-pane",
              "nodeId": "editor-main",
              "label": "Editor",
              "chrome": false,
              "config": {
                "format": "markdown",
                "readOnly": false,
                "showLineNumbers": true,
                "hideHeader": true
              }
            },
            {
              "type": "pane",
              "appType": "terminal",
              "nodeId": "editor-terminal",
              "label": "Terminal",
              "chrome": false,
              "config": {
                "promptPrefix": "hive>",
                "welcomeBanner": true,
                "collapsed": false
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
[
  {
    "id": "sidebar.toggle",
    "label": "Toggle Sidebar",
    "category": "view",
    "defaultShortcut": "Ctrl+B",
    "scope": "global",
    "handler": "applets.sidebar.toggle"
  }
]
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
