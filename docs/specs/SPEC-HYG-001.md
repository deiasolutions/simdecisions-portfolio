# SPEC-HYG-001: Centralized Identity & Path Resolution

## Objective
Unify Node ID generation and database path resolution to prevent state divergence and identity collisions between CLI and module-based hivenode startups.

## Current Issues (Evidence)
- **Contradiction 1:** `hivenode/config.py` uses `uuid.uuid4().hex[:12]` while `hivenode/cli.py` uses `secrets.token_hex(4)`.
- **Contradiction 2:** `simdecisions/database.py` defaults to `repo_root/.deia/efemera.db` while `hivenode/config.py` defaults to `~/.shiftcenter/efemera.db`.

## Deliverables
- [ ] New module `hivenode/identity.py` containing centralized `get_node_id()` and `get_storage_path(db_name: str)` logic.
- [ ] Refactor `hivenode/config.py` to import from `hivenode/identity.py`.
- [ ] Refactor `hivenode/cli.py` to remove duplicate `_create_config_if_needed` generation logic.
- [ ] Refactor `simdecisions/database.py` to use `hivenode.identity` for its default database path.

## Test Requirements
- [ ] Unit test: `get_node_id()` must return the SAME ID on subsequent calls if config.yml exists.
- [ ] Integration test: Verify `hivenode` started via CLI and `hivenode` started via `python -m hivenode` connect to the exact same physical `efemera.db`.

## Constraints
- No changes to `~/.shiftcenter/` path itself (preserve existing data).
- Preference: Maintain `node-` prefix.
- Follow Hard Rule 4: Keep `identity.py` under 500 lines.
