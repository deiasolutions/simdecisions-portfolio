# PLAN: IR Density Measurement Implementation

**Date:** 2026-04-06  
**Source:** BRIEFING-IR-DENSITY-MEASUREMENT.md + PROCESS-DOC-DRIVEN-DEVELOPMENT.md + SPEC-IRD-DEDS-METRICS-FRAMEWORK.md  
**Status:** READY FOR DISPATCH

---

## Summary

Implement IR Density measurement as a quality metric for **two document types**:

1. **Hive specs** (SPEC-*.md, TASK-*.md, IMPL-*.md) — acceptance criteria, file paths, code blocks
2. **PRISM-IR process definitions** (*.prism.md, *.ir.yaml) — nodes, actions, guards, SLAs

Integrated with:
- **Gate 0** — density check before dispatch (spec mode)
- **Doc-driven development** — density check on IMPL docs before QA review
- **PRISM-IR validation** — density check on process definitions
- **Calibration ledger** — correlate density with build outcomes

---

## Dual-Mode Scoring

### Mode Detection

```python
def detect_doc_type(text: str) -> str:
    """Auto-detect document type for scoring."""
    # PRISM-IR markers (YAML process definitions)
    if re.search(r'^v:\s*["\']?\d', text, re.MULTILINE) and (
        'nodes:' in text or 'Process:' in text or 'flow:' in text
    ):
        return "prism"
    # Hive spec markers (markdown specs)
    if '## Acceptance Criteria' in text or '## Smoke Test' in text or '## Objective' in text:
        return "spec"
    return "unknown"
```

### Mode: `spec` (Hive SPEC/TASK/IMPL files)

**Executable elements:**

| Element | How to count |
|---------|--------------|
| Acceptance criteria | `- [ ]` or `- [x]` checkbox count |
| Deliverables | Bullet points under `## Deliverables` |
| Smoke test commands | Code blocks or bullets under `## Smoke Test` |
| File paths | Matches to path patterns (`/path/to/file.py`, `src/...`) |
| Code blocks | Fenced code block count |
| Schema lines | Lines inside code blocks |
| Constraint items | Bullets under `## Constraints` |

**Sub-metrics (spec mode):**

```python
instruction_density = (acceptance_criteria + deliverables + smoke_tests) / total_lines
reference_density = (file_paths + code_block_lines) / total_lines
constraint_clarity = sections_present / expected_sections  # 7 expected
```

**Expected sections (spec mode):**
1. Priority
2. Depends On (or Dependencies)
3. Model Assignment (or Model)
4. Objective
5. Acceptance Criteria
6. Smoke Test
7. Constraints

**Composite (spec mode, Phase 1):**

```python
ir_density_spec = 0.40 * instruction_density + 0.30 * reference_density + 0.30 * constraint_clarity
```

**Benchmarks (spec mode):**

| Score | Rating | Action |
|-------|--------|--------|
| < 0.2 | Poor | Block dispatch |
| 0.2-0.4 | Weak | Warn, recommend revision |
| 0.4-0.6 | Acceptable | Proceed |
| 0.6-0.8 | Good | Proceed |
| > 0.8 | Excellent | Proceed, flag as exemplar |

---

### Mode: `prism` (PRISM-IR Process Definitions)

**Executable elements (from SPEC-IRD-DEDS):**

| Category | Examples | Weight |
|----------|----------|--------|
| Nodes | task, fork, join, end, start | 1.0 |
| Actions | set, emit, require, cancel | 1.0 |
| Conditions | guards (`g:`), edge conditions (`c:`) | 1.0 |
| SLAs | `sla:` with breach handlers | 1.0 |
| Resources | pool definitions with capacity/skills | 1.0 |
| Timings | duration distributions | 1.0 |
| Events | emit, trigger definitions | 1.0 |
| Entity attrs | typed attributes in schema | 0.5 |
| Lifecycle states | states in entity lifecycle | 0.5 |
| Generators | arrival patterns | 1.0 |
| Join policies | mode, lineageFrom | 1.0 |
| Constraints | top-level constraints | 1.0 |

**Calculation (prism mode):**

```python
def estimate_tokens(text: str) -> int:
    """Phase 1: simple approximation (~10-15% variance from tiktoken)."""
    return len(text) // 4

def calculate_ird_prism(text: str) -> dict:
    tokens = estimate_tokens(text)
    kilotokens = tokens / 1000
    elements = count_prism_elements(text)  # weighted sum
    ird = elements / kilotokens if kilotokens > 0 else 0
    return {
        "tokens": tokens,
        "kilotokens": kilotokens,
        "elements": elements,
        "ird": ird,
        "rating": get_ird_rating(ird)
    }

def get_ird_rating(ird: float) -> str:
    if ird < 10: return "verbose"
    if ird < 20: return "acceptable"
    if ird < 30: return "efficient"
    return "optimal"
```

