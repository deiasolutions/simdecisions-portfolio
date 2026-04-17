---
name: hive-diagnostics
description: >-
  Survey the repo, run grep audits, and produce gap reports. Use when
  planning a new feature (survey before build principle), debugging
  missing files, assessing spec coverage, or producing architectural
  gap analysis. Covers grep commands for locating file paths, specs,
  task files, gap report format, severity levels, and stale file
  detection.
license: Proprietary
compatibility: Requires grep, find, basic shell commands
metadata:
  author: Q88N
  version: "1.0"
  deia:
    cert_tier: 3
    carbon_class: light
    requires_human: false
---

# Hive Diagnostics

## When to Use

- **Survey before build:** Planning a new feature and need to understand existing patterns
- **Gap analysis:** Identifying missing components, stale files, or broken references
- **Spec coverage audit:** Checking which specs have implementations vs. which are stale
- **File location:** "Where is the X module?" or "Does Y file exist?"
- **Dependency mapping:** Understanding what depends on what
- **Pre-refactor assessment:** Before major changes, survey what will be affected

## Steps

### Step 1: Define the Survey Scope

Before running commands, be clear on what you're surveying:

| Survey Type | Question to Answer | Example |
|-------------|-------------------|---------|
| **Pattern extraction** | "How do existing implementations do X?" | "How are FastAPI routers structured?" |
| **File location** | "Where is component Y?" | "Where is the dispatch script?" |
| **Coverage gap** | "Which specs lack implementation?" | "Which SPEC-XXX files have no matching task files?" |
| **Stale file detection** | "What files reference deleted components?" | "What task files reference packages/ (deleted during flatten)?" |
| **Dependency impact** | "What breaks if I change X?" | "What imports simdecisions.core (old namespace)?" |

### Step 2: Standard Grep Commands

**Locate files by pattern:**
```bash
# Find all spec files
find docs/specs -name "SPEC-*.md"

# Find all task files
find .deia/hive/tasks -name "TASK-*.md" -o -name "*-TASK-*.md"

# Find skills
find .deia/skills -name "SKILL.md"

# Find response files
find .deia/hive/responses -name "*-RESPONSE.md"
```

**Grep for content patterns:**
```bash
# Find all files that import a module
grep -r "from hivenode.scheduler" --include="*.py"

# Find all references to a deleted path
grep -r "packages/core" --include="*.py" --include="*.md"

# Find all hardcoded colors (Hard Rule #3 violation)
grep -r "#[0-9A-Fa-f]\{6\}" --include="*.tsx" --include="*.css"

# Find all TODOs or stubs (Hard Rule #6 violation)
grep -r "# TODO\|// TODO\|pass  # stub" --include="*.py" --include="*.ts"

# Find all specs with NEEDS DAVE INPUT
grep -r "NEEDS DAVE INPUT" docs/specs/
```

**Count matches:**
```bash
# How many spec files exist?
find docs/specs -name "SPEC-*.md" | wc -l

# How many task files reference a spec?
grep -l "SPEC-SKILL-PRIMITIVE-001" .deia/hive/tasks/*.md | wc -l

# How many tests exist for a module?
find tests/hivenode/scheduler -name "test_*.py" | wc -l
```

### Step 3: Produce a Gap Report

A gap report identifies missing, broken, or stale components. Format:

