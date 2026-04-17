# TASK-BEE-R04: EGG System + App Registry + Loading

**Assigned to:** BEE (Sonnet)
**From:** Q33NR
**Date:** 2026-03-23
**Wave:** A (parallel with R01-R03, R05-R09)

---

## Objective

Audit the EGG parsing system, app registry, and loading states. Load every .egg.md file and document which render vs which fail.

## Old Repo Locations

- `C:\Users\davee\OneDrive\Documents\GitHub\platform\canonical\` — old EGG files, registry
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\scenarios\` — scenario parser

## New Repo Locations

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\` — all .egg.md files
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\` — parseEggMd.ts, eggInflater.ts, eggWiring.ts
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\` — app registry, constants.ts (APP_REGISTRY)

## Specific Questions

1. List EVERY .egg.md file. For each: does it have a valid layout block? Does its appType resolve in the registry? Flag any that reference unregistered appTypes.
2. Does appType "text" resolve to text-pane? (alias handling)
3. What happens when an EGG references an unregistered appType?
4. Is there a 404 EGG for bad routes?
5. Does the apps directory/home EGG show all available apps?
6. Does EGG drop + tab negotiation work?
7. Are loading, empty, and error states implemented for all panes?
8. Compare the old scenario/EGG system against the new one — what capabilities were lost?

## Output Format

YAML frontmatter with counts, then sections: PORTED AND WORKING, PORTED BUT BROKEN, NEVER PORTED, PARTIALLY PORTED, REDUNDANTLY REBUILT, GENUINELY NEW, QUALITY ISSUES.

Write to: `.deia/hive/responses/2026-03-23-BEE-R04-RESPONSE-egg-system.md`
Append to shared log.

## Shared Log

Append interesting findings to `.deia/hive/coordination/2026-03-23-RESEARCH-FINDINGS-LOG.md`.
Format: `### [HH:MM] BEE-R04 | [SEVERITY] | CATEGORY\n\nOne-liner.\n\n---`
SEVERITY: [CRIT], [WARN], [NOTE], [FYI]. CATEGORY: MISSING, BROKEN, REGRESSED, REDUNDANT-BUILD, ALREADY-FIXED, QUALITY, SECURITY.

## IMPORTANT
- READ-ONLY research. Do NOT modify code. Do NOT commit.
