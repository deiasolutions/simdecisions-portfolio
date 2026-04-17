# Backlog Items — Batch Insertion Prompt

**Date:** 2026-03-12
**Origin:** Q88N voice-to-spec session with Mr. AI (Claude, Anthropic)
**Master Document:** BACKLOG-USER-UTILITY-DASHBOARD.docx (consolidated backlog item with all context)

---

## Instructions

You are receiving 12 spec documents and 1 master backlog document from a product session on 2026-03-12. Each spec below should be added as a separate backlog item in the backlog items database. The master backlog document (BACKLOG-USER-UTILITY-DASHBOARD.docx) contains the full narrative context for all items — reference it for any clarification needed.

For each item below, create a backlog entry with the fields specified. All items originated from the same session and are interconnected. The `related_items` field captures those connections.

---

## ITEM 01: eFone — Voice-Only Chat Channels

| Field | Value |
|-------|-------|
| id | `SPEC-EFONE-001` |
| title | eFone — Voice-Only Chat Channels |
| summary | Efemera EGG configuration for voice-first communication in chat channels. Friends drop into voice calls without leaving Efemera. Same primitives serve consumer chat and team standups. Composed from capture-source (P-17), webrtc_engine, spatial_audio, stt-engine (P-19), text-pane, tts-engine (P-20). AI agents participate as voice members. |
| type | spec |
| product_area | Efemera |
| component | capture-source, webrtc_engine, spatial_audio, stt-engine, tts-engine, text-pane |
| status | backlog |
| owner | Q88N |
| related_items | SPEC-ECAMERA-001, SPEC-MEETING-INTEL-001, SPEC-EFEMERA-LAYOUT-001 |
| tags | efemera, voice, webrtc, eFone, communication |
| spec_document | SPEC-EFONE-VOICE-CHANNELS.docx |

---

## ITEM 02: eCamera — Video Layer

| Field | Value |
|-------|-------|
| id | `SPEC-ECAMERA-001` |
| title | eCamera — Video Layer |
| summary | Additive video layer for eFone sessions. Toggle camera on = eCamera. Uses capture-source (P-17, camera+mic), webrtc_engine, halo-light (P-21), stream-output (P-18), broadcast_compositor. Screen share native. Feeds Center Stage broadcast product. |
| type | spec |
| product_area | Efemera |
| component | capture-source, webrtc_engine, halo-light, stream-output, broadcast_compositor |
| status | backlog |
| owner | Q88N |
| related_items | SPEC-EFONE-001, SPEC-MEETING-INTEL-001 |
| tags | efemera, video, webrtc, eCamera, center-stage, broadcast |
| spec_document | SPEC-ECAMERA-VIDEO-LAYER.docx |

---

## ITEM 03: Meeting Intelligence

| Field | Value |
|-------|-------|
| id | `SPEC-MEETING-INTEL-001` |
| title | Meeting Intelligence — Transcription, Time Allocation, Segment Classification |
| summary | Every eFone/eCamera session generates live transcription with ra96it speaker attribution. Time allocation tracking computes per-speaker and per-segment durations. LLM classifies segments (WASTE/INFORM/DISCUSS/DECIDE/ACTION/CLOSE/TANGENT). Meeting score computed from allocation. Three-currency cost tracking for meetings. Transcripts feed Event Ledger and training pipeline. |
| type | spec |
| product_area | Efemera / SimDecisions |
| component | stt-engine, Event Ledger, rollup_engine, ZORTZI harness |
| status | backlog |
| owner | Q88N |
| related_items | SPEC-EFONE-001, SPEC-ECAMERA-001, SPEC-PM-ROLLUP-001, SPEC-IR-DENSITY-001, SPEC-PROJECT-RECOG-001 |
| tags | meeting, transcription, time-allocation, training-data, three-currencies, ABCDEFG |
| spec_document | SPEC-MEETING-INTELLIGENCE.docx |

---

## ITEM 04: Per-User Project Recognition Model

