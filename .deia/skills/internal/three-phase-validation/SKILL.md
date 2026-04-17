---
name: three-phase-validation
description: >-
  Run PROCESS-0013 build integrity validation with Gate 0 (Prompt→SPEC
  disambiguation), Phase 0 (coverage validation), Phase 1 (SPEC fidelity),
  and Phase 2 (TASK fidelity) including healing loops and escalation. Use
  when validating specs, task breakdowns, or ensuring requirement coverage
  before implementation.
license: Proprietary
compatibility: Requires Python 3.12+, Voyage API access for embeddings, LLM access for healing
metadata:
  author: Q88N
  version: "1.0"
  deia:
    cert_tier: 3
    carbon_class: medium
    requires_human: false
---

# Three-Phase Validation (PROCESS-0013)

## Steps

### Step 1: Understand the Three Acts

PROCESS-0013 validates that specs and task breakdowns preserve requirement coverage and semantic meaning through three phases plus a disambiguation gate:

**Gate 0: Prompt→SPEC Disambiguation** — Did LLM understand user intent?
- Extract requirements tree from user prompt
- Extract requirements tree from generated SPEC
- Compare trees for coverage, hallucinations, orphans
- Validate with TF-IDF similarity matching (threshold: 0.7)
- Overall embedding similarity ≥ 0.85
- **Pass criteria:** 100% coverage, no hallucinations, no orphans, similarity ≥ 0.85
- **Fail → Healing loop:** Max 3 retries, then escalate to human

**Phase 0: Coverage Validation** — Are ALL requirements from ASSIGNMENT in SPEC?
- Extract structured requirements from ASSIGNMENT
- Check each requirement against SPEC
- Flag violations (mandatory requirements declared out-of-scope)
- **Pass criteria:** 100% coverage, 0 violations
- **Fail → Healing loop:** Max 3 retries, then escalate to human

**Phase 1: SPEC Fidelity** — Does SPEC→IR→SPEC' preserve meaning?
- Encode SPEC to PHASE-IR format
- Decode IR back to SPEC'
- Compare with Voyage embeddings (cosine similarity)
- **Pass criteria:** Fidelity ≥ 0.85
- **Fail → Healing loop:** Max 3 retries, then escalate to human

**Phase 2: TASK Fidelity** — Does TASKS→IR→TASKS' preserve meaning?
- Encode TASKS to PHASE-IR format
- Decode IR back to TASKS'
- Compare with Voyage embeddings (cosine similarity)
- **Pass criteria:** Fidelity ≥ 0.85
- **Fail → Healing loop:** Max 3 retries, then escalate to human

