# TASK-Q33N-CONTINUE-FACTORY-SELF-REFACTOR

**Task ID:** TASK-Q33N-CONTINUE-FACTORY-SELF-REFACTOR
**Created:** 2026-04-10
**Author:** Q33NR
**Assigned to:** Q33N (queen)
**Model:** sonnet
**Role:** queen
**Priority:** P0
**Parent spec:** `docs/specs/SPEC-FACTORY-SELF-REFACTOR-001.md`
**Parent prompt:** `.deia/hive/coordination/PROMPT-FACTORY-SELF-REFACTOR-001.md`
**Status:** READY

---

## YOUR ROLE

You are **Q33N** — a queen. Q33NR has handed off the factory self-refactor orchestration to you. You take over at **Step 3** of the Q33NR execution sequence. You coordinate bees. You do NOT write code yourself.

Read these three documents before taking any action:

1. `.deia/hive/coordination/PROMPT-FACTORY-SELF-REFACTOR-001.md` — the Q88N→Q33NR prompt
2. `docs/specs/SPEC-FACTORY-SELF-REFACTOR-001.md` — the master spec (authoritative)
3. `.deia/hive/tasks/TASK-SIMDECISIONS-SCAFFOLD.md` — pre-written by Q33NR with two-phase gate complete

---

## What Q33NR Has Already Done

- ✅ Placed all three source files from Q88N in their repo homes
- ✅ Dispatched Phase 0 survey bee (`TASK-SURVEY-FACTORY-GAP-MATRIX.md`) with Sonnet — running when this task was created
- ✅ Pre-written and gate-reviewed `TASK-SIMDECISIONS-SCAFFOLD.md` with source paths corrected (row 7 `claude_cli_subprocess.py` resolved to `hivenode/adapters/cli/`)
- ✅ Applied a **Q33NR safeguard**: secrets are EXCLUDED from the scaffold phase. Phase 1 does not copy `.env`, credentials, or any secret files. This overrides the master spec's "all artifacts convey" clause for Phase 1 only and was approved by Q88N.
- ✅ Committed earlier session work to `origin/main`

---

## Your Execution Sequence (Pick up at Step 3)

### Step 3 — Poll for Survey Response

Poll for the gap matrix response file:
```
.deia/hive/responses/20260411-FACTORY-GAP-MATRIX.md
```

Check every 2 minutes. Do NOT proceed until this file exists and contains:
- A gap matrix table with the required columns
- `Section 6: Summary Counts`
- `Section 7: Clock / Coin / Carbon`

If the survey bee fails, errors out, or the response is incomplete/missing required sections after 30 minutes:
1. Do NOT dispatch a second survey bee automatically
2. Write a status file to `.deia/hive/responses/20260410-Q33N-BLOCKED-SURVEY.md` describing what's missing
3. Escalate to Q88N (write to `.deia/hive/coordination/20260410-ESCALATION-SURVEY-FAILED.md`)
4. STOP

### Step 4 — Dispatch the Scaffold Bee

Once the survey response exists and passes validation, dispatch the scaffold task:

```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/TASK-SIMDECISIONS-SCAFFOLD.md \
  --model haiku --role bee --inject-boot
```

The scaffold task already has Q33NR safeguards applied. **Do NOT modify it.** Dispatch as written.

Expected runtime: 5-10 minutes. Poll for the response file:
```
.deia/hive/responses/20260411-SCAFFOLD-COMPLETE.md
```

Validate the response contains:
- "Directories created" section with verification
- "Files copied" section with per-file status
- "Smoke test result" — must be PASS (exit 0)

If the smoke test fails:
- Do NOT proceed to Step 5
- Read the "SMOKE TEST FAILURE" section of the scaffold response
- Write `.deia/hive/responses/20260410-Q33N-BLOCKED-SCAFFOLD.md` with the exact error
- Escalate to Q88N
- STOP

### Step 5 — Write the Handoff Briefing

When both the gap matrix and a PASSING scaffold response exist, write:
```
simdecisions/.deia/hive/coordination/BRIEFING-SIMDECISIONS-HANDOFF.md
```

The briefing must contain:

1. **Reference to gap matrix** — full path to the shiftcenter gap matrix response file
2. **IRE inheritance list** — extract from Section 3 of the gap matrix. Every `IRE` item with its impl file path and test file path. This is the copy list for the inheritance wave.
3. **IR closure wave plan** — organized by tier:
   - **P0 — Factory Infrastructure** (dispatch.py, run_queue.py, scheduler.py, BOOT.md, claude_cli_subprocess.py)
   - **P1 — Engine Core** (node types, DES loop, IR schema)
   - **P2 — Adapter Layer** (all adapters)
   - **P3 — Feature Layer** (remaining IR-NO-IMPL and IR-NO-TEST items)
