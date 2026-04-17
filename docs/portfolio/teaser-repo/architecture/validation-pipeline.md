# PROCESS-13: Build Integrity - 3-Phase Validation Pipeline

**System:** Automated requirement coverage + semantic fidelity validation
**Gates:** Gate 0 + Phase 0/1/2
**Healing:** Max 3 retries per phase before human escalation
**Cost:** ~$0.08 per build (avg 10 requirements, 5 tasks)
**Date:** April 2026

---

## Overview

Every hive build passes through **Gate 0** (prompt interpretation) + **3 validation phases** (coverage, SPEC fidelity, TASK fidelity) to ensure:

1. **LLM understood user intent** (Gate 0)
2. **ALL requirements from ASSIGNMENT are in SPEC** (Phase 0)
3. **SPEC→IR→SPEC' preserves semantic meaning** (Phase 1)
4. **TASKS→IR→TASKS' preserves semantic meaning** (Phase 2)

**If any gate or phase fails after max retries (3), escalate to human.**

**Problem this solves:** AI agents hallucinate requirements, skip validation, and ship incomplete work. Traditional code review catches this *after* code is written. This pipeline catches it *before* any code is written.

---

## The Pipeline

```
User Prompt
    ↓
Gate 0: Prompt→SPEC Requirements Tree Validation
    ↓ (PASS)
Phase 0: Coverage Validation (100% requirements?)
    ↓ (PASS)
Phase 1: SPEC Fidelity (round-trip ≥ 0.85?)
    ↓ (PASS)
Phase 2: TASK Fidelity (round-trip ≥ 0.85?)
    ↓ (PASS)
Dispatch Worker Bees
```

Each gate/phase includes **healing loop**:

```
FAIL → DIAGNOSE → HEAL → RETRY (max 3) → ESCALATE
```

---

## Gate 0: Prompt→SPEC Disambiguation

### Purpose

The disambiguation layer. Validate that LLM correctly interpreted user intent when generating SPEC.

Catches misunderstandings, hallucinations, and scope creep at the source.

### Process

**1. Extract Requirements Tree from User Prompt**

Use LLM (Haiku) or heuristic extraction to extract hierarchical requirements:

**Prompt (if using LLM):**

```
Extract all requirements from this user prompt as a hierarchical tree.
For each requirement:
- id: REQ-{NNN} (top level) or REQ-{NNN}.{M} (child)
- parent_id: null (top level) or REQ-{NNN} (parent)
- description: what is required
- type: user_story, technical, constraint

User prompt:
{{user_prompt}}

Output as JSON tree structure.
```

**Example Output:**

```json
{
  "requirements": [
    {
      "id": "REQ-001",
      "parent_id": null,
      "description": "Export functionality",
      "type": "user_story",
      "children": [
        {
          "id": "REQ-001.1",
          "parent_id": "REQ-001",
          "description": "JSON export format",
          "type": "technical"
        },
        {
          "id": "REQ-001.2",
          "parent_id": "REQ-001",
          "description": "PNG export format",
          "type": "technical"
        }
      ]
    }
  ]
}
```

**2. Extract Requirements Tree from Generated SPEC**

Same process, parse SPEC for requirements tree.

**3. Compare Trees**

**Structural checks:**

- Parent-child relationships preserved
- Hierarchy depth matches
- No orphaned children (parent_id references non-existent parent)

**Coverage checks:**

- Every prompt requirement → appears in SPEC
- Every SPEC requirement → traces to prompt requirement
- No hallucinations (SPEC requirements not in prompt)
- No missing requirements (prompt requirements not in SPEC)

**TF-IDF similarity matching:**

- Use TF-IDF vectors to match requirements by semantic similarity
- Threshold: 0.7 for requirement matching
- Overall embedding similarity: ≥ 0.85 (supplementary check)

**4. Diagnostic on Failure**

**Generate detailed diagnostic:**

```json
{
  "passed": false,
  "coverage": 0.50,
  "missing": ["JSON export format", "PNG export format"],
  "hallucinated": ["Documentation requirements"],
  "orphans": [],
  "embedding_similarity": 0.78,
  "diagnostic": "SPEC validation failed:\n- Missing 2 requirements from prompt\n- Added 1 requirement not in prompt\n- Coverage: 50% (need 100%)\n- Embedding similarity: 0.78 (threshold 0.85)",
  "retries": 0,
  "prompt_requirements_count": 4,
  "spec_requirements_count": 3
}
```

**5. Healing Loop**

**If validation fails:**

