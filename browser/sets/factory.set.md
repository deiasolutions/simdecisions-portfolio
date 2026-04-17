---
egg: factory
version: 1.0.0
schema_version: 3
displayName: DEIA Factory
description: Mobile Factory Manager — queue, alerts, responses, and approvals in a tabbed interface with FAB for spec submission.
author: daaaave-atx
favicon: /icons/factory.svg
defaultRoute: /factory
license: MIT
_stub: false
auth: required
chromeMode: compact
---

# DEIA Factory

Mobile-first factory manager with four main tabs accessible via bottom navigation:
1. **Queue** — monitor active bees and queued specs
2. **Alerts** — notification feed for build events
3. **Responses** — read bee outputs and responses
4. **Approvals** — REQUIRE_HUMAN gate decisions

Bottom nav floats at the bottom for tab switching. Floating action button (FAB) opens spec-submit slideover on demand.

```layout
{
  "type": "split",
  "direction": "vertical",
  "ratio": ["1fr", "56px"],
  "children": [
    {
      "type": "split",
      "direction": "horizontal",
      "ratio": 0.5,
      "children": [
        {
          "type": "split",
          "direction": "horizontal",
          "ratio": 0.5,
          "children": [
            {
              "type": "pane",
              "nodeId": "factory-queue",
              "appType": "queue-pane",
              "label": "Queue",
              "config": {
                "busEvent": "queue:updated",
                "displayMode": "compact"
              },
              "visibility": "visible"
            },
            {
              "type": "pane",
              "nodeId": "factory-alerts",
              "appType": "notification-pane",
              "label": "Alerts",
              "config": {
                "busEvent": "notification:updated",
                "displayMode": "compact"
              },
              "visibility": "hidden"
            }
          ]
        },
        {
          "type": "split",
          "direction": "horizontal",
          "ratio": 0.5,
          "children": [
            {
              "type": "pane",
              "nodeId": "factory-responses",
              "appType": "response-browser",
              "label": "Responses",
              "config": {
                "busEvent": "response:updated",
                "displayMode": "compact"
              },
              "visibility": "hidden"
            },
            {
              "type": "pane",
              "nodeId": "factory-approvals",
              "appType": "approval-cards",
              "label": "Approvals",
              "config": {
                "busEvent": "approval:updated",
                "displayMode": "compact"
              },
              "visibility": "hidden"
            }
          ]
        }
      ]
    },
    {
      "type": "pane",
      "nodeId": "factory-bottom-nav",
      "appType": "bottom-nav",
      "label": "Nav",
      "chrome": false,
      "seamless": true,
      "config": {
        "tabs": [
          {
            "id": "tab-queue",
            "label": "Queue",
            "icon": "list",
            "target": "factory-queue"
          },
          {
            "id": "tab-alerts",
            "label": "Alerts",
            "icon": "bell",
            "target": "factory-alerts"
          },
          {
            "id": "tab-responses",
            "label": "Responses",
            "icon": "message",
            "target": "factory-responses"
          },
          {
            "id": "tab-approvals",
            "label": "Approvals",
            "icon": "check-circle",
            "target": "factory-approvals"
          }
        ],
        "fabButton": {
          "id": "fab-submit",
          "icon": "plus",
          "label": "Submit Spec",
          "trigger": "factory:submit-spec"
        }
      }
    }
  ],
  "slideover": [
    {
      "type": "pane",
      "nodeId": "factory-spec-submit",
      "appType": "spec-submit",
      "label": "Submit Spec",
      "chrome": false,
      "config": {},
      "slideoverMeta": {
        "edge": "bottom",
        "height": "70vh",
        "trigger": "factory:submit-spec",
        "dockable": false,
        "defaultDocked": false,
        "minDockHeight": 600
      }
    }
  ]
}
```

```ui
{
  "chromeMode": "compact",
  "commandPalette": false,
  "akk": false
}
```

```tabs
[
  { "id": "tab-factory", "eggId": "factory", "label": "Factory", "active": false }
]
```

```commands
[
  {
    "name": "submit-spec",
    "label": "Submit Spec",
    "description": "Open spec submission dialog",
    "shortcut": "Cmd+K"
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
  "storage": {
    "localStorage": true,
    "sessionStorage": true
  },
  "network": {
    "allowedDomains": ["localhost"]
  },
  "bus_emit": [
    "queue:*",
    "notification:*",
    "factory:*",
    "diff:*",
    "build:*",
    "gate_enforcer:*",
    "response:*",
    "approval:*",
    "factory:submit-spec"
  ],
  "bus_receive": [
    "queue:*",
    "notification:*",
    "factory:*",
    "diff:*",
    "build:*",
    "gate_enforcer:*",
    "response:*",
    "approval:*"
  ]
}
```

```settings
{
  "mobileOptimized": true,
  "compactDisplay": true,
  "tabVisibility": {
    "queue": true,
    "alerts": true,
    "responses": true,
    "approvals": true
  }
}
```