**Benchmarks (prism mode):**

| IRD | Rating | Interpretation |
|-----|--------|----------------|
| < 10/kt | Verbose | Excess boilerplate, needs compression |
| 10-20/kt | Acceptable | Functional but room for improvement |
| 20-30/kt | Efficient | Well-authored specification |
| > 30/kt | Optimal | Highly optimized, minimal waste |

**Reference comparisons:**

| Format | Typical IRD | Notes |
|--------|-------------|-------|
| BPMN XML | 5-10/kt | XML ceremony, no action language |
| PRISM-IR | 20-30/kt | YAML compact, actions inline |
| English prose | 2-5/kt | Ambiguous, not executable |

---

## Integration Points

### Where IR Density Fits in the Build Cycle

```
SPEC-*.md                           IMPL-*.md                    *.prism.md
    │                                   │                            │
    ▼                                   ▼                            ▼
┌──────────────────┐            ┌──────────────────┐          ┌──────────────────┐
│  IR DENSITY      │            │  IR DENSITY      │          │  IR DENSITY      │
│  mode: spec      │            │  mode: spec      │          │  mode: prism     │
│                  │            │                  │          │                  │
│  Gate 0 check    │            │  Schema check    │          │  Process check   │
│  Warn < 0.4      │            │  before QA bee   │          │  Warn < 10/kt    │
│  Block < 0.2     │            │  gets task       │          │  Block < 5/kt    │
└──────────────────┘            └──────────────────┘          └──────────────────┘
         │                               │                            │
         ▼                               ▼                            ▼
    DISPATCHER                      BEE-QA-*                   PRISM Validator
```

### Data Flow

```
ir_density.py score SPEC-MW-011.md
    │
    ├── mode: spec (auto-detected)
    ├── instruction_density: 0.81
    ├── reference_density: 0.68
    ├── constraint_clarity: 0.86
    ├── composite: 0.78
    │
    ▼
inv_estimates (new column: ir_density)

ir_density.py score loan-approval.prism.md
    │
    ├── mode: prism (auto-detected)
    ├── tokens: 1250
    ├── kilotokens: 1.25
    ├── elements: 32
    ├── ird: 25.6
    ├── rating: efficient
    │
    ▼
process_registry (new column: ird)
```

---

## Decisions (per briefing + this session)

| Question | Decision | Rationale |
|----------|----------|-----------|
| Weight `ir_cost_efficiency` in Phase 1? | **No** — set to 0 | No actuals yet. Redistribute to other 3. |
| Gate 0 density check: block or warn? | **Warn initially** | Calibrate threshold from real data first. |
| Score TASK files too? | **Yes** | Same sections as SPEC. Both get scored. |
| Score IMPL files? | **Yes** | Quality gate before QA bee review. |
| Score PRISM-IR files? | **Yes** | Dual-mode scorer. Auto-detect. |
| Tokenizer for PRISM mode? | **chars/4 approximation** | No external dependency. Within 10-15% accuracy. Upgrade to tiktoken in Phase 2 if needed. |
| Backfill timing? | **After process tested** | Don't create IMPL docs for a pipeline that doesn't exist yet. |

---

## Phased Rollout

**Do not change the pipeline mid-MW-build.** IR Density scorer is standalone first.

