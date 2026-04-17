# SPEC-FACTORY-SELF-REFACTOR-001
## Factory Self-Refactor → simdecisions Repo

**Spec ID:** SPEC-FACTORY-SELF-REFACTOR-001
**Created:** 2026-04-10
**Author:** Q88N + Mr. AI
**Status:** APPROVED — READY FOR DISPATCH
**Priority:** P0
**Type:** Bootstrap / Self-Build
**Blocks:** All simdecisions work

---

## Intent

The `shiftcenter` factory refactors itself into a new peer repo: `simdecisions`.

`simdecisions` is not a branch. It is not a subfolder. It is a sovereign repo that:
- Inherits every verified IRE from `shiftcenter`
- Stands up its own `.deia/hive/` factory infrastructure as its first act
- Finishes its own build using its own Q33N from that point forward

Q33NR fires the first shot from `shiftcenter`. Control transfers to `simdecisions`'s own Q33N once the scaffold and hive infrastructure are in place.

---

## Execution Chain

```
Q33NR (shiftcenter)
  └─▶ TASK-SURVEY-FACTORY-GAP-MATRIX  [Sonnet bee — shiftcenter hive]
        └─▶ gap_matrix.md produced
  └─▶ TASK-SIMDECISIONS-SCAFFOLD      [Haiku bee — shiftcenter hive]
        └─▶ new repo created, .deia/hive/ bootstrapped
  └─▶ TASK-FACTORY-HANDOFF-BRIEF      [Q33NR writes briefing for simdecisions Q33N]
        └─▶ simdecisions Q33N activated
              └─▶ IRE inheritance wave   [parallel Haiku bees — simdecisions hive]
              └─▶ IR closure waves       [Sonnet bees — simdecisions hive]
              └─▶ BAT verification pass  [BAT bee — simdecisions hive]
              └─▶ cutover declared
```

---

## Phase 0 — Survey (shiftcenter hive)

**Assigned bee:** Sonnet
**Task file:** `TASK-SURVEY-FACTORY-GAP-MATRIX.md`
**Output:** `.deia/hive/responses/20260411-FACTORY-GAP-MATRIX.md`

The survey bee reads the entire `shiftcenter` repo and produces a gap matrix.

### Gap Matrix Schema

```
| spec_id | spec_file | has_implementation | impl_file | has_test | test_file | test_passes | ire_status |
```

`ire_status` values:
- `IRE` — implementation exists, test exists, test passes
- `IR-NO-IMPL` — spec exists, no implementation
- `IR-NO-TEST` — implementation exists, no test
- `IR-TEST-FAIL` — implementation exists, test exists, test fails
- `DEFERRED` — explicitly deferred in spec frontmatter

### Survey Scope

The bee reads (in order):
1. All files under `docs/specs/` — catalogue every spec ID and its stated acceptance criteria
2. All files under `src/` — map each impl file to its parent spec
3. All files under `tests/` — map each test file to its parent impl
4. `.deia/hive/tasks/` and `.deia/hive/responses/` — identify completed task coverage
5. `engine/` — node types, adapters, dispatch chain
6. `hivenode/adapters/cli/` — dispatch.py, run_queue.py, scheduler.py

The bee does NOT modify any files. Research only.

### Gap Matrix Output Sections

1. **IRE items** — full list of confirmed executable specs with test evidence
2. **IR-NO-IMPL items** — specs with no implementation; prioritized P0/P1/P2/P3
3. **IR-NO-TEST items** — implementations with no test coverage
4. **IR-TEST-FAIL items** — regressions requiring fixes before transfer
5. **DEFERRED items** — explicitly parked; carry forward as DEFERRED stubs
6. **Summary counts** — total by status
7. **Recommended closure order** — P0 factory infra first, then engine, then adapters, then feature layer

---

## Phase 1 — Scaffold (shiftcenter hive, Haiku)

**Task file:** `TASK-SIMDECISIONS-SCAFFOLD.md`

### New Repo Structure

