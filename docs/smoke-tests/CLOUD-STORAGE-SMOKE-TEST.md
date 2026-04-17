# Cloud Storage Adapter — Manual Smoke Test

## Objective

Verify that chat conversations saved in the browser are persisted to Railway cloud storage and restored on page refresh.

This smoke test validates the complete end-to-end cloud storage integration from the user's perspective: saving chat messages from the browser, verifying they're written to Railway cloud storage, refreshing the page, and confirming messages load back correctly.

---

## Prerequisites

Before running this smoke test, verify the following components are configured and running:

### Environment & Deployment
- [ ] Railway hivenode deployed and running
  - Verify deployment status in Railway dashboard (Status: Active)
  - Know the Railway hivenode URL (e.g., `https://shiftcenter-hivenode.up.railway.app`)
  - Verify health endpoint responds: `curl https://[your-railway-url]/health` → `{"status": "ok"}`
- [ ] Browser dev server running
  - `cd browser && npm run dev`
  - Default URL: `http://localhost:5173`
- [ ] Browser configured to use cloud hivenode (not localhost)
  - Check `browser/.env` file contains: `VITE_HIVENODE_URL=https://[your-railway-url]`
  - OR check runtime config in browser settings

### Authentication
- [ ] Valid JWT token from ra96it.com
  - Token must not be expired (check `exp` claim: visit jwt.io)
  - Token must include `sub` field (user ID)
  - Token stored in browser localStorage key: `auth_token`
- [ ] How to get a token:
  1. Login to ra96it.com
  2. Open DevTools → Application → Local Storage → `https://ra96it.com`
  3. Copy value from `auth_token` key
  4. Paste into your app's localStorage under `auth_token`

### Browser & DevTools
- [ ] Modern browser with DevTools (Chrome, Firefox, Edge, Safari)
- [ ] DevTools accessible (press F12)
- [ ] Network tab can preserve logs across page refresh
- [ ] Console tab can display errors and warnings

### Optional: Railway Storage Access
- [ ] SSH access to Railway container (for direct file verification)
- [ ] Railway logs access (for observing write operations)
- [ ] Railway CLI installed (`railway` command available)

---

## Step-by-Step Test

### Step 1: Open the Browser App and DevTools

1. Navigate to `http://localhost:5173` (or your dev server URL)
2. Wait for the app to fully load
3. Open browser DevTools: press **F12** (Windows/Linux) or **Cmd+Option+I** (Mac)
4. Switch to the **Network** tab
5. Set Network tab filter to: `storage/write` (to isolate storage requests)

### Step 2: Create a Conversation (or Open Terminal)

1. Open a terminal pane or chat interface in the app
2. Ensure a conversation is active (or create a new one)
3. Note the conversation ID from localStorage:
   - Open DevTools **Console** tab
   - Run: `Object.keys(localStorage).filter(k => k.includes('terminal_conv')).slice(0, 1)`
   - Copy the conversation ID for later reference

### Step 3: Send Test Messages to Chat

1. In the terminal/chat pane, type: **`Test message 1 for cloud storage`**
2. Send the message (press Enter or click Send)
3. Wait 1-2 seconds for persistence
4. Type: **`Test message 2: This should persist to Railway`**
5. Send the message
6. Type: **`Final message: Verify after refresh`**
7. Send the message

**Expected:** Three messages appear in the chat pane in order.

### Step 4: Verify Network Requests

In the **Network** tab (filtered for `storage/write`):

1. Look for **POST** requests to `/storage/write`
2. For each request, check:
   - **Status:** Should be `200 OK`
   - **Request Headers:** Look for `Authorization: Bearer <token>`
   - **Request Payload:** Expand the request and check JSON body:
     ```json
     {
       "uri": "cloud://chats/2026-03-16/conversation-conv-XXXXXXXXX.md",
       "content_base64": "# Conversation...(base64 encoded)"
     }
     ```
   - **Response:** Should show `{"ok": true, "uri": "cloud://chats/..."}`

3. **Count:** You should see **at least 4 write requests:**
   - 1 for initial conversation file creation (empty messages)
   - 3 for the three messages you sent (one per addMessage call)

