# SPEC-EFEMERA-CONN-11: Port Moderation Pipeline -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-28

## Files Modified

### Created Files
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\moderation\__init__.py` — module init
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\moderation\pipeline.py` — TASaaS scanner pipeline (174 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\moderation\routes.py` — moderation queue endpoints (166 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\moderation\logger.py` — event logger to system channels (64 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_efemera_moderation.py` — comprehensive tests (329 lines, 30 tests)

### Modified Files
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\routes.py` — integrated pipeline into `create_message` endpoint
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` — registered moderation routes

## What Was Done

### 1. Pipeline Module (pipeline.py)
- Ported from `platform/efemera/src/efemera/tasaas/pipeline.py`
- Three scanners:
  - **PII scanner** — detects email, phone, SSN, credit card via regex → FLAG + redact
  - **Toxicity scanner** — detects harassment, threats via keyword patterns → FLAG
  - **Crisis scanner** — detects suicide risk, violence threats → BLOCK
  - False positive exclusions: "kill the process", "shoot me an email"
- Decision priority: BLOCK > FLAG > PASS
- `run_pipeline(content: str) -> ScanResult` — sequential pipeline execution

### 2. Moderation Routes (routes.py)
- **GET /efemera/moderation/queue** — list held/blocked messages
  - Filter by status: held, blocked, all (default: held)
  - Returns message preview (first 200 chars)
- **POST /efemera/moderation/{id}/review** — approve or reject held message
  - approve → moderation_status=approved
  - reject → moderation_status=blocked
- **POST /efemera/moderation/{id}/resubmit** — re-run pipeline on edited message
  - Still blocked → 422 error
  - Now clean → approved
  - Still flagged → remains held

### 3. Moderation Logger (logger.py)
- `log_moderation_event()` — writes to moderation-log channel
- `log_error_event()` — writes to bugs-admin channel
- Both use system channels created by CONN-09

### 4. Integration with create_message
- Pipeline runs automatically on POST `/efemera/channels/{id}/messages`
- BLOCK decision → returns 422, logs to moderation-log
- FLAG decision → sets moderation_status=held, applies PII redaction, logs
- PASS decision → moderation_status=approved
- Opt-in: if moderation module not importable, messages pass through unmoderated
- Pipeline errors logged to bugs-admin but don't fail message creation

### 5. Test Coverage (30 tests)
- **PII scanner:** 5 tests (email, phone, SSN, credit card, clean)
- **Toxicity scanner:** 3 tests (harassment, threat, clean)
- **Crisis scanner:** 5 tests (suicide, violence, false positives)
- **Pipeline:** 6 tests (clean, PII, toxic, crisis, priority logic)
- **Integration:** 3 tests (clean approved, PII held, crisis blocked)
- **Moderation queue:** 2 tests (list held, default filter)
- **Review endpoint:** 2 tests (approve, reject)
- **Resubmit endpoint:** 1 test (re-run pipeline)
- **Logger:** 2 tests (moderation-log, bugs-admin)

## Test Results

```
$ python -m pytest tests/hivenode/test_efemera_moderation.py -v
========================== 30 passed, 1 warning in 3.65s ==========================
```

All efemera tests (144 tests):
```
$ python -m pytest tests/hivenode/test_efemera*.py -v
========================== 144 passed, 1 warning in 22.63s =========================
```

## Acceptance Criteria

- [x] PII scanner detects email, phone, SSN, credit card
- [x] PII scanner: clean text passes
- [x] Toxicity scanner detects toxic keywords
- [x] Crisis scanner detects crisis keywords, returns BLOCK
- [x] Pipeline priority: BLOCK > FLAG > PASS
- [x] Pipeline: crisis content returns BLOCK
- [x] Pipeline: PII content returns FLAG
- [x] Pipeline: clean content returns PASS
- [x] create_message: flagged content gets moderation_status=held
- [x] create_message: blocked content gets moderation_status=blocked
- [x] create_message: clean content gets moderation_status=approved
- [x] Moderation queue lists held messages
- [x] Review: approve changes status to approved
- [x] Review: reject changes status to blocked
- [x] Resubmit: re-runs pipeline
- [x] Logger: moderation event logged to moderation-log channel
- [x] Logger: error logged to bugs-admin channel
- [x] All tests pass

## Smoke Test

- [x] `cd hivenode && python -m pytest tests/hivenode/test_efemera_moderation.py -v` — all pass
- [x] `cd hivenode && python -m pytest tests/hivenode/test_efemera*.py -v` — no regressions (144 tests pass)

## Implementation Notes

### Adaptation from Platform
- Platform used SQLAlchemy ORM → adapted to SQLite store pattern
- Platform's `get_system_channel_id()` → adapted to `store.get_channel()`
- Platform's Message model → adapted to dict-based message objects
- Platform's DB session commit → adapted to SQLite `conn.commit()`

### Opt-In Design
- Moderation is opt-in: if `hivenode.efemera.moderation.pipeline` import fails, messages pass through unmoderated
- This allows the pipeline to be disabled by simply not installing the module or renaming it

### Error Handling
- Pipeline errors logged to bugs-admin but don't fail message creation
- Logger failures are silent (logged to Python logger but don't raise)
- Blocked content returns 422 (client knows message was rejected)
- Held content returns 201 (message created but not visible)

### Redaction
- PII redaction applied to stored content when FLAG decision
- Original content never stored for PII-flagged messages
- Redaction format: `[REDACTED-EMAIL]`, `[REDACTED-PHONE]`, etc.

### False Positives
- Crisis scanner has exclusion patterns for technical jargon
- "kill the process" → PASS (technical)
- "shoot me an email" → PASS (colloquial)
- "blow up my phone" → PASS (colloquial)

## File Sizes
- `pipeline.py`: 174 lines (under 500 ✓)
- `routes.py`: 166 lines (under 500 ✓)
- `logger.py`: 64 lines (under 500 ✓)
- `test_efemera_moderation.py`: 329 lines (under 500 ✓)

## Dependencies Met
- CONN-07: messages table has `moderation_status` field ✓
- CONN-09: moderation-log and bugs-admin channels exist ✓

## Next Steps
SPEC-EFEMERA-CONN-12 can now proceed (uses moderation pipeline for content filtering).
