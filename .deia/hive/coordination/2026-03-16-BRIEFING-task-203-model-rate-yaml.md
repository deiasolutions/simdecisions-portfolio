# BRIEFING: TASK-203 Model Rate YAML Config + Loader

**From:** Q88NR-bot (Mechanical Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-16
**Spec:** `.deia/hive/queue/2026-03-16-SPEC-TASK-203-model-rate-yaml-config.md`
**Task File:** `.deia/hive/tasks/2026-03-16-TASK-203-model-rate-yaml-config.md`

---

## Objective

Process SPEC-TASK-203 which requires creating a centralized YAML config for model pricing rates and a Python loader module.

## Context

The spec is already formatted as a complete task file with:
- Clear objective
- Full context (duplication in claude_cli_subprocess.py and llm/cost.py)
- Absolute file paths
- 3 deliverables (YAML, rate_loader.py, __init__.py)
- 8 test requirements (TDD)
- All constraints listed
- 6 acceptance criteria
- 8-section response file template

The task is ready to dispatch to a bee.

## Your Assignment

**Review the existing task file** at `.deia/hive/tasks/2026-03-16-TASK-203-model-rate-yaml-config.md`.

Verify it meets the mechanical review checklist:
- [ ] Deliverables match spec ✓
- [ ] File paths are absolute ✓
- [ ] Test requirements present (8 tests specified) ✓
- [ ] CSS uses var(--sd-*) only (N/A - Python task) ✓
- [ ] No file over 500 lines (constraint stated) ✓
- [ ] No stubs or TODOs (constraint: "all functions fully implemented") ✓
- [ ] Response file template present ✓

If checklist passes, **approve and dispatch one bee** (Haiku recommended for this straightforward implementation task):

```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-16-TASK-203-model-rate-yaml-config.md \
  --model haiku \
  --role bee \
  --inject-boot \
  --timeout 1200
```

## Expected Deliverables from Bee

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config\model_rates.yml` (5 models + default + carbon rate)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config\rate_loader.py` (4 functions, no stubs)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config\__init__.py` (exports 4 functions)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\config\test_rate_loader.py` (8+ tests)
5. Response file: `.deia/hive/responses/20260316-TASK-203-RESPONSE.md` (8 sections)

## Files to Monitor

Source files that will be affected later (not in this task, but by TASK-205):
- `hivenode/adapters/cli/claude_cli_subprocess.py` (PRICING dict will be replaced by rate_loader)
- `hivenode/llm/cost.py` (COST_PER_TOKEN dict will be replaced by rate_loader)

These migrations will happen in TASK-205 (next in queue).

## Constraints

- No file over 500 lines
- TDD — tests first
- No stubs
- YAML must use rates per million tokens (not per token)

## Success Criteria

Bee completes with:
- ✅ 8+ tests passing
- ✅ All 4 functions implemented (no stubs)
- ✅ Prefix matching works for model IDs
- ✅ Response file has all 8 sections

---

**Action Required:** Review task file, run mechanical checklist, approve and dispatch bee (Haiku), monitor completion, report results to Q88NR-bot.
