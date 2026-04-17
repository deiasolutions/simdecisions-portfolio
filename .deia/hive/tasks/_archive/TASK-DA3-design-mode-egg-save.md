# TASK: BEE-DA3 — Design Mode + EGG Save/Write

**Date:** 2026-03-19
**Bee:** BEE-DA3
**Type:** Research audit (no code changes)
**Model:** Sonnet

---

## Mission

Audit the platform repo for any existing Design Mode implementation and EGG write/save capabilities. Determine the gap between the Product Session spec (§7, §8) and what's actually built.

## Platform Repo Location

`C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\`

Also check: `C:\Users\davee\OneDrive\Documents\GitHub\platform\` root for the Product Session doc (`2026-03-10-PRODUCT-SESSION-CANONICAL.docx` or similar).

## Shiftcenter Repo Location

This repo (current working directory). Reference commit `850317c` for March 15 state. Use `git show 850317c:<path>` to read files at that point if needed.

---

## Questions to Answer

Emit each answer as a separate atomic finding.

1. Does any implementation of Design Mode exist in the platform repo? Even partial? Look for: `ELEMENT_SELECTED` bus events, scene_system mode switching, property editor terminal.
2. Is there any implementation of `egg_writer` — serializing the current layout tree back to `.egg.md`?
3. How does workspace persistence currently work? (`shell.reducer` → serialization → storage). What format? What's stored?
4. Is the `register` block (draft change tracking per §8.1) implemented anywhere?
5. What's the gap between the spec (Product Session §7-8) and what's actually built?

## Files to Start With

- `shell.reducer.js` — look for SAVE, LOAD, SERIALIZE actions
- `shell.utils.js` — `serializeTree()`, `deserializeTree()`
- Any file referencing `egg_writer`, `design`, `inspector`, `ELEMENT_SELECTED`
- EGG loader/inflater files

---

## Output Format

### Research Finding

```
---
bee: BEE-DA3
type: RESEARCH
finding: N
source: platform/simdecisions-2/src/components/shell/shell.reducer.js:L50-L80
shift: false
---

[Your finding text here]

DIVERGENCE: [none|describe]
P0: [none|describe security issue]
BACKLOG: [none|describe improvement with provenance {source_bee: BEE-DA3, task_context: "...", file: ...}]
```

### NVWR Review Item

NVWR fires on first view of every file, then respects a 2-hour cooldown (`NVWR_REVIEW_PERIOD_S = 7200`). When NVWR fires, scan for:
1. **Security** — auth bypass, injection, secrets in code, unsafe deserialization, missing input validation
2. **Code quality** — dead code, unreachable branches, duplication, missing error handling, hardcoded config
3. **Spec drift** — code that contradicts a locked spec or ADR

```
---
bee: BEE-DA3
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

On completion of NVWR scan for a file, emit: `NVWR_REVIEW_COMPLETE: {file_path, bee: BEE-DA3, timestamp, items_found: N}`

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
