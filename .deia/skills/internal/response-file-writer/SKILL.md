---
name: response-file-writer
description: >-
  Write properly formatted bee response files after completing a task,
  following the mandatory 8-section format with Clock/Coin/Carbon reporting,
  acceptance criteria marking, and test results. Use when finishing any
  bee task, reporting completion to Q33N, or documenting work outcomes.
license: Proprietary
compatibility: Requires access to .deia/hive/responses/ directory
metadata:
  author: Q88N
  version: "1.0"
  deia:
    cert_tier: 3
    carbon_class: none
    requires_human: false
---

# Response File Writer

## Steps

### Step 1: Determine Response File Name

Response files follow this naming convention:

```
YYYYMMDD-{TASK-ID}-RESPONSE.md
```

Examples:
- `20260412-TASK-042-RESPONSE.md`
- `20260315-BUILD-QUEUE-CORE-RESPONSE.md`

**Rules:**
- Use ISO date format YYYYMMDD (no hyphens)
- TASK-ID should match the task file you're responding to
- Always end with `-RESPONSE.md`
- Save to `.deia/hive/responses/` directory

### Step 2: Write Header Section (Section 1 of 8)

Start with status, model used, and date:

```markdown
# {Task ID}: {Title} -- {STATUS}

**Status:** COMPLETE | FAILED (reason)
**Model:** Haiku | Sonnet | Opus
**Date:** YYYY-MM-DD
**Bot ID:** BEE-{timestamp}-{task-id} (if applicable)
```

**Status values:**
- `COMPLETE` — all acceptance criteria met, tests pass
- `FAILED (blocked by X)` — specify blocker
- `FAILED (tests failing)` — tests written but not passing
- `FAILED (missing dependencies)` — missing libraries, files, etc.

### Step 3: Write Files Modified Section (Section 2 of 8)

List every file you created or modified with absolute paths:

```markdown
---

## Files Modified

**Files created:**
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\path\to\new_file.py` (127 LOC)
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\path\to\test_file.py` (85 LOC)

**Files modified:**
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\path\to\existing.py` (added 42 lines)

**Files deleted:**
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\path\to\obsolete.py`
```

**Rules:**
- Use absolute paths (same as in task file)
- Include line counts for new files
- Specify what changed for modified files
- If no files were deleted, omit that subsection

### Step 4: Write What Was Done Section (Section 3 of 8)

Bullet list of concrete changes, not intent:

```markdown
---

## What Was Done

- Implemented `calculate_total()` function in `billing.py` with tax calculation logic
- Added 12 unit tests covering normal cases, edge cases (zero amount, negative tax), and error paths
- Modified `main.py` to import and call `calculate_total()`
- Refactored `format_currency()` helper to accept optional locale parameter
- Fixed TypeScript error in `BillingPane.tsx` by updating prop interface
```

**Anti-patterns:**
- ✗ "Worked on the billing feature"
- ✗ "Implemented requirements"
- ✗ "Fixed bugs"

**Good patterns:**
- ✓ "Implemented X function with Y logic"
- ✓ "Added N tests covering [scenarios]"
- ✓ "Fixed [specific error] by [specific change]"

### Step 5: Write Test Results Section (Section 4 of 8)

Report test counts, pass/fail, and coverage:

```markdown
---

## Test Results

**Tests written:** 12
**Tests passing:** 12
**Tests failing:** 0
**Coverage:** 87% (lines), 92% (branches)

### Test Scenarios Covered
- Normal billing calculation (positive amounts, valid tax rates)
- Edge cases: zero amount, 0% tax, 100% tax
- Error cases: negative amount, invalid tax rate, missing currency
- Integration: end-to-end billing flow from cart to invoice

### Test Files
- `tests\hivenode\billing\test_calculate_total.py` (12 tests)
```

**If tests are failing:**
```markdown
## Test Results

**Tests written:** 12
**Tests passing:** 10
**Tests failing:** 2

### Failing Tests
1. `test_negative_tax_rate` — AssertionError: expected ValueError, got None
2. `test_currency_conversion` — KeyError: 'EUR' in conversion table

### Root Cause
Currency conversion table incomplete. EUR, GBP, JPY missing.

### Next Steps
Add currency conversion rates or mark as FAILED with blocker.
```

### Step 6: Write Build Verification Section (Section 5 of 8)

Report whether build/lint/type-check passed:

```markdown
---

## Build Verification

**pytest:** PASS (12/12 tests passing)
**mypy:** PASS (no type errors)
**npm run build:** PASS (bundle size: 2.3 MB)
**eslint:** PASS (0 errors, 0 warnings)

No build errors detected.
```

**If build failed:**
```markdown
## Build Verification

**pytest:** FAIL (2/12 tests failing — see Test Results)
**mypy:** PASS
**npm run build:** FAIL

### Build Errors
```
ERROR in BillingPane.tsx:42:18
TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.
```

### Status
Marking task as FAILED (build errors).
```

### Step 7: Write Acceptance Criteria Section (Section 6 of 8)

Copy acceptance criteria from task file. Mark each with [x] or [ ]:

```markdown
---

## Acceptance Criteria

- [x] `calculate_total()` function implemented with tax logic
- [x] All tests pass (12/12 passing, 87% coverage)
- [x] No TypeScript errors
- [x] No hardcoded colors (CSS vars only)
- [ ] Build passes locally — **FAILED:** TS2345 error in BillingPane.tsx (see Build Verification)
- [x] Response file written with all 8 sections
```

