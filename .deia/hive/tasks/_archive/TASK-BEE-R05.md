# TASK-BEE-R05: Hivenode Backend — Auth, LLM, Ledger, Governance

**Assigned to:** BEE (Sonnet)
**From:** Q33NR
**Date:** 2026-03-23
**Wave:** A (parallel with R01-R04, R06-R09)

---

## Objective

Audit the Python backend. Compare what existed in the old efemera/platform repos against what hivenode has now. Cover auth, LLM routing, event ledger, gate enforcer, prompt service, inventory routes, queue runner.

## Old Repo Locations

- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\` — DES, ledger, governance, RAG, builds, chat, production, optimization
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\tests\` — test suite
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\services\ra96it-api\` — auth service
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\` — look for runtime/, core/, src/ dirs

## New Repo Locations

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\` — FastAPI backend
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\` — DES, PHASE-IR
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\` — auth (if separate)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\` — test suite

## Specific Questions

1. Does the auth flow work? Login -> JWT -> API call -> response?
2. What LLM providers are wired? Which actually have working code (not stubs)?
3. Does the event ledger write events? Can you read them back?
4. Is gate_enforcer wired to any actual gates? Or just scaffolded?
5. Does the inventory API (features, bugs, backlog) work?
6. Is the heartbeat endpoint functional?
7. Does the queue runner dispatch bees?
8. What routes exist but have no handler implementation (stub routes)?
9. Are there any hardcoded API keys, URLs, or secrets? (security audit)
10. Compare old efemera backend (~5,100 lines PHASE-IR alone) vs new engine/ — what percentage ported?

## Output Format

YAML frontmatter + sections. Write to: `.deia/hive/responses/2026-03-23-BEE-R05-RESPONSE-hivenode-backend.md`
Append to shared log.

## Shared Log

Append interesting findings to `.deia/hive/coordination/2026-03-23-RESEARCH-FINDINGS-LOG.md`.
Format: `### [HH:MM] BEE-R05 | [SEVERITY] | CATEGORY\n\nOne-liner.\n\n---`
SEVERITY: [CRIT], [WARN], [NOTE], [FYI]. CATEGORY: MISSING, BROKEN, REGRESSED, REDUNDANT-BUILD, ALREADY-FIXED, QUALITY, SECURITY.

## IMPORTANT
- READ-ONLY research. Do NOT modify code. Do NOT commit.
- Flag any hardcoded secrets, API keys, or credentials as [CRIT] | SECURITY.
