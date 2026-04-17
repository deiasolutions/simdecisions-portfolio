# SPEC-ANALYTICS-003: Tracking Snippet + Vercel Route + Deploy Verification

**MODE: EXECUTE**

## Priority
P1

## Depends On
SPEC-ANALYTICS-002

## Model Assignment
sonnet

## Objective

Add the analytics tracking snippet to all public-facing HTML pages and the React app entry point. Add the Vercel proxy route for `/beacon`. Verify end-to-end data flow.

## Read First

- `hivenode/routes/analytics_routes.py` — the beacon endpoint created by SPEC-ANALYTICS-002
- `vercel.json` — current routing rules (the new `/beacon` route must be placed before domain-specific catch-alls)
- `browser/public/simdecisions-landing.html` — example static HTML page
- `browser/public/blog/index.html` — example blog page
- `browser/app.html` — React app entry point

## Implementation

### Part 1: JS Tracking Snippet

The following snippet goes in every page. Add it as the last `<script>` before `</body>`:

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

**Properties:**
- Respects `Do Not Track` browser setting — if DNT=1, snippet exits immediately, no data sent
- No cookies. Session ID via `sessionStorage` — scoped to the browser tab, auto-expires on tab close
- `sendBeacon()` — non-blocking, fire-and-forget, survives page navigation
- ~450 bytes. Zero external dependencies. Zero third-party requests.
- Session ID is two concatenated `Math.random().toString(36)` values for sufficient entropy (~20 chars)

### Part 2: Add Snippet to All Pages (14 files)

Add the snippet before `</body>` in each of these files:

**Static landing pages:**
1. `browser/public/shiftcenter-landing.html`
2. `browser/public/simdecisions-landing.html`
3. `browser/public/chat-landing.html`
4. `browser/public/hodeia.html`
5. `browser/public/hodeia-kaixo.html`
6. `browser/public/hodeia-kaixo_eu.html`

**Blog pages:**
7. `browser/public/blog/index.html`
8. `browser/public/blog/token-burn-trap.html`
9. `browser/public/blog/constitution-ai-needs.html`
10. `browser/public/blog/moltbook-republic-without-constitution.html`
11. `browser/public/blog/meta-moltbook-no-constitution.html`
12. `browser/public/blog/orchestration-is-the-product.html`
13. `browser/public/blog/nate-jones-agent-infrastructure-stack.html`

**React app:**
14. `browser/app.html`

**IMPORTANT:** If any blog HTML files listed above do not exist yet (they may not have been created by the blog specs), skip those files and note which were skipped in the response.

### Part 3: Vercel Route

Add to `vercel.json` **before** the domain-specific catch-all routes but **after** the existing `/auth/(.*)` and `/api/(.*)` proxy rules:

```json
{ "src": "/beacon", "dest": "https://hivenode-production.up.railway.app/beacon" }
```

This ensures `/beacon` is proxied to Railway hivenode on ALL domains (simdecisions.com, shiftcenter.com, etc.) before any domain-specific route catches it.

### Part 4: Games Page (optional)

If `browser/public/games/` contains any HTML files, add the snippet to those too. These are public-facing game pages that should also be tracked.

## Acceptance Criteria

- [ ] Tracking snippet added to `browser/public/shiftcenter-landing.html`
- [ ] Tracking snippet added to `browser/public/simdecisions-landing.html`
- [ ] Tracking snippet added to `browser/public/chat-landing.html`
- [ ] Tracking snippet added to `browser/public/hodeia.html`
- [ ] Tracking snippet added to `browser/public/hodeia-kaixo.html`
- [ ] Tracking snippet added to `browser/public/hodeia-kaixo_eu.html`
- [ ] Tracking snippet added to `browser/public/blog/index.html`
- [ ] Tracking snippet added to all existing blog post HTML files in `browser/public/blog/`
- [ ] Tracking snippet added to `browser/app.html`
- [ ] Snippet placement: last `<script>` before `</body>` in every file
- [ ] Snippet respects Do Not Track (`navigator.doNotTrack==="1"` → early return)
- [ ] Snippet uses `sessionStorage` for session ID (not localStorage, not cookies)
- [ ] Snippet uses `navigator.sendBeacon()` with Blob content-type application/json
- [ ] `vercel.json` has `/beacon` route proxying to `https://hivenode-production.up.railway.app/beacon`
- [ ] `/beacon` route is placed AFTER `/auth/` and `/api/` rules but BEFORE domain catch-alls
- [ ] Response file lists all files modified and any files skipped (not found)

## Smoke Test

After adding snippets, verify the HTML is valid:
```bash
# Check that the snippet appears in all target files
cd /c/Users/davee/OneDrive/Documents/GitHub/shiftcenter
grep -rl "sendBeacon.*beacon" browser/public/ browser/app.html | sort
# Should list all 14 files (minus any that don't exist yet)

# Check vercel.json has the route
grep "beacon" vercel.json
# Should show the proxy rule
```

## Constraints

- Do NOT modify the snippet content — use it exactly as specified above
- Do NOT modify any existing JavaScript or page content — only ADD the snippet
- Do NOT add the snippet to files that already contain it (idempotent)
- Place snippet as last `<script>` before `</body>` — after any existing scripts
- `vercel.json` uses the legacy `routes` array (NOT `rewrites`) — match existing format
- Max diff: each HTML file gets +7 lines (the snippet). vercel.json gets +1 line.
- No stubs, no placeholders

## Infrastructure Note

This spec is infrastructure — no Clock/Coin/Carbon tracking required. When a dashboard pane is built in the future to visualize this data, that pane's render cost should emit to the Event Ledger like any other primitive.

## Response File

`.deia/hive/responses/20260409-ANALYTICS-003-RESPONSE.md`
