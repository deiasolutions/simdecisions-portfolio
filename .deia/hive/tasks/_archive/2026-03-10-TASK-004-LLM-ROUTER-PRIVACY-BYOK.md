# TASK-004: LLM Router + Privacy Port + Sensitivity Gate + BYOK

## Objective

Two-phase task: (1) port the privacy module from the old SimDecisions repo, (2) build the LLM router with sensitivity gate and BYOK key storage on top. The router is what makes the AI Chat App work — it takes a prompt, decides if it's sensitive, and routes to the right LLM.

## Dependencies

- **TASK-001 (Event Ledger)** must be complete. Every routing decision emits to the Event Ledger.

## Phase 1: Port Privacy Module

Copy `hivenode/privacy/` from the old repo. These files are already modular with relative imports — no `simdecisions.*` imports to fix. Port all 8 files:

| File | Lines | Key Classes | Notes |
|------|-------|-------------|-------|
| `__init__.py` | 34 | exports | Just re-exports |
| `hasher.py` | 50 | `DocumentHasher` | SHA-256 hashing, hash chains |
| `redactor.py` | 130 | `PIIRedactor`, `PIIMatch` | Regex PII detection — **the sensitivity gate uses this** |
| `purger.py` | 78 | `SecurePurger` | Secure text/file deletion |
| `audit_trail.py` | 192 | `AuditTrail`, `AuditEvent` | Hash-chained audit log |
| `consent.py` | 124 | `ConsentManager`, `ConsentToken` | Consent token management |
| `training_store.py` | 116 | `TrainingStore`, `TrainingSample` | Anonymized embedding storage |
| `pipeline.py` | 281 | `PrivacyPipeline`, `EmbeddingService` | Full pipeline orchestrator |

**Source location:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\src\simdecisions\privacy\`

**Port rules:**
- All internal imports are already relative (`.hasher`, `.redactor`, etc.) — no changes needed
- `pipeline.py` has optional `voyageai` and `anthropic` imports — keep them as optional (conditional import with fallback to hash embeddings)
- Do NOT add voyageai or anthropic to pyproject.toml — they are optional runtime deps

**Port tests too.** Existing tests from old repo (copy and adapt path):

| Test File | Lines | Coverage |
|-----------|-------|----------|
| `test_redactor.py` | 330 | All PII types + edge cases |
| `test_audit_trail.py` | 354 | Hash chains, integrity, reports |
| `test_consent.py` | 304 | Grant/revoke/verify, edge cases |
| `test_pipeline.py` | 367 | Full flow, privacy guarantees |

**Source location for tests:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\tests\privacy\`

**Write NEW tests for files missing coverage:**
- `test_hasher.py` — hash_document, hash_chain, verify_hash (string + bytes)
- `test_purger.py` — purge_text, purge_file, purge_multiple
- `test_training_store.py` — add_sample, get_sample, get_all, batch retrieval, deterministic IDs

**Import path adjustments for ported tests:** The old tests import from `simdecisions.privacy.*` — change to `hivenode.privacy.*`. Example:
```python
# Old: from simdecisions.privacy.redactor import PIIRedactor
# New: from hivenode.privacy.redactor import PIIRedactor
```

## Phase 2: Build LLM Router

### Architecture

```
User Prompt → Sensitivity Gate → Router Decision → LLM Call → Response
                    ↓                    ↓
              PIIRedactor          Event Ledger
              (from Phase 1)       (routing event)
```

### 2A. Sensitivity Gate (`hivenode/llm/sensitivity.py`)

Layer 1 only (regex-based). Uses `PIIRedactor` from the ported privacy module.

```python
class SensitivityGate:
    """Classifies prompts as sensitive or clean using regex PII detection."""

    def classify(self, text: str) -> SensitivityResult:
        """
        Scan text for PII patterns.

        Returns:
            SensitivityResult with:
                - is_sensitive: bool
                - score: float (0.0 = clean, 1.0 = highly sensitive)
                - detections: list of PIIMatch objects
                - categories: set of detected PII types (EMAIL, SSN, etc.)
        """