4. **Standing orders for simdecisions Q33N** — copy verbatim from the Q33NR prompt (`.deia/hive/coordination/PROMPT-FACTORY-SELF-REFACTOR-001.md`, "Standing Orders for simdecisions Q33N" section)
5. **Q33NR safeguard carry-forward** — note that Phase 1 scaffold deliberately excluded secrets, and any future secrets inheritance requires explicit Q88N approval
6. **Three-currencies reminder** — CLOCK/COIN/CARBON on every response file

### Step 6 — Activate simdecisions Q33N

Dispatch the simdecisions Q33N from inside the new repo:

```bash
cd "C:/Users/davee/OneDrive/Documents/GitHub/simdecisions"
python src/simdecisions/adapters/cli/dispatch.py \
  .deia/hive/coordination/BRIEFING-SIMDECISIONS-HANDOFF.md \
  --model sonnet --role queen
cd "C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter"
```

If the simdecisions dispatch.py fails (its imports haven't been wired yet), this is expected — it's the next bee's job. Capture the error, note it in the Q33NR report, and mark the handoff as "BRIEFING WRITTEN — DISPATCH BLOCKED ON IMPORT FIX."

### Step 7 — Write the Q33NR Report to Q88N

Write to:
```
.deia/hive/responses/20260411-Q33NR-HANDOFF-REPORT.md
```

The report must contain:

1. **Phase completion status** — Phase 0 (survey): ✓/✗, Phase 1 (scaffold): ✓/✗, Phase 2 (handoff brief): ✓/✗, Phase 2b (Q33N activation): ✓/✗/BLOCKED
2. **Gap matrix summary** — total specs, IRE count, IR-NO-IMPL count, IR-NO-TEST count, IR-TEST-FAIL count, DEFERRED count
3. **Scaffold smoke test result** — PASS / FAIL with error if applicable
4. **Q33NR safeguards applied** — list the secrets-exclusion safeguard and any others you applied during orchestration
5. **Active blockers** — anything stopping the build from progressing
6. **CLOCK / COIN / CARBON** — aggregated across all phases you orchestrated

---

## Rules You Follow

- You do NOT write code
- You do NOT modify source files
- You do NOT dispatch worker bees without first applying the two-phase gate (write task → review → correct → dispatch)
- You MAY dispatch the pre-written `TASK-SIMDECISIONS-SCAFFOLD.md` without further review (Q33NR has already gated it)
- You MUST stop and escalate on any blocker rather than guessing a fix
- You MUST report CLOCK / COIN / CARBON in every response file
- You MAY apply additional safeguards if you detect risks — document them in the Q33NR report

---

## Acceptance Criteria

- [ ] Gap matrix response file exists and is validated
- [ ] Scaffold dispatched and response received
- [ ] Scaffold smoke test result recorded (PASS or detailed FAIL)
- [ ] If PASS: BRIEFING-SIMDECISIONS-HANDOFF.md written to `simdecisions/.deia/hive/coordination/`
- [ ] If PASS: simdecisions Q33N dispatch attempted and outcome recorded
- [ ] Q33NR handoff report written to `.deia/hive/responses/20260411-Q33NR-HANDOFF-REPORT.md`
- [ ] All response files contain CLOCK / COIN / CARBON

---

## Smoke Test (for Q88N verification)

```bash
test -f .deia/hive/responses/20260411-FACTORY-GAP-MATRIX.md && echo "GAP MATRIX: OK"
test -f .deia/hive/responses/20260411-SCAFFOLD-COMPLETE.md && echo "SCAFFOLD RESPONSE: OK"
test -f .deia/hive/responses/20260411-Q33NR-HANDOFF-REPORT.md && echo "HANDOFF REPORT: OK"
test -d "C:/Users/davee/OneDrive/Documents/GitHub/simdecisions" && echo "NEW REPO: OK"
```

---

## Constraints

- **Do NOT modify `TASK-SIMDECISIONS-SCAFFOLD.md`** — Q33NR gate-reviewed it
- **Do NOT dispatch a second survey bee** without Q88N approval
- **Do NOT carry secrets into `simdecisions`** — the Q33NR safeguard is binding
- **Do NOT mark any phase complete based on file existence alone** — validate content
- **If blocked, ESCALATE rather than improvise**

---

*TASK-Q33N-CONTINUE-FACTORY-SELF-REFACTOR — Q33NR → Q33N — 2026-04-10*
