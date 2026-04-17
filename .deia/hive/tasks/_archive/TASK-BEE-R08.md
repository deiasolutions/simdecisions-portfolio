# TASK-BEE-R08: Dead Code + File Size + Architecture Violations

**Assigned to:** BEE (Sonnet)
**From:** Q33NR
**Date:** 2026-03-23
**Wave:** B (parallel with Wave A)

---

## Objective

Structural code quality audit across the entire shiftcenter monorepo. Find dead code, oversized files, circular dependencies, console.log pollution, TODO debt, and banned patterns.

## Repo Path

`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\`

## Checklist

1. **Files over 500 lines** — list every one with line count. The 500-line limit is a hard rule in this repo (BOOT.md). 1,000 is the absolute max.
2. **Dead imports** — imported but never used in that file
3. **Dead exports** — exported but never imported by any other file in the repo
4. **Dead files** — files that nothing imports (orphans). Check browser/src/, hivenode/, engine/
5. **Circular dependencies** — A imports B imports A. Check both TypeScript and Python
6. **Console.log in production code** — list all instances (exclude test files). console.warn and console.error are OK
7. **TODO/FIXME/HACK comments** — list all with file:line and surrounding context
8. **Duplicate functionality** — two files doing the same thing (e.g., two different date formatters, two bus implementations)
9. **`_outbox/` usage** — this directory is BANNED. Does it exist anywhere? Does any code reference it?
10. **Test coverage gaps** — which directories under browser/src/ and hivenode/ have ZERO test files?

## Method

Use grep/find/file analysis. This is read-only research. You are scanning for patterns, not running code.

For dead exports: check each exported symbol against all other files in the repo. If nothing imports it, it's dead.

For circular deps: trace import chains. Focus on browser/src/shell/, browser/src/primitives/, browser/src/infrastructure/.

## Output

Write to: `.deia/hive/responses/2026-03-23-BEE-R08-RESPONSE-code-quality.md`
Append to shared log: `.deia/hive/coordination/2026-03-23-RESEARCH-FINDINGS-LOG.md`
Format: "### [HH:MM] BEE-R08 | [SEVERITY] | CATEGORY\n\nOne-liner.\n\n---"

## IMPORTANT
- READ-ONLY research. Do NOT modify code. Do NOT commit.
