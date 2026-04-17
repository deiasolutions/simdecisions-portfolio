# PROCESS-0013: Build Integrity - 3-Phase Validation with Traceability

**Version:** 1.0
**Date:** 2026-02-25
**Status:** ACTIVE
**Applies To:** All hive builds (Q33N coordinated and solo bee builds)

---

## Overview

Every hive build MUST follow Gate 0 plus 3 validation phases to ensure requirement coverage and semantic fidelity:

1. **Gate 0: Prompt→SPEC Disambiguation** - Did LLM understand user intent? (Requirements tree validation)
2. **Phase 0: Coverage Validation** - Are ALL requirements from ASSIGNMENT in SPEC?
3. **Phase 1: SPEC Fidelity** - Does SPEC→IR→SPEC' preserve meaning?
4. **Phase 2: TASK Fidelity** - Does TASKS→IR→TASKS' preserve meaning?

**If any gate or phase fails after max retries (3), escalate to human. Do not proceed to implementation without approval.**

**All gates and phases include healing loops:** FAIL → DIAGNOSE → HEAL → RETRY (max 3) → ESCALATE

---

## The Problem This Solves

**Q33N-003B Case Study:**
- Phase 1 fidelity: 0.9128 (PASS ✓)
- Phase 2 fidelity: 0.9023 (PASS ✓)
- **Actual delivery:** Missing 2 UI requirements (FAIL ✗)

**Root Cause:** SPEC declared UI requirements "out of scope" even though ASSIGNMENT explicitly required them. Fidelity checks validated internal consistency but NOT requirement coverage.

**Solution:** Add Phase 0 coverage validation BEFORE fidelity checks.

---

## Gate 0: Prompt→SPEC Requirements Tree Validation

### Purpose
The disambiguation layer. Validate that LLM correctly interpreted user intent when generating SPEC.

This catches misunderstandings, hallucinations, and scope creep at the source before any other validation runs.

### Process

#### 1. Extract Requirements Tree from User Prompt

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

#### 2. Extract Requirements Tree from Generated SPEC

Same process, parse SPEC for requirements tree.

#### 3. Compare Trees

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

**Implementation:** `src/simdecisions/qce/tree_compare.py`

```python
from simdecisions.qce.tree_compare import compare_requirements_trees

result = compare_requirements_trees(
    user_prompt=user_spec,
    spec_text=spec_text,
    llm_adapter=None  # Optional: pass LLM adapter for extraction
)
```

#### 4. Diagnostic on Failure

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

#### 5. Healing Loop

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

#### 6. Human Escalation

**When max retries reached:**
```markdown
Gate 0 failed after 3 retries. Manual intervention needed.

User prompt:
[original prompt]

Generated SPEC:
[current SPEC]

Diagnostic:
[diagnostic message]

Please review and either:
1. Type 'approve' to override validation
2. Type 'edited' after manually editing SPEC
3. Type 'abort' to stop the task
```

**Human options:**
- **approve**: Override validation and proceed to Phase 0
- **edited**: User manually fixed SPEC, reload and proceed to Phase 0
- **abort**: Terminal failure, stop the entire process

#### 7. Success Criteria

```python
gate0.passed == True                  # All checks passed
gate0.coverage == 1.0                 # 100% coverage
len(gate0.missing) == 0               # No missing requirements
len(gate0.hallucinated) == 0          # No hallucinated requirements
len(gate0.orphans) == 0               # No orphaned children
gate0.embedding_similarity >= 0.85    # Semantic similarity threshold
```

**If Gate 0 FAILS after 3 retries → Human intervention required. Do NOT proceed to Phase 0 without approval.**

---

## Phase 0: Coverage Validation

### Purpose
Ensure SPEC covers 100% of mandatory requirements from ASSIGNMENT.

### Process

#### 1. Extract Requirements from ASSIGNMENT

Use LLM (Haiku or platform Llama) to extract structured requirements:

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

#### 2. Check Coverage in SPEC

For EACH requirement, use LLM to check if it's covered in SPEC:

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

#### 3. Generate Coverage Report

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

...
```

### Success Criteria

```python
# ALL of these must be true:
1. No violations (mandatory requirements declared out of scope)
2. No missing requirements
3. Coverage score = 1.0 (100%)
4. Partial coverage explicitly approved by human (if any)
```

### Healing Loop

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

**Human escalation prompt:**
```markdown
Phase 0 coverage validation failed after 3 retries. Manual intervention needed.

