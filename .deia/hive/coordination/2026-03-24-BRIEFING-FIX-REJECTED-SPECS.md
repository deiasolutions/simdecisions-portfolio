# BRIEFING: Fix 5 Rejected Specs in _needs_review

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-24
**Priority:** P0 (blocking queue throughput)

---

## Situation

Gate 0 validation was fixed (priority format + file path existence). 15 of 20 specs now pass and are back in the active queue. 5 specs remain in `_needs_review/` with legitimate content issues.

## Your Job

Fix each spec so it passes Gate 0 validation, then move it back to `.deia/hive/queue/`.

## Specs to Fix

### 1. SPEC-BUG-019.md
**Problem:** No priority in any recognized format.
**Fix:** Add `**Priority:** P1` (or appropriate priority) to the frontmatter.

### 2. SPEC-CANVAS-DRAG-ISOLATION.md
**Problem:** No acceptance criteria found.
**Fix:** Add `## Acceptance Criteria` section with `- [ ]` checklist items.

### 3. SPEC-CANVAS-IR-PIPELINE.md
**Problem:** No acceptance criteria found.
**Fix:** Add `## Acceptance Criteria` section with `- [ ]` checklist items.

### 4. SPEC-PALETTE-COLLAPSE.md
**Problem:** No acceptance criteria found.
**Fix:** Add `## Acceptance Criteria` section with `- [ ]` checklist items.

### 5. SPEC-TURTLE-PENUP.md
**Problem:** No acceptance criteria found.
**Fix:** Add `## Acceptance Criteria` section with `- [ ]` checklist items.

## Validation

After fixing each spec, verify it passes Gate 0:

```python
import sys; sys.path.insert(0, '.deia/hive/scripts/queue')
from gate0 import validate_spec
from spec_parser import parse_spec
from pathlib import Path

spec = parse_spec(Path('.deia/hive/queue/_needs_review/SPEC-NAME.md'))
result = validate_spec(spec, Path('.'))
print(f'PASSED: {result.passed}')
print(result.summary)
```

## After Fixing

Move each passing spec from `_needs_review/` to `.deia/hive/queue/` using `shutil.move()`.

## Constraints

- Read each spec first to understand its intent before writing acceptance criteria
- Acceptance criteria must use `- [ ]` checkbox format
- Keep criteria specific and testable — not vague
- Do NOT change the spec's objective or scope, only add the missing sections
