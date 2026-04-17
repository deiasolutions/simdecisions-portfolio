---
egg: chat
version: 1.0.0
schema_version: 3
displayName: "Chat"
description: "AI chat interface powered by terminal primitive and terminal service"
author: "DEIA Solutions"
defaultRoute: /chat
---

# Chat EGG

AI chat interface with LLM integration, session management, and 3-currency ledger.

## Layout

```layout
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
      "ratio": 0.7,
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
          "nodeId": "chat-main",
          "appType": "terminal",
          "label": "Terminal",
          "config": {
            "llmProvider": "anthropic",
            "statusBarCurrencies": ["clock", "coin", "carbon"],
            "promptPrefix": "hive>",
            "routeTarget": "ai",
            "zone2Position": "bottom",
            "zone2Default": "expanded",
            "links": {
              "to_text": "chat-output"
            }
          }
        }
      ]
    }
  ]
}
```

## UI

```ui
{
  "theme": "default",
  "statusBar": true,
  "menuBar": false,
  "shellTabBar": false
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
