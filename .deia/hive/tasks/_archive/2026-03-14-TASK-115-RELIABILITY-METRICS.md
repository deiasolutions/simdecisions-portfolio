# TASK-115: Reliability Calculator + Metrics Updater

**Wave:** 3
**Model:** sonnet
**Role:** bee
**Depends on:** TASK-113, TASK-114

---

## Objective

Build reliability scoring system and async event processor that updates index metrics based on Event Ledger feedback (retrieval, verification, human responses).

## Source Spec

Port from: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-RAG-001-rag-pipeline-port.md`
Decomposition: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-Q33N-BRIEFING-PORT-RAG-PIPELINE-TASK-DECOMPOSITION.md`

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (ReliabilityMetrics, RelevanceMetrics)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py` (IndexStorage)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\events\ledger.py` (Event Ledger query interface)

## Files to Create

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\reliability.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\metrics_updater.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_reliability.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_metrics_updater.py`

## Files to Modify

None

## Deliverables

### reliability.py (296 lines)

**Class:** `ReliabilityCalculator`

**Attributes:**
- `storage: IndexStorage` — for reading/writing IndexRecord
- `db_session: Optional[Session]` — for Event Ledger queries (can be None for tests)

**Methods:**

1. **`__init__(storage: IndexStorage, db_session: Optional[Session] = None)`**
   - Store parameters

2. **`calculate_reliability(artifact_id: str) -> float`**
   - Formula: `0.5 × LLM_used_ratio + 0.3 × helpful_ratio + 0.2 × IR_verification_rate`
   - LLM_used_ratio = llm_used / (llm_used + llm_ignored) if total > 0 else 0.5
   - helpful_ratio = helpful_feedback / (helpful_feedback + not_helpful_feedback) if total > 0 else 0.5
   - IR_verification_rate = verified_count / (verified_count + failed_count + untested_count) if total > 0 else 0.0
   - Return float between 0.0 and 1.0

3. **`calculate_availability(artifact_id: str) -> float`**
   - Query Event Ledger for `context.loaded` events for this artifact_id
   - Count success (disposition=ALLOW) vs failures (disposition=DENY)
   - Formula: success_loads / total_loads if total_loads > 0 else 1.0
   - Return float between 0.0 and 1.0

4. **`calculate_latency(artifact_id: str) -> int`**
   - Query Event Ledger for `context.loaded` events (last 100)
   - Extract duration_ms from each event
   - Return average duration_ms as integer

5. **`calculate_cost(artifact_id: str) -> CCCMetadata`**
   - Query Event Ledger for `context.loaded` events
   - Sum clock_ms, coin_usd, carbon_kg from all events
   - Return CCCMetadata(clock_ms=total_clock, coin_usd=total_coin, carbon_kg=total_carbon)

6. **`is_canon(artifact_id: str) -> bool`**
   - Retrieve IndexRecord from storage
   - Canon criteria:
     - retrieval_count > 1000 AND
     - reliability_score > 0.90 AND
     - IR_verification_rate > 0.80
   - Return True if all criteria met, else False

7. **`update_reliability_metrics(artifact_id: str) -> ReliabilityMetrics`**
   - Call all calculation methods:
     - reliability_score = `calculate_reliability(artifact_id)`
     - availability = `calculate_availability(artifact_id)`
     - latency_ms = `calculate_latency(artifact_id)`
   - Create new ReliabilityMetrics(reliability_score, availability, latency_ms, last_updated=now)
   - Fetch IndexRecord from storage
   - Update record.reliability = new metrics
   - Call `storage.update(record)` to persist
   - Return new ReliabilityMetrics

### test_reliability.py (8+ tests)

**Test cases:**
- Test `calculate_reliability()` with known inputs (0.5 LLM, 0.3 helpful, 0.2 IR)
- Test `calculate_reliability()` with zero feedback → returns 0.5 (default)
- Test `calculate_availability()` with 8 success, 2 failures → 0.8
- Test `calculate_availability()` with zero loads → 1.0 (default)
- Test `calculate_latency()` with known durations → returns average
- Test `calculate_cost()` sums CCC from events correctly
- Test `is_canon()` returns True for high-traffic high-reliability artifact
- Test `is_canon()` returns False for low retrieval_count
- Test `update_reliability_metrics()` persists to storage

---

### metrics_updater.py (355 lines)

**Class:** `MetricsUpdater`

**Attributes:**
- `db_session: Session` — SQLAlchemy session for Event Ledger
- `index_storage: IndexStorage` — for updating IndexRecord metrics
- `poll_interval_seconds: int` — default 60
- `running: bool` — daemon state
- `last_processed_event_id: Optional[str]` — cursor for incremental event polling

**Methods:**

1. **`__init__(db_session: Session, index_storage: IndexStorage, poll_interval_seconds: int = 60)`**
   - Store parameters
   - running = False
   - last_processed_event_id = None

2. **`start() -> None`**
   - Set running = True
   - Spawn async event processing loop
   - Use `asyncio.create_task(_poll_loop())` or threading.Thread

3. **`stop() -> None`**
   - Set running = False
   - Graceful shutdown (finish current batch, then exit)

4. **`_poll_loop() -> None`**
   - While running:
     - Call `_process_new_events()`
     - Sleep for poll_interval_seconds
     - Repeat

5. **`_process_new_events() -> int`**
   - Query Event Ledger for events AFTER last_processed_event_id
   - Filter by event_type IN: `context.loaded`, `ir_pair.verified`, `ir_pair.failed`, `human.responded`, `context.indexed`
   - For each event: route to handler based on event_type
   - Update last_processed_event_id to last event processed
   - Return count of events processed

6. **`_handle_context_loaded(event: dict) -> None`**
   - Extract artifact_id from event.data
   - Fetch IndexRecord from storage
   - Increment relevance.retrieval_count += 1
   - If event.data.llm_used == True: increment relevance.llm_used += 1
   - Else: increment relevance.llm_ignored += 1
   - Update staleness.days_stale = (now - indexed_at).days
   - Call `storage.update(record)`

7. **`_handle_ir_pair_verified(event: dict) -> None`**
   - Extract artifact_id from event.data
   - Call `_recalculate_ir_summary(artifact_id, verified_delta=+1)`

8. **`_handle_ir_pair_failed(event: dict) -> None`**
   - Extract artifact_id from event.data
   - Call `_recalculate_ir_summary(artifact_id, failed_delta=+1)`

9. **`_handle_human_responded(event: dict) -> None`**
   - Extract artifact_id from event.data
   - Extract feedback from event.data.feedback ("helpful" or "not_helpful")
   - Fetch IndexRecord from storage
   - If feedback == "helpful": increment relevance.helpful_feedback += 1
   - Else: increment relevance.not_helpful_feedback += 1
   - Call `storage.update(record)`

10. **`_recalculate_ir_summary(artifact_id: str, verified_delta: int = 0, failed_delta: int = 0) -> None`**
    - Fetch IndexRecord from storage
    - Get all chunks: `storage.get_chunks(artifact_id)`
    - Flatten all ir_pairs from chunks
    - Recount by status: verified_count, failed_count, untested_count
    - Apply deltas: verified_count += verified_delta, failed_count += failed_delta
    - Update record.ir_summary = new IRSummary
    - Call `storage.update(record)`

### test_metrics_updater.py (10+ tests)

**Test cases (use mock events):**
- Test `_handle_context_loaded()` increments retrieval_count
- Test `_handle_context_loaded()` increments llm_used when event.data.llm_used=True
- Test `_handle_context_loaded()` increments llm_ignored when event.data.llm_used=False
- Test `_handle_context_loaded()` updates staleness.days_stale
- Test `_handle_ir_pair_verified()` increments verified_count
- Test `_handle_ir_pair_failed()` increments failed_count
- Test `_handle_human_responded()` increments helpful_feedback
- Test `_handle_human_responded()` increments not_helpful_feedback
- Test `_recalculate_ir_summary()` recounts IR pairs from chunks
- Test `_process_new_events()` routes events to correct handlers
- Test poll loop runs and processes events (use mock sleep + short interval)

## Acceptance Criteria

- [ ] All listed files created
- [ ] All tests pass (`python -m pytest tests/hivenode/rag/indexer/test_reliability.py tests/hivenode/rag/indexer/test_metrics_updater.py -v`)
- [ ] No file exceeds 500 lines
- [ ] PORT not rewrite — same reliability formulas (0.5 LLM + 0.3 helpful + 0.2 IR), same event handlers as platform/efemera
- [ ] TDD: tests written first
- [ ] 18+ tests total (8 reliability + 10 metrics_updater)
- [ ] Canon criteria: retrieval_count > 1000, reliability > 0.90, verification_rate > 0.80

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-115-RESPONSE.md`

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
