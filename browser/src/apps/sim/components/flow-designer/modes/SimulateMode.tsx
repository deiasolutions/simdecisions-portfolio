/**
 * SimulateMode
 *
 * * SimulateMode — Top-level container for the Simulate mode.
 * Renders a read-only ReactFlow canvas with real-time DES animation overlays,
 * plus the SimulationPanel side bar for controls and stats.
 *
 * ADR-019: Visual Flow Designer — Simulate Mode
 *
 * Checkpoint wiring (BEE-10):
 *  - useCheckpoints is hooked in to store simulation snapshots when a
 *    checkpoint node is reached during the DES run.
 *  - CheckpointFlash plays a diamond animation over the canvas on each hit.
 *  - CheckpointTimeline is rendered below the canvas (collapsible).
 *  - CheckpointManager is rendered in a collapsible right-panel drawer so
 *    the user can restore previous snapshots for Compare mode.
 *
 * Dependencies:
 * - import React, { useState, useCallback, useMemo, useEffect, useRef } from "react";
 * - import {
 * - import { colors, fonts } from "../../../lib/theme";
 * - import PhaseNode from "../nodes/PhaseNode";
 * - import CheckpointNode from "../nodes/CheckpointNode";
 * - import SimulationPanel from "../simulation/SimulationPanel";
 * - import SimulationConfigDialog from "../simulation/SimulationConfig";
 * - import { useSimulation } from "../simulation/useSimulation";
 * - import { simResultsStore } from "../simulation/SimulationResultsStore";
 * - import { CheckpointFlash } from "../animation/CheckpointFlash";
 *
 * Components/Functions:
 * - nodeTypes: TypeScript function/component
 * - getNodeStyle: TypeScript function/component
 * - deriveFlowId: TypeScript function/component
 * - sorted: TypeScript function/component
 * - SimulateMode: TypeScript function/component
 * - simulation: TypeScript function/component
 * - flowId: TypeScript function/component
 * - checkpoints: TypeScript function/component
 * - prevPassedCountRef: TypeScript function/component
 * - prev: TypeScript function/component
 * - curr: TypeScript function/component
 * - irSnapshot: TypeScript function/component
 * - checkpointLabel: TypeScript function/component
 * - handleCheckpointSelect: TypeScript function/component
 * - handleRestoreCheckpoint: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
