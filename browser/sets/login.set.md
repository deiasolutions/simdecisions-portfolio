---
egg: login
version: 1.0.0
schema_version: 3
displayName: "Login"
description: "Authentication page for GitHub OAuth and dev-login"
author: "DEIA Solutions"
favicon: /icons/login.svg
defaultRoute: /login
auth: public
---

# Login EGG

Minimal authentication interface for hodeia authentication.
Provides GitHub OAuth flow and dev-login option (when available).

## Layout

```layout
{
  "type": "pane",
  "nodeId": "auth-pane",
  "appType": "auth",
  "label": "Login",
  "config": {
    "onAuthSuccess": "handleAuthSuccess"
  }
}
```

## Features

- GitHub OAuth button (click → fetch login URL → redirect to GitHub)
- Dev-login button (optional, shown when `/dev-login/available` returns true)
- Consent section (Terms, Privacy, Community Guidelines)
- Loading spinner during redirect
- CSS variables only (no hardcoded colors)
- localStorage persistence (`sd_auth_token`, `sd_auth_user`)
