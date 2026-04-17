# TASK-M4NIM-001 — Q33NR LAUNCH INSTRUCTIONS
**Date:** 2026-04-10  
**Issued by:** Q88N  
**To:** Q33NR  
**Classification:** Spike / Proof of Concept  
**#NOKINGS**

---

## Context

This is a departure from normal process. Q33NR is dispatching directly
to an Opus bee for this task. Q33N is not involved. This is intentional —
the task is a one-shot creative spike, not a governed build task.

The output of this spike will inform the formal M4nim pipeline spec.

---

## What You Are Dispatching

A one-shot Manim scene file generation task to an Opus bee.

The bee will produce a complete, self-contained ManimCE Python scene file
for the first SimDecisions YouTube video. No follow-up tasks. No subtasks.
One prompt in, one scene file out.

---

## The Prompt

The complete prompt is in:
`M4NIM-OPUS-PROMPT-001.md`

Copy everything below the first line (the line that says
"Copy everything below this line into Opus") into the Opus bee's context.
Do not add anything. Do not remove anything. Do not summarize it.
Pass it verbatim.

---

## Opus Bee Instructions

- Model: Claude Opus (latest)
- Temperature: default
- Max tokens: 4000 (the scene file will be ~150-300 lines)
- System prompt: none — the task prompt is self-contained
- One shot — do not retry automatically if output looks wrong

---

## What You Get Back

Opus will return a Python file starting with a module docstring and
ending with the last line of Python code. Nothing before, nothing after.

---

## What To Do With The Output

1. Save the raw Python output as:
   `alterverse_decision.py`

2. Place it in:
   `.deia/m4nim/scenes/alterverse_decision.py`
   (create the directory if it does not exist)

3. Run test render (low quality, fast):
   ```
   manim alterverse_decision.py AlterverseDecision -ql -p
   ```
   The `-p` flag opens the video automatically when done.

4. If render succeeds — forward the `.mp4` path to Q88N. Task complete.

5. If render fails — copy the full stderr error output and forward to Q88N
   with the scene file attached. Do not attempt to fix it. Q88N will
   decide whether to run Round 2.

---

## Acceptance Gate

Q33NR reviews the scene file BEFORE dispatching the render. Check:

- [ ] File starts with the correct module docstring
- [ ] Scene class is named `AlterverseDecision`
- [ ] Brand constants (SD_DARK, SD_BLUE, etc.) are defined at the top
- [ ] No external asset imports (no SVG, PNG, audio file references)
- [ ] No LaTeX-heavy expressions (plain Text objects only)
- [ ] NARRATION comments are present at major animation beats
- [ ] File ends with valid Python (no truncation)

If any check fails — return the output to Q88N before rendering.
Do not render a file that fails the acceptance gate.

---

## Completion Report

Write a brief completion report to:
`.deia/hive/responses/20260410-TASK-M4NIM-001-RESPONSE.md`

Required fields:
1. Status: COMPLETE / FAILED / NEEDS_REVISION
2. Scene file path
3. Render result: SUCCESS / FAILED (include last 5 lines of stderr if failed)
4. Acceptance gate: all checks passed / which checks failed
5. CLOCK: wall time from dispatch to render result
6. COIN: Opus call cost (tokens in × rate + tokens out × rate)
7. CARBON: estimated CO2e for the LLM call
8. Next step recommendation

---

## Notes

- This is Round 1 of a maximum 3-round retry loop
- Round 2 (if needed) will be dispatched by Q88N with error context added
- This spike is dogfood — SimDecisions is simulating its own build strategy
  as the subject of the video it is producing. Do not lose that thread.

---

*Issued by Q88N — 2026-04-10 — #NOKINGS*