```

**Scoring logic:**
- 0 detections → score 0.0, not sensitive
- 1+ detections → sensitive, score based on severity:
  - SSN, MONEY: weight 1.0 (financial/identity)
  - PHONE, ADDRESS: weight 0.7 (personal)
  - EMAIL, PERSON: weight 0.5 (contact info)
- Score = min(1.0, sum of weights / 3.0)

**The gate does NOT modify the prompt.** It classifies only. Redaction is a future layer.

### 2B. LLM Router (`hivenode/llm/router.py`)

Routes prompts to the right LLM based on sensitivity classification.

```python
class LLMRouter:
    """Routes prompts to appropriate LLM based on sensitivity and user config."""

    def __init__(self, ledger_writer, byok_store, config):
        ...

    def route(self, prompt: str, user_id: str, actor: str,
              system: str = "", preferred_provider: str = None,
              preferred_model: str = None, **kwargs) -> RouteResult:
        """
        Route a prompt to the appropriate LLM.

        Flow:
        1. Run sensitivity gate
        2. If sensitive → route to local (Ollama)
        3. If clean → route to preferred provider or default cloud
        4. Look up BYOK key for the chosen provider
        5. Call the LLM via adapter
        6. Emit routing decision to Event Ledger
        7. Return response + routing metadata

        Returns:
            RouteResult with:
                - response: str (LLM response)
                - provider: str (which provider was used)
                - model: str (which model was used)
                - sensitivity: SensitivityResult
                - routed_local: bool (was it routed locally due to sensitivity?)
                - cost_usd: float
                - cost_carbon: float
        """
```

**Routing rules:**
- Sensitive prompt → always Ollama (local, no data leaves machine)
- Clean prompt + user has BYOK key for preferred provider → use that provider
- Clean prompt + no BYOK key → use default provider from config
- Ollama unavailable + sensitive → raise `SensitiveContentError` (do NOT fall back to cloud)
- Cloud unavailable + clean → fall back to Ollama if available

**Supported providers** (using adapters already in `hivenode/adapters/`):
- `anthropic` — AnthropicAdapter
- `openai` — OpenAIAdapter
- `gemini` — GeminiAdapter
- `ollama` — OllamaAdapter (always local, always safe for sensitive)

### 2C. BYOK Key Storage (`hivenode/llm/byok.py`)

Users store their own API keys for cloud providers. Keys encrypted at rest.

```python
class BYOKStore:
    """Encrypted storage for user-provided API keys."""

    def __init__(self, db_path: str, encryption_key: str):
        """
        Args:
            db_path: SQLite database path
            encryption_key: Fernet encryption key (from config)
        """

    def store_key(self, user_id: str, provider: str, api_key: str) -> None:
        """Store encrypted API key for a provider."""

    def get_key(self, user_id: str, provider: str) -> str | None:
        """Retrieve and decrypt API key. Returns None if not stored."""

    def list_keys(self, user_id: str) -> list[dict]:
        """List stored keys metadata (provider, created_at, last_used). No raw keys."""

    def delete_key(self, user_id: str, provider: str) -> bool:
        """Delete stored key. Returns True if existed."""

    def update_last_used(self, user_id: str, provider: str) -> None:
        """Update last_used timestamp after successful API call."""
```

**Database schema:**
```sql
CREATE TABLE byok_keys (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     TEXT NOT NULL,
    provider    TEXT NOT NULL CHECK(provider IN ('anthropic','openai','gemini')),
    encrypted_key TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f','now')),
    last_used   TEXT,
    UNIQUE(user_id, provider)
);
```

**Encryption:** Use `cryptography.fernet.Fernet` (already a dependency via pyjwt[crypto]).

**Reference file:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\src\simdecisions\auth\api_keys-1.py` — read this for the bcrypt key storage pattern. Adapt the pattern: instead of bcrypt hashing (one-way), use Fernet encryption (reversible, since we need to decrypt keys for API calls).

### 2D. Router Config (`hivenode/llm/config.py`)

```python
@dataclass
class RouterConfig:
    """LLM Router configuration."""
    default_provider: str = "anthropic"
    default_model: str = "claude-sonnet-4-5-20250929"
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    fernet_key: str = ""  # BYOK encryption key
    providers: dict = field(default_factory=lambda: {
        "anthropic": {"models": ["claude-opus-4-6", "claude-sonnet-4-5-20250929", "claude-haiku-4-5-20251001"]},
        "openai": {"models": ["gpt-4o", "gpt-4o-mini"]},
        "gemini": {"models": ["gemini-2.0-flash"]},
        "ollama": {"models": ["llama3.2", "mistral", "codellama"]},
    })
```

### Event Ledger Integration

Every routing decision emits to the Event Ledger:

| event_type | actor | target | payload |
|------------|-------|--------|---------|
| `llm.route` | caller actor | `llm:{provider}:{model}` | `{sensitive: bool, score: float, categories: [...], cost_usd, cost_carbon}` |
| `llm.route.blocked` | caller actor | `llm:none` | `{reason: "sensitive_no_local", categories: [...]}` |

All events use `domain: "llm"`, `signal_type: "internal"`.

## File Structure

```
hivenode/privacy/                  -- Phase 1: Ported
├── __init__.py
├── hasher.py
├── redactor.py
├── purger.py
├── audit_trail.py
├── consent.py
├── training_store.py
└── pipeline.py

hivenode/llm/                      -- Phase 2: New build
├── __init__.py
├── sensitivity.py
├── router.py
├── byok.py
└── config.py
```

