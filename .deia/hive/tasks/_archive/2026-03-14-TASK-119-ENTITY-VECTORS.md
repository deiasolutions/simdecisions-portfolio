# TASK-119: Entity Vector System (Alpha, Sigma, Rho, Pi)

**Wave:** 4
**Model:** sonnet
**Role:** bee
**Depends on:** TASK-118

---

## Objective

Build the entity vector calculation system (Alpha autonomy, Sigma quality, Rho reliability, Pi bot/human preference) with 30-day decay windows and confidence weighting. Split into 2 files per Rule 4 (no file over 500 lines).

## Source Spec

Port from: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-RAG-001-rag-pipeline-port.md`
Decomposition: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-Q33N-BRIEFING-PORT-RAG-PIPELINE-TASK-DECOMPOSITION.md`

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\embeddings.py` (bot embedding functions)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\events\ledger.py` (Event Ledger query interface)

## Files to Create

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\vectors_core.py` (data model + helpers, ~350 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\vectors_compute.py` (5 compute functions, ~336 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\entities\test_vectors.py`

## Files to Modify

None

## Deliverables

### vectors_core.py (~350 lines)

**Helper functions:**

1. **`_fetch_events(entity_id: str, event_type: str, db: Session, days: int = 30) -> list[dict]`**
   - Query Event Ledger for events WHERE actor_id = entity_id AND event_type = ? AND timestamp > (now - days)
   - Apply 30-day exponential decay weighting: `weight = exp(-days_ago / 30)`
   - Return list of events with weights attached

2. **`_get_sla_target(domain: str, db: Session) -> int`**
   - Query SLA table for domain (if exists)
   - Return SLA target in milliseconds
   - Fallback: 3,600,000 ms (1 hour) if no SLA defined

3. **`_get_entity_prompt(entity_id: str, db: Session) -> Optional[str]`**
   - Query EntityComponent table for entity_id
   - Return system_prompt field
   - Return None if not found

4. **`_upsert_profile(entity_id: str, domain: str, vector_name: str, value: float, confidence: float, source: str, db: Session) -> None`**
   - Upsert EntityProfile table:
     ```python
     {
       "entity_id": entity_id,
       "domain": domain,
       "vector_name": vector_name,  # "alpha", "sigma", "rho", "pi_bot", "pi_human"
       "value": value,
       "confidence": confidence,
       "source": source,  # "computed", "observed", "declared", "imported"
       "updated_at": now
     }
     ```
   - Use SQLAlchemy ON CONFLICT DO UPDATE

5. **`_upsert_component(entity_id: str, component_type: str, system_prompt: Optional[str], metadata: dict, db: Session) -> None`**
   - Upsert EntityComponent table:
     ```python
     {
       "entity_id": entity_id,
       "component_type": component_type,  # "bot", "human", "skill", "tool"
       "system_prompt": system_prompt,
       "metadata": metadata,  # JSONB field
       "updated_at": now
     }
     ```

6. **`get_entity_vector(entity_id: str, domain: str, vector_name: str, db: Session) -> tuple[float, float]`**
   - Query EntityProfile for entity_id + domain + vector_name
   - If found: return (value, confidence)
   - Else: cold-start cascade:
     1. Try domain average: query all entities in domain, compute mean
     2. If domain avg exists: return (domain_avg, confidence=0.3)
     3. Else: return neutral (0.5, confidence=0.1)

7. **`compute_global_vector(entity_id: str, vector_name: str, db: Session) -> tuple[float, float]`**
   - Query EntityProfile for entity_id + all domains + vector_name
   - Compute confidence-weighted average:
     ```python
     weighted_sum = sum(value * confidence for value, confidence in domain_values)
     total_confidence = sum(confidence for _, confidence in domain_values)
     global_value = weighted_sum / total_confidence if total_confidence > 0 else 0.5
     global_confidence = total_confidence / len(domain_values) if domain_values else 0.1
     ```
   - Return (global_value, global_confidence)

**Confidence formula:**
```python
def compute_confidence(sample_size: int, source: str) -> float:
    # Sample size factor: diminishing returns
    size_factor = sample_size / (sample_size + 10)

    # Source multipliers
    source_multipliers = {
        "computed": 1.0,
        "observed": 1.0,
        "declared": 0.6,
        "imported": 0.5
    }

    return size_factor * source_multipliers.get(source, 0.5)
```

---

### vectors_compute.py (~336 lines)

**Function:** `compute_alpha(entity_id: str, domain: str, db: Session) -> tuple[float, float]`

**Implementation:**
- Alpha = autonomy score (0-1)
- Fetch events from last 30 days: `task.claimed`, `task.completed`, `task.failed`
- Classify signals:
  - Internal: `task.claimed` by entity (self-initiated)
  - External: `task.assigned` to entity (human-initiated)
- Formula: `alpha = internal_signals / total_signals`
- Confidence: `compute_confidence(total_signals, source="computed")`
- Return (alpha, confidence)

**Function:** `compute_sigma(entity_id: str, domain: str, db: Session) -> tuple[float, float]`

**Implementation:**
- Sigma = quality score (0-1)
- Fetch events: `task.completed`, `task.failed`
- Detect rework: sequences of `task.failed` → `task.completed` for same task_id
- Formula:
  ```python
  outcome = completed_count / (completed_count + failed_count) if total > 0 else 0.5
  rework_fraction = rework_sequences / completed_count if completed_count > 0 else 0.0
  sigma = outcome * (1 - rework_fraction)
  ```
- Confidence: `compute_confidence(completed_count + failed_count, source="computed")`
- Return (sigma, confidence)

**Function:** `compute_rho(entity_id: str, domain: str, db: Session) -> tuple[float, float]`

**Implementation:**
- Rho = reliability score (0-1) — SLA adherence
- Fetch events: `task.completed`
- Get SLA target: `_get_sla_target(domain, db)`
- For each task: check if duration_ms <= SLA_target
- Formula: `rho = tasks_meeting_sla / total_tasks`
- Confidence: `compute_confidence(total_tasks, source="computed")`
- Return (rho, confidence)

**Function:** `compute_pi_bot(entity_id: str, domain: str, db: Session) -> tuple[float, float]`

**Implementation:**
- Pi_bot = bot preference (0-1) — cosine similarity to domain archetype
- Get system_prompt: `_get_entity_prompt(entity_id, db)`
- If no prompt: return (0.5, confidence=0.1) cold-start
- Call `compute_pi_bot_full(entity_id, domain, system_prompt, db=db)` from embeddings.py
- Extract domain_sim from result
- Confidence: `compute_confidence(1, source="computed")` (always 1 sample for bot embeddings)
- Return (domain_sim, confidence)

**Function:** `compute_pi_human(entity_id: str, domain: str, db: Session) -> tuple[float, float]`

**Implementation:**
- Pi_human = human preference (0-1)
- Two sources:
  1. **Observed (high-alpha entities):** Fetch `task.claimed` events, compute claim_rate in domain
  2. **Declared:** Query EntityProfile for declared pi_human value
- Prefer observed over declared
- If observed available: return (claim_rate, confidence based on sample size)
- Else if declared available: return (declared_value, confidence=0.6)
- Else: return (0.5, confidence=0.1) cold-start

**Function:** `recalculate_entity(entity_id: str, domain: str, db: Session) -> dict`

**Implementation:**
- Full recalculation of all vectors for entity in domain
- Steps:
  1. Compute alpha: `compute_alpha(entity_id, domain, db)`
  2. Compute sigma: `compute_sigma(entity_id, domain, db)`
  3. Compute rho: `compute_rho(entity_id, domain, db)`
  4. Compute pi_bot: `compute_pi_bot(entity_id, domain, db)`
  5. Compute pi_human: `compute_pi_human(entity_id, domain, db)`
  6. Upsert all 5 profiles: `_upsert_profile()` for each
  7. Append to history table (optional): EntityVectorHistory (entity_id, domain, vector_name, value, confidence, timestamp)
- Return stats:
  ```python
  {
    "entity_id": entity_id,
    "domain": domain,
    "vectors": {
      "alpha": {"value": alpha, "confidence": alpha_conf},
      "sigma": {"value": sigma, "confidence": sigma_conf},
      "rho": {"value": rho, "confidence": rho_conf},
      "pi_bot": {"value": pi_bot, "confidence": pi_bot_conf},
      "pi_human": {"value": pi_human, "confidence": pi_human_conf}
    },
    "updated_at": now.isoformat()
  }
  ```

---

### test_vectors.py (20+ tests)

**Test cases (use mock Event Ledger data):**

**Alpha tests (4):**
- Test alpha with 8 internal, 2 external signals → 0.8
- Test alpha with zero signals → 0.5 (default)
- Test alpha confidence increases with sample size
- Test 30-day decay weighting (older events weighted less)

**Sigma tests (4):**
- Test sigma with 9 completed, 1 failed, 0 rework → 0.9
- Test sigma with rework sequences (failed → completed) → reduced score
- Test sigma with zero tasks → 0.5 (default)
- Test sigma confidence based on sample size

**Rho tests (4):**
- Test rho with 8 tasks meeting SLA, 2 exceeding → 0.8
- Test rho with all tasks meeting SLA → 1.0
- Test rho with zero tasks → 1.0 (default optimistic)
- Test rho with custom SLA target (not default 1 hour)

**Pi_bot tests (3):**
- Test pi_bot with high domain similarity → 0.9
- Test pi_bot with no prompt → 0.5 (cold-start)
- Test pi_bot confidence always low (1 sample)

**Pi_human tests (3):**
- Test pi_human observed (high claim rate) → 0.85
- Test pi_human declared fallback → 0.6 confidence
- Test pi_human cold-start → 0.5 (no data)

**Integration tests (2):**
- Test `recalculate_entity()` computes all 5 vectors
- Test `compute_global_vector()` weighted average across domains

**Helper tests (2):**
- Test `get_entity_vector()` cold-start cascade (local → domain avg → neutral)
- Test `compute_confidence()` formula with sample sizes

## Acceptance Criteria

- [ ] All listed files created
- [ ] All tests pass (`python -m pytest tests/hivenode/entities/test_vectors.py -v`)
- [ ] No file exceeds 500 lines (MUST split vectors.py into vectors_core.py + vectors_compute.py)
- [ ] PORT not rewrite — same 5 formulas (alpha, sigma, rho, pi_bot, pi_human), same 30-day decay, same confidence weighting as platform/efemera
- [ ] TDD: tests written first
- [ ] 20+ tests covering all 5 vectors with known inputs, cold-start cascade, domain averages, edge cases (zero events, no SLA, rework detection)
- [ ] Confidence formula: `(sample_size / (sample_size + 10)) × source_multiplier`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-119-RESPONSE.md`

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
