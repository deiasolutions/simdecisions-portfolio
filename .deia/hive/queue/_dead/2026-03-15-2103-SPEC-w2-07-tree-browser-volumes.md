# SPEC: Wire tree-browser to real volume storage home reads files

## Priority
P1.15

## Model Assignment
sonnet

## Objective
Wire tree-browser to volume storage: home:// protocol reads actual files from the volume system. List directories, read files, show file sizes and dates. Connect volumeAdapter to real backend.

## Acceptance Criteria
- [ ] home:// lists real directories
- [ ] File contents load in text-pane
- [ ] File metadata (size, date) displayed
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-2103-SPEC-w2-07-tree-browser-volumes", "status": "running", "model": "sonnet", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it to prevent conflicts with other bees:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-15-2103-SPEC-w2-07-tree-browser-volumes", "files": ["path/to/file1.py", "path/to/file2.py"]}
2. If response has conflicts (ok=false), you are queued FIFO. Poll GET http://localhost:8420/build/claims every 30s until the file is yours.
3. When done with a file, release it early so other bees can proceed:
   POST http://localhost:8420/build/release with JSON:
   {"task_id": "2026-03-15-2103-SPEC-w2-07-tree-browser-volumes", "files": ["path/to/file1.py"]}
4. On heartbeat complete/failed, all your claims auto-release. Claims expire after 10 minutes.

## Smoke Test
- [ ] cd browser && npx vitest run src/primitives/tree-browser/
- [ ] No new test failures
