---
name: manim-animation
description: >-
  Generate ManimCE Python scene files that render to animated explainer videos.
  Use when asked to animate a concept, visualize a process flow, produce a
  SimDecisions explainer video, render a PRISM-IR flow as animation, or create
  any programmatic animation for YouTube or Tribunal segments. Triggers on:
  "animate", "manim", "explainer video", "visualize this flow", "render this
  concept", "make a video of".
license: Apache-2.0
compatibility: Requires ManimCE (pip install manim), FFmpeg on PATH, Python 3.12+
metadata:
  author: Q88N
  version: "1.0"
  deia:
    cert_tier: -1
    carbon_class: heavy
    requires_human: false
---

# Manim Animation Skill

You write complete, self-contained ManimCE Python scene files from a concept
description or PRISM-IR input. A drone executes the render. You do not render.
You do not test your own output. BAT validates.

Read `references/manimce-patterns.md` before writing any scene.
Read `references/brand-constants.md` for all color values — never hardcode hex inline.

---

## Steps

### Step 1: Parse the input

Identify the input type from the task file:

- `natural_language` — a concept description in plain English
- `prism_ir` — a `.prism.md` file path; read the flow graph before writing

For PRISM-IR input, map the graph to scene structure:
- Nodes → animated objects (rectangles, circles, text labels)
- Edges → arrows with token animations
- Decision gates → branching fork animations
- Checkpoints → visual markers with pause beats

### Step 2: Plan the scene before writing

Write a brief internal plan (as a Python comment block at the top of the file,
after the module docstring) covering:
- Number of acts / major beats
- Objects introduced per beat
- Camera moves (if any — default Scene only, no ThreeDScene)
- Approximate timing per beat to hit target duration

Do not skip this. Unplanned scenes drift past target duration and fail BAT.

### Step 3: Write the scene file

Follow all rules in `references/manimce-patterns.md`. Key rules here:

- Scene class name must match the task file `scene_class` field exactly
- Import brand constants from the top of the file — never inline hex
- Insert `# NARRATION: "..."` comments before every major beat
- Keep all objects within the default frame (roughly ±6 units wide, ±3.5 tall)
- Use `self.wait()` deliberately — silence carries meaning in animation
- Never use external assets (no SVG, PNG, audio file imports)
- No LaTeX unless the task file explicitly requires it

### Step 4: Write the module docstring

First thing in the file, before imports:

```python
"""
Concept: [one sentence]
Target duration: [N] seconds
Input type: natural_language | prism_ir
Dispatch task: [TASK-ID]
Manim animation skill version: 1.0
Round: [N]
"""
```

### Step 5: Write the render command

At the end of your completion report, include the exact render command:

```bash
# Test render (fast, low quality)
manim [scene_file].py [SceneClass] -ql -p

# Final render (slow, high quality)
manim [scene_file].py [SceneClass] -qh -p
```

Always test with `-ql` before final `-qh`.

---

## Output Format

Your deliverable is a single `.py` file. Nothing else.

- Starts with module docstring
- Followed by brand constant definitions
- Followed by imports (`from manim import *`)
- Followed by the scene class
- Ends with the last line of Python
- No explanation text before or after the code

File goes to: `.deia/m4nim/scenes/[scene_name].py`

---

## Narration Cues

Every major beat gets a narration comment. The Kokoro TTS pipeline reads these
to sync audio. Format is strict:

```python
# NARRATION: "Exact words the narrator will speak."
self.wait(3)
```

Place the comment immediately before the `self.wait()` that follows the beat.
Duration in `self.wait()` must be long enough for the narration to complete
at normal speaking pace (~2.5 words per second).

---

## Retry Protocol

If the drone returns a render error, you will receive the full stderr in the
next task. Read the error carefully — Manim errors are precise. Common fixes:

- `NameError` — object referenced before creation; reorder your construct() method
- `AttributeError` — wrong method name; check `references/manimce-patterns.md`
- `ValueError: math domain error` — bad geometry; check coordinate values
- LaTeX errors — remove LaTeX, use plain `Text()` instead

Fix only the reported error. Do not refactor the whole scene on a retry.
Maximum 3 rounds before escalating to Q88N.

---

## Gotchas

- `VGroup.arrange()` modifies positions in place — call it before `self.add()` or `self.play()`
- `Transform()` morphs one object into another — the original object is consumed; don't reference it after
- `FadeOut()` removes the object from the scene — don't animate it again after fading
- `self.wait(0)` is valid and useful for synchronization but adds a frame; use sparingly
- Text objects do not wrap automatically — break long strings manually with `\n`
- Arrow direction is from `start` to `end` — easy to reverse accidentally
- `AnimationGroup` plays animations simultaneously; `LaggedStart` staggers them
- ManimCE version matters — this skill targets v0.18+ syntax; older tutorials may use deprecated APIs
- On Windows, FFmpeg must be on the system PATH, not just installed
- Rendering at `-qh` can take 10-30 minutes for a 90-second scene on CPU; RTX GPU significantly faster

---

## Content Categories

**Core Concepts** — canonical SimDecisions explainers. Evergreen. YouTube-indexed permanently.
Examples: DEF→SIM→BRA→COMP→DEC→EXE loop, Alterverse branching, Three Currencies, PRISM-IR.

**Evolution Log** — when SimDecisions refactors itself, animate what changed and why.
These are dispatched automatically by the organism refactor protocol.

**Tribunal Segments** — short clips for Fr4nk episodes. Max 60 seconds. No narration cues
needed — Fr4nk provides live commentary over the animation.

---

## References

- `references/manimce-patterns.md` — ManimCE syntax, objects, animations, positioning
- `references/brand-constants.md` — SimDecisions color palette and typography constants

See also: `docs/specs/SPEC-SKILL-PRIMITIVE-001.md` for the skill primitive spec.
