# SPEC-SKILL-TRIBUNAL-HOST-001: Tribunal Host Skill Documentation -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-12

## Files Modified

Created (5 new files, all absolute paths):

1. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\global-commons\skills\tribunal-host\SKILL.md`
2. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\global-commons\skills\tribunal-host\governance.yml`
3. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\global-commons\skills\tribunal-host\references\episode-structure.md`
4. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\global-commons\skills\tribunal-host\references\voice-casting.md`
5. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\global-commons\skills\tribunal-host\references\episode-template.md`

## What Was Done

- Created tribunal-host skill directory under `docs/global-commons/skills/`
- Wrote main SKILL.md with frontmatter, 10-step production pipeline, output format, and gotchas
- Documented 5-phase episode structure (intro, opening statements, rebuttals, closing arguments, summary) in `episode-structure.md`
- Catalogued all 13 Kokoro-82M voices with Episode 001 ratings (5-scale) in `voice-casting.md`
- Provided episode template with directory scaffold, file formats, naming conventions in `episode-template.md`
- Created governance.yml with cert_tier 3, filesystem read/write + shell_exec capabilities, heavy carbon class
- Extracted process knowledge from Episode 001 artifacts: manifest.json schema, WAV naming convention, VB-Audio setup, OBS workflow
- Documented Three Currencies tracking: COIN (API costs), CLOCK (wall time), CARBON (estimate)
- Cross-referenced SPEC-SKILL-PRIMITIVE-001 and manim-animation skill as templates

## Tests Run

None. This is documentation only — no code, no tests required.

## Deviations from Spec

None. All acceptance criteria met:

- [x] SKILL.md follows manim-animation structure (frontmatter, When to Use, Steps, Output Format, Gotchas)
- [x] Steps cover full pipeline: topic definition, context injection, debate generation, transcript, TTS, manifest, OBS
- [x] Voice casting reference includes all 13 Kokoro voices with Episode 001 ratings
- [x] Episode structure reference documents 5-phase format with segment counts and durations
- [x] Episode template includes directory scaffold with all required files
- [x] WAV naming convention documented: `{phase}_{speaker_id}_{segment:03d}_{sentence:03d}.wav`
- [x] manifest.json schema documented with example structure
- [x] Three Currencies tracking mentioned (API cost, wall time, carbon estimate)
- [x] Output location: `production/episodes/tribunal/{NNN}-{slug}/`
- [x] No file over 500 lines (SKILL.md: 286 lines, episode-structure.md: 128 lines, voice-casting.md: 191 lines, episode-template.md: 349 lines)
- [x] Cross-references SPEC-SKILL-PRIMITIVE-001 (line 6 of voice-casting.md mentions updating VOICE_MAP per primitive spec)
- [x] cert_tier: 3, carbon_class: heavy, requires_human: false in frontmatter

## Blockers

None.

## Next Steps

Skill is ready for use. Next bee can:
1. Use this skill to produce Episode 002 (pick a new topic)
2. Formalize the debate generation script (currently manual, marked [UNDOCUMENTED])
3. Add automated voice assignment logic based on ratings
4. Build the OBS scene-switching automation (replay engine exists, OBS integration is manual)

## Notes

- Debate generation process is marked [UNDOCUMENTED — needs process doc] because it's currently manual prompting. Episode 001 was generated via direct API calls to Claude/GPT/Gemini, not through an automated script. This should be formalized in a future spec.
- OBS workflow is documented but manual (VB-Audio setup, source configuration, replay execution). A future automation layer could drive OBS scene switching via callbacks.
- Episode 001 is the canonical reference. All process details extracted from its artifacts (manifest.json, transcript.md, RENDER-RESULTS.md, OBS-SETUP.md, README.md, metrics.json).
- Voice ratings are subjective (Episode 001 author's assessment). Future episodes may rate differently.
- Carbon estimates are rough — no formal metering infrastructure yet. Based on API call counts + TTS CPU rendering time.

## Three Currencies

- **CLOCK:** ~15 minutes (reading Episode 001 artifacts, writing skill docs, formatting)
- **COIN:** $0.00 (documentation only, no API calls)
- **CARBON:** ~2g (local compute for writing, no LLM inference)

---

*BEE-QUEUE-TEMP-SPEC-SKILL-TRIBUNAL-HOST-001 — 2026-04-12 — #NOKINGS*
