---
egg: monitor
version: 1.0.0
schema_version: 3
displayName: "Build Monitor"
description: "Live build queue monitor with SSE heartbeat feed from hivenode"
author: "DEIA Solutions"
defaultRoute: /monitor
auth: required
---

# Build Monitor EGG

Live dashboard for monitoring dispatch processes, queue runners, and wave orchestration. Connects to hivenode SSE at /build/stream.

Layout: monitor pane (1fr) + status-bar (24px).

## Layout

```layout
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["1fr", "24px"],
  "children": [
    {
      "type": "pane",
      "nodeId": "monitor-main",
      "appType": "build-monitor",
      "label": "Build Monitor",
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

## Permissions

```permissions
{
  "network": {
    "allowedDomains": [
      "localhost:8420"
    ]
  }
}
```
