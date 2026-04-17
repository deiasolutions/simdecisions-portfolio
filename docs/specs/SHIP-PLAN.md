# SHIP PLAN: Current State → Production

**Date:** 2026-03-14
**Starting point:** 2,600+ tests, DES engine 97% ported, PHASE-IR 76%, Flow Designer ported (29,174 lines), shell 74%, canvas 42%, inventory on PostgreSQL, build queue operational, build monitor working.

---

## WAVE 0: CLEAN THE HOUSE (do first, before any features)

Everything from overnight needs to be committed, tested, and verified. No new features until the repo is clean.

| # | Task | Who | Est |
|---|------|-----|-----|
| 0.1 | Run full test suites (browser + hivenode + engine), report all failures | Q33NR | 30m |
| 0.2 | Fix import path failures from overnight ports | Haiku bees | 1-2h |
| 0.3 | Resolve file conflicts where multiple bees edited same files | Q33NR direct | 1h |
| 0.4 | Commit in logical groups, push to dev | Q33NR | 30m |
| 0.5 | Clean junk entries from bugs table (5 test bugs) | Q33NR direct | 5m |
| 0.6 | Move BL-043 (BABOK) from P0 to P2 | Q33NR direct | 1m |
| 0.7 | Verify BL-070 (envelope handlers) is actually done — diagnostic said 21 tests pass | Q33NR | 10m |
| 0.8 | Verify BL-065 (SDEditor 6 modes) works end-to-end | Q33NR | 10m |
| 0.9 | Verify BL-110 (status alignment) works | Q33NR | 5m |
| 0.10 | Verify flow designer port (29,174 lines) actually renders and works | Q33NR | 30m |

**Exit criteria:** All tests pass (or known failures logged as bugs). All overnight work committed. Repo is clean. We know exactly what works and what doesn't.

---

## WAVE 1: FINISH THE PORTS (complete what's half done)

No new features. Just finish porting what should have been ported completely.

| # | Task | BL | Lines | Model | Est |
|---|------|----|-------|-------|-----|
| 1.1 | Port Properties Panel (16 files, 6 accordion sections, full node editor) | BL-121 | ~2,669 | Sonnet | 2h |
| 1.2 | Port PHASE-IR CLI toolchain (13 subcommands) + domain vocab YAMLs | BL-124 | ~1,564 | Sonnet | 1.5h |
| 1.3 | Port PHASE-IR trace system (25 event types, JSONL export) + trace routes | BL-124 | ~548 | Haiku | 45m |
| 1.4 | Port PHASE-IR models.py + schema_routes.py + validate_schema.py | BL-124 | ~409 | Haiku | 30m |
| 1.5 | Port DES engine_routes.py | BL-125 | ~265 | Haiku | 20m |
| 1.6 | Port canvas missing node types (13 types: BPMN + annotations) | — | ~1,110 | Sonnet | 1.5h |
| 1.7 | Port canvas animation system (6 components) | — | ~749 | Haiku | 45m |
| 1.8 | Port canvas lasso selection + zoom controls + annotation badge | — | ~435 | Haiku | 30m |
| 1.9 | Port canvas test files (10 old test files) | — | ~2,348 | Haiku | 1h |
| 1.10 | Port RAG advanced: indexer service | BL-123 | ~3,060 | Sonnet | 2h |
| 1.11 | Port RAG advanced: entity vectors + Voyage AI + BOK services | BL-123 | ~1,497 | Sonnet | 1.5h |
| 1.12 | Port shell chrome: MenuBar + ShellTabBar + WorkspaceBar | — | ~906 | Sonnet | 1h |
| 1.13 | Port shell chrome: GovernanceProxy + SpotlightOverlay + PaneMenu | — | ~361 | Haiku | 30m |
| 1.14 | Port shell chrome: remaining (NotificationModal, ShortcutsPopup, LayoutSwitcher, PinnedPaneWrapper, MaximizedOverlay, dragDropUtils) | — | ~281 | Haiku | 30m |
| 1.15 | Port canvas chatbot dialect (.md file) + find chat-with-process spec | — | unknown | Haiku | 30m |
| 1.16 | Find and port kanban board component | BL-071 | unknown | Sonnet | 1h |