ASSIGNMENT:
[assignment text]

Generated SPEC:
[current SPEC]

Coverage Report:
[JSON report]

Please review and either:
1. Type 'approve' to override validation
2. Type 'edited' after manually editing SPEC
3. Type 'abort' to stop the task
```

**If Phase 0 FAILS after 3 retries → Escalate to human. Do NOT proceed to Phase 1 without approval.**

---

## Phase 1: SPEC Fidelity Validation

### Purpose
Ensure SPEC→IR encoding preserves semantic meaning.

### Process

#### 1. Encode SPEC to IR
Use LLM (Haiku or Sonnet) to convert SPEC to PHASE-IR format.

#### 2. Decode IR back to SPEC'
Use LLM to convert IR back to English specification.

#### 3. Compare with Voyage Embeddings
```python
spec_embedding = voyage_embed(spec_text)
spec_prime_embedding = voyage_embed(spec_prime_text)

fidelity = cosine_similarity(spec_embedding, spec_prime_embedding)
```

#### 4. Generate Fidelity Report

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

### Success Criteria

```python
fidelity >= 0.85  # With Voyage or TF-IDF embeddings (may raise to 0.90)
```

### Healing Loop

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

**Human escalation prompt:**
```markdown
Phase 1 SPEC fidelity validation failed after 3 retries. Manual intervention needed.

Original SPEC:
[original SPEC]