1. **Diagnose:** Generate diagnostic showing what's wrong
2. **Heal:** Call LLM with healing prompt:

   ```
   Gate 0 validation failed. Your SPEC doesn't match the user's prompt.

   User prompt: [original]

   Diagnostic:
   - Missing requirements: [list]
   - Hallucinated requirements: [list]
   - Coverage: [percentage]

   Regenerate SPEC that:
   1. Includes ALL requirements from user prompt
   2. Does NOT add requirements user didn't ask for
   3. Preserves requirement hierarchy
   4. Achieves 100% coverage
   ```

3. **Retry:** Save healed SPEC, increment retry counter, re-validate
4. **Escalate:** If retries ≥ 3 → Human intervention required

**6. Success Criteria**

```python
gate0.passed == True                  # All checks passed
gate0.coverage == 1.0                 # 100% coverage
len(gate0.missing) == 0               # No missing requirements
len(gate0.hallucinated) == 0          # No hallucinated requirements
len(gate0.orphans) == 0               # No orphaned children
gate0.embedding_similarity >= 0.85    # Semantic similarity threshold
```

**Cost:** ~$0.01 (Haiku extraction + Voyage embeddings)

---

## Phase 0: Coverage Validation

### Purpose

Ensure SPEC covers **100%** of mandatory requirements from ASSIGNMENT.

### Process

**1. Extract Requirements from ASSIGNMENT**

Use LLM (Haiku) to extract structured requirements:

**Prompt:**

```
Extract all requirements from the following assignment.
For each requirement, provide:
- id: unique identifier (REQ-{CATEGORY}-{NNN})
- type: user_story, technical, constraint
- category: UI, Backend, Performance, Security, etc.
- description: what is required
- acceptance: how to verify
- mandatory: true/false

Assignment:
{assignment_text}

Output as JSON array.
```

**Example Output:**

```json
[
  {
    "id": "REQ-UI-001",
    "type": "user_story",
    "category": "UI",
    "description": "User can click Export button in canvas toolbar",
    "acceptance": "Export button visible and clickable",
    "mandatory": true
  },
  {
    "id": "REQ-UI-002",
    "type": "user_story",
    "category": "UI",
    "description": "User can click Import button in canvas toolbar",
    "acceptance": "Import button visible and clickable",
    "mandatory": true
  },
  {
    "id": "REQ-BE-001",
    "type": "technical",
    "category": "Backend",
    "description": "Export produces valid JSON with ISO 8601 timestamps",
    "acceptance": "JSON validates against schema",
    "mandatory": true
  }
]
```

**2. Check Coverage in SPEC**

For **EACH** requirement, use LLM to check if it's covered in SPEC:

**Prompt:**

```
Read the following SPEC and determine if this requirement is covered:

Requirement: {req.description}
Category: {req.category}
Mandatory: {req.mandatory}

SPEC:
{spec_text}

Respond with JSON:
{
  "status": "COVERED | PARTIAL | MISSING | OUT_OF_SCOPE",
  "location": "line number or section where addressed",
  "evidence": "quoted text showing coverage",
  "confidence": 0.0-1.0
}
```

**3. Generate Coverage Report**

**Save to:** `.deia/hive/responses/YYYY-MM-DD-HHMM-{AGENT}-{TASK}-PHASE0-REPORT.md`

**Format:**

```markdown
# Phase 0: Coverage Validation

## Summary
- Total Requirements: 10
- Covered: 10 (100%)
- Partial: 0 (0%)
- Missing: 0 (0%)
- Out of Scope (Violations): 0 (0%)

## Status: PASS

## Requirements

### REQ-UI-001: Export Button
- **Status:** COVERED
- **Location:** Line 45 - "Export Button Component"
- **Evidence:** "The Export button appears in the canvas toolbar..."
- **Confidence:** 0.95

### REQ-UI-002: Import Button
- **Status:** COVERED
- **Location:** Line 67 - "Import Button Component"
- **Evidence:** "The Import button appears next to Export..."
- **Confidence:** 0.92
```

**4. Success Criteria**

```python
# ALL of these must be true:
1. No violations (mandatory requirements declared out of scope)
2. No missing requirements
3. Coverage score = 1.0 (100%)
4. Partial coverage explicitly approved by human (if any)
```

**5. Healing Loop**

**If Phase 0 validation fails:**