**Exit criteria:** Every module from the old repos that belongs in shiftcenter is ported. Zero "should have been ported but wasn't" items remain. Full test suites pass.

---

## WAVE 2: WIRE IT TOGETHER (integration, not features)

The pieces exist. Now connect them so they actually work end-to-end.

| # | Task | What it connects | Model | Est |
|---|------|-----------------|-------|-----|
| 2.1 | Wire Process 13 quality gates into dispatch pipeline | Spec validation → build → test → review. The thing that prevents garbage. | Sonnet | 2h |
| 2.2 | Wire canvas chatbot: terminal NL → LLM → to_ir → canvas renders nodes | The "describe and watch it build" demo | Sonnet | 1.5h |
| 2.3 | Wire properties panel to canvas: select node → properties show → edit → canvas updates | Full node editing loop | Sonnet | 1h |
| 2.4 | Wire flow designer to DES engine: load flow → /sim/start → events stream back | Actually simulate a process | Sonnet | 2h |
| 2.5 | Wire DES events to canvas: tokens move, nodes light up, resources change color | Visual simulation playback | Sonnet | 2h |
| 2.6 | Wire shell chrome: MenuBar renders, tabs switch workspaces, spotlight opens | App feels complete | Haiku | 1h |
| 2.7 | Wire tree-browser to real volume storage: home:// reads actual files | File browser works for real | Sonnet | 1h |
| 2.8 | Wire chat persistence: conversations save to volume, tree-browser lists them, click to reload | Chat history works | Sonnet | 1h |
| 2.9 | Wire canvas palette: drag from tree-browser → drop on canvas → node created | Drag-and-drop node creation | Haiku | 45m |
| 2.10 | Wire governance: GovernanceProxy shows approval modal on gate_enforcer warn/ask dispositions | Governance has a face | Haiku | 45m |

**Exit criteria:** A user can describe a process in chat, watch it build on the canvas, edit node properties, run a simulation, and see results — all in one session. Chat history persists. File browser reads real files. Governance gates work visually.

---

## WAVE 3: DEPLOY + HARDEN (make it accessible)

| # | Task | What it does | Model | Est |
|---|------|-------------|-------|-----|
| 3.1 | Repoint Vercel to shiftcenter/browser/, Railway to shiftcenter/hivenode/ | BL-066. Code goes live at dev.shiftcenter.com | Config | 1h |
| 3.2 | dev.shiftcenter.com DNS (Cloudflare CNAME) | Staging URL works | Config | 10m |
| 3.3 | Subdomain → EGG routing in App.tsx | chat.efemera.live → chat.egg, code.shiftcenter.com → code.egg, etc. | Haiku | 30m |
| 3.4 | Rate limiting on auth routes | BL-027. Can't go public without this. | Haiku | 30m |
| 3.5 | BL-085 cost storage format + model rate lookup table | Three currencies tracked with real values | Haiku | 1h |
| 3.6 | Cloud storage adapter verified end-to-end on Railway | cloud:// actually works on the deployed server | Sonnet | 1h |
| 3.7 | Volume sync: home:// ↔ cloud:// verified working | Data survives across devices | Sonnet | 2h |
| 3.8 | Smoke test suite against deployed URLs (Playwright) | Automated deploy verification | Sonnet | 1h |
| 3.9 | HTTPS + CORS configured correctly | Browser can talk to API without errors | Config | 30m |
| 3.10 | Error handling: user sees helpful messages, not stack traces | Production polish | Haiku | 1h |

**Exit criteria:** dev.shiftcenter.com loads, users can use it, data persists, security basics are in place, smoke tests pass after every deploy.

---

## WAVE 4: PRODUCT POLISH (make it not embarrassing)