**Rules:**
- If criterion is met: `[x]` with no explanation needed
- If criterion is NOT met: `[ ]` with explanation after `—`
- Never mark `[x]` if the criterion actually failed
- Never omit a criterion from the task file

### Step 8: Write Three Currencies Section (Section 7 of 8)

Report actual time, cost, and carbon consumed:

```markdown
---

## Three Currencies (Clock, Coin, Carbon)

| Currency | Estimate | Actual | Delta |
|----------|----------|--------|-------|
| Clock | 45 minutes | 52 minutes | +7 min |
| Coin | $0.08 USD | $0.11 USD | +$0.03 |
| Carbon | ~5g CO₂e | ~7g CO₂e | +2g |

**Model used:** Claude Sonnet 4.5
**Tokens:** 18,200 input, 4,500 output
**Cache hits:** 12,800 tokens (70% hit rate)
```

**ALL THREE currencies are mandatory.** Never skip one.

**Cost calculation:**
- Sonnet: $3/M input, $15/M output
- Haiku: $0.25/M input, $1.25/M output
- Opus: $15/M input, $75/M output

**Carbon estimation:**
- Light task (< 20k tokens): ~5g
- Medium task (20k-100k tokens): ~15g
- Heavy task (> 100k tokens): ~50g

### Step 9: Write Blockers / Follow-ups Section (Section 8 of 8)

Document issues, deferred work, or next steps:

```markdown
---

## Blockers / Follow-ups

**None.** Task completed successfully.
```

**If there are blockers:**
```markdown
## Blockers / Follow-ups

### Blockers
- Currency conversion table incomplete (EUR, GBP, JPY missing) — blocks `test_currency_conversion`
- Requires Q88N approval to add third-party API for live exchange rates

### Deferred Work
- Performance optimization for large invoices (> 1000 line items) — not in scope for this task

### Next Steps
1. Add static currency conversion rates for common currencies
2. File backlog item for live exchange rate API integration (estimated P2)
```

### Step 10: Save Response File

Save to `.deia/hive/responses/YYYYMMDD-{TASK-ID}-RESPONSE.md`

Verify:
- All 8 sections present
- Absolute paths used
- All three currencies reported
- Acceptance criteria copied from task and marked

## Output Format

Complete response file structure:

```markdown
# {Task ID}: {Title} -- {STATUS}

**Status:** COMPLETE | FAILED (reason)
**Model:** Haiku | Sonnet | Opus
**Date:** YYYY-MM-DD

---

## Files Modified

{absolute paths with line counts}

---

## What Was Done

{bullet list of concrete changes}

---

## Test Results

**Tests written:** N
**Tests passing:** N
**Tests failing:** N
**Coverage:** X%

{test scenarios and files}

---

## Build Verification

**pytest:** PASS | FAIL
**mypy:** PASS | FAIL
**npm run build:** PASS | FAIL

{errors if any}

---

## Acceptance Criteria

- [x] {criterion met}
- [ ] {criterion not met} — {explanation}

---

## Three Currencies (Clock, Coin, Carbon)

| Currency | Estimate | Actual | Delta |
|----------|----------|--------|-------|
| Clock | {time} | {time} | {delta} |
| Coin | {cost} | {cost} | {delta} |
| Carbon | {grams} | {grams} | {delta} |

**Model used:** {model}
**Tokens:** {input}, {output}

---

## Blockers / Follow-ups

{none or detailed list}
```

## Gotchas

### 1. Missing Any Section = Incomplete Response
Response files are rejected if they skip any of the 8 sections. Even if "Blockers / Follow-ups" is empty, write "**None.** Task completed successfully."

### 2. Three Currencies Are All Mandatory
"Time: 52 minutes" without Coin and Carbon is incomplete. All three or none.

### 3. [x] on a Failed Criterion = Dishonest
If a test is failing, mark it `[ ]` with explanation. Never mark `[x]` on something that didn't actually pass.

### 4. "What Was Done" Must Be Concrete
Vague entries like "implemented requirements" or "fixed issues" don't count. Specify which function, which file, which error, which test.

### 5. Response Files Go in .deia/hive/responses/
Not in `.deia/hive/tasks/`, not in `docs/`, not in the repo root.

### 6. File Naming: No Hyphens in Date
Task files: `2026-04-12-HHMM-BEE-TASK-042-ASSIGNMENT.md` (hyphens in date)
Response files: `20260412-TASK-042-RESPONSE.md` (no hyphens in date)

### 7. Build Verification ≠ Test Results
**Test Results** = did your unit tests pass?
**Build Verification** = did `pytest`, `mypy`, `npm run build`, `eslint` pass?

Both sections are required. Don't combine them.

### 8. Token Counts and Cache Hits
If available, report token counts (input/output) and cache hit rate. This helps with cost/carbon accuracy.

### 9. Absolute Paths Match Task File
If the task file used Windows paths (`C:\Users\davee\...`), use Windows paths in the response. If Linux, use Linux. Don't mix.

### 10. Anti-Pattern: "Tests not needed"
Never write "no tests needed" without justification. Pure CSS, documentation, and config files are the only exceptions (BOOT.md Rule 5). If you're modifying code, you need tests.

### 11. [UNDOCUMENTED — needs process doc]
How to handle partial completion (e.g., 80% done but ran out of budget). Current practice: mark FAILED, report what WAS done, flag remaining work as blocker. No formal partial-credit system exists.

### 12. [UNDOCUMENTED — needs process doc]
When to write response file if task is blocked early (e.g., missing dependency discovered 5 minutes in). Current practice: still write full 8-section response, mark Tests/Build as "N/A — blocked before implementation", document blocker in Section 8.
