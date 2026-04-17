---
egg: chat2
version: 1.0.0
schema_version: 3
displayName: "Chat 2"
description: "AI chat with SC Keyboard input — headless terminal routes through bus"
author: "DEIA Solutions"
defaultRoute: /chat2
auth: required
---

# Chat 2 EGG

AI chat interface using SC Keyboard as the input method. Terminal runs headless
(no built-in prompt) and receives text via `buffer:submit` bus events from the keyboard.

Layout: top-bar (36px) + menu-bar (30px) + chat output (1fr) + headless terminal (1px) + keyboard (280px) + status-bar (24px).

## Layout

```layout
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["36px", "30px", "1fr", "400px", "24px"],
  "children": [
    {
      "type": "pane",
      "nodeId": "chrome-top",
      "appType": "top-bar",
      "label": "Top",
      "seamless": true,
      "config": {
        "appName": "Chat 2",
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
      "direction": "horizontal",
      "ratio": ["1fr", "1px"],
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
            "routeTarget": "ai",
            "inputSource": "bus",
            "displayMode": "minimal",
            "hideStatusBar": true,
            "promptPrefix": "chat2>",
            "zone2Position": "hidden",
            "brandName": "Chat 2",
            "links": {
              "to_text": "chat-output"
            }
          }
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
