# TASK-SKILL-AUDIT-001: Agent Skills Landscape Audit + Threat Classification

**Date:** 2026-04-12  
**Assigned by:** Q88N  
**Routed via:** Q33NR  
**Spec dependency:** `docs/specs/SPEC-SKILL-PRIMITIVE-001.md` (ingested to repo)  
**Priority:** P1 — Enables TASK-019 (Skills Wrapper) to become real  
**Estimated effort:** Medium (2-3 bee sessions)

---

## Objective

Survey the public agent skills ecosystem, inventory what exists, classify each category by threat profile, and produce a rubric that maps directly to our certification tiers (-1 to 3) defined in SPEC-SKILL-PRIMITIVE-001 §5.2.

This is two passes. Do them in order.

---

## Pass 1 — Landscape Inventory

### Sources to Survey

1. **Anthropic official catalog:** https://github.com/anthropics/skills
2. **OpenAI official catalog:** https://github.com/openai/skills
3. **agentskills.io specification:** https://agentskills.io/specification (read the full spec — bee must know this format cold)
4. **Microsoft skills:** search GitHub for Microsoft agent skills catalog
5. **Google Workspace skills:** search for Google Workspace agent skills
6. **Vercel skills:** search for Vercel agent skills catalog
7. **Supabase skills:** search for Supabase agent skills
8. **awesome-agent-skills:** https://github.com/skillmatic-ai/awesome-agent-skills (meta-index)

### Deliverable: `SKILL-LANDSCAPE-INVENTORY.md`

For each catalog, produce a table:

```
| Skill Name | Category | What It Does | Overlaps With DEIA? | Interest Level | Notes |
```

**Category** values (standardize across all catalogs):
- code-review
- document-generation (docx, pdf, pptx, xlsx)
- frontend-design
- testing
- deployment
- data-analysis
- mcp-server-building
- project-management
- content-creation
- security-audit
- api-integration
- other (specify)

**Overlaps With DEIA?** — Flag any skill that duplicates something we already do or have specced. Reference the DEIA component by ID (e.g., "overlaps with bee-dispatch skill from SPEC-SKILL-PRIMITIVE-001 §4.1").

**Interest Level:**
- **IMPORT** — We want this. Bring it in through the governance pipeline.
- **STUDY** — Interesting approach. Read and learn from it, no immediate import.
- **IGNORE** — Not relevant to our stack.
- **WALL-OFF** — Relevant but dangerous. Needs maximum sandboxing or custom restrictions.

---

## Pass 2 — Threat Model by Category

### Deliverable: `SKILL-THREAT-RUBRIC.md`

For each **category** from Pass 1 (not each individual skill), answer:

1. **Filesystem access:** Does this category of skill typically need to read/write files? Which paths?
2. **Network access:** Does it call external APIs, fetch URLs, or phone home?
3. **Shell execution:** Does it run scripts, install packages, or invoke CLI tools?
4. **User data exposure:** Could it access, log, or exfiltrate user content?
5. **Model invocation:** Does it call LLMs directly (token cost / carbon implications)?
6. **Prompt injection surface:** Could the skill's instructions be crafted to override agent behavior?
7. **Blast radius:** If this skill misbehaves, what's the worst case? (contained / local / platform / external)

Then for each category, assign:

```
| Category | Default Cert Tier | Capability Grants at That Tier | Promotion Path | Notes |
```

This table becomes the **classification rubric** that governance.yml generation uses when a new skill is ingested. It is the operational heart of TASK-019.

---

## Pass 3 — Recommendations

### Deliverable: Append to `SKILL-THREAT-RUBRIC.md`

A short section at the end:

1. **Top 5 skills to import first** — highest value, lowest risk. These are the pilot batch for the ingestion pipeline (SPEC-SKILL-PRIMITIVE-001 §5.3).
2. **Top 3 skills to wall off** — high value but high risk. Need custom governance.yml overrides.
3. **Any patterns observed** — structural commonalities across dangerous skills, red flags to automate detection for in TASaaS.
4. **Format compliance notes** — how closely do real-world skills actually follow the agentskills.io spec? Any deviations we need to handle in our ingestion pipeline?

---

## Constraints

- Do NOT execute any third-party skill code. Read only.
- Do NOT install any skill into the repo. This is a survey, not an integration task.
- Reference SPEC-SKILL-PRIMITIVE-001 for all governance terminology and tier definitions.
- If a catalog requires authentication to access, skip it and note the limitation.

---

## Output Files

Place in `docs/research/` (research artifacts, not bee responses):

1. `docs/research/SKILL-LANDSCAPE-INVENTORY.md`
2. `docs/research/SKILL-THREAT-RUBRIC.md`

Also write the standard bee response to `.deia/hive/responses/20260412-SKILL-AUDIT-001-RESPONSE.md` with status, summary, and three currencies.

---

## Success Criteria

- Every major public skill catalog surveyed (minimum 5 of 8 sources)
- Inventory covers at least 50 distinct skills across categories
- Every category has a threat model row
- Classification rubric maps cleanly to SPEC-SKILL-PRIMITIVE-001 §5.2 tiers
- Top 5 / Top 3 recommendations are specific and justified