### Step 5: Inspect Stored Data (Optional — Requires Base64 Decoding)

In the **Console** tab, decode a stored message:

1. Copy the `content_base64` value from a `/storage/write` response
2. Run in console:
   ```javascript
   atob('PASTE_BASE64_HERE')
   ```
3. Verify the decoded output contains your test message text
4. Confirm it's in markdown format (e.g., `role: user` or `role: assistant`)

### Step 6: Hard Refresh the Page

1. Press **Ctrl+Shift+R** (Windows) or **Cmd+Shift+R** (Mac) for a hard refresh
2. Clear browser cache if prompted
3. Wait for page to fully load (watch Network tab for `/health` and related requests)

### Step 7: Verify Load Requests

In the **Network** tab (change filter to `storage/read`):

1. Look for **GET** requests to `/storage/read`
2. Check the request URL contains the conversation ID:
   ```
   /storage/read?uri=cloud%3A%2F%2Fchats%2F2026-03-16%2Fconversation-conv-XXXXXXXXX.md
   ```
3. Check response:
   - **Status:** Should be `200 OK`
   - **Response Preview:** Should show markdown content with your test messages

### Step 8: Verify Chat Messages Restored

1. After page refresh, examine the terminal/chat pane
2. Verify all **three messages** are present:
   - "Test message 1 for cloud storage"
   - "Test message 2: This should persist to Railway"
   - "Final message: Verify after refresh"
3. Verify **message order** is correct (in chronological order)
4. Verify **timestamps** are preserved (if displayed)

### Step 9: Check Browser Console for Errors

In the **Console** tab:

1. Look for any red error messages (❌)
2. Filter for `cloud` or `storage` to find relevant logs
3. Verify **no errors** like:
   - `Failed to persist user message`
   - `Failed to persist assistant message`
   - `Cloud storage unreachable`
   - `Conversation not found`

### Step 10: Verify Chat Index (Optional)

In the **Network** tab (change filter to `index.json`):

1. Look for requests to `/storage/read?uri=cloud%3A%2F%2Fchats%2Findex.json`
2. Check response contains conversation metadata:
   ```json
   [
     {
       "id": "conv-XXXXXXXXX",
       "title": null,
       "created_at": "2026-03-16T...",
       "updated_at": "2026-03-16T...",
       "message_count": 3
     }
   ]
   ```

---

## Expected Results

### Network Requests
- ✅ **POST /storage/write** returns **200 OK**
- ✅ File is written to **cloud://chats/YYYY-MM-DD/conversation-[id].md**
- ✅ **GET /storage/read** on page refresh returns **200 OK**
- ✅ **Content-Type** header is correct (application/octet-stream for reads)

### Chat Messages
- ✅ All **3 test messages** restored after page refresh
- ✅ **Message order** is correct (chronological)
- ✅ **Timestamps** are preserved (if applicable)
- ✅ Message **content matches exactly** what was sent

### Browser State
- ✅ **No console errors** (red ❌ messages)
- ✅ **No 401 Unauthorized** errors
- ✅ **No 404 File Not Found** errors
- ✅ **No 503 Service Unavailable** errors

---

## Verification (Optional — For Cloud Storage Admins)

If you have access to Railway storage, verify the file was written correctly:

### Via Railway SSH
1. Open Railway project dashboard
2. Find hivenode service and click **Shell** tab
3. List storage files:
   ```bash
   find /persistent-volume/chats -type f -name "*.md" 2>/dev/null | tail -5
   ```
4. View the most recent conversation file:
   ```bash
   cat /persistent-volume/chats/2026-03-16/conversation-conv-*.md | head -50
   ```
5. Verify the file contains your test messages in markdown format

### Via Railway Logs
1. Open Railway project dashboard → hivenode service → **Logs** tab
2. Filter for `POST /storage/write` in the past 5 minutes
3. Look for log entries like:
   ```
   POST /storage/write - 200 - 542ms - cloud://chats/2026-03-16/conversation-conv-XXXXXXXXX.md
   ```
4. Verify log shows successful write with status 200

