---
schema_version: 3
type: config
eggId: routing.config
name: Hostname Routing Table
description: Maps hostnames to EGG IDs. Replaces hardcoded hostnameMap in eggResolver.ts.
author: ShiftCenter Platform Team
version: 1.0.0
---

# Hostname Routing Table

This config EGG defines which app EGG to load based on the current hostname.
Making routing configurable without code changes.

Priority order:
1. URL param `?egg=` (override)
2. Hostname exact match in `subdomains` map
3. `fallback` EGG ID

```routing
{
  "subdomains": {
    "chat.efemera.live": "chat",
    "code.shiftcenter.com": "code",
    "pm.shiftcenter.com": "pm",
    "dev.shiftcenter.com": "chat",
    "apps.shiftcenter.com": "apps",
    "dev.ra96it.com": "login",
    "ra96it.com": "login",
    "www.ra96it.com": "login",
    "localhost:5173": "chat",
    "localhost:3000": "chat"
  },
  "fallback": "chat",
  "urlParam": "egg"
}
```
