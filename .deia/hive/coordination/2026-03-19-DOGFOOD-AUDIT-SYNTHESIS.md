# Dogfood Audit Synthesis — 2026-03-19

**Compiled by:** Q33NR
**Bees:** BEE-DA1 through BEE-DA5 (all Sonnet, all COMPLETE)
**Total cost:** $12.89 | Total turns: 183 | Total duration: ~22 min

---

## Executive Summary

The dogfood IDE pipeline — terminal prompt → LLM → structured response → pane routing → visual render — is **fully ported and significantly extended** beyond platform. Zero P0 security issues found. Three NVWR items (2x P2, 1x P1). The biggest gap is not in ported code but in **unbuilt spec features**: the Visual EGG Builder (Product Session §7) and Draft/Release Model (§8) are 0% implemented in either repo.

**Shiftcenter is AHEAD of platform** in: mute system (5 levels), SDEditor modes (6 vs 2), terminal routing modes (5 vs 1), file attachment, syntax highlighting, visual diff viewer, bus-routed LLM calls, and efemera chat integration.

---

## Section 1: Port As-Is (Correctly Ported, No Changes Needed)

These features were ported from platform with zero divergence or intentional architectural adaptation:

| Feature | Platform Source | Shiftcenter Target | Bee |
|---------|---------------|-------------------|-----|
| Terminal → LLM call chain | useTerminalSession.ts | useTerminal.ts | DA1 |
| Envelope parsing (6-slot JSON) | responseRouter.ts | terminalResponseRouter.ts | DA1 |
| to_text ops routing (append/replace/insert/delete/set) | responseRouter.ts | terminalResponseRouter.ts | DA1 |
| Dialect system (patois + envelope + IR) | dialectLoader.ts | dialectLoader.ts | DA1 |
| Zone 2 rendering (5 entry types) | FrankCLI.tsx | TerminalApp.tsx | DA1 |
| MessageBus routing (subscribe/send/nonce) | shell.context.js | messageBus.ts | DA2 |
| GovernanceProxy permissions enforcement | GovernanceProxy.tsx | GovernanceProxy.tsx | DA2 |
| EGG permissions (bus_emit/bus_receive) | EGG schema | EGG schema | DA2 |
| Platform invariants (5 types bypass governance) | GovernanceProxy.tsx | GovernanceProxy.tsx | DA2 |
| settings_advertisement (schema discovery) | EfemeraApp.tsx | same pattern | DA2 |
| Unified diff parser (applyUnifiedDiff) | unifiedDiff.ts | unifiedDiff.ts | DA4 |
| Co-Author paragraph rewrite | SDEditor.tsx | SDEditor.tsx (bus-routed) | DA4 |
| CSS variable pattern (var(--sd-*)) | sd-editor.css | sd-editor.css | DA4 |
| Shell executor (allowlist/denylist + ledger) | N/A (new) | shell.py + executor.py | DA5 |
| JWT auth via ra96it JWKS | N/A (new) | dependencies.py | DA5 |

---

## Section 2: Shiftcenter Extensions (Ahead of Platform)

Features that exist in shiftcenter but NOT in platform:

| Feature | Description | Bee |
|---------|-------------|-----|
| 5-level mute system | none/notifications/inbound/outbound/full — enforced during send() and broadcast | DA2 |
| 4 new terminal routing modes | ai, ir, relay, canvas (platform has shell only) | DA1 |
| File attachment support | Attach file content to LLM prompt | DA1 |
| Proxy LLM mode | Route through hivenode /llm/chat with BYOK key forwarding | DA1 |
| Visual diff viewer (DiffView.tsx) | Color-coded unified diff with dual gutter | DA4 |
| Code mode with syntax highlighting | highlight.js, 9 languages, line numbers, copy button | DA4 |
| 4 new SDEditor modes | code, diff, process-intake, chat (platform has rendered + raw) | DA4 |
| Bus-routed LLM calls | Co-Author routes through bus to terminal, not direct provider | DA4 |
| Efemera chat integration | channel:selected + channel:message-received in text-pane | DA4 |
| metrics_advertisement invariant | 5th platform invariant (platform has 4) | DA2 |

**Recommendation:** Port mute system, code mode, and visual diff viewer from shiftcenter back to platform.

---

## Section 3: P0 Fixes Required

**None.** Zero P0 security or correctness issues found across all 5 audits.

---

## Section 4: Missing for Dogfood (Spec Gaps)

These are features described in Product Session spec that exist in neither repo:

| Gap | Spec Reference | Severity | Bee |
|-----|---------------|----------|-----|
| scene_system design stage | §7.1 | FULL GAP — 0% built | DA3 |
| ELEMENT_SELECTED bus event | §7.1 | FULL GAP — 0% built | DA3 |
| Click-to-select / hover-to-highlight | §7.1 | FULL GAP — 0% built | DA3 |
| EGG writer (shell tree → .egg.md) | §7, §9.4 | FULL GAP — 0% built | DA3 |
| Register block (draft change tracking) | §8.1 | FULL GAP — 0% built | DA3 |
| Property editor terminal (universal) | §7.1 | ARCHITECTURE GAP — canvas has React panel, spec wants terminal | DA3 |
| Release command (strip register, bump version) | §8.3 | FULL GAP — 0% built | DA3 |
| Diff-queue mode for multi-hunk LLM edits | EGG setting stub | STUB ONLY — 0% built | DA4 |
| General-purpose WebSocket (presence + typing) | Platform efemera ws.py | NOT PORTED — platform has it, shiftcenter doesn't | DA5 |
| Streaming shell output | N/A | NOT BUILT — synchronous HTTP only | DA5 |

