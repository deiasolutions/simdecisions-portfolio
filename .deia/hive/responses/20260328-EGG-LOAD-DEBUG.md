# EGG-LOAD-DEBUG: Playwright Diagnostic -- canvas2 EGG Load Investigation

**Status:** COMPLETE
**Model:** Opus
**Date:** 2026-03-28

## Summary

**canvas2 EGG loads SUCCESSFULLY.** The reported "Failed to load EGG" error was NOT reproduced by Playwright headless Chromium. All three test scenarios (canvas2, chat, no-egg-param) rendered their full layouts without any "Failed to load" text visible in the DOM.

---

## 1. Every Console Message (Verbatim)

### canvas2 (`?egg=canvas2`) -- 12 messages

| # | Type | Message |
|---|------|---------|
| 0 | debug | `[vite] connecting...` |
| 1 | info | `Download the React DevTools for a better development experience` |
| 2 | debug | `[vite] connected.` |
| 3 | log | `[eggWiring] Registered 6 commands` |
| 4 | log | `[eggWiring] Away manager loaded` |
| 5 | log | `[eggWiring] Permissions registered: [storage, network, bus_emit, bus_receive]` |
| 6 | warning | `WebSocket connection to 'ws://localhost:8020/ws/collaboration?flow_id=flow-untitled-flow&user_id=anonymous&display_name=Anonymous' failed: WebSocket is closed before the connection is established.` |
| 7 | error | `Failed to load resource: the server responded with a status of 404 (Not Found)` at `/api/flow-events/batch` |
| 8 | warning | `[useEventLedger] Flush error: APIError: API error 404: Not Found` |
| 9 | error | `Failed to load resource: the server responded with a status of 404 (Not Found)` at `/api/flow-events/batch` |
| 10 | warning | `[useEventLedger] Flush error: APIError: API error 404: Not Found` |
| 11 | error | `WebSocket connection to 'ws://localhost:8020/ws/collaboration?...' failed: ERR_CONNECTION_REFUSED` |

**Page errors (uncaught exceptions): 0**

### chat (`?egg=chat`) -- 19 messages

| # | Type | Message |
|---|------|---------|
| 0 | debug | `[vite] connecting...` |
| 1 | debug | `[vite] connected.` |
| 2 | info | `Download the React DevTools...` |
| 3 | log | `[eggWiring] Registered 1 commands` |
| 4 | log | `[eggWiring] Permissions registered: [llm, storage, network]` |
| 5-18 | error | `Failed to load resource: the server responded with a status of 401 (Unauthorized)` at `http://localhost:8420/node/discover` (14 times) |

**Page errors (uncaught exceptions): 0**

### no-egg-param (default `/`) -- 36 messages

| # | Type | Message |
|---|------|---------|
| 0 | debug | `[vite] connecting...` |
| 1 | debug | `[vite] connected.` |
| 2 | info | `Download the React DevTools...` |
| 3-5 | warning | `routing.config.egg not loaded -- using hardcoded hostname mappings` (3 times) |
| 6 | log | `[eggWiring] Registered 1 commands` |
| 7 | log | `[eggWiring] Permissions registered: [llm, storage, network]` |
| 8-35 | error | `Failed to load resource: 401 (Unauthorized)` at `http://localhost:8420/node/discover` (28 times) |

**Page errors (uncaught exceptions): 0**

---

## 2. Every Network Request and Status Code

### canvas2 -- 432 requests total

- **All source files (JS, TS, CSS): 200 OK** (430 requests)
- **EGG file: 200 OK** -- `GET http://localhost:5173/canvas2.egg.md` (fetched 2 times, both 200)
- **Auth identity: 200 OK** -- `GET http://localhost:8420/auth/identity` (2 times)
- **Font files: 200 OK** -- Google Fonts DM Sans, JetBrains Mono, Newsreader

**Failed requests (2):**
- `POST http://localhost:5173/api/flow-events/batch` -- 404 Not Found (2 times)
  - Cause: Vite dev server does not proxy `/api/flow-events/batch` to hivenode. The sim component's event ledger tries to POST telemetry events.

### chat -- 459 requests total

- **All source files: 200 OK**
- **EGG file: 200 OK** -- `GET http://localhost:5173/chat.egg.md` (2 times, both 200)

**Failed requests (14):**
- `GET http://localhost:8420/node/discover` -- 401 Unauthorized (14 times)
  - Cause: hivenode `verify_jwt()` rejects requests with no JWT. The browser's `hivenodeDiscovery.ts` polls this endpoint without auth.

### no-egg-param -- 487 requests total

- **All source files: 200 OK**
- **EGG file: 200 OK** -- `GET http://localhost:5173/chat.egg.md` (2 times, both 200, resolved from hostname mapping)

**Failed requests (28):**
- `GET http://localhost:8420/node/discover` -- 401 Unauthorized (28 times)
  - Same cause as chat -- longer load time meant more polling cycles

---

## 3. The Exact Error Message Shown to the User

**There is NO "Failed to load EGG" error visible.** The DOM was searched for:
- Any element containing "Failed to load" text: **NOT FOUND**
- Any element containing "Error" text: matched only CSS `<style>` elements that contain the word "Error" in class names (e.g., `.terminal-error`, `.terminal-error-suggestion`) -- these are CSS rule definitions, not visible error messages
- Any element with `class*="error"` or `class*="Error"`: **NONE found**

