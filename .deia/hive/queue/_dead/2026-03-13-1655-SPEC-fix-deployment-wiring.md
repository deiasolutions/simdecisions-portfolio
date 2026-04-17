# SPEC: Fix failures from deployment-wiring

## Priority
P0

## Objective
Fix the errors reported after processing deployment-wiring. See error details below.

## Context
Original spec: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-13-1654-SPEC-fix-deployment-wiring.md
Fix cycle: 2 of 2

### Error Details
Dispatch failed with exit code 1: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\gemini.py:2: FutureWarning: 

All support for the `google.generativeai` package has ended. It will no longer be receiving 
updates or bug fixes. Please switch to the `google.genai` package as soon as possible.
See README for more details:

https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

  import google.generativeai as genai
Traceback (most recent call last):
  File "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py", line 366, in <module>
    sys.exit(main())
             ^^^^^^
  File "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py", line 353, in main
    response = dispatch_bee(
               ^^^^^^^^^^^^^
  File "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py", line 297, in dispatch_bee
    with open(response_file, "w", encoding="utf-8") as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
OSError: [Errno 22] Invalid argument: 'C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\shiftcenter\\.deia\\hive\\responses\\20260313-1654-BEE-OLLAMA:LLAMA3.1:8B-QUEUE-TEMP-2026-03-13-1654-SPEC-FIX-DEPLOYMENT-WIRING-RAW.txt'


## Acceptance Criteria
- [ ] All original acceptance criteria still pass
- [ ] Reported errors are resolved
- [ ] No new test regressions

## Model Assignment
sonnet

## Constraints
- Do not break existing tests
- Fix the reported errors, do not refactor
