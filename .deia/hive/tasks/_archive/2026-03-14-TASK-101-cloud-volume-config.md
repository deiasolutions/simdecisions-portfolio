# TASK-101: Update Volume Config Schema for Cloud

## Objective
Add `cloud_url` and `auth_token` fields to the volume configuration schema so cloud volumes can be configured via YAML config or environment variables.

## Context
CloudAdapter needs `cloud_url` and `auth_token` to connect to the remote hivenode. The VolumeRegistry reads volume config from YAML. We need to add the cloud-specific fields to the config schema.

## Dependencies
- Can run in parallel with TASK-099 (no file overlap)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\config.py` (if it exists)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\registry.py` (how config is consumed)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\` (existing config YAML files)

## Deliverables
- [ ] If `hivenode/storage/config.py` exists, add cloud volume fields. If not, create it (~60 lines):
  - `cloud_url: str` — URL of remote hivenode (e.g., `https://api.shiftcenter.io`)
  - `auth_token: str` — JWT token for authentication
  - `queue_dir: str` — local path for offline write queue (default: `~/.shiftcenter/sync_queue/`)
  - Environment variable fallbacks: `SHIFTCENTER_CLOUD_URL`, `SHIFTCENTER_AUTH_TOKEN`
- [ ] Document the config fields with docstrings
- [ ] Add tests — 4+ tests:
  - Config loads cloud_url from YAML
  - Config falls back to env var when YAML missing
  - Config validates cloud_url is a valid URL
  - Default queue_dir is `~/.shiftcenter/sync_queue/`

## Constraints
- No file over 500 lines
- Do NOT store secrets in YAML files committed to git
- Environment variables are the primary secret source

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260314-TASK-101-RESPONSE.md`

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