| Phase | When | What | Tasks |
|-------|------|------|-------|
| **0** | Now (tonight's build) | Standalone scorer + Gate 0 warning | IRD-01, IRD-02 |
| **1** | After MW build completes | Create doc directories, add IMPL requirement to template, manual QA | IRD-04, doc-driven dev setup |
| **2** | After Phase 1 stable | QA bee automation, state machine changes, scheduler integration | Full PROCESS-DOC-DRIVEN-DEV |
| **3** | After Phase 2 stable | Backfill historical tasks, correlate with actuals, tune thresholds | IRD-03, backfill batch |

**Tonight's scope:** IRD-01 and IRD-02 only. Everything else deferred.

---

## CLI Design

```bash
# Auto-detect mode, score single file
python _tools/ir_density.py score path/to/file.md

# Force mode
python _tools/ir_density.py score path/to/file.md --mode spec
python _tools/ir_density.py score path/to/file.md --mode prism

# Batch score directory
python _tools/ir_density.py batch .deia/hive/queue/backlog/
python _tools/ir_density.py batch prism_specs/ --mode prism

# Gate check (for CI/dispatch integration)
python _tools/ir_density.py gate-check SPEC-MW-011.md --min-density 0.4
python _tools/ir_density.py gate-check loan.prism.md --min-ird 10

# Correlate with build outcomes (Phase 2)
python _tools/ir_density.py correlate

# Output formats
python _tools/ir_density.py batch .deia/hive/ --format table   # default
python _tools/ir_density.py batch .deia/hive/ --format json
python _tools/ir_density.py batch .deia/hive/ --format csv
```

**Output example (spec mode):**

```
IR Density Report (spec mode)
═══════════════════════════════════════════════════════════════
File                          Instr   Ref    Clarity  Composite
───────────────────────────────────────────────────────────────
SPEC-MW-011-mobile-nav.md     0.81    0.68   0.86     0.78 ████████
SPEC-MW-012-tree-browser.md   0.65    0.72   0.71     0.69 ███████
SPEC-MW-013-dashboard.md      0.42    0.31   0.57     0.43 ████
SPEC-MW-014-terminal.md       0.18    0.12   0.43     0.24 ██ ⚠️ WEAK
───────────────────────────────────────────────────────────────
Average: 0.54    Min: 0.24    Max: 0.78
```

**Output example (prism mode):**

```
IR Density Report (prism mode)
═══════════════════════════════════════════════════════════════
File                          Tokens   Elements   IRD/kt   Rating
───────────────────────────────────────────────────────────────
loan-approval.prism.md        1250     32         25.6     efficient
order-processing.prism.md     890      28         31.5     optimal
user-onboarding.prism.md      2100     18         8.6      verbose ⚠️
───────────────────────────────────────────────────────────────
Average: 21.9 IRD/kt
```

---

## Task Breakdown

### TASK-IRD-01: Core Scorer (Dual-Mode)

**Priority:** P1  
**Model:** sonnet  
**Depends on:** None  
**Estimated:** 60 min

**Objective:**  
Create `_tools/ir_density.py` with dual-mode scoring (spec + prism).

**Deliverables:**
- `_tools/ir_density.py` — main CLI and scoring logic
- `_tools/tests/test_ir_density.py` — TDD tests

**Acceptance Criteria:**
- [ ] `detect_doc_type(text)` returns "spec" | "prism" | "unknown"
- [ ] `score_spec(text)` returns dict with instruction/reference/clarity/composite
- [ ] `score_prism(text)` returns dict with tokens/elements/ird/rating
- [ ] `score(text)` auto-detects mode and delegates
- [ ] CLI: `ir_density.py score <file>` works for both types
- [ ] CLI: `--mode spec|prism` forces mode
- [ ] Validate on 5+ real spec files, 3+ real PRISM files
- [ ] No LLM calls — pure static analysis
- [ ] Token estimation via chars/4 (no external dependencies)

**Smoke Test:**
```bash
# Spec mode
python _tools/ir_density.py score .deia/hive/queue/backlog/SPEC-MW-011.md
# Expected: mode: spec, composite: 0.XX

# PRISM mode
python _tools/ir_density.py score examples/loan-approval.prism.md
# Expected: mode: prism, ird: XX.X, rating: efficient
```

**Constraints:**
- Match `inventory.py` CLI pattern (argparse, subcommands)
- File < 400 lines (both modes)
- TDD: tests first
- No external dependencies (use chars/4 for token estimation)

**Files to create:**
- `_tools/ir_density.py`
- `_tools/tests/test_ir_density.py`

**Files to read:**
- `.deia/hive/scripts/queue/spec_parser.py` — existing section parsing
- `docs/specs/2026-02-23-SPEC-IRD-DEDS-METRICS-FRAMEWORK.md` — original IRD spec
- `github.com/deiasolutions/prism-ir/SPEC.md` — PRISM-IR element definitions

---

### TASK-IRD-02: Batch Scoring + Gate 0 Integration

**Priority:** P1  
**Model:** sonnet  
**Depends on:** TASK-IRD-01  
**Estimated:** 30 min

**Objective:**  
Add batch scoring and Gate 0 density check.

**Deliverables:**
- `ir_density.py batch` command
- `ir_density.py gate-check` command
- Gate 0 hook in `gate0.py`

**Acceptance Criteria:**
- [ ] `batch <dir>` scores all matching files, outputs table
- [ ] `batch --format json|csv` for machine consumption
- [ ] `gate-check <file> --min-density 0.4` returns exit code 0 (pass) or 1 (fail)
- [ ] `gate-check <file> --min-ird 10` works for prism mode
- [ ] Gate 0 calls density check as 6th validation step
- [ ] Warn if density < 0.4 (spec) or IRD < 10 (prism)
- [ ] Block if density < 0.2 (spec) or IRD < 5 (prism)
- [ ] Thresholds configurable via flags

**Smoke Test:**
```bash
python _tools/ir_density.py batch .deia/hive/queue/backlog/
# Expected: table of specs with density scores

python _tools/ir_density.py gate-check .deia/hive/queue/backlog/SPEC-MW-011.md --min-density 0.4
# Expected: exit code 0 if >= 0.4, exit code 1 if < 0.4
```

**Constraints:**
- No changes to spec file format
- Thresholds are soft defaults, configurable

**Files to modify:**
- `_tools/ir_density.py` (add batch, gate-check)
- `.deia/hive/scripts/queue/gate0.py` (add density check)

---

### TASK-IRD-03: Calibration Ledger Integration

**Priority:** P2  
**Model:** sonnet  
**Depends on:** TASK-IRD-01, EST-02 (calibration ledger)  
**Estimated:** 30 min  
**Status:** DEFERRED — Phase 3 (after MW build + doc-driven dev stable)

**Objective:**  
Record IR density in inv_estimates, enable correlation analysis.

**Deliverables:**
- New column `ir_density` in inv_estimates
- `ir_density.py correlate` command

**Acceptance Criteria:**
- [ ] `inv_estimates` table has `ir_density REAL` column
- [ ] Dispatcher records density at dispatch time
- [ ] `correlate` command outputs: density vs cost_delta, density vs fidelity
- [ ] Correlation coefficient and scatter plot data

**Smoke Test:**
```bash
python _tools/ir_density.py correlate
# Expected: correlation table (requires 30+ tasks with actuals)
```

**Constraints:**
- Requires calibration ledger data (EST-02 dependency)
- Requires 30+ tasks with actuals before meaningful correlation

**Files to modify:**
- `hivenode/inventory/store.py` — add ir_density column
- `_tools/ir_density.py` — add correlate command
- `.deia/hive/scripts/queue/dispatcher.py` — record density at dispatch

---

### TASK-IRD-04: IMPL Doc Density Gate

**Priority:** P1  
**Model:** sonnet  
**Depends on:** TASK-IRD-01, PROCESS-DOC-DRIVEN-DEVELOPMENT implementation  
**Estimated:** 20 min  
**Status:** DEFERRED — Phase 1 (after MW build completes)

**Objective:**  
Add density check to IMPL doc validation before QA bee review.

**Deliverables:**
- Density check in doc-validator flow
- Low-density IMPL docs flagged for revision

**Acceptance Criteria:**
- [ ] IMPL docs scored before QA bee assignment
- [ ] Density < 0.3 → task stays in `_code_complete/`, build bee prompted to add detail
- [ ] Density >= 0.3 → proceeds to QA bee
- [ ] Density recorded in IMPL frontmatter

**Smoke Test:**
```bash
# Simulate: IMPL doc with minimal content
python _tools/ir_density.py gate-check .deia/docs/impl/IMPL-TEST-001.md --min-density 0.3
# Expected: FAIL if sparse, PASS if sufficient
```

**Constraints:**
- Requires PROCESS-DOC-DRIVEN-DEVELOPMENT to be implemented first
- Threshold lower than SPEC (0.3 vs 0.4) — IMPL docs are shorter

**Files to modify:**
- Queue-runner or doc-validator hook (doesn't exist yet)
- `_tools/ir_density.py` (if needed)

---

## File Structure

```
_tools/
├── ir_density.py              # Main CLI + scoring logic
├── tests/
│   └── test_ir_density.py     # TDD tests
└── fixtures/
    ├── spec_high_density.md   # Test fixture
    ├── spec_low_density.md    # Test fixture
    ├── prism_efficient.yaml   # Test fixture
    └── prism_verbose.yaml     # Test fixture
```

---

## Open Items

1. ~~**tiktoken dependency**~~ — RESOLVED: Using chars/4 approximation. No external dependency.
2. **PRISM-IR test files** — Need 3+ real .prism.md files for validation. Pull from prism-ir repo examples.
3. **Threshold calibration** — Initial values are estimates. Revisit after 30+ scored tasks (Phase 3).
4. ~~**Backfill timing**~~ — RESOLVED: Wait until process tested (Phase 3).

---

## Tonight's Dispatch

**Only these tasks go to backlog tonight:**

| Task | Priority | Est | Status |
|------|----------|-----|--------|
| TASK-IRD-01 | P1 | 60 min | READY |
| TASK-IRD-02 | P1 | 30 min | READY (depends on IRD-01) |

**Deferred:**

| Task | Phase | Blocker |
|------|-------|---------|
| TASK-IRD-03 | Phase 3 | EST-02 + 30 tasks with actuals |
| TASK-IRD-04 | Phase 1 | MW build complete + doc-driven dev implemented |

---

## References

- `docs/specs/2026-02-23-SPEC-IRD-DEDS-METRICS-FRAMEWORK.md` — Original IRD/DEDS spec
- `2026-04-06-BRIEFING-IR-DENSITY-MEASUREMENT.md` — Hive spec adaptation
- `PROCESS-DOC-DRIVEN-DEVELOPMENT.md` — Doc-driven development flow
- `github.com/deiasolutions/prism-ir` — PRISM-IR spec (element definitions)
