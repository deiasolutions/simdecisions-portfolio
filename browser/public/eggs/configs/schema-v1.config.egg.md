---
schema_version: 3
type: config
eggId: schema-v1.config
name: Schema v1 Field Translation
description: Legacy field name mappings for EGGs with schema_version 1. Kept permanently so old EGGs always work.
author: SimDecisions Platform Team
version: 1.0.0
---

# Schema v1 Translation Table

This config EGG provides backward compatibility for EGGs written before schema_version 3.
When an app EGG declares `schema_version: 1`, the inflater runs it through this translation table
before validation. This ensures old EGGs work forever without manual migration.

Field mappings (oldName -> newName):
- `id` -> `nodeId` (all node types)
- `appConfig` -> `config` (app nodes)
- `title` -> `label` (app nodes)
- `pane` -> `appType` (app nodes, rare legacy usage)
- `cols` -> `children` (split/triple-split nodes, rare)

```fieldMap
{
  "node": {
    "id": "nodeId",
    "title": "label",
    "appConfig": "config",
    "pane": "appType"
  },
  "split": {
    "cols": "children"
  },
  "triple-split": {
    "cols": "children"
  }
}
```
