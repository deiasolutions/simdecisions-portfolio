/**
 * terminalResponseRouter
 *
 * * terminalResponseRouter.ts — GENERIC INFRASTRUCTURE. DO NOT ADD APP-SPECIFIC SLOTS.
 *
 * Parses the terminal's structured response envelope and dispatches
 * each slot to the appropriate bus target.
 *
 * Ported from simdecisions-2/src/services/terminal/terminalResponseRouter.ts
 *
 * ── SDK RULES ──────────────────────────────────────────────────────────────
 * This router is shared by ALL terminal instances across ALL eggs.
 * It knows about transport (bus routing) — NOT about specific apps.
 *
 * Built-in slots (to_text, to_explorer, to_ir, to_simulator) are platform
 * primitives. They exist because SC core provides those pane types.
 *
 * For egg-specific communication (turtle commands, chart data, game events,
 * etc.) use the GENERIC to_bus slot:
 *
 *   "to_bus": [{ "type": "MY_CUSTOM_EVENT", "target": "*", "data": {...} }]
 *
 * The egg's .egg.md prompt block teaches the terminal what bus messages to emit.
 * The receiving app subscribes to those message types via usePaneContext.
 * The router just delivers — it never interprets to_bus message contents.
 *
 * If you're tempted to add to_turtle, to_chart, to_game, etc. — STOP.
 * Use to_bus. The egg owns the protocol, not the router.
 *
 * Envelope format: src/services/terminal/prompts/envelope.md
 *
 * Dependencies:
 * - import type { MessageBus } from '../../infrastructure/relay_bus/messageBus';
 * - import type {
 *
 * Components/Functions:
 * - FALLBACK_ENVELOPE: TypeScript function/component
 * - ERROR_ENVELOPE: TypeScript function/component
 * - stripCodeFences: TypeScript function/component
 * - trimmed: TypeScript function/component
 * - fenced: TypeScript function/component
 * - extractJson: TypeScript function/component
 * - fenceMatch: TypeScript function/component
 * - inner: TypeScript function/component
 * - start: TypeScript function/component
 * - ch: TypeScript function/component
 * - parseEnvelope: TypeScript function/component
 * - cleaned: TypeScript function/component
 * - jsonStr: TypeScript function/component
 * - parsed: TypeScript function/component
 * - routeEnvelope: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
