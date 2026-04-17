# TASK-SKILL-SCAFFOLD-001: Skill Directory + First Three Internal Skills

**Date:** 2026-04-12  
**Assigned by:** Q88N  
**Spec dependency:** `docs/specs/SPEC-SKILL-PRIMITIVE-001.md`  
**Audit dependency:** `docs/research/SKILL-LANDSCAPE-INVENTORY.md`, `docs/research/SKILL-THREAT-RUBRIC.md`  
**Priority:** P1  
**Estimated effort:** 1 bee session

---

## Objective

1. Create the `.deia/skills/` directory structure in the repo
2. Write the first three internal SKILL.md files in agentskills.io format
3. Generate governance.yml sidecars for each

---

## Part 1 — Directory Structure

Create:

```
.deia/skills/
├── internal/          # Skills authored by Q88N / hive
│   ├── bee-dispatch/
│   │   ├── SKILL.md
│   │   └── governance.yml
│   ├── spec-writer/
│   │   ├── SKILL.md
│   │   └── governance.yml
│   └── hive-diagnostics/
│       ├── SKILL.md
│       └── governance.yml
└── imported/          # Third-party skills (empty for now)
    └── .gitkeep
```

No other files. No scripts/, references/, or assets/ subdirectories yet — add those only when a specific skill needs them.

---

## Part 2 — Three Internal Skills

Write each SKILL.md in agentskills.io format. YAML frontmatter with `name`, `description`, `license`, `metadata` (including `deia.cert_tier: 3`). Markdown body with Steps, Output Format, and Gotchas sections.

### 2.1 bee-dispatch

**What this skill teaches an agent:** How to format and send task files to Mr. Code via the hive dispatch system.

**Survey before writing.** Grep the repo for:
- `.deia/hive/scripts/dispatch/dispatch.py`
- `.deia/config/injections/`
- `.deia/hive/coordination/`
- Any existing dispatch documentation

The SKILL.md must reflect actual current dispatch mechanics found in the repo, not assumptions. If the file paths have moved, document what you found.

**Minimum content to cover:**
- Task file naming convention
- Required sections in a task file (Objective, Constraints, Output Files, Success Criteria, Three Currencies)
- How dispatch.py routes to a bee
- How injection shims are loaded (base.md + claude_code.md)
- What goes in `.deia/hive/responses/` vs `docs/` vs other locations

### 2.2 spec-writer

**What this skill teaches an agent:** How to produce specs in DEIA format.

**Survey before writing.** Grep the repo for:
- `docs/specs/SPEC-*.md` — sample at least 5 existing specs to extract the pattern
- Any spec templates or spec-writing process docs

The SKILL.md should codify the actual pattern found in existing specs — not invent a new one.

**Minimum content to cover:**
- Frontmatter fields (Version, Date, Author, Status, Tags)
- Standard sections (Problem Statement, proposed solution, implementation, ADR cross-references)
- Status values and what they mean
- Where specs are stored (`docs/specs/`)
- The NEEDS DAVE INPUT convention for unresolved design decisions

### 2.3 hive-diagnostics

**What this skill teaches an agent:** How to survey the repo, run grep audits, and produce gap reports.

**Survey before writing.** Grep the repo for:
- `gap-report.md` or any gap analysis output
- Existing audit/survey patterns in hive responses
- The "survey before build" process references

**Minimum content to cover:**
- The mandatory "survey before build" principle
- Standard grep commands for locating file paths, specs, task files
- How to produce a gap report (format, severity levels, source references)
- How to check for stale/orphaned files

---

## Part 3 — governance.yml for Each

Generate a governance.yml sidecar for each skill using the template from SPEC-SKILL-PRIMITIVE-001 §5.1. All three are internal skills:

```yaml
cert_tier: 3
capabilities:
  filesystem_read: true
  filesystem_write: false
  network_access: false
  shell_exec: false
  user_data_access: false
  model_invocation: false
  event_ledger_write: true
blast_radius: contained
budget:
  clock_max_seconds: 300
  coin_max_usd: 0.00
  carbon_max_grams: 0.0
```

Adjust capabilities per skill — bee-dispatch may need `filesystem_write: true` for task file creation, hive-diagnostics needs `shell_exec: true` for grep commands. Use judgment based on what the skill actually does.

---

## Constraints

- Follow agentskills.io spec exactly. `name` field: lowercase + hyphens only, max 64 chars.
- `description` field: must include both what the skill does AND when to use it. 1-1024 chars.
- SKILL.md body under 500 lines. If longer, split into references/ files.
- Do NOT invent process details. Everything in these skills must come from what's actually in the repo. If something is undocumented, write `[UNDOCUMENTED — needs process doc]` in the Gotchas section.

---

## Output Files

```
.deia/skills/internal/bee-dispatch/SKILL.md
.deia/skills/internal/bee-dispatch/governance.yml
.deia/skills/internal/spec-writer/SKILL.md
.deia/skills/internal/spec-writer/governance.yml
.deia/skills/internal/hive-diagnostics/SKILL.md
.deia/skills/internal/hive-diagnostics/governance.yml
.deia/skills/imported/.gitkeep
```

---

## Success Criteria

- All 7 files created and committed
- Each SKILL.md passes agentskills.io frontmatter validation (name, description present, constraints met)
- Each SKILL.md body reflects actual repo state, not assumptions
- Each governance.yml capabilities match what the skill actually needs
- No external dependencies, no network calls, no package installs
