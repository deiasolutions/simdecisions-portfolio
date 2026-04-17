# TASK-110: Indexer Models + Scanner

**Wave:** 1
**Model:** sonnet
**Role:** bee
**Depends on:** None

---

## Objective

Port the indexer data model and file scanner from platform/efemera to hivenode/rag/indexer.

## Source Spec

Port from: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-RAG-001-rag-pipeline-port.md`
Decomposition: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-Q33N-BRIEFING-PORT-RAG-PIPELINE-TASK-DECOMPOSITION.md`

## Files to Create

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\scanner.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_models.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_scanner.py`

## Files to Modify

None

## Deliverables

### models.py (179 lines)
- **Enums:**
  - `class ArtifactType(str, Enum)` — 9 types: CODE, PHASE_IR, ADR, SPEC, DOCUMENT, NOTEBOOK, CONFIG, TEST, OTHER
  - `class StorageTier(str, Enum)` — 4 tiers: HOT, WARM, COLD, ARCHIVE
  - `class IRStatus(str, Enum)` — 4 statuses: VERIFIED, FAILED, UNTESTED, UNKNOWN

- **Pydantic Models:**
  - `class CCCMetadata(BaseModel)` — clock_ms: int, coin_usd: float, carbon_kg: float
  - `class IRPair(BaseModel)` — intent: str, result: str, status: IRStatus, verified_at: Optional[datetime]
  - `class IRSummary(BaseModel)` — verified_count: int, failed_count: int, untested_count: int
  - `class ReliabilityMetrics(BaseModel)` — reliability_score: float (0-1), availability: float (0-1), latency_ms: int, last_updated: datetime
  - `class RelevanceMetrics(BaseModel)` — retrieval_count: int, llm_used: int, llm_ignored: int, helpful_feedback: int, not_helpful_feedback: int
  - `class StalenessInfo(BaseModel)` — indexed_at: datetime, modified_at: datetime, days_stale: int
  - `class ProvenanceInfo(BaseModel)` — source: str, actor_id: str, node_id: str, indexed_by: str
  - `class EmbeddingRecord(BaseModel)` — artifact_id: str, engine: str, vector: list[float], dimension: int, created_at: datetime
  - `class IndexRecord(BaseModel)` — artifact_id: str (UUID), path: str, artifact_type: ArtifactType, storage_tier: StorageTier, keywords: list[str], content_hash: str, engines: list[str], ir_summary: IRSummary, ccc: CCCMetadata, reliability: ReliabilityMetrics, relevance: RelevanceMetrics, staleness: StalenessInfo, provenance: ProvenanceInfo, created_at: datetime, updated_at: datetime

### scanner.py (164 lines)
- **Function:** `scan(repo_path: Path, skip_dirs: Optional[set[str]] = None) -> Iterator[tuple[Path, ArtifactType]]`
  - Recursively walks `repo_path`
  - Skips 12 directories (default): `node_modules`, `.git`, `__pycache__`, `venv`, `.venv`, `dist`, `build`, `.next`, `.turbo`, `coverage`, `.pytest_cache`, `.mypy_cache`
  - Yields `(file_path, artifact_type)` for each file
  - File type detection logic:
    - `_is_phase_ir_file(path)` — JSON with keys: `"meta"`, `"nodes"`, `"edges"`, `"version"`
    - ADR: files in `docs/adr/` or `decisions/` matching `*-adr-*.md` or `ADR-*.md`
    - SPEC: files in `docs/specs/` matching `SPEC-*.md`
    - CODE: `.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.go`, `.rs`, `.java`, `.c`, `.cpp`, `.h`, `.hpp`
    - TEST: filenames starting with `test_` or ending with `.test.{py,js,ts,tsx}`
    - NOTEBOOK: `.ipynb`
    - CONFIG: `.json`, `.yaml`, `.yml`, `.toml`, `.ini`, `.env`, `.cfg`
    - DOCUMENT: `.md`, `.txt`, `.rst`, `.adoc`
    - OTHER: everything else

- **Helper:** `_is_phase_ir_file(file_path: Path) -> bool`
  - Read JSON
  - Check for required keys: `meta`, `nodes`, `edges`, `version`
  - Return True if all present, False otherwise

- **Constants:**
  - `DEFAULT_SKIP_DIRS: set[str]` — the 12 directories to skip

### __init__.py
- Export all models and scanner function
- `__all__ = ["ArtifactType", "StorageTier", "IRStatus", "CCCMetadata", "IRPair", "IRSummary", "ReliabilityMetrics", "RelevanceMetrics", "StalenessInfo", "ProvenanceInfo", "EmbeddingRecord", "IndexRecord", "scan"]`

## Tests

### test_models.py (8+ tests)
- Test all enum values are valid
- Test IndexRecord creation with all fields
- Test Pydantic validation (missing required fields, invalid types)
- Test datetime serialization/deserialization
- Test IRSummary counts
- Test CCCMetadata numeric values
- Test EmbeddingRecord vector dimension validation

### test_scanner.py (7+ tests)
- Test scanning empty directory
- Test scanning directory with all artifact types (9 test files, 1 per type)
- Test PHASE-IR detection (valid PHASE-IR JSON vs regular JSON)
- Test ADR detection (path + filename pattern)
- Test SPEC detection (path + filename pattern)
- Test skip directories (verify `node_modules`, `.git`, etc. are skipped)
- Test TEST file detection (both `test_*.py` and `*.test.ts` patterns)
- Test recursive directory walking

## Acceptance Criteria

- [ ] All listed files created
- [ ] All tests pass (`python -m pytest tests/hivenode/rag/indexer/ -v`)
- [ ] No file exceeds 500 lines
- [ ] PORT not rewrite — same data model, same skip list, same artifact types as platform/efemera
- [ ] TDD: tests written first
- [ ] 15+ tests total covering all artifact types, skip logic, PHASE-IR detection

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-110-RESPONSE.md`

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