### Via Direct File Inspection
1. If you have local access to Railway persistent volume mount, browse:
   ```
   [VOLUME_PATH]/chats/2026-03-16/conversation-conv-XXXXXXXXX.md
   ```
2. Verify file is valid markdown with conversation structure:
   ```markdown
   # Conversation: conv-XXXXXXXXX

   Created: 2026-03-16T...

   ## Message 1

   **Role:** user
   **Content:** Test message 1 for cloud storage
   **Created:** 2026-03-16T...

   ...
   ```

---

## Troubleshooting

### No POST /storage/write Request Appears

**Symptoms:** Network tab shows no `/storage/write` requests when sending messages.

**Possible Causes:**
1. Browser is not configured to use cloud hivenode
2. Chat persistence is disabled
3. Conversation ID is null (conversation not initialized)

**Debug Steps:**
1. Check `.env` or config: `VITE_HIVENODE_URL` should point to Railway hivenode, not localhost
2. In Console, run: `localStorage.getItem('sd:terminal_conversations')`
   - If empty, conversation system not initialized
3. Check if persistence is enabled in EGG config (`persistConversations: true`)
4. Check conversation ID is not null:
   ```javascript
   // In useTerminal.ts, verify conversationId is passed to persistChatMessages()
   console.log('Conversation ID:', conversationId)
   ```

### 401 Unauthorized on /storage/write

**Symptoms:** Network tab shows `/storage/write` returning **401 Unauthorized**.

**Possible Causes:**
1. JWT token missing or not included in request
2. JWT token expired
3. JWT token invalid or malformed

**Debug Steps:**
1. Check localStorage for auth token:
   ```javascript
   localStorage.getItem('auth_token') // or similar key
   ```
2. If token exists, verify it's not expired:
   ```javascript
   // Decode JWT header.payload.signature
   const token = localStorage.getItem('auth_token')
   const parts = token.split('.')
   const payload = JSON.parse(atob(parts[1]))
   console.log('Token expires:', new Date(payload.exp * 1000))
   ```
3. If expired, refresh token from ra96it.com OAuth login
4. Verify token is included in request headers:
   ```javascript
   // In chatApi.ts, hivenodeWrite() should include Authorization header
   ```

### 404 File Not Found on /storage/read

**Symptoms:** Page refresh triggers `/storage/read`, but returns **404 Not Found**.