### What IS visible on canvas2:
- Menu bar: File, Edit, View, Tools, Help
- Palette sidebar with node types (Start, End, Node, Decision, Resource, etc.)
- Canvas with a sample flow: Start -> Intake -> Valid? -> Processor Pool -> End
- Zoom controls (52%)
- IR terminal with prompt `ir>` and "No API key configured" message
- Status bar: Canvas | claude-sonnet-4-5 | clock: 0.0s | coin: $0.0000 | carbon: 0.0000g

---

## 4. Screenshot Paths

| Scenario | Path |
|----------|------|
| canvas2 | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260328-canvas2-debug.png` |
| chat | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260328-chat-debug.png` |
| no-egg-param | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260328-no-egg-param-debug.png` |
| Full raw output | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260328-egg-load-debug-raw.txt` |

---

## 5. Comparison -- Does Chat Also Fail? Does No-Egg-Param Work?

| Scenario | Loads? | "Failed to load" visible? | EGG fetch status | Page errors |
|----------|--------|--------------------------|------------------|-------------|
| `?egg=canvas2` | YES | NO | 200 OK (x2) | 0 |
| `?egg=chat` | YES | NO | 200 OK (x2) | 0 |
| `/` (default) | YES | NO | 200 OK (x2, chat.egg.md) | 0 |

**All three scenarios load successfully.** None show "Failed to load EGG."

Error counts are misleading -- they are all non-fatal network errors:
- canvas2: 3 console errors (2x `/api/flow-events/batch` 404, 1x WebSocket refused) -- sim component telemetry, not EGG loading
- chat: 14 console errors (all `/node/discover` 401) -- hivenode discovery polling without JWT
- default: 28 console errors (all `/node/discover` 401) -- same, more polling cycles

---

## 6. Root Cause Assessment

**The "Failed to load EGG" error reported by the user was NOT reproduced in this diagnostic run.** Possible explanations:

1. **Transient Vite HMR state:** The user may have seen the error during a hot-module-reload cycle where the EGG loader temporarily threw before Vite finished serving the updated module. A full page refresh would have cleared it.

2. **Browser cache / stale state:** If the user had an older version of `eggLoader.ts` or `parseEggMd.ts` cached that contained a parsing bug since fixed, the error would appear until a hard refresh (Ctrl+Shift+R).

3. **The error was real but is now fixed:** If any recent commits modified the EGG loading pipeline (`eggLoader.ts`, `parseEggMd.ts`, `eggInflater.ts`, `eggToShell.ts`), the fix may already be on the current `dev` branch.

4. **The error is intermittent / race condition:** The EGG file is fetched twice (seen in network logs). If the second fetch raced with the first and one failed transiently, the error boundary could flash "Failed to load" before the successful response replaced it. This was not observed in the diagnostic run.

### Non-EGG Issues Found (Not Blocking, But Worth Noting)

| Issue | Severity | Detail |
|-------|----------|--------|
| `/api/flow-events/batch` 404 | P3 | Vite dev server does not proxy this path to hivenode. The sim component's `useEventLedger` POSTs telemetry here. Add a proxy rule in `vite.config.ts` or suppress the error in dev mode. |
| `ws://localhost:8020` refused | P3 | Collaboration WebSocket server is not running. `useCollaboration.ts` tries to connect. Not a bug -- the collaboration server simply is not started. |
| `/node/discover` 401 x14-28 | P2 | `hivenodeDiscovery.ts` polls `localhost:8420/node/discover` without JWT. The endpoint requires auth via `verify_jwt()`. Either the endpoint should use `verify_jwt_or_local()` for local dev, or the discovery poller should include the JWT from `authStore`. The polling is aggressive (14-28 times in 3 seconds). |
| `routing.config.egg not loaded` | P3 | Warning on no-egg-param route. Uses hardcoded hostname mappings as fallback. Working as intended for localhost dev. |

---

## 7. Fix Recommendation

**No fix needed for the reported issue** -- canvas2 EGG loads correctly. If the user sees the error again:

1. **Hard refresh** (Ctrl+Shift+R) to clear any stale HMR state
2. **Check Vite terminal** for TypeScript compilation errors that could cause partial module delivery
3. **Check browser DevTools Network tab** to confirm `/canvas2.egg.md` returns 200 with valid content

**For the secondary issues found:**

- **P2: `/node/discover` 401 spam** -- Modify `hivenodeDiscovery.ts` to either: (a) not poll when no JWT is available, or (b) change the hivenode endpoint to use `verify_jwt_or_local()`. Also add backoff/retry logic to reduce the 14-28 requests in 3 seconds.
- **P3: `/api/flow-events/batch` 404** -- Add proxy config in `vite.config.ts`: `'/api/flow-events': { target: 'http://localhost:8420' }` or silence the error in dev mode in `useEventLedger.ts`.

---

## Files Created

| File | Purpose |
|------|---------|
| `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\e2e\egg-load-debug.spec.ts` | Playwright test spec (test-runner format) |
| `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\e2e\run-debug.mjs` | Direct Playwright diagnostic script (used for actual run) |
| `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260328-canvas2-debug.png` | Screenshot: canvas2 |
| `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260328-chat-debug.png` | Screenshot: chat |
| `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260328-no-egg-param-debug.png` | Screenshot: no-egg-param |
| `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260328-egg-load-debug-raw.txt` | Full raw diagnostic output (all console messages, all network requests) |
| `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260328-EGG-LOAD-DEBUG.md` | This deliverable |

## Clock / Cost / Carbon

- **Clock:** ~8 minutes
- **Cost:** ~$0.15 (Opus session, no bee dispatch)
- **Carbon:** ~0.02g CO2e