| Field | Value |
|-------|-------|
| id | `SPEC-PROJECT-RECOG-001` |
| title | Per-User Project Recognition Model (Private) |
| summary | Embedding-based classifier trained on user's own conversation patterns. Routes exchanges to correct project_tag without keyword matching. Private to user's ra96it account — NOT shared, NOT used to train platform models. Lives on user's hivenode. Bootstraps from manual seed tags, auto-classifies with confidence scoring. BYOLLM applies. |
| type | spec |
| product_area | 8OS / ZORTZI |
| component | embedding_protocol, ZORTZI harness, hivenode_api, Event Ledger |
| status | backlog |
| owner | Q88N |
| related_items | SPEC-TOPIC-TREE-001, SPEC-PM-ROLLUP-001, SPEC-MEETING-INTEL-001 |
| tags | embedding, classification, privacy, BYOLLM, project-attribution, hivenode |
| spec_document | SPEC-PROJECT-RECOGNITION-MODEL.docx |

---

## ITEM 05: Topic Tree Browser

| Field | Value |
|-------|-------|
| id | `SPEC-TOPIC-TREE-001` |
| title | Topic Tree Browser — Semantic Topic Navigation |
| summary | All work browsable in a topic tree rendered by tree-browser (P-07) with embedding-index adapter. Auto-generated from user's embedding space — semantic clusters form branches. Self-organizing, no manual folder creation. Brainstorms and unattributed work visible by subject. Clicking nodes filters dashboard metrics. |
| type | spec |
| product_area | 8OS / ShiftCenter |
| component | tree-browser (P-07), embedding_protocol, embedding-index adapter |
| status | backlog |
| owner | Q88N |
| related_items | SPEC-PROJECT-RECOG-001, BACKLOG-USER-UTILITY-DASHBOARD |
| tags | topic-tree, embedding, navigation, tree-browser, semantic-search |
| spec_document | SPEC-TOPIC-TREE-BROWSER.docx |

---

## ITEM 06: SC Keyboard — Custom On-Screen Keyboard Primitive

| Field | Value |
|-------|-------|
| id | `SPEC-SC-KEYBOARD-001` |
| title | SC Keyboard — Custom On-Screen Keyboard Primitive |
| summary | New pane primitive (P-33 candidate) rendering a custom on-screen keyboard. Numbers visible on QWERTY row permanently (no mode switching). Jumbo mode rotates keyboard to landscape independent of device orientation. Pinnable orientation separate from app orientation. Position-shift detection via DeviceMotion API. iPhone extended into safe area. Keyboard layouts on Global Commons — community contributed. |
| type | spec |
| product_area | ShiftCenter / Efemera |
| component | relay_bus, split_pane, Global Commons |
| status | backlog |
| owner | Q88N |
| related_items | SPEC-EFEMERA-LAYOUT-001 |
| tags | keyboard, mobile, primitive, accessibility, global-commons, #NOKINGS |
| spec_document | SPEC-SC-KEYBOARD-PRIMITIVE.docx |

---

## ITEM 07: Efemera Layout Personalization

| Field | Value |
|-------|-------|
| id | `SPEC-EFEMERA-LAYOUT-001` |
| title | Efemera Layout Personalization — User-Designed EGG Configs |
| summary | Full SC Stage layout engine (tiled/floating/hybrid) applied to Efemera chat. Users design their own layouts, save as named EGG configs, switch between favorites. Multiple saved layouts (Work mode, Social mode, Focus mode). Friends-online via tree-browser with presence adapter. EGG swap preserves state via applet_shell session store. |
| type | spec |
| product_area | Efemera |
| component | split_pane, applet_shell, egg_loader, tree-browser (presence adapter) |
| status | backlog |
| owner | Q88N |
| related_items | SPEC-EFONE-001, SPEC-SC-KEYBOARD-001 |
| tags | efemera, layout, EGG-config, favorites, personalization, split-pane |
| spec_document | SPEC-EFEMERA-LAYOUT-PERSONALIZATION.docx |