Reconstructed SPEC':
[reconstructed SPEC']

Fidelity Report:
[JSON with fidelity score]

Please review and either:
1. Type 'approve' to override validation
2. Type 'edited' after manually editing SPEC
3. Type 'abort' to stop the task
```

**If Phase 1 FAILS after 3 retries → Escalate to human. Do NOT proceed to Phase 2 without approval.**

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

### Success Criteria

```python
fidelity >= 0.85  # With Voyage or TF-IDF embeddings
```

### Healing Loop

**If Phase 2 validation fails:**

1. **Diagnose:** Fidelity score < 0.85, semantic meaning lost in round-trip
2. **Heal:** Call LLM with healing prompt:
   ```
   Phase 2 TASK fidelity validation failed. The round-trip TASKS→IR→TASKS' lost semantic meaning.

   Original TASKS:
   [original TASKS]

   Reconstructed TASKS':
   [reconstructed TASKS']

   Fidelity Score: [score]

   Regenerate TASKS that:
   1. Preserves all dependencies and relationships
   2. Makes task ordering explicit
   3. Preserves all implementation details
   4. Achieves fidelity ≥ 0.85
   5. Uses the same format with traceability IDs (TASK-NNN, SPEC-NNN, REQ-CAT-NNN)
   ```
3. **Retry:** Save healed TASKS, increment retry counter, re-run Phase 2 (encode→decode→compare)
4. **Escalate:** If retries ≥ 3 → Human intervention required

**Human escalation prompt:**
```markdown
Phase 2 TASK fidelity validation failed after 3 retries. Manual intervention needed.

Original TASKS:
[original TASKS]

Reconstructed TASKS':
[reconstructed TASKS']

Fidelity Report:
[JSON with fidelity score]

Please review and either:
1. Type 'approve' to override validation
2. Type 'edited' after manually editing TASKS
3. Type 'abort' to stop the task
```

**If Phase 2 FAILS after 3 retries → Escalate to human. Do NOT proceed to implementation without approval.**

---

## Traceability ID System

### ID Format

Every artifact gets a unique ID following this scheme:

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

### SPEC Format with IDs

```markdown
## Export Button Component
**ID:** SPEC-001
**Implements:** REQ-UI-001
**Category:** UI

The Export button appears in the canvas toolbar next to the zoom controls...

### Acceptance Criteria
- Button visible in toolbar
- Clicking button opens export dialog
- Icon uses Lucide Download icon
```

### TASK Format with IDs

```markdown
## TASK-001: Build Export Button Component
**ID:** TASK-001
**Implements:** SPEC-001
**Satisfies:** REQ-UI-001
**Assignee:** Haiku
**Complexity:** Simple

Create a new ExportButton.tsx component that renders a button in the toolbar.

### Files to Create
- simdecisions-2/src/components/buttons/ExportButton.tsx
- simdecisions-2/src/components/buttons/ExportButton.test.tsx

### Dependencies
- None (standalone component)
```

### Code Format with Traceability Comments

```typescript
// Implements: TASK-001 | Satisfies: REQ-UI-001
// File: simdecisions-2/src/components/buttons/ExportButton.tsx
export function ExportButton() {
  const { openExportDialog } = useUIStore();

  return (
    <button
      onClick={openExportDialog}
      className="toolbar-button"
      title="Export Scenario"
    >
      <Download size={20} />
    </button>
  );
}
```

### Test Format with Traceability Comments

```typescript
// Verifies: REQ-UI-001, REQ-UI-002
// File: simdecisions-2/src/components/buttons/ExportButton.test.tsx
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ExportButton } from './ExportButton';

describe('ExportButton', () => {
  // Verifies: REQ-UI-001
  it('renders export button in toolbar', () => {
    render(<ExportButton />);
    expect(screen.getByTitle('Export Scenario')).toBeInTheDocument();
  });

  // Verifies: REQ-UI-001
  it('opens export dialog on click', () => {
    // ... test implementation
  });
});
```

---

## Traceability Graph Structure

All IDs form a directed acyclic graph (DAG):

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

### Graph Schema

```typescript
interface TraceabilityGraph {
  nodes: TraceNode[];
  edges: TraceEdge[];
}

interface TraceNode {
  id: string;                    // REQ-UI-001, SPEC-001, etc.
  type: 'requirement' | 'spec' | 'task' | 'code' | 'test';
  data: {
    text?: string;               // Human-readable description
    file?: string;               // Source file path
    line?: number;               // Line number in file
    category?: string;           // UI, Backend, Security, etc.
    mandatory?: boolean;         // Is this required?
    embedding?: number[];        // Voyage embedding (1024 dimensions)
  };
}

interface TraceEdge {
  source: string;                // Parent node ID
  target: string;                // Child node ID
  type: 'implements' | 'breaks_into' | 'produces' | 'tested_by';
}
```

### Graph Queries

```python
# Find all code implementing UI requirements
ui_code = graph.query(
    start_type='requirement',
    category='UI',
    end_type='code'
)

# Find orphaned requirements (no downstream implementation)
orphans = graph.find_nodes(
    type='requirement',
    has_outgoing_edges=False
)

# Get full lineage for a requirement
lineage = graph.get_descendants('REQ-UI-001')
# Returns: [SPEC-001, TASK-001, CODE-001, TEST-001]
```

---

## Worker Bee Implementation Requirements

### Permission Mode

Worker bees MUST run with `dangerous=True` to bypass permission hooks:

```python
dispatch_bee(
    task=task,
    model="haiku",
    branch="main",
    dangerous=True,  # REQUIRED - bypasses file write hooks
    cwd="C:\Users\davee\OneDrive\Documents\GitHub\platform"
)
```

**Why:** Permission hooks block file writes in automated mode. `dangerous=True` disables hooks for autonomous execution.

### Traceability Comments

Every file MUST include traceability comments at the top:

```typescript
// Implements: TASK-{NNN} | Satisfies: REQ-{CAT}-{NNN}
// Phase: {phase_name}
// Assignee: {model_tier}
```

### Test Requirements

Every requirement MUST have at least one test that verifies it:

```typescript
// Verifies: REQ-{CAT}-{NNN}
it('test description matching acceptance criteria', () => {
  // ... test implementation
});
```

---

## File Naming Conventions

### Task Files
```
.deia/hive/tasks/YYYY-MM-DD-HHMM-{AGENT}-{TASK_ID}-ASSIGNMENT.md
.deia/hive/tasks/YYYY-MM-DD-HHMM-{AGENT}-{TASK_ID}-SPEC.md
.deia/hive/tasks/YYYY-MM-DD-HHMM-{AGENT}-{TASK_ID}-TASKS.md
```

### Response Files
```
.deia/hive/responses/YYYY-MM-DD-HHMM-{AGENT}-{TASK_ID}-PHASE0-REPORT.md
.deia/hive/responses/YYYY-MM-DD-HHMM-{AGENT}-{TASK_ID}-PHASE1-REPORT.md
.deia/hive/responses/YYYY-MM-DD-HHMM-{AGENT}-{TASK_ID}-PHASE2-REPORT.md
.deia/hive/responses/YYYY-MM-DD-HHMM-{AGENT}-{TASK_ID}-BEE-{N}-COMPLETION.md
```

### Archive on Completion
```
# Move completed task files to archive
mv .deia/hive/tasks/YYYY-MM-DD-HHMM-{AGENT}-{TASK_ID}-*.md \
   .deia/hive/tasks/_archive/
```

---

## Git Commit Format

After all phases pass and implementation completes, commit with full report:

```bash
git commit -m "$(cat <<'EOF'
{Feature Title} - Task {TASK_ID}

Phase 0: Coverage - PASS (100% coverage, 0 violations)
Phase 1: SPEC Fidelity - PASS (0.9128)
Phase 2: TASK Fidelity - PASS (0.9023)

Requirements Satisfied:
  - REQ-UI-001: Export Button
  - REQ-UI-002: Import Button
  - REQ-BE-001: JSON Export Format

Files Changed:
  - simdecisions-2/src/components/buttons/ExportButton.tsx (87 LOC)
  - simdecisions-2/src/components/buttons/ImportButton.tsx (91 LOC)
  - simdecisions-2/src/services/export/scenarioExport.ts (82 LOC)

Tests Added:
  - 8 tests covering all UI requirements
  - 12 tests covering backend validation

Co-Authored-By: {Agent Model} <noreply@anthropic.com>
EOF
)"
```

---

## Token & Cost Tracking (4 Currencies)

### MANDATORY: Track All LLM Calls BY MODEL

Every phase report and completion report MUST include token tracking broken down by model:

**Phase Report Format:**
```markdown
## Token Usage by Model

| Operation | Model | Input Tokens | Output Tokens | Total Tokens | Cost |
|-----------|-------|--------------|---------------|--------------|------|
| Extract requirements | Haiku | 1,200 | 450 | 1,650 | $0.0033 |
| Check coverage (10 reqs) | Haiku | 8,500 | 2,100 | 10,600 | $0.0212 |
| **TOTAL Phase 0** | - | **9,700** | **2,550** | **12,250** | **$0.0245** |

## Model Breakdown

| Model | Input | Output | Total | Cost |
|-------|-------|--------|-------|------|
| Haiku | 9,700 | 2,550 | 12,250 | $0.0245 |

## 3-Currency Analysis

| Currency | Value |
|----------|-------|
| Clock | 5s |
| Cost | $0.0245 |
| Carbon | ~0.5g CO2 |
```

**Completion Report Format:**
```markdown
## Token Summary by Phase

| Phase | Input | Output | Total | Cost |
|-------|-------|--------|-------|------|
| Phase 0 | 9,700 | 2,550 | 12,250 | $0.0245 |
| Phase 1 | 5,200 | 1,800 | 7,000 | $0.0140 |
| Phase 2 | 6,500 | 2,200 | 8,700 | $0.0174 |
| Workers | 42,000 | 18,500 | 60,500 | $0.1210 |
| **TOTAL** | **63,400** | **25,050** | **88,450** | **$0.1769** |

## Token Summary by Model

| Model | Input | Output | Total | Cost | % of Total Cost |
|-------|-------|--------|-------|------|-----------------|
| Haiku | 48,200 | 19,500 | 67,700 | $0.0677 | 38% |
| Sonnet | 15,200 | 5,550 | 20,750 | $0.1038 | 59% |
| Voyage (embeddings) | - | - | - | $0.0054 | 3% |
| **TOTAL** | **63,400** | **25,050** | **88,450** | **$0.1769** | **100%** |

## 3-Currency Analysis

| Currency | Total |
|----------|-------|
| Clock | 143s (2.4m) |
| Cost | $0.1769 |
| Carbon | ~18g CO2 |
```

### Per Build (avg 10 requirements, 5 tasks)

**By Phase:**

| Phase | Input | Output | Total | Clock | Cost | Carbon |
|-------|-------|--------|-------|-------|------|--------|
| Phase 0 | ~10k | ~2.5k | ~12k | ~5s | $0.0043 | ~0.5g |
| Phase 1 | ~5k | ~2k | ~7k | ~8s | $0.0032 | ~0.8g |
| Phase 2 | ~7k | ~2k | ~9k | ~10s | $0.0048 | ~1.0g |
| Workers | ~40k | ~18k | ~58k | ~120s | $0.07 | ~10g |
| **TOTAL** | **~62k** | **~24.5k** | **~86k** | **~143s** | **$0.08** | **~12g** |

**By Model:**

| Model | Input | Output | Total | Cost | % of Total |
|-------|-------|--------|-------|------|------------|
| Haiku (Q33N + Workers) | ~48k | ~19k | ~67k | $0.067 | 84% |
| Sonnet (Complex Tasks) | ~14k | ~5.5k | ~19k | $0.010 | 12% |
| Voyage (Embeddings) | - | - | - | $0.003 | 4% |
| **TOTAL** | **~62k** | **~24.5k** | **~86k** | **$0.08** | **100%** |

**Note:** If using Vercel AI SDK, OpenAI API, Gemini API, or other cloud LLM providers, break down tokens by provider and model.

**ROI:** 8 cents and 86k tokens prevents dropped requirements that could cost hours of rework.

---

## Error Handling

### Phase 0 Failure Example

```markdown
# Phase 0: Coverage Validation

## Summary
- Total Requirements: 10
- Covered: 8 (80%)
- Missing: 0 (0%)
- Out of Scope (Violations): 2 (20%)

## Status: FAIL

## Violations

### REQ-UI-001: Export Button
- **Status:** OUT_OF_SCOPE
- **Issue:** Mandatory UI requirement declared out of scope at line 92
- **Evidence:** "Out of Scope: Modifying existing ExportDialog.tsx"
- **Action Required:** Add Export Button component to SPEC

### REQ-UI-002: Import Button
- **Status:** OUT_OF_SCOPE
- **Issue:** Mandatory UI requirement declared out of scope at line 92
- **Evidence:** "Out of Scope: Modifying existing ImportDialog.tsx"
- **Action Required:** Add Import Button component to SPEC

## Next Steps

1. Rewrite SPEC to include REQ-UI-001 and REQ-UI-002
2. Rerun Phase 0 validation
3. Proceed to Phase 1 only if coverage = 100%
```

**Action:** Return SPEC to queen or spec writer. Do NOT proceed.

### Phase 1/2 Failure Example

```markdown
# Phase 1: SPEC Fidelity Validation

**Fidelity:** 0.72
**Threshold:** 0.85
**Status:** FAIL

## Issue

Round-trip validation shows semantic drift:
- Original SPEC mentions "real-time updates via WebSocket"
- Reconstructed SPEC' dropped "real-time" concept entirely
- Lost concept: streaming, live updates, push notifications

## Next Steps

1. Review IR encoding for WebSocket/streaming concepts
2. Retry with different model (Sonnet instead of Haiku)
3. Add explicit IR nodes for real-time requirements
4. Rerun Phase 1 validation
```

**Action:** Iterate on IR encoding. Do NOT proceed to Phase 2.

---

## Success Criteria Summary

```python
# Build is READY FOR IMPLEMENTATION when:
gate_0.passed == True           # Prompt→SPEC interpretation correct (100% coverage, no hallucinations)
phase_0.passed == True          # 100% coverage, 0 violations
phase_1.fidelity >= 0.85        # SPEC→IR→SPEC' preserves meaning
phase_2.fidelity >= 0.85        # TASKS→IR→TASKS' preserves meaning

# Only then dispatch worker bees with dangerous=True
```

## Healing Loop Summary

All gates and phases follow the same healing pattern:

1. **Validate:** Run validation checks
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

## References

- **Q33N-003B Case Study:** `.deia/hive/responses/2026-02-25-Q33N-003B-COMPLETION.md`
- **Quality & Compliance Engine Spec:** `_outbox/2026-02-25-QUALITY-COMPLIANCE-ENGINE-SPEC.md`
- **Session Traceability Breakthrough:** `_outbox/2026-02-25-SESSION-TRACEABILITY-BREAKTHROUGH.md`
- **Railway Integration Spec:** `_outbox/2026-02-25-RAILWAY-HIVE-INTEGRATION-SPEC.md`

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-25 | Initial process documentation |

---

**END OF PROCESS-0013**
