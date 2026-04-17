# SPEC-VIDEO-GOVERNED-BUILD-001

**MODE: EXECUTE**

**Spec ID:** SPEC-VIDEO-GOVERNED-BUILD-001
**Created:** 2026-04-12
**Author:** Q88N
**Type:** VIDEO — Manim animation for YouTube
**Status:** READY
**Channel:** @daaaave-atx

---

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Skill
manim-animation

---

## Purpose

Produce a ~90 second animated explainer video contrasting two approaches
to AI-assisted software development: The Governed Build vs Black Box
Development. The video is the first published episode on @daaaave-atx
YouTube channel.

The animation runs side by side — left side shows The Governed Build,
right side shows Black Box Development. The Governed Build wins on
visibility, auditability, and ownership. The right side dims at the end.

---

## Files to Read First

- `docs/global-commons/skills/manim-animation/brand-constants.md`
  Brand color palette, usage rules, Three Currencies visual convention, typography scale
- `docs/global-commons/skills/manim-animation/manimce-patterns.md`
  Scene skeleton template, text/shape/animation patterns, timing conventions, debugging tips
- `.deia/m4nim/scenes/alterverse_decision.py`
  Prior scene using same brand constants — use as structural reference for act-based pacing
- `C:\Users\davee\Downloads\governed_build.py`
  Existing draft of this scene — use as starting point, fix and complete to match this spec

## Output Location

- Scene file: `production/episodes/governed-build/governed_build.py`
- Manim renders to: `production/episodes/governed-build/media/` (default Manim output tree)

---

## Concept

Two paths. Same goal. Different ownership.

**Left — The Governed Build:**
- Human + Claude co-author a spec. Questions resolved before anything runs.
- Spec atomizes into task files. Dependencies declared. DAG derived.
- Tasks fan out in parallel where possible. Sequential where required.
- Right model assigned per task (Haiku / Sonnet / Opus / Python script).
- Skills loaded per task.
- Every output tested by BAT.
- Files at every layer — the transcript is the filesystem.
- Three Currencies tracked: CLOCK / COIN / CARBON.

**Right — Black Box Development:**
- One prompt. One big API call. Output appears.
- Nothing else visible. No structure. No transcript. No audit trail.
- You have no idea what happened in there.

---

## Narration Script

Voice: bf_emma (Kokoro-82M British female)
Pace: ~2.5 words per second

| CUE | NARRATION |
|-----|-----------|
| Title frame | "Two ways to build with AI." |
| Split screen appears | "One you own. One you don't." |
| Right side — prompt drops into black box | "Black box. You write a prompt. Something comes back." |
| Right side — nothing else visible | "You have no idea what happened in there." |
| Left side — human + Claude writing spec | "Governed build. You co-author the spec." |
| Questions resolved | "Every question answered before anything runs." |
| DAG forms, tasks fan out | "Your spec atomizes into tasks. Dependencies mapped." |
| Parallel vs sequential | "What can run in parallel, runs. What must wait, waits." |
| Model tags appear per task | "Right model for each task. Your call." |
| Both sides — output appears | "Both produce output." |
| Left side — transcript label | "One leaves a transcript. One leaves nothing." |
| BAT validates, currencies tick | "Every output tested. Every cost measured. Clock. Coin. Carbon." |
| Left glows, right dims | "One build you can audit, govern, and improve. One you can't." |
| Ending frame | "This is SimDecisions. Build governed." |

---

## Visual Requirements

**Title frame:**
- Handle `@daaaave-atx` top left corner, muted color
- Text: "Two ways to build with AI." centered, large, white

**Split screen:**
- Left column header: "THE GOVERNED BUILD" in green
- Right column header: "BLACK BOX DEVELOPMENT" in red
- Vertical divider line, muted color, center screen

**Left side — Governed Build nodes (top to bottom):**
1. human + claude nodes with double arrow between them
2. spec node below, green
3. "questions answered." label
4. Task nodes fanning out (TASK-001, TASK-002 in parallel; TASK-003 dependent)
5. Model tags beneath each task (haiku / sonnet / opus)
6. Output node, green
7. "+ full transcript." label
8. "BAT validates." label
9. Three Currency tags: CLOCK / COIN / CARBON

**Right side — Black Box nodes (top to bottom):**
1. prompt node, muted
2. Black box rectangle, black fill, "?" centered in muted color
3. output node, muted
4. "nothing else." label in red

**Ending frame (full screen, clean):**
- "SimDecisions" large, white, bold, centered
- "Build governed." below, green
- "simdecisions.com" and "@daaaave-atx" side by side, below tagline

**Colors — brand constants only:**
- Background: SD_DARK
- Left column accent: SD_GREEN
- Right column accent: SD_RED
- Nodes: SD_SURFACE fill, SD_BLUE stroke (governed) / SD_MUTED stroke (black box)
- Text: SD_WHITE primary, SD_MUTED secondary
- CLOCK: SD_CLOCK / COIN: SD_COIN / CARBON: SD_CARBON

**Final beat:**
- Right side fades to 15% opacity
- Left column header brightens to SD_GREEN
- Hold 2.5 seconds before ending frame transition

---

## Acceptance Criteria

- [ ] Scene renders without error at `-ql`
- [ ] Scene renders without error at `-qh`
- [ ] Video length is 80-100 seconds
- [ ] Title frame shows `@daaaave-atx` handle
- [ ] Split screen shows both column headers
- [ ] Left side shows: spec, DAG, model tags, BAT, Three Currencies
- [ ] Right side shows: black box with "?" and "nothing else." label
- [ ] All narration cue comments present at correct beats
- [ ] Right side dims to low opacity at final beat
- [ ] Ending frame shows: SimDecisions, "Build governed.", both CTAs
- [ ] No hardcoded hex colors — brand constants only
- [ ] Module docstring present with all required fields
- [ ] Output file at `production/episodes/governed-build/governed_build.py`

## Smoke Test

```bash
cd production/episodes/governed-build
manim governed_build.py GovernedBuild -ql -p
# Expected: renders without error, video opens, ~90 seconds
```

## Constraints

- Scene class name: `GovernedBuild`
- Output file: `production/episodes/governed-build/governed_build.py`
- No LaTeX
- No external assets
- No ThreeDScene or MovingCameraScene
- Brand constants defined at top of file before imports
- NARRATION comments before every major beat

## Response File

`.deia/hive/responses/20260412-SPEC-VIDEO-GOVERNED-BUILD-001-RESPONSE.md`

---

*SPEC-VIDEO-GOVERNED-BUILD-001 — Q88N — 2026-04-12 — #NOKINGS*