---

## ITEM 08: Localhost Deployment with ra96it JWT Recertification

| Field | Value |
|-------|-------|
| id | `SPEC-LOCALHOST-JWT-001` |
| title | Localhost Deployment with ra96it JWT Recertification |
| summary | Entire ShiftCenter stack runs locally via 'hive up'. Any localhost instance authenticates against ra96it before platform features activate. 15-minute JWT, refresh rotation, 60-second revocation. Two credentials: session JWT (interactive) + utility token in .hive/ (sync daemon). Tier enforcement at edge via JWT claims. 24-hour offline grace period for local-only features. Rate limiting per-JWT. |
| type | spec |
| product_area | Hivenode / ra96it |
| component | hivenode_api, ra96it auth, gate_enforcer, Event Ledger |
| status | backlog |
| owner | Q88N |
| related_items | TASK-021 (ra96it auth), SPEC-EFONE-001, SPEC-EFEMERA-LAYOUT-001 |
| tags | localhost, JWT, hivenode, #NOKINGS, self-hosted, authentication, offline |
| spec_document | SPEC-LOCALHOST-DEPLOYMENT-JWT.docx |

---

## ITEM 09: PM Dashboard Auto-Rollup

| Field | Value |
|-------|-------|
| id | `SPEC-PM-ROLLUP-001` |
| title | PM Dashboard Auto-Rollup — Automatic Sprint Visibility |
| summary | PM gets automatic rollup from Event Ledger via rollup_engine. Sprint scope by project_tag + date range. Activity breakdown by activity_type. Cost per sprint in CLOCK/COIN/CARBON/TOKENS. Model utilization breakdown. No manual time tracking — the ledger IS the status update. Maps to Schedule View composite in UNIFIED-COMPONENT-REGISTRY. |
| type | spec |
| product_area | SimDecisions / ShiftCenter |
| component | rollup_engine, Event Ledger, dashboard (P-15), chart (P-14), table (P-13) |
| status | backlog |
| owner | Q88N |
| related_items | TASK-010 (Cost Tracking), TASK-011 (Dashboard v1), SPEC-MEETING-INTEL-001, SPEC-PROJECT-RECOG-001 |
| tags | PM, sprint, rollup, three-currencies, dashboard, auto-attribution |
| spec_document | SPEC-PM-DASHBOARD-AUTO-ROLLUP.docx |

---

## ITEM 10: IR Density Per Exchange

| Field | Value |
|-------|-------|
| id | `SPEC-IR-DENSITY-001` |
| title | IR Density Per Exchange — Structured Intent Metric |
| summary | Novel metric: IR primitives generated per tokens consumed. Measures how efficiently conversation translates into actionable PHASE-IR structure. Four sub-metrics: IR Density, IR Yield (executable vs. descriptive), Exchange Cost (cost_triple), IR Cost Efficiency ($/executable node). Training signal for surrogate model pipeline. Low-density on expensive models = optimization target. |
| type | spec |
| product_area | SimDecisions / PHASE-IR |
| component | PHASE-IR compiler, ZORTZI harness, Event Ledger |
| status | backlog |
| owner | Q88N |
| related_items | SPEC-MEETING-INTEL-001, SPEC-PM-ROLLUP-001, SPEC-COST-RATE-001 |
| tags | IR-density, PHASE-IR, metric, surrogate, ABCDEFG, training-data |
| spec_document | SPEC-IR-DENSITY-METRIC.docx |

---

## ITEM 11: Cost Storage Format & Model Rate Lookup Table

