---
egg: kanban
version: 1.0.0
schema_version: 3
displayName: "Kanban"
description: "Feature inventory kanban board with drag-drop, filters, and accordion columns"
author: "DEIA Solutions"
defaultRoute: /kanban
auth: required
---

# Kanban EGG

Feature inventory kanban board backed by hivenode API. Accordion columns, priority/type filters, drag-drop reordering, mobile responsive.

## Layout

```layout
{
  "type": "pane",
  "nodeId": "kanban-board",
  "appType": "kanban",
  "label": "Kanban",
  "config": {}
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
  "sessionRestoreScope": "global",
  "restoreOrder": "sessionFirst",
  "defaultDocuments": []
}
```

## Permissions

```permissions
{
  "storage": {
    "localStorage": true,
    "sessionStorage": false
  },
  "network": {
    "allowedDomains": [
      "localhost",
      "hivenode.railway.app"
    ]
  }
}
```
