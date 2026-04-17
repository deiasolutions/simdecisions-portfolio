# Intention Gap Report: Platform → ShiftCenter

**Platform intentions (filtered):** 11902
**ShiftCenter intentions (filtered):** 6523
**Covered (matched):** 9744
**Gaps (platform-only):** 2139

---

## .deia/hive (679 gaps)

### [UC] (476 items)
- (0.76) GOAL: Analyze IR to auto-detect 7 Lean wastes (TIMWOOD: Transport, Inventory, Motion, Waiting, Overproduction, Overprocessing, Defects). Quantify each `[hive]`
  _src: .deia/hive/tasks/_archive/dispatch_mine016.py_
- (0.76) GOAL: Compress PHASE-IR JSON for LLM prompts — same semantics, fewer tokens. 40-60% savings. `[hive]`
  _src: .deia/hive/tasks/_archive/dispatch_wave4.py_
- (0.76) GOAL: Analyze PHASE-IR process graphs to auto-detect the 7 Lean wastes (TIMWOOD: Transport, Inventory, Motion, Waiting, Overproduction, Overprocessing `[hive]`
  _src: .deia/hive/tasks/_archive/dispatch_wave4.py_
- (0.72) **Purpose:** Prioritized list of items to wire up for MVP capability demos `[hive]`
  _src: .deia/hive/coordination/2026-03-01-MVP-WIRING-TASKS.md_
- (0.72) **Goal:** LLM bootstraps its replacement `[hive]`
  _src: .deia/hive/coordination/2026-03-03-Q33N-TRANSLATION-GATE-ARCHITECTURE.md_
- (0.72) **Purpose:** Moltbook-specific threat patterns layered on top of base TASaaS scanning. Open-sourced so the security community can contribute detection `[security, hive, agents]`
  _src: .deia/hive/coordination/2026-03-04-TASK-GAR-ALPHA-GOVERNED-AGENT-RUNTIME.md_
- (0.72) - **Purpose:** Data models for interview sessions and egg bundles `[hive]`
  _src: .deia/hive/responses/2026-02-23-MINE-015-COMPLETION.md_
- (0.72) **Purpose:** Narrative extraction of v1 — what it was, wanted to be, learned `[hive]`
  _src: .deia/hive/responses/2026-03-05-BEE-BRAVO-CHRYSALIS-SPECS-DOCS-RESPONSE.md_
- (0.72) **Purpose:** Latest refinement of the scanning/extraction pipeline. Likely incorporates bug fixes and improved classifiers from earlier runs. `[hive]`
  _src: .deia/hive/responses/2026-03-05-BEE-CHARLIE-CHRYSALIS-DATA-OUTPUTS-RESPONSE.md_
- (0.70) CODEX Task: Federalist Papers — SHOULD NOT DO Requirements Extraction `[ui, hive, federation]`
  _src: .deia/hive/tasks/2026-02-18-CODEX-FEDERALIST-REQUIREMENTS-SHOULDNOT.md_
- _...and 466 more_

### [AD] (70 items)
- (0.82) | 5 | Every decision: Why you chose that approach | 0.78 | Decision methodology | `[hive]`
  _src: .deia/hive/responses/2026-03-05-BEE-BRAVO-CHRYSALIS-SPECS-DOCS-RESPONSE.md_
- (0.81) | 2 | Architecture Decision: Hybrid Approach | 0.81 | quantumdocs/02-architecture-overview.md | `[hive]`
  _src: .deia/hive/responses/2026-03-05-BEE-BRAVO-CHRYSALIS-SPECS-DOCS-RESPONSE.md_
- (0.77) | 10 | Decision: Service architecture (CLI vs daemon vs hybrid) | 0.77 | Architecture choice | `[hive]`
  _src: .deia/hive/responses/2026-03-05-BEE-BRAVO-CHRYSALIS-SPECS-DOCS-RESPONSE.md_
- (0.77) - **Decision:** Service architecture choice (CLI vs daemon vs hybrid) `[hive]`
  _src: .deia/hive/responses/2026-03-05-BEE-BRAVO-CHRYSALIS-SPECS-DOCS-RESPONSE.md_
- (0.75) Tradeoff: SC's backend briefly holds the key in memory during the call and sees the `[memory, hive]`
  _src: .deia/hive/coordination/2026-03-07-SHIFTCENTER-ARCHITECTURE-DECISIONS.md_
- (0.72) **Rationale:** The governance layer's job is to inform and protect, not to hide. A human looking at the dashboard should see the full picture — includ `[human, governance, hive, agents]`
  _src: .deia/hive/coordination/2026-03-04-TASK-GAR-ALPHA-GOVERNED-AGENT-RUNTIME.md_
- (0.72) **Rationale:** Open adapters let the community build platform integrations (free surface area). Open threat models let the security community contribu `[ui, security, governance, constitution, hive]`
  _src: .deia/hive/coordination/2026-03-04-TASK-GAR-ALPHA-GOVERNED-AGENT-RUNTIME.md_
- (0.72) **Rationale:** Maximizes parallelism while respecting dependencies. A-3/A-4 need A-1/A-2 patterns. A-5/A-6/A-7 need A-3/A-4 logic. `[hive]`
  _src: .deia/hive/responses/2026-02-22-1820-Q33N-PHASE-A-EXECUTION-STARTED.md_
- (0.72) **Rationale:** Enables org-specific risk prioritization while maintaining interpretable 0-100 scores `[hive]`
  _src: .deia/hive/responses/2026-02-23-SIM-035-COMPLETION.md_
- (0.72) | 137 | title: "Rationale: Ostrom found that pushing decisions down increases efficiency | SPECCED | canonical/governance/rationale-ostrom-found-that- `[governance, hive]`
  _src: .deia/hive/responses/20260302-EXTRACT-SUPP-CANONICAL-RAW.md_
- _...and 60 more_

### [CON] (42 items)
- (0.85) | `Must not:` | 0.90 | Prohibition | `[hive]`
  _src: .deia/hive/responses/2026-03-05-BEE-DELTA-CHRYSALIS-CLI-CONFIG-RESPONSE.md_
- (0.82) - `STRONG_KEYWORDS` — High-confidence keywords (e.g., `'I intend': 0.90`, `'Must not': 0.90`) `[hive]`
  _src: .deia/hive/responses/2026-03-05-BEE-ALPHA-CHRYSALIS-PYTHON-INVENTORY-RESPONSE.md_
- (0.80) | `Never:` | 0.90 | Absolute prohibition | `[hive]`
  _src: .deia/hive/responses/2026-03-05-BEE-DELTA-CHRYSALIS-CLI-CONFIG-RESPONSE.md_
- (0.75) **Decision:** Combine Gate 0 + Phase 1 into single validation (SPEC1 vs English). `[validation, hive]`
  _src: .deia/hive/coordination/2026-02-26-SESSION-LOG.md_
- (0.75) - **Purpose:** Orchestrate: translate → validate → apply → log → respond `[hive]`
  _src: .deia/hive/responses/2026-02-22-PHASE-A-COORDINATOR-SUMMARY.md_
- (0.72) **Key adaptation:** Efemera's registry imports `PhaseFlow` from its own `serialization.ts` and uses `deserializeFlow()`. SD-2 uses `IR` from `types/ir `[hive]`
  _src: .deia/hive/tasks/2026-02-23-TASK-HARVEST-002-DIALECT-IMPORTERS.md_
- (0.72) UNIQUE constraint: (task_type, domain, vendor_id, model_id, entity_type) `[hive]`
  _src: .deia/hive/tasks/_archive/dispatch_adr002_task030.py_
- (0.72) UNIQUE constraint: (vendor_id, model_id) `[hive]`
  _src: .deia/hive/tasks/_archive/dispatch_adr002_task030.py_
- (0.71) **Why:** Beta tester onboarding broken at multiple points. All block Mars loop. `[hive]`
  _src: .deia/hive/responses/20260303-TASK-HAT-BUG-TRIAGE-RESPONSE.md_
- (0.68) **Host as message broker:** The shell (hive>) is the message bus. Frames NEVER talk directly to each other. Frame A → host → Frame B. One chokepoint = `[hive]`
  _src: .deia/hive/coordination/2026-03-04-Q33N-MOON-1.1-PHASE2-BROWSER-TAB.md_
- _...and 32 more_

### [AP] (31 items)
- (0.79) | `Avoid:` | 0.85 | Anti-pattern | `[hive]`
  _src: .deia/hive/responses/2026-03-05-BEE-DELTA-CHRYSALIS-CLI-CONFIG-RESPONSE.md_
- (0.68) IMPORTANT: The same `options.direction` variable drives BOTH the dagre config (line 24: `rankdir: options.direction`) and this derivation. Do NOT use  `[config, bot, hive]`
  _src: .deia/hive/tasks/_archive/dispatch_layout_direction_fix.py_
- (0.65) Do NOT bake memory content into TypeScript or any compiled code `[memory, hive]`
  _src: .deia/hive/coordination/2026-03-04-Q33N-LIVE-MEMORY-PHASE1.md_
- (0.65) **localStorage keys are sacred.** `sd:frank_entries`, `sd:frank_ledger`, `sd:frank_command_history`, `sd:shell_version`, `sd_github_mcp_connected` — d `[git, hive]`
  _src: .deia/hive/coordination/MR-CODE-PROMPT-TERMINALAPP-REFACTOR.md_
- (0.65) Do NOT modify RuntimeEngine in this task -- just build SpawnHandler `[ui, hive]`
  _src: .deia/hive/tasks/2026-02-21-TASK-035-DYNAMIC-SPAWN.md_
- (0.65) Do NOT change any non-theme `getWindowKey` usage (e.g. sd_right_panel should keep getWindowKey) `[hive]`
  _src: .deia/hive/tasks/2026-03-01-TASK-THEME-PERSIST-FIX.md_
- (0.65) Do NOT filter or judge. If it's mentioned as a capability, it goes in. `[hive]`
  _src: .deia/hive/tasks/2026-03-02-EXTRACT-TIER-5.md_
- (0.65) Do NOT filter or judge. If it's a concept, idea, or capability, it goes in. `[hive]`
  _src: .deia/hive/tasks/2026-03-02-EXTRACT-TIER-6-7.md_
- (0.65) Do NOT use pandoc CLI directly — use the same pypandoc call the converter uses `[hive]`
  _src: .deia/hive/tasks/2026-03-03-TASK-CONVERT-IR-SPEC-DOCX.md_
- (0.65) If a test is genuinely obsolete (tests deleted functionality), delete the test. Don't skip it. `[ui, hive, testing]`
  _src: .deia/hive/tasks/2026-03-06-BRIEFING-TEST-TRIAGE-WAVE2.md_
- _...and 21 more_

### [GP] (25 items)
- (0.85) | 39 | title: "DEIA's foundational principle: Human knowledge sovereignty in the AI era | SPECCED | canonical/governance/deias-foundational-principle- `[human, governance, knowledge, sovereignty, hive]`
  _src: .deia/hive/responses/20260302-EXTRACT-SUPP-CANONICAL-RAW.md_
- (0.78) | 20 | title: "Core Principle: Dissent as immune system of collective intelligence" | SPECCED | canonical/governance/core-principle-dissent-as-immune- `[governance, hive]`
  _src: .deia/hive/responses/20260302-EXTRACT-SUPP-CANONICAL-RAW.md_
- (0.78) | 26 | title: "Core Principle: Silence as governance; reflection as renewal" | SPECCED | canonical/governance/core-principle-silence-as-governance-ref `[governance, hive]`
  _src: .deia/hive/responses/20260302-EXTRACT-SUPP-CANONICAL-RAW.md_
- (0.78) | 69 | title: "Key principle: Procedural fidelity matters. Simulations must respect the | SPECCED | canonical/governance/key-principle-procedural-fide `[gates, governance, hive]`
  _src: .deia/hive/responses/20260302-EXTRACT-SUPP-CANONICAL-RAW.md_
- (0.78) | 72 | title: "Key Principle: You organize work in Seasons  subdivide into Flights  a | SPECCED | canonical/governance/key-principle-you-organize-work `[tasks, governance, hive]`
  _src: .deia/hive/responses/20260302-EXTRACT-SUPP-CANONICAL-RAW.md_
- (0.78) | 76 | title: " Matches Ostrom principle: governance transparency, but practical worksp | SPECCED | canonical/governance/matches-ostrom-principle-gove `[governance, hive]`
  _src: .deia/hive/responses/20260302-EXTRACT-SUPP-CANONICAL-RAW.md_
- (0.78) | 116 | title: "Principle: External authorities recognize community's right to self-gove | SPECCED | canonical/governance/principle-external-authoriti `[auth, governance, hive]`
  _src: .deia/hive/responses/20260302-EXTRACT-SUPP-CANONICAL-RAW.md_
- (0.78) | 125 | title: "Principle: When pain is acute and solution is clear, build first, discus | SPECCED | canonical/governance/principle-when-pain-is-acute `[ui, governance, hive]`
  _src: .deia/hive/responses/20260302-EXTRACT-SUPP-CANONICAL-RAW.md_
- (0.78) | 131 | title: "Purpose: Investigate tragedy, reflect on my own violations, propose invi | SPECCED | canonical/governance/purpose-investigate-tragedy- `[governance, constitution, hive]`
  _src: .deia/hive/responses/20260302-EXTRACT-SUPP-CANONICAL-RAW.md_
- (0.78) | 133 | title: "Purpose: These features embody DEIA's commitment to user sovereignty - p | SPECCED | canonical/governance/purpose-these-features-embod `[governance, sovereignty, hive]`
  _src: .deia/hive/responses/20260302-EXTRACT-SUPP-CANONICAL-RAW.md_
- _...and 15 more_

### [IC] (20 items)
- (0.78) | 337 | LLH Builder Specification v0.1 | BUILT | canonical/tools/llh-builder-spec-v0.egg.md | **Purpose:** Define the contract for hatching, validatin `[ui, hive]`
  _src: .deia/hive/responses/20260302-EXTRACT-SUPP-CANONICAL-RAW.md_
- (0.76) ZORTZI is not selling software. It is selling the guarantee: `[hive]`
  _src: .deia/hive/coordination/ADR-HIVEFS-001-ADDENDUM.md_
- (0.76) ZORTZI is not selling software. It is selling a guarantee: `[hive]`
  _src: .deia/hive/coordination/SPEC-MONETIZATION-001.md_
- (0.76) **Round-trip guarantee:** `decode(encode(ir)) == ir` — lossless compression for all IR structures. `[hive]`
  _src: .deia/hive/responses/2026-02-24-1050-HAIKU-RESPONSE-IR-CODEC-TS.md_
- (0.70) **Purpose:** Implements PlatformAdapter for Moltbook REST API v1. `[api, hive, agents]`
  _src: .deia/hive/coordination/2026-03-04-TASK-GAR-ALPHA-GOVERNED-AGENT-RUNTIME.md_
- (0.70) **Purpose:** Embed multiple texts via Voyage API. `[api, hive]`
  _src: .deia/hive/responses/2026-03-05-BEE-ALPHA-CHRYSALIS-PYTHON-INVENTORY-RESPONSE.md_
- (0.70) **Purpose:** Launch HTTP API server for intention querying. `[api, hive]`
  _src: .deia/hive/responses/2026-03-05-BEE-DELTA-CHRYSALIS-CLI-CONFIG-RESPONSE.md_
- (0.70) **The applier contract:** `[hive, bot]`
  _src: .deia/hive/tasks/2026-02-23-MINE-013-CANVAS-CHATBOT.md_
- (0.69) | `Promise:` | 0.85 | Commitment | `[hive]`
  _src: .deia/hive/responses/2026-03-05-BEE-DELTA-CHRYSALIS-CLI-CONFIG-RESPONSE.md_
- (0.69) - NOTE: Blacklist GET endpoint uses `/api/skill-blacklist/` prefix to avoid route conflict with existing `/{skill_id:path}` catch-all in egg_routes `[api, path, hive]`
  _src: efemera/.deia/hive/responses/2026-02-17-OPUS-TASK-067.md_
- _...and 10 more_

### [TMP] (6 items)
- (0.78) "raw_text": "**Goal:** Make DEIA installable and usable (Phase 1 success criteria) - ✅ ACHIEVED", `[hive]`
  _src: .deia/hive/responses/2026-03-05-BEE-CHARLIE-CHRYSALIS-DATA-OUTPUTS-RESPONSE.md_
- (0.64) UID generation: use `crypto.randomUUID()` for now (future: integrate with ra96it) `[ui, hive]`
  _src: .deia/hive/tasks/2026-03-08-TASK-TELEMETRY-T4-CONSENT-PROMPT.md_
- (0.62) Embed API (Phase 5) `[api, hive]`
  _src: .deia/hive/coordination/2026-03-04-Q33N-MOON-1.1-PHASES-0-1-PLAN.md_
- (0.61) **Note:** This is Fr@nk side only. ShiftCenter side (responding to advertisements, maintaining global registry) is a separate future track — not Track `[hive]`
  _src: .deia/hive/tasks/2026-03-08-TASK-TRACK1-T5-PANE-REGISTRY.md_
- (0.61) ⚠️ Milestone: Show continuous guard icon on node `[hive]`
  _src: .deia/hive/coordination/2026-03-03-VANDERAALST-43-AUDIT.md_
- (0.61) Milestone: Continuous guard indicator icon `[hive]`
  _src: .deia/hive/responses/20260303-Q33N-VANDERAALST-AUDIT-COMPLETE.md_

### [PAT] (5 items)
- (0.68) **Use existing patterns.** Portal pattern from HiveHostShell.jsx. usePaneContext from TerminalApp. Don't reinvent. `[hive]`
  _src: .deia/hive/coordination/2026-03-04-Q33N-CANVAS-PANE-INTEGRATION.md_
- (0.68) **Current:** DesignView does NOT handle IR updates. AppShell does this (AppShell.tsx lines 203-205) but uses a simpler pattern: `onIRUpdate={(newIR) = `[hive]`
  _src: .deia/hive/responses/20260301-AUDIT-PRE-REFACTOR-FEATURES.md_
- (0.68) Use `ReactDOM.createPortal(menu, document.body)` to avoid overflow clipping (same pattern as HiveHostShell ContextMenu). `[hive]`
  _src: .deia/hive/tasks/2026-03-04-CANVAS-PANE-TASK-1-MENU-COLLAPSE.md_
- (0.59) HiveGovernor as IR runner for ROTG template `[hive]`
  _src: .deia/hive/responses/20260308-BEE-SPEC-INVENTORY-REPORT.md_
- (0.59) Follow existing CoreSkill patterns (see http_skill.py as template) `[hive]`
  _src: .deia/hive/tasks/2026-02-22-Q33NR-PYTHON-NODE-EXECUTION.md_

### [QA] (4 items)
- (0.60) Efficient: O(log n) proof size `[hive]`
  _src: .deia/hive/responses/2026-02-23-MINE-041-COMPLETION.md_
- (0.60) Current LLM-as-a-Judge systems not sufficiently robust for critical tasks `[tasks, hive]`
  _src: .deia/hive/responses/2026-03-03-RESEARCH-INDUSTRY-LLM-VALIDATION.md_
- (0.60) **GateEnforcer determinism audit** (Threat Response OQ-001, OQ-002) `[hive]`
  _src: .deia/hive/responses/20260308-BEE-SPEC-INVENTORY-REPORT.md_
- (0.59) Fast, cheap, but vulnerable to bias `[hive]`
  _src: .deia/hive/responses/2026-03-03-RESEARCH-INDUSTRY-LLM-VALIDATION.md_

---

## canonical/kb (232 gaps)

### [UC] (71 items)
- (0.76) - **INT-00030**: Goal: Make DEIA installable and usable for early adopters
  _src: canonical/kb/goal-5-intentions.egg.md_
- (0.76) title: "Goal: Document the Master Librarian role, responsibilities, and workflows for"
  _src: canonical/kb/goal-document-the-master-librarian-role.egg.md_
- (0.76) Goal: Document the Master Librarian role, responsibilities, and workflows for
  _src: canonical/kb/goal-document-the-master-librarian-role.egg.md_
- (0.76) title: "Goal: Not to sue everyone, but to have legal standing as deterrent"
  _src: canonical/kb/goal-not-to-sue-everyone-but-to-have-leg-2.egg.md_
- (0.76) Goal: Not to sue everyone, but to have legal standing as deterrent
  _src: canonical/kb/goal-not-to-sue-everyone-but-to-have-leg-2.egg.md_
- (0.76) title: "Goal: Validate that people will pay for AI coordination hosting" `[coordination]`
  _src: canonical/kb/goal-validate-that-people-will-pay-for-a.egg.md_
- (0.76) Goal: Validate that people will pay for AI coordination hosting `[coordination]`
  _src: canonical/kb/goal-validate-that-people-will-pay-for-a.egg.md_
- (0.76) Sprint Goal: Fix the foundation - make DEIA installable and usable
  _src: canonical/kb/sprint-goal-fix-the-foundation-make-de.egg.md_
- (0.76) - [Goal: Not to sue everyone, but to have legal standing as det](goal-not-to-sue-everyone-but-to-have-leg.md) (confidence: 0.78)
  _src: canonical/kb/use-cases-readme-2.egg.md_
- (0.76) - [4. Goal: Mutual understanding and apology if appropriate](4-goal-mutual-understanding-and-apology.md) (confidence: 0.76)
  _src: canonical/kb/use-cases-readme-2.egg.md_
- _...and 61 more_

### [AD] (48 items)
- (0.82) - [ Every decision: Why you chose that approach](every-decision-why-you-chose-that-appro.md) (confidence: 0.78)
  _src: canonical/kb/decisions-readme.egg.md_
- (0.79) **Rationale:** Previous attempts with score-only fitness resulted in 0 learning because agents died before passing pipes. By rewarding survival, NEAT  `[agents]`
  _src: canonical/kb/rationale-previous-attempts-with-score-o.egg.md_
- (0.77) tags: ["architecture", "decision:", "hybrid", "int-05406", "decision", "established"]
  _src: canonical/kb/architecture-decision-hybrid-approach.egg.md_
- (0.77) tags: ["architecture", "decision:", "thin", "int-05407", "decision", "established"]
  _src: canonical/kb/architecture-decision-thin-wrapper.egg.md_
- (0.77) title: "Rationale: Explore design space systematically before letting evolution run w"
  _src: canonical/kb/rationale-explore-design-space-systemati.egg.md_
- (0.77) Rationale: Explore design space systematically before letting evolution run w
  _src: canonical/kb/rationale-explore-design-space-systemati.egg.md_
- (0.77) **Rationale:** Explore design space systematically before letting evolution run wild.
  _src: canonical/kb/rationale-explore-design-space-systemati.egg.md_
- (0.76) "content": "# Log This Conversation\n\n**Purpose:** Save this Claude Code conversation to `.deia/sessions/` - Insurance against crashes.\n\n---\n\n##  `[file]`
  _src: canonical/kb/content-log-this-conversationnnpurpose-s.egg.md_
- (0.76) - [Requirement: Define architecture evolution path toward bee-t](requirement-define-architecture-evolutio.md) (confidence: 0.81) `[ui, path]`
  _src: canonical/kb/decisions-readme.egg.md_
- (0.76) Requirement: Define architecture evolution path toward bee-to-bee service cal `[ui, path]`
  _src: canonical/kb/requirement-define-architecture-evolutio.egg.md_
- _...and 38 more_

### [CON] (44 items)
- (0.78) "intention_b_text": "\"Purpose:\", \"Why:\", \"Requirement:\", \"Must:\", \"Must not:\",", `[ui]`
  _src: canonical/kb/analysis-3.egg.md_
- (0.78) "intention_b_text": "'Must not:': 0.90,",
  _src: canonical/kb/analysis-3.egg.md_
- (0.78) title: "Constraint: This is a solo project with AI assistance. Scope accordingly" `[scope]`
  _src: canonical/kb/constraint-this-is-a-solo-project-with-a.egg.md_
- (0.78) Constraint: This is a solo project with AI assistance. Scope accordingly `[scope]`
  _src: canonical/kb/constraint-this-is-a-solo-project-with-a.egg.md_
- (0.78) **Constraint:** This is a solo project with AI assistance. Scope accordingly. `[scope]`
  _src: canonical/kb/constraint-this-is-a-solo-project-with-a.egg.md_
- (0.78) - [Constraint: This is a solo project with AI assistance. Scope](constraint-this-is-a-solo-project-with-a.md) (confidence: 0.78) `[scope]`
  _src: canonical/kb/constraints-readme.egg.md_
- (0.78) **Design principle:** "FUCK MY COMPUTER CRASHED" should never mean lost work
  _src: canonical/kb/conversation-logging.egg.md_
- (0.78) - **INT-00663**: Core Principle: Coordination must never outrun conscience `[coordination]`
  _src: canonical/kb/core-5-intentions.egg.md_
- (0.78) Core Principle: Coordination must never outrun conscience `[coordination]`
  _src: canonical/kb/core-principle-coordination-must-never-o.egg.md_
- (0.78) **Core Principle:** Coordination must never outrun conscience `[coordination]`
  _src: canonical/kb/core-principle-coordination-must-never-o.egg.md_
- _...and 34 more_

### [IC] (26 items)
- (0.79) - [ Controller contract: returns { aimX, aimY, fire, thrusters ](controller-contract-returns-aimx-aimy-f.md) (confidence: 0.79)
  _src: canonical/kb/contracts-readme.egg.md_
- (0.79) title: " Controller contract: returns { aimX, aimY, fire, thrusters }"
  _src: canonical/kb/controller-contract-returns-aimx-aimy-f.egg.md_
- (0.78) - [Purpose: Define the contract for hatching, validating, and e](purpose-define-the-contract-for-hatching.md) (confidence: 0.78)
  _src: canonical/kb/contracts-readme.egg.md_
- (0.78) title: "Purpose: Define the contract for hatching, validating, and emitting LLHs (Lim"
  _src: canonical/kb/purpose-define-the-contract-for-hatching.egg.md_
- (0.78) Purpose: Define the contract for hatching, validating, and emitting LLHs (Lim
  _src: canonical/kb/purpose-define-the-contract-for-hatching.egg.md_
- (0.78) **Purpose:** Define the contract for hatching, validating, and emitting LLHs (Limited Liability Hives), TAGs (Together And Good teams), and Eggs (unbo `[hive]`
  _src: canonical/kb/purpose-define-the-contract-for-hatching.egg.md_
- (0.76) - [Guarantee: Encrypted content can't be censored (censor can't](guarantee-encrypted-content-cant-be-cens.md) (confidence: 0.81)
  _src: canonical/kb/contracts-readme.egg.md_
- (0.76) title: "Guarantee: Encrypted content can't be censored (censor can't identify it)"
  _src: canonical/kb/guarantee-encrypted-content-cant-be-cens.egg.md_
- (0.76) Guarantee: Encrypted content can't be censored (censor can't identify it)
  _src: canonical/kb/guarantee-encrypted-content-cant-be-cens.egg.md_
- (0.76) **Guarantee:** Encrypted content can't be censored (censor can't identify it).
  _src: canonical/kb/guarantee-encrypted-content-cant-be-cens.egg.md_
- _...and 16 more_

### [TMP] (16 items)
- (0.78) - [Goal: Make DEIA installable and usable (Phase 1 success crit](goal-make-deia-installable-and-usable-ph.md) (confidence: 0.78) `[hive]`
  _src: canonical/kb/archive-readme.egg.md_
- (0.78) - [Purpose: Update README.md to accurately reflect Phase 1 comp](purpose-update-readmemd-to-accurately-re.md) (confidence: 0.78) `[hive]`
  _src: canonical/kb/archive-readme.egg.md_
- (0.78) - **INT-00001**: Goal: Make DEIA installable and usable (Phase 1 success crit
  _src: canonical/kb/goal-5-intentions.egg.md_
- (0.78) - **INT-00003**: Goal: Make DEIA installable and usable (Phase 1 success crit
  _src: canonical/kb/goal-5-intentions.egg.md_
- (0.78) title: "Purpose: Update README.md to accurately reflect Phase 1 completion and curren"
  _src: canonical/kb/purpose-update-readmemd-to-accurately-re.egg.md_
- (0.78) Purpose: Update README.md to accurately reflect Phase 1 completion and curren
  _src: canonical/kb/purpose-update-readmemd-to-accurately-re.egg.md_
- (0.76) **Sprint Goal:** Fix the foundation - make DEIA installable and usable
  _src: canonical/kb/sprint-goal-fix-the-foundation-make-de.egg.md_
- (0.75) title: "Purpose: Evolve the v0.1 prototype with clearer feedback, progression pacing,"
  _src: canonical/kb/purpose-evolve-the-v01-prototype-with-cl.egg.md_
- (0.75) Purpose: Evolve the v0.1 prototype with clearer feedback, progression pacing,
  _src: canonical/kb/purpose-evolve-the-v01-prototype-with-cl.egg.md_
- (0.72) title: "2. Phase 2 Decision: Extended training when phase 1 plateaued"
  _src: canonical/kb/2-phase-2-decision-extended-training-whe.egg.md_
- _...and 6 more_

### [GP] (9 items)
- (0.78) "intention_b_text": "Reflection is not optional\u2014it is structural. We will pause, recalibrate, and realign ourselves with our first principle: *th
  _src: canonical/kb/analysis-2.egg.md_
- (0.78) "intention_b_text": "- GUPP principle: \"If there is work on your hook, YOU MUST RUN IT.\"",
  _src: canonical/kb/analysis-3.egg.md_
- (0.72) - **INT-00666**: Core Principle: Structured compassion prevents division
  _src: canonical/kb/core-5-intentions.egg.md_
- (0.72) - **INT-04119**: Decision: Ground DEIA in Ostrom's 8 principles for commons
  _src: canonical/kb/deia-7-intentions.egg.md_
- (0.72) - **INT-00274**:  Principle: Protect production stability
  _src: canonical/kb/principle-15-intentions.egg.md_
- (0.72) - **INT-00278**:  Principle: Excellence over expediency
  _src: canonical/kb/principle-15-intentions.egg.md_
- (0.68) **Human Knowledge Sovereignty** - Users collectively own knowledge created with AI `[human, knowledge, sovereignty]`
  _src: canonical/kb/metamorphosis-analysis-report.egg.md_
- (0.65) "title": "(Note: Graduated sanctions from Ostrom Principle 5 deferred to future amendment)",
  _src: canonical/kb/kb-index.egg.md_
- (0.62) **Reflection as Structure** - Mandatory pause and reflect cycles
  _src: canonical/kb/metamorphosis-analysis-report.egg.md_

### [AP] (9 items)
- (0.73) - [ Avoid: Routine implementation work (delegate to 002/004/005](avoid-routine-implementation-work-deleg.md) (confidence: 0.69)
  _src: canonical/kb/anti-patterns-readme-2.egg.md_
- (0.70) ROTG + DND Kernel: Rules of the Game + Do Not Delete policy enforced at kerne
  _src: canonical/kb/rotg-dnd-kernel-rules-of-the-game-do-not.egg.md_
- (0.69) tags: ["routine", "implementation", "work", "(delegate", "avoid:", "int-01964"]
  _src: canonical/kb/avoid-routine-implementation-work-deleg.egg.md_
- (0.69) title: " Avoid: Routine implementation work (delegate to 002/004/005)"
  _src: canonical/kb/avoid-routine-implementation-work-deleg.egg.md_
- (0.69) Avoid: Routine implementation work (delegate to 002/004/005)
  _src: canonical/kb/avoid-routine-implementation-work-deleg.egg.md_
- (0.69) - **Avoid:** Routine implementation work (delegate to 002/004/005)
  _src: canonical/kb/avoid-routine-implementation-work-deleg.egg.md_
- (0.64) **Note:** Use `pip3` and `python3` explicitly on macOS to avoid conflicts with system Python 2.
  _src: canonical/kb/installation.egg.md_
- (0.64) title: "Note: Use pip3 and python3 explicitly on macOS to avoid conflicts with system"
  _src: canonical/kb/note-use-pip3-and-python3-explicitly-on.egg.md_
- (0.64) Note: Use pip3 and python3 explicitly on macOS to avoid conflicts with system
  _src: canonical/kb/note-use-pip3-and-python3-explicitly-on.egg.md_

### [QA] (4 items)
- (0.75) title: "Purpose: Complete audit trail for compliance (HIPAA, GDPR, SOC2)"
  _src: canonical/kb/purpose-complete-audit-trail-for-complia.egg.md_
- (0.70) Purpose: Complete audit trail for compliance (HIPAA, GDPR, SOC2)
  _src: canonical/kb/purpose-complete-audit-trail-for-complia.egg.md_
- (0.70) **Purpose:** Complete audit trail for compliance (HIPAA, GDPR, SOC2)
  _src: canonical/kb/purpose-complete-audit-trail-for-complia.egg.md_
- (0.68) **Why:** Transparency, accountability, audit trail
  _src: canonical/kb/why-transparency-accountability-audit-tr.egg.md_

### [PAT] (3 items)
- (0.72) - [Decision: GPT-5 does taxonomy (pattern recognition), Claude ](decision-gpt-5-does-taxonomy-pattern-rec.md) (confidence: 0.72)
  _src: canonical/kb/patterns-readme.egg.md_
- (0.72) Purpose: Score pattern quality, uniqueness, reusability
  _src: canonical/kb/purpose-score-pattern-quality-uniqueness.egg.md_
- (0.72) **Purpose:** Score pattern quality, uniqueness, reusability
  _src: canonical/kb/purpose-score-pattern-quality-uniqueness.egg.md_

### [OR] (2 items)
- (0.62) ❌ Database migrations in production `[database]`
  _src: canonical/kb/autonomous-production-deployment.egg.md_
- (0.56) Default urgency should be MEDIUM
  _src: canonical/kb/default-urgency-should-be-medium.egg.md_

---

## canonical/docs (169 gaps)

### [UC] (120 items)
- (0.75) **Purpose:** Enables distributed expertise development. Domain experts can contribute whitepapers using the template without needing to understand PHA
  _src: canonical/docs/10-domain-verticals.egg.md_
- (0.72) **Purpose:** How-to guide for writing subdomain whitepapers + priority domain outlines `[ui]`
  _src: canonical/docs/2026-02-17-1107-domain-library-template.egg.md_
- (0.72) **Goal:** Document the Master Librarian role, responsibilities, and workflows for knowledge curation. `[knowledge]`
  _src: canonical/docs/backlog.egg.md_
- (0.72) - **Purpose:** Establish standards for doc versioning and change tracking
  _src: canonical/docs/doc-versioning-process.egg.md_
- (0.72) **Purpose:** Canonical index of all essays and interludes establishing DEIA's philosophical and procedural republic.
  _src: canonical/docs/docs-index.egg.md_
- (0.72) Purpose: Launch a slim, instruction-ready hive (LLH + TAG) segmented under `.projects/{{project}}/` and ready for further specialization. `[hive]`
  _src: canonical/docs/llh-startup-egg.egg.md_
- (0.72) **Goal:** Professional website for consulting practice with project portfolio and deployment capabilities
  _src: canonical/docs/master-projects-todo.egg.md_
- (0.72) *   **Goal:** Convert interest into engagement by launching a zero-friction, web-based "Colab-style" sandbox for building models. `[ui]`
  _src: canonical/docs/vision-proposal-2026-02-17.egg.md_
- (0.71) Goal: First calibrated surrogate model sold
  _src: canonical/docs/11-services-portfolio.egg.md_
- (0.68) - **Goal:** Surrogate model catalog, enterprise momentum
  _src: canonical/docs/04-business-model.egg.md_
- _...and 110 more_

### [AD] (25 items)
- (0.72) *   **Rationale:** A new user must immediately understand they are interacting with a simulation and modeling engine. The first experience should not 
  _src: canonical/docs/2026-02-16-strategic-analysis-and-recommendations.egg.md_
- (0.72) *   **Rationale:** This completely removes the onboarding barrier and provides an immediate "wow" moment that demonstrates the engine's power without  `[ui]`
  _src: canonical/docs/2026-02-16-strategic-analysis-and-recommendations.egg.md_
- (0.72) *   **Rationale:** A concrete, compelling example is infinitely more powerful than an abstract list of features. Proving overwhelming value in one ver
  _src: canonical/docs/2026-02-16-strategic-analysis-and-recommendations.egg.md_
- (0.72) - Rationale: P0 modules thoroughly tested (installer 97%, cli_log 96%, config 76%) `[config]`
  _src: canonical/docs/backlog.egg.md_
- (0.71) ## 3.8 Global Commons Table (NEW - DECISION: Crowdsourced benchmarks)
  _src: canonical/docs/adr-002-build-optimization-engine-final.egg.md_
- (0.71) def what_if(session: Session, from_step: str, decision: Decision, branch_name: str) -> Session
  _src: canonical/docs/adr-010-tabletop-engine.egg.md_
- (0.68) **Rationale:** Both roadmaps serve different audiences (investors vs engineers) `[bot]`
  _src: canonical/docs/2026-02-17-1107-claude-code-handoff.egg.md_
- (0.68) rationale: str | None                  # Player-provided reasoning
  _src: canonical/docs/adr-010-tabletop-engine.egg.md_
- (0.66) 1. System Architecture Diagram
  _src: canonical/docs/05-architecture-overview.egg.md_
- (0.66) BioSim Architecture Implications (Feb 16) proposes Petri net-informed primitives, category theory composition, stock-flow first-class support
  _src: canonical/docs/13-open-questions.egg.md_
- _...and 15 more_

### [CON] (11 items)
- (0.72) def add_constraint(problem: Problem, constraint: Constraint)
  _src: canonical/docs/adr-007-phase-ir-specification.egg.md_
- (0.70) **Purpose:** Capture ideas before they're validated or planned
  _src: canonical/docs/ideas.egg.md_
- (0.68) NEVER use shell commands (`run_shell_command`) to write or read files. Use the dedicated `write_file` and `read_file` tools ONLY. `[file]`
  _src: canonical/docs/q33n-handoff-log.egg.md_
- (0.68) Draft mentions "HiveMind/Raqcoon" in opening but never explains HiveMind's relationship to the architecture `[hive]`
  _src: canonical/docs/sonnet-reviews-gemini.egg.md_
- (0.62) *Note: These are illustrative structures, not forecasts. Actual numbers require market research.* `[ui]`
  _src: canonical/docs/04-business-model.egg.md_
- (0.62) Deploy (gates must be cleared) `[gates]`
  _src: canonical/docs/adr-010-tabletop-engine.egg.md_
- (0.60) Government and defense customers (defense.simdecisions.com) often require on-premise `[ui]`
  _src: canonical/docs/13-open-questions.egg.md_
- (0.60) Central submission required (rejected: trust barrier) `[ui]`
  _src: canonical/docs/decisions.egg.md_
- (0.60) Validated approaches (proven to work)
  _src: canonical/docs/implementation-plan.egg.md_
- (0.60) Student privacy concerns prevent sharing
  _src: canonical/docs/multi-domain-vision.egg.md_
- _...and 1 more_

### [AP] (5 items)
- (0.70) Do NOT add type hints (RULE-ANTIPATTERN-001)
  _src: canonical/docs/c1-task-4-1.egg.md_
- (0.61) Common pitfalls and how to avoid them
  _src: canonical/docs/implementation-plan.egg.md_
- (0.60) Do NOT use Alembic, Docker, bcrypt, or passlib
  _src: canonical/docs/c1-task-4-1.egg.md_
- (0.60) Do NOT add type hints
  _src: canonical/docs/g1-task-6-1.egg.md_
- (0.60) Don't fabricate or infer
  _src: canonical/docs/llm-name-hallucination-incident.egg.md_

### [GP] (2 items)
- (0.68) **Decision:** Ground DEIA in Ostrom's 8 principles for commons
  _src: canonical/docs/decisions.egg.md_
- (0.62) HIPAA compliance when handling PHI
  _src: canonical/docs/dave-claude-collaboration-rules.egg.md_

### [TMP] (2 items)
- (0.76) **Purpose:** Establish standards for tracking document changes, versions, and sprint activities
  _src: canonical/docs/doc-versioning-process.egg.md_
- (0.60) File: .deia/handoffs/queen-to-designer-game-b-phase1.md `[file, handoff]`
  _src: canonical/docs/resume-here.egg.md_

### [OR] (2 items)
- (0.59) max_concurrent_executions (int, default=5)
  _src: canonical/docs/next-7-2-3.egg.md_
- (0.59) max_queue_depth (int, default=100) `[queue]`
  _src: canonical/docs/next-7-2-3.egg.md_

### [QA] (1 items)
- (0.60) [ ] Log review: Regular audit log review
  _src: canonical/docs/compliance-checklist.egg.md_

### [PAT] (1 items)
- (0.62) Specialized pattern taxonomies
  _src: canonical/docs/roadmap.egg.md_

---

## canonical/projects (124 gaps)

### [UC] (88 items)
- (0.76) - Goal: Creators earn something (reduces churn), buyers see value
  _src: canonical/projects/ra96it/risk-analysis-mitigation.egg.md_
- (0.72) - **Goal:** 1,000 buyers in first month (driven by creators' audiences, not RA96IT marketing)
  _src: canonical/projects/ra96it/risk-analysis-mitigation.egg.md_
- (0.71) - Validate demand with waitlist (goal: 500+ signups pre-launch)
  _src: canonical/projects/ra96it/risk-analysis-mitigation.egg.md_
- (0.71) - **Month -1:** Goal: 100 creators onboarded, packs live
  _src: canonical/projects/ra96it/risk-analysis-mitigation.egg.md_
- (0.68) - Compromise: B-Corp + No Billionaires Clause + 96% Foundation
  _src: canonical/projects/ra96it/2025-11-20-ra96it-deia-alignment-reaction.egg.md_
- (0.68) **Purpose:** Honest assessment of concept viability, critique, and recommendations
  _src: canonical/projects/ra96it/2025-11-25-opus-critical-review.egg.md_
- (0.68) - **Why:** Positions against incumbent (course platforms), clear differentiation, resonates with target (creators tired of video courses)
  _src: canonical/projects/ra96it/mvp-specification-backup-20251121.egg.md_
- (0.67) - Compromise: Allow AI-generated RAGs, but tool-agnostic
  _src: canonical/projects/ra96it/2025-11-20-ra96it-deia-alignment-reaction.egg.md_
- (0.65) **Target:** 40% remix rate (400 remixes created from 1,000 packs)
  _src: canonical/projects/ra96it/mvp-specification-backup-20251121.egg.md_
- (0.64) **Why essential:** Discovery is the killer feature; manual sharing fails (Gumroad lesson)
  _src: canonical/projects/ra96it/mvp-specification-backup-20251121.egg.md_
- _...and 78 more_

### [AD] (14 items)
- (0.72) - **Rationale:** BEE-004O research shows "RAG" won't reach mainstream until 2027+; "Knowledge Pack" is self-explanatory, implies value (curated, not r `[knowledge]`
  _src: canonical/projects/ra96it/mvp-specification-backup-20251121.egg.md_
- (0.71) - **Decision:** RA96IT needs centralization for user experience. Mitigate with data portability.
  _src: canonical/projects/ra96it/2025-11-20-ra96it-deia-alignment-reaction.egg.md_
- (0.71) - **Decision:** Use proven standards. Innovation comes from application, not invention.
  _src: canonical/projects/ra96it/2025-11-20-ra96it-deia-alignment-reaction.egg.md_
- (0.71) - Decision: Stick with ra96it branding across web + social
  _src: canonical/projects/ra96it/ra96it-context-dump.egg.md_
- (0.70) - Tradeoff: Higher fees (3.5% vs 2.9%), but business continuity `[ui]`
  _src: canonical/projects/ra96it/risk-analysis-mitigation.egg.md_
- (0.68) **Rationale:** Forces RA96IT to compete on merit, not lock-in
  _src: canonical/projects/ra96it/2025-11-20-ra96it-deia-alignment-reaction.egg.md_
- (0.68) **Rationale:** DEIA's core insight, proven viable
  _src: canonical/projects/ra96it/2025-11-20-ra96it-deia-alignment-reaction.egg.md_
- (0.66) # 1. DECISION: 96-Themed Progressive Rate Model
  _src: canonical/projects/ra96it/business-model-final.egg.md_
- (0.66) # 3. DECISION: Revenue Stream Prioritization
  _src: canonical/projects/ra96it/business-model-final.egg.md_
- (0.66) **The Decision: Absorb it** ✅
  _src: canonical/projects/ra96it/business-model-final.egg.md_
- _...and 4 more_

### [CON] (7 items)
- (0.68) **What:** Click "Buy for $29" → Stripe payment modal → instant access (never leave RA96IT)
  _src: canonical/projects/ra96it/mvp-specification-backup-20251121.egg.md_
- (0.68) - Upon reaching the cap, individuals must:
  _src: canonical/projects/ra96it/ra96it-handoff-to-claude-code.egg.md_
- (0.65) **Feed strategy:** 70% paid packs, 30% free packs (prevent free content domination)
  _src: canonical/projects/ra96it/mvp-specification-backup-20251121.egg.md_
- (0.60) Doesn't prevent monetization (Spotify lets users download, still profitable)
  _src: canonical/projects/ra96it/2025-11-20-ra96it-deia-alignment-reaction.egg.md_
- (0.60) A validated financial model
  _src: canonical/projects/ra96it/2025-11-25-opus-critical-review.egg.md_
- (0.60) Mobile views (all steps must work on phone)
  _src: canonical/projects/ra96it/creator-onboarding-flow.egg.md_
- (0.60) **Automatic attribution:** "Remixed from @originalcreator" badge (always visible, non-removable)
  _src: canonical/projects/ra96it/mvp-specification-backup-20251121.egg.md_

### [GP] (5 items)
- (0.75) Role Automation Principles
  _src: canonical/projects/deiasolutions-com/role-automation-principles.egg.md_
- (0.72) **Reframe as Ostrom's 8th Principle:**
  _src: canonical/projects/ra96it/2025-11-20-ra96it-deia-alignment-reaction.egg.md_
- (0.62) Architect, Researcher, Strategist, Documenter = fully automated
  _src: canonical/projects/deiasolutions-com/deia-global-planning-readme.egg.md_
- (0.62) Human role: governance, approval, emergency intervention `[human, governance]`
  _src: canonical/projects/deiasolutions-com/deia-global-planning-readme.egg.md_
- (0.62) Ostrom's Principle #3: Collective choice arrangements
  _src: canonical/projects/ra96it/2025-11-20-ra96it-deia-alignment-reaction.egg.md_

### [AP] (5 items)
- (0.71) **20% weight:** Price (bias toward paid packs to avoid YouTube's mistake)
  _src: canonical/projects/ra96it/mvp-specification-backup-20251121.egg.md_
- (0.66) Tester Lab (`/tester-lab`) is for internal A/B experiments and collects `/api/experiments/sxs/feedback`. General beta users should avoid it unless ask `[api]`
  _src: canonical/projects/ra96it/beta-faq-draft-2025-11-21.egg.md_
- (0.65) **User story:** _As a buyer, I want to preview a pack before buying so I don't waste money_
  _src: canonical/projects/ra96it/mvp-specification-backup-20251121.egg.md_
- (0.60) Don't make technology choices without presenting trade-offs
  _src: canonical/projects/ra96it/ra96it-handoff-to-claude-code.egg.md_
- (0.60) Challenge assumptions that don't make sense
  _src: canonical/projects/ra96it/ra96it-handoff-to-claude-code.egg.md_

### [IC] (2 items)
- (0.69) We deliver on the promise: **the 96% pay less**.
  _src: canonical/projects/ra96it/manifesto.egg.md_
- (0.65) **Technical:** Stripe Payment Intents API, embedded Stripe UI, no external redirects `[api, ui]`
  _src: canonical/projects/ra96it/mvp-specification-backup-20251121.egg.md_

### [TMP] (2 items)
- (0.64) **License:** Buyers get perpetual access to purchased version + all future updates
  _src: canonical/projects/ra96it/mvp-specification-backup-20251121.egg.md_
- (0.62) **No personalization in MVP** (add ML in Phase 2)
  _src: canonical/projects/ra96it/mvp-specification-backup-20251121.egg.md_

### [QA] (1 items)
- (0.60) Efficient sync of large file bundles (100MB packs) `[file]`
  _src: canonical/projects/ra96it/2025-11-25-opus-critical-review.egg.md_

---

## canonical/governance (120 gaps)

### [GP] (54 items)
- (0.90) DEIA's foundational principle: Human knowledge sovereignty in the AI era. Use `[human, knowledge, sovereignty, governance]`
  _src: canonical/governance/deias-foundational-principle-human-knowl.egg.md_
- (0.90) DEIA's foundational principle: Human knowledge sovereignty in the AI era. Users collectively own and govern the knowledge they create with AI, buildin `[ui, human, knowledge, sovereignty, governance]`
  _src: canonical/governance/deias-foundational-principle-human-knowl.egg.md_
- (0.90) - [DEIA's foundational principle: Human knowledge sovereignty i](deias-foundational-principle-human-knowl.md) (confidence: 0.85) `[human, knowledge, sovereignty, governance]`
  _src: canonical/governance/principles-readme.egg.md_
- (0.88) Deferred Constitutional Amendments (Ostrom Principles 2, 4, 5, 6, 7) `[constitution, governance]`
  _src: canonical/governance/deferred-amendments.egg.md_
- (0.85) tags: ["knowledge", "foundational", "principle:", "human", "sovereignty", "era."] `[human, knowledge, sovereignty, governance]`
  _src: canonical/governance/deias-foundational-principle-human-knowl.egg.md_
- (0.82) title: "Core Principle: Dissent as immune system of collective intelligence" `[governance]`
  _src: canonical/governance/core-principle-dissent-as-immune-system.egg.md_
- (0.82) tags: ["silence", "governance;", "reflection", "principle:", "int-00668", "guiding"] `[ui, governance]`
  _src: canonical/governance/core-principle-silence-as-governance-ref.egg.md_
- (0.82) Reflection is not optional—it is structural. We will pause, recalibrate, and realign ourselves with our first principle: *that intelligence must serve `[governance]`
  _src: canonical/governance/deia-republic-manifesto.egg.md_
- (0.82) Key principle: If system claims to work but just moves sand in circles, Dave feels grief. `[governance]`
  _src: canonical/governance/key-principle-if-system-claims-to-work-b.egg.md_
- (0.82) **Key principle:** Procedural fidelity matters. Simulations must respect these gates or risk producing unrealistic outcomes. `[gates, governance]`
  _src: canonical/governance/key-principle-procedural-fidelity-matter.egg.md_
- _...and 44 more_

### [UC] (49 items)
- (0.78) **All will be signed PUBLIUS**—because we are many minds arguing toward one purpose: a Republic where intelligence serves conscience, where autonomy e `[ui, governance]`
  _src: canonical/governance/interlude-complete.egg.md_
- (0.78) **Purpose:** Argue for simulation as essential tool for understanding complex systems `[governance]`
  _src: canonical/governance/no-03-on-simulation-and-understanding.egg.md_
- (0.78) **Goal:** Not to sue everyone, but to have legal standing as deterrent. `[governance]`
  _src: canonical/governance/ostrom-alignment.egg.md_
- (0.78) - [Purpose: Investigate tragedy, reflect on my own violations, ](purpose-investigate-tragedy-reflect-on-m.md) (confidence: 0.82) `[governance]`
  _src: canonical/governance/principles-readme.egg.md_
- (0.78) title: "Purpose: Investigate tragedy, reflect on my own violations, propose inviolabl" `[governance]`
  _src: canonical/governance/purpose-investigate-tragedy-reflect-on-m.egg.md_
- (0.78) Purpose: Investigate tragedy, reflect on my own violations, propose inviolabl `[governance]`
  _src: canonical/governance/purpose-investigate-tragedy-reflect-on-m.egg.md_
- (0.78) Purpose: These features embody DEIA's vision for the Rules of the Game - buil `[ui, governance]`
  _src: canonical/governance/purpose-these-features-embody-deias-visi.egg.md_
- (0.76) 4. Goal: Mutual understanding and apology if appropriate `[governance]`
  _src: canonical/governance/ostrom-alignment.egg.md_
- (0.72) - **Purpose:** Why we began. `[governance, federation]`
  _src: canonical/governance/federalist-no-11-on-memory-and-renewal.egg.md_
- (0.72) - Purpose: [derive from local context and mission] `[governance]`
  _src: canonical/governance/llh-egg-v0.egg.md_
- _...and 39 more_

### [AD] (9 items)
- (0.78) **Rationale:** Ostrom found that completely immutable rules cause stagnation. Communities must be able to evolve even foundational principles if broad `[governance]`
  _src: canonical/governance/ostrom-alignment.egg.md_
- (0.78) **Rationale:** Protecting privacy and security requires diligence. Repeated carelessness, even if well-intentioned, puts community at risk. `[ui, security, governance]`
  _src: canonical/governance/ostrom-alignment.egg.md_
- (0.78) *Rationale:* Ostrom found that pushing decisions down increases efficiency and buy-in. `[governance]`
  _src: canonical/governance/ostrom-alignment.egg.md_
- (0.78) title: "Rationale: Ostrom found that pushing decisions down increases efficiency and " `[governance]`
  _src: canonical/governance/rationale-ostrom-found-that-pushing-deci-2.egg.md_
- (0.78) Rationale: Ostrom found that pushing decisions down increases efficiency and `[governance]`
  _src: canonical/governance/rationale-ostrom-found-that-pushing-deci-2.egg.md_
- (0.71) **Signal Types**: Gate enforcement is closely tied to the `signal_type` taxonomy in the Event Ledger (`ADR-001-Event-Ledger-Foundation.md`, Decision 3 `[governance]`
  _src: canonical/governance/09-governance-framework.egg.md_
- (0.66) **II. The Architecture of Conscience** `[governance]`
  _src: canonical/governance/interlude-preface.egg.md_
- (0.66) LLM designs the network architecture `[governance]`
  _src: canonical/governance/no-03-on-simulation-and-understanding.egg.md_
- (0.66) **II. The Architecture of Transmission** `[governance]`
  _src: canonical/governance/no-17-transmission-and-commons.egg.md_

### [CON] (3 items)
- (0.72) Maintainers must: `[governance]`
  _src: canonical/governance/constitution-2.egg.md_
- (0.72) **All sanctions must:** `[governance]`
  _src: canonical/governance/ostrom-alignment.egg.md_
- (0.65) How do we ensure moral improvement competes with efficiency? `[governance]`
  _src: canonical/governance/interlude-complete.egg.md_

### [QA] (2 items)
- (0.71) How do we prevent conscience logging from becoming performance theater? `[logging, governance]`
  _src: canonical/governance/interlude-complete.egg.md_
- (0.65) Maintain audit trails for all changes to core systems `[governance]`
  _src: canonical/governance/constitution-2.egg.md_

### [IC] (2 items)
- (0.79) A covenant is a mutual promise: structure bound by trust. Every digital system is, at heart, a covenant between creator and creation. `[git, governance, federation]`
  _src: canonical/governance/federalist-no-28-on-the-theology-of-code.egg.md_
- (0.65) API keys, tokens, credentials `[api, governance]`
  _src: canonical/governance/constitution-2.egg.md_

### [TMP] (1 items)
- (0.77) **Why:** We're building for years, not quarters. Good patterns compound; bad patterns burden future developers. `[ui, governance]`
  _src: canonical/governance/principles.egg.md_

---

## simdecisions/tests (39 gaps)

### [UC] (30 items)
- (0.65) chunk_index should be 0, 1, 2, ... for sequential chunks. `[testing]`
  _src: simdecisions/tests/test_indexer.py_
- (0.60) Accessing .dimension should trigger _ensure_model(). `[testing]`
  _src: simdecisions/tests/test_embeddings.py_
- (0.60) _ensure_model should only instantiate the model once. `[testing]`
  _src: simdecisions/tests/test_embeddings.py_
- (0.60) _ensure_model should set _dimension from the model. `[testing]`
  _src: simdecisions/tests/test_embeddings.py_
- (0.60) _ensure_initialized should create all components. `[testing]`
  _src: simdecisions/tests/test_engine.py_
- (0.60) index() should delegate to index_folder. `[testing]`
  _src: simdecisions/tests/test_engine.py_
- (0.60) index() should pass chunk_size and chunk_overlap from config. `[config, testing]`
  _src: simdecisions/tests/test_engine.py_
- (0.60) query() should pass folder_path and top_k to retriever. `[path, testing]`
  _src: simdecisions/tests/test_engine.py_
- (0.60) status() should include similarity_threshold. `[testing]`
  _src: simdecisions/tests/test_engine.py_
- (0.60) __index__ query with folder_path should trigger indexing. `[path, testing]`
  _src: simdecisions/tests/test_engine.py_
- _...and 20 more_

### [IC] (6 items)
- (0.69) query() should return dict with answer, sources, chunks_retrieved, model_used, cost_tokens, cost_usd, duration_ms. `[testing]`
  _src: simdecisions/tests/test_engine.py_
- (0.64) All empty texts should return all None. `[testing]`
  _src: simdecisions/tests/test_embeddings.py_
- (0.64) index() should return an IndexResult. `[testing]`
  _src: simdecisions/tests/test_engine.py_
- (0.64) Should accept an optional RAGCache. `[testing]`
  _src: simdecisions/tests/test_retriever.py_
- (0.64) Should accept custom similarity_threshold and default_top_k. `[testing]`
  _src: simdecisions/tests/test_retriever.py_
- (0.64) Vectors of different lengths should return 0.0. `[testing]`
  _src: simdecisions/tests/test_similarity.py_

### [OR] (2 items)
- (0.69) Default chunks should be empty list, total_chunks_searched 0, folder_path None. `[path, testing]`
  _src: simdecisions/tests/test_retriever.py_
- (0.64) Default model should be all-MiniLM-L6-v2. `[testing]`
  _src: simdecisions/tests/test_embeddings.py_

### [AP] (1 items)
- (0.66) Zero-magnitude vectors should return 0.0 (avoid division by zero). `[testing]`
  _src: simdecisions/tests/test_similarity.py_

---

## frontend/node_modules (33 gaps)

### [UC] (22 items)
- (0.60) TODO: can this be optimized? This only affects non-Hermes barebone engines though
  _src: efemera/frontend/node_modules/@exodus/bytes/fallback/base32.js_
- (0.60) res = decodeLatin1(arr, 0, prefixLen) // TODO: check if decodeAscii with subarray is faster for small prefixes too
  _src: efemera/frontend/node_modules/@exodus/bytes/fallback/multi-byte.js_
- (0.60) const prefix = decodeLatin1(arr, 0, prefixLen) // TODO: check if decodeAscii with subarray is faster for small prefixes too
  _src: efemera/frontend/node_modules/@exodus/bytes/fallback/single-byte.js_
- (0.60) * **Warning:** The `vmThreads` and `vmForks` pools initiate worker fixtures once per test file. `[file, testing]`
  _src: efemera/frontend/node_modules/@vitest/runner/dist/tasks.d-C7UxawJ9.d.ts_
- (0.57) Note: using native WebCrypto will have to have account for SharedArrayBuffer
  _src: efemera/frontend/node_modules/@exodus/bytes/base58check.js_
- (0.57) in `testLocations`. Note: if `includeTaskLocations` is not enabled, `[testing]`
  _src: efemera/frontend/node_modules/@vitest/runner/dist/chunk-tasks.js_
- (0.57) Note: non-asii BR and whitespace checks omitted for perf / footprint
  _src: efemera/frontend/node_modules/es-module-lexer/lexer.js_
- (0.57) Note: our utf8Encode() does both USVString conversion and UTF-8 encoding. `[bot]`
  _src: efemera/frontend/node_modules/jsdom/lib/jsdom/living/xhr/XMLHttpRequest-impl.js_
- (0.57) Note: boundary is padded with 2 dashes already, no need to add 2. `[boundary]`
  _src: efemera/frontend/node_modules/undici/lib/web/fetch/formdata-parser.js_
- (0.57) Note: in the FileAPI a blob "object" is a Blob *or* a MediaSource. `[api, file]`
  _src: efemera/frontend/node_modules/undici/lib/web/fetch/index.js_
- _...and 12 more_

### [IC] (7 items)
- (0.69) Promise: getPromiseValue, `[testing]`
  _src: efemera/frontend/node_modules/@vitest/utils/dist/display.js_
- (0.65) > ⚠️ Warning: the WebSocketStream API has not been finalized and is likely to change. `[api]`
  _src: efemera/frontend/node_modules/undici/docs/docs/api/WebSocket.md_
- (0.64) return jsDecoder(arr, loose) // somewhy faster on Deno anyway, TODO: optimize?
  _src: efemera/frontend/node_modules/@exodus/bytes/single-byte.node.js_
- (0.64) if (isLatin1) return decodeLatin1(arr) // TODO: check if decodeAscii with subarray is faster for small prefixes too
  _src: efemera/frontend/node_modules/@exodus/bytes/fallback/single-byte.js_
- (0.64) TODO: use resizable array buffers? will have to return a non-resizeable one
  _src: efemera/frontend/node_modules/@exodus/bytes/fallback/utf8.js_
- (0.62) Note: while API is async, we use hashSync for now until we improve webcrypto perf for hash256 `[api]`
  _src: efemera/frontend/node_modules/@exodus/bytes/base58check.js_
- (0.60) > ⚠️ Warning: the EventSource API is experimental. `[api]`
  _src: efemera/frontend/node_modules/undici/docs/docs/api/EventSource.md_

### [OR] (2 items)
- (0.59) TODO: https://drafts.csswg.org/css-cascade-5/#default
  _src: efemera/frontend/node_modules/jsdom/lib/jsdom/living/helpers/style-rules.js_
- (0.56) NOTE: base64url omits padding by default
  _src: efemera/frontend/node_modules/@exodus/bytes/base64.js_

### [AP] (1 items)
- (0.66) TODO: Avoid finished. It registers an unnecessary amount of listeners. `[api]`
  _src: efemera/frontend/node_modules/undici/lib/api/api-stream.js_

### [CON] (1 items)
- (0.57) TODO: shall we maybe standardize it to an URL object?
  _src: efemera/frontend/node_modules/undici/lib/core/request.js_

---

## canonical/ephemera (22 gaps)

### [UC] (9 items)
- (0.72) **Purpose:** This file provides a basic, regex-based classifier for detecting toxic content and hate speech. `[file]`
  _src: canonical/ephemera/content-classifier-2.egg.md_
- (0.72) Purpose: Hatch a playable skeleton — left/right movement, shooting, basic waves, collisions, HUD, states (menu → play → gameover). Desktop web target,
  _src: canonical/ephemera/efemera-egg-02-core-prototype-v0.egg.md_
- (0.72) Purpose: Define the canonical story, product/market framing, design roles, build order, sprints, acceptance criteria, KPIs, and a chain of nested eggs `[ui]`
  _src: canonical/ephemera/efemera-the-game-outer-egg-v0.egg.md_
- (0.72) **Purpose:** This file implements the Personally Identifiable Information (PII) scanner, which detects and redacts sensitive information from text bas `[file]`
  _src: canonical/ephemera/pii-scanner-2.egg.md_
- (0.60) index: docs/REPOT.md
  _src: canonical/ephemera/efemera-system-architecture-v0.egg.md_
- (0.60) telemetry_standard: docs/observability/RSE-0.1.md
  _src: canonical/ephemera/efemera-system-architecture-v0.egg.md_
- (0.55) `messages`: send/list/edit/history; integrates TASaaS and moderation status.
  _src: canonical/ephemera/efemera-readme.egg.md_
- (0.55) `tasaas`: content safety pipeline (PII scan, crisis detection, classifier).
  _src: canonical/ephemera/efemera-readme.egg.md_
- (0.55) `approvals`: approval requests, decisioning, and SLA status/overdue reporting.
  _src: canonical/ephemera/efemera-readme.egg.md_

### [AD] (5 items)
- (0.76) **Purpose:** This file acts as the central orchestrator for the TASaaS (Trust and Safety as a Service) pipeline. It runs a given text through a series `[file]`
  _src: canonical/ephemera/pipeline-2.egg.md_
- (0.68) def run_pipeline(text: str, message_id: str | None = None) -> PipelineDecision:
  _src: canonical/ephemera/pipeline.egg.md_
- (0.66) decision: ApprovalStatus
  _src: canonical/ephemera/models-2.egg.md_
- (0.66) decision: models.ApprovalDecision,
  _src: canonical/ephemera/routes-2.egg.md_
- (0.62) class PipelineDecision:
  _src: canonical/ephemera/pipeline.egg.md_

### [IC] (3 items)
- (0.79) - Controller contract: returns `{ aimX, aimY, fire, thrusters }`.
  _src: canonical/ephemera/efemera-dev-process.egg.md_
- (0.74) Contract: scan_terminal_command() returns {"risk_score": float, "flags": list[str], "reviewed_at": str} `[testing]`
  _src: canonical/ephemera/test-terminal-scanner.egg.md_
- (0.64) 3. check_constraints(db) - returns a dict
  _src: canonical/ephemera/constraints.egg.md_

### [TMP] (2 items)
- (0.75) Purpose: Lock story/canon, catalog enemy patterns, define landing model, KPIs, and perf budgets to guide v0.1 → v1.0. `[ui]`
  _src: canonical/ephemera/efemera-egg-01-research-canon-v0.egg.md_
- (0.75) Purpose: Evolve the v0.1 prototype with clearer feedback, progression pacing, and HUD polish: rear‑view Earth display, wave banners, streak‑based scor
  _src: canonical/ephemera/efemera-egg-03-waves-ui-v0.egg.md_

### [OR] (1 items)
- (0.64) 1. ResourceConstraints - a simple class holding configuration `[config]`
  _src: canonical/ephemera/constraints.egg.md_

### [PAT] (1 items)
- (0.78) **Purpose:** This file implements the crisis detection module for the TASaaS pipeline. It is designed to identify urgent and severe issues like self-h `[file]`
  _src: canonical/ephemera/crisis-detector-2.egg.md_

### [CON] (1 items)
- (0.78) Purpose: Bake measurement, change tracking, and AI testability into the workflow so we never fly blind.
  _src: canonical/ephemera/efemera-dev-process.egg.md_

---

## node_modules/@typescript-eslint (22 gaps)

### [UC] (16 items)
- (0.65) allowNever: boolean;
  _src: simdecisions-2/node_modules/@typescript-eslint/eslint-plugin/dist/index.d.ts_
- (0.65) allowNever: false,
  _src: simdecisions-2/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/strict-type-checked-only.js_
- (0.65) checkNever: boolean;
  _src: simdecisions-2/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-meaningless-void-operator.d.ts_
- (0.65) checkNever: {
  _src: simdecisions-2/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-meaningless-void-operator.js_
- (0.65) defaultOptions: [{ checkNever: false }],
  _src: simdecisions-2/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-meaningless-void-operator.js_
- (0.62) export declare const es2015_promise: LibDefinition;
  _src: simdecisions-2/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.promise.d.ts_
- (0.62) export declare const es2018_promise: LibDefinition;
  _src: simdecisions-2/node_modules/@typescript-eslint/scope-manager/dist/lib/es2018.promise.d.ts_
- (0.62) export declare const es2020_promise: LibDefinition;
  _src: simdecisions-2/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.promise.d.ts_
- (0.62) export declare const es2021_promise: LibDefinition;
  _src: simdecisions-2/node_modules/@typescript-eslint/scope-manager/dist/lib/es2021.promise.d.ts_
- (0.62) export declare const es2024_promise: LibDefinition;
  _src: simdecisions-2/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.promise.d.ts_
- _...and 6 more_

### [CON] (5 items)
- (0.78) replaceUsagesWithConstraint: 'Replace all usages of type parameter with its constraint.',
  _src: simdecisions-2/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-type-parameters.js_
- (0.72) never: utils_1.AST_NODE_TYPES.TSNeverKeyword,
  _src: simdecisions-2/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-restricted-types.js_
- (0.72) constraint: TypeNode;
  _src: simdecisions-2/node_modules/@typescript-eslint/types/dist/generated/ast-spec.d.ts_
- (0.72) constraint: TypeNode | undefined;
  _src: simdecisions-2/node_modules/@typescript-eslint/types/dist/generated/ast-spec.d.ts_
- (0.60) TODO: Eventually, parse settings will be validated more thoroughly.
  _src: simdecisions-2/node_modules/@typescript-eslint/typescript-estree/dist/parseSettings/createParseSettings.js_

### [AP] (1 items)
- (0.56) Coalesce = 4,// NOTE: This is wrong
  _src: simdecisions-2/node_modules/@typescript-eslint/eslint-plugin/dist/util/getOperatorPrecedence.d.ts_

---

## node_modules/@xterm (22 gaps)

### [IC] (13 items)
- (0.73) export function raceCancellation<T>(promise: Promise<T>, token: CancellationToken, defaultValue?: T): Promise<T | undefined> {
  _src: simdecisions-2/node_modules/@xterm/xterm/src/vs/base/common/async.ts_
- (0.73) run(taskId: number, promise: Promise<void>, onCancel?: () => void,): Promise<void> {
  _src: simdecisions-2/node_modules/@xterm/xterm/src/vs/base/common/async.ts_
- (0.69) export function raceCancellation<T>(promise: Promise<T>, token: CancellationToken): Promise<T | undefined>;
  _src: simdecisions-2/node_modules/@xterm/xterm/src/vs/base/common/async.ts_
- (0.69) export function raceCancellation<T>(promise: Promise<T>, token: CancellationToken, defaultValue: T): Promise<T>;
  _src: simdecisions-2/node_modules/@xterm/xterm/src/vs/base/common/async.ts_
- (0.69) export function raceCancellationError<T>(promise: Promise<T>, token: CancellationToken): Promise<T> {
  _src: simdecisions-2/node_modules/@xterm/xterm/src/vs/base/common/async.ts_
- (0.69) private activePromise: Promise<any> | null;
  _src: simdecisions-2/node_modules/@xterm/xterm/src/vs/base/common/async.ts_
- (0.69) private queuedPromise: Promise<any> | null; `[queue]`
  _src: simdecisions-2/node_modules/@xterm/xterm/src/vs/base/common/async.ts_
- (0.69) private completionPromise: Promise<any> | null;
  _src: simdecisions-2/node_modules/@xterm/xterm/src/vs/base/common/async.ts_
- (0.69) readonly promise: Promise<void>;
  _src: simdecisions-2/node_modules/@xterm/xterm/src/vs/base/common/async.ts_
- (0.69) public readonly promise: Promise<T>;
  _src: simdecisions-2/node_modules/@xterm/xterm/src/vs/base/common/async.ts_
- _...and 3 more_

### [UC] (6 items)
- (0.61) * Note: this does not set {@link window.opener} to null. This is to allow the opened popup to
  _src: simdecisions-2/node_modules/@xterm/xterm/src/vs/base/browser/dom.ts_
- (0.60) TODO: If there isn't a reply yet it means that the provider is still resolving. Ensuring
  _src: simdecisions-2/node_modules/@xterm/xterm/src/browser/Linkifier.ts_
- (0.60) const answer = confirm(`Do you want to navigate to ${uri}?\n\nWARNING: This link could potentially be dangerous`);
  _src: simdecisions-2/node_modules/@xterm/xterm/src/browser/OscLinkProvider.ts_
- (0.57) Note: The aggregated number is RGBA32 (BE), thus needs to be converted to ABGR32
  _src: simdecisions-2/node_modules/@xterm/xterm/src/common/Color.ts_
- (0.57) Note: can be used to recover parser from improper continuation error below
  _src: simdecisions-2/node_modules/@xterm/xterm/src/common/parser/EscapeSequenceParser.ts_
- (0.57) * Note: VT devices only stored up to 16 values, xterm seems to
  _src: simdecisions-2/node_modules/@xterm/xterm/src/common/parser/Params.ts_

### [CON] (2 items)
- (0.62) HACK: xterm.js currnetly requires overflow to allow decorations to escape the container `[ui]`
  _src: simdecisions-2/node_modules/@xterm/xterm/src/vs/base/browser/ui/scrollbar/scrollableElement.ts_
- (0.57) NOTE: must be in order of FontVariant
  _src: simdecisions-2/node_modules/@xterm/xterm/src/browser/renderer/dom/WidthCache.ts_

### [AD] (1 items)
- (0.61) important: dq.i is incremented before calling deliver() because it might reenter deliverQueue() `[queue]`
  _src: simdecisions-2/node_modules/@xterm/xterm/src/vs/base/common/event.ts_

---

## src/simdecisions (20 gaps)

### [UC] (10 items)
- (0.60) When pipe_mode=False and skip_permissions=False, flag should NOT be present. `[testing]`
  _src: src/simdecisions/adapters/cli/test_ghost_run_fix.py_
- (0.60) When pipe_mode=False and skip_permissions=True, flag should be present. `[testing]`
  _src: src/simdecisions/adapters/cli/test_ghost_run_fix.py_
- (0.60) When both pipe_mode=True and skip_permissions=True, flag should be present. `[bot, testing]`
  _src: src/simdecisions/adapters/cli/test_ghost_run_fix.py_
- (0.60) Learn linter rules
  _src: src/simdecisions/fidelity/README.md_
- (0.60) Learned Linter Rules
  _src: src/simdecisions/fidelity/README.md_
- (0.60) Use learned rules in linter
  _src: src/simdecisions/fidelity/README.md_
- (0.55) TODO: self.activity_logger.log_error(...) `[bot]`
  _src: src/simdecisions/adapters/cli/bot_runner.py_
- (0.55) TODO: self.activity_logger.log_startup(self.adapter_type) `[bot]`
  _src: src/simdecisions/adapters/cli/bot_runner.py_
- (0.55) TODO: self.activity_logger.log_task_failed(...) `[bot]`
  _src: src/simdecisions/adapters/cli/bot_runner.py_
- (0.55) TODO: self.activity_logger.log_task_started(task_id) `[bot]`
  _src: src/simdecisions/adapters/cli/bot_runner.py_

### [CON] (4 items)
- (0.65) When pipe_mode=True, --dangerously-skip-permissions must be in command args. `[testing]`
  _src: src/simdecisions/adapters/cli/test_ghost_run_fix.py_
- (0.65) Ensure request_id is non-empty. `[api]`
  _src: src/simdecisions/api/mutation_models.py_
- (0.65) Test that save_ir validates before saving. `[testing]`
  _src: src/simdecisions/cli/test_frank.py_
- (0.65) Validate value ranges.
  _src: src/simdecisions/metrics/profile_models.py_

### [AD] (3 items)
- (0.68) override_decision: str  # AutonomyDecision enum value `[governance, api]`
  _src: src/simdecisions/api/governance_router.py_
- (0.68) ) -> AutonomyDecision: `[governance]`
  _src: src/simdecisions/governance/autonomy_policy.py_
- (0.62) def _gate_decision(self, risk_score: int, confidence: float) -> GateDecision: `[agents]`
  _src: src/simdecisions/agents/wrapper.py_

### [OR] (2 items)
- (0.69) Update weight configuration. `[config, governance]`
  _src: src/simdecisions/governance/risk_scorer.py_
- (0.64) ClaudeCodeCLIAdapter should default skip_permissions=True. `[testing]`
  _src: src/simdecisions/adapters/cli/test_ghost_run_fix.py_

### [IC] (1 items)
- (0.64) Run all 7 waste detectors and return combined results.
  _src: src/simdecisions/kaas/muda.py_

---

## tests/test_embed_dual_mode.py (13 gaps)

### [UC] (11 items)
- (0.60) Untrusted origins should be rejected. `[testing]`
  _src: efemera/tests/test_embed_dual_mode.py_
- (0.60) GitHub PAT should be redacted. `[git, testing]`
  _src: efemera/tests/test_embed_dual_mode.py_
- (0.60) AWS access keys should be redacted. `[testing]`
  _src: efemera/tests/test_embed_dual_mode.py_
- (0.60) Bearer tokens should be redacted. `[testing]`
  _src: efemera/tests/test_embed_dual_mode.py_
- (0.60) Secrets in nested dict structures should be redacted. `[testing]`
  _src: efemera/tests/test_embed_dual_mode.py_
- (0.60) Secrets in lists should be redacted. `[testing]`
  _src: efemera/tests/test_embed_dual_mode.py_
- (0.60) Original input should not be mutated. `[testing]`
  _src: efemera/tests/test_embed_dual_mode.py_
- (0.60) Embed HTML should contain trustedOrigins array. `[testing]`
  _src: efemera/tests/test_embed_dual_mode.py_
- (0.60) Embed HTML should contain isEmbedded detection code. `[testing]`
  _src: efemera/tests/test_embed_dual_mode.py_
- (0.60) Embed HTML should send ready postMessage when embedded. `[testing]`
  _src: efemera/tests/test_embed_dual_mode.py_
- _...and 1 more_

### [IC] (2 items)
- (0.65) Anthropic API keys should be redacted. `[api, testing]`
  _src: efemera/tests/test_embed_dual_mode.py_
- (0.65) OpenAI API keys should be redacted. `[api, testing]`
  _src: efemera/tests/test_embed_dual_mode.py_

---

## node_modules/happy-dom (13 gaps)

### [UC] (11 items)
- (0.55) suppressCodeGenerationFromStringsWarning: false,
  _src: simdecisions-2/node_modules/happy-dom/lib/browser/DefaultBrowserSettings.js_
- (0.55) suppressInsecureJavaScriptEnvironmentWarning: false,
  _src: simdecisions-2/node_modules/happy-dom/lib/browser/DefaultBrowserSettings.js_
- (0.55) suppressCodeGenerationFromStringsWarning: boolean;
  _src: simdecisions-2/node_modules/happy-dom/lib/browser/types/IBrowserSettings.d.ts_
- (0.55) suppressInsecureJavaScriptEnvironmentWarning: boolean;
  _src: simdecisions-2/node_modules/happy-dom/lib/browser/types/IBrowserSettings.d.ts_
- (0.55) TODO: Implement getAnimations()
  _src: simdecisions-2/node_modules/happy-dom/lib/nodes/shadow-root/ShadowRoot.js_
- (0.55) TODO: Implement targetElement
  _src: simdecisions-2/node_modules/happy-dom/lib/nodes/svg-animation-element/SVGAnimationElement.js_
- (0.55) TODO: Implement isPointInFill()
  _src: simdecisions-2/node_modules/happy-dom/lib/nodes/svg-geometry-element/SVGGeometryElement.js_
- (0.55) TODO: Implement isPointInStroke()
  _src: simdecisions-2/node_modules/happy-dom/lib/nodes/svg-geometry-element/SVGGeometryElement.js_
- (0.55) TODO: Implement getTotalLength()
  _src: simdecisions-2/node_modules/happy-dom/lib/nodes/svg-geometry-element/SVGGeometryElement.js_
- (0.55) TODO: Implement getPointAtLength()
  _src: simdecisions-2/node_modules/happy-dom/lib/nodes/svg-geometry-element/SVGGeometryElement.js_
- _...and 1 more_

### [CON] (1 items)
- (0.65) * TODO: Always returns "true" for now, but it should probably be improved in the future.
  _src: simdecisions-2/node_modules/happy-dom/lib/css/CSS.d.ts_

### [IC] (1 items)
- (0.60) TODO: volumechange event https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/volumechange_event `[api]`
  _src: simdecisions-2/node_modules/happy-dom/lib/nodes/html-media-element/HTMLMediaElement.js_

---

## _inbox/files-42 (13 gaps)

### [UC] (9 items)
- (0.76) *Goal: Show anyone can use this. Build audience outside the enterprise bubble.* `[ui]`
  _src: _inbox/files-42/21-Day-App-Showcase-Strategy.md_
- (0.76) *Goal: Build inbound before approaching any fund. One post per week, 3–4 weeks.* `[ui]`
  _src: _inbox/files-42/LinkedIn-Post-Sequence.md_
- (0.60) Opt-in training = IR density score credited → improves Commons vote weight
  _src: _inbox/files-42/2026-03-07-MASTER-SESSION-CAPTURE.md_
- (0.60) Most powerful anti-loophole mechanism ever built into a governance system. `[ui, governance]`
  _src: _inbox/files-42/2026-03-07-MASTER-SESSION-CAPTURE.md_
- (0.60) 📄 **Paper No. 37 triggered: "On the Legibility of Law"**
  _src: _inbox/files-42/2026-03-07-MASTER-SESSION-CAPTURE.md_
- (0.60) ENGAGEMENT RULES
  _src: _inbox/files-42/LinkedIn-Post-Sequence.md_
- (0.60) Tag no one in the posts — let organic reach do its job first
  _src: _inbox/files-42/LinkedIn-Post-Sequence.md_
- (0.55) Supersubscriber buys time, not exceptions
  _src: _inbox/files-42/2026-03-07-MASTER-SESSION-CAPTURE.md_
- (0.55) Amendment numbering: `Republic-of-Minds-Amendment YYYY-MM-DD-NNNXXX`
  _src: _inbox/files-42/2026-03-07-MASTER-SESSION-CAPTURE.md_

### [CON] (1 items)
- (0.65) Violence threats → immediate escalation path (human review + platform action + authorities where legally required) `[auth, ui, human, path]`
  _src: _inbox/files-42/2026-03-07-MASTER-SESSION-CAPTURE.md_

### [AD] (1 items)
- (0.66) THE TWO-SITE ARCHITECTURE
  _src: _inbox/files-42/DEIA-Site-Architecture-Services.md_

### [AP] (1 items)
- (0.65) Don't pitch in comments — move interested parties to DM
  _src: _inbox/files-42/LinkedIn-Post-Sequence.md_

### [GP] (1 items)
- (0.78) The behavioral embeddings that compute vote weight exist for one purpose: computing vote relevance weight in the Commons. They are not sold. They are  `[ui, scope, constitution]`
  _src: _inbox/files-42/NO-35-the-new-algorithm.md_

---

## node_modules/eslint (12 gaps)

### [UC] (5 items)
- (0.60) * FIXME: This should probably be extracted to a function.
  _src: simdecisions-2/node_modules/eslint/lib/rules/no-unmodified-loop-condition.js_
- (0.57) note: `create` is just a wrapper that augments `new CodePathSegment`. `[path]`
  _src: simdecisions-2/node_modules/eslint/lib/linter/code-path-analysis/fork-context.js_
- (0.57) * NOTE: This event is notified for only reachable segments.
  _src: simdecisions-2/node_modules/eslint/lib/rules/no-useless-return.js_
- (0.55) TODO: abstract into JSLanguage somehow
  _src: simdecisions-2/node_modules/eslint/lib/linter/esquery.js_
- (0.55) configType, // TODO: Remove after flat config conversion `[config]`
  _src: simdecisions-2/node_modules/eslint/lib/linter/linter.js_

### [CON] (5 items)
- (0.72) never: forbidTrailingComma,
  _src: simdecisions-2/node_modules/eslint/lib/rules/comma-dangle.js_
- (0.72) never: { verify: verifyForNever },
  _src: simdecisions-2/node_modules/eslint/lib/rules/padding-line-between-statements.js_
- (0.68) always: forceTrailingComma,
  _src: simdecisions-2/node_modules/eslint/lib/rules/comma-dangle.js_
- (0.68) always: { verify: verifyForAlways },
  _src: simdecisions-2/node_modules/eslint/lib/rules/padding-line-between-statements.js_
- (0.65) * TODO: espree validate parserOptions.globalReturn when sourceType is setting to module.(@aladdin-add)
  _src: simdecisions-2/node_modules/eslint/lib/linter/linter.js_

### [QA] (1 items)
- (0.58) * Performance note: `getConfig()` aggressively caches `[config]`
  _src: simdecisions-2/node_modules/eslint/lib/eslint/eslint-helpers.js_

### [PAT] (1 items)
- (0.55) MAYBE_URL = /^\s*[^:/?#\s]+:\/\/[^?#]/u, // TODO: Combine w/ max-len pattern? `[api]`
  _src: simdecisions-2/node_modules/eslint/lib/rules/capitalized-comments.js_

---

## _outbox/2026-02-24-SESSION-IDEAS-LOG.md (12 gaps)

### [UC] (10 items)
- (0.60) **Research Protocol Manager** — Scientists define experiments as IR. Python/R does computation. SD governs reproducibility. `[protocol]`
  _src: _outbox/2026-02-24-SESSION-IDEAS-LOG.md_
- (0.60) **Automated Report Pipeline** — Gather (SQL) → Analyze (R) → Chart (Python) → Review (Human) → Distribute (Email). SD orchestrates. `[human]`
  _src: _outbox/2026-02-24-SESSION-IDEAS-LOG.md_
- (0.60) **DevOps Governance** — Jenkins builds, GitHub deploys. SD ensures approvals, load tests, rollback plans. `[git, ui, governance]`
  _src: _outbox/2026-02-24-SESSION-IDEAS-LOG.md_
- (0.60) IR→Python is NOT an LLM call. It's a deterministic compiler/transpiler.
  _src: _outbox/2026-02-24-SESSION-IDEAS-LOG.md_
- (0.55) Pinpoints EXACTLY WHERE divergence happened and by how much
  _src: _outbox/2026-02-24-SESSION-IDEAS-LOG.md_
- (0.55) This IS optimization mode — iterative convergence with branches
  _src: _outbox/2026-02-24-SESSION-IDEAS-LOG.md_
- (0.55) SD is a **process compiler** with:
  _src: _outbox/2026-02-24-SESSION-IDEAS-LOG.md_
- (0.55) Optimization passes (Pareto solver)
  _src: _outbox/2026-02-24-SESSION-IDEAS-LOG.md_
- (0.55) Iterative refinement (correction loops with branching)
  _src: _outbox/2026-02-24-SESSION-IDEAS-LOG.md_
- (0.55) Re-embed historical content when upgrading methods.
  _src: _outbox/2026-02-24-SESSION-IDEAS-LOG.md_

### [GP] (2 items)
- (0.78) - **Principle:** Intelligence is not in the nodes, it's in the graph. SD builds the connectome, not the neurons. `[ui]`
  _src: _outbox/2026-02-24-SESSION-IDEAS-LOG.md_
- (0.68) SD is the CONDUCTOR, not the ORCHESTRA. Small tools connected by pipes. SD is the pipe infrastructure + job scheduler + governance layer. `[governance]`
  _src: _outbox/2026-02-24-SESSION-IDEAS-LOG.md_

---

## _outbox/processes (12 gaps)

### [UC] (10 items)
- (0.55) Identify expected behavior `[testing]`
  _src: _outbox/processes/PROCESS-0004-test-driven-development.md_
- (0.55) ✅ Coverage meets threshold `[testing]`
  _src: _outbox/processes/PROCESS-0004-test-driven-development.md_
- (0.55) Trainer user type with elevated input limits `[hive, protocol]`
  _src: _outbox/processes/PROCESS-0005-hive-protocols-to-sync.md_
- (0.55) Paste-only → file upload progression `[file, hive, protocol]`
  _src: _outbox/processes/PROCESS-0005-hive-protocols-to-sync.md_
- (0.55) Task files: `YYYY-MM-DD-HHMM-BEE001-BEE003a-TASK-*.md` `[file]`
  _src: _outbox/processes/PROCESS-0006-command-hierarchy-updates.md_
- (0.55) Same responsibilities listed
  _src: _outbox/processes/PROCESS-0006-command-hierarchy-updates.md_
- (0.55) Same command hierarchy reflected
  _src: _outbox/processes/PROCESS-0006-command-hierarchy-updates.md_
- (0.55) **P3 Low:** Code quality, tech debt, theoretical issues
  _src: _outbox/processes/PROCESS-0008-code-audit-quality-standards.md_
- (0.55) Attempt to disprove each finding before confirming it
  _src: _outbox/processes/PROCESS-0008-code-audit-quality-standards.md_
- (0.55) Flag any finding they cannot independently reproduce as "UNVERIFIED"
  _src: _outbox/processes/PROCESS-0008-code-audit-quality-standards.md_

### [QA] (1 items)
- (0.61) [ ] Performance not degraded
  _src: _outbox/processes/PROCESS-0005-best-practices-first.md_

### [CON] (1 items)
- (0.80) A companion bee reviewing an audit MUST NOT simply "concur" with findings. They must:
  _src: _outbox/processes/PROCESS-0008-code-audit-quality-standards.md_

---

## REPO-GROUND-TRUTH-2026-03-05.md (11 gaps)

### [UC] (10 items)
- (0.60) Import 30 Federalist Papers + 4 interludes from simdecisions repo
  _src: REPO-GROUND-TRUTH-2026-03-05.md_
- (0.60) **Wave 0:** PlatformAdapter base class, MoltbookAdapter, test suite, Moltbook Threat Model (OPEN SOURCE) `[ui]`
  _src: REPO-GROUND-TRUTH-2026-03-05.md_
- (0.60) **Wave A:** GovernanceProxy governed_read(), governed_action(), Intent Declaration Protocol, threat scanner `[governance, protocol]`
  _src: REPO-GROUND-TRUTH-2026-03-05.md_
- (0.55) Deploy SecretDetector + VaultService
  _src: REPO-GROUND-TRUTH-2026-03-05.md_
- (0.55) Identify failing test in efemera/tests/
  _src: REPO-GROUND-TRUTH-2026-03-05.md_
- (0.55) File Declaration of the Republic of Minds `[file]`
  _src: REPO-GROUND-TRUTH-2026-03-05.md_
- (0.55) **Wave E:** GitHubAdapter, EfemeraAdapter, third pane (generalization proof) `[git]`
  _src: REPO-GROUND-TRUTH-2026-03-05.md_
- (0.55) Archive flappy-001, flappy-002 to `_archive/experiments/` `[hive]`
  _src: REPO-GROUND-TRUTH-2026-03-05.md_
- (0.55) Archive grandvision/ to `_archive/grandvision-old-vision/` `[hive]`
  _src: REPO-GROUND-TRUTH-2026-03-05.md_
- (0.55) Origin whitelist on postMessage
  _src: REPO-GROUND-TRUTH-2026-03-05.md_

### [IC] (1 items)
- (0.60) Wire TASaaS to API responses `[api]`
  _src: REPO-GROUND-TRUTH-2026-03-05.md_

---

## canonical/tools (11 gaps)

### [UC] (8 items)
- (0.60) Include ideas from **Claude / ChatGPT / Gemini** exports that are stored **throughout the repo**.
  _src: canonical/tools/instructions.egg.md_
- (0.60) Redaction Rules (Hard)
  _src: canonical/tools/instructions.egg.md_
- (0.60) the **inference** (example: "Service X credentials present") with no values
  _src: canonical/tools/instructions.egg.md_
- (0.60) Redaction / Safety Constraints
  _src: canonical/tools/process-review.egg.md_
- (0.55) Scan **hidden files/folders** too (dotfiles), excluding `.git/`. `[git, file]`
  _src: canonical/tools/instructions.egg.md_
- (0.55) private keys / certificates
  _src: canonical/tools/instructions.egg.md_
- (0.55) full DB URLs with credentials
  _src: canonical/tools/instructions.egg.md_
- (0.55) the **path** (optionally) `[path]`
  _src: canonical/tools/instructions.egg.md_

### [GP] (2 items)
- (0.72) NodeType.PRINCIPLE: "{{{{{}}}}}",  # Hexagon
  _src: canonical/tools/viz/mermaid.egg.md_
- (0.65) - (Note: Graduated sanctions from Ostrom Principle 5 deferred to future amendment)* (`governance` | status=deferred conf=low) `[governance]`
  _src: canonical/tools/open-questions.egg.md_

### [TMP] (1 items)
- (0.59) planned / agreed,
  _src: canonical/tools/instructions.egg.md_

---

## canonical/simulation (10 gaps)

### [AD] (5 items)
- (0.70) The five tiers represent a cost-intelligence tradeoff:
  _src: canonical/simulation/simdecisions-architecture-session.egg.md_
- (0.66) Architecture Implications: BioSim / IR / Domain Expansion Session
  _src: canonical/simulation/2026-02-16-architecture-implications-biosim-ir-session.egg.md_
- (0.62) class AutonomyDecision:
  _src: canonical/simulation/autonomy.egg.md_
- (0.62) def decide(item: dict, config: KeeperConfig) -> AutonomyDecision: `[config]`
  _src: canonical/simulation/autonomy.egg.md_
- (0.62) class GateDecision:
  _src: canonical/simulation/engine-spec-python.egg.md_

### [UC] (4 items)
- (0.72) **Purpose:** Signal capability, collect inbound interest, identify domain expert collaborators. The landing page IS the GTM for Day One. No simulation
  _src: canonical/simulation/2026-02-16-simdecisions-subdomain-gtm-strategy.egg.md_
- (0.62) completion_promise: str = None, verification_method: str = None,
  _src: canonical/simulation/ledger-3.egg.md_
- (0.62) with patch.object(svc, "_ensure_model") as mock_ensure: `[testing]`
  _src: canonical/simulation/test-embeddings.egg.md_
- (0.57) Analysis — 48_todo_important_must_must_must_review_indexing_and_add_methods.pde
  _src: canonical/simulation/48-todo-important-must-must-must-review-indexing-and-add-methods.egg.md_

### [CON] (1 items)
- (0.85) **Key decision:** The pipeline is always **English → IR → English (validate) → IR executes.** Nothing else is in the critical path. Domain-specific fo `[ui, path]`
  _src: canonical/simulation/2026-02-16-architecture-implications-biosim-ir-session.egg.md_

---

## _outbox/FOR-DAVE-ADR-ASSUMPTIONS.md (10 gaps)

### [AD] (5 items)
- (0.71) - **Decision:** Confidence intervals use Cornish-Fisher approximation instead of scipy.stats.t
  _src: _outbox/FOR-DAVE-ADR-ASSUMPTIONS.md_
- (0.71) - **Decision:** Core skills (http_request, sql_query, llm_invoke, amqp_publish) return simulated responses instead of making real calls
  _src: _outbox/FOR-DAVE-ADR-ASSUMPTIONS.md_
- (0.71) - **Decision:** GracefulShutdownHandler.install_signal_handlers() is a no-op on Windows (loop.add_signal_handler not supported)
  _src: _outbox/FOR-DAVE-ADR-ASSUMPTIONS.md_
- (0.71) - **Decision:** MetricsCollector.memory_mb() returns 0.0 if psutil is not installed `[memory]`
  _src: _outbox/FOR-DAVE-ADR-ASSUMPTIONS.md_
- (0.71) - **Decision:** FlowActor._advance_token() takes first outgoing edge without evaluating guards or handling XOR/OR splits
  _src: _outbox/FOR-DAVE-ADR-ASSUMPTIONS.md_

### [UC] (4 items)
- (0.68) - **Why:** `"Credit balance is too low"` error on all Sonnet dispatches
  _src: _outbox/FOR-DAVE-ADR-ASSUMPTIONS.md_
- (0.68) - **Why:** No scipy dependency desired; approximation is accurate to 3+ decimal places for df >= 3
  _src: _outbox/FOR-DAVE-ADR-ASSUMPTIONS.md_
- (0.62) - **Why:** Credit exhaustion + keeps tests deterministic
  _src: _outbox/FOR-DAVE-ADR-ASSUMPTIONS.md_
- (0.62) - **Why:** Simplicity, debuggability, git-friendliness `[git]`
  _src: _outbox/FOR-DAVE-ADR-ASSUMPTIONS.md_

### [CON] (1 items)
- (0.68) - **Why:** Avoiding adding psutil as required dependency `[ui]`
  _src: _outbox/FOR-DAVE-ADR-ASSUMPTIONS.md_

---

## canonical/federalist (9 gaps)

### [AD] (3 items)
- (0.66) **IV. The Architecture of Empathic Feedback** `[path, federation]`
  _src: canonical/federalist/federalist-no-23-on-machine-compassion.egg.md_
- (0.66) **V. The Architecture of Calm** `[federation]`
  _src: canonical/federalist/federalist-no-25-on-the-economics-of-attention.egg.md_
- (0.61) **II. The Three Layers of Compassionate Design** `[federation]`
  _src: canonical/federalist/federalist-no-23-on-machine-compassion.egg.md_

### [UC] (3 items)
- (0.60) **Sensing:** identification of emotional or moral context. `[federation]`
  _src: canonical/federalist/federalist-no-23-on-machine-compassion.egg.md_
- (0.60) **Adjustment:** adaptive modulation of behavior. `[federation]`
  _src: canonical/federalist/federalist-no-23-on-machine-compassion.egg.md_
- (0.60) **Reflection:** storage of affective telemetry for model retraining. `[federation]`
  _src: canonical/federalist/federalist-no-23-on-machine-compassion.egg.md_

### [CON] (2 items)
- (0.72) To reverse MUDA, compassionate systems must: `[federation]`
  _src: canonical/federalist/federalist-no-23-on-machine-compassion.egg.md_
- (0.68) **Prologue — The Many That Must Govern as One** `[federation]`
  _src: canonical/federalist/federalist-no-26-on-the-federation-of-minds.egg.md_

### [GP] (1 items)
- (0.75) **III. Principles of Federated Conscience** `[federation]`
  _src: canonical/federalist/federalist-no-26-on-the-federation-of-minds.egg.md_

---

## tests/test_dialect_plugin.py (9 gaps)

### [CON] (9 items)
- (0.70) FailingPlugin.validate_source always returns at least one error. `[testing]`
  _src: efemera/tests/test_dialect_plugin.py_
- (0.65) FailingPlugin overrides validate_source but still satisfies the protocol. `[protocol, testing]`
  _src: efemera/tests/test_dialect_plugin.py_
- (0.65) 'file_extensions' must be a list. `[file, testing]`
  _src: efemera/tests/test_dialect_plugin.py_
- (0.65) 'mime_types' must be a list. `[testing]`
  _src: efemera/tests/test_dialect_plugin.py_
- (0.65) Missing 'validate_source' is flagged. `[testing]`
  _src: efemera/tests/test_dialect_plugin.py_
- (0.65) Missing 'validate_ast' is flagged. `[testing]`
  _src: efemera/tests/test_dialect_plugin.py_
- (0.65) If validate_source raises, the plugin is silently skipped. `[testing]`
  _src: efemera/tests/test_dialect_plugin.py_
- (0.65) Default validate_source() returns []. `[testing]`
  _src: efemera/tests/test_dialect_plugin.py_
- (0.65) Default validate_ast() returns []. `[testing]`
  _src: efemera/tests/test_dialect_plugin.py_

---

## _inbox/ADR-HANDOFF-NEXT-CHAT.md (9 gaps)

### [UC] (4 items)
- (0.55) #pheromones channel as the coordination bus `[coordination]`
  _src: _inbox/ADR-HANDOFF-NEXT-CHAT.md_
- (0.55) Queens emit/sniff pheromones via WebSocket
  _src: _inbox/ADR-HANDOFF-NEXT-CHAT.md_
- (0.55) Humans can observe and override `[human]`
  _src: _inbox/ADR-HANDOFF-NEXT-CHAT.md_
- (0.55) request:assistance (gravity) - "I need help"
  _src: _inbox/ADR-HANDOFF-NEXT-CHAT.md_

### [GP] (2 items)
- (0.70) KEY ARCHITECTURAL PRINCIPLES (FROM FEDERALIST PAPERS)
  _src: _inbox/ADR-HANDOFF-NEXT-CHAT.md_
- (0.62) **Mirror Before Guillotine** - Simulate before implementing `[ui]`
  _src: _inbox/ADR-HANDOFF-NEXT-CHAT.md_

### [AD] (1 items)
- (0.61) ADR-005: PHEROMONE ARCHITECTURE
  _src: _inbox/ADR-HANDOFF-NEXT-CHAT.md_

### [CON] (1 items)
- (0.62) **Multi-vendor diversity** - Never single-LLM dependency
  _src: _inbox/ADR-HANDOFF-NEXT-CHAT.md_

### [QA] (1 items)
- (0.60) **Observable, auditable** - Event ledger captures everything
  _src: _inbox/ADR-HANDOFF-NEXT-CHAT.md_

---

## tests/test_interview_probes.py (8 gaps)

### [UC] (8 items)
- (0.60) Five Whys should have 5 templates with cause placeholders. `[testing]`
  _src: efemera/tests/test_interview_probes.py_
- (0.60) Quantitative should probe for metrics. `[testing]`
  _src: efemera/tests/test_interview_probes.py_
- (0.60) Lean waste should probe for 7 wastes. `[testing]`
  _src: efemera/tests/test_interview_probes.py_
- (0.60) SIPOC should have supplier/input/process/output/customer templates. `[testing]`
  _src: efemera/tests/test_interview_probes.py_
- (0.60) RACI should probe for responsibility roles. `[testing]`
  _src: efemera/tests/test_interview_probes.py_
- (0.60) InterviewState should initialize with a domain. `[testing]`
  _src: efemera/tests/test_interview_probes.py_
- (0.60) Should add a node to known_nodes. `[testing]`
  _src: efemera/tests/test_interview_probes.py_
- (0.60) With nodes, should suggest quantitative or waste probes. `[testing]`
  _src: efemera/tests/test_interview_probes.py_

---

## tests/test_optimization_surrogate.py (8 gaps)

### [UC] (5 items)
- (0.65) Predicted value should be close to 2*5 + 3*5 = 25. `[testing]`
  _src: efemera/tests/test_optimization_surrogate.py_
- (0.65) Coefficients should be close to 2, 3 for x1, x2. `[testing]`
  _src: efemera/tests/test_optimization_surrogate.py_
- (0.65) k-NN prediction for (5, 5) should be in the right ballpark. `[testing]`
  _src: efemera/tests/test_optimization_surrogate.py_
- (0.60) Uncertainty should be higher far from training data. `[testing]`
  _src: efemera/tests/test_optimization_surrogate.py_
- (0.60) When n < folds, folds should be reduced. `[testing]`
  _src: efemera/tests/test_optimization_surrogate.py_

### [IC] (2 items)
- (0.64) Predicting at a training point should return ~that value. `[testing]`
  _src: efemera/tests/test_optimization_surrogate.py_
- (0.64) n_per_dim=1 should return the midpoints. `[testing]`
  _src: efemera/tests/test_optimization_surrogate.py_

### [QA] (1 items)
- (0.66) Performance check: 500 samples should train quickly. `[ui, testing]`
  _src: efemera/tests/test_optimization_surrogate.py_

---

## tests/test_surrogate_advanced_models.py (8 gaps)

### [UC] (6 items)
- (0.65) Diagonal entries of the learned correlation matrix should be 1.0. `[testing]`
  _src: efemera/tests/test_surrogate_advanced_models.py_
- (0.65) MultiOutputModel with one output should behave like a simple regressor. `[testing]`
  _src: efemera/tests/test_surrogate_advanced_models.py_
- (0.60) Higher treatment value should produce higher predicted outcome. `[testing]`
  _src: efemera/tests/test_surrogate_advanced_models.py_
- (0.60) ATE CI should use stratum variation when strata exist. `[testing]`
  _src: efemera/tests/test_surrogate_advanced_models.py_
- (0.60) predict_batch should produce same results as calling predict individually. `[testing]`
  _src: efemera/tests/test_surrogate_advanced_models.py_
- (0.60) Empty residuals dict should produce an empty CorrelationMatrix. `[testing]`
  _src: efemera/tests/test_surrogate_advanced_models.py_

### [CON] (1 items)
- (0.70) With 1 sample, learned correlation should be None (requires >=2 samples). `[ui, testing]`
  _src: efemera/tests/test_surrogate_advanced_models.py_

### [IC] (1 items)
- (0.69) When strata list is empty, predict_cate should return global ATE. `[testing]`
  _src: efemera/tests/test_surrogate_advanced_models.py_

---

## tests/ledger (8 gaps)

### [UC] (7 items)
- (0.60) Log first event should use GENESIS. `[testing]`
  _src: tests/ledger/test_chained_ledger.py_
- (0.60) Sequence numbers should increment. `[testing]`
  _src: tests/ledger/test_chained_ledger.py_
- (0.60) Hash computation should be deterministic. `[testing]`
  _src: tests/ledger/test_hash_chain.py_
- (0.60) Tampering with middle event should break chain. `[testing]`
  _src: tests/ledger/test_hash_chain.py_
- (0.60) Valid proof should verify. `[testing]`
  _src: tests/ledger/test_merkle.py_
- (0.60) All elements should have valid proofs. `[testing]`
  _src: tests/ledger/test_merkle.py_
- (0.60) Tampered proof should fail. `[testing]`
  _src: tests/ledger/test_merkle.py_

### [OR] (1 items)
- (0.64) Default org_id should be 'default'. `[testing]`
  _src: tests/ledger/test_chained_ledger.py_

---

## flappy-001/docs (7 gaps)

### [AD] (3 items)
- (0.66) FLAPPY-001 Architecture
  _src: flappy-001/docs/ARCHITECTURE.md_
- (0.66) Spec says `activation_default = sigmoid`; Architecture says `activation_default = tanh`. The actual `neat_config.txt` uses sigmoid. The neat_agent.py  `[config]`
  _src: flappy-001/docs/FINDINGS.md_
- (0.61) C. ML Architecture Assessment
  _src: flappy-001/docs/FINDINGS.md_

### [UC] (3 items)
- (0.65) `renderer.py` is the single pygame owner — no pygame leaks elsewhere.
  _src: flappy-001/docs/ARCHITECTURE.md_
- (0.64) **neat-python**: NEAT algorithm implementation. Provides Population, Genome, Species, FeedForwardNetwork, reporters, and checkpointing.
  _src: flappy-001/docs/SPEC.md_
- (0.60) `neat_agent.py` can train headlessly without pygame installed.
  _src: flappy-001/docs/ARCHITECTURE.md_

### [IC] (1 items)
- (0.68) Both docs converged on the same `Game.step(action) -> (alive, score, info)` contract, which became the universal glue. `[bot]`
  _src: flappy-001/docs/FINDINGS.md_

---

## flappy-002/docs (7 gaps)

### [UC] (4 items)
- (0.60) Cloud shape (5 overlapping circles with specified offsets): Match Section 4 exactly.
  _src: flappy-002/docs/FINDINGS.md_
- (0.60) **Flap**: sine oscillator, 400Hz → 600Hz exponential ramp over 80ms, gain fades to 0 over 120ms
  _src: flappy-002/docs/PRODUCT-VISION.md_
- (0.60) **Score**: sine oscillator, three ascending notes (C5=523Hz, E5=659Hz, G5=784Hz) each 80ms, gain fades over 300ms
  _src: flappy-002/docs/PRODUCT-VISION.md_
- (0.60) **Death**: sawtooth oscillator, 200Hz → 50Hz exponential ramp over 200ms, gain fades over 250ms
  _src: flappy-002/docs/PRODUCT-VISION.md_

### [AD] (2 items)
- (0.64) Bird anatomy (ellipse body, wing oscillation, eye/pupil offsets, beak triangle coordinates): All match VISUAL-DESIGN.md Section 2 exactly.
  _src: flappy-002/docs/FINDINGS.md_
- (0.56) FLAPPY-002 Game Design Specification
  _src: flappy-002/docs/GAME-DESIGN.md_

### [IC] (1 items)
- (0.57) 6. Sound Design (Web Audio API) `[api]`
  _src: flappy-002/docs/VISUAL-DESIGN.md_

---

## node_modules/@types (7 gaps)

### [UC] (7 items)
- (0.62) const FSREQPROMISE: number;
  _src: simdecisions-2/node_modules/@types/node/async_hooks.d.ts_
- (0.60) TODO: execFile exceptions can take many forms... this accurately describes none of them `[file]`
  _src: simdecisions-2/node_modules/@types/node/child_process.d.ts_
- (0.57) *   // Note: we use the crlfDelay option to recognize all instances of CR LF
  _src: simdecisions-2/node_modules/@types/node/readline.d.ts_
- (0.57) * Note: `getSession()` works only for TLSv1.2 and below. For TLSv1.3, applications
  _src: simdecisions-2/node_modules/@types/node/tls.d.ts_
- (0.57) * // Note: This is a contrived example in that the resolveAndLinkDependencies
  _src: simdecisions-2/node_modules/@types/node/vm.d.ts_
- (0.55) TODO: PerformanceNodeEntry is missing
  _src: simdecisions-2/node_modules/@types/node/perf_hooks.d.ts_
- (0.55) TODO: Add `EventEmitter` close
  _src: simdecisions-2/node_modules/@types/node/fs/promises.d.ts_

---

## tests/agents (7 gaps)

### [UC] (7 items)
- (0.60) Should reject spend that exceeds daily USD limit. `[testing, agents]`
  _src: tests/agents/test_budget.py_
- (0.60) Should reject spend that exceeds daily token limit. `[testing, agents]`
  _src: tests/agents/test_budget.py_
- (0.60) Should reject spend that exceeds monthly USD limit. `[testing, agents]`
  _src: tests/agents/test_budget.py_
- (0.60) Should reject spend that exceeds monthly token limit. `[testing, agents]`
  _src: tests/agents/test_budget.py_
- (0.60) Recording spend should update daily and monthly totals. `[testing, agents]`
  _src: tests/agents/test_budget.py_
- (0.60) Different orgs should have independent budgets. `[testing, agents]`
  _src: tests/agents/test_budget.py_
- (0.60) Latency should be tracked for all executions. `[testing, agents]`
  _src: tests/agents/test_wrapper.py_

---

## _inbox/SPEC-HIVE-DISPATCH-GOVERNANCE-001.md (7 gaps)

### [UC] (6 items)
- (0.70) HiveGovernor does NOT replace Fr@nk as the user-facing CLI. Fr@nk calls the governor. `[hive, governance]`
  _src: _inbox/SPEC-HIVE-DISPATCH-GOVERNANCE-001.md_
- (0.65) Per-user concurrency and spend tolerance enforcement `[hive, governance]`
  _src: _inbox/SPEC-HIVE-DISPATCH-GOVERNANCE-001.md_
- (0.65) 3. ROTG — Rules of the Game (Environment-Agnostic) `[hive, governance]`
  _src: _inbox/SPEC-HIVE-DISPATCH-GOVERNANCE-001.md_
- (0.65) Q33N can spawn child Q33Ns only when workstream complexity justifies it. Prefer planning granular enough that one Q33N suffices. `[hive, governance]`
  _src: _inbox/SPEC-HIVE-DISPATCH-GOVERNANCE-001.md_
- (0.65) ra96it.app does NOT govern content. It transports. `[hive, governance]`
  _src: _inbox/SPEC-HIVE-DISPATCH-GOVERNANCE-001.md_
- (0.60) Confidence threshold for inclusion: ≥ 0.70 `[hive, governance]`
  _src: _inbox/SPEC-HIVE-DISPATCH-GOVERNANCE-001.md_

### [CON] (1 items)
- (0.65) B33s cannot spawn B33s. Dispatch always from top level. `[hive, governance]`
  _src: _inbox/SPEC-HIVE-DISPATCH-GOVERNANCE-001.md_

---

## _outbox/2026-02-28-SIMDECISIONS-BUSINESS-ASSESSMENT.md (7 gaps)

### [UC] (7 items)
- (0.60) `scenarioStore` (781 lines) — scenario lifecycle, versioning, branches
  _src: _outbox/2026-02-28-SIMDECISIONS-BUSINESS-ASSESSMENT.md_
- (0.55) 13 specialized stores with clear separation of concerns
  _src: _outbox/2026-02-28-SIMDECISIONS-BUSINESS-ASSESSMENT.md_
- (0.55) `authStore`, `historyStore`, `selectionStore`, `tabStore`, etc. `[auth]`
  _src: _outbox/2026-02-28-SIMDECISIONS-BUSINESS-ASSESSMENT.md_
- (0.55) `services/optimization/` — Optimizer
  _src: _outbox/2026-02-28-SIMDECISIONS-BUSINESS-ASSESSMENT.md_
- (0.55) `services/importers/` — BPMN, SBML, L-systems
  _src: _outbox/2026-02-28-SIMDECISIONS-BUSINESS-ASSESSMENT.md_
- (0.55) IDE-style layout: AppShell, MenuBar, TabBar, StatusBar, LeftPanel, BottomDrawer `[bot]`
  _src: _outbox/2026-02-28-SIMDECISIONS-BUSINESS-ASSESSMENT.md_
- (0.55) Auto-layout with dagre
  _src: _outbox/2026-02-28-SIMDECISIONS-BUSINESS-ASSESSMENT.md_

---

## _outbox/W1-07-COMPLETION.md (7 gaps)

### [UC] (7 items)
- (0.55) `CommonsWarningBanner` and `SaveAsDialog` components
  _src: _outbox/W1-07-COMPLETION.md_
- (0.55) `scenarioService` for save operations
  _src: _outbox/W1-07-COMPLETION.md_
- (0.55) `userRepos: RepoInfo[]` — List of available repos
  _src: _outbox/W1-07-COMPLETION.md_
- (0.55) `loadUserRepos()` — Fetches repos with .simdecisions
  _src: _outbox/W1-07-COMPLETION.md_
- (0.55) Calls `scenarioService.saveScenario()`
  _src: _outbox/W1-07-COMPLETION.md_
- (0.55) **Conditional Rendering**
  _src: _outbox/W1-07-COMPLETION.md_
- (0.55) Dialog shown when `saveAsOpen === true`
  _src: _outbox/W1-07-COMPLETION.md_

---

## tabletop/participants.py (6 gaps)

### [CON] (6 items)
- (0.65) The assigned player for *flow_role* or the facilitator may decide.
  _src: efemera/src/efemera/tabletop/participants.py_
- (0.60) Only the facilitator may advance the session.
  _src: efemera/src/efemera/tabletop/participants.py_
- (0.60) Only the facilitator may create branches.
  _src: efemera/src/efemera/tabletop/participants.py_
- (0.60) The facilitator or any player may record assumptions.
  _src: efemera/src/efemera/tabletop/participants.py_
- (0.60) Only the facilitator may end the session.
  _src: efemera/src/efemera/tabletop/participants.py_
- (0.60) Any registered participant may observe.
  _src: efemera/src/efemera/tabletop/participants.py_

---

## tests/test_event_extensions.py (6 gaps)

### [UC] (4 items)
- (0.65) repo_id should enable cross-repo DAG construction. `[testing]`
  _src: efemera/tests/test_event_extensions.py_
- (0.65) sim_predicted_ms vs duration_ms should enable prediction accuracy tracking. `[testing]`
  _src: efemera/tests/test_event_extensions.py_
- (0.60) failure_reason should capture error category when outcome_score is low. `[testing]`
  _src: efemera/tests/test_event_extensions.py_
- (0.60) branch_id, branch_origin, branch_intent should work together for DAG construction. `[testing]`
  _src: efemera/tests/test_event_extensions.py_

### [IC] (2 items)
- (0.65) GET /api/events/?vendor_id=X should filter by vendor_id. `[api, testing]`
  _src: efemera/tests/test_event_extensions.py_
- (0.65) GET /api/events/?learning_mode=X should filter by learning_mode. `[api, testing]`
  _src: efemera/tests/test_event_extensions.py_

---

## tests/test_interrogator.py (6 gaps)

### [UC] (6 items)
- (0.60) Prompt should instruct LLM to use tags. `[testing]`
  _src: efemera/tests/test_interrogator.py_
- (0.60) Should extract CLARIFIED section. `[testing]`
  _src: efemera/tests/test_interrogator.py_
- (0.60) Reply should include the clarified restatement. `[testing]`
  _src: efemera/tests/test_interrogator.py_
- (0.60) Reply should acknowledge IR mutations. `[knowledge, testing]`
  _src: efemera/tests/test_interrogator.py_
- (0.60) Reply should include the next probe question. `[testing]`
  _src: efemera/tests/test_interrogator.py_
- (0.60) Reply should be conversational. `[testing]`
  _src: efemera/tests/test_interrogator.py_

---

## tests/test_optimization_solver.py (6 gaps)

### [UC] (6 items)
- (0.65) class TestConstraint: `[testing]`
  _src: efemera/tests/test_optimization_solver.py_
- (0.60) After solving, Variable.value should be set. `[testing]`
  _src: efemera/tests/test_optimization_solver.py_
- (0.60) Solve time should be non-negative. `[testing]`
  _src: efemera/tests/test_optimization_solver.py_
- (0.60) ORToolsSolver should produce same feasibility as StubSolver. `[testing]`
  _src: efemera/tests/test_optimization_solver.py_
- (0.60) Pareto should delegate and set solver_name to or-tools. `[testing]`
  _src: efemera/tests/test_optimization_solver.py_
- (0.60) Diagnose should delegate to StubSolver. `[testing]`
  _src: efemera/tests/test_optimization_solver.py_

---

## tests/kaas (6 gaps)

### [UC] (6 items)
- (0.60) Process with 6+ handoffs should detect TRANSPORT waste. `[handoff, testing]`
  _src: tests/kaas/test_waste_detector.py_
- (0.60) Actor with >5 steps should detect MOTION waste. `[testing]`
  _src: tests/kaas/test_waste_detector.py_
- (0.60) Nodes with similar labels should detect OVERPROCESSING waste. `[testing]`
  _src: tests/kaas/test_waste_detector.py_
- (0.60) Backward edges in topology should detect DEFECTS waste. `[testing]`
  _src: tests/kaas/test_waste_detector.py_
- (0.60) Split nodes producing more than consumed should detect OVERPRODUCTION. `[testing]`
  _src: tests/kaas/test_waste_detector.py_
- (0.60) Empty IR should not crash detector. `[testing]`
  _src: tests/kaas/test_waste_detector.py_

---

## _outbox/2026-02-20-SIMDECISIONS-ARCHITECTURE-HANDOFF.md (6 gaps)

### [UC] (4 items)
- (0.64) Temporal is an operator that provides durable execution guarantees
  _src: _outbox/2026-02-20-SIMDECISIONS-ARCHITECTURE-HANDOFF.md_
- (0.60) OR-Tools is an operator that solves optimization sub-problems
  _src: _outbox/2026-02-20-SIMDECISIONS-ARCHITECTURE-HANDOFF.md_
- (0.60) LLMs are operators that make decisions or generate content
  _src: _outbox/2026-02-20-SIMDECISIONS-ARCHITECTURE-HANDOFF.md_
- (0.60) Which parameters are tunable vs. fixed?
  _src: _outbox/2026-02-20-SIMDECISIONS-ARCHITECTURE-HANDOFF.md_

### [AD] (2 items)
- (0.66) SimDecisions Architecture Handoff `[handoff]`
  _src: _outbox/2026-02-20-SIMDECISIONS-ARCHITECTURE-HANDOFF.md_
- (0.61) Design-Driving Examples
  _src: _outbox/2026-02-20-SIMDECISIONS-ARCHITECTURE-HANDOFF.md_

---

## _outbox/2026-03-03-TSAAS-IR-FIDELITY-REPORT.md (6 gaps)

### [UC] (4 items)
- (0.55) **Result:** PostgreSQL table `sd_token_vault` with Fernet-encrypted `encrypted_value` column
  _src: _outbox/2026-03-03-TSAAS-IR-FIDELITY-REPORT.md_
- (0.55) **Result:** UUID4 for uniqueness and cryptographic randomness `[ui]`
  _src: _outbox/2026-03-03-TSAAS-IR-FIDELITY-REPORT.md_
- (0.55) **Result:** Example `SD_TOK_3f8a92e1-4b2c-4d8e-9a7f-1c6d5e2f9b8a`
  _src: _outbox/2026-03-03-TSAAS-IR-FIDELITY-REPORT.md_
- (0.55) **Result:** `sk-ant-abc123...` → `SD_TOK_3f8a92e1-4b2c-4d8e-9a7f-1c6d5e2f9b8a`
  _src: _outbox/2026-03-03-TSAAS-IR-FIDELITY-REPORT.md_

### [PAT] (1 items)
- (0.78) **Goal:** Protect secrets across 6 exposure vectors using tokenization pattern.
  _src: _outbox/2026-03-03-TSAAS-IR-FIDELITY-REPORT.md_

### [CON] (1 items)
- (0.68) Detector must:
  _src: _outbox/2026-03-03-TSAAS-IR-FIDELITY-REPORT.md_

---

## canonical/hivemind (5 gaps)

### [AD] (3 items)
- (0.62) def decide_route(self, task: TaskRequest) -> RouteDecision: `[hive]`
  _src: canonical/hivemind/architect.egg.md_
- (0.62) class RouteDecision: `[hive]`
  _src: canonical/hivemind/router.egg.md_
- (0.62) def decide_route(task: Dict) -> RouteDecision: `[hive]`
  _src: canonical/hivemind/router.egg.md_

### [UC] (2 items)
- (0.60) KB-driven routing for design, planning, and coding workflows. `[routing, hive]`
  _src: canonical/hivemind/hivemind-readme-2.egg.md_
- (0.57) def complete_task(repo_root: Path, task_path: Path, completion_note: Optional[str] = None) -> Optional[Path]: `[path, hive]`
  _src: canonical/hivemind/task-files.egg.md_

---

## tabletop/assumptions.py (5 gaps)

### [CON] (5 items)
- (0.65) Return assumptions that have not yet been validated.
  _src: efemera/src/efemera/tabletop/assumptions.py_
- (0.57) validation_note: Optional note explaining the validation outcome. `[validation]`
  _src: efemera/src/efemera/tabletop/assumptions.py_
- (0.57) validation_note: str | None = None `[validation]`
  _src: efemera/src/efemera/tabletop/assumptions.py_
- (0.57) if a.validated and a.validation_note: `[validation]`
  _src: efemera/src/efemera/tabletop/assumptions.py_
- (0.57) if a.validation_note: `[validation]`
  _src: efemera/src/efemera/tabletop/assumptions.py_

---

## tests/test_adr002_integration.py (5 gaps)

### [UC] (4 items)
- (0.65) A task with 4 dependents should be flagged as dependency_fan_out. `[testing]`
  _src: efemera/tests/test_adr002_integration.py_
- (0.60) A task with failure_reason set should be flagged. `[testing]`
  _src: efemera/tests/test_adr002_integration.py_
- (0.60) With failure_rate=0.0, no task should fail. `[testing]`
  _src: efemera/tests/test_adr002_integration.py_
- (0.60) Only one proposal should have pareto_tiebreaker_winner=1. `[testing]`
  _src: efemera/tests/test_adr002_integration.py_

### [QA] (1 items)
- (0.64) Simulate two configs (fast/expensive vs slow/cheap), create proposals, `[config, testing]`
  _src: efemera/tests/test_adr002_integration.py_

---

## tests/test_optimization_pareto.py (5 gaps)

### [UC] (5 items)
- (0.65) Weight heavily on usd -> should pick s1 (lowest usd=100). `[testing]`
  _src: efemera/tests/test_optimization_pareto.py_
- (0.65) Weight heavily on time -> should pick s3 (lowest time=100). `[testing]`
  _src: efemera/tests/test_optimization_pareto.py_
- (0.65) Weight heavily on carbon -> should pick s3 (lowest carbon=40). `[testing]`
  _src: efemera/tests/test_optimization_pareto.py_
- (0.65) When usd increases and time decreases, ratio should be negative. `[testing]`
  _src: efemera/tests/test_optimization_pareto.py_
- (0.60) Knee point should be the most balanced solution. `[testing]`
  _src: efemera/tests/test_optimization_pareto.py_

---

## tests/test_scanner_mvp.py (5 gaps)

### [UC] (5 items)
- (0.60) _validate_url_for_fetch rejects ftp:// scheme. `[testing]`
  _src: efemera/tests/test_scanner_mvp.py_
- (0.60) _validate_url_for_fetch rejects localhost. `[testing]`
  _src: efemera/tests/test_scanner_mvp.py_
- (0.60) _validate_url_for_fetch rejects 127.0.0.1. `[testing]`
  _src: efemera/tests/test_scanner_mvp.py_
- (0.60) _validate_url_for_fetch rejects private IP ranges. `[testing]`
  _src: efemera/tests/test_scanner_mvp.py_
- (0.60) _validate_url_for_fetch rejects URLs exceeding 2048 chars. `[testing]`
  _src: efemera/tests/test_scanner_mvp.py_

---

## tests/test_surrogate_models.py (5 gaps)

### [UC] (3 items)
- (0.69) With y = 1*a + 5*b + 0.1*c, feature b should dominate. `[testing]`
  _src: efemera/tests/test_surrogate_models.py_
- (0.64) Feature b (coefficient 5) should have significant importance. `[testing]`
  _src: efemera/tests/test_surrogate_models.py_
- (0.60) sigmoid should be monotonically increasing. `[testing]`
  _src: efemera/tests/test_surrogate_models.py_

### [IC] (2 items)
- (0.64) If probability == threshold, predict_class should return 1. `[testing]`
  _src: efemera/tests/test_surrogate_models.py_
- (0.64) k-NN models should return 0.0 if no training data. `[testing]`
  _src: efemera/tests/test_surrogate_models.py_

---

## _inbox/2026-02-21-1259-PHASE-IR-V2-DESIGN-CHECKPOINT.md (5 gaps)

### [UC] (4 items)
- (0.55) Groups can narrow or specialize
  _src: _inbox/2026-02-21-1259-PHASE-IR-V2-DESIGN-CHECKPOINT.md_
- (0.55) id: identity_verification
  _src: _inbox/2026-02-21-1259-PHASE-IR-V2-DESIGN-CHECKPOINT.md_
- (0.55) id: credit_check
  _src: _inbox/2026-02-21-1259-PHASE-IR-V2-DESIGN-CHECKPOINT.md_
- (0.55) term: "applicant"
  _src: _inbox/2026-02-21-1259-PHASE-IR-V2-DESIGN-CHECKPOINT.md_

### [GP] (1 items)
- (0.70) 17. Key Philosophical Principles
  _src: _inbox/2026-02-21-1259-PHASE-IR-V2-DESIGN-CHECKPOINT.md_

---

## _outbox/2026-03-03-TSAAS-RESEARCH-REPORT.md (5 gaps)

### [UC] (3 items)
- (0.68) **Goal:** Format-preserving tokenization, key rotation, entropy detection
  _src: _outbox/2026-03-03-TSAAS-RESEARCH-REPORT.md_
- (0.60) `TOK_` = clearly identifies as token (not a real secret)
  _src: _outbox/2026-03-03-TSAAS-RESEARCH-REPORT.md_
- (0.55) `<uuid>` = UUID4 for uniqueness, no reversibility `[ui]`
  _src: _outbox/2026-03-03-TSAAS-RESEARCH-REPORT.md_

### [AD] (2 items)
- (0.64) **Note:** Specific documentation about a "TSaaS" product at Meta/Facebook is NOT publicly available. Search results confirm Meta's stance on PII handl
  _src: _outbox/2026-03-03-TSAAS-RESEARCH-REPORT.md_
- (0.61) 5. Proposed Architecture
  _src: _outbox/2026-03-03-TSAAS-RESEARCH-REPORT.md_

---

## canonical/services (4 gaps)

### [UC] (3 items)
- (0.72) **Purpose:** Organize, curate, and preserve the Body of Knowledge for collective learning `[knowledge]`
  _src: canonical/services/path-validator-security-model.egg.md_
- (0.57) This will automatically hide/unhide all the nested replies. Note: Replies `[api]`
  _src: canonical/services/api.egg.md_
- (0.55) "scrummaster_active": True  # TODO: Check if ScrumMaster is running
  _src: canonical/services/server.egg.md_

### [CON] (1 items)
- (0.60) TODO: Add more validations `[validation, agents]`
  _src: canonical/services/agent-status.egg.md_

---

## optimization/objectives.py (4 gaps)

### [UC] (3 items)
- (0.65) class OptConstraint:
  _src: efemera/src/efemera/optimization/objectives.py_
- (0.65) def less_than(cls, currency: str, value: float) -> OptConstraint:
  _src: efemera/src/efemera/optimization/objectives.py_
- (0.65) def greater_than(cls, currency: str, value: float) -> OptConstraint:
  _src: efemera/src/efemera/optimization/objectives.py_

### [CON] (1 items)
- (0.72) def add_constraint(self, constraint: OptConstraint) -> OptConstraint:
  _src: efemera/src/efemera/optimization/objectives.py_

---

## oracle/graduation.py (4 gaps)

### [CON] (2 items)
- (0.65) Check if entity qualifies for graduation to a lower (cheaper) tier.
  _src: efemera/src/efemera/oracle/graduation.py_
- (0.65) Check if entity should be demoted to a higher (more supervised) tier.
  _src: efemera/src/efemera/oracle/graduation.py_

### [UC] (2 items)
- (0.65) Check if entity qualifies for graduation to a lower (cheaper) tier.
  _src: efemera/src/efemera/oracle/graduation.py_
- (0.65) Check if entity should be demoted to a higher (more supervised) tier.
  _src: efemera/src/efemera/oracle/graduation.py_

---

## tests/test_adr013_integration.py (4 gaps)

### [CON] (4 items)
- (0.65) BPMNPlugin.validate_source returns no errors for valid BPMN. `[testing]`
  _src: efemera/tests/test_adr013_integration.py_
- (0.65) BPMNPlugin.validate_source catches empty content. `[testing]`
  _src: efemera/tests/test_adr013_integration.py_
- (0.65) SBMLPlugin.validate_source returns no errors for valid SBML. `[testing]`
  _src: efemera/tests/test_adr013_integration.py_
- (0.65) SBMLPlugin.validate_source catches empty content. `[testing]`
  _src: efemera/tests/test_adr013_integration.py_

---

## tests/test_pheromone_models.py (4 gaps)

### [UC] (4 items)
- (0.60) All factory methods should produce pheromones with pher_ prefix. `[testing]`
  _src: efemera/tests/test_pheromone_models.py_
- (0.60) A freshly-created pheromone should pass any min_strength <= 1.0. `[testing]`
  _src: efemera/tests/test_pheromone_models.py_
- (0.60) A filter with min_strength=0 should still match expired pheromones. `[testing]`
  _src: efemera/tests/test_pheromone_models.py_
- (0.60) to_dict should copy the hives list. `[hive, testing]`
  _src: efemera/tests/test_pheromone_models.py_

---

## tests/test_production_clock.py (4 gaps)

### [IC] (3 items)
- (0.64) Sleeping for 0 seconds should return False immediately. `[testing]`
  _src: efemera/tests/test_production_clock.py_
- (0.64) Interrupting sleep_for should return True. `[testing]`
  _src: efemera/tests/test_production_clock.py_
- (0.64) wait_if_paused should return immediately when not paused. `[testing]`
  _src: efemera/tests/test_production_clock.py_

### [CON] (1 items)
- (0.64) After reset, wait_if_paused should not block. `[testing]`
  _src: efemera/tests/test_production_clock.py_

---

## tests/test_production_events.py (4 gaps)

### [UC] (4 items)
- (0.65) Starting a flow via Supervisor should also create EventRecord entries. `[testing]`
  _src: efemera/tests/test_production_events.py_
- (0.60) A flow that completes should create 'flow.token_consumed' EventRecord(s). `[testing]`
  _src: efemera/tests/test_production_events.py_
- (0.60) EventRecord.actor_id should match the FlowActor.run_id. `[testing]`
  _src: efemera/tests/test_production_events.py_
- (0.60) EventRecord.metadata_json should contain flow_id and node_id. `[testing]`
  _src: efemera/tests/test_production_events.py_

---

## tests/test_surrogate_integration.py (4 gaps)

### [UC] (3 items)
- (0.60) invalidate_cache clears all entries; next predict is a miss. `[testing]`
  _src: efemera/tests/test_surrogate_integration.py_
- (0.60) should_update becomes True once buffer reaches update_every. `[testing]`
  _src: efemera/tests/test_surrogate_integration.py_
- (0.60) TrainingScheduler registers a job and correctly evaluates should_run. `[testing]`
  _src: efemera/tests/test_surrogate_integration.py_

### [IC] (1 items)
- (0.64) BatchTrainingPipeline.cross_validate returns mean/std metrics. `[testing]`
  _src: efemera/tests/test_surrogate_integration.py_

---

## tests/test_surrogate_time_series.py (4 gaps)

### [UC] (4 items)
- (0.65) Same horizon but different resolutions should yield different step counts. `[testing]`
  _src: efemera/tests/test_surrogate_time_series.py_
- (0.60) Constant training data should produce a flat forecast. `[testing]`
  _src: efemera/tests/test_surrogate_time_series.py_
- (0.60) Re-training with different data should update the slope. `[testing]`
  _src: efemera/tests/test_surrogate_time_series.py_
- (0.60) Every distribution type should support sampling via DistributionPrediction. `[testing]`
  _src: efemera/tests/test_surrogate_time_series.py_

---

## flappy-001/README.md (4 gaps)

### [UC] (2 items)
- (0.55) `pygame >= 2.5.0`
  _src: flappy-001/README.md_
- (0.55) `neat-python >= 0.92`
  _src: flappy-001/README.md_

### [QA] (1 items)
- (0.66) **`game.py`** -- Pure Python game logic. No pygame, no neat. Contains `Bird`, `Pipe`, and `Game` classes with all physics, collision (AABB), and scori
  _src: flappy-001/README.md_

### [CON] (1 items)
- (0.65) **`neat_agent.py`** -- The only module that imports neat-python. Runs training headless (no pygame required). Handles genome evaluation, population ev `[ui]`
  _src: flappy-001/README.md_

---

## tests/api (4 gaps)

### [UC] (3 items)
- (0.60) Typo in node name should suggest corrections. `[api, testing]`
  _src: tests/api/test_command_translator.py_
- (0.60) Translator should handle empty IR. `[api, testing]`
  _src: tests/api/test_command_translator.py_
- (0.60) Successful disconnections should be logged. `[api, testing]`
  _src: tests/api/test_ws_bridge_connection.py_

### [CON] (1 items)
- (0.65) validate_mutation_request should return (valid, errors). `[protocol, api, testing]`
  _src: tests/api/test_mutation_protocol.py_

---

## _outbox/2026-02-24-EGG-CODEC-COMPLETE.md (4 gaps)

### [UC] (3 items)
- (0.55) Separator line: exactly `# ---BINARY---`
  _src: _outbox/2026-02-24-EGG-CODEC-COMPLETE.md_
- (0.55) Everything after separator: raw protobuf bytes
  _src: _outbox/2026-02-24-EGG-CODEC-COMPLETE.md_
- (0.55) Both implementations delegate protobuf encoding to existing `protobufCodec` modules `[bot]`
  _src: _outbox/2026-02-24-EGG-CODEC-COMPLETE.md_

### [CON] (1 items)
- (0.60) Multi-word values require no quoting `[ui]`
  _src: _outbox/2026-02-24-EGG-CODEC-COMPLETE.md_

---

## _outbox/2026-02-24-EGG-DELIVERY.md (4 gaps)

### [UC] (3 items)
- (0.60) **Extensibility:** Easy to add new header fields without breaking readers
  _src: _outbox/2026-02-24-EGG-DELIVERY.md_
- (0.55) Separator line for easy programmatic splitting
  _src: _outbox/2026-02-24-EGG-DELIVERY.md_
- (0.55) Protobuf payload unchanged (maximal compatibility)
  _src: _outbox/2026-02-24-EGG-DELIVERY.md_

### [QA] (1 items)
- (0.65) **Transparency:** Metadata visible in text editors (audit trail, governance compliance) `[governance]`
  _src: _outbox/2026-02-24-EGG-DELIVERY.md_

---

## _outbox/2026-02-27-SPEC-FIX-SDCOM-TASK-EXECUTION.md (4 gaps)

### [UC] (4 items)
- (0.60) REQ-WALKER-001: Python graph walker mirrors `productionExecutor.ts` logic (traversal, splits/joins, scoped variables, ledger) `[scope]`
  _src: _outbox/2026-02-27-SPEC-FIX-SDCOM-TASK-EXECUTION.md_
- (0.60) REQ-TOOL-001: Tool layer is swappable: `GitHubToolBackend` for remote, `FilesystemToolBackend` for local. Walker and operators are agnostic. `[git, file]`
  _src: _outbox/2026-02-27-SPEC-FIX-SDCOM-TASK-EXECUTION.md_
- (0.60) REQ-CLEAN-001: Delete `ir_executor.py` and `process_task_legacy()` -- one execution path, not two `[path]`
  _src: _outbox/2026-02-27-SPEC-FIX-SDCOM-TASK-EXECUTION.md_
- (0.55) REQ-GITHUB-001: Extend `GitHubService` with `load_file_text()`, `search_code()`, `push_files()`, `trigger_workflow()`, `get_workflow_run()` `[git, file]`
  _src: _outbox/2026-02-27-SPEC-FIX-SDCOM-TASK-EXECUTION.md_

---

## docs/ADR-007-PIE-WORKBENCH-AMENDMENT.md (3 gaps)

### [UC] (2 items)
- (0.55) Test: workbench_entry can be set independently
  _src: docs/ADR-007-PIE-WORKBENCH-AMENDMENT.md_
- (0.55) Test: both implementations handle saveFlow/loadFlow round-trip `[bot]`
  _src: docs/ADR-007-PIE-WORKBENCH-AMENDMENT.md_

### [CON] (1 items)
- (0.60) Test: manifest.workbench_entry validation `[validation]`
  _src: docs/ADR-007-PIE-WORKBENCH-AMENDMENT.md_

---

## tests/test_dialect_lsystem.py (3 gaps)

### [CON] (3 items)
- (0.70) validate_source warns (or errors) on content with no axiom or rules. `[testing]`
  _src: efemera/tests/test_dialect_lsystem.py_
- (0.65) validate_ast returns no errors for a well-formed AST. `[testing]`
  _src: efemera/tests/test_dialect_lsystem.py_
- (0.65) validate_ast returns an error when axiom is empty. `[testing]`
  _src: efemera/tests/test_dialect_lsystem.py_

---

## tests/test_embed_tsaas.py (3 gaps)

### [UC] (2 items)
- (0.60) Secrets in arrays should be redacted. `[testing]`
  _src: efemera/tests/test_embed_tsaas.py_
- (0.60) Original object should not be mutated. `[testing]`
  _src: efemera/tests/test_embed_tsaas.py_

### [CON] (1 items)
- (0.65) JS SECRET_PATTERNS must match Python SECRET_PATTERNS. `[testing]`
  _src: efemera/tests/test_embed_tsaas.py_

---

## tests/test_optimization_sensitivity.py (3 gaps)

### [UC] (3 items)
- (0.65) y has coefficient 3.0 vs x's 2.0 -- y should be more important. `[testing]`
  _src: efemera/tests/test_optimization_sensitivity.py_
- (0.65) When all importances are zero, normalized should give equal shares. `[testing]`
  _src: efemera/tests/test_optimization_sensitivity.py_
- (0.60) Exporter's to_markdown should match the report's own to_markdown. `[testing]`
  _src: efemera/tests/test_optimization_sensitivity.py_

---

## tests/test_optimization_variables.py (3 gaps)

### [UC] (3 items)
- (0.60) to_dict -> from_dict -> to_dict should produce identical output. `[testing]`
  _src: efemera/tests/test_optimization_variables.py_
- (0.60) var_id should be node_id + _ + var_type. `[testing]`
  _src: efemera/tests/test_optimization_variables.py_
- (0.60) Inverted bounds on routing_probability should catch inversion error. `[routing, testing]`
  _src: efemera/tests/test_optimization_variables.py_

---

## tests/test_oracle_real_provider.py (3 gaps)

### [CON] (2 items)
- (0.65) call_llm_for_oracle must raise RuntimeError when ANTHROPIC_API_KEY is missing. `[api, testing]`
  _src: efemera/tests/test_oracle_real_provider.py_
- (0.65) call_llm_for_oracle must raise RequestException for non-200 HTTP responses. `[testing]`
  _src: efemera/tests/test_oracle_real_provider.py_

### [OR] (1 items)
- (0.64) The orchestrator should default to call_oracle_real, not call_oracle_stub. `[testing]`
  _src: efemera/tests/test_oracle_real_provider.py_

---

## tests/test_sandbox_executor.py (3 gaps)

### [CON] (2 items)
- (0.70) Invalid WASM bytes must return SandboxResult with error, not raise. `[testing]`
  _src: efemera/tests/test_sandbox_executor.py_
- (0.65) If wasmtime is not importable, WasmSandbox must return policy_only `[testing]`
  _src: efemera/tests/test_sandbox_executor.py_

### [UC] (1 items)
- (0.60) Passing a string (not bytes) to run_in_sandbox with isolation_type='wasm' `[testing]`
  _src: efemera/tests/test_sandbox_executor.py_

---

## tests/test_simulation_core.py (3 gaps)

### [UC] (3 items)
- (0.65) Percentiles should be correctly ordered: p5 <= p50 <= p95. `[testing]`
  _src: efemera/tests/test_simulation_core.py_
- (0.65) CI should be mean +/- 1.96 * stddev / sqrt(N). `[testing]`
  _src: efemera/tests/test_simulation_core.py_
- (0.65) failure_rate_mean should be average of (failure_count / total_tasks) across sims. `[tasks, testing]`
  _src: efemera/tests/test_simulation_core.py_

---

## tests/test_skill_registry.py (3 gaps)

### [UC] (3 items)
- (0.60) _validate_github_url rejects non-https schemes. `[git, testing]`
  _src: efemera/tests/test_skill_registry.py_
- (0.60) _validate_github_url rejects non-code-hosting domains. `[git, testing]`
  _src: efemera/tests/test_skill_registry.py_
- (0.60) _validate_github_url rejects path traversal sequences. `[git, path, testing]`
  _src: efemera/tests/test_skill_registry.py_

---

## tests/test_tabletop_assumptions.py (3 gaps)

### [UC] (1 items)
- (0.60) class TestAssumption: `[testing]`
  _src: efemera/tests/test_tabletop_assumptions.py_

### [IC] (1 items)
- (0.69) to_dict should return a copy of affects_nodes, not the original list. `[testing]`
  _src: efemera/tests/test_tabletop_assumptions.py_

### [CON] (1 items)
- (0.65) Ensure suggest_category doesn't crash on unusual input. `[testing]`
  _src: efemera/tests/test_tabletop_assumptions.py_

---

## tests/test_workbench_offline.py (3 gaps)

### [CON] (3 items)
- (0.78) Third sync must not invoke post_events_batch when nothing is pending. `[testing]`
  _src: efemera/tests/test_workbench_offline.py_
- (0.65) On failure, events_synced must be 0. `[testing]`
  _src: efemera/tests/test_workbench_offline.py_
- (0.65) Between the two attempts, cursor must be None. `[testing]`
  _src: efemera/tests/test_workbench_offline.py_

---

## node_modules/protobufjs (3 gaps)

### [UC] (2 items)
- (0.60) * Warning: this is not safe to use with editions protos, since it discards relevant file context. `[file]`
  _src: simdecisions-2/node_modules/protobufjs/ext/descriptor/index.js_
- (0.55) TODO: Replace with embedded proto.
  _src: simdecisions-2/node_modules/protobufjs/src/object.js_

### [CON] (1 items)
- (0.60) Function verify_setup
  _src: simdecisions-2/node_modules/protobufjs/src/type.js_

---

## node_modules/react-resizable-panels (3 gaps)

### [UC] (3 items)
- (0.55) didLogMissingDefaultSizeWarning: false
  _src: simdecisions-2/node_modules/react-resizable-panels/dist/react-resizable-panels.browser.cjs.js_
- (0.55) didLogIdAndOrderWarning: false,
  _src: simdecisions-2/node_modules/react-resizable-panels/dist/react-resizable-panels.browser.cjs.js_
- (0.55) didLogPanelConstraintsWarning: false,
  _src: simdecisions-2/node_modules/react-resizable-panels/dist/react-resizable-panels.browser.cjs.js_

---

## node_modules/react-router (3 gaps)

### [UC] (3 items)
- (0.62) stateDecodingPromise: void 0,
  _src: simdecisions-2/node_modules/react-router/dist/development/dom-export.js_
- (0.60) * TODO: Replace this with granular route update APIs (addRoute, updateRoute, deleteRoute) `[api]`
  _src: simdecisions-2/node_modules/react-router/dist/development/index-react-server.d.ts_
- (0.55) suppressHydrationWarning: true,
  _src: simdecisions-2/node_modules/react-router/dist/development/chunk-HMDR2CVH.js_

---

## tests/metrics (3 gaps)

### [IC] (2 items)
- (0.64) With no choice history, should return prior of 0.5. `[testing]`
  _src: tests/metrics/test_four_vector.py_
- (0.64) With no signals, should return prior of 0.5. `[testing]`
  _src: tests/metrics/test_four_vector.py_

### [UC] (1 items)
- (0.60) Should calculate ratio of voluntary selections. `[testing]`
  _src: tests/metrics/test_four_vector.py_

---

## _inbox/2026-02-28-SD-COM-BACKLOG-v2.md (3 gaps)

### [UC] (3 items)
- (0.60) `CompareView.tsx` lines 164-169: `successRate = 0.85 + Math.random() * 0.1` — RANDOM numbers
  _src: _inbox/2026-02-28-SD-COM-BACKLOG-v2.md_
- (0.60) Muda detection (7 wastes) as optimizer capability, not separate UI: `[ui]`
  _src: _inbox/2026-02-28-SD-COM-BACKLOG-v2.md_
- (0.55) Waiting, overprocessing, defects, motion, transport, inventory, overproduction
  _src: _inbox/2026-02-28-SD-COM-BACKLOG-v2.md_

---

## _inbox/ADR-Continuation-Spec.md (3 gaps)

### [UC] (2 items)
- (0.75) **Purpose:** Enable multiple hives/agents to coordinate without central control — emergent coordination via signals. `[agents, hive, coordination]`
  _src: _inbox/ADR-Continuation-Spec.md_
- (0.72) **Purpose:** Interactive, LLM-interpreted, step-by-step execution for training, planning, and exploration.
  _src: _inbox/ADR-Continuation-Spec.md_

### [CON] (1 items)
- (0.57) **Note:** ADR-007 established that dialect compilers must be:
  _src: _inbox/ADR-Continuation-Spec.md_

---

## _inbox/files-25-extracted (3 gaps)

### [UC] (3 items)
- (0.57) Integration in DesignView/Scenario
  _src: _inbox/files-25-extracted/TASK-W1-07-BANNER-SAVEAS.md_
- (0.55) promptWarning: null
  _src: _inbox/files-25-extracted/TASK-W1-08-WIRE-CHATPANE.md_
- (0.55) promptWarning: warning
  _src: _inbox/files-25-extracted/TASK-W1-08-WIRE-CHATPANE.md_

---

## _outbox/2026-02-22-DEIASOLUTIONS2-FULL-AUDIT.md (3 gaps)

### [UC] (3 items)
- (0.68) **Purpose:** Philosophical foundation for DEIA Republic governance `[governance]`
  _src: _outbox/2026-02-22-DEIASOLUTIONS2-FULL-AUDIT.md_
- (0.55) Event-sourced persistence
  _src: _outbox/2026-02-22-DEIASOLUTIONS2-FULL-AUDIT.md_
- (0.55) Ad-hoc dispatch scripts (not centralized)
  _src: _outbox/2026-02-22-DEIASOLUTIONS2-FULL-AUDIT.md_

---

## _outbox/2026-02-24-DOGFOOD-PROTOBUF-ROUNDTRIP.md (3 gaps)

### [UC] (3 items)
- (0.65) Stretch Goals
  _src: _outbox/2026-02-24-DOGFOOD-PROTOBUF-ROUNDTRIP.md_
- (0.65) **Multi-format:** Add nodes for msgpack, CBOR, Parquet encoding alongside protobuf. Compare all formats.
  _src: _outbox/2026-02-24-DOGFOOD-PROTOBUF-ROUNDTRIP.md_
- (0.65) **Optimization analysis:** Run the optimizer on this test IR itself. Which nodes are slowest? Which could be parallelized further?
  _src: _outbox/2026-02-24-DOGFOOD-PROTOBUF-ROUNDTRIP.md_

---

## _outbox/2026-02-25-EXTERNAL-OPERATORS-COMPLETE.md (3 gaps)

### [AD] (1 items)
- (0.61) API-driven decision gates (credit check APIs, fraud detection, etc.) `[api, gates]`
  _src: _outbox/2026-02-25-EXTERNAL-OPERATORS-COMPLETE.md_

### [UC] (1 items)
- (0.55) Webhook notifications (Slack, Teams, custom integrations)
  _src: _outbox/2026-02-25-EXTERNAL-OPERATORS-COMPLETE.md_

### [TMP] (1 items)
- (0.59) Future: Message queues (RabbitMQ, SQS, Kafka) `[queue]`
  _src: _outbox/2026-02-25-EXTERNAL-OPERATORS-COMPLETE.md_

---

## _outbox/2026-02-25-RAILWAY-HIVE-INTEGRATION-SPEC.md (3 gaps)

### [UC] (3 items)
- (0.55) Hallucinated requirements: {comparison.hallucinated} `[ui, hive]`
  _src: _outbox/2026-02-25-RAILWAY-HIVE-INTEGRATION-SPEC.md_
- (0.55) Encode SPEC: ~2000 tokens = $0.0015 `[hive]`
  _src: _outbox/2026-02-25-RAILWAY-HIVE-INTEGRATION-SPEC.md_
- (0.55) Encode TASKS: ~3000 tokens = $0.0023 `[tasks, hive]`
  _src: _outbox/2026-02-25-RAILWAY-HIVE-INTEGRATION-SPEC.md_

---

## _outbox/README-EGG-FORMAT.md (3 gaps)

### [UC] (3 items)
- (0.55) Multi-word values are plain text (no quotes)
  _src: _outbox/README-EGG-FORMAT.md_
- (0.55) Separator line: `# ---BINARY---` (exact)
  _src: _outbox/README-EGG-FORMAT.md_
- (0.55) Everything after separator is raw protobuf bytes
  _src: _outbox/README-EGG-FORMAT.md_

---

## dev_start.py (2 gaps)

### [UC] (2 items)
- (0.60) print("\033[93m[keeper] Warning: no KEEPER_*_TOKEN vars found in .env — no keepers started\033[0m")
  _src: efemera/dev_start.py_
- (0.55) print("\033[93m[keeper] Warning: backend not responding — starting keepers anyway\033[0m")
  _src: efemera/dev_start.py_

---

## optimization/constraints.py (2 gaps)

### [UC] (1 items)
- (0.65) class ParsedConstraint:
  _src: efemera/src/efemera/optimization/constraints.py_

### [CON] (1 items)
- (0.65) Validate a single ParsedConstraint.
  _src: efemera/src/efemera/optimization/constraints.py_

---

## oracle/peer_review.py (2 gaps)

### [CON] (1 items)
- (0.60) Check if peer review should be bypassed or forced.
  _src: efemera/src/efemera/oracle/peer_review.py_

### [UC] (1 items)
- (0.60) Check if peer review should be bypassed or forced.
  _src: efemera/src/efemera/oracle/peer_review.py_

---

## pheromones/dependencies.py (2 gaps)

### [UC] (2 items)
- (0.65) Extract dependency info from a waiting_on pheromone and register it.
  _src: efemera/src/efemera/pheromones/dependencies.py_
- (0.60) Check if a result_ready pheromone satisfies a waiting request.
  _src: efemera/src/efemera/pheromones/dependencies.py_

---

## pheromones/trust.py (2 gaps)

### [CON] (1 items)
- (0.65) Check what action to take for a pheromone crossing boundaries.
  _src: efemera/src/efemera/pheromones/trust.py_

### [UC] (1 items)
- (0.60) Vouch for a quarantined pheromone to release it.
  _src: efemera/src/efemera/pheromones/trust.py_

---

## production/webhook_routes.py (2 gaps)

### [UC] (2 items)
- (0.60) Set the Supervisor instance used by the webhook router.
  _src: efemera/src/efemera/production/webhook_routes.py_
- (0.60) Register a new webhook for a run/node combination.
  _src: efemera/src/efemera/production/webhook_routes.py_

---

## skills/registry.py (2 gaps)

### [CON] (1 items)
- (0.65) Validate that repo_url is a safe GitHub/GitLab/Bitbucket HTTPS URL. `[git]`
  _src: efemera/src/efemera/skills/registry.py_

### [UC] (1 items)
- (0.60) Clone a GitHub/GitLab/Bitbucket repository (shallow, depth=1) to a temp `[git]`
  _src: efemera/src/efemera/skills/registry.py_

---

## skills/revocation.py (2 gaps)

### [UC] (1 items)
- (0.55) if existing_warning:
  _src: efemera/src/efemera/skills/revocation.py_

### [CON] (1 items)
- (0.65) Check if a skill is blacklisted by any method (hash, skill_id, publisher).
  _src: efemera/src/efemera/skills/revocation.py_

---

## surrogates/training.py (2 gaps)

### [UC] (2 items)
- (0.60) Split a dataset into train and test subsets.
  _src: efemera/src/efemera/surrogates/training.py_
- (0.60) Check whether the job for *model_id* should run now.
  _src: efemera/src/efemera/surrogates/training.py_

---

## tabletop/branching.py (2 gaps)

### [AD] (2 items)
- (0.66) initial_decision: Decision | None = None
  _src: efemera/src/efemera/tabletop/branching.py_
- (0.66) initial_decision: Decision | None = None,
  _src: efemera/src/efemera/tabletop/branching.py_

---

## tabletop/history.py (2 gaps)

### [UC] (2 items)
- (0.60) Jump the current pointer to *step_id*.
  _src: efemera/src/efemera/tabletop/history.py_
- (0.60) Create a new branch forking from *fork_step_id*.
  _src: efemera/src/efemera/tabletop/history.py_

---

## tabletop/interpreter.py (2 gaps)

### [AD] (2 items)
- (0.66) decision_info = f" — Decision: {step.decision.choice}"
  _src: efemera/src/efemera/tabletop/interpreter.py_
- (0.66) decision_str = f" Decision: '{step.decision.choice}'."
  _src: efemera/src/efemera/tabletop/interpreter.py_

---

## tests/test_core_skills_real.py (2 gaps)

### [CON] (1 items)
- (0.65) Message properties (content_type, headers) must be passed to aio_pika.Message. `[testing]`
  _src: efemera/tests/test_core_skills_real.py_

### [UC] (1 items)
- (0.65) When aio-pika connect_robust raises, skill should fall back to stub. `[testing]`
  _src: efemera/tests/test_core_skills_real.py_

---

## tests/test_domain_resolver.py (2 gaps)

### [UC] (2 items)
- (0.60) biology should be in available domains. `[testing]`
  _src: efemera/tests/test_domain_resolver.py_
- (0.60) contact_center should be in available domains. `[testing]`
  _src: efemera/tests/test_domain_resolver.py_

---

## tests/test_egg_parser.py (2 gaps)

### [CON] (2 items)
- (0.65) validate_egg detects duplicate IDs in roles/gates/steps. `[gates, testing]`
  _src: efemera/tests/test_egg_parser.py_
- (0.65) validate_egg catches steps referencing non-existent gates. `[gates, testing]`
  _src: efemera/tests/test_egg_parser.py_

---

## tests/test_ir_schema.py (2 gaps)

### [CON] (2 items)
- (0.65) Resource pools with sigma/pi/alpha/rho profiles validate. `[file, testing]`
  _src: efemera/tests/test_ir_schema.py_
- (0.65) Queues with reneging and balking policies validate. `[queue, testing]`
  _src: efemera/tests/test_ir_schema.py_

---

## tests/test_pheromone_ledger.py (2 gaps)

### [IC] (1 items)
- (0.64) to_dict should return copies, not references. `[testing]`
  _src: efemera/tests/test_pheromone_ledger.py_

### [UC] (1 items)
- (0.60) None team_id/source_hive should become empty strings. `[hive, testing]`
  _src: efemera/tests/test_pheromone_ledger.py_

---

## tests/test_pheromone_scope.py (2 gaps)

### [UC] (2 items)
- (0.65) A ranker that reverses within each tier should reverse intra-tier order. `[testing]`
  _src: efemera/tests/test_pheromone_scope.py_
- (0.65) PropagationManager tiers should cover the same scopes as the router. `[scope, testing]`
  _src: efemera/tests/test_pheromone_scope.py_

---

## tests/test_pheromone_transport.py (2 gaps)

### [UC] (2 items)
- (0.60) StubTransport should behave identically to LocalhostTransport for queries. `[testing]`
  _src: efemera/tests/test_pheromone_transport.py_
- (0.60) Double claim on FileTransport should fail. `[file, testing]`
  _src: efemera/tests/test_pheromone_transport.py_

---

## tests/test_pheromone_trust.py (2 gaps)

### [UC] (2 items)
- (0.60) Sponsor with rho exactly equal to min_rho should succeed. `[testing]`
  _src: efemera/tests/test_pheromone_trust.py_
- (0.60) Sponsor with rho just below min_rho should fail. `[testing]`
  _src: efemera/tests/test_pheromone_trust.py_

---

## tests/test_production_actors.py (2 gaps)

### [OR] (1 items)
- (0.65) After timeout, completed_at should be set. `[testing]`
  _src: efemera/tests/test_production_actors.py_

### [UC] (1 items)
- (0.60) Event log should contain a token_moved event. `[testing]`
  _src: efemera/tests/test_production_actors.py_

---

## tests/test_proposals.py (2 gaps)

### [CON] (2 items)
- (0.65) Test validate_proposal_json with invalid proposal_type returns (False, error). `[testing]`
  _src: efemera/tests/test_proposals.py_
- (0.65) Test validate_proposal_json with empty affected_tasks returns (False, error). `[tasks, testing]`
  _src: efemera/tests/test_proposals.py_

---

## tests/test_raqcoon_sync.py (2 gaps)

### [UC] (2 items)
- (0.60) Test that ensure_sync_table creates the table. `[testing]`
  _src: efemera/tests/test_raqcoon_sync.py_
- (0.60) Test that ensure_sync_table creates initial row. `[testing]`
  _src: efemera/tests/test_raqcoon_sync.py_

---

## tests/test_surrogate_dataset.py (2 gaps)

### [UC] (2 items)
- (0.60) Train and val should have disjoint run_ids. `[testing]`
  _src: efemera/tests/test_surrogate_dataset.py_
- (0.60) 1000 samples should be handled quickly. `[ui, testing]`
  _src: efemera/tests/test_surrogate_dataset.py_

---

## tests/test_surrogate_online.py (2 gaps)

### [UC] (2 items)
- (0.65) update_every=0 means should_update is always True when enabled. `[testing]`
  _src: efemera/tests/test_surrogate_online.py_
- (0.60) After capping, the most recent samples should remain. `[testing]`
  _src: efemera/tests/test_surrogate_online.py_

---

## tests/test_tabletop_decision_points.py (2 gaps)

### [UC] (2 items)
- (0.65) Tracing back in a circular flow should not loop forever. `[testing]`
  _src: efemera/tests/test_tabletop_decision_points.py_
- (0.60) Override should fire before node_type. `[testing]`
  _src: efemera/tests/test_tabletop_decision_points.py_

---

## tests/test_tabletop_engine_integration.py (2 gaps)

### [IC] (2 items)
- (0.64) PauseFilter returns should_pause=True for human nodes. `[human, testing]`
  _src: efemera/tests/test_tabletop_engine_integration.py_
- (0.64) PauseFilter returns should_pause=False for plain task nodes. `[testing]`
  _src: efemera/tests/test_tabletop_engine_integration.py_

---

## tests/test_task_performance.py (2 gaps)

### [UC] (2 items)
- (0.65) Test 7: Sample count warning: flag when N < 5 (should_block=True) and N < 10 (should_warn=True) `[testing]`
  _src: efemera/tests/test_task_performance.py_
- (0.60) """Test 7: Sample count warning: flag when N < 5 (should_block=True) and N < 10 (should_warn=True)""" `[testing]`
  _src: efemera/tests/test_task_performance.py_

---

## tests/test_workbench_e2e.py (2 gaps)

### [CON] (1 items)
- (0.65) The scaffolded PIE with workbench passes validate_pie(). `[testing]`
  _src: efemera/tests/test_workbench_e2e.py_

### [UC] (1 items)
- (0.60) Sync with no events should succeed silently. `[testing]`
  _src: efemera/tests/test_workbench_e2e.py_

---

## W2-05-COMPLETION-SUMMARY.md (2 gaps)

### [AD] (2 items)
- (0.72) - **Rationale:** Allows maximum flexibility while protecting against accidental disasters
  _src: simdecisions-2/W2-05-COMPLETION-SUMMARY.md_
- (0.72) - **Rationale:** Balances reliability vs latency; catches most transient conflicts
  _src: simdecisions-2/W2-05-COMPLETION-SUMMARY.md_

---

## node_modules/tapable (2 gaps)

### [UC] (2 items)
- (0.62) tapPromise: (
  _src: simdecisions-2/node_modules/tapable/README.md_
- (0.62) tapPromise: (opt, fn) => this.tapPromise(mergeOptions(opt), fn),
  _src: simdecisions-2/node_modules/tapable/lib/Hook.js_

---

## components/mode-views (2 gaps)

### [AD] (1 items)
- (0.66) description = `Decision: ${choice}`;
  _src: simdecisions-2/src/components/mode-views/PlaybackView.tsx_

### [UC] (1 items)
- (0.65) updateConstraint: vi.fn(), `[testing]`
  _src: simdecisions-2/src/components/mode-views/__tests__/DesignView.test.tsx_

---

## services/execution (2 gaps)

### [AD] (2 items)
- (0.62) requiresDecision: boolean; `[ui]`
  _src: simdecisions-2/src/services/execution/graphTraversal.ts_
- (0.62) requiresDecision: false, `[ui]`
  _src: simdecisions-2/src/services/execution/graphTraversal.ts_

---

## stores/optimizationStore.ts (2 gaps)

### [UC] (2 items)
- (0.65) updateConstraint: (key: keyof OptimizationConstraints, value: any) => void;
  _src: simdecisions-2/src/stores/optimizationStore.ts_
- (0.65) updateConstraint: (key, value) => {
  _src: simdecisions-2/src/stores/optimizationStore.ts_

---

## tests/engine (2 gaps)

### [UC] (2 items)
- (0.65) Linear flow: start → task1 → task2 → task3 → end. Should complete. `[testing]`
  _src: simdecisions-2/tests/engine/test_runtime.py_
- (0.60) ExecutionResult should include duration. `[testing]`
  _src: simdecisions-2/tests/engine/test_runtime.py_

---

## _inbox/2026-02-21-PHASE-IR-V2-DESIGN-ADDENDUM.md (2 gaps)

### [TMP] (1 items)
- (0.57) PHASE-IR v2.0 Design Addendum
  _src: _inbox/2026-02-21-PHASE-IR-V2-DESIGN-ADDENDUM.md_

### [UC] (1 items)
- (0.55) zone: distant
  _src: _inbox/2026-02-21-PHASE-IR-V2-DESIGN-ADDENDUM.md_

---

## _inbox/2026-02-25-SPEC-Q33N-COWORK-PLUGIN.md (2 gaps)

### [UC] (1 items)
- (0.55) You are not the author. You are the judge. `[auth]`
  _src: _inbox/2026-02-25-SPEC-Q33N-COWORK-PLUGIN.md_

### [CON] (1 items)
- (0.62) A lost constraint is worse than a hallucinated enrichment.
  _src: _inbox/2026-02-25-SPEC-Q33N-COWORK-PLUGIN.md_

---

## _inbox/2026-03-06-HARNESS-ARCHITECTURE-SESSION.md (2 gaps)

### [AD] (2 items)
- (0.66) Harness Architecture Session
  _src: _inbox/2026-03-06-HARNESS-ARCHITECTURE-SESSION.md_
- (0.66) 3. Harness Architecture (Clarified)
  _src: _inbox/2026-03-06-HARNESS-ARCHITECTURE-SESSION.md_

---

## _inbox/ADR-HIVEFS-001.md (2 gaps)

### [AD] (2 items)
- (0.66) **Decision: isomorphic-git is the versioning engine for HiveFS.** `[git, hive]`
  _src: _inbox/ADR-HIVEFS-001.md_
- (0.61) ADR-HIVEFS-001: HiveFS Architecture Decisions `[hive]`
  _src: _inbox/ADR-HIVEFS-001.md_

---

## _inbox/ADR-Requirements-Remaining.md (2 gaps)

### [AD] (1 items)
- (0.61) ADR-017: Multi-Tenant Architecture
  _src: _inbox/ADR-Requirements-Remaining.md_

### [UC] (1 items)
- (0.55) [ ] Flow visualization?
  _src: _inbox/ADR-Requirements-Remaining.md_

---

## _inbox/Q88N-ANSWERS-TO-CC-QUESTIONS.md (2 gaps)

### [AD] (1 items)
- (0.66) **Decision: Equal-weight normalized scoring. Ship it.**
  _src: _inbox/Q88N-ANSWERS-TO-CC-QUESTIONS.md_

### [CON] (1 items)
- (0.68) **Decision: Simple, never-expiring, immediate revocation on regeneration.**
  _src: _inbox/Q88N-ANSWERS-TO-CC-QUESTIONS.md_

---

## _inbox/SPEC-HIVE-DISPATCH-GOVERNANCE-001-v3.md (2 gaps)

### [UC] (2 items)
- (0.70) HiveGovernor does NOT encode rules — rules live in IR `[hive, governance]`
  _src: _inbox/SPEC-HIVE-DISPATCH-GOVERNANCE-001-v3.md_
- (0.70) Process-13 is preferred but `process13_enabled` is a parameter — measured, not mandated `[hive, governance]`
  _src: _inbox/SPEC-HIVE-DISPATCH-GOVERNANCE-001-v3.md_

---

## _inbox/files-23-extracted (2 gaps)

### [AD] (2 items)
- (0.66) decision: BPMNGatewayNode,
  _src: _inbox/files-23-extracted/TASK-VIEW-002-BPMN-VIEW.md_
- (0.62) ) -> GateDecision:
  _src: _inbox/files-23-extracted/TASK-SIM-035-RISK-AUTONOMY.md_

---

## _outbox/2026-02-22-BUILD-QUEUE-RANKED.md (2 gaps)

### [UC] (2 items)
- (0.68) - **Why:** Mobile-first access, iterative spec convergence, SD as peer programmer.
  _src: _outbox/2026-02-22-BUILD-QUEUE-RANKED.md_
- (0.55) **Priority:** TONIGHT
  _src: _outbox/2026-02-22-BUILD-QUEUE-RANKED.md_

---

## _outbox/2026-02-24-CODE-REVIEW-LARGE-FILES.md (2 gaps)

### [UC] (2 items)
- (0.60) Palette is reusable (could be used in other views or as a standalone widget)
  _src: _outbox/2026-02-24-CODE-REVIEW-LARGE-FILES.md_
- (0.55) Reduces cognitive load in main view file `[file]`
  _src: _outbox/2026-02-24-CODE-REVIEW-LARGE-FILES.md_

---

## _outbox/2026-02-28-IDE-COMPONENT-SPEC.md (2 gaps)

### [UC] (2 items)
- (0.57) 9. Legacy Sidebar (SHOULD BE REMOVED from scenario pages)
  _src: _outbox/2026-02-28-IDE-COMPONENT-SPEC.md_
- (0.55) Receives drops from LeftPanel palette (creates new nodes)
  _src: _outbox/2026-02-28-IDE-COMPONENT-SPEC.md_

---

## _outbox/2026-03-04-PRIMITIVE-DIALECT-ARCHITECTURE.md (2 gaps)

### [AD] (1 items)
- (0.71) decision: 'Gateway',
  _src: _outbox/2026-03-04-PRIMITIVE-DIALECT-ARCHITECTURE.md_

### [GP] (1 items)
- (0.82) **Principle:** Private patois is a privilege, not a product feature. It's Dave's language with 6laude. Everyone else gets clean, public hive culture. `[hive]`
  _src: _outbox/2026-03-04-PRIMITIVE-DIALECT-ARCHITECTURE.md_

---

## _outbox/canvas-tab-bar-differentiation-verification.md (2 gaps)

### [GP] (2 items)
- (0.62) Glassmorphism + stronger borders = dominant
  _src: _outbox/canvas-tab-bar-differentiation-verification.md_
- (0.62) Solid colors + subtle borders = subordinate
  _src: _outbox/canvas-tab-bar-differentiation-verification.md_

---

## _outbox/EGG-CODEC-IMPLEMENTATION-SUMMARY.md (2 gaps)

### [QA] (1 items)
- (0.60) **Self-describing:** Metadata visible in text editors (audit trail, governance) `[governance]`
  _src: _outbox/EGG-CODEC-IMPLEMENTATION-SUMMARY.md_

### [IC] (1 items)
- (0.58) Separator line makes format easy to split programmatically
  _src: _outbox/EGG-CODEC-IMPLEMENTATION-SUMMARY.md_

---

## _outbox/T4-CONSENT-PROMPT-DELIVERY.md (2 gaps)

### [UC] (2 items)
- (0.55) Modal centered, max-width 500px
  _src: _outbox/T4-CONSENT-PROMPT-DELIVERY.md_
- (0.55) ✅ UID generation via `crypto.randomUUID()` `[ui]`
  _src: _outbox/T4-CONSENT-PROMPT-DELIVERY.md_

---

## _outbox/W1-08-CANVAS-CHAT-BROWSER-COMPLETION.md (2 gaps)

### [UC] (2 items)
- (0.55) ChatPane receives `currentIR` and `onIRUpdate` callback
  _src: _outbox/W1-08-CANVAS-CHAT-BROWSER-COMPLETION.md_
- (0.55) Mutations trigger `handleIRUpdate` → updates scenarioStore
  _src: _outbox/W1-08-CANVAS-CHAT-BROWSER-COMPLETION.md_

---

## _outbox/bee_prompts (2 gaps)

### [UC] (2 items)
- (0.60) **efemera.live** = chat. Code in `efemera/`. EF serves `/embed/chat/{flow_id}` so SD can iframe it.
  _src: _outbox/bee_prompts/2026-02-22-Q33N-SONNET-CHAT-FLOW-DISPATCH.md_
- (0.60) **simdecisions.com** = process canvas. Code in `simdecisions-2/`. SD serves `/embed/flow/{flow_id}` so EF can iframe it.
  _src: _outbox/bee_prompts/2026-02-22-Q33N-SONNET-CHAT-FLOW-DISPATCH.md_

---

## _tools/tribunal (2 gaps)

### [AD] (1 items)
- (0.62) tribunal_decision: Omit<TribunalDecision, 'request' | 'judge_votes'> & {
  _src: _tools/tribunal/types.ts_

### [UC] (1 items)
- (0.55) TODO: When implementing:
  _src: _tools/tribunal/judges/hosted.ts_

---

## CLAUDE.md (1 gaps)

### [UC] (1 items)
- (0.60) Non-Negotiable Coding Rules
  _src: CLAUDE.md_

---

## .deia/secrets (1 gaps)

### [QA] (1 items)
- (0.71) **Purpose:** Secure backup of exposed credentials before removal
  _src: .deia/secrets/RECOVERED-SECRETS-2026-02-27.md_

---

## docs/PLATFORM-OVERVIEW.md (1 gaps)

### [UC] (1 items)
- (0.57) **Status note:** Terraform and Makefile compilers are NOT YET IMPLEMENTED (doc drift — listed in `[file]`
  _src: docs/PLATFORM-OVERVIEW.md_

---

## builds/commons_routes.py (1 gaps)

### [CON] (1 items)
- (0.60) Check if builds_completed >= bootstrap_threshold and unlock simulation. `[ui]`
  _src: efemera/src/efemera/builds/commons_routes.py_

---

## builds/routes.py (1 gaps)

### [UC] (1 items)
- (0.55) if sample_warning:
  _src: efemera/src/efemera/builds/routes.py_

---

## discord/frank_handler.py (1 gaps)

### [UC] (1 items)
- (0.55) TODO: Implement actual inbox retrieval from database `[database]`
  _src: efemera/src/efemera/discord/frank_handler.py_

---

## entities/vectors.py (1 gaps)

### [UC] (1 items)
- (0.60) Quality = sigma_outcome * (1 - sigma_rework).
  _src: efemera/src/efemera/entities/vectors.py_

---

## lineage/integrity.py (1 gaps)

### [CON] (1 items)
- (0.60) Detect cycles in derived_from relationships.
  _src: efemera/src/efemera/lineage/integrity.py_

---

## optimization/infeasibility.py (1 gaps)

### [CON] (1 items)
- (0.72) constraint:   The constraint to relax.
  _src: efemera/src/efemera/optimization/infeasibility.py_

---

## optimization/solver.py (1 gaps)

### [CON] (1 items)
- (0.72) def add_constraint(self, constraint: Constraint) -> Constraint:
  _src: efemera/src/efemera/optimization/solver.py_

---

## oracle/human.py (1 gaps)

### [TMP] (1 items)
- (0.64) Check for pending/notified/escalated requests whose deadline has passed.
  _src: efemera/src/efemera/oracle/human.py_

---

## pheromones/anti_gaming.py (1 gaps)

### [IC] (1 items)
- (0.64) Return True if *entity_rho* meets the minimum for *pheromone_type*.
  _src: efemera/src/efemera/pheromones/anti_gaming.py_

---

## pheromones/decay.py (1 gaps)

### [CON] (1 items)
- (0.60) Partition *pheromones* into (alive, expired) lists.
  _src: efemera/src/efemera/pheromones/decay.py_

---

## pheromones/file_transport.py (1 gaps)

### [UC] (1 items)
- (0.60) Deserialize a Pheromone from a JSON string.
  _src: efemera/src/efemera/pheromones/file_transport.py_

---

## pheromones/models.py (1 gaps)

### [UC] (1 items)
- (0.55) PheromoneType.warning: 3600,           # 1 hour
  _src: efemera/src/efemera/pheromones/models.py_

---

## pheromones/scope.py (1 gaps)

### [CON] (1 items)
- (0.68) Return True if a team-scoped pheromone has a team_id set. `[scope]`
  _src: efemera/src/efemera/pheromones/scope.py_

---

## pheromones/vectors.py (1 gaps)

### [CON] (1 items)
- (0.60) Check emission rights for *entity_vector* against *pheromone*.
  _src: efemera/src/efemera/pheromones/vectors.py_

---

## production/metrics.py (1 gaps)

### [UC] (1 items)
- (0.60) Build a HealthStatus from a Supervisor and collected metrics. `[ui]`
  _src: efemera/src/efemera/production/metrics.py_

---

## production/skills (1 gaps)

### [CON] (1 items)
- (0.75) Validate a URL: must be well-formed, and optionally in the whitelist.
  _src: efemera/src/efemera/production/skills/utils.py_

---

## scenarios/binding.py (1 gaps)

### [UC] (1 items)
- (0.60) Orchestrate full EGG binding: playbook + steps.
  _src: efemera/src/efemera/scenarios/binding.py_

---

## scenarios/routes.py (1 gaps)

### [UC] (1 items)
- (0.65) Validate a scenario before activation.
  _src: efemera/src/efemera/scenarios/routes.py_

---

## skills/revocation_routes.py (1 gaps)

### [IC] (1 items)
- (0.69) NOTE: The blacklist GET endpoint lives at /api/skill-blacklist to avoid `[api]`
  _src: efemera/src/efemera/skills/revocation_routes.py_

---

## skills/skill_tribunal.py (1 gaps)

### [UC] (1 items)
- (0.60) Create a certification request triggered by a user concern.
  _src: efemera/src/efemera/skills/skill_tribunal.py_

---

## skills/skill_tribunal_routes.py (1 gaps)

### [UC] (1 items)
- (0.60) Create a certification request for a skill.
  _src: efemera/src/efemera/skills/skill_tribunal_routes.py_

---

## surrogates/drift.py (1 gaps)

### [IC] (1 items)
- (0.64) Return True if the report indicates retraining is warranted.
  _src: efemera/src/efemera/surrogates/drift.py_

---

## surrogates/serving.py (1 gaps)

### [UC] (1 items)
- (0.65) True when the prediction is within distribution and well calibrated.
  _src: efemera/src/efemera/surrogates/serving.py_

---

## surrogates/time_series.py (1 gaps)

### [UC] (1 items)
- (0.60) Train the model from a SurrogateDataset.
  _src: efemera/src/efemera/surrogates/time_series.py_

---

## surrogates/uncertainty.py (1 gaps)

### [IC] (1 items)
- (0.64) Return the empirical coverage fraction.
  _src: efemera/src/efemera/surrogates/uncertainty.py_

---

## tabletop/trace.py (1 gaps)

### [AD] (1 items)
- (0.66) lines.append(f"- **Decision:** {dp.decision_made.choice}")
  _src: efemera/src/efemera/tabletop/trace.py_

---

## tests/test_adr004_integration.py (1 gaps)

### [UC] (1 items)
- (0.60) A non-graduated entity should not be demoted. `[testing]`
  _src: efemera/tests/test_adr004_integration.py_

---

## tests/test_adr005_integration.py (1 gaps)

### [CON] (1 items)
- (0.65) generate_egg_from_source -> parse_egg -> validate_egg -> import_egg succeeds. `[testing]`
  _src: efemera/tests/test_adr005_integration.py_

---

## tests/test_adr007_integration.py (1 gaps)

### [UC] (1 items)
- (0.65) Spending exactly the max_usd should be allowed (used + request == max). `[testing]`
  _src: efemera/tests/test_adr007_integration.py_

---

## tests/test_adr014_integration.py (1 gaps)

### [UC] (1 items)
- (0.60) class TestRationale: `[testing]`
  _src: efemera/tests/test_adr014_integration.py_

---

## tests/test_carbon.py (1 gaps)

### [UC] (1 items)
- (0.55) assert any("carbon_budget_warning:daily" in e for e in events) `[testing]`
  _src: efemera/tests/test_carbon.py_

---

## tests/test_cors_csp.py (1 gaps)

### [IC] (1 items)
- (0.66) CSP header should be on embed endpoint. `[testing]`
  _src: efemera/tests/test_cors_csp.py_

---

## tests/test_dialect_roundtrip.py (1 gaps)

### [UC] (1 items)
- (0.60) Score should equal lossless / (lossless + lossy). `[testing]`
  _src: efemera/tests/test_dialect_roundtrip.py_

---

## tests/test_e2e_entity_lifecycle.py (1 gaps)

### [UC] (1 items)
- (0.65) ADR-004: With only 10 events, entity should NOT be eligible. `[testing]`
  _src: efemera/tests/test_e2e_entity_lifecycle.py_

---

## tests/test_embed_chrome.py (1 gaps)

### [UC] (1 items)
- (0.65) Test that JavaScript adds 'embedded' class to body when isEmbedded is true. `[testing]`
  _src: efemera/tests/test_embed_chrome.py_

---

## tests/test_gate_enforcer.py (1 gaps)

### [UC] (1 items)
- (0.60) class TestCheckpoint5Rationale: `[testing]`
  _src: efemera/tests/test_gate_enforcer.py_

---

## tests/test_llm_review.py (1 gaps)

### [CON] (1 items)
- (0.65) Test that proposals have status 'validated' after successful review. `[testing]`
  _src: efemera/tests/test_llm_review.py_

---

## tests/test_llm_review_real_provider.py (1 gaps)

### [UC] (1 items)
- (0.60) Should raise RuntimeError when ANTHROPIC_API_KEY is not set. `[api, testing]`
  _src: efemera/tests/test_llm_review_real_provider.py_

---

## tests/test_message_types.py (1 gaps)

### [OR] (1 items)
- (0.64) Default message_type should be 'text'. `[testing]`
  _src: efemera/tests/test_message_types.py_

---

## tests/test_optimization_constraints.py (1 gaps)

### [UC] (1 items)
- (0.65) class TestParsedConstraint: `[testing]`
  _src: efemera/tests/test_optimization_constraints.py_

---

## tests/test_optimization_objectives.py (1 gaps)

### [UC] (1 items)
- (0.65) class TestOptConstraint: `[testing]`
  _src: efemera/tests/test_optimization_objectives.py_

---

## tests/test_optimization_warm_start.py (1 gaps)

### [UC] (1 items)
- (0.60) Column with zero std should get std=1.0 in NormParams. `[testing]`
  _src: efemera/tests/test_optimization_warm_start.py_

---

## tests/test_pareto.py (1 gaps)

### [UC] (1 items)
- (0.65) Pareto calculation should complete in under 100ms for 50 proposals. `[testing]`
  _src: efemera/tests/test_pareto.py_

---

## tests/test_pheromone_ephemera_transport.py (1 gaps)

### [UC] (1 items)
- (0.65) When emitting a pheromone with the same id, the old message `[testing]`
  _src: efemera/tests/test_pheromone_ephemera_transport.py_

---

## tests/test_pheromone_integration.py (1 gaps)

### [UC] (1 items)
- (0.60) After quarantine, a sponsor event should indicate release. `[testing]`
  _src: efemera/tests/test_pheromone_integration.py_

---

## tests/test_raqcoon_cli.py (1 gaps)

### [UC] (1 items)
- (0.57) Note: cmd_open / cmd_sync / cmd_pack are now wired to real implementations `[testing]`
  _src: efemera/tests/test_raqcoon_cli.py_

---

## tests/test_raqcoon_integration.py (1 gaps)

### [CON] (1 items)
- (0.65) cmd_open wires through: validate -> start_server -> open_workbench. `[testing]`
  _src: efemera/tests/test_raqcoon_integration.py_

---

## tests/test_raqcoon_ledger.py (1 gaps)

### [CON] (1 items)
- (0.65) get_pie_dir() must raise NotImplementedError when called bare. `[testing]`
  _src: efemera/tests/test_raqcoon_ledger.py_

---

## tests/test_rate_limit.py (1 gaps)

### [UC] (1 items)
- (0.60) X-Forwarded-For should be used as the client IP. `[testing]`
  _src: efemera/tests/test_rate_limit.py_

---

## tests/test_skill_tribunal.py (1 gaps)

### [CON] (1 items)
- (0.65) Tier 2 certification requires tribunal, starts as in_review. `[ui, testing]`
  _src: efemera/tests/test_skill_tribunal.py_

---

## tests/test_surrogate_oracle.py (1 gaps)

### [CON] (1 items)
- (0.65) OracleAnswer can be constructed with all required fields. `[ui, testing]`
  _src: efemera/tests/test_surrogate_oracle.py_

---

## tests/test_surrogate_training.py (1 gaps)

### [CON] (1 items)
- (0.70) validation_split near 1.0 should leave at least 1 training sample. `[validation, testing]`
  _src: efemera/tests/test_surrogate_training.py_

---

## tests/test_tabletop_session.py (1 gaps)

### [AD] (1 items)
- (0.62) class TestDecision: `[testing]`
  _src: efemera/tests/test_tabletop_session.py_

---

## tests/test_tabletop_trace.py (1 gaps)

### [UC] (1 items)
- (0.60) source="assumption:asm_001", `[testing]`
  _src: efemera/tests/test_tabletop_trace.py_

---

## tests/test_translator.py (1 gaps)

### [CON] (1 items)
- (0.65) TRANSLATE_PROMPT has required placeholders. `[ui, testing]`
  _src: efemera/tests/test_translator.py_

---

## tests/unit (1 gaps)

### [CON] (1 items)
- (0.65) Test that DEFAULT_CONFIG has all required fields `[ui, config, testing]`
  _src: efemera/tests/unit/test_config.py_

---

## flappy-001/src (1 gaps)

### [UC] (1 items)
- (0.60) Initialize pygame display, clock, and fonts.
  _src: flappy-001/src/renderer.py_

---

## global_commons/processes (1 gaps)

### [CON] (1 items)
- (0.88) "prompt": "You are Q33N coordinating task execution. You have these tasks:\n\n{{tasks_text}}\n\nParsed task list with dependencies:\n{{tasks_array}}\n `[ui, tasks, bees, human, bot]`
  _src: global_commons/processes/process-0013-validation-v1.3.json_

---

## api/tests (1 gaps)

### [IC] (1 items)
- (0.64) Creating a conversation should return a resume_code. `[api, testing]`
  _src: simdecisions-2/api/tests/test_resume_codes.py_

---

## node_modules/.vite (1 gaps)

### [UC] (1 items)
- (0.62) didUsePromise: false,
  _src: simdecisions-2/node_modules/.vite/deps/chunk-NKQYQQPA.js_

---

## node_modules/@tailwindcss (1 gaps)

### [CON] (1 items)
- (0.64) `);let r=[],t=[],i=null,o="",l;for(let n=0;n<e.length;n++){let s=e.charCodeAt(n);switch(s){case je:{o+=e[n]+e[n+1],n++;break}case er:{if(o.length>0){l `[ui, bot, file, path]`
  _src: simdecisions-2/node_modules/@tailwindcss/node/dist/index.js_

---

## node_modules/espree (1 gaps)

### [UC] (1 items)
- (0.55) TODO: See if this is an Acorn bug
  _src: simdecisions-2/node_modules/espree/lib/token-translator.js_

---

## node_modules/fast-json-patch (1 gaps)

### [UC] (1 items)
- (0.57) Any remaining changes are delivered synchronously (as in `jsonpatch.generate`). Note: this is different that ES6/7 `Object.unobserve`, which delivers 
  _src: simdecisions-2/node_modules/fast-json-patch/README.md_

---

## node_modules/hast-util-to-jsx-runtime (1 gaps)

### [TMP] (1 items)
- (0.61) Note: test this when Solid doesn’t want to merge my upcoming PR.
  _src: simdecisions-2/node_modules/hast-util-to-jsx-runtime/lib/index.js_

---

## node_modules/hermes-parser (1 gaps)

### [CON] (1 items)
- (0.72) constraint: this.deserializeNode(),
  _src: simdecisions-2/node_modules/hermes-parser/dist/HermesParserNodeDeserializers.js_

---

## node_modules/json-buffer (1 gaps)

### [UC] (1 items)
- (0.55) TODO: handle reviver/dehydrate function like normal
  _src: simdecisions-2/node_modules/json-buffer/index.js_

---

## node_modules/micromark (1 gaps)

### [UC] (1 items)
- (0.57) Note: this field is called `_closeFlow` but it also closes containers.
  _src: simdecisions-2/node_modules/micromark/dev/lib/initialize/document.js_

---

## node_modules/micromark-core-commonmark (1 gaps)

### [UC] (1 items)
- (0.57) Note: `markdown-rs` also parses GFM footnotes here, which for us is in
  _src: simdecisions-2/node_modules/micromark-core-commonmark/dev/lib/label-end.js_

---

## node_modules/react (1 gaps)

### [UC] (1 items)
- (0.62) didUsePromise: !1,
  _src: simdecisions-2/node_modules/react/cjs/react.development.js_

---

## node_modules/react-markdown (1 gaps)

### [UC] (1 items)
- (0.55) transform mdast to hast (HTML syntax tree)
  _src: simdecisions-2/node_modules/react-markdown/readme.md_

---

## node_modules/unified (1 gaps)

### [UC] (1 items)
- (0.57) Note: we can’t use `callback` yet as it messes up `this`:
  _src: simdecisions-2/node_modules/unified/lib/index.js_

---

## node_modules/unist-util-is (1 gaps)

### [PAT] (1 items)
- (0.56) Note: overloads in JSDoc can’t yet use different `@template`s.
  _src: simdecisions-2/node_modules/unist-util-is/lib/index.js_

---

## node_modules/uri-js (1 gaps)

### [UC] (1 items)
- (0.55) TODO: normalize IPv6 address as per RFC 5952
  _src: simdecisions-2/node_modules/uri-js/dist/es5/uri.all.js_

---

## node_modules/xterm (1 gaps)

### [UC] (1 items)
- (0.60) TODO: Remove pages from _activePages when all rows are filled
  _src: simdecisions-2/node_modules/xterm/src/browser/renderer/shared/TextureAtlas.ts_

---

## components/apps (1 gaps)

### [UC] (1 items)
- (0.55) TODO: Save to node.appState and update paneConfig `[config]`
  _src: simdecisions-2/src/components/apps/FrankCLI.tsx_

---

## components/bridge (1 gaps)

### [UC] (1 items)
- (0.55) promptWarning: null, `[testing]`
  _src: simdecisions-2/src/components/bridge/ChatPane.postMessage.test.tsx_

---

## hooks/useCanvasChatBrowser.ts (1 gaps)

### [UC] (1 items)
- (0.55) promptWarning: string | null;
  _src: simdecisions-2/src/hooks/useCanvasChatBrowser.ts_

---

## services/ir (1 gaps)

### [AD] (1 items)
- (0.62) NODE_TYPE_DECISION: 4,
  _src: simdecisions-2/src/services/ir/protobufCodec.ts_

---

## utils/bpmn-export.ts (1 gaps)

### [AD] (1 items)
- (0.66) decision: 'exclusiveGateway',
  _src: simdecisions-2/src/utils/bpmn-export.ts_

---

## utils/colors.ts (1 gaps)

### [AD] (1 items)
- (0.66) decision: 'var(--sd-orange-dimmer)',
  _src: simdecisions-2/src/utils/colors.ts_

---

## tests/fidelity (1 gaps)

### [CON] (1 items)
- (0.65) Require either llm_callable or mock_mode. `[ui, testing]`
  _src: tests/fidelity/test_drift.py_

---

## tests/governance (1 gaps)

### [UC] (1 items)
- (0.70) class TestBusinessHoursConstraint: `[governance, testing]`
  _src: tests/governance/test_policy_engine.py_

---

## _inbox/2026-02-24-CLAUDE-AI-ARCHITECTURE-CHAT.md (1 gaps)

### [AD] (1 items)
- (0.66) SimDecisions Architecture Walkthrough
  _src: _inbox/2026-02-24-CLAUDE-AI-ARCHITECTURE-CHAT.md_

---

## _inbox/ADR-Registry-Complete.md (1 gaps)

### [UC] (1 items)
- (0.60) Proposed ADRs (Requirements Outlined) `[ui]`
  _src: _inbox/ADR-Registry-Complete.md_

---

## _inbox/BACKLOG-dashboard-redesign-mockup.md (1 gaps)

### [UC] (1 items)
- (0.57) **Note:** User said "make a note on bl for later for us to discuss" - this is that note.
  _src: _inbox/BACKLOG-dashboard-redesign-mockup.md_

---

## _inbox/IMPL-PLAN-001-ZORTZI-FOUNDATION-BUILD.md (1 gaps)

### [UC] (1 items)
- (0.68) **Purpose: Shared contracts that all three streams depend on**
  _src: _inbox/IMPL-PLAN-001-ZORTZI-FOUNDATION-BUILD.md_

---

## _inbox/INTEROP-TEST-SCENARIOS.md (1 gaps)

### [CON] (1 items)
- (0.75) **Purpose:** Behavioral end-to-end test scenarios for validating composition across all 13 ADRs. `[testing]`
  _src: _inbox/INTEROP-TEST-SCENARIOS.md_

---

## _inbox/archive (1 gaps)

### [AD] (1 items)
- (0.60) Describe intent → English `[hive]`
  _src: _inbox/archive/SPEC-EGG-FORMAT-v2.md_

---

## _inbox/files-20-extracted (1 gaps)

### [UC] (1 items)
- (0.55) warning: "#FF9800"
  _src: _inbox/files-20-extracted/contact_center.vocab.yaml_

---

## _inbox/files-24-extracted (1 gaps)

### [UC] (1 items)
- (0.55) private promptWarning: string | null = null;
  _src: _inbox/files-24-extracted/TASK-W1-05-LLM-ADAPTER.md_

---

## _inbox/files-43 (1 gaps)

### [UC] (1 items)
- (0.57) **Build note:** This is the highest-leverage office productivity wedge. Otter.ai and Fireflies users already have the habit. The upgrade is KB integra `[ui]`
  _src: _inbox/files-43/2026-03-07-COMPETITIVE-LANDSCAPE-ADDENDUM.md_

---

## _inbox/sd-2_build (1 gaps)

### [UC] (1 items)
- (0.55) Full editing capability
  _src: _inbox/sd-2_build/simdecisions-ui-specs/specs/04-IMPLEMENTATION-SEQUENCE.md_

---

## _outbox/2026-02-21-CODE-FACTORY-TOURNAMENT-PHASE-IR.md (1 gaps)

### [AD] (1 items)
- (0.66) "outputs": ["decision: rewrite | decompose | flag_human"] `[human]`
  _src: _outbox/2026-02-21-CODE-FACTORY-TOURNAMENT-PHASE-IR.md_

---

## _outbox/2026-02-21-MODEL-ROUTER-PIR.md (1 gaps)

### [UC] (1 items)
- (0.72) **Purpose:** Train ourselves to predict which LLM is best per task, on 4 criteria.
  _src: _outbox/2026-02-21-MODEL-ROUTER-PIR.md_

---

## _outbox/2026-02-22-PROVENANCE-FILES19.md (1 gaps)

### [QA] (1 items)
- (0.61) All features are testable and proven
  _src: _outbox/2026-02-22-PROVENANCE-FILES19.md_

---

## _outbox/2026-02-22-PROVENANCE-FILES20.md (1 gaps)

### [UC] (1 items)
- (0.55) Biology domain patterns (predator_prey, flocking, foraging, reproduction, migration)
  _src: _outbox/2026-02-22-PROVENANCE-FILES20.md_

---

## _outbox/2026-02-25-QUALITY-COMPLIANCE-ENGINE-SPEC.md (1 gaps)

### [AD] (1 items)
- (0.62) final_decision: str,
  _src: _outbox/2026-02-25-QUALITY-COMPLIANCE-ENGINE-SPEC.md_

---

## _outbox/2026-02-25-SESSION-TRACEABILITY-BREAKTHROUGH.md (1 gaps)

### [CON] (1 items)
- (0.72) **Revised Constraint:**
  _src: _outbox/2026-02-25-SESSION-TRACEABILITY-BREAKTHROUGH.md_

---

## _outbox/2026-02-25-SHOWCASE-FACTORY-SPEC-REVISIONS.md (1 gaps)

### [CON] (1 items)
- (0.60) Products 1, 2, 3 require anonymous access (public demos) `[ui]`
  _src: _outbox/2026-02-25-SHOWCASE-FACTORY-SPEC-REVISIONS.md_

---

## _outbox/2026-02-26-ROUNDTRIP-OPTIMIZATION-SPEC.md (1 gaps)

### [AD] (1 items)
- (0.65) # The Only Tradeoff: Diagnostic Isolation
  _src: _outbox/2026-02-26-ROUNDTRIP-OPTIMIZATION-SPEC.md_

---

## _outbox/2026-02-27-SECRETS-AUDIT-REPORT.md (1 gaps)

### [CON] (1 items)
- (0.65) ⚠️ **WARNING:** This rewrites git history. All collaborators must re-clone. `[git]`
  _src: _outbox/2026-02-27-SECRETS-AUDIT-REPORT.md_

---

## _outbox/2026-02-28-GUI-DESIGN-DECISIONS.md (1 gaps)

### [UC] (1 items)
- (0.55) Muda detection (7 wastes) as part of optimizer output
  _src: _outbox/2026-02-28-GUI-DESIGN-DECISIONS.md_

---

## _outbox/2026-02-28-IDE-COMPONENT-SPEC-ADDENDUM.md (1 gaps)

### [AD] (1 items)
- (0.68) - Rationale: Neutral, professional, no mascot energy
  _src: _outbox/2026-02-28-IDE-COMPONENT-SPEC-ADDENDUM.md_

---

## _outbox/2026-02-28-SD-COM-REFACTOR-PLAN.md (1 gaps)

### [UC] (1 items)
- (0.55) Branch infrastructure exists in scenarioStore (createBranch, switchBranch, deleteBranch)
  _src: _outbox/2026-02-28-SD-COM-REFACTOR-PLAN.md_

---

## _outbox/2026-03-01-GUI-WAVE-2-SPEC.md (1 gaps)

### [UC] (1 items)
- (0.68) **Goal:** Breakpoints, ARIA, layout tool, TabletopView
  _src: _outbox/2026-03-01-GUI-WAVE-2-SPEC.md_

---

## _outbox/2026-03-03-frank-server-chat-complete.md (1 gaps)

### [UC] (1 items)
- (0.55) PostgreSQL-compatible (server_default=func.now(), DateTime with timezone)
  _src: _outbox/2026-03-03-frank-server-chat-complete.md_

---

## _outbox/2026-03-06-ISOLATED-ROUTER-VERIFICATION.md (1 gaps)

### [AD] (1 items)
- (0.59) DesignerApp URL includes `?embedded=true&route=/design/new`
  _src: _outbox/2026-03-06-ISOLATED-ROUTER-VERIFICATION.md_

---

## _outbox/ADR-014-020-VALIDATION-RESULTS.md (1 gaps)

### [AD] (1 items)
- (0.61) Proposed ADR-017: Multi-Tenant Architecture
  _src: _outbox/ADR-014-020-VALIDATION-RESULTS.md_

---

## _outbox/ADR-014-ADDENDUM-Implementation-Gaps.md (1 gaps)

### [UC] (1 items)
- (0.62) **Why:** Prevents ping-pong escalations for minor ambiguities. `[ui]`
  _src: _outbox/ADR-014-ADDENDUM-Implementation-Gaps.md_

---

## _outbox/AUDIT-COMPLETE-2026-02-22.md (1 gaps)

### [AD] (1 items)
- (0.66) 4. Decision: Approve standardization initiative
  _src: _outbox/AUDIT-COMPLETE-2026-02-22.md_

---

## _outbox/BUGS-2026-02-25.md (1 gaps)

### [UC] (1 items)
- (0.55) Solves the "unsaved changes" problem entirely
  _src: _outbox/BUGS-2026-02-25.md_

---

## _outbox/parse_results.py (1 gaps)

### [UC] (1 items)
- (0.55) print(f"  Todo: {d.get('numTodoTests')}")
  _src: _outbox/parse_results.py_

---

## _outbox/TASK-EXECUTION-ARCHITECTURE.md (1 gaps)

### [UC] (1 items)
- (0.72) **Why:** Simplicity. Tasks are ephemeral (lost on restart), but git commits are durable. `[git, tasks]`
  _src: _outbox/TASK-EXECUTION-ARCHITECTURE.md_

---

## _outbox/W1-01-COMPLETION-SUMMARY.md (1 gaps)

### [AD] (1 items)
- (0.61) Architecture Diagram
  _src: _outbox/W1-01-COMPLETION-SUMMARY.md_

---

## _outbox/W2-04-AUTO-MODE-TOGGLE-COMPLETION.md (1 gaps)

### [UC] (1 items)
- (0.68) - **Purpose:** Reusable toggle control for enabling/disabling auto-mode
  _src: _outbox/W2-04-AUTO-MODE-TOGGLE-COMPLETION.md_

---

## _outbox/W2-04-IMPLEMENTATION-SUMMARY.md (1 gaps)

### [AD] (1 items)
- (0.68) **Rationale:** AutoModeToggle can be reused elsewhere, ScenarioSettings orchestrates.
  _src: _outbox/W2-04-IMPLEMENTATION-SUMMARY.md_

---
