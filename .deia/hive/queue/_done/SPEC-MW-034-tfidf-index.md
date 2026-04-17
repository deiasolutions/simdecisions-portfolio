# SPEC: TF-IDF Suggestion Index for Terminal

## Priority
P2

## Objective
Build a TF-IDF-based suggestion index for the terminal that analyzes command history to provide context-aware command suggestions. The index ranks commands based on term frequency-inverse document frequency scoring to surface relevant commands based on the current context.

## Context
The Mobile Workdesk terminal needs intelligent command suggestions to accelerate user workflows. TF-IDF (Term Frequency-Inverse Document Frequency) is a statistical measure that evaluates how relevant a command is to the current context based on historical usage patterns. This foundation enables the pill UI (MW-035) to display the most contextually relevant commands.

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/terminal/TerminalApp.tsx` — terminal component structure
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/services/terminal/shellCommands.ts` — existing command infrastructure
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:146` — task context in scheduler

## Dependencies
None (Phase 6 foundation task)

## Acceptance Criteria
- [ ] `TFIDFIndex` class in `hivenode/terminal/tfidf_index.py` with `fit()`, `suggest()`, and `update()` methods
- [ ] `fit(commands: list[str])` — builds TF-IDF model from command history
- [ ] `suggest(context: str, top_k: int = 5) -> list[tuple[str, float]]` — returns ranked suggestions with scores
- [ ] `update(new_command: str)` — incrementally updates index with new commands
- [ ] REST endpoint: `POST /api/terminal/suggest` — accepts context, returns suggestions
- [ ] REST endpoint: `POST /api/terminal/train` — accepts command history, rebuilds index
- [ ] Use scikit-learn or custom TF-IDF implementation (no external ML dependencies preferred)
- [ ] Command history stored in SQLite: `terminal_history` table (timestamp, command, context)
- [ ] Index persistence to disk (pickle or JSON) for fast restarts
- [ ] 12+ unit tests covering scoring, ranking, edge cases (empty history, single command, duplicates)
- [ ] Performance: `suggest()` completes in <50ms for 1000+ command history

## Smoke Test
- [ ] Fit index with 100 sample commands
- [ ] Query `suggest("file operations", top_k=3)` → returns ["ls", "cp", "mv"] with scores
- [ ] Update index with new command "grep pattern file.txt"
- [ ] Re-query — "grep" appears in suggestions for "search operations"
- [ ] 12+ tests pass with 100% coverage of TFIDFIndex class
- [ ] Endpoint `/api/terminal/suggest` returns JSON: `[{"command": "ls", "score": 0.85}, ...]`

## Model Assignment
sonnet

## Constraints
- Location: `hivenode/terminal/tfidf_index.py` (new file)
- Location: `hivenode/terminal/routes.py` — add endpoints (or create if new)
- Database: SQLite table `terminal_history` in hivenode.db
- No external ML libraries beyond stdlib (or scikit-learn if already in deps)
- Index persistence: JSON or pickle to `.data/terminal_tfidf.pkl`
- Max 400 lines for TFIDFIndex class
- Max 150 lines for tests
- TDD: tests first, then implementation
- All endpoints use `verify_jwt_or_local()` auth pattern
