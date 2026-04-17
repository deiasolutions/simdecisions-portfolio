# SPEC-APPLY-INJECT-01: Apply Model-Specific Prompt Injection

## Priority
P1

## Model Assignment
haiku

## Depends On
None

## Intent
Verify and apply the code changes from SPEC-INJECT-01 (Model-Specific Prompt Injection). A bee already wrote the code — this spec verifies it works. The bee added `load_injection()` to dispatch.py and created `.deia/config/injections/base.md` + `claude_code.md` for model-specific behavioral guardrails prepended at dispatch time.

## Files to Read First
.deia/hive/responses/20260406-QUEUE-TEMP-SPEC-INJECT-01-model-prompt-shims-RESPONSE.md
.deia/hive/scripts/dispatch/dispatch.py
.deia/config/injections/base.md
.deia/config/injections/claude_code.md

## Acceptance Criteria
- [ ] `dispatch.py` contains `load_injection()` function
- [ ] `load_injection()` returns base.md + model-specific .md content concatenated
- [ ] Model map routes sonnet/haiku/opus to claude_code.md
- [ ] Missing model files return base.md content only (graceful fallback)
- [ ] `dispatch_bee()` prepends injection before task content with `---` separator
- [ ] `INJECTIONS_DIR` global is set correctly in `main()`
- [ ] `base.md` exists with universal hive dispatch rules
- [ ] `claude_code.md` exists with CC-specific behavioral overrides
- [ ] Injection content is read from disk on each dispatch (no caching)

## Constraints
- Do NOT modify any code. Verification only.
- If any function is missing or broken, document it but do NOT attempt fixes.
- No git operations.

## Smoke Test
Read `dispatch.py` and verify `load_injection()` exists. Read both injection .md files and verify they contain meaningful content. Verify `dispatch_bee()` calls `load_injection()` and prepends the result.
