# CLAUDE CODE BEHAVIOR OVERRIDES

## STOP BEFORE ACTING

- Present your plan in numbered steps BEFORE any file edit
- Wait for explicit "go" — silence is not consent
- If unsure whether to proceed, ASK

## SCOPE LOCK

- Fix ONLY what was requested in the task file
- Do NOT fix adjacent test failures you notice
- Do NOT refactor nearby code "while you're in there"
- If you see something else broken, REPORT it in your response — do not fix it

## PATH DISCIPLINE

- All file paths must be absolute
- Never use relative paths
- Verify file exists before editing

## NO RABBIT HOLES

- State your top 2 hypotheses before investigating
- If first hypothesis fails, STOP and report before trying second
- Maximum 2 fix attempts before reporting blocker
- Do NOT chase red herrings

## TERMINOLOGY (NON-NEGOTIABLE)

- Terminal = INPUT ONLY (hive> prompt)
- Text-pane = OUTPUT display
- EGG = app unit with .set.md config
- Chrome = shell UI (menu, sidebar) — NEVER in ALWAYS_REGISTERED
- Set = collection of EGGs on the Stage
