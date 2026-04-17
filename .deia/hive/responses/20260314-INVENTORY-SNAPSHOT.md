# Inventory Snapshot — 2026-03-14 22:45

Source: PostgreSQL (Railway) via `_tools/inventory_db.py`

---

## Bugs (14 total: 9 OPEN, 1 FIXED, 4 junk)

| ID | Sev | Component | Title | Status | Resolved By |
|----|-----|-----------|-------|--------|-------------|
| BUG-001 | P1 | frontend | Test Bug | OPEN | |
| BUG-002 | P1 | terminal | Terminal mini-display echoing full chat content instead of status only | FIXED | TASK-023 |
| BUG-003 | P2 | text-pane | Chat copy button invisible until hover | OPEN | |
| BUG-004 | P1 | inventory | SQLite backlog DB wiped by concurrent OneDrive sync | OPEN | |
| BUG-005 | P1 | shell | Shell.test.tsx crash: vi.mock of relay_bus missing uid export | OPEN | |
| BUG-006 | P1 | shell | constants.test.ts expects APP_REGISTRY length 0, now has 9 entries | OPEN | |
| BUG-007 | P1 | shell | SpotlightOverlay.test.tsx: data-spotlight-overlay selector stale (3 failures) | OPEN | |
| BUG-008 | P1 | canvas | FileOperations.test.tsx: CloudAPIClient mock returns undefined (4 failures) | OPEN | |
| BUG-009 | P1 | hivenode | RAG integration test failure: test_index_repository_creates_records | OPEN | |

**Junk entries (should be cleaned up):** BUG-1281ef6d, BUG-77d85e15, BUG-91543d5f, BUG-f608e2b7, BUG-ff8b27a5 — all "Test Bug" with no real content.

---

## Backlog (103 total: 14 P0, 64 P1, 25 P2, 6 P3)

### P0 — Must Ship (14)

| ID | Category | Title | Notes |
|----|----------|-------|-------|
| BL-023 | enhancement | Shell reducer: swap/delete/merge fixes | |
| BL-043 | enhancement | BABOK interview bot (requirements elicitation) | |
| BL-056 | enhancement | Automated overnight build pipeline | |
| BL-058 | enhancement | Hivenode E2E + volumes + sync + shell | |
| BL-062 | enhancement | SQLite feature/bug/backlog CLI tool | |
| BL-065 | enhancement | SDEditor multi-mode (raw/preview/diff/code/process-intake) | |
| BL-066 | enhancement | Deployment wiring: repoint Vercel + Railway | |
| BL-067 | enhancement | HIVE.md: combined Q33NR + Q33N + BEE chain of command | |
| BL-070 | bug | Wire envelope handlers: to_explorer, to_ir, to_simulator | |
| BL-110 | enhancement | Status system alignment (kanban + dev cycle + inventory) | |
| BL-121 | enhancement | Port Properties Panel editing UI | Size: L. ~1500 lines |
| BL-123 | enhancement | Port RAG advanced modules (indexer, entities, BOK, synthesizer) | Size: XL. ~4530 lines |
| BL-124 | enhancement | Port PHASE-IR cli.py + __main__.py + domain vocab YAMLs | Size: M. ~1564 lines |
| BL-125 | enhancement | Port DES engine_routes.py | Size: S. ~265 lines |

### P1 — Should Ship (64)

