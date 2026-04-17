# TASK-BEE-R07: Hardcoded Colors + CSS Variable Audit

**Assigned to:** BEE (Sonnet)
**From:** Q33NR
**Date:** 2026-03-23
**Wave:** B (parallel with Wave A)

---

## Objective

Find every hardcoded color in browser/src/. Map the full var(--sd-*) variable set. This repo's rule: CSS uses var(--sd-*) only, no hex, no rgb(), no named colors.

## Method

Search all .tsx, .ts, .css files in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\` for:
- Hex colors: #xxx, #xxxxxx, #xxxxxxxx
- RGB/RGBA: rgb(, rgba(
- HSL/HSLA: hsl(, hsla(
- Named colors used as values (but NOT in CSS variable names)

Exclude: node_modules, var(-- definitions in theme files (those are allowed)

Also audit the CSS variable system:
- What var(--sd-*) variables are defined? In which theme files?
- Which variables are used in code but NOT defined?
- Which variables are defined but NEVER used?

## Deliverables

1. Complete list of hardcoded color instances with file:line
2. Full var(--sd-*) variable catalog
3. Variables used but not defined
4. Variables defined but never used
5. Files ranked by number of violations
6. Recommended variable mapping for each hardcoded value

## Output

Write to: `.deia/hive/responses/2026-03-23-BEE-R07-RESPONSE-css-audit.md`
Append to shared log: `.deia/hive/coordination/2026-03-23-RESEARCH-FINDINGS-LOG.md`
Format: "### [HH:MM] BEE-R07 | [SEVERITY] | CATEGORY\n\nOne-liner.\n\n---"

## IMPORTANT
- READ-ONLY research. Do NOT modify code. Do NOT commit.