```markdown
# Gap Report: <Survey Title>

**Date:** YYYY-MM-DD
**Surveyed by:** <Bot ID or role>
**Scope:** <What was surveyed>

## Summary

- **Total items surveyed:** N
- **Gaps identified:** M
- **Severity breakdown:**
  - Critical: X
  - High: Y
  - Medium: Z
  - Low: W

---

## Critical Gaps (blocking production)

### GAP-001: Missing implementation for SPEC-XXX

**Severity:** Critical
**Impact:** Feature X cannot ship without this
**Evidence:**
- SPEC file exists: `docs/specs/SPEC-XXX-001.md`
- No task files reference it: `grep -l "SPEC-XXX-001" .deia/hive/tasks/*.md` → 0 results
- No implementation files found: `grep -r "XXXModule" --include="*.py"` → 0 results

**Recommended action:** Create task file for implementation

---

## High Gaps (impacts quality)

### GAP-002: Stale imports referencing deleted packages/ directory

**Severity:** High
**Impact:** Import errors on startup, tests will fail
**Evidence:**
```bash
$ grep -r "from packages\." --include="*.py"
hivenode/routes/health.py:5:from packages.core.config import VERSION
tests/hivenode/test_health.py:3:from packages.core.routes import health
```

**Recommended action:** Update imports to new flat structure (hivenode.*, simdecisions.*)

---

## Medium Gaps (technical debt)

### GAP-003: Hardcoded colors in 12 files

**Severity:** Medium
**Impact:** Violates Hard Rule #3, prevents theming
**Evidence:**
```bash
$ grep -r "#[0-9A-Fa-f]\{6\}" --include="*.tsx"
browser/src/apps/canvas.tsx:47:  background: "#FF5733"
browser/src/primitives/button.tsx:12:  color: "#3498DB"
...
```

**Recommended action:** Replace with `var(--sd-*)` CSS variables

---

## Low Gaps (nice-to-have)

### GAP-004: No tests for new hive-diagnostics skill

**Severity:** Low
**Impact:** Skill not validated, could have bugs
**Evidence:**
- Skill file exists: `.deia/skills/internal/hive-diagnostics/SKILL.md`
- No test file: `tests/skills/test_hive_diagnostics.py` does not exist

**Recommended action:** Add test coverage (optional, skill is docs-only)

---

## Appendix: Full Survey Output

[Optional: paste full grep/find output for reference]
```

### Step 4: Severity Levels

Use this rubric to assign severity:

| Severity | When to Use | Examples |
|----------|-------------|----------|
| **Critical** | Blocks production, breaks core functionality | Missing implementation for approved spec, broken imports that crash startup, security vulnerability |
| **High** | Degrades quality, fails tests, violates hard rules | Stale imports (tests fail), hardcoded colors (rule violation), missing required files |
| **Medium** | Technical debt, not urgent | No tests for new feature, verbose code over 500 lines, TODO comments |
| **Low** | Nice-to-have, cosmetic | Typos in comments, missing optional docs, unused variables |

### Step 5: Source References

Every gap must cite **evidence** — the exact grep command or find command that revealed it.

**Bad:**
```markdown
### GAP-001: Some files are missing
There are missing files.
```

**Good:**
```markdown
### GAP-001: Missing task files for SPEC-SKILL-PRIMITIVE-001

**Evidence:**
```bash
$ grep -l "SPEC-SKILL-PRIMITIVE-001" .deia/hive/tasks/*.md
# (no output — 0 task files reference this spec)

$ ls docs/specs/SPEC-SKILL-PRIMITIVE-001.md
docs/specs/SPEC-SKILL-PRIMITIVE-001.md  # spec exists
```
**Conclusion:** Spec is approved but no tasks created yet.
```

### Step 6: Recommended Actions

Each gap should include a **recommended action** — what to do about it.

**Format:**
```markdown
**Recommended action:** <Concrete next step>
**Assigned to:** <Role or leave blank for Q88N to decide>
**Priority:** P0 | P1 | P2
```

**Examples:**
- `Create task file TASK-IMPL-SKILL-001 to implement SPEC-SKILL-PRIMITIVE-001`
- `Run find-replace: s/packages\.core/hivenode/g across all .py files`
- `Add test file tests/skills/test_hive_diagnostics.py (P2, optional)`

### Step 7: Detecting Stale Files

**Stale file = references something that no longer exists.**

**Common stale patterns:**
```bash
# References to deleted packages/ directory (post-flatten)
grep -r "packages\." --include="*.py" --include="*.md"

# References to deleted eggs/ directory (now browser/sets/)
grep -r "eggs/" --include="*.ts" --include="*.tsx" --include="*.md"

# Imports from old namespaces
grep -r "from simdecisions\.core" --include="*.py"
grep -r "from simdecisions\.engine" --include="*.py"

# References to deleted specs/tasks
# (Harder to detect — requires cross-checking file existence)
```

**How to report stale files:**
```markdown
### GAP-XXX: Stale references to deleted packages/ directory

**Severity:** High (will cause import errors)
**Files affected:** 47
**Evidence:**
```bash
$ grep -r "from packages\." --include="*.py" | wc -l
47
```

**Sample violations:**
- `hivenode/routes/health.py:5` — `from packages.core.config`
- `tests/hivenode/test_health.py:3` — `from packages.core.routes`

**Recommended action:** Bulk find-replace `packages.core` → `hivenode`, `packages.engine` → `simdecisions`
```

### Step 8: Output Location

Gap reports go to:
- **Formal reports:** `docs/audits/<date>-<topic>-gap-report.md`
- **Working notes:** `.deia/intention-engine/gap-report.md` (scratch file, can overwrite)
- **Briefing attachments:** Inline in `.deia/hive/coordination/<briefing>.md`

## Output Format

A complete gap report should have:

1. **Executive summary** (total items, gaps, severity breakdown)
2. **Gaps grouped by severity** (Critical → High → Medium → Low)
3. **Evidence for each gap** (grep/find commands, file paths)
4. **Recommended actions** (concrete next steps)
5. **Optional appendix** (full raw output for deep-dive)

**Length:** Under 500 lines. If longer, split into:
- Main report (summary + critical/high gaps)
- Appendix file (full details)

## Gotchas

### 1. Survey Without Specific Goal

**Bad:**
```bash
grep -r "TODO" .
# (spits out 5000 lines of mixed results)
```

**Good:**
```bash
# Survey goal: Find TODOs in production code (not tests, not docs)
grep -r "# TODO" --include="*.py" \
  --exclude-dir=tests \
  --exclude-dir=docs \
  hivenode/ simdecisions/
```

Always scope the survey to answer a specific question.

### 2. No Evidence in Gap Report

A gap without evidence is not actionable. Every gap needs:
- The grep/find command that revealed it
- Sample file paths or line numbers
- Count of affected items

### 3. Confusing Grep Syntax (Windows)

**Windows Git Bash gotcha:**
```bash
# This fails on Windows (quote escaping)
grep -r "from packages\.core"

# This works
grep -r "from packages\\.core"
# Or use single quotes
grep -r 'from packages\.core'
```

Always test grep commands before pasting into gap report.

### 4. Overwhelming Output

**Symptom:** Grep returns 10,000 lines, unreadable.

**Fix:** Use `head`, `wc -l`, or filter further:
```bash
# Just count matches
grep -r "TODO" --include="*.py" | wc -l

# Show first 20 matches
grep -r "TODO" --include="*.py" | head -20

# Show only file names (not content)
grep -rl "TODO" --include="*.py"
```

### 5. False Positives in Grep

**Example:** Searching for `core` matches `score`, `encore`, `hardcore`.

**Fix:** Use word boundaries:
```bash
# Bad (matches substrings)
grep -r "core" --include="*.py"

# Good (matches whole word)
grep -r "\bcore\b" --include="*.py"

# Better (matches module path)
grep -r "from.*\.core" --include="*.py"
```

### 6. Forgetting to Exclude Tests/Docs

When surveying production code, exclude tests and docs:

```bash
grep -r "pattern" \
  --include="*.py" \
  --exclude-dir=tests \
  --exclude-dir=docs \
  --exclude-dir=.deia \
  hivenode/ simdecisions/
```

Otherwise, gap report will flag test fixtures, example code, etc.

### 7. No Severity Assignment

Every gap needs a severity level (Critical | High | Medium | Low). If you can't decide:
- **Does it block production?** → Critical
- **Does it break tests or violate hard rules?** → High
- **Is it technical debt?** → Medium
- **Is it cosmetic or optional?** → Low

### 8. Gap Report Without Recommended Actions

A gap without a recommended action is just noise. Every gap should end with:

```markdown
**Recommended action:** <Concrete step>
**Priority:** P0 | P1 | P2
```

### 9. Surveying Generated/Build Files

**Bad:**
```bash
grep -r "pattern" .
# Searches node_modules/, .venv/, dist/, build/, etc.
```

**Good:**
```bash
grep -r "pattern" \
  --exclude-dir=node_modules \
  --exclude-dir=.venv \
  --exclude-dir=dist \
  --exclude-dir=build \
  --exclude-dir=.git \
  hivenode/ simdecisions/ browser/
```

Always exclude build artifacts, dependencies, and .git.

### 10. Stale Gap Report (Not Updated After Fixes)

Gap reports are **snapshots** — they reflect state at survey time. If gaps are fixed, archive the report:

**Move to:**
```
docs/audits/<date>-<topic>-gap-report.md
→ docs/audits/_resolved/<date>-<topic>-gap-report.md
```

Or add a **Resolution** section to the original report:

```markdown
## Resolution (2026-04-12)

- GAP-001: Fixed in commit abc123
- GAP-002: Fixed in commit def456
- GAP-003: Accepted as technical debt, moved to backlog

**Status:** RESOLVED
```

## Examples from Repo

**Gap report (intention coverage):**
- `.deia/intention-engine/gap-report.md` — Platform → ShiftCenter coverage analysis

**Audit task (stale files):**
- `.deia/hive/tasks/_archive/2026-03-14-TASK-091-audit-gap-analysis.md` — Audit task example

**Survey output (architectural):**
- `.deia/audits/2026-04-08/delta/GAP-ANALYSIS.md` — Delta audit from repo flatten
