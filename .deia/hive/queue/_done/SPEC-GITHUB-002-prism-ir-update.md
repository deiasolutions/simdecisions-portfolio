---
id: GITHUB-002
priority: P1
model: sonnet
role: bee
depends_on: []
---
# SPEC-GITHUB-002: PRISM-IR Public Repo Update

## Priority
P1

## Model Assignment
sonnet

## Depends On
(none)

## Objective
Update the existing `deiasolutions/prism-ir` public repo with improved README, WIRE framework positioning, and a PATTERNS.md showing 43/43 van der Aalst coverage.

## Constraints
- You are in EXECUTE mode. Write all code. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- Use `gh` CLI for all GitHub operations (already authenticated)
- Do NOT publish any proprietary engine code — spec, schema, docs, and sanitized examples only
- Compiler implementation is proprietary — spec and schema are open
- All claims must be defensible
- Written for technical hiring manager audience

## Files to Read First
- `docs/PRISM-IR.md` — the full PRISM-IR specification (line 1146 has pattern coverage verification)

## Steps

1. Audit current repo state: `gh repo view deiasolutions/prism-ir --json name,description`
2. Clone to temp dir: `gh repo clone deiasolutions/prism-ir /tmp/prism-ir`
3. Check existing files: README.md, SPEC.md, BLOG.md, tests.yaml, LICENSE
4. Read the local `docs/PRISM-IR.md` for authoritative content
5. Update README.md with content below
6. Create PATTERNS.md with van der Aalst 43-pattern coverage table
7. Commit and push

## README.md Content Requirements

- What PRISM-IR is: a YAML-based universal intermediate representation for encoding any process flow
- Position within WIRE framework: PRISM-IR is the IR layer of WIRE (Wiki, Intention, Result, Executable)
- The 11 primitives: flow, node, edge, port, timing, group, resource, variable, token, distribution, checkpoint
- **Coverage: 100% of van der Aalst's 43 canonical workflow patterns** (verified)
- The novel IRD (Intention/Reaction Density) metric
- IRE fidelity: Intention → Result → Executable as the quality gate
- Dialect compiler targets: BPMN 2.0, SBML, L-systems, Workflow YAML, Terraform, Makefile
- Note: compiler implementation is proprietary — spec and schema are open

## PATTERNS.md Content

Table of all 43 van der Aalst canonical workflow patterns with columns:
- Pattern # | Pattern Name | Category | PRISM-IR Coverage | Notes

Categories: Basic Control Flow, Advanced Branching, Structural, Multiple Instance, State-based, Cancellation, Iteration, Termination, Trigger

All 43 must show "Covered" status. Extract pattern details from `docs/PRISM-IR.md`.

## Acceptance Criteria
- [ ] README.md updated with WIRE positioning and 100% pattern coverage claim
- [ ] PATTERNS.md exists showing 43/43 van der Aalst coverage
- [ ] No proprietary engine code in repo
- [ ] LICENSE is Apache 2.0
- [ ] Content is accurate per docs/PRISM-IR.md

## Smoke Test
```bash
gh api repos/deiasolutions/prism-ir/contents/README.md -q .name && echo README
gh api repos/deiasolutions/prism-ir/contents/PATTERNS.md -q .name && echo PATTERNS
```

## Response Location
`.deia/hive/responses/20260408-GITHUB-002-RESPONSE.md`
