# TASK-W1-C: Regent slot estimation and reservation protocol (process doc)

## Objective
Write a process documentation file (`.deia/processes/P-10-SLOT-RESERVATION.md`) that defines how the regent (Q88NR-bot) estimates bee count from a spec, when to call hivenode's `/slot-reserve` and `/slot-release` endpoints, and how to check slot availability before approving Q33N to dispatch the next bee.

This is NOT a code task. This is a workflow/instruction doc for future Q88NR sessions.

## Context
After TASK-W1-A (hivenode slot endpoints) and TASK-W1-B (queue runner slot polling), the infrastructure is in place. Now we need to define the regent's workflow:

1. Regent reads spec from queue runner
2. Regent estimates how many bees the spec will need (count acceptance criteria sections, OR read `## Bee Count` header if present)
3. Regent calls `POST /build/slot-reserve` with estimated count
4. Regent dispatches Q33N to write task files
5. Regent reviews task files
6. Regent approves Q33N to dispatch first bee
7. After each bee completes (response file written), regent calls `POST /build/slot-release` with `released: 1`
8. Before approving Q33N to dispatch next bee, regent checks `GET /build/slot-status` — if `available < 1`, tells Q33N to wait
9. When all bees done, regent calls final `/slot-release` to free remaining slots
10. Regent writes response file

This process ensures the regent controls bee dispatch pace and prevents concurrency explosions.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\processes\` — see existing process docs for format and style
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\HIVE.md` — regent (Q88NR) workflow, lines 25-101
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` — slot reservation endpoints (added by TASK-W1-A)

## Deliverables

### 1. Process doc file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\processes\P-10-SLOT-RESERVATION.md`

The doc must include these sections:

#### Section 1: Overview
- [ ] What this protocol is for (prevent uncontrolled bee concurrency)
- [ ] Who uses it (Q88NR-bot, not Q33N or bees)
- [ ] When to use it (every spec processed by regent)

#### Section 2: Bee Count Estimation
- [ ] How to estimate bee count from a spec:
  - If spec has `## Bee Count` header with an integer, use it directly
  - If no `## Bee Count` header, count acceptance criteria groups (count `##` headers under `## Acceptance Criteria` section)
  - If no acceptance criteria, estimate based on deliverables (1 bee per major deliverable)
  - If uncertain, default to 3 bees
- [ ] Example spec snippets showing each case

#### Section 3: Slot Reservation Workflow (step-by-step)
- [ ] Step 1: Read spec file
- [ ] Step 2: Estimate bee count (using rules from Section 2)
- [ ] Step 3: Call `POST http://localhost:8000/build/slot-reserve` with `{"spec_id": "<spec-id>", "bee_count": N}`
  - Include exact curl example
  - Include expected response: `{"ok": true, "total_reserved": N, "available": M}`
- [ ] Step 4: Dispatch Q33N to write task files
- [ ] Step 5: Review task files, approve dispatch
- [ ] Step 6: Before approving Q33N to dispatch EACH bee, check `GET http://localhost:8000/build/slot-status`
  - If `available < 1`, tell Q33N: "Slots full. Wait 30 seconds and check again."
  - If `available >= 1`, approve dispatch
- [ ] Step 7: After each bee completes (response file written), call `POST http://localhost:8000/build/slot-release` with `{"spec_id": "<spec-id>", "released": 1}`
  - Include exact curl example
  - Include expected response: `{"ok": true, "remaining": N, "available": M}`
- [ ] Step 8: Repeat steps 6-7 for all bees
- [ ] Step 9: When all bees done, call final `/slot-release` to free remaining slots (if any still reserved)
- [ ] Step 10: Write response file

#### Section 4: Error Handling
- [ ] What if hivenode is unreachable? (log warning, proceed without slot reservation — queue runner will fall back to default)
- [ ] What if `/slot-reserve` returns error? (log error, proceed — queue runner will use default 1-slot-per-spec)
- [ ] What if `/slot-release` returns error? (log error, retry once, then proceed — slots will eventually expire or be freed on hivenode restart)

#### Section 5: Examples
- [ ] Full example: spec with 5 acceptance criteria groups → estimate 5 bees → reserve 5 slots → dispatch → release 1 slot per bee → final release
- [ ] Full example: spec with `## Bee Count: 8` header → reserve 8 slots directly
- [ ] Edge case: spec needs 12 bees, but capacity is 10 → regent reserves 12, queue runner waits until enough slots free (other specs finish)

#### Section 6: Integration Points
- [ ] Hivenode endpoints used:
  - `POST /build/slot-reserve`
  - `POST /build/slot-release`
  - `GET /build/slot-status`
- [ ] Queue runner behavior: polls `/slot-status`, waits if `available < 1`
- [ ] Q33N role: dispatches bees ONLY when regent approves (no change from current workflow)

## Test Requirements
This is a documentation task — NO CODE TESTS.

However, the doc MUST be validated:
- [ ] Readable markdown format
- [ ] All code examples are valid (curl commands, JSON payloads)
- [ ] No broken links
- [ ] File saved to correct path: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\processes\P-10-SLOT-RESERVATION.md`

## Constraints
- No file over 500 lines (this doc should be ~200-300 lines)
- Clear, concise language
- Code examples must be copy-paste ready
- Follow format/style of existing process docs in `.deia/processes/`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-W1-C-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — state "No tests (documentation task)" OR describe validation performed
5. **Build Verification** — N/A for docs, but confirm file is readable markdown
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Model Assignment
**Sonnet** — requires understanding regent workflow, writing clear instructions.

## Success Criteria
- Process doc file exists at `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\processes\P-10-SLOT-RESERVATION.md`
- All 6 sections present and complete
- Code examples are valid and copy-paste ready
- Doc is readable and follows existing process doc format
- Future Q88NR sessions can read this doc and implement the protocol
