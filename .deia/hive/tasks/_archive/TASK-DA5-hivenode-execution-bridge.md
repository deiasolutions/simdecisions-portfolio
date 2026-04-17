# TASK: BEE-DA5 — Hivenode Execution Bridge

**Date:** 2026-03-19
**Bee:** BEE-DA5
**Type:** Research audit (no code changes)
**Model:** Sonnet

---

## Mission

Audit the hivenode (Python FastAPI backend) in both platform and shiftcenter repos. Focus on execution-related endpoints, websocket state, and what would be needed to bridge the terminal in the browser to backend code execution.

## Platform Repo Location

`C:\Users\davee\OneDrive\Documents\GitHub\platform\`

Also check the BEE2 implementation audit if it exists in project docs: `2026-01-05-BEE2-IMPLEMENTATION-AUDIT.md`

## Shiftcenter Repo Location

This repo (current working directory). Reference commit `850317c` for March 15 state. Use `git show 850317c:<path>` to read files at that point if needed.

---

## Questions to Answer

Emit each answer as a separate atomic finding.

1. What execution-related endpoints exist on the hivenode? (The BEE2 audit lists 27 endpoints — focus on anything that runs code, executes commands, or manages processes.)
2. What is the current state of the websocket endpoint (`/api/ws`)? Is it still echo-only or has it been upgraded?
3. How does the terminal in the browser connect to the hivenode? Is there a websocket bridge? HTTP polling? Or is it browser-only with no backend connection?
4. What would it take to add a `/api/exec` endpoint that accepts `{code, language, cwd}` and returns `{stdout, stderr, exit_code}`? What security gates are needed? (GateEnforcer integration? REQUIRE_HUMAN?)
5. What authentication does the hivenode use? Is it the ra96it bot token system or something simpler?

## Files to Start With

- `server.py` (main FastAPI app)
- `core/` directory
- `adapters/` directory
- Any websocket handler files
- The BEE2 implementation audit (in project knowledge)
- `shiftcenter/hivenode/` directory for comparison

---

## Output Format

### Research Finding

```
---
bee: BEE-DA5
type: RESEARCH
finding: N
source: platform/efemera/src/server.py:L50-L80
shift: false
---

[Your finding text here]

DIVERGENCE: [none|describe]
P0: [none|describe security issue]
BACKLOG: [none|describe improvement with provenance {source_bee: BEE-DA5, task_context: "...", file: ...}]
```

### NVWR Review Item

NVWR fires on first view of every file, then respects a 2-hour cooldown (`NVWR_REVIEW_PERIOD_S = 7200`). When NVWR fires, scan for:
1. **Security** — auth bypass, injection, secrets in code, unsafe deserialization, missing input validation
2. **Code quality** — dead code, unreachable branches, duplication, missing error handling, hardcoded config
3. **Spec drift** — code that contradicts a locked spec or ADR

```
---
bee: BEE-DA5
type: NVWR
review: N
source: path/to/file.py:L89
category: SECURITY|QUALITY|SPEC-DRIFT
severity: P0|P1|P2
nvwr_cooldown_reset: true
---

[Description of the issue]

KANBAN-TITLE: [one-line summary]
KANBAN-TAGS: [area tags]
```

On completion of NVWR scan for a file, emit: `NVWR_REVIEW_COMPLETE: {file_path, bee: BEE-DA5, timestamp, items_found: N}`

---

## Porting Doctrine Reference Card

```
IF code_in_platform == code_in_shiftcenter:
    → FINDING: "Ported correctly. No action."

IF code_in_platform != code_in_shiftcenter AND difference_is_security_fix:
    → P0: Log with both file paths, exact diff, security rationale.

IF code_in_platform != code_in_shiftcenter AND difference_is_NOT_security:
    → BACKLOG: "Divergence from platform. Port the platform version."
      Include: platform file, shiftcenter file, what changed, provenance.

IF code_exists_in_platform BUT NOT in_shiftcenter:
    → BACKLOG: "Missing port. Platform has X, shiftcenter doesn't."

IF code_exists_in_shiftcenter BUT NOT in_platform:
    → RESEARCH finding: "New in shiftcenter. Not from platform."
      Q33N decides if this is intentional new work or accidental divergence.
```

---

## Rules

- This is RESEARCH ONLY. Do NOT modify any files.
- Emit findings atomically — one finding per output block.
- Do NOT mix RESEARCH and NVWR in the same block.
- P0s get flagged immediately.