| Field | Value |
|-------|-------|
| id | `SPEC-COST-RATE-001` |
| title | Cost Storage Format & Model Rate Lookup Table |
| summary | Token costs stored in scientific notation (e.g., 3.0e-4 per million tokens). Platform-level rate lookup table in PostgreSQL: model_name, cost_per_mtok_input, cost_per_mtok_output, rate_effective_date. Updated by platform ops. Staleness detection via effective_date. Cost computation: (tokens * rate / 1M) for each direction. Three currencies always tracked together. |
| type | spec |
| product_area | Platform Infrastructure |
| component | Event Ledger, PostgreSQL |
| status | backlog |
| owner | Q88N |
| related_items | TASK-010 (Cost Tracking), SPEC-PM-ROLLUP-001, SPEC-IR-DENSITY-001 |
| tags | cost-tracking, three-currencies, rate-table, scientific-notation, tokens |
| spec_document | SPEC-COST-STORAGE-RATE-LOOKUP.docx |

---

## ITEM 12: User-Shared Dashboard (Opt-In Cost Monitoring)

| Field | Value |
|-------|-------|
| id | `SPEC-SHARED-DASH-001` |
| title | User-Shared Dashboard — Opt-In Cost Monitoring |
| summary | Users opt to share dashboard data per project_tag via ra96it permission grants. Viewer (client PM) sees CLOCK/COIN/CARBON + tokens x model + rate lookup. gate_enforcer mediates access. TSaaS wraps permission check. Per-project sharing only — no bulk exposure. Revocable. Surfaces as dashboard composite with publish-toggles. |
| type | spec |
| product_area | Dashboard / ra96it |
| component | gate_enforcer, TSaaS, ra96it permissions, dashboard (P-15) |
| status | backlog |
| owner | Q88N |
| related_items | SPEC-PM-ROLLUP-001, SPEC-COST-RATE-001, SPEC-LOCALHOST-JWT-001 |
| tags | sharing, permissions, dashboard, client-billing, gate-enforcer, TSaaS |
| spec_document | SPEC-USER-SHARED-DASHBOARD.docx |

---

## Cross-Reference: All Spec Documents

| # | Spec ID | Document Filename | Product Area |
|---|---------|-------------------|--------------|
| 1 | SPEC-EFONE-001 | SPEC-EFONE-VOICE-CHANNELS.docx | Efemera |
| 2 | SPEC-ECAMERA-001 | SPEC-ECAMERA-VIDEO-LAYER.docx | Efemera |
| 3 | SPEC-MEETING-INTEL-001 | SPEC-MEETING-INTELLIGENCE.docx | Efemera / SimDecisions |
| 4 | SPEC-PROJECT-RECOG-001 | SPEC-PROJECT-RECOGNITION-MODEL.docx | 8OS / ZORTZI |
| 5 | SPEC-TOPIC-TREE-001 | SPEC-TOPIC-TREE-BROWSER.docx | 8OS / ShiftCenter |
| 6 | SPEC-SC-KEYBOARD-001 | SPEC-SC-KEYBOARD-PRIMITIVE.docx | ShiftCenter / Efemera |
| 7 | SPEC-EFEMERA-LAYOUT-001 | SPEC-EFEMERA-LAYOUT-PERSONALIZATION.docx | Efemera |
| 8 | SPEC-LOCALHOST-JWT-001 | SPEC-LOCALHOST-DEPLOYMENT-JWT.docx | Hivenode / ra96it |
| 9 | SPEC-PM-ROLLUP-001 | SPEC-PM-DASHBOARD-AUTO-ROLLUP.docx | SimDecisions / ShiftCenter |
| 10 | SPEC-IR-DENSITY-001 | SPEC-IR-DENSITY-METRIC.docx | SimDecisions / PHASE-IR |
| 11 | SPEC-COST-RATE-001 | SPEC-COST-STORAGE-RATE-LOOKUP.docx | Platform Infrastructure |
| 12 | SPEC-SHARED-DASH-001 | SPEC-USER-SHARED-DASHBOARD.docx | Dashboard / ra96it |

**Master backlog document:** BACKLOG-USER-UTILITY-DASHBOARD.docx (contains full narrative context for all 12 items)

---

*Q88N · 2026-03-12 · DEIA Solutions · CC BY 4.0*
