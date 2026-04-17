# SPEC-EFEMERA-CONN-11: Port Moderation Pipeline

> **Project:** Efemera Connector (12 specs submitted as batch, 2026-03-28)
> Dependencies between specs ensure correct execution order.
> Design doc: `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md`

## Priority
P1

## Depends On
- SPEC-EFEMERA-CONN-07-backend-schema
- SPEC-EFEMERA-CONN-09-rbac-system-channels (logger writes to moderation-log and bugs-admin channels)

## Model Assignment
sonnet

## Objective

Port the TASaaS content safety pipeline and moderation queue from platform to hivenode. This provides PII detection, content classification, crisis detection, and a moderation review workflow. Moderation logger writes to system channels created by CONN-09.

## Read First

- `.deia/BOOT.md` — hard rules
- Platform source:
  - `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\tasaas\pipeline.py` (130 lines)
  - `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\moderation\routes.py` (161 lines)
  - `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\moderation\logger.py` (73 lines)
- `hivenode/efemera/store.py` — messages table has moderation_status field (from CONN-07)
- `.deia/hive/responses/20260328-EFEMERA-ASSESSMENT.md` — sections 1.5, 1.6

## Files to Create

### 1. `hivenode/efemera/moderation/__init__.py`
Empty init.

### 2. `hivenode/efemera/moderation/pipeline.py` (~130 lines)
Port from platform's `tasaas/pipeline.py`. Sequential scanner pipeline.

```python
class Decision(str, Enum):
    PASS = "pass"
    FLAG = "flag"
    BLOCK = "block"

@dataclass
class ScanResult:
    decision: Decision
    reason: Optional[str] = None
    scanner: Optional[str] = None
    details: Optional[dict] = None

PII_PATTERNS = {
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "phone": r'\b(?:\+?1[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b',
    "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
    "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
}

def scan_pii(content: str) -> ScanResult: ...
def scan_toxicity(content: str) -> ScanResult: ...
def scan_crisis(content: str) -> ScanResult: ...

def run_pipeline(content: str) -> ScanResult:
    """Run all scanners. Priority: BLOCK > FLAG > PASS."""
```

### 3. `hivenode/efemera/moderation/routes.py` (~160 lines)
Moderation queue management endpoints.

### 4. `hivenode/efemera/moderation/logger.py` (~70 lines)
Logs moderation events to system channels (moderation-log and bugs-admin — created by CONN-09).

### Integration with create_message

Add moderation pipeline intercept to `routes.py` `create_message` endpoint:
```python
scan = run_pipeline(req.content)
moderation_status = "approved"
if scan.decision == Decision.BLOCK:
    moderation_status = "blocked"
elif scan.decision == Decision.FLAG:
    moderation_status = "held"
```

## Acceptance Criteria
- [ ] PII scanner detects email, phone, SSN, credit card
- [ ] PII scanner: clean text passes
- [ ] Toxicity scanner detects toxic keywords
- [ ] Crisis scanner detects crisis keywords, returns BLOCK
- [ ] Pipeline priority: BLOCK > FLAG > PASS
- [ ] Pipeline: crisis content returns BLOCK
- [ ] Pipeline: PII content returns FLAG
- [ ] Pipeline: clean content returns PASS
- [ ] create_message: flagged content gets moderation_status=held
- [ ] create_message: blocked content gets moderation_status=blocked
- [ ] create_message: clean content gets moderation_status=approved
- [ ] Moderation queue lists held messages
- [ ] Review: approve changes status to approved
- [ ] Review: reject changes status to blocked
- [ ] Resubmit: re-runs pipeline
- [ ] Logger: moderation event logged to moderation-log channel
- [ ] Logger: error logged to bugs-admin channel
- [ ] All tests pass

## Smoke Test
- [ ] `cd hivenode && python -m pytest tests/hivenode/test_efemera_moderation.py -v` — all pass
- [ ] `cd hivenode && python -m pytest tests/ -v` — no regressions

## Constraints
- Port from platform code — adapt to our SQLite store pattern
- Pipeline runs synchronously (no async LLM calls — regex/keyword matching)
- Moderation is opt-in: if pipeline module is not importable, messages pass through unmoderated
- Moderation log channels must exist (created by CONN-09 system channel seeding)
- No file exceeds 500 lines
- TDD: write tests first

## Response File
20260328-EFEMERA-CONN-11-RESPONSE.md
