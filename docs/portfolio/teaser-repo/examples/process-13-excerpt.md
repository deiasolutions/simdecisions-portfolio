# PROCESS-13 Excerpt: Build Integrity 3-Phase Validation

**Source:** Full specification in private repo
**Purpose:** Portfolio demonstration of systematic AI correction

---

## Overview

Every hive build passes through Gate 0 + 3 validation phases to ensure requirement coverage and semantic fidelity. If any gate/phase fails after max retries (3), escalate to human.

---

## Gate 0: Prompt→SPEC Requirements Tree Validation

### Purpose

Validate that LLM correctly interpreted user intent when generating SPEC. Catches misunderstandings, hallucinations, and scope creep at the source.

### Process

1. **Extract requirements tree from user prompt** (LLM + TF-IDF)
2. **Extract requirements tree from generated SPEC**
3. **Compare trees:**
   - Structural checks (parent-child relationships preserved)
   - Coverage checks (no missing/hallucinated requirements)
   - TF-IDF similarity (≥ 0.7 per requirement, ≥ 0.85 overall)
4. **If FAIL:** Generate diagnostic → LLM healing prompt → Regenerate SPEC → Retry (max 3) → Escalate

### Success Criteria

```python
gate0.passed == True                  # All checks passed
gate0.coverage == 1.0                 # 100% coverage
len(gate0.missing) == 0               # No missing requirements
len(gate0.hallucinated) == 0          # No hallucinated requirements
gate0.embedding_similarity >= 0.85    # Semantic similarity threshold
```

---

## Phase 0: Coverage Validation

### Purpose

Ensure SPEC covers **100%** of mandatory requirements from ASSIGNMENT.

### Process

1. **Extract requirements from ASSIGNMENT** (LLM + structured JSON)
2. **For each requirement, check if covered in SPEC:**
   - LLM reads SPEC, returns COVERED | PARTIAL | MISSING | OUT_OF_SCOPE
3. **Generate coverage report** with evidence (line numbers, quoted text)
4. **If FAIL:** Heal SPEC with diagnostic feedback, retry (max 3), escalate

### Success Criteria

```python
# ALL of these must be true:
1. No violations (mandatory requirements declared out of scope)
2. No missing requirements
3. Coverage score = 1.0 (100%)
```

---

## Phase 1: SPEC Fidelity Validation

### Purpose

Ensure SPEC→IR encoding preserves semantic meaning.

### Process

1. **Encode SPEC to IR** (Phase-IR format)
2. **Decode IR back to SPEC'** (reconstructed specification)
3. **Compare SPEC vs SPEC'** with Voyage embeddings (cosine similarity)
4. **If fidelity < 0.85:** Heal SPEC (clearer language), retry (max 3), escalate

### Success Criteria

```python
fidelity >= 0.85  # Semantic meaning preserved in round-trip
```

---

## Phase 2: TASK Fidelity Validation

### Purpose

Ensure task breakdown preserves SPEC intent.

### Process

Same as Phase 1, but for TASKS:

1. Encode TASKS to IR
2. Decode IR back to TASKS'
3. Compare with Voyage embeddings
4. If fidelity < 0.85: Heal TASKS, retry (max 3), escalate

### Success Criteria

```python
fidelity >= 0.85  # Semantic meaning preserved
```

---

## Healing Loop Pattern

All gates and phases follow the same healing pattern:

1. **Validate** → Run validation checks
2. **Pass?** → Proceed to next phase
3. **Fail?** → Check retry count
   - **Retries < 3:** Generate diagnostic → Call LLM with healing prompt → Save healed artifact → Increment retry counter → Re-validate
   - **Retries ≥ 3:** Escalate to human for manual intervention
4. **Human Decision:**
   - **approve:** Override validation and proceed
   - **edited:** User manually fixed artifact, proceed
   - **abort:** Terminal failure, stop process

This ensures every validation failure gets up to 3 automated healing attempts before requiring human intervention.

---

## Cost & Metrics

**Per Build (avg 10 requirements, 5 tasks):**

| Phase | Tokens | Model | Cost |
|-------|--------|-------|------|
| Gate 0 | ~4k | Haiku | $0.008 |
| Phase 0 | ~12k | Haiku | $0.024 |
| Phase 1 | ~7k | Haiku | $0.014 |
| Phase 2 | ~9k | Haiku | $0.018 |
| Voyage | - | Voyage | $0.005 |
| **TOTAL** | **~32k** | - | **$0.069** |

**ROI:** $0.08 per validated build prevents hours of rework from dropped requirements.

**From 1,358 Completed Specs:**

- **Autonomous completion:** 98.7%
- **Human escalation:** 1.3% (17 specs)
- **Average cost per spec:** $0.08
- **Average time per spec:** ~143 seconds (2.4 minutes)
- **Regressions:** 0 (all tests pass after completion)

---

## Example: Real Validation Failure (Anonymized)

**Input:** "Add Export/Import buttons to canvas toolbar"

**Gate 0:** PASS (user prompt → SPEC requirements tree matched 100%)

**Phase 0 Coverage:**

- REQ-UI-001: Export Button → COVERED (SPEC line 45)
- REQ-UI-002: Import Button → COVERED (SPEC line 67)
- REQ-BE-001: JSON Export Format → COVERED (SPEC line 82)
- **Coverage: 100%, Status: PASS**

**Phase 1 SPEC Fidelity:**

- Original SPEC → Phase-IR → SPEC'
- Fidelity: 0.9128
- **Status: PASS** (≥ 0.85)

**Phase 2 TASK Fidelity:**

- TASKS → Phase-IR → TASKS'
- Fidelity: 0.9023
- **Status: PASS** (≥ 0.85)

**Result:** Bees dispatched, 8 tests written, all passing, 0 regressions.

---

**END OF EXCERPT**

Full PROCESS-13 specification (1039 lines) available in private repo on request.
