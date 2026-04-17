# SPEC: Fix Deployment Wiring — Dispatch Filename Bug

## Priority
P1

## Objective
Fix the dispatch.py bug where colons in model names (e.g., `ollama:llama3.1:8b`) produce invalid filenames on Windows. The response file path contains `:` characters which Windows rejects.

## Context
Error from earlier queue run:
```
OSError: [Errno 22] Invalid argument: '...\20260313-1654-BEE-OLLAMA:LLAMA3.1:8B-QUEUE-TEMP-...-RAW.txt'
```

The colon in the model name `ollama:llama3.1:8b` makes the filename invalid on Windows.

Files to read first:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py` — response file naming logic (around line 290-300)

## Acceptance Criteria
- [ ] Model names with colons are sanitized in response filenames (replace `:` with `-`)
- [ ] Response file for `ollama:llama3.1:8b` creates valid filename like `...-BEE-OLLAMA-LLAMA3.1-8B-...-RAW.txt`
- [ ] All other model names still produce correct filenames
- [ ] 3+ tests covering colon sanitization, normal model names, edge cases
- [ ] Existing dispatch tests still pass

## Model Assignment
haiku

## Constraints
- Only fix the filename sanitization — do NOT refactor dispatch.py
- Do not change the response file format, only sanitize the model name portion