**Key insight from DA3:** The Visual EGG Builder and Draft/Release Model are the largest spec gaps. Canvas has a local design mode for editing IR nodes, but this is NOT the universal scene_system stage described in §7. These are net-new features, not ports.

---

## Section 5: NVWR Summary

| # | Severity | Title | File | Bee |
|---|----------|-------|------|-----|
| 1 | P1 | Document platform invariants security rationale | GovernanceProxy.tsx:L139-L177 | DA2 |
| 2 | P2 | Fix MessageBus.resetMetrics() — reset subscriberCount | messageBus.ts:L257 | DA2 |
| 3 | P2 | Fix MessageBus.resetMetrics() — reset subscriberCount (platform) | shell.context.js:L163 | DA2 |

**NVWR-1 (P1):** 5 message types bypass governance AND mute. No vulnerability found (GovernanceProxy wraps every pane), but the security rationale is not documented. If future code exposes raw bus access, these become attack vectors. Document why each type is invariant.

**NVWR-2 + NVWR-3 (P2):** `resetMetrics()` in both repos resets `messageCount` and `messagesByType` but forgets `subscriberCount`. Low impact (only matters if telemetry is enabled, reset, then read). One-line fix in each repo: `this._metrics.subscriberCount = 0`.

---

## Section 6: Contradictions Resolved

| Topic | DA Finding | Resolution |
|-------|-----------|------------|
| Wiring: declarative vs imperative? | DA2: Hybrid model | EGG layout has declarative `config.links` hints; app code reads hints + uses dynamic routing. MessageBus enforces PERMISSIONS, not topology. No centralized routing table. |
| settings_advertisement = capability discovery? | DA2: No | settings_advertisement is for SETTINGS SCHEMA discovery (pane label + setting forms). Capabilities declared statically in EGG `permissions` block. |
| diff-queue exists? | DA4: No | Platform EGG declares `frank.insertMode: "diff-queue"` but zero implementation exists. Setting is a stub for planned feature. Shiftcenter correctly omits it. |
| Shell exec endpoint exists? | DA5: Yes | `/shell/exec` already exists in shiftcenter hivenode. No separate `/api/exec` needed. LOCAL-ONLY mode with allowlist/denylist + Event Ledger logging. |
| Cross-pane message leak (BUG-024)? | DA2: Architecture is sound | MessageBus is per-Shell per-window. GovernanceProxy wraps every pane. No raw bus access for applets. If BUG-024 persists, investigate app registration or browser storage, not MessageBus. |

---

## Section 7: Backlog Items Surfaced

| Title | Source | Priority | Size |
|-------|--------|----------|------|
| Implement scene_system design stage (§7.1) | DA3 | P1 | XL |
| Implement EGG writer (shell tree → .egg.md) | DA3 | P1 | L |
| Implement register block (§8.1) | DA3 | P1 | L |
| Refactor properties panel to terminal-based inspector | DA3 | P2 | M |
| Implement diff-queue mode for multi-hunk LLM edits | DA4 | P2 | L |
| Add general-purpose WebSocket to hivenode | DA5 | P2 | M |
| Add streaming shell output via WebSocket | DA5 | P2 | M |
| Add GateEnforcer integration to /shell/exec | DA5 | P2 | M |
| Document ra96it integration requirements | DA5 | P3 | S |
| Port mute system from shiftcenter → platform | DA2 | P3 | M |
| Port file attachment to platform | DA1 | P3 | S |

---

## Cost Summary

| Bee | Task | Duration | Cost | Turns | Findings | NVWR |
|-----|------|----------|------|-------|----------|------|
| DA1 | Terminal LLM pipeline | 242s | $2.26 | 26 | 10 | 0 |
| DA2 | Cross-pane bus wiring | 272s | $3.00 | 45 | 5 | 3 |
| DA3 | Design mode + EGG save | 343s | $3.15 | 45 | 7 | 0 |
| DA4 | Text-pane diff rendering | 180s | $1.80 | 24 | 8 | 0 |
| DA5 | Hivenode execution bridge | 391s | $2.68 | 43 | 5 | 0 |
| **TOTAL** | | **1428s** | **$12.89** | **183** | **35** | **3** |

---

## Verdict

**The dogfood IDE pipeline works.** Terminal → LLM → envelope → routing → pane render is complete and sound. The critical path for dogfood readiness is NOT in the existing ported code — it's in the unbuilt Visual EGG Builder and Draft/Release Model from Product Session §7-8. Those are XL net-new features that require architectural decisions before implementation.

**Immediate action items:**
1. Fix `resetMetrics()` bug (P2, one-liner, both repos)
2. Document platform invariants security rationale (P1, docs only)
3. Decide priority of scene_system / EGG writer vs other backlog items

---

**Q33NR signing off. Dogfood Audit Swarm complete. 5/5 bees returned. 35 findings. 0 P0. 3 NVWR.**
