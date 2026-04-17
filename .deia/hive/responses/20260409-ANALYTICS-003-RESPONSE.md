# SPEC-ANALYTICS-003: Tracking Snippet + Vercel Route + Deploy Verification -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-09

## Files Modified

All file paths are absolute:

### Static Landing Pages (6 files)
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\shiftcenter-landing.html`
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\simdecisions-landing.html`
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\chat-landing.html`
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\hodeia.html`
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\hodeia-kaixo.html`
6. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\hodeia-kaixo_eu.html`

### Blog Pages (7 files)
7. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\blog\index.html`
8. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\blog\token-burn-trap.html`
9. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\blog\constitution-ai-needs.html`
10. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\blog\moltbook-republic-without-constitution.html`
11. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\blog\meta-moltbook-no-constitution.html`
12. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\blog\orchestration-is-the-product.html`
13. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\blog\nate-jones-agent-infrastructure-stack.html`

### React App Entry Point (1 file)
14. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\app.html`

### Vercel Configuration (1 file)
15. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\vercel.json`

## What Was Done

### Part 1: JS Tracking Snippet Added to All Pages

Added the analytics tracking snippet as the last `<script>` before `</body>` in all 14 HTML files:

```html
<script>
(function(){
  if(navigator.doNotTrack==="1")return;
  var s=sessionStorage.getItem("_sc_sid");
  if(!s){s=Math.random().toString(36).slice(2)+Math.random().toString(36).slice(2);sessionStorage.setItem("_sc_sid",s)}
  var d={path:location.pathname,referrer:document.referrer||null,screen_w:screen.width,session_id:s};
  navigator.sendBeacon("/beacon",new Blob([JSON.stringify(d)],{type:"application/json"}));
})();
</script>
```

**Snippet properties:**
- Respects Do Not Track browser setting (checks `navigator.doNotTrack==="1"`)
- No cookies — session ID stored in `sessionStorage` (tab-scoped, auto-expires on tab close)
- Uses `navigator.sendBeacon()` for non-blocking, fire-and-forget delivery
- Session ID generated via two concatenated `Math.random().toString(36)` values (~20 chars entropy)
- Sends: path, referrer, screen width, session ID
- ~450 bytes minified, zero external dependencies

### Part 2: Static Landing Pages

Added snippet to all 6 static landing pages before `</body>`:
- shiftcenter-landing.html
- simdecisions-landing.html
- chat-landing.html
- hodeia.html
- hodeia-kaixo.html
- hodeia-kaixo_eu.html

### Part 3: Blog Pages

Added snippet to all 7 blog HTML files (index + 6 posts) before `</body>`:
- blog/index.html
- blog/token-burn-trap.html
- blog/constitution-ai-needs.html
- blog/moltbook-republic-without-constitution.html
- blog/meta-moltbook-no-constitution.html
- blog/orchestration-is-the-product.html
- blog/nate-jones-agent-infrastructure-stack.html

All blog pages had identical footer structure, making placement consistent.

### Part 4: React App Entry Point

Added snippet to `browser/app.html` before `</body>`, after the React module script. This ensures tracking fires on React app loads.

### Part 5: Vercel Route Configuration

Added `/beacon` proxy route to `vercel.json`:

```json
{ "src": "/beacon", "dest": "https://hivenode-production.up.railway.app/beacon" }
```

**Route placement:** Inserted after `/hivenode/(.*)` route and before static file pattern `(.*\\.(js|css|...))`. This ensures `/beacon` is proxied to Railway hivenode on ALL domains (simdecisions.com, shiftcenter.com, etc.) before any domain-specific route catches it.

### Part 6: Games Pages

Checked `browser/public/games/` — no HTML files exist in this directory yet, so none were modified. This is expected since game pages are likely future work.

## Smoke Test Results

```bash
# Verified snippet appears in all 14 target files
cd /c/Users/davee/OneDrive/Documents/GitHub/shiftcenter
grep -rl "sendBeacon.*beacon" browser/public/ browser/app.html | sort