```
tests/hivenode/privacy/            -- Phase 1: Ported + new
├── __init__.py
├── conftest.py
├── test_redactor.py               -- Ported (fix imports)
├── test_audit_trail.py            -- Ported (fix imports)
├── test_consent.py                -- Ported (fix imports)
├── test_pipeline.py               -- Ported (fix imports)
├── test_hasher.py                 -- NEW
├── test_purger.py                 -- NEW
├── test_training_store.py         -- NEW

tests/hivenode/llm/                -- Phase 2: All new
├── __init__.py
├── conftest.py
├── test_sensitivity.py
├── test_router.py
├── test_byok.py
├── test_config.py
```

## What NOT to Build

- No FBB PII scanner (layer 2 — future)
- No hash cache for repeated prompts (layer 3 — future)
- No streaming responses (future)
- No FastAPI routes (API layer comes later)
- No frontend code
- No real LLM calls in tests (mock all adapters)
- No quota/rate limiting on routing
- No prompt logging (privacy concern — only log routing decisions, never prompt content)

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Minimum 50 tests across all test files
- [ ] Privacy module ported tests pass unchanged (after import fix)
- [ ] New privacy tests cover hasher, purger, training_store
- [ ] Sensitivity gate tests: clean prompt, email-only, SSN, multi-PII, empty string, score calculation
- [ ] Router tests: clean→cloud, sensitive→local, BYOK key lookup, no BYOK→default, sensitive+no-local→error, cloud-down→fallback, ledger emission
- [ ] BYOK tests: store/get/list/delete, encryption roundtrip, wrong encryption key, duplicate provider, update last_used
- [ ] Edge cases: empty prompt, prompt with only whitespace, very long prompt, Unicode PII, binary content rejected

## Constraints

- Python 3.13
- No file over 500 lines
- No stubs — every function fully implemented (except actual LLM API calls in router which use the existing adapters)
- No external dependencies beyond what's already in pyproject.toml + stdlib
- All timestamps in ISO 8601 UTC
- All entity IDs follow `{type}:{id}` format
- NEVER log prompt content to the Event Ledger — only routing decisions and metadata
- Router tests must mock all adapter `call()` methods — no real API calls

## Files to Read First

- `hivenode/ledger/writer.py` — Event Ledger writer (TASK-001)
- `hivenode/adapters/base.py` — BaseAdapter interface
- `hivenode/adapters/anthropic.py` — AnthropicAdapter (example adapter)
- `hivenode/adapters/ollama.py` — OllamaAdapter (local LLM)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\src\simdecisions\privacy\redactor.py` — PII patterns to port
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\src\simdecisions\auth\api_keys-1.py` — BYOK reference pattern

## Deliverables

### Phase 1: Port
- [ ] `hivenode/privacy/__init__.py`
- [ ] `hivenode/privacy/hasher.py`
- [ ] `hivenode/privacy/redactor.py`
- [ ] `hivenode/privacy/purger.py`
- [ ] `hivenode/privacy/audit_trail.py`
- [ ] `hivenode/privacy/consent.py`
- [ ] `hivenode/privacy/training_store.py`
- [ ] `hivenode/privacy/pipeline.py`
- [ ] `tests/hivenode/privacy/__init__.py`
- [ ] `tests/hivenode/privacy/conftest.py`
- [ ] `tests/hivenode/privacy/test_redactor.py` (ported)
- [ ] `tests/hivenode/privacy/test_audit_trail.py` (ported)
- [ ] `tests/hivenode/privacy/test_consent.py` (ported)
- [ ] `tests/hivenode/privacy/test_pipeline.py` (ported)
- [ ] `tests/hivenode/privacy/test_hasher.py` (new)
- [ ] `tests/hivenode/privacy/test_purger.py` (new)
- [ ] `tests/hivenode/privacy/test_training_store.py` (new)

### Phase 2: Build
- [ ] `hivenode/llm/__init__.py`
- [ ] `hivenode/llm/sensitivity.py`
- [ ] `hivenode/llm/router.py`
- [ ] `hivenode/llm/byok.py`
- [ ] `hivenode/llm/config.py`
- [ ] `tests/hivenode/llm/__init__.py`
- [ ] `tests/hivenode/llm/conftest.py`
- [ ] `tests/hivenode/llm/test_sensitivity.py`
- [ ] `tests/hivenode/llm/test_router.py`
- [ ] `tests/hivenode/llm/test_byok.py`
- [ ] `tests/hivenode/llm/test_config.py`
- [ ] Updated `pyproject.toml` with `hivenode.privacy` and `hivenode.llm` packages

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-004-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full paths
3. **What Was Done** -- bullet list of concrete changes
4. **Test Results** -- test files run, pass/fail counts
5. **Build Verification** -- pytest output summary
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- edge cases, dependencies, recommended next tasks

DO NOT skip any section. A response without all 8 sections is incomplete.
