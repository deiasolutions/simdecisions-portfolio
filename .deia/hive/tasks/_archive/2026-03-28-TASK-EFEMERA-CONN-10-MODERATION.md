# TASK-EFEMERA-CONN-10: Port Moderation Pipeline

## Objective
Port the TASaaS content safety pipeline and moderation queue API from platform. After this task, messages pass through PII/toxicity/crisis scanning, and moderators can review held/blocked content.

## Context
Platform moderation has three components:
1. **TASaaS pipeline** (`tasaas/pipeline.py`): Sequential scanner — PII detection → content classification → crisis detection. Three decisions: pass (deliver), flag (hold), block (reject).
2. **Moderation logger** (`moderation/logger.py`): Logs moderation events to system channels.
3. **Moderation routes** (`moderation/routes.py`): Queue listing, review (approve/reject), resubmit, withdraw.

ShiftCenter has none of this. Messages are delivered unfiltered.

**Depends on:** TASK-EFEMERA-CONN-07 (moderation_status field must exist in schema), TASK-EFEMERA-CONN-08 (system channels for logging).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\tasaas\pipeline.py` (130 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\moderation\logger.py` (73 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\moderation\routes.py` (161 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\store.py` (after CONN-07)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\routes.py` (current routes)

## Deliverables

### 1. Create `hivenode/efemera/moderation/__init__.py`
- [ ] Empty init file for moderation package

### 2. Create `hivenode/efemera/moderation/pipeline.py` (~130 lines)
Port from platform's `tasaas/pipeline.py`:
- [ ] `ScannerResult` dataclass: scanner (str), passed (bool), flags (list), details (dict)
- [ ] `PipelineDecision` dataclass: message_id, decision ('pass'/'flag'/'block'), results (list), redacted_content (optional), reason, timestamp
- [ ] `run_pipeline(text: str, message_id: str | None = None) -> PipelineDecision` function
- [ ] PII scanner: detect emails, phone numbers, SSNs, credit cards via regex. If found: flag + redact.
- [ ] Content classifier: detect toxic/hate keywords. Hate speech: block. Toxic: flag.
- [ ] Crisis detector: detect self-harm/violence indicators. Critical/high: block. Low/medium: flag.
- [ ] Decision priority: crisis block > hate block > flag (any) > pass

### 3. Create `hivenode/efemera/moderation/logger.py` (~70 lines)
Port from platform's `moderation/logger.py`:
- [ ] `log_moderation_event(store, sender_id, channel_id, decision, reason, content_preview="")` — writes a system message to the moderation_log channel
- [ ] `log_error_event(store, error_type, error_message, context="")` — writes to bugs_admin channel
- [ ] Content preview truncated to 100 characters
- [ ] Uses SYSTEM_USER_ID as author

### 4. Create `hivenode/efemera/moderation/routes.py` (~160 lines)
Port from platform's `moderation/routes.py`:
- [ ] `GET /moderation/queue?status_filter=held` — list held/blocked messages (max 100)
- [ ] `POST /moderation/{message_id}/review` — approve or reject (body: action + optional reason)
- [ ] `GET /moderation/log?limit=50` — list all non-approved messages
- [ ] `POST /moderation/{message_id}/resubmit` — re-run pipeline on held message
- [ ] `DELETE /moderation/{message_id}/withdraw` — sender withdraws held message

### 5. Integrate pipeline into message creation
- [ ] Modify the message creation flow in routes.py: run `run_pipeline(content)` before saving
- [ ] If decision='block': return 422 with reason, save message with moderation_status='blocked'
- [ ] If decision='flag': save with moderation_status='held', redacted content if applicable
- [ ] If decision='pass': save with moderation_status='approved'
- [ ] Log all flag/block events via moderation logger

### 6. Register routes
- [ ] Register moderation routes in `hivenode/routes/__init__.py` under `/efemera/moderation`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing efemera tests still pass
- [ ] New test files:
  - `tests/hivenode/test_efemera_pipeline.py` (pipeline unit tests)
  - `tests/hivenode/test_efemera_moderation.py` (moderation API tests)

### Test cases required (30+ tests):
**Pipeline:**
- Clean text passes all scanners
- Email in text: flags PII, redacts
- Phone number: flags PII, redacts
- SSN pattern: flags PII, redacts
- Toxic content: flags
- Hate speech: blocks
- Crisis indicators: blocks (high severity)
- Mixed PII + toxic: flags (not block unless hate/crisis)
- Decision priority: crisis > hate > flag > pass
- Redacted content replaces PII patterns

**Moderation logger:**
- log_moderation_event writes to moderation_log channel
- log_error_event writes to bugs_admin channel
- Content preview truncated at 100 chars

**Moderation routes:**
- Queue returns held messages
- Queue with status_filter='blocked' returns blocked messages
- Queue with status_filter='all' returns all non-approved
- Review approve: status → 'approved'
- Review reject: status → 'rejected'
- Review 404 for non-existent message
- Review 400 for already-approved message
- Resubmit re-runs pipeline on held message
- Resubmit blocked again → 422
- Resubmit passes → approved
- Withdraw changes status to 'withdrawn'
- Withdraw 400 if not held

**Integration:**
- Send clean message: approved, visible in list
- Send message with PII: held, NOT visible in list
- Send message with hate speech: blocked, 422 response
- Send message with crisis content: blocked, 422 response
- Moderation event logged on flag/block

## Constraints
- No file over 500 lines
- No stubs
- PII detection uses regex patterns (not external APIs)
- Content classification uses keyword matching (not ML models) — port the exact patterns from platform
- Crisis detection uses keyword matching — port exact patterns
- Do NOT import any external NLP/ML libraries
- Moderation routes under `/efemera/moderation/` prefix

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-EFEMERA-CONN-10-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
