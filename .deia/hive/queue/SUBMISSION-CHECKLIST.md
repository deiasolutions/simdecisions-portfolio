# Spec Submission Checklist

**Every spec placed in `backlog/` or `queue/` must pass ALL checks below.**
Q33NR verifies before approving. Q33N verifies before writing. Bees don't submit specs.

---

## How to Use This Document

This document is the single source of truth for writing factory specs. If you are an LLM agent (bee, Q33N, Q33NR) or a human writing a spec:

1. **Read this entire document first.** Do not skip sections.
2. **Copy the template** from the "Spec Template" section at the bottom.
3. **Fill in every required section.** The "Required Sections" checklist tells you what's mandatory.
4. **Run the "Before Moving to backlog/" mental test** at the end.
5. **If your spec gets bounced to `_needs_review/`**, read the "Gate 0 Validation" and "Common Failure Modes" sections to diagnose why.

When writing a spec that produces OTHER specs as output (a meta-spec), the output specs must ALSO follow this document. Include this instruction in your meta-spec: "Output specs must conform to `.deia/hive/queue/SUBMISSION-CHECKLIST.md`."

---

## Naming Convention

- [ ] Filename starts with `SPEC-`
- [ ] Format: `SPEC-{ID}-{short-description}.md` (all lowercase after ID)
- [ ] ID is unique — no collision with any spec in `_done/`, `_active/`, `queue/`, or `backlog/`
- [ ] ID parts use digits for sequence numbers, letters for sub-tasks: `WAVE0-A`, `MW-031`, `CONN-05`
- [ ] No date prefix in filename (dates go in frontmatter, not filenames)
- [ ] Description slug uses dashes, no underscores: `ddd-directories` not `ddd_directories`

### ID Extraction Rule

The scheduler extracts task ID by stripping `SPEC-`, splitting on `-`, and taking parts up to and including the first numeric segment (plus any single-letter suffix). Your ID must survive this:

| Filename | Extracted ID | OK? |
|----------|-------------|-----|
| `SPEC-MW-031-menu-bar.md` | MW-031 | Yes |
| `SPEC-WAVE0-A-ddd-dirs.md` | WAVE0-A | Yes (after fix) |
| `SPEC-INFRA-01-crash-fix.md` | INFRA-01 | Yes |
| `SPEC-EFEMERA-CONN-05-cleanup.md` | EFEMERA-CONN-05 | Yes |
| `TASK-WAVE0-A-ddd-dirs.md` | (not found) | NO — must start with SPEC- |
| `SPEC-fix-the-bug.md` | (no ID) | NO — needs numeric segment |

---

## Required Sections

- [ ] `## Priority` — P0, P1, P2, or P3 on its own line below the heading
- [ ] `## Model Assignment` — haiku, sonnet, or opus
- [ ] `## Depends On` — list of SPEC IDs, or "None"
- [ ] `## Objective` — 1-3 sentences, what and why (parser also accepts `## Intent`)
- [ ] `## Files to Read First` — file paths the bee needs for context
- [ ] `## Acceptance Criteria` — concrete, verifiable items in `- [ ]` format
- [ ] `## Constraints` — budget, rules, limits in `- ` format
- [ ] `## Smoke Test` — how to verify the task completed, in `- [ ]` format

---

## Acceptance Criteria Format

- [ ] Every criterion uses `- [ ]` checkbox format
- [ ] NOT numbered lists (`1. 2. 3.`)
- [ ] NOT bullet points without checkboxes (`- thing`)
- [ ] Each criterion is independently verifiable
- [ ] At least 1 criterion exists (Gate 0 rejects specs with 0 criteria)

---

## Smoke Test Format

- [ ] Every item uses `- [ ]` checkbox format (same parser as acceptance criteria)
- [ ] NOT code blocks alone — wrap the command in a checkbox line

---

## File Paths (Files to Read First)

- [ ] No backticks around paths — write `hivenode/main.py` not `` `hivenode/main.py` ``
- [ ] No description suffixes — write `hivenode/main.py` not `hivenode/main.py — the main entry point`
- [ ] All paths relative to repo root
- [ ] All referenced files actually exist (Gate 0 checks every path on disk)

---

## Content Quality

- [ ] Objective is specific enough that a bee can start without asking questions
- [ ] Acceptance criteria are pass/fail — no subjective language ("good", "clean", "appropriate")
- [ ] Constraints include: no file over 500 lines, no stubs, no git operations
- [ ] If research-only: state "No code changes" explicitly in constraints
- [ ] Depends On IDs match actual spec filenames in the pipeline

---

## Pipeline Safety