| # | Task | What it does | Est |
|---|------|-------------|-----|
| 4.1 | Chat bubbles verified: user right, AI left, markdown, copy button, typing indicator, avatars, grouping | Chat looks like a product | 1h verify/fix |
| 4.2 | Terminal up-arrow command history | BL-069 | 30m |
| 4.3 | Seamless pane borders | BL-002 | 30m |
| 4.4 | Expandable terminal input | BL-003 | 30m |
| 4.5 | Theme verified: dark mode looks good, all var(--sd-*) working, no hardcoded colors | Visual consistency | 1h |
| 4.6 | Empty states: empty panes show helpful text, not blank boxes | UX polish | 30m |
| 4.7 | Loading states: panes show spinner while content loads | UX polish | 30m |
| 4.8 | Error states: pane shows error message if an applet fails to load | UX polish | 30m |
| 4.9 | canvas.egg.md verified: 5-pane layout, palette, properties, terminal, canvas | SimDecisions product renders correctly | 1h |
| 4.10 | chat.egg.md verified: 3-pane layout, tree-browser, text-pane, terminal | Chat product renders correctly | 30m |
| 4.11 | efemera.egg.md verified: chat with Efemera branding | Efemera product renders correctly | 30m |
| 4.12 | Keyboard shortcuts working: Escape protocol, Ctrl+Z undo, Ctrl+Shift+P command palette | Power user basics | 1h |

**Exit criteria:** Someone who isn't Dave can open the app, understand what they're looking at, and use it without instructions.

---

## WAVE 5: SHIP

| # | Task | What it does | Est |
|---|------|-------------|-----|
| 5.1 | Merge dev → main | Production deploy | 10m |
| 5.2 | Verify production URLs work (chat.efemera.live, code.shiftcenter.com, etc.) | Live check | 30m |
| 5.3 | Run full smoke test against production | Final verification | 30m |
| 5.4 | Global Commons Phase A: static content at deiasolutions.org (Federalist Papers, design tokens, ethics.yml defaults) | GC exists publicly | 2h |
| 5.5 | Landing page: what is ShiftCenter, one screenshot, sign up link | People can find you | 2h |
| 5.6 | First LinkedIn post | Tell the world | 30m |
| 5.7 | ra96it sign-up flow working end-to-end | New users can create accounts | Verify |
| 5.8 | BYOK flow verified: paste API key → chat works immediately | First-run experience | Verify |
| 5.9 | One complete demo video (5 min): describe process → watch it build → simulate → see results | Proof it works | 2h |

**Exit criteria:** A stranger can find the product, sign up, paste an API key, and use SimDecisions to describe, build, and simulate a process. The video shows the full flow.

---

## TIMELINE ESTIMATE

| Wave | Work | Calendar (with build queue) |
|------|------|-----------------------------|
| Wave 0: Clean | 4-5 hours | Day 1 (morning) |
| Wave 1: Ports | 15-17 hours bee time | Day 1-2 (overnight queue) |
| Wave 2: Wire | 13-14 hours bee time | Day 2-3 (overnight queue) |
| Wave 3: Deploy | 8-9 hours | Day 3-4 |
| Wave 4: Polish | 7-8 hours | Day 4-5 |
| Wave 5: Ship | 7-8 hours | Day 5-6 |

**6 days from clean repo to shipped product.** If the build queue runs overnight each night and you review/direct during the day.

That's aggressive but achievable. The code exists — this is porting, wiring, and polishing, not inventing.

---

## WHAT THIS SHIPS AS

SimDecisions: "Describe your process. Watch it build. Simulate it. See where it breaks."

One product. One URL. Governed agents, constitutional framework, simulation-before-execution. The thing nobody else has.

The chat app (Efemera) and the IDE (code.shiftcenter.com) ship as bonus EGG configurations of the same platform. Same deploy. Same code. Different face.

---

## RULES FOR THE BUILD

1. **Port first, build second.** If it exists in the old repo, PORT IT. Do not rebuild.
2. **Process 13 wired by Wave 2.** No more shipping without quality gates.
3. **Survey before every task.** No bee gets a task file without Q33N confirming what exists in the old repo first.
4. **Max 3 bees overnight.** Cost control.
5. **Heartbeats to build monitor.** Dave checks progress from his browser.
6. **Morning report every day.** Dave reviews before the next wave starts.
7. **NEEDS_DAVE items flagged immediately.** Don't guess. Don't fill from training data. Ask.