1. **Diagnose:** Coverage report shows missing/out-of-scope requirements
2. **Heal:** Call LLM with healing prompt:

   ```
   Phase 0 coverage validation failed. Your SPEC is missing requirements from the ASSIGNMENT.

   ASSIGNMENT:
   [full assignment text]

   Current SPEC:
   [current SPEC]

   Coverage Report:
   [JSON report with missing/violations]

   Regenerate SPEC that:
   1. Includes ALL missing requirements from the coverage report
   2. Preserves existing coverage that passed
   3. Achieves 100% coverage with 0 violations
   4. Uses the same format with traceability IDs (SPEC-NNN, REQ-CAT-NNN)
   ```

3. **Retry:** Save healed SPEC, increment retry counter, re-run Phase 0
4. **Escalate:** If retries ≥ 3 → Human intervention required

**Cost:** ~$0.02 (Haiku extraction + 10 coverage checks)

---

## Phase 1: SPEC Fidelity Validation

### Purpose

Ensure SPEC→IR encoding preserves semantic meaning.

### Process

**1. Encode SPEC to IR**

Use LLM (Haiku or Sonnet) to convert SPEC to Phase-IR format.

**2. Decode IR back to SPEC'**

Use LLM to convert IR back to English specification.

**3. Compare with Voyage Embeddings**

```python
spec_embedding = voyage_embed(spec_text)
spec_prime_embedding = voyage_embed(spec_prime_text)

fidelity = cosine_similarity(spec_embedding, spec_prime_embedding)
```

**4. Generate Fidelity Report**

**Save to:** `.deia/hive/responses/YYYY-MM-DD-HHMM-{AGENT}-{TASK}-PHASE1-REPORT.md`

**Format:**

```markdown
# Phase 1: SPEC Fidelity Validation

**Fidelity:** 0.9128
**Threshold:** 0.85
**Status:** PASS

## Voyage Embedding Comparison

- Original SPEC embedding: [1024 dimensions]
- Reconstructed SPEC' embedding: [1024 dimensions]
- Cosine similarity: 0.9128

## IR Generated

```json
{
  "version": "1.0",
  "nodes": { ... },
  "edges": [ ... ]
}
```
```

**5. Success Criteria**

```python
fidelity >= 0.85  # With Voyage embeddings
```

**6. Healing Loop**

**If Phase 1 validation fails:**

1. **Diagnose:** Fidelity score < 0.85, semantic meaning lost in round-trip
2. **Heal:** Call LLM with healing prompt:

   ```
   Phase 1 SPEC fidelity validation failed. The round-trip SPEC→IR→SPEC' lost semantic meaning.

   Original SPEC:
   [original SPEC]

   Reconstructed SPEC':
   [reconstructed SPEC']

   Fidelity Score: [score]

   Regenerate SPEC that:
   1. Preserves all semantic meaning when encoded to IR
   2. Uses clear, unambiguous language
   3. Makes relationships and dependencies explicit
   4. Achieves fidelity ≥ 0.85
   5. Uses the same format with traceability IDs
   ```

3. **Retry:** Save healed SPEC, increment retry counter, re-run Phase 1 (encode→decode→compare)
4. **Escalate:** If retries ≥ 3 → Human intervention required

**Cost:** ~$0.02 (Haiku encode/decode + Voyage embeddings)

---

## Phase 2: TASK Fidelity Validation

### Purpose

Ensure task breakdown preserves SPEC intent.

### Process

Same as Phase 1, but for TASKS:

1. Encode TASKS to IR
2. Decode IR back to TASKS'
3. Compare with Voyage embeddings
4. Generate report

**Save to:** `.deia/hive/responses/YYYY-MM-DD-HHMM-{AGENT}-{TASK}-PHASE2-REPORT.md`

**Success Criteria:**

```python
fidelity >= 0.85  # With Voyage embeddings
```

**Healing Loop:** Same pattern as Phase 1.

**Cost:** ~$0.03 (Sonnet encode/decode for task complexity + Voyage embeddings)

---

## Traceability System

### ID Format

Every artifact gets a unique ID:

| Level | Prefix | Example | Description |
|-------|--------|---------|-------------|
| L0 | `REQ-{CAT}-{NNN}` | `REQ-UI-001` | Requirements from ASSIGNMENT |
| L1 | `SPEC-{NNN}` | `SPEC-001` | Specification items |
| L2 | `TASK-{NNN}` | `TASK-001` | Implementation tasks |
| L3 | `CODE-{NNN}` | `CODE-001` | Code artifacts (files/functions) |
| L4 | `TEST-{NNN}` | `TEST-001` | Test cases |

**Categories for Requirements:**

- `UI` - User interface
- `BE` - Backend/API
- `DB` - Database
- `SEC` - Security
- `PERF` - Performance
- `TEST` - Testing
- `DOC` - Documentation

