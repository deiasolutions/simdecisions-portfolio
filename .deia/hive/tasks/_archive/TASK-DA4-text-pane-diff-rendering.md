# TASK: BEE-DA4 — Text-Pane / SDEditor Diff Rendering

**Date:** 2026-03-19
**Bee:** BEE-DA4
**Type:** Research audit (no code changes)
**Model:** Sonnet

---

## Mission

Audit the SDEditor and text-pane components in the platform repo for diff rendering, Co-Author editing, and markdown capabilities. Determine what exists for the dogfood IDE's diff workflow.

## Platform Repo Location

`C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\`

## Shiftcenter Repo Location

This repo (current working directory). Reference commit `850317c` for March 15 state. Use `git show 850317c:<path>` to read files at that point if needed.

---

## Questions to Answer

Emit each answer as a separate atomic finding.

1. Does SDEditor currently support `diffMode`? How does it render diffs?
2. What is the `diff queue` referenced in AppletShell ("accept/reject incoming edits")? Is it implemented?
3. How does Co-Author work? This is the mechanism for LLM-suggested edits appearing in the editor. Trace the data flow.
4. What markdown rendering capabilities exist? Can it render code blocks with syntax highlighting? Diff blocks?
5. How does `acceptEditsOn` work? What's the UX for accepting/rejecting a diff?

## Files to Start With

- SDEditor component files
- Any files referencing `diffMode`, `diff-viewer`, `acceptEdits`, `Co-Author`
- AppletShell — the diff queue implementation
- `diff-viewer` applet if it exists as a separate component

---

## Output Format

### Research Finding

```
---
bee: BEE-DA4
type: RESEARCH
finding: N
source: platform/simdecisions-2/src/components/sdeditor/SDEditor.jsx:L100-L130
shift: false
---

[Your finding text here]

DIVERGENCE: [none|describe]
P0: [none|describe security issue]
BACKLOG: [none|describe improvement with provenance {source_bee: BEE-DA4, task_context: "...", file: ...}]
```

### NVWR Review Item

NVWR fires on first view of every file, then respects a 2-hour cooldown (`NVWR_REVIEW_PERIOD_S = 7200`). When NVWR fires, scan for:
1. **Security** — auth bypass, injection, secrets in code, unsafe deserialization, missing input validation
2. **Code quality** — dead code, unreachable branches, duplication, missing error handling, hardcoded config
3. **Spec drift** — code that contradicts a locked spec or ADR

```
---
bee: BEE-DA4
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

On completion of NVWR scan for a file, emit: `NVWR_REVIEW_COMPLETE: {file_path, bee: BEE-DA4, timestamp, items_found: N}`

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
