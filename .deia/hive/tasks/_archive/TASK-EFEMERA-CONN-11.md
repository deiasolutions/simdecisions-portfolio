# TASK-EFEMERA-CONN-11: Port Moderation Pipeline

**Priority:** P1
**Depends on:** CONN-07, CONN-09
**Blocks:** CONN-12
**Model:** Sonnet
**Role:** Bee

## Objective

Port the TASaaS content safety pipeline and moderation queue from platform to hivenode. This provides PII detection, content classification, crisis detection, and a moderation review workflow.

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
"""TASaaS content safety pipeline — PII, toxicity, crisis detection."""
import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

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

# PII patterns
PII_PATTERNS = {
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "phone": r'\b(?:\+?1[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b',
    "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
    "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
}

# Toxic keyword patterns (simplified — platform used ML, we use keyword matching)
TOXIC_PATTERNS = [...]  # port from platform
CRISIS_PATTERNS = [...]  # port from platform

def scan_pii(content: str) -> ScanResult: ...
def scan_toxicity(content: str) -> ScanResult: ...
def scan_crisis(content: str) -> ScanResult: ...

def run_pipeline(content: str) -> ScanResult:
    """Run all scanners. Returns the highest-severity result.
    Priority: crisis/hate=BLOCK, toxic+PII=FLAG, PII-only=FLAG, clean=PASS.
    """
    results: List[ScanResult] = []
    results.append(scan_pii(content))
    results.append(scan_toxicity(content))
    results.append(scan_crisis(content))

    # Highest severity wins
    for r in results:
        if r.decision == Decision.BLOCK:
            return r
    for r in results:
        if r.decision == Decision.FLAG:
            return r
    return ScanResult(decision=Decision.PASS)
```

### 3. `hivenode/efemera/moderation/routes.py` (~160 lines)

Port from platform's `moderation/routes.py`. Moderation queue management.

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/moderation")

class ReviewRequest(BaseModel):
    action: str = Field(..., pattern="^(approve|reject)$")
    reviewer_id: str = Field(default="local-user")
    reason: Optional[str] = None

@router.get("/queue")
async def list_moderation_queue(status: str = "held"):
    """List messages in moderation queue (held or blocked)."""
    store = _get_store()
    # Query messages WHERE moderation_status = status
    ...

@router.post("/messages/{message_id}/review")
async def review_message(message_id: str, req: ReviewRequest):
    """Approve or reject a held/blocked message."""
    store = _get_store()
    # Update moderation_status
    ...

@router.post("/messages/{message_id}/resubmit")
async def resubmit_message(message_id: str):
    """Resubmit a blocked message through the pipeline again."""
    store = _get_store()
    # Re-run pipeline, update status
    ...

@router.delete("/messages/{message_id}")
async def withdraw_message(message_id: str, req: WithdrawRequest):
    """Sender withdraws their own held message."""
    ...
```

### 4. `hivenode/efemera/moderation/logger.py` (~70 lines)

Port from platform's `moderation/logger.py`. Logs moderation events to system channels.

```python
def log_moderation_event(store, action: str, message_id: str, reviewer_id: str, reason: str = "") -> None:
    """Log a moderation action to the moderation_log channel."""
    store.create_message(
        channel_id="moderation-log",
        author_id="system",
        author_name="Moderation",
        content=f"[{action.upper()}] Message {message_id} by {reviewer_id}. {reason}",
        author_type="system",
        message_type="system",
    )

def log_moderation_error(store, error: str) -> None:
    """Log a moderation error to the bugs_admin channel."""
    store.create_message(
        channel_id="bugs-admin",
        author_id="system",
        author_name="Moderation",
        content=f"[ERROR] {error}",
        author_type="system",
        message_type="system",
    )
```

### Integration with Message Creation

**Update `routes.py` `create_message` endpoint:**

```python
from hivenode.efemera.moderation.pipeline import run_pipeline, Decision

@router.post("/channels/{channel_id}/messages", status_code=201)
async def create_message(channel_id: str, req: CreateMessageRequest):
    store = _get_store()
    # Run moderation pipeline
    scan = run_pipeline(req.content)
    moderation_status = "approved"
    moderation_reason = None
    if scan.decision == Decision.BLOCK:
        moderation_status = "blocked"
        moderation_reason = scan.reason
    elif scan.decision == Decision.FLAG:
        moderation_status = "held"
        moderation_reason = scan.reason

    msg = store.create_message(
        channel_id=channel_id,
        author_id=req.author_id,
        author_name=req.author_name,
        content=req.content,
        moderation_status=moderation_status,
        moderation_reason=moderation_reason,
    )

    if moderation_status != "approved":
        from hivenode.efemera.moderation.logger import log_moderation_event
        log_moderation_event(store, moderation_status, msg["id"], "pipeline", scan.reason or "")

    return msg
```

**Register moderation routes** in `hivenode/routes/__init__.py` or in the efemera router.

## Tests to Create

### `tests/hivenode/test_efemera_moderation.py`
- PII scanner: detects email, phone, SSN, credit card
- PII scanner: clean text passes
- Toxicity scanner: detects toxic keywords
- Crisis scanner: detects crisis keywords, returns BLOCK
- Pipeline priority: BLOCK > FLAG > PASS
- Pipeline: crisis content returns BLOCK
- Pipeline: PII content returns FLAG
- Pipeline: clean content returns PASS
- create_message: flagged content gets moderation_status=held
- create_message: blocked content gets moderation_status=blocked
- create_message: clean content gets moderation_status=approved
- Moderation queue: lists held messages
- Review: approve changes status to approved
- Review: reject changes status to blocked
- Resubmit: re-runs pipeline
- Logger: moderation event logged to moderation-log channel
- Logger: error logged to bugs-admin channel

## Constraints

- Port from platform code — adapt to our SQLite store pattern
- Pipeline runs synchronously (no async LLM calls — this is regex/keyword matching)
- Moderation is opt-in: if pipeline module is not importable, messages pass through unmoderated
- Moderation log channels must exist (created by CONN-09 system channel seeding)
- No file exceeds 500 lines
- TDD: write tests first
