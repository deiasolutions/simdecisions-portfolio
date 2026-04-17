/**
 * Modes.test
 *
 * * Modes.test.tsx
 *
 * Tests for the FlowMode type system, mode-specific type definitions,
 * and the playback/simulation/tabletop hook contracts.
 *
 * Strategy: @testing-library/react is not installed, so component rendering
 * is not used. We test:
 *   1. FlowMode string literal union — all 5 values are valid
 *   2. SimulationState, PlaybackState, CompareState — structural completeness
 *   3. PHASE_IR_PRIMITIVES — all 11 primitives present
 *   4. PLAYBACK_SPEEDS — Fibonacci scale, length, content
 *   5. DEFAULT_SIM_CONFIG — default values
 *   6. PlaybackControls props interface — via typed mock callbacks
 *   7. SimulationConfig interface — field presence and types
 *   8. useTabletop types — ChatMessage, DecisionOption, TabletopPhase, TabletopSession
 *   9. Mode switching — callback invocation contracts
 *  10. useSimulation event handler logic (via direct handleEvent-equivalent tests)
 *  11. usePlayback step/speed/reset pure logic
 *  12. TabletopChat session/message state contracts
 *
 * Dependencies:
 * - import { describe, it, expect, vi, beforeEach } from "vitest";
 * - import type {
 * - import { PHASE_IR_PRIMITIVES } from "../types";
 * - import {
 * - import type {
 * - import {
 * - import type {
 * - import type {
 *
 * Components/Functions:
 * - ALL_MODES: TypeScript function/component
 * - mode: TypeScript function/component
 * - mode: TypeScript function/component
 * - mode: TypeScript function/component
 * - mode: TypeScript function/component
 * - mode: TypeScript function/component
 * - unique: TypeScript function/component
 * - onModeChange: TypeScript function/component
 * - modes: TypeScript function/component
 * - mode: TypeScript function/component
 * - setMode: TypeScript function/component
 * - setMode: TypeScript function/component
 * - setMode: TypeScript function/component
 * - setMode: TypeScript function/component
 * - state: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
