/**
 * useSimulation
 *
 * * useSimulation — Hook that connects to the SimDecisions DES backend via WebSocket,
 * manages simulation lifecycle (start/pause/resume/stop/reset), and streams events
 * to update flow graph state in real time.
 *
 * ADR-019: Visual Flow Designer — Simulate Mode
 * TASK-175: Wire to backend DES engine with fallback to LocalDESEngine
 *
 * Dependencies:
 * - import { useState, useRef, useCallback, useEffect } from "react";
 * - import { WS_URL } from "../../../lib/config";
 * - import { getToken } from "../../../lib/auth";
 * - import type { Node, Edge } from "@xyflow/react";
 * - import type {
 * - import { LocalDESEngine } from "./LocalDESEngine";
 * - import { desClient } from "../../../services/desClient";
 * - import type { PhaseFlow } from "../file-ops/serialization";
 *
 * Components/Functions:
 * - DEFAULT_SIM_CONFIG: TypeScript function/component
 * - INITIAL_STATS: TypeScript function/component
 * - reactFlowToPhaseFlow: TypeScript function/component
 * - now: TypeScript function/component
 * - MAX_EVENT_LOG: TypeScript function/component
 * - useSimulation: TypeScript function/component
 * - wsRef: TypeScript function/component
 * - localEngineRef: TypeScript function/component
 * - handleEvent: TypeScript function/component
 * - newLog: TypeScript function/component
 * - next: TypeScript function/component
 * - next: TypeScript function/component
 * - next: TypeScript function/component
 * - connectWs: TypeScript function/component
 * - token: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