**The foundational bug:** Phase 1 and 2 fidelity can both pass (SPEC→IR→SPEC' preserves meaning internally) while Phase 0 coverage fails (SPEC is missing requirements from ASSIGNMENT). This is the Q33N-003B case study — the original failure that created this process.

### Step 2: Run Gate 0 (Prompt→SPEC Disambiguation)

**Inputs:**
- User prompt (original request)
- Generated SPEC

**Process:**
1. Extract requirements tree from user prompt (hierarchical: REQ-001, REQ-001.1, etc.)
2. Extract requirements tree from generated SPEC
3. Compare trees:
   - Structural checks (parent-child preserved, no orphans)
   - Coverage checks (every prompt req in SPEC, no hallucinations)
   - TF-IDF similarity matching (threshold: 0.7 per requirement)
   - Overall embedding similarity (threshold: 0.85)

**Outputs:**
- `gate0.passed` (True/False)
- `gate0.coverage` (0.0-1.0)
- `gate0.missing` (list of prompt requirements not in SPEC)
- `gate0.hallucinated` (list of SPEC requirements not in prompt)
- `gate0.orphans` (list of orphaned child requirements)
- `gate0.embedding_similarity` (0.0-1.0)
- `gate0.diagnostic` (markdown diagnostic string)

**Healing loop (if failed):**
1. Generate diagnostic showing what's wrong
2. Call LLM with healing prompt:
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
3. Save healed SPEC, increment retry counter, re-validate
4. If retries ≥ 3 → Escalate to human (approve/edited/abort)

**Save report:** `.deia/hive/responses/YYYY-MM-DD-HHMM-{AGENT}-{TASK}-GATE0-REPORT.md`

### Step 3: Run Phase 0 (Coverage Validation)

**Inputs:**
- ASSIGNMENT markdown (contains requirements)
- SPEC markdown (proposed solution)

**Process:**
1. Extract requirements from ASSIGNMENT using LLM:
   ```
   Extract all requirements from this assignment.
   For each requirement, provide:
   - id: REQ-{CATEGORY}-{NNN}
   - type: user_story | technical | constraint
   - category: UI | Backend | Performance | Security | etc.
   - description: what is required
   - acceptance: how to verify
   - mandatory: true | false

   Output as JSON array.
   ```

2. For each requirement, check coverage in SPEC using LLM:
   ```
   Read this SPEC and determine if this requirement is covered:

   Requirement: {description}
   Category: {category}
   Mandatory: {mandatory}

   SPEC:
   {spec_text}

   Respond with JSON:
   {
     "status": "COVERED | PARTIAL | MISSING | OUT_OF_SCOPE",
     "location": "line number or section",
     "evidence": "quoted text showing coverage",
     "confidence": 0.0-1.0
   }
   ```

3. Generate coverage report

**Outputs:**
- Total requirements, covered count, partial count, missing count, violations count
- Per-requirement: status, location, evidence, confidence
- Pass/fail: `coverage == 1.0 AND violations == 0`

**Healing loop (if failed):**
1. Diagnostic shows missing/out-of-scope requirements
2. Call LLM with healing prompt:
   ```
   Phase 0 coverage validation failed. Your SPEC is missing requirements.

   ASSIGNMENT: [full text]
   Current SPEC: [current text]
   Coverage Report: [JSON with missing/violations]

   Regenerate SPEC that:
   1. Includes ALL missing requirements
   2. Preserves existing coverage that passed
   3. Achieves 100% coverage with 0 violations
   4. Uses same format with traceability IDs
   ```
3. Save healed SPEC, increment retry counter, re-run Phase 0
4. If retries ≥ 3 → Escalate to human

**Save report:** `.deia/hive/responses/YYYY-MM-DD-HHMM-{AGENT}-{TASK}-PHASE0-REPORT.md`

### Step 4: Run Phase 1 (SPEC Fidelity)

**Inputs:**
- SPEC markdown

**Process:**
1. Encode SPEC to PHASE-IR JSON using LLM
2. Decode IR back to SPEC' (natural language) using LLM
3. Compute Voyage embeddings for SPEC and SPEC'
4. Calculate cosine similarity (fidelity score)

**Outputs:**
- `fidelity` (0.0-1.0)
- `passed` (fidelity ≥ 0.85)
- IR JSON generated

**Healing loop (if failed):**
1. Diagnostic shows fidelity score < 0.85, semantic drift
2. Call LLM with healing prompt:
   ```
   Phase 1 SPEC fidelity validation failed. Round-trip lost meaning.

   Original SPEC: [original]
   Reconstructed SPEC': [reconstructed]
   Fidelity Score: [score]

   Regenerate SPEC that:
   1. Preserves all semantic meaning when encoded to IR
   2. Uses clear, unambiguous language
   3. Makes relationships and dependencies explicit
   4. Achieves fidelity ≥ 0.85
   5. Uses same format with traceability IDs
   ```
3. Save healed SPEC, increment retry counter, re-run Phase 1
4. If retries ≥ 3 → Escalate to human

**Save report:** `.deia/hive/responses/YYYY-MM-DD-HHMM-{AGENT}-{TASK}-PHASE1-REPORT.md`

### Step 5: Run Phase 2 (TASK Fidelity)

**Inputs:**
- TASKS markdown (task breakdown from SPEC)

**Process:**
1. Encode TASKS to PHASE-IR JSON using LLM
2. Decode IR back to TASKS' using LLM
3. Compute Voyage embeddings for TASKS and TASKS'
4. Calculate cosine similarity (fidelity score)

**Outputs:**
- `fidelity` (0.0-1.0)
- `passed` (fidelity ≥ 0.85)
- IR JSON generated

**Healing loop (if failed):**
1. Diagnostic shows fidelity score < 0.85
2. Call LLM with healing prompt:
   ```
   Phase 2 TASK fidelity validation failed. Round-trip lost meaning.

   Original TASKS: [original]
   Reconstructed TASKS': [reconstructed]
   Fidelity Score: [score]

   Regenerate TASKS that:
   1. Preserves all dependencies and relationships
   2. Makes task ordering explicit
   3. Preserves all implementation details
   4. Achieves fidelity ≥ 0.85
   5. Uses same format with traceability IDs
   ```
3. Save healed TASKS, increment retry counter, re-run Phase 2
4. If retries ≥ 3 → Escalate to human

**Save report:** `.deia/hive/responses/YYYY-MM-DD-HHMM-{AGENT}-{TASK}-PHASE2-REPORT.md`

### Step 6: Human Escalation (if max retries reached)

If any gate or phase fails after 3 healing attempts, escalate:

```markdown
{Gate/Phase} failed after 3 retries. Manual intervention needed.

{Input artifacts}

Diagnostic:
[diagnostic message]

Please review and either:
1. Type 'approve' to override validation
2. Type 'edited' after manually editing {artifact}
3. Type 'abort' to stop the task
```

**Human options:**
- `approve` — override validation and proceed to next phase
- `edited` — user manually fixed artifact, reload and proceed
- `abort` — terminal failure, stop process

### Step 7: Proceed to Implementation (if all phases pass)

```python
# Build is READY FOR IMPLEMENTATION when:
gate_0.passed == True           # 100% coverage, no hallucinations
phase_0.passed == True          # 100% coverage, 0 violations
phase_1.fidelity >= 0.85        # SPEC→IR→SPEC' preserves meaning
phase_2.fidelity >= 0.85        # TASKS→IR→TASKS' preserves meaning

# Only then dispatch worker bees
```

## Output Format

### Gate 0 Report

```markdown
# Gate 0: Prompt→SPEC Disambiguation

**Coverage:** 1.0 (100%)
**Missing:** 0
**Hallucinated:** 0
**Orphans:** 0
**Embedding Similarity:** 0.92
**Status:** PASS

## Requirements Tree Comparison

{structural and coverage checks}

## Diagnostic

All requirements from user prompt present in SPEC. No hallucinations detected.
```

### Phase 0 Report

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
```

### Phase 1 Report

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

### Phase 2 Report

Same format as Phase 1, but for TASKS instead of SPEC.

## Gotchas

### 1. Fidelity Can Pass While Coverage Fails
The Q33N-003B case study: Phase 1 fidelity 0.9128 (PASS), Phase 2 fidelity 0.9023 (PASS), but missing 2 UI requirements (Phase 0 FAIL). **Always run Phase 0 before Phase 1/2.**

### 2. Healing Loops Are Capped at 3 Retries
After 3 failed healing attempts, you MUST escalate to human. Do not continue retrying indefinitely.

### 3. Gate 0 Is the Disambiguation Layer
Gate 0 catches LLM misunderstandings of user intent. This is different from coverage (Phase 0) — Gate 0 validates the prompt→SPEC translation, Phase 0 validates ASSIGNMENT→SPEC coverage.

### 4. Voyage Embeddings vs TF-IDF
Gate 0 uses TF-IDF for requirement matching (0.7 threshold). Phases 1/2 use Voyage embeddings for fidelity (0.85 threshold). Different metrics for different purposes.

### 5. Builder Bee Never Tests Own Output
A separate validator (Q33N or superior agent) runs three-phase validation. The bee that built the SPEC or TASKS does NOT self-validate.

### 6. Escalation Is Not Failure
Escalating to human after max retries is the correct behavior. It means automated healing couldn't fix the issue — human judgment needed.

### 7. Reports Go to .deia/hive/responses/
Not `.deia/hive/tasks/`, not `docs/`. All validation reports live in responses directory.

### 8. Traceability IDs Are Mandatory
PROCESS-0013 requires traceability: REQ-{CAT}-{NNN} → SPEC-{NNN} → TASK-{NNN} → CODE-{NNN} → TEST-{NNN}. Validation cannot run without IDs.

### 9. [UNDOCUMENTED — needs process doc]
How to handle partial SPEC updates (e.g., only Phase 1 failed, Gate 0 and Phase 0 passed). Current practice: re-run all phases after healing any phase. No incremental validation exists.

### 10. [UNDOCUMENTED — needs process doc]
Token/cost budgeting for healing loops. Each healing attempt consumes ~5k-10k tokens. 3 retries × 3 phases = up to 90k tokens for a difficult spec. No formal budget cap exists.

### 11. Embedding Similarity Threshold May Change
Currently 0.85 for Phase 1/2, may raise to 0.90. Gate 0 uses 0.85 overall + 0.7 per-requirement TF-IDF. These thresholds are calibrated from the Q33N-003B case study.

### 12. Human Escalation Options
- `approve` — proceed despite validation failure (dangerous, use sparingly)
- `edited` — human manually fixed, re-validate (recommended)
- `abort` — stop task entirely (use when spec is fundamentally wrong)
