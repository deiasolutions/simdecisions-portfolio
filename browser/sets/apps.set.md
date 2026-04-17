---
egg: apps
version: 0.1.0
schema_version: 3
displayName: App Directory
description: Browse and launch ShiftCenter EGGs.
author: daaaave-atx
defaultRoute: /apps
license: MIT
_stub: false
auth: required
---

# App Directory EGG

Browse and launch ShiftCenter EGGs. Grid view of all installed applications with search, filtering by category, and quick launch.

Layout: status-bar (24px) + apps-home pane (1fr).

```layout
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["1fr", "24px"],
  "children": [
    {
      "type": "pane",
      "nodeId": "apps-directory",
      "appType": "apps-home",
      "label": "App Directory",
      "config": {
        "sections": ["core", "productivity", "platform"],
        "showSearch": true
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
  { "id": "tab-apps", "eggId": "apps-home", "label": "Apps", "active": true }
]
```

```permissions
{
  "storage": { "localStorage": true, "sessionStorage": false },
  "network": { "allowedDomains": ["localhost", "hivenode.railway.app"] },
  "bus_emit": ["egg:inflate"],
  "bus_receive": []
}
```

```settings
{
  "defaultView": "grid"
}
```
