---
egg: build-monitor
version: 1.0.0
schema_version: 3
displayName: Build Monitor
description: Live 4-column build pipeline monitor — active bees, queue, build log, completed results.
author: daaaave-atx
favicon: /icons/build-monitor.svg
defaultRoute: /build-monitor
license: MIT
_stub: false
auth: required
---

# Build Monitor EGG

Live build pipeline monitor with 4-column layout. Data flows from hivenode
at localhost:8420 through an invisible data service applet, broadcast on the
bus, consumed by tree-browser panes.

Layout:
- Top (28px): build-data-service — SSE connection + compact status bar
- Dashboard (8%): build-dashboard — pipeline stage counts with type breakdown
- Col 1 (15%): ACTIVE BEES — currently running/dispatched tasks
- Col 2 (15%): RUNNER QUEUE — specs waiting to be dispatched
- Col 3 (45%): BUILD LOG — heartbeat log feed, newest first
- Col 4 (25%): COMPLETED — failed then completed, newest first

```layout
{
  "type": "split",
  "direction": "horizontal",
  "ratio": 0.04,
  "children": [
    {
      "type": "pane",
      "nodeId": "build-service",
      "appType": "build-data-service",
      "label": "Status",
      "chrome": false,
      "config": {}
    },
    {
      "type": "split",
      "direction": "horizontal",
      "ratio": 0.08,
      "children": [
        {
          "type": "pane",
          "nodeId": "build-dashboard",
          "appType": "build-dashboard",
          "label": "Pipeline",
          "chrome": false,
          "config": {}
        },
        {
          "type": "split",
          "direction": "vertical",
          "ratio": 0.30,
      "children": [
        {
          "type": "split",
          "direction": "vertical",
          "ratio": 0.50,
          "children": [
            {
              "type": "pane",
              "nodeId": "build-bees",
              "appType": "tree-browser",
              "label": "Active",
              "config": {
                "adapter": "bus",
                "busEvent": "build:bees-updated",
                "header": "ACTIVE",
                "searchPlaceholder": "Search bees..."
              }
            },
            {
              "type": "pane",
              "nodeId": "build-runner",
              "appType": "tree-browser",
              "label": "Queue",
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
          "type": "split",
          "direction": "vertical",
          "ratio": 0.64,
          "children": [
            {
              "type": "pane",
              "nodeId": "build-log",
              "appType": "tree-browser",
              "label": "Build Log",
              "config": {
                "adapter": "bus",
                "busEvent": "build:log-updated",
                "header": "BUILD LOG",
                "searchPlaceholder": "Search log..."
              }
            },
            {
              "type": "pane",
              "nodeId": "build-completed",
              "appType": "tree-browser",
              "label": "Completed",
              "config": {
                "adapter": "bus",
                "busEvent": "build:completed-updated",
                "header": "COMPLETED",
                "searchPlaceholder": "Search results..."
              }
            }
          ]
        }
      ]
        }
      ]
    }
  ]
}
```

```ui
{
  "chromeMode": "auto",
  "commandPalette": false,
  "menuBar": false,
  "statusBar": false,
  "shellTabBar": false
}
```

```tabs
[
  { "id": "tab-build-monitor", "eggId": "build-monitor", "label": "Build Monitor", "active": true }
]
```

```commands
[]
```

```settings
{
  "pollingInterval": 5000
}
```

```permissions
{
  "storage": { "localStorage": false, "sessionStorage": false },
  "network": { "allowedDomains": ["localhost"] },
  "bus_emit": [
    "build:bees-updated",
    "build:runner-updated",
    "build:log-updated",
    "build:completed-updated"
  ],
  "bus_receive": [
    "build:bees-updated",
    "build:runner-updated",
    "build:log-updated",
    "build:completed-updated"
  ]
}
```