- [ ] Spec does not duplicate work already in `_done/` (check by ID AND by intent)
- [ ] Spec does not conflict with anything currently in `_active/`
- [ ] If part of a wave/series: all specs in the series use the same prefix with distinct suffixes
- [ ] Model assignment matches complexity: haiku for plumbing, sonnet for logic, opus for architecture

---

## Gate 0 Validation

Gate 0 is a programmatic check (no LLM) that runs before any spec is dispatched. ALL 6 checks must pass or the spec is moved to `_needs_review/`. The checks are defined in `.deia/hive/scripts/queue/gate0.py`.

| # | Check | What It Validates | Common Failure |
|---|-------|------------------|----------------|
| 1 | `priority_present` | `## Priority` exists with P0/P1/P2/P3 | Missing section or value not on own line |
| 2 | `acceptance_criteria_present` | At least 1 criterion found | Wrong format (numbered list instead of `- [ ]`) |
| 3 | `file_paths_exist` | Every path in "Files to Read First" exists on disk | Typo in path, file was renamed/deleted |
| 4 | `deliverables_coherence` | Deliverables don't contradict acceptance criteria | "DO NOT modify X" in deliverables but AC says "fix X" |
| 5 | `scope_sanity` | Objective doesn't reference files forbidden in constraints | Objective says "fix auth.ts" but constraints say "DO NOT modify auth.ts" |
| 6 | `ir_density` | Spec has sufficient information density (score >= 0.2) | Spec too vague, no concrete file paths or requirements |

### Diagnosing a Bounce

If your spec lands in `_needs_review/`, run Gate 0 manually:

```bash
python -c "
import sys
from pathlib import Path
sys.path.insert(0, '.deia/hive/scripts/queue')
from gate0 import validate_spec
from spec_parser import parse_spec
spec = parse_spec(Path('.deia/hive/queue/_needs_review/YOUR-SPEC.md'))
result = validate_spec(spec, '.')
print(f'Overall: {\"PASS\" if result.passed else \"FAIL\"}')
for check in result.checks:
    print(f'  {check.name}: {\"PASS\" if check.passed else \"FAIL\"} -- {check.message}')
"
```

---

## Common Failure Modes

These are real failures that have caused specs to bounce. Learn from them.

### 1. Duplicate Section Headings

The parser uses `re.search` which finds the FIRST `## Acceptance Criteria` in the file. If your spec contains a template or example block with `## Acceptance Criteria` as a heading (even inside a code fence), the parser matches THAT one first — not your real one.

**Fix:** Put your real `## Acceptance Criteria` section BEFORE any template/example blocks. Or don't use `## ` headings inside code fences — use plain text descriptions instead.

### 2. Numbered Lists Instead of Checkboxes

The parser only recognizes `- [ ]` and `- [x]` as acceptance criteria. Numbered lists, plain bullets, or any other format is silently ignored.

### 3. File Paths With Backticks or Descriptions

"Files to Read First" paths must be bare: `browser/src/App.tsx`. The path extractor strips backticks and trailing descriptions, but backticks can confuse the existence check.

### 4. Contradictory Scope

If your objective names a file and your constraints say "DO NOT modify" that same file, Gate 0 rejects for scope incoherence. Resolve the contradiction.

### 5. Missing Numeric ID Segment

The filename `SPEC-fix-the-bug.md` has no numeric segment, so the ID extractor fails. Always include a number: `SPEC-FIX-001-the-bug.md`.

---

## Spec Template

Copy this template. Fill in every section. Delete the instructions in parentheses.

```markdown
# SPEC-{ID}-{short-description}: Title

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

(1-3 sentences: what needs to happen and why.)

## Files to Read First

(Bare file paths, one per line with `- ` prefix. Every path must exist.)

- browser/src/example/File.tsx
- hivenode/example/routes.py

## Acceptance Criteria

(Checkbox format. Each item independently verifiable. At least 1 required.)

- [ ] First verifiable outcome
- [ ] Second verifiable outcome
- [ ] All existing tests still pass
- [ ] N+ new tests cover the change

## Smoke Test

(Checkbox format. Quick manual or CLI verification.)

- [ ] curl or pytest command that proves it works

## Constraints

(Simple bullet format. Rules the bee must follow.)

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Use var(--sd-*) CSS variables only

## Files to Modify

(Optional. Paths that will be created or changed.)

- browser/src/example/File.tsx
- browser/src/example/File.css
```

---

## Before Moving to backlog/

Run this mental test: "If I hand this spec to a bee with no other context besides BOOT.md, can it complete the task and I can verify every acceptance criterion?" If no, the spec needs more detail.

Then run this format test: "Does every `## Acceptance Criteria` item start with `- [ ]`? Is the FIRST `## Acceptance Criteria` heading in the file my REAL one, not one inside a template block?" If no, fix the format.
