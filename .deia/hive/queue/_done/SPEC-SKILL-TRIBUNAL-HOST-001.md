# SPEC-SKILL-TRIBUNAL-HOST-001

**MODE: EXECUTE**

**Spec ID:** SPEC-SKILL-TRIBUNAL-HOST-001
**Created:** 2026-04-12
**Author:** Q88N
**Type:** SKILL — Write a formal SKILL.md for the Tribunal podcast production format
**Status:** READY

---

## Priority
P2

## Depends On
None

## Model Assignment
sonnet

## Skill
spec-writer

---

## Purpose

Write a complete SKILL.md for `tribunal-host` — the structured multi-model AI debate
podcast format. The skill should codify the full production pipeline so any bee can
pick up a topic and produce a complete episode (transcript + TTS render + manifest).

The Tribunal format is proven — Episode 001 is fully rendered with 160 WAV files,
and Episode 002 has a complete production package (topic, context, prompts, script,
scoring rubric). But the process knowledge lives scattered across episode artifacts.
This skill formalizes it as a repeatable, dispatchable process.

---

## Files to Read First

- `docs/global-commons/skills/manim-animation/SKILL.md`
  Reference skill — use this as the structural template (frontmatter, Steps, Output Format, Gotchas)
- `docs/global-commons/skills/manim-animation/brand-constants.md`
  Example of a references/ file within a skill directory
- `.deia/skills/internal/spec-writer/SKILL.md`
  Another reference skill — internal style
- `docs/specs/SPEC-SKILL-PRIMITIVE-001.md`
  Formal spec defining skills as primitives — tribunal-host is listed at line 62
- `production/episodes/tribunal/001-who-should-hire-dave/README.md`
  Episode 001 status, voice assignments, production state
- `production/episodes/tribunal/001-who-should-hire-dave/OBS-SETUP.md`
  VB-Audio + OBS multi-track recording guide
- `production/episodes/tribunal/001-who-should-hire-dave/RENDER-RESULTS.md`
  TTS render summary and metrics
- `production/episodes/tribunal/001-who-should-hire-dave/render/manifest.json`
  Audio manifest structure — timing, speaker routing, WAV file naming convention
- `production/episodes/tribunal/001-who-should-hire-dave/format.yaml`
  Episode-level format overrides
- `production/episodes/tribunal/001-who-should-hire-dave/metrics.json`
  API cost metrics from debate generation
- `production/episodes/tribunal/001-who-should-hire-dave/transcript.md`
  Full debate transcript — the output structure
- `production/episodes/tribunal/001-who-should-hire-dave/context.md`
  Evidence injection format
- `production/episodes/tribunal/001-who-should-hire-dave/topic.md`
  Debate topic/motion format
- `production/episodes/tribunal/001-who-should-hire-dave/personas.md`
  Panelist persona definitions
- `production/episodes/tribunal/000-who-should-hire-dave/`
  Episode 000 — simpler prototype, compare to see evolution
- `production/episodes/tribunal/002-workers-ai-cant-replace/topic.md`
  Episode 002 topic — latest format with debate rules and context mode
- `production/episodes/tribunal/002-workers-ai-cant-replace/context.md`
  Episode 002 context — full source material with citations and data tables
- `production/episodes/tribunal/002-workers-ai-cant-replace/frank-prompts.md`
  Episode 002 Fr4nk prompts — system prompt + 8 segment-level turn prompts + production notes
- `production/episodes/tribunal/002-workers-ai-cant-replace/debater-prompts.md`
  Episode 002 debater prompts — per-position system prompts with evidence, rhetorical stance, opponent guides
- `production/episodes/tribunal/002-workers-ai-cant-replace/scoring-rubric.md`
  Episode 002 Three Currencies rubric — scoring templates, OBS ticker layout, audience guide
- `production/episodes/tribunal/002-workers-ai-cant-replace/script.md`
  Episode 002 full pre-scripted transcript — 6 phases including Fr4nk Q&A round (evolved from EP 001's 5-phase format)

---

## Deliverables

- [ ] `docs/global-commons/skills/tribunal-host/SKILL.md` — The main skill document
- [ ] `docs/global-commons/skills/tribunal-host/references/episode-structure.md` — Episode format covering both the 5-phase structure (EP 001: intro, opening statements, rebuttals, closing arguments, summary) and the evolved 6-phase structure (EP 002: intro, data summary, Baumol mechanism, opening statements, Q&A round, closing arguments, Three Currencies checkpoints, audience verdict)
- [ ] `docs/global-commons/skills/tribunal-host/references/voice-casting.md` — Kokoro voice catalog with ratings, assignment rules, voice ID reference
- [ ] `docs/global-commons/skills/tribunal-host/references/episode-template.md` — Directory scaffold and file templates for a new episode

## Acceptance Criteria

- [ ] SKILL.md follows same structure as manim-animation SKILL.md (frontmatter, When to Use, Steps, Output Format, Gotchas)
- [ ] Steps cover the full pipeline: topic definition, context injection, debate generation, transcript production, TTS rendering, manifest creation, OBS recording
- [ ] Voice casting reference includes all 13 Kokoro voices with ratings from Episode 001
- [ ] Episode structure reference documents both EP 001 (5-phase) and EP 002 (6-phase with Fr4nk Q&A) formats, with segment counts and typical durations
- [ ] Episode template includes directory scaffold covering the full file set: `topic.md`, `context.md`, `personas.md` or `debater-prompts.md`, `frank-prompts.md`, `scoring-rubric.md`, `format.yaml`, `script.md` (if pre-scripted) or `transcript.md` (if live), `render/manifest.json`, `render/wavs/`
- [ ] WAV naming convention documented: `{phase}_{speaker_id}_{segment_index:03d}_{sentence_index:03d}.wav`
- [ ] manifest.json schema documented
- [ ] Three Currencies tracking mentioned (API cost from metrics.json, wall time, carbon estimate)
- [ ] Output location: `production/episodes/tribunal/{NNN}-{slug}/`
- [ ] No file over 500 lines
- [ ] Cross-references SPEC-SKILL-PRIMITIVE-001 and manim-animation skill
- [ ] cert_tier: 3, carbon_class: heavy, requires_human: false in frontmatter

## Constraints

- This is documentation only — no Python code, no new features
- Extract process knowledge from Episode 001 AND Episode 002 artifacts — EP 002 is the latest format and should be treated as the primary reference where they differ
- Keep SKILL.md under 300 lines; push detail to references/
- Do not document the replay/OBS engine (that module doesn't exist yet) — document the manual OBS workflow from OBS-SETUP.md instead

## Response File

`.deia/hive/responses/20260412-SPEC-SKILL-TRIBUNAL-HOST-001-RESPONSE.md`

---

*SPEC-SKILL-TRIBUNAL-HOST-001 — Q33NR on behalf of Q88N — 2026-04-12 — #NOKINGS*
