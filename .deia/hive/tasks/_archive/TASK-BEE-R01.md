# TASK-BEE-R01: Shell + Layout + DnD Comparison

**Assigned to:** BEE (Sonnet)
**From:** Q33NR
**Date:** 2026-03-23
**Wave:** A (parallel with R02-R09)

---

## Objective

Compare the shell/layout/DnD system between the OLD repos and the current shiftcenter monorepo. Document what's ported, what's broken, what's missing.

## Old Repo Locations

- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\` — shell reducer, actions, chrome, layout, split, resize
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\` — look for shell/, layout/, pane/ directories

## New Repo Locations

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\` — Shell.tsx, PaneChrome.tsx, SplitContainer.tsx, eggToShell.ts, types, etc.
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\` — relay_bus, etc.

## Common Paths

- OLD_EFEMERA: C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\
- OLD_SD2: C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\
- OLD_PLATFORM: C:\Users\davee\OneDrive\Documents\GitHub\platform\
- SHIFTCENTER: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\
- RESPONSES: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\
- SHARED_LOG: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\coordination\2026-03-23-RESEARCH-FINDINGS-LOG.md

## Specific Questions

1. Does pane swap work? Delete? Merge?
2. Does drag-to-dock work? Drag-to-float? Return from float?
3. Do all shell chrome buttons function (close, collapse, pin, maximize)?
4. Is the FAB menu implemented? Is it sticky? Does it show correct categories?
5. Are pane borders computed from the tree or hardcoded?
6. List every file over 500 lines in shell/. List every hardcoded hex/rgb value.
7. Compare the shell reducer/dispatch between old and new — what actions exist in old but not new?

## Output Format

Use YAML frontmatter with counts:
```yaml
---
bee_id: BEE-R01
domain: Shell + Layout + DnD
features_existed_old: [count]
features_exist_new: [count]
features_missing: [count]
features_broken: [count]
features_working: [count]
hardcoded_colors: [count]
dead_code_files: [count]
files_over_500_lines: [list]
---
```

Then sections: PORTED AND WORKING, PORTED BUT BROKEN, NEVER PORTED, PARTIALLY PORTED, REDUNDANTLY REBUILT, GENUINELY NEW, QUALITY ISSUES.

## Output Files

Write final results to: `.deia/hive/responses/2026-03-23-BEE-R01-RESPONSE-shell-layout-dnd.md`
Append findings to shared log: `.deia/hive/coordination/2026-03-23-RESEARCH-FINDINGS-LOG.md`

## Shared Log Format

Append-only. Never edit prior entries. Use this format:

```
### [HH:MM] BEE-R01 | [SEVERITY] | CATEGORY

One-liner finding.

---
```

SEVERITY: [CRIT], [WARN], [NOTE], [FYI]
CATEGORY: MISSING, BROKEN, REGRESSED, REDUNDANT-BUILD, ALREADY-FIXED, QUALITY, SECURITY

## IMPORTANT

- This is READ-ONLY research. Do NOT modify any source files. Do NOT commit anything.
- For every "REDUNDANTLY REBUILT" item: compare line count, test count, feature completeness between old and new. Flag whether old version is better.
