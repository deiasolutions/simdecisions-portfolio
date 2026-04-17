/**
 * AnimationOverlay
 *
 * * AnimationOverlay — Renders all simulation animations on top of the flow canvas
 *
 * Displays:
 * - NodePulse: Glow effect on active nodes
 * - TokenAnimation: Moving dots along edges with token flow
 * - ResourceBar: Utilization bars on resource nodes
 * - SimClock: Prominent clock in top-right corner
 * - QueueBadge: Queue count badges on nodes with queued tokens
 * - CheckpointFlash: Diamond flash animation when checkpoints are reached
 *
 * All animations respect viewport transformations (pan/zoom) and reset when simulation stops.
 *
 * Dependencies:
 * - import React, { useMemo } from 'react';
 * - import { NodePulse } from './NodePulse';
 * - import { TokenAnimation } from './TokenAnimation';
 * - import { ResourceBar } from './ResourceBar';
 * - import { SimClock } from './SimClock';
 * - import { QueueBadge } from './QueueBadge';
 * - import { CheckpointFlash } from './CheckpointFlash';
 * - import type { SimulationState, SimulationStats } from '../simulation/useSimulation';
 * - import type { Viewport, Node, Edge } from '@xyflow/react';
 *
 * Components/Functions:
 * - AnimationOverlay: TypeScript function/component
 * - nodePositions: TypeScript function/component
 * - map: TypeScript function/component
 * - nodeQueueLengths: TypeScript function/component
 * - queueMap: TypeScript function/component
 * - event: TypeScript function/component
 * - recentCheckpoints: TypeScript function/component
 * - recent: TypeScript function/component
 * - toScreenPosition: TypeScript function/component
 * - state: TypeScript function/component
 * - isActive: TypeScript function/component
 * - screenPos: TypeScript function/component
 * - tokenCount: TypeScript function/component
 * - sourcePos: TypeScript function/component
 * - targetPos: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