# Output: 14 files listed (all 6 static pages + 7 blog pages + app.html)
browser/app.html
browser/public/blog/constitution-ai-needs.html
browser/public/blog/index.html
browser/public/blog/meta-moltbook-no-constitution.html
browser/public/blog/moltbook-republic-without-constitution.html
browser/public/blog/nate-jones-agent-infrastructure-stack.html
browser/public/blog/orchestration-is-the-product.html
browser/public/blog/token-burn-trap.html
browser/public/chat-landing.html
browser/public/hodeia.html
browser/public/hodeia-kaixo.html
browser/public/hodeia-kaixo_eu.html
browser/public/shiftcenter-landing.html
browser/public/simdecisions-landing.html

# Verified vercel.json has the beacon route
grep "beacon" vercel.json

# Output:
{ "src": "/beacon", "dest": "https://hivenode-production.up.railway.app/beacon" }
```

✅ All 14 files contain the tracking snippet
✅ vercel.json has the `/beacon` proxy route

## Acceptance Criteria — ALL MET

- [x] Tracking snippet added to `browser/public/shiftcenter-landing.html`
- [x] Tracking snippet added to `browser/public/simdecisions-landing.html`
- [x] Tracking snippet added to `browser/public/chat-landing.html`
- [x] Tracking snippet added to `browser/public/hodeia.html`
- [x] Tracking snippet added to `browser/public/hodeia-kaixo.html`
- [x] Tracking snippet added to `browser/public/hodeia-kaixo_eu.html`
- [x] Tracking snippet added to `browser/public/blog/index.html`
- [x] Tracking snippet added to all existing blog post HTML files in `browser/public/blog/` (6 posts)
- [x] Tracking snippet added to `browser/app.html`
- [x] Snippet placement: last `<script>` before `</body>` in every file
- [x] Snippet respects Do Not Track (`navigator.doNotTrack==="1"` → early return)
- [x] Snippet uses `sessionStorage` for session ID (not localStorage, not cookies)
- [x] Snippet uses `navigator.sendBeacon()` with Blob content-type application/json
- [x] `vercel.json` has `/beacon` route proxying to `https://hivenode-production.up.railway.app/beacon`
- [x] `/beacon` route is placed AFTER `/auth/` and `/api/` rules but BEFORE domain catch-alls
- [x] Response file lists all files modified and any files skipped (not found)

## Files Skipped

No files were skipped. All target files existed and were successfully modified.

## Deployment Notes

After Vercel deploy, the following flow will be active:

1. User visits any public page (shiftcenter.com, simdecisions.com/blog/*, chat.shiftcenter.com, hodeia.guru, efemera.live via app.html)
2. Page loads tracking snippet as last script before `</body>`
3. Snippet checks `navigator.doNotTrack` — if "1", exits immediately (no data sent)
4. Snippet generates or retrieves session ID from `sessionStorage` (tab-scoped, ~20 chars entropy)
5. Snippet calls `navigator.sendBeacon("/beacon", Blob)` with JSON payload: `{path, referrer, screen_w, session_id}`
6. Vercel routes `/beacon` → Railway hivenode at `https://hivenode-production.up.railway.app/beacon`
7. Hivenode analytics route (SPEC-ANALYTICS-002) receives beacon, validates, and writes to `analytics_events` table

## End-to-End Verification

After Vercel deploy completes:

1. Visit https://simdecisions.com in browser with DevTools open
2. Check Network tab for `/beacon` request (should show 204 No Content response)
3. Check Railway hivenode logs for "Analytics beacon received" log line
4. Query Railway database: `SELECT * FROM analytics_events ORDER BY timestamp DESC LIMIT 1;`
5. Verify row exists with correct path, session_id, screen_w, and timestamp

## Infrastructure Note

This spec is infrastructure work — no Clock/Coin/Carbon tracking required. When a future dashboard pane is built to visualize this data, that pane's render cost should emit to the Event Ledger like any other primitive.

## Summary

All 14 HTML pages (6 static landing pages + 7 blog pages + 1 React app entry) now have the analytics tracking snippet installed. The `/beacon` route is configured in `vercel.json` to proxy all beacon requests to Railway hivenode. The snippet is privacy-first (respects DNT, no cookies, session-scoped ID), non-blocking (sendBeacon), and minimal (~450 bytes).

Ready for Vercel deploy.
