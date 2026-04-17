# TASK-SURVEY-FACTORY-GAP-MATRIX

**Task ID:** TASK-SURVEY-FACTORY-GAP-MATRIX
**Created:** 2026-04-10
**Author:** Q33NR
**Assigned to:** BEE (Sonnet)
**Model:** sonnet
**Role:** bee
**Priority:** P0
**Blocks:** TASK-SIMDECISIONS-SCAFFOLD, BRIEFING-SIMDECISIONS-HANDOFF
**Status:** READY

---

## YOUR ROLE

You are a **bee**. Research only. You do NOT modify any files. You do NOT write code. You read, catalogue, and report.

---

## Intent

Survey the `shiftcenter` repo and produce a complete gap matrix: every spec mapped to its implementation and test, with IRE status for each. This matrix is the source of truth for what `simdecisions` inherits and what it must build.

---

## Survey Scope — Read These In Order

### 1. Specs
Read every file under `docs/specs/`. For each file, extract:
- Spec ID (from frontmatter or filename)
- Title
- Stated acceptance criteria (copy verbatim if under 10 lines; summarize if longer)
- Any `status:` frontmatter field

### 2. Implementations
Read `src/simdecisions/` recursively. For each `.py` file, extract:
- File path
- Which spec ID it implements (look for spec references in comments or docstrings)
- Key classes/functions defined

### 3. Tests
Read `tests/` recursively. For each test file, extract:
- File path
- Which implementation file it tests
- Test function names
- Last known pass/fail (run `pytest <file> --tb=no -q` and capture output)

### 4. Engine
Read:
- `engine/des/engine.py` — note all node types handled
- `engine/des/core.py` — event loop coverage
- `engine/phase_ir/schema.py` — valid `op:` types
- `engine/phase_ir/validation.py` — validation rules

### 5. Hive Infrastructure
Read:
- `src/simdecisions/adapters/cli/dispatch.py`
- `src/simdecisions/adapters/cli/run_queue.py`
- `hivenode/adapters/cli/claude_cli_subprocess.py`
- `.deia/config/injections/base.md`
- `.deia/config/injections/claude_code.md`

Report: does each file exist? Line count? Key functions?

### 6. Completed Tasks
Read `.deia/hive/tasks/_archive/` — list all archived task IDs.
Read `.deia/hive/responses/` — list all response files. Cross-reference with spec list to identify which specs have completed task evidence.

---

## Gap Matrix — Required Output Format

Write the gap matrix as a markdown table with these exact columns:

```
| spec_id | spec_file | has_impl | impl_file | has_test | test_file | test_passes | ire_status | priority |
```

**ire_status values:**
- `IRE` — impl exists + test exists + test passes
- `IR-NO-IMPL` — spec exists, no implementation found
- `IR-NO-TEST` — impl exists, no test found
- `IR-TEST-FAIL` — impl exists, test exists, test fails
- `DEFERRED` — spec frontmatter contains `status: DEFERRED` or equivalent
- `UNKNOWN` — cannot determine from available files (explain in notes)

**priority values** (for non-IRE items only):
- `P0` — factory infrastructure (dispatch, queue, scheduler, boot)
- `P1` — engine core (node types, DES loop, IR schema)
- `P2` — adapter layer
- `P3` — feature layer

---

## Required Output Sections

Your response file MUST contain all of the following:

### Section 1: Files Read
List every file you read with path and line count. No guessing — only report files you actually read.

### Section 2: Gap Matrix
Full table as specified above. Every spec gets a row. No omissions.

### Section 3: IRE Items (inherit list)
List of all `IRE` items with their impl and test file paths. This is the copy list for Phase 1.

### Section 4: IR Closure Items by Priority
Grouped by P0/P1/P2/P3. Each item: spec_id, what's missing, estimated bee-hours.

### Section 5: Hive Infrastructure Status
For each of the 5 hive files surveyed: exists? (yes/no), line count, key functions, test coverage (yes/no).

### Section 6: Summary Counts
```
Total specs:          N
IRE:                  N
IR-NO-IMPL:           N
IR-NO-TEST:           N
IR-TEST-FAIL:         N
DEFERRED:             N
UNKNOWN:              N
```

### Section 7: Clock / Coin / Carbon
All three. Measured actuals. Never omit.

---

## Constraints

- RESEARCH ONLY — do not modify any file in `shiftcenter`
- If a file does not exist, write `FILE NOT FOUND` — do not guess
- Run pytest only in `--tb=no -q` mode to capture pass/fail without noise
- Do not interpret or editorialize — report what the files say
- If you cannot determine a field, write `UNKNOWN` and explain why

---

## Response File

Write your complete response to:
```
.deia/hive/responses/20260411-FACTORY-GAP-MATRIX.md
```

---

## Smoke Test

```bash
test -f .deia/hive/responses/20260411-FACTORY-GAP-MATRIX.md && echo "EXISTS" || echo "MISSING"
grep -c "| IRE |" .deia/hive/responses/20260411-FACTORY-GAP-MATRIX.md
grep -c "| IR-NO-IMPL |" .deia/hive/responses/20260411-FACTORY-GAP-MATRIX.md
```

---

*TASK-SURVEY-FACTORY-GAP-MATRIX — Q33NR — 2026-04-10*
