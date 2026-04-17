# SPEC: Context Weighting Logic for Terminal Suggestions

## Priority
P2

## Objective
Implement context-aware weighting logic that combines TF-IDF scores with runtime context signals (active pane, recent commands, workspace state) to produce more relevant command suggestions. This bridges the backend TF-IDF index (MW-034) with the frontend pill UI (MW-035).

## Context
Pure TF-IDF scoring ranks commands based on historical patterns but doesn't account for real-time context like which pane is active, what files are open, or recent command sequences. Context weighting multiplies TF-IDF scores by context-specific boosts to surface more situationally relevant suggestions.

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-034-tfidf-index.md` — TF-IDF backend
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-035-pill-ui.md` — pill UI component
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/Shell.tsx` — shell state (active pane)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/terminal/TerminalApp.tsx` — terminal component
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:148` — task context in scheduler

## Dependencies
- MW-035 (pill UI component must exist to display weighted suggestions)

## Acceptance Criteria
- [ ] `ContextWeighter` class in `browser/src/services/terminal/contextWeighter.ts`
- [ ] `weight(suggestions: Suggestion[], context: RuntimeContext) -> Suggestion[]` method
- [ ] RuntimeContext includes: `activePane: string`, `recentCommands: string[]`, `openFiles: string[]`, `currentDirectory: string`
- [ ] Weighting rules:
  - Boost file commands (ls, cat, grep) by 1.5x if `activePane === 'text-pane'`
  - Boost git commands by 2x if `currentDirectory` contains `.git`
  - Boost recently used commands by 1.3x if in `recentCommands` (last 5)
  - Decay older commands by 0.9x per hour since last use
- [ ] Backend endpoint: `POST /api/terminal/suggest-weighted` — accepts TF-IDF suggestions + context, returns weighted results
- [ ] Frontend integration: `TerminalApp.tsx` calls weighted endpoint instead of raw TF-IDF
- [ ] Re-rank suggestions after weighting (sort by `tfidf_score * context_weight`)
- [ ] Log weighting decisions for debugging (console.debug in dev, no-op in prod)
- [ ] 10+ unit tests covering each weighting rule, edge cases (empty context, no active pane)
- [ ] Performance: weighting completes in <10ms for 50 suggestions

## Smoke Test
- [ ] Fetch TF-IDF suggestions: `[{command: "ls", score: 0.8}, {command: "git status", score: 0.7}]`
- [ ] Apply context: `{activePane: "text-pane", currentDirectory: "/repo/.git"}`
- [ ] Weighted results: `[{command: "git status", score: 1.4}, {command: "ls", score: 1.2}]` (git boosted)
- [ ] Pills render in new order (git status first)
- [ ] 10+ tests pass with 100% coverage of weighting logic

## Model Assignment
sonnet

## Constraints
- Location: `browser/src/services/terminal/contextWeighter.ts` (new file)
- Location: `hivenode/terminal/routes.py` — add `/api/terminal/suggest-weighted` endpoint
- Integration: modify `TerminalApp.tsx` to use weighted suggestions
- Max 300 lines for weighter class + endpoint
- Max 150 lines for tests
- TDD: tests first, then implementation
- All backend endpoints use `verify_jwt_or_local()` auth pattern