```
simdecisions/
├── .deia/
│   ├── hive/
│   │   ├── tasks/
│   │   │   └── _archive/
│   │   ├── responses/
│   │   ├── coordination/
│   │   └── scripts/
│   │       └── dispatch/
│   ├── processes/
│   ├── config/
│   │   └── injections/
│   │       ├── base.md
│   │       └── claude_code.md
│   └── BOOT.md
├── engine/
│   ├── des/
│   └── phase_ir/
├── src/
│   └── simdecisions/
│       └── adapters/
│           └── cli/
│               ├── dispatch.py
│               ├── run_queue.py
│               └── claude_cli_subprocess.py
├── hivenode/
│   └── adapters/
│       └── cli/
├── docs/
│   ├── specs/
│   ├── impl/
│   └── adr/
├── tests/
├── README.md
└── pyproject.toml
```

### Bootstrap Sequence (in order, no skipping)

1. Create repo directory at peer level to `shiftcenter`
2. Create `.deia/` hierarchy with all subdirs
3. Copy `BOOT.md` from `shiftcenter` — update repo name references to `simdecisions`
4. Copy all `.deia/processes/` files verbatim — processes are repo-agnostic
5. Copy `.deia/config/injections/` verbatim
6. Copy `dispatch.py`, `run_queue.py`, `claude_cli_subprocess.py` — these are the factory's heartbeat
7. Copy `engine/phase_ir/schema.py` and `engine/phase_ir/validation.py` — IR schema is foundational
8. Write `README.md` with one line: "simdecisions — process orchestration engine. Build in progress."
9. Write `pyproject.toml` with project name `simdecisions`, Python 3.13, no deps yet
10. Smoke test: `python src/simdecisions/adapters/cli/dispatch.py --help` must return without error

**Acceptance Criteria:**
- [ ] All directories created
- [ ] dispatch.py executes without import error
- [ ] BOOT.md present and references `simdecisions`
- [ ] `.deia/hive/tasks/` is writable
- [ ] Smoke test passes

---

## Phase 2 — Handoff Brief (Q33NR writes)

Q33NR writes `BRIEFING-SIMDECISIONS-HANDOFF.md` into `simdecisions/.deia/hive/coordination/`.

The briefing contains:
1. The gap matrix (full, by reference to response file path)
2. The IRE inheritance list — which files to copy verbatim from `shiftcenter` (no bee touches these)
3. The IR closure wave plan (see Phase 3)
4. Standing orders for `simdecisions` Q33N — she runs the build from here

Q33NR then dispatches simdecisions Q33N:
```
python simdecisions/src/simdecisions/adapters/cli/dispatch.py \
  simdecisions/.deia/hive/coordination/BRIEFING-SIMDECISIONS-HANDOFF.md \
  --model sonnet --role queen
```

From this point, `shiftcenter` hive is read-only reference. `simdecisions` hive owns the build.

---

## Artifact Conveyance Rule (Absolute)

**All `shiftcenter` artifacts carry forward into `simdecisions` — including secrets, logs, and specs.**

Artifacts that convey:
- All spec files, including those containing credentials, tokens, or account identifiers
- All log files (`.deia/bot-logs/`, `*.jsonl`, `*.log`) — full operational history transfers
- All response files, including cost telemetry
- All `.env` and secrets config files
- Every file in `.deia/` — processes, config, injections, coordination briefs

`simdecisions` is the successor. It inherits the full operational context of `shiftcenter`. History is an asset.

---

## Phase 3 — IRE Inheritance Wave (simdecisions Q33N, parallel Haiku)

## Phase 3 — IRE Inheritance Wave (simdecisions Q33N, parallel Haiku)

For every item with `ire_status: IRE` in the gap matrix:

1. Q33N copies the spec file to `simdecisions/docs/specs/`
2. Q33N copies the implementation file(s) to the correct path in `simdecisions/src/`
3. Q33N copies the test file(s) to `simdecisions/tests/`
4. BAT bee runs the test — must pass in the new repo context
5. If test passes → item confirmed IRE in simdecisions
6. If test fails → item demoted to `IR-NO-TEST`, enters IR Closure Wave

No bee modifies IRE-inherited files. Copy only. If a test fails after copy, the environment is the bug — fix the environment, not the code.

