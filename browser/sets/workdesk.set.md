---
egg: workdesk
version: 0.2.0
schema_version: 3
displayName: Workdesk
description: Conversation workspace with chat output, command terminal, build queue sidebar, and keyboard input.
author: daaaave-atx
defaultRoute: /workdesk
license: MIT
_stub: false
auth: required
---

# Workdesk

Conversational command workspace. Chat output on the left, build queue sidebar on the right, terminal at the bottom. Standard chrome frame.

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
        "appName": "Workdesk",
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
      "ratio": 0.75,
      "children": [
        {
          "type": "split",
          "direction": "horizontal",
          "ratio": 0.70,
          "children": [
            {
              "type": "pane",
              "nodeId": "workdesk-chat",
              "appType": "text-pane",
              "label": "Conversation",
              "chrome": false,
              "config": {
                "format": "markdown",
                "readOnly": true,
                "renderMode": "chat",
                "hideHeader": true
              }
            },
            {
              "type": "pane",
              "nodeId": "workdesk-engine",
              "appType": "terminal",
              "label": "Command",
              "chrome": false,
              "config": {
                "llmProvider": "anthropic",
                "statusBarCurrencies": ["clock", "coin", "carbon"],
                "promptPrefix": "hive>",
                "routeTarget": "ai",
                "brandName": "Workdesk",
                "links": {
                  "to_text": "workdesk-chat"
                }
              }
            }
          ]
        },
        {
          "type": "pane",
          "nodeId": "workdesk-queue",
          "appType": "tree-browser",
          "label": "Queue",
          "chrome": false,
          "config": {
            "adapter": "bus",
            "busEvent": "build:runner-updated",
            "header": "QUEUE",
            "searchPlaceholder": "Search queue..."
          }
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
      "api.openai.com",
      "localhost"
    ]
  },
  "bus_emit": [
    "terminal:input",
    "conversation:message",
    "queue:refresh"
  ],
  "bus_receive": [
    "terminal:response",
    "conversation:message",
    "conversation:assistant-response",
    "build:runner-updated"
  ]
}
```

```settings
{
  "voiceEnabled": true,
  "suggestionsEnabled": true,
  "notificationBadges": true,
  "queuePollInterval": 10000
}
```
