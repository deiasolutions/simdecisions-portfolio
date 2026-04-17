---
egg: constitution
version: 1.0.0
schema_version: 3
displayName: "Constitution"
description: "Hodeia governance home — ethics, carbon, grace. #NOKINGS. User sovereignty over data and compute."
author: "DEIA Solutions"
favicon: /icons/constitution.svg
defaultRoute: /constitution
auth: public
---

# Constitution EGG

Governance document browser for hodeia.org. Surfaces DEIA principles: ethics.yml, carbon.yml, grace.yml, and the constitutional framework.

Layout:
- Left (22%): tree-browser with governance-docs adapter — document list
- Right (78%): text-pane in doc renderMode — rendered document content

```layout
{
  "type": "split",
  "direction": "vertical",
  "ratio": 0.22,
  "children": [
    {
      "type": "pane",
      "nodeId": "constitution-nav",
      "appType": "tree-browser",
      "label": "Documents",
      "config": {
        "adapter": "governance-docs",
        "header": "Governance",
        "searchPlaceholder": "Search documents..."
      }
    },
    {
      "type": "pane",
      "nodeId": "constitution-content",
      "appType": "text-pane",
      "label": "Document",
      "config": {
        "format": "markdown",
        "readOnly": true,
        "renderMode": "doc"
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

## Startup

```startup
{
  "sessionRestore": false,
  "sessionRestoreScope": "none",
  "restoreOrder": "sessionFirst",
  "defaultDocuments": []
}
```

## Permissions

```permissions
{
  "storage": { "localStorage": true, "sessionStorage": false },
  "network": { "allowedDomains": ["localhost", "hivenode.railway.app"] },
  "bus_emit": ["file:selected"],
  "bus_receive": ["file:selected"]
}
```
