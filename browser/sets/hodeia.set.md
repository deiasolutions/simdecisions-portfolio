---
egg: hodeia
version: 1.0.0
schema_version: 3
displayName: "Hodeia"
description: "Brand home — sky theme landing page. hodeia gara — we are the cloud."
author: "DEIA Solutions"
favicon: /icons/hodeia.svg
defaultRoute: /
auth: public
---

# Hodeia EGG

Brand landing page for hodeia.guru. Sky theme with day/night toggle, seasonal particles, city weather animations, domain liturgy, product grid, and three currencies.

## Layout

```layout
{
  "type": "pane",
  "nodeId": "hodeia-landing",
  "appType": "hodeia-landing",
  "label": "Hodeia",
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
  "network": { "allowedDomains": ["fonts.googleapis.com", "fonts.gstatic.com"] }
}
```
