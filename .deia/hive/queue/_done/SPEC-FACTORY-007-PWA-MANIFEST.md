# SPEC-FACTORY-007: Factory PWA Manifest

**MODE: EXECUTE**

**Spec ID:** SPEC-FACTORY-007
**Created:** 2026-04-09
**Author:** Q88N
**Type:** CONFIG
**Status:** READY
**Wave:** 1 (no dependencies)

---

## Priority
P0

## Depends On
None

## Model Assignment
haiku

## Purpose

Create PWA manifest and update service worker for Factory mobile app. Enables "Add to Home Screen" on iOS/Android with DEIA Factory branding. Adds `/factory/` routes to network-first caching.

**Deliverable:** PWA config files (~80 lines total)

---

## Current State

Existing PWA files:
- `browser/public/manifest.json` — Hodeia branding
- `browser/public/sw.js` — basic cache strategy, no push

Need:
- Factory-specific manifest (or update existing)
- Service worker updates for `/factory/` routes
- Push notification listener stub (for P2)

---

## Implementation

### Option A: Separate Manifest (Recommended)

Create `manifest-factory.json` for factory-specific branding. Load via query param or subdomain detection.

### Option B: Update Existing

Update `manifest.json` with factory branding (simpler but loses Hodeia branding).

**Going with Option A** — separate manifest allows different branding per product.

---

## Files

### browser/public/manifest-factory.json

```json
{
  "name": "DEIA Factory",
  "short_name": "Factory",
  "description": "AI Factory Operations Manager",
  "start_url": "/?set=factory",
  "display": "standalone",
  "orientation": "portrait-primary",
  "background_color": "#0a0a0f",
  "theme_color": "#8b5cf6",
  "icons": [
    {
      "src": "/icons/factory-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/factory-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ],
  "categories": ["productivity", "developer tools"],
  "shortcuts": [
    {
      "name": "Queue",
      "short_name": "Queue",
      "url": "/?set=factory&tab=queue",
      "icons": [{ "src": "/icons/queue-96.png", "sizes": "96x96" }]
    },
    {
      "name": "New Spec",
      "short_name": "Spec",
      "url": "/?set=factory&action=new-spec",
      "icons": [{ "src": "/icons/plus-96.png", "sizes": "96x96" }]
    }
  ],
  "screenshots": [
    {
      "src": "/screenshots/factory-queue.png",
      "sizes": "1080x1920",
      "type": "image/png",
      "label": "Queue Dashboard"
    }
  ]
}
```

### browser/public/sw.js (Updates)

Add to existing service worker:

```javascript
// Add to NETWORK_FIRST_ROUTES
const NETWORK_FIRST_ROUTES = [
  '/api/',
  '/factory/',      // <-- ADD
  '/build/',
  '/governance/',
];

// Add push notification listener (stub for P2)
self.addEventListener('push', (event) => {
  if (!event.data) return;
  
  const data = event.data.json();
  const options = {
    body: data.body || 'Factory notification',
    icon: '/icons/factory-192.png',
    badge: '/icons/factory-badge-72.png',
    tag: data.tag || 'factory-notification',
    data: {
      url: data.url || '/?set=factory',
    },
    actions: data.actions || [],
  };
  
  event.waitUntil(
    self.registration.showNotification(data.title || 'DEIA Factory', options)
  );
});

// Handle notification click
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  const url = event.notification.data?.url || '/?set=factory';
  
  event.waitUntil(
    clients.matchAll({ type: 'window' }).then((windowClients) => {
      // Focus existing window if open
      for (const client of windowClients) {
        if (client.url.includes('set=factory') && 'focus' in client) {
          return client.focus();
        }
      }
      // Otherwise open new window
      return clients.openWindow(url);
    })
  );
});
```

### browser/index.html (Update)

Add manifest switching logic:

```html
<script>
  // Load appropriate manifest based on route
  const isFactory = window.location.search.includes('set=factory') || 
                    window.location.hostname.startsWith('factory.');
  const manifestUrl = isFactory ? '/manifest-factory.json' : '/manifest.json';
  document.querySelector('link[rel="manifest"]').href = manifestUrl;
</script>
```

Or simpler — update the `<link>` tag dynamically in React.

---

## Icon Assets Needed

Create placeholder icons (can be refined later):

| File | Size | Purpose |
|------|------|---------|
| `icons/factory-192.png` | 192x192 | Home screen icon |
| `icons/factory-512.png` | 512x512 | Splash screen |
| `icons/factory-badge-72.png` | 72x72 | Notification badge |
| `icons/queue-96.png` | 96x96 | Shortcut icon |
| `icons/plus-96.png` | 96x96 | New spec shortcut |

For now: copy existing icons and rename, or create simple colored squares.

---

## File Targets

| File | Action | Lines |
|------|--------|-------|
| `browser/public/manifest-factory.json` | CREATE | ~50 |
| `browser/public/sw.js` | MODIFY | +30 |
| `browser/index.html` or `App.tsx` | MODIFY | +5 |
| `browser/public/icons/factory-*.png` | CREATE | (assets) |

---

## Reference Files

Read before implementation:
- `browser/public/manifest.json` — existing manifest format
- `browser/public/sw.js` — existing service worker
- `browser/index.html` — manifest link location

---

## Acceptance Criteria

- [ ] `manifest-factory.json` exists and is valid JSON
- [ ] Service worker caches `/factory/` routes network-first
- [ ] Push notification listener registered (stub, no backend yet)
- [ ] Notification click opens factory view
- [ ] Manifest switches based on `?set=factory` param
- [ ] "Add to Home Screen" works on iOS Safari
- [ ] "Add to Home Screen" works on Android Chrome
- [ ] App launches in standalone mode (no browser chrome)

## Smoke Test

```bash
# Manifest exists and is valid
cat browser/public/manifest-factory.json | jq

# Service worker has factory routes
grep -q "/factory/" browser/public/sw.js && echo "Route added" || echo "MISSING"

# Push listener exists
grep -q "addEventListener('push'" browser/public/sw.js && echo "Push listener" || echo "MISSING"

# Manual test:
# 1. Open http://localhost:5173/?set=factory on mobile
# 2. Tap "Add to Home Screen" (iOS: Share > Add to Home Screen)
# 3. Launch from home screen
# 4. Verify standalone mode (no URL bar)
```

## Constraints

- No external dependencies
- Keep service worker under 100 lines total
- Icons can be placeholders for now
- Push notifications are stubs only (backend in P2)

## Response File

`.deia/hive/responses/20260409-FACTORY-007-RESPONSE.md`

---

*SPEC-FACTORY-007 — Q88N — 2026-04-09*