---

## Phase 4 — IR Closure Waves (simdecisions Q33N, Sonnet bees)

Prioritized by tier:

**P0 — Factory Infrastructure** (must close first; blocks everything else)
- dispatch.py full test coverage
- run_queue.py full test coverage
- scheduler.py (create if absent)
- claude_cli_subprocess.py adapter tests
- BOOT.md process validation

**P1 — Engine Core**
- All `op:` node types with implementation + test
- DES engine event loop coverage
- IR schema validation tests

**P2 — Adapter Layer**
- All adapter implementations with tests
- Headless adapter parity with CLI adapter

**P3 — Feature Layer**
- All remaining IR-NO-IMPL and IR-NO-TEST items from gap matrix

### Per-Item Closure Protocol (PROCESS-13)

For each IR item assigned to a bee:

1. **Validate Plan** — bee reads spec, writes a 3-sentence plan confirming understanding. Q33N reviews. No code until plan approved.
2. **Execute with Self-Check** — bee implements, runs round-trip validation: does the output match the acceptance criteria stated in the spec?
3. **BAT Validates** — separate BAT bee (not the builder) runs tests and marks IRE or flags regression.

Builder bee never tests own output. No exceptions.

---

## Phase 5 — BAT Verification Pass

BAT bee reads the full gap matrix (updated after each closure wave) and runs:
```bash
pytest tests/ -v --tb=short > .deia/hive/responses/20260411-BAT-FULL-PASS.md
```

Any failure → revision task written by Q33N → back to Phase 4.

When BAT reports 0 failures across all items that were `IRE` at inheritance time plus all newly closed IR items → cutover declared.

---

## Phase 6 — Cutover

Q33N writes `CUTOVER-COMPLETE.md` to `simdecisions/.deia/hive/responses/`:
- Date/time
- IRE count (inherited + newly closed)
- DEFERRED count (carried as stubs)
- CLOCK / COIN / CARBON for full build

`shiftcenter` repo: frozen, not deleted. It is the holdout reference.
`simdecisions` repo: active. All future SimDecisions work dispatches from here.

---

## DEFERRED Items Protocol

Any IR item that cannot close in this build gets a stub file:
```
simdecisions/docs/specs/DEFERRED/SPEC-XXX-STUB.md
```

Stub contains:
- Original spec ID
- Why deferred
- What's needed to close it
- Estimated tier (P0/P1/P2/P3)

Deferred items are NOT forgotten. They are the next build's backlog.

---

## IRE Definition (Locked)

An item is IRE if and only if:
1. A PRISM-IR encoded spec node exists (or a spec file with PRISM-IR `intent:` field)
2. An implementation exists at the correct path
3. A BAT-passing test exists that exercises the acceptance criteria

All three required. No partial credit. "Implementation exists" without a test is `IR-NO-TEST`, not IRE.

---

## Three Currencies — Full Build

All bees report CLOCK / COIN / CARBON in every response file.
Q33N aggregates to a build-level total in the cutover brief.
No currency omitted. No estimates — measured actuals only.

---

## Response Files Required

| Phase | File |
|-------|------|
| 0 | `shiftcenter/.deia/hive/responses/20260411-FACTORY-GAP-MATRIX.md` |
| 1 | `shiftcenter/.deia/hive/responses/20260411-SCAFFOLD-COMPLETE.md` |
| 2 | `simdecisions/.deia/hive/coordination/BRIEFING-SIMDECISIONS-HANDOFF.md` |
| 3 | `simdecisions/.deia/hive/responses/20260411-IRE-INHERITANCE-COMPLETE.md` |
| 4+ | `simdecisions/.deia/hive/responses/20260411-IR-CLOSURE-WAVE-{N}.md` |
| 5 | `simdecisions/.deia/hive/responses/20260411-BAT-FULL-PASS.md` |
| 6 | `simdecisions/.deia/hive/responses/20260411-CUTOVER-COMPLETE.md` |

---

*SPEC-FACTORY-SELF-REFACTOR-001 — Q88N + Mr. AI — 2026-04-10*
