# TASK-209: Cloud Storage Adapter Manual Smoke Test Documentation

## Objective
Write clear, step-by-step instructions for manually smoke testing the cloud storage adapter end-to-end from the browser UI. Document how to verify that chat conversations save to cloud storage and load on page refresh.

## Context
The cloud storage adapter E2E tests (TASK-190) verify the HTTP API layer. This task documents the **manual smoke test** from the user's perspective: saving a chat conversation from the browser, verifying it's written to Railway cloud storage, refreshing the page, and verifying it loads back.

This is a **documentation task**, not a code task. The output is a markdown document with step-by-step instructions that Q88N (Dave) or any developer can follow to verify the cloud storage integration works end-to-end.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminalChatPersist.ts` — chat persistence logic
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\buildDataService.tsx` — data service wiring (if relevant to cloud storage)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\build-monitor.egg.md` — example EGG config (if it uses terminal with chat persistence)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-16-3005-SPEC-w3-06-cloud-adapter-e2e.md` — original spec with smoke test requirement

## Deliverables
- [ ] New documentation file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\smoke-tests\CLOUD-STORAGE-SMOKE-TEST.md`
- [ ] Section: **Prerequisites** — what needs to be running (Railway hivenode, browser dev server, JWT token)
- [ ] Section: **Step-by-Step Test** — numbered steps to perform the smoke test
- [ ] Section: **Expected Results** — what should happen at each step
- [ ] Section: **Verification** — how to verify the file was written to cloud storage (Railway logs, storage inspection, etc.)
- [ ] Section: **Troubleshooting** — common issues and how to debug them
- [ ] Section: **Success Criteria** — checklist of what indicates the smoke test passed

## Test Requirements
- [ ] Documentation is clear, concise, and actionable
- [ ] Steps are numbered and sequential
- [ ] Expected results are specific (not vague like "it should work")
- [ ] Includes commands for checking Railway storage (if accessible)
- [ ] Includes JWT token generation instructions (or placeholder for where to get one)
- [ ] Assumes reader has basic knowledge of browser dev tools but explains terminal/network inspection

## Documentation Structure

```markdown
# Cloud Storage Adapter — Manual Smoke Test

## Objective
Verify that chat conversations saved in the browser are persisted to Railway cloud storage and restored on page refresh.

## Prerequisites
- [ ] Railway hivenode deployed and running (SPEC-3000 complete)
- [ ] Railway hivenode URL known (e.g., https://shiftcenter-hivenode.up.railway.app)
- [ ] Valid JWT token from ra96it.com (or test token)
- [ ] Browser dev server running (npm run dev)
- [ ] Browser configured to use cloud hivenode (check .env or config)

## Step-by-Step Test

### Step 1: Open the Browser App
1. Navigate to http://localhost:5173 (or your dev server port)
2. Open browser dev tools (F12)
3. Go to Network tab, filter for "storage"

### Step 2: Start a Chat Conversation
1. Open a terminal pane (or chat pane)
2. Type a message: "Test message for cloud storage smoke test"
3. Send the message
4. Type a second message: "This should persist to Railway cloud"
5. Send the message

### Step 3: Verify Save Request
1. In Network tab, verify you see a POST request to /storage/write
2. Check request payload contains:
   - `uri: "cloud://conversations/[conversation-id].json"`
   - `content_base64: [base64 encoded conversation data]`
3. Check response status is 200 OK
4. Check response body contains: `{"ok": true, "uri": "cloud://..."}`

### Step 4: Refresh the Page
1. Hard refresh the browser (Ctrl+F5 or Cmd+Shift+R)
2. Wait for page to fully load
3. Verify terminal/chat pane is visible

### Step 5: Verify Load Request
1. In Network tab, verify you see a GET request to /storage/read
2. Check request params contain: `uri=cloud://conversations/[conversation-id].json`
3. Check response status is 200 OK
4. Check response body contains the conversation data

### Step 6: Verify Chat Messages
1. In the terminal/chat pane, verify both messages are present:
   - "Test message for cloud storage smoke test"
   - "This should persist to Railway cloud"
2. Verify message order is correct
3. Verify timestamps are preserved

## Expected Results
- ✅ POST /storage/write returns 200 OK
- ✅ File is written to cloud://conversations/[id].json
- ✅ GET /storage/read on page refresh returns 200 OK
- ✅ Chat messages are restored in correct order
- ✅ No console errors in browser dev tools

## Verification (Optional)
If you have access to Railway storage:
1. SSH into Railway container (if allowed)
2. Navigate to persistent volume mount (check Railway env vars)
3. Verify file exists at: `[volume]/conversations/[id].json`
4. Verify file content is valid JSON with expected messages

Or use Railway logs:
1. Open Railway project logs
2. Filter for "POST /storage/write"
3. Verify log entry shows successful write

## Troubleshooting

### No POST /storage/write request
- Check browser config — is it pointing to cloud hivenode URL?
- Check localStorage settings — is cloud storage enabled?
- Check terminal persistence config — is `persistConversations: true`?

### 401 Unauthorized on /storage/write
- JWT token missing or expired
- Check browser localStorage for `auth_token`
- Generate new JWT from ra96it.com

### 404 File Not Found on /storage/read
- Conversation file not written yet
- Check conversation ID matches between write and read
- Verify file was written to correct volume (cloud:// not local://)

### 503 Service Unavailable
- Cloud hivenode is down
- Check Railway deployment status
- Check network connectivity

### Messages don't restore on refresh
- Check /storage/read request was made
- Check response data is valid JSON
- Check browser console for parsing errors
- Verify conversation ID persistence across sessions

## Success Criteria
- [ ] Chat messages saved to cloud storage on send
- [ ] Cloud storage returns 200 OK for write
- [ ] Page refresh loads chat from cloud storage
- [ ] Cloud storage returns 200 OK for read
- [ ] All messages restored in correct order
- [ ] No errors in browser console
- [ ] No errors in Railway logs (if accessible)
```

## Constraints
- Documentation file under 300 lines
- All file paths absolute (Windows format in task docs, generic in smoke test doc)
- Clear, actionable language (imperative mood: "Open browser", not "The user should open browser")
- Includes specific Network tab inspection steps
- Includes specific console error checks
- Includes Railway verification steps (optional, for those with access)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-209-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — N/A (this is a documentation task, but state "Documentation reviewed for clarity")
5. **Build Verification** — N/A (state "Documentation task, no build required")
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — any gaps in documentation, follow-up tasks

DO NOT skip any section.

## Acceptance Criteria
- [ ] Documentation file created: `docs/smoke-tests/CLOUD-STORAGE-SMOKE-TEST.md`
- [ ] Prerequisites section lists all requirements
- [ ] Step-by-step test section has clear numbered steps
- [ ] Expected results section specifies exact outcomes
- [ ] Verification section includes Railway storage inspection (optional)
- [ ] Troubleshooting section covers common failure scenarios
- [ ] Success criteria checklist included
- [ ] Documentation is clear and actionable
- [ ] File under 300 lines

## Notes
- This is a **documentation task**, not a coding task. No code changes required.
- The smoke test is **manual** — it's performed by a human, not automated.
- The goal is to give Q88N (Dave) or any developer a clear checklist for verifying cloud storage works end-to-end from the browser.
- If chat persistence is not yet wired to cloud storage in the browser, note this in the "Issues / Follow-ups" section of the response file. The documentation should describe the **intended behavior** based on the architecture.
- Include placeholder sections for features not yet implemented (e.g., "Once chat persistence is wired to cloud storage, you will see...").
