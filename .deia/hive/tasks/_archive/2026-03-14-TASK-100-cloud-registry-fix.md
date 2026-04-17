# TASK-100: Fix Cloud Registry Instantiation

## Objective
Fix VolumeRegistry line 160 to pass the correct parameters to CloudAdapter constructor.

## Context
The registry currently does:
```python
adapter = CloudAdapter(endpoint, bucket)
```
But CloudAdapter's constructor expects:
```python
def __init__(self, cloud_url: str, auth_token: str, queue_dir: str = "~/.shiftcenter/sync_queue/"):
```
This causes a TypeError at runtime when VolumeRegistry tries to create a cloud adapter.

## Dependencies
- **TASK-099 must be complete** (CloudAdapter is now sync)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\registry.py` (line ~160)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\cloud.py` (constructor signature)

## Deliverables
- [ ] Modify `hivenode/storage/registry.py` line ~160:
  - Pass `cloud_url` from volume config (e.g., `vol_config.get("cloud_url")` or env var `SHIFTCENTER_CLOUD_URL`)
  - Pass `auth_token` from volume config or env var `SHIFTCENTER_AUTH_TOKEN`
  - Pass `queue_dir` from volume config with default `~/.shiftcenter/sync_queue/`
- [ ] Add fallback to environment variables if config values missing
- [ ] Add test in `tests/hivenode/storage/test_registry.py` (or existing test file) — 3+ tests:
  - Registry creates CloudAdapter with correct params from config
  - Registry falls back to env vars when config missing
  - Registry raises clear error if neither config nor env var provided

## Constraints
- No file over 500 lines
- Do NOT change CloudAdapter constructor — fix the CALLER
- Do NOT hardcode URLs or tokens

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260314-TASK-100-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Model Assignment
haiku
