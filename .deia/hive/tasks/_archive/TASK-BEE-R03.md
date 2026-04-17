# TASK-BEE-R03: Terminal + Commands + Bus Integration Comparison

**Assigned to:** BEE (Sonnet)
**From:** Q33NR
**Date:** 2026-03-23
**Wave:** A (parallel with R01-R02, R04-R09)

---

## Objective

Compare the terminal system between OLD repos and shiftcenter. Map every slash command, every terminal mode, every bus integration point.

## Old Repo Locations

- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\` — look for terminal/, command/, cli/
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\` — CLI adapter, router
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\` — look for runtime/ (command handlers)

## New Repo Locations

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\` — TerminalApp.tsx, useTerminal.ts
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\` — MessageBus

## Common Paths

- OLD_EFEMERA: C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\
- OLD_SD2: C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\
- OLD_PLATFORM: C:\Users\davee\OneDrive\Documents\GitHub\platform\
- SHIFTCENTER: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\
- RESPONSES: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\
- SHARED_LOG: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\coordination\2026-03-23-RESEARCH-FINDINGS-LOG.md

## Specific Questions

1. List every slash command that exists in the terminal. Which ones actually work?
2. Does command history (up arrow) work?
3. Is useTerminal.ts really 900+ lines? What can be split?
4. Does terminal -> bus -> pane routing work for all target pane types?
5. Does the LLM response render correctly in the terminal?
6. Is the expandable input overlay implemented?
7. What terminal modes exist (ai, chat, shell, ir, relay)? Which ones work?

## Output Format

Use YAML frontmatter with counts:
```yaml
---
bee_id: BEE-R03
domain: Terminal + Commands + Bus Integration
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

Write final results to: `.deia/hive/responses/2026-03-23-BEE-R03-RESPONSE-terminal-commands.md`
Append findings to shared log: `.deia/hive/coordination/2026-03-23-RESEARCH-FINDINGS-LOG.md`

## Shared Log Format

Append-only. Never edit prior entries. Use this format:

```
### [HH:MM] BEE-R03 | [SEVERITY] | CATEGORY

One-liner finding.

---
```

SEVERITY: [CRIT], [WARN], [NOTE], [FYI]
CATEGORY: MISSING, BROKEN, REGRESSED, REDUNDANT-BUILD, ALREADY-FIXED, QUALITY, SECURITY

## IMPORTANT

- READ-ONLY research. Do NOT modify code. Do NOT commit.
