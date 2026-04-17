---
egg: chat
version: 1.0.0
schema_version: 3
displayName: "Chat"
description: "AI chat interface powered by terminal primitive and terminal service"
author: "DEIA Solutions"
defaultRoute: /chat
auth: required
---

# Chat EGG

AI chat interface with LLM integration, session management, and 3-currency ledger.

Layout: top-bar (36px) + menu-bar (30px) + main split (1fr) + status-bar (24px).

## Layout

```layout
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["36px", "30px", "1fr", "280px", "24px"],
  "children": [
    {
      "type": "pane",
      "nodeId": "chrome-top",
      "appType": "top-bar",
      "label": "Top",
      "seamless": true,
      "config": {
        "appName": "Chat",
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
      "ratio": 0.22,
      "children": [
        {
          "type": "pane",
          "nodeId": "chat-sidebar",
          "appType": "tree-browser",
          "label": "History",
          "config": {
            "adapter": "chat-history",
            "header": "History",
            "searchPlaceholder": "Search chats..."
          }
        },
        {
          "type": "split",
          "direction": "horizontal",
          "ratio": ["1fr", "1px"],
          "seamless": true,
          "children": [
            {
              "type": "pane",
              "nodeId": "chat-output",
              "appType": "text-pane",
              "label": "Chat",
              "config": {
                "format": "markdown",
                "readOnly": true,
                "renderMode": "chat"
              }
            },
            {
              "type": "pane",
              "nodeId": "chat-engine",
              "appType": "terminal",
              "label": "Engine",
              "seamless": true,
              "config": {
                "llmProvider": "anthropic",
                "statusBarCurrencies": ["clock", "coin", "carbon"],
                "promptPrefix": "hive>",
                "routeTarget": "ai",
                "inputSource": "bus",
                "displayMode": "minimal",
                "hideStatusBar": true,
                "zone2Position": "hidden",
                "brandName": "Chat",
                "links": {
                  "to_text": "chat-output"
                }
              }
            }
          ]
        }
      ]
    },
    {
      "type": "pane",
      "nodeId": "chat-keyboard",
      "appType": "sc-keyboard",
      "label": "Keyboard",
      "seamless": true,
      "config": {}
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
    "name": "new",
    "label": "New Conversation",
    "description": "Start a new conversation",
    "shortcut": "Cmd+N"
  }
]
```

## Startup

```startup
{
  "sessionRestore": true,
  "sessionRestoreScope": "perUser",
  "restoreOrder": "sessionFirst",
  "defaultDocuments": []
}
```

## Permissions

```permissions
{
  "llm": {
    "providers": ["anthropic", "groq", "openai"],
    "requireApiKey": true,
    "allowBYOK": true
  },
  "storage": {
    "localStorage": true,
    "sessionStorage": true
  },
  "network": {
    "allowedDomains": [
      "api.anthropic.com",
      "api.groq.com",
      "api.openai.com"
    ]
  }
}
```
