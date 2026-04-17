# TASK-BEE-R00: Environment Baseline (Smoke Test)

**Assigned to:** BEE (Sonnet)
**From:** Q33NR
**Date:** 2026-03-23
**Wave:** 0 (runs first, before all others)

---

## Objective

Verify the research environment before dispatching 10 bees. Establish the baseline pass/fail state.

## Tasks

1. Run `pytest` from repo root — document pass/fail count
2. Run `npm run build` from browser/ — document errors vs clean build
3. Run `npx vitest run` from repo root — document pass/fail count
4. Document Node version (`node --version`), Python version (`python --version`)
5. List installed npm packages (`npm ls --depth=0` from browser/)
6. List installed pip packages (`pip list` or `pip freeze`)
7. Check if Railway PG is reachable: look at hivenode config for DATABASE_URL, try to connect
8. Verify `.deia/BOOT.md` and `.deia/HIVE.md` exist and are readable

## Common Paths

- OLD_EFEMERA: C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\
- OLD_SD2: C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\
- OLD_PLATFORM: C:\Users\davee\OneDrive\Documents\GitHub\platform\
- SHIFTCENTER: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\
- RESPONSES: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\
- SHARED_LOG: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\coordination\2026-03-23-RESEARCH-FINDINGS-LOG.md

## Output

Write final results to: `.deia/hive/responses/2026-03-23-BEE-R00-RESPONSE-environment-baseline.md`
Append findings to shared log: `.deia/hive/coordination/2026-03-23-RESEARCH-FINDINGS-LOG.md`

## Shared Log Format

Append-only. Never edit prior entries. Use this format:

```
### [HH:MM] BEE-R00 | [SEVERITY] | CATEGORY

One-liner finding.

---
```

SEVERITY: [CRIT], [WARN], [NOTE], [FYI]
CATEGORY: MISSING, BROKEN, REGRESSED, REDUNDANT-BUILD, ALREADY-FIXED, QUALITY, SECURITY

## IMPORTANT

- This is READ-ONLY research. Do NOT modify any source files.
- Do NOT commit anything.
- If build or tests are RED, document exactly what fails. Do NOT try to fix anything.
