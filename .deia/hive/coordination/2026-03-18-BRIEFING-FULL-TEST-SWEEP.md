# Briefing: Full Test Sweep — Post-30-Item Build

## Objective
Run the complete test suite across all layers and report what's passing and what's broken. This is a health check after the 30-item overnight build.

## What To Do

1. Run hivenode tests: `python -m pytest tests/hivenode/ -q`
   - If import errors block collection, skip the broken module and run the rest: `python -m pytest tests/hivenode/ -q --ignore=tests/hivenode/rag`
   - Then separately try: `python -m pytest tests/hivenode/rag/ -q`

2. Run browser tests: `cd browser && npx vitest run`

3. Run engine tests: `python -m pytest engine/ -q`

4. Run queue tests: `python -m pytest .deia/hive/scripts/queue/tests/test_run_queue.py .deia/hive/scripts/queue/tests/test_run_queue_heartbeat.py .deia/hive/scripts/queue/tests/test_dispatch_handler.py -q`

## Known Issues
- `tests/hivenode/rag/test_models.py` has an import error: `ReliabilityMetadata` not found in `hivenode/rag/indexer/models.py` — likely a bee output that didn't land
- Queue tests: 52 passed (already verified)

## Report Format
For each test suite:
- Total passed / failed / errors
- List every failing test name and a 1-line reason
- List every import/collection error

Write response to: `.deia/hive/responses/20260318-FULL-TEST-SWEEP-REPORT.md`
