# TASK: BEE-DA2 — Cross-Pane Communication (Bus Wiring)

**Date:** 2026-03-19
**Bee:** BEE-DA2
**Type:** Research audit (no code changes)
**Model:** Sonnet

---

## Mission

Audit the bus wiring between panes in both `platform` (simdecisions-2) and `shiftcenter` repos. Trace how messages flow between terminal, canvas, text-pane, and other primitives.

## Platform Repo Location

`C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\`

## Shiftcenter Repo Location

This repo (current working directory). Reference commit `850317c` for March 15 state. Use `git show 850317c:<path>` to read files at that point if needed.

---

## Questions to Answer

Emit each answer as a separate atomic finding.

1. How does `content_push` work end-to-end? Trace a message from terminal → bus → target pane. Include the governance checkpoint.
2. How does a pane declare what it can receive? Is there a capability advertisement on mount?
3. How does the user (or the EGG) specify which pane talks to which pane? Is wiring declarative (in EGG layout) or imperative (bus.send with explicit target nodeId)?
4. What is `settings_advertisement` and how does it relate to pane discovery?
5. **DIVERGENCE CHECK:** Compare bus implementation in `platform` vs `shiftcenter` at March 15. Flag any differences. Apply the Porting Doctrine.

## Files to Start With

- `shell.context.js` → `MessageBus.send()`
- `SPEC-HIVE-HOST-SHELL.md` §10 (Message Bus)
- Any component that calls `bus.send()` or `bus.subscribe()`
- `shiftcenter` equivalent files at March 15 commit

---

## Output Format

### Research Finding

```
---
bee: BEE-DA2
type: RESEARCH
finding: N
source: platform/simdecisions-2/src/components/shell/shell.context.js:L142-L168
shift: false
---

[Your finding text here]

DIVERGENCE: [none|describe]
P0: [none|describe security issue]
BACKLOG: [none|describe improvement with provenance {source_bee: BEE-DA2, task_context: "...", file: ...}]
```

### NVWR Review Item

NVWR fires on first view of every file, then respects a 2-hour cooldown (`NVWR_REVIEW_PERIOD_S = 7200`). When NVWR fires, scan for:
1. **Security** — auth bypass, injection, secrets in code, unsafe deserialization, missing input validation
2. **Code quality** — dead code, unreachable branches, duplication, missing error handling, hardcoded config
3. **Spec drift** — code that contradicts a locked spec or ADR

```
---
bee: BEE-DA2
type: NVWR
review: N
source: path/to/file.js:L89
category: SECURITY|QUALITY|SPEC-DRIFT
severity: P0|P1|P2
nvwr_cooldown_reset: true
---

[Description of the issue]

KANBAN-TITLE: [one-line summary]
KANBAN-TAGS: [area tags]
```

On completion of NVWR scan for a file, emit: `NVWR_REVIEW_COMPLETE: {file_path, bee: BEE-DA2, timestamp, items_found: N}`

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
