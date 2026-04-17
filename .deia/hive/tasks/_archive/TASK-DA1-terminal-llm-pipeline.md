# TASK: BEE-DA1 — Terminal → LLM Response Pipeline

**Date:** 2026-03-19
**Bee:** BEE-DA1
**Type:** Research audit (no code changes)
**Model:** Sonnet

---

## Mission

Audit the `platform` repo (simdecisions-2) and the `shiftcenter` repo to trace how the terminal sends prompts to an LLM and receives responses.

## Platform Repo Location

`C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\`

## Shiftcenter Repo Location

This repo (current working directory). Reference commit `850317c` for March 15 state. Use `git show 850317c:<path>` to read files at that point if needed.

---

## Questions to Answer

Emit each answer as a separate atomic finding.

1. How does the terminal component send prompts to an LLM provider? Trace the call chain from user input at `hive>` to the API call.
2. What LLM provider abstraction exists? Is it model-agnostic (BYOLLM)?
3. How does the terminal handle structured responses (code blocks, diffs, IR)? Does it parse response content types?
4. What is the `to_text` routing mechanism referenced in the prompt blocks? How does terminal output get routed to other panes?
5. What is Zone 2 rendering? How does it differ from Zone 1 input? What formats does Zone 2 support?

## Files to Start With

- `shell.context.js` (MessageBus, envelope routing)
- Any file containing `to_text`, `to_user`, `content_push`
- The terminal/frank component files
- Any LLM provider or AI assistant modules

Look in `platform/simdecisions-2/src/components/shell/` and related directories.

---

## Output Format

### Research Finding

```
---
bee: BEE-DA1
type: RESEARCH
finding: N
source: platform/simdecisions-2/src/components/shell/shell.context.js:L142-L168
shift: false
---

[Your finding text here]

DIVERGENCE: [none|describe]
P0: [none|describe security issue]
BACKLOG: [none|describe improvement with provenance {source_bee: BEE-DA1, task_context: "...", file: ...}]
```

### NVWR Review Item

NVWR fires on first view of every file, then respects a 2-hour cooldown (`NVWR_REVIEW_PERIOD_S = 7200`). When NVWR fires, scan for:
1. **Security** — auth bypass, injection, secrets in code, unsafe deserialization, missing input validation
2. **Code quality** — dead code, unreachable branches, duplication, missing error handling, hardcoded config
3. **Spec drift** — code that contradicts a locked spec or ADR

```
---
bee: BEE-DA1
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

On completion of NVWR scan for a file, emit: `NVWR_REVIEW_COMPLETE: {file_path, bee: BEE-DA1, timestamp, items_found: N}`

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
