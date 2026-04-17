# SPEC-IDENTITY-001-unify-node-id: Unify Node ID Generation and DB Path Resolution

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

The system has two conflicting implementations for node ID generation (`uuid.uuid4().hex[:12]` in `config.py` vs `secrets.token_hex(4)` in `cli.py`) and two different default paths for `efemera.db` (`~/.shiftcenter/` in `config.py` vs `.deia/` in `database.py`). This causes state divergence depending on how hivenode is started. Consolidate identity and path resolution into a single authoritative module and update all consumers.

## Files to Read First

- hivenode/config.py
- hivenode/cli.py
- simdecisions/database.py
- hivenode/main.py

## Acceptance Criteria

- [ ] New module `hivenode/identity.py` exists with `get_node_id()` and `get_db_path(db_name: str)` functions
- [ ] `get_node_id()` uses a single generation strategy (either uuid or secrets, not both) and caches the result after first generation to `~/.shiftcenter/config.yml`
- [ ] `get_node_id()` returns the same ID on repeated calls if config.yml already has one
- [ ] `get_db_path()` resolves to a single canonical location for each database name
- [ ] `hivenode/config.py` imports `get_node_id` from `hivenode/identity.py` instead of inline uuid generation (line 161)
- [ ] `hivenode/cli.py` imports `get_node_id` from `hivenode/identity.py` instead of inline secrets generation (line 434)
- [ ] `simdecisions/database.py` does NOT import from hivenode — instead it accepts a `db_path` parameter with no default, and callers pass the path from hivenode.identity
- [ ] No circular dependency between simdecisions/ and hivenode/ packages
- [ ] All existing tests still pass
- [ ] 4+ new tests: idempotent node ID, config.yml persistence, db_path resolution, no cross-package import in simdecisions/

## Smoke Test

- [ ] Start hivenode via `python -m uvicorn hivenode.main:app`, note node ID in logs
- [ ] Start hivenode via `python -m hivenode` (CLI), verify same node ID appears

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- simdecisions/ must NOT depend on hivenode/ (engine is independent of runner)
- Preserve existing data in `~/.shiftcenter/` — do not move or delete existing config files
- Preserve `node-` prefix convention