**Possible Causes:**
1. Conversation file was not written to cloud storage
2. File was written to wrong volume (home:// instead of cloud://)
3. Conversation ID mismatch between write and read

**Debug Steps:**
1. Verify write request succeeded (status 200) before refresh
2. Check conversation file URI in write request:
   - Should be: `cloud://chats/YYYY-MM-DD/conversation-conv-XXXXXXXXX.md`
   - NOT: `home://chats/...` or `localhost://...`
3. Verify conversation ID on load matches ID that was written:
   ```javascript
   // Before refresh, log conversation ID
   // After refresh, verify same ID is used in read request
   ```
4. Check if write request was queued (offline scenario):
   - Response included `{"queued": true}` instead of `{"ok": true}`
   - Indicates cloud was unreachable; file queued for sync

### 503 Service Unavailable

**Symptoms:** `/storage/write` or `/storage/read` returns **503 Service Unavailable**.

**Possible Causes:**
1. Railway hivenode is down or being redeployed
2. Cloud storage adapter is offline
3. Persistent volume is unmounted or inaccessible

**Debug Steps:**
1. Check Railway dashboard: hivenode service status (green = running)
2. Check hivenode `/health` endpoint:
   ```javascript
   fetch('https://shiftcenter-hivenode.up.railway.app/health')
     .then(r => r.json())
     .then(console.log)
   ```
3. Check Railway logs for storage-related errors:
   - Search for "cloud adapter" or "volume offline"
4. If volume is offline, check Railway PostgreSQL or object storage service status

### Messages Don't Restore After Page Refresh

**Symptoms:** Page refresh succeeds, but chat pane is empty (messages not loaded).

**Possible Causes:**
1. `/storage/read` request failed but error was silently caught
2. Response data is malformed (not valid JSON or markdown)
3. Conversation loading failed due to parsing error

**Debug Steps:**
1. Check Console for silent errors:
   ```javascript
   // In chatApi.ts, errors are caught but may only console.warn()
   ```
2. Verify response content is valid markdown:
   - In Network tab, check `/storage/read` response preview
   - Should show markdown with `# Conversation:` header
3. Check parseConversation() function in chatMarkdown.ts:
   - Add console.log() to debug markdown parsing
4. Verify conversation index is readable:
   ```javascript
   fetch('https://shiftcenter-hivenode.up.railway.app/storage/read?uri=cloud%3A%2F%2Fchats%2Findex.json')
     .then(r => r.text())
     .then(console.log)
   ```

### CORS Errors on /storage/write or /storage/read

**Symptoms:** Console shows CORS error: `Access-Control-Allow-Origin` missing.

**Possible Causes:**
1. Railway hivenode CORS headers not configured correctly
2. Browser is making request from different origin than allowed
3. HTTP method (POST, DELETE) blocked by CORS policy

**Debug Steps:**
1. Check Railway hivenode `/health` response headers for CORS:
   ```bash
   curl -i https://shiftcenter-hivenode.up.railway.app/health | grep -i access-control
   ```
2. Verify hivenode config allows browser origin:
   - Should include `*` or explicit origin (e.g., `https://dev.shiftcenter.local`)
3. Check that preflight OPTIONS request is successful:
   - Network tab should show OPTIONS request before POST/DELETE
   - OPTIONS should return 200 OK with CORS headers

### Network Timeout (>30 seconds)

**Symptoms:** `/storage/write` or `/storage/read` takes >30 seconds or times out.

**Possible Causes:**
1. Railway hivenode is slow (high load or cold start)
2. Persistent volume is slow (I/O bottleneck)
3. Network latency is high (geographic distance)

**Debug Steps:**
1. Check Railway metrics: CPU, memory, network usage
2. Check persistent volume I/O metrics
3. Measure network latency:
   ```bash
   ping shiftcenter-hivenode.up.railway.app
   ```
4. Consider implementing request retry logic with exponential backoff

---

## Success Criteria Checklist

Mark each item as ✅ (pass) or ❌ (fail):

### Network & HTTP
- [ ] ✅ POST /storage/write returns 200 OK
- [ ] ✅ Response body is JSON with `ok: true` and file URI
- [ ] ✅ GET /storage/read returns 200 OK
- [ ] ✅ Read response contains full conversation markdown

### Chat Persistence
- [ ] ✅ Three test messages appear in chat pane after sending
- [ ] ✅ Messages maintain correct order (chronological)
- [ ] ✅ Each message has correct content (no truncation or corruption)

### Page Refresh
- [ ] ✅ Page refresh completes without errors (HTTP 200)
- [ ] ✅ Chat pane loads and displays
- [ ] ✅ All three messages restored to chat pane after refresh
- [ ] ✅ Message order remains correct after reload
- [ ] ✅ Timestamps preserved (if applicable)

### Cloud Storage
- [ ] ✅ File written to `cloud://chats/YYYY-MM-DD/conversation-[id].md`
- [ ] ✅ File is accessible on page refresh
- [ ] ✅ File content is valid markdown (no binary corruption)

### Browser State
- [ ] ✅ No console errors (red ❌ messages)
- [ ] ✅ No 401, 403, 404, or 5xx HTTP errors
- [ ] ✅ No CORS errors
- [ ] ✅ No timeout errors

### Optional: Cloud Storage Admin
- [ ] ✅ File visible in Railway persistent volume
- [ ] ✅ File content is valid markdown with correct structure
- [ ] ✅ Railway logs show successful write operations

---

## Summary

**If all checkboxes are ✅:** Cloud storage adapter is working correctly end-to-end.

**If any items are ❌:** Reference the troubleshooting section, collect logs, and report the failure mode in a GitHub issue with the Network tab screenshot and Console output.

**Next Steps:** After successful smoke test, proceed to integration tests covering edge cases (offline scenarios, concurrent writes, large message payloads, etc.).
