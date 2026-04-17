# SPEC: Fix failures from w1-02-phase-ir-cli

## Priority
P0

## Objective
Fix the errors reported after processing w1-02-phase-ir-cli. See error details below.

## Context
Original spec: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-15-0753-SPEC-w1-02-phase-ir-cli.md
Fix cycle: 1 of 2

### Error Details
Dispatch failed with exit code 4294967295: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\gemini.py:2: FutureWarning: 

All support for the `google.generativeai` package has ended. It will no longer be receiving 
updates or bug fixes. Please switch to the `google.genai` package as soon as possible.
See README for more details:

https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

  import google.generativeai as genai


## Acceptance Criteria
- [ ] All original acceptance criteria still pass
- [ ] Reported errors are resolved
- [ ] No new test regressions

## Model Assignment
sonnet

## Constraints
- Do not break existing tests
- Fix the reported errors, do not refactor