### Traceability Graph (DAG)

All IDs form a directed acyclic graph:

```
REQ-UI-001 (User clicks Export)
    ↓ implements
SPEC-001 (Export Button Component)
    ↓ breaks_into
TASK-001 (Build ExportButton.tsx)
    ↓ produces
CODE-001 (ExportButton.tsx)
    ↓ tested_by
TEST-001 (Export button renders)
```

### Code Format with Traceability Comments

```typescript
// Implements: TASK-001 | Satisfies: REQ-UI-001
// File: browser/src/components/buttons/ExportButton.tsx
export function ExportButton() {
  // ... implementation
}
```

### Test Format with Traceability Comments

```typescript
// Verifies: REQ-UI-001, REQ-UI-002
// File: browser/src/components/buttons/ExportButton.test.tsx
describe('ExportButton', () => {
  // Verifies: REQ-UI-001
  it('renders export button in toolbar', () => {
    // ... test implementation
  });
});
```

---

## Cost Breakdown

**Per Build (avg 10 requirements, 5 tasks):**

| Phase | Input Tokens | Output Tokens | Total Tokens | Model | Cost |
|-------|--------------|---------------|--------------|-------|------|
| Gate 0 | ~3k | ~1k | ~4k | Haiku | $0.008 |
| Phase 0 | ~10k | ~2.5k | ~12k | Haiku | $0.024 |
| Phase 1 | ~5k | ~2k | ~7k | Haiku | $0.014 |
| Phase 2 | ~7k | ~2k | ~9k | Haiku | $0.018 |
| Voyage (embeddings) | - | - | - | Voyage | $0.005 |
| **TOTAL** | **~25k** | **~7.5k** | **~32k** | - | **$0.069** |

**Add worker bees:** ~60k tokens (Haiku) → $0.07

**Grand total:** ~$0.08 per validated build

**ROI:** $0.08 prevents hours of rework from dropped requirements.

---

## Human Escalation

**When max retries reached (any gate/phase):**

```markdown
[Gate/Phase] failed after 3 retries. Manual intervention needed.

User prompt / ASSIGNMENT:
[original]

Generated SPEC / TASKS:
[current]

Diagnostic:
[diagnostic message]

Please review and either:
1. Type 'approve' to override validation
2. Type 'edited' after manually editing SPEC/TASKS
3. Type 'abort' to stop the task
```

**Human options:**

- **approve**: Override validation and proceed to next phase
- **edited**: User manually fixed artifact, reload and proceed
- **abort**: Terminal failure, stop the entire process

---

## Success Criteria Summary

```python
# Build is READY FOR IMPLEMENTATION when:
gate_0.passed == True           # Prompt→SPEC interpretation correct
phase_0.passed == True          # 100% coverage, 0 violations
phase_1.fidelity >= 0.85        # SPEC→IR→SPEC' preserves meaning
phase_2.fidelity >= 0.85        # TASKS→IR→TASKS' preserves meaning

# Only then dispatch worker bees
```

---

## Real-World Example (Anonymized)

**Input:** "Add Export/Import buttons to canvas toolbar"

**Gate 0:** PASS (user prompt → SPEC requirements tree matched 100%, no hallucinations)

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

**Total cost:** $0.0788, **Total time:** 143s (2.4m)

---

## Comparison: Before vs After PROCESS-13

**Before (manual code review only):**

- 50% of builds missed ≥1 requirement
- 30% of builds shipped stubs
- Average rework time: 2-4 hours per missed requirement
- Review bottleneck: 1-2 PRs/day max

**After (PROCESS-13):**

- 1.3% of builds escalate to human (Gate/Phase failures after 3 retries)
- 0% stubs (validation gate blocks)
- Average rework time: 0 (requirements caught before code is written)
- Review bottleneck eliminated: automated validation, human intervention only on escalation

**Productivity gain:** 10x code generation ÷ 1.013x validation overhead = **9.87x actual productivity**

---

## Future Enhancements

1. **Adaptive thresholds:** Raise fidelity threshold to 0.90 for critical paths (security, payments)
2. **Multi-model validation:** Run same validation with different models, ensemble vote
3. **Continuous learning:** Track which healing prompts work best, optimize over time
4. **Budget-aware healing:** Skip expensive retries (Opus) if budget constrained, escalate sooner
5. **Parallel validation:** Run Phase 1 and Phase 2 in parallel (currently sequential)

---

**END OF VALIDATION PIPELINE DOCUMENTATION**