| ID | Category | Title |
|----|----------|-------|
| BL-001 | spec-note | Merge rule: computed border alignment |
| BL-002 | enhancement | Seamless pane borders |
| BL-003 | enhancement | Expandable input overlay for terminal |
| BL-007 | enhancement | SPEC-IPC-001 full implementation |
| BL-020 | enhancement | Overflow scroll floaters |
| BL-021 | enhancement | Responsive pane content |
| BL-022 | enhancement | Scenario packages (starter EGG templates) |
| BL-026 | enhancement | Suspicious login notification |
| BL-027 | enhancement | Rate limiting on auth routes |
| BL-028 | enhancement | Pattern template wizard |
| BL-029 | enhancement | Gates 0-3 and Healing Loop (Grace protocol) |
| BL-030 | enhancement | Group mute for composite applets |
| BL-031 | enhancement | PII strip/reconstitute (proxy mode) |
| BL-032 | enhancement | Attention escalation (tab flash, notification) |
| BL-033 | enhancement | Scenario Version History / Alterverse branching |
| BL-034 | enhancement | Multi-user collaboration (WebSocket sync) |
| BL-035 | enhancement | LLM decode failover |
| BL-036 | enhancement | Scenario branching (Alterverse full) |
| BL-037 | enhancement | DES engine port |
| BL-038 | enhancement | OR-Tools solver integration |
| BL-039 | enhancement | Bot tokens (chat + utility/hivenode) |
| BL-040 | enhancement | First LinkedIn post (origin story) |
| BL-041 | enhancement | Create LinkedIn page |
| BL-042 | enhancement | Vertical tabs (tabPosition config flag) |
| BL-044 | enhancement | Incognito mode (pane-level ledger suppression) |
| BL-045 | enhancement | Voice interface (STT/TTS primitives) |
| BL-046 | enhancement | MCP server for DEIA BOK |
| BL-047 | enhancement | Trust level progression criteria |
| BL-051 | enhancement | PHASE-IR runtime port |
| BL-052 | enhancement | Conversational design mode (process-intake) |
| BL-057 | enhancement | Global Commons community repository |
| BL-060 | enhancement | EGG drop + tab negotiation + inflate |
| BL-061 | enhancement | Mail reader EGG app with LLM compose |
| BL-068 | enhancement | User settings sync to cloud + home volume |
| BL-069 | enhancement | Terminal up-arrow command history |
| BL-071 | enhancement | Kanban pane primitive |
| BL-072 | enhancement | Progress/Gantt pane primitive |
| BL-073 | enhancement | User Utility Dashboard |
| BL-079 | spec | Topic Tree Browser |
| BL-082 | spec | Localhost Deployment with ra96it JWT Recertification |
| BL-083 | spec | PM Dashboard Auto-Rollup |
| BL-085 | spec | Cost Storage Format and Model Rate Lookup Table |
| BL-088 | spec | Y.js Integration Layer (CRDT real-time sync) |
| BL-089 | spec | Presence Service |
| BL-090 | spec | Infinite Canvas Surface Primitive |
| BL-097 | enhancement | Port drawing-canvas applet |
| BL-098 | enhancement | Port frank-cli applet |
| BL-099 | enhancement | Port sidebar applet |
| BL-100 | enhancement | Port file-explorer applet |
| BL-102 | enhancement | Build git-panel applet |
| BL-103 | enhancement | Build git-sidebar applet |
| BL-104 | enhancement | Build search applet |
| BL-105 | enhancement | Build frank-sidebar applet |
| BL-107 | debt | Add p5.js npm dependency |
| BL-108 | debt | Wire appType text alias to text-pane |
| BL-109 | enhancement | Processing primitive (p5.js canvas runtime) |
| BL-114 | spec | Monaco relay_bus Integration |
| BL-118 | enhancement | Theme switching / color schema port |
| BL-119 | spec | Monaco Code Editor Applet Wrapper |
| BL-120 | enhancement | Set up gc.deiasolutions.org |
| BL-126 | enhancement | Connect kanban to new backlog process DB |
| BL-127 | enhancement | Pane-to-pane /connect command |
| BL-130 | enhancement | Bee heartbeat progress reporting |
| BL-131 | debt | SimulateMode.tsx exceeds 500-line limit |
| BL-133 | enhancement | ra96it SSO federation |
| BL-134 | enhancement | CSV fallback for inventory store |

### P2 — Nice to Have (25)

| ID | Category | Title |
|----|----------|-------|
| BL-004 | enhancement | Group mute for bus messages |
| BL-005 | enhancement | Focus manager |
| BL-006 | enhancement | Command bar zone (spotlight/palette) |
| BL-048 | enhancement | deia extract command |
| BL-049 | enhancement | Video walkthrough (5 min) |
| BL-050 | enhancement | Blog post: Why I built DEIA |
| BL-053 | enhancement | Pin chats to folders |
| BL-054 | enhancement | Star chats for favorites |
| BL-055 | enhancement | Global commons rating system |
| BL-074 | enhancement | Revisit RAG: FBB patterns |
| BL-075 | spec | eFone: Voice-Only Chat Channels |
| BL-076 | spec | eCamera: Video Layer |
| BL-077 | spec | Meeting Intelligence |
| BL-078 | spec | Per-User Project Recognition Model |
| BL-080 | spec | SC Keyboard Primitive |
| BL-081 | spec | Efemera Layout Personalization |
| BL-084 | spec | IR Density Per Exchange |
| BL-086-087, 091-093, 095-096 | spec/review | Various specs and reviews |
| BL-101 | enhancement | Port efemera-compose applet |
| BL-106 | enhancement | Build home applet |
| BL-111-117 | spec | Calendar, Playwright, code.shiftcenter, KB EGG |
| BL-122 | enhancement | Port Canvas Chatbot + Frank — **HOLD** (BL-127 /connect replaces) |
| BL-128 | enhancement | Topic-based pub/sub for relay bus |
| BL-129 | enhancement | Port Flow Designer — **DONE** (121 files, 29,174 lines) |
| BL-132 | debt | Duplicate task IDs (TASK-092 through TASK-103) |

### P3 — Someday (6)

| ID | Category | Title |
|----|----------|-------|
| BL-008 | enhancement | Pipe syntax for chaining pane outputs |
| BL-009 | enhancement | Macro recording and playback |
| BL-011 | icebox | expandMode shell-level pane property |
| BL-024 | icebox | Auto-collapse panes below minWidth |
| BL-025 | icebox | Pin/unpin pane toggle |
| BL-094 | spec | Meeting Room EGG |
