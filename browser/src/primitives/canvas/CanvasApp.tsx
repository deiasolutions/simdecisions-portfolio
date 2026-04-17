/**
 * CanvasApp
 *
 * * CanvasApp.tsx — ReactFlow canvas for PHASE-IR graphs.
 * Ported from platform/simdecisions-2/Canvas.tsx.
 * BroadcastChannel → relay_bus, Zustand stores → bus events.
 *
 * 22 node types: 9 core (start, end, task, decision, checkpoint, split, join, queue, group),
 * 6 BPMN (bpmn-start, bpmn-end, bpmn-task, bpmn-gateway, bpmn-subprocess, bpmn-event),
 * 7 annotation (annotation-ellipse, annotation-image, annotation-line, annotation-rect,
 *   annotation-text, sticky-note, callout).
 * Smart edge routing with back-edge support. Lasso freeform selection.
 * Bus integration: receives IR deposits by data shape, publishes canvas:node-selected / canvas:edge-selected.
 *
 * Dependencies:
 * - import React, { useCallback, useEffect, useMemo, useState, useRef } from 'react';
 * - import {
 * - import '@xyflow/react/dist/style.css';
 * - import './canvas.css';
 * - import dagre from 'dagre';
 * - import type { MessageBus } from '../../infrastructure/relay_bus/messageBus';
 * - import type { MessageEnvelope } from '../../infrastructure/relay_bus/types/messages';
 * - import type { Flow as IRFlow, Node as IRNode, Edge as IREdge } from '../../types/ir';
 * - import type { NodeData, CanvasNodeType, Badge, OperatorData, TimingData } from './canvasTypes';
 * - import { applySmartHandles } from './edgeHandles';
 *
 * Components/Functions:
 * - nodeTypes: TypeScript function/component
 * - edgeTypes: TypeScript function/component
 * - getNodeColor: TypeScript function/component
 * - IR_TYPE_MAP: TypeScript function/component
 * - mapIRType: TypeScript function/component
 * - RESIZABLE_TYPES: TypeScript function/component
 * - layoutWithDagre: TypeScript function/component
 * - g: TypeScript function/component
 * - pos: TypeScript function/component
 * - CanvasInner: TypeScript function/component
 * - reactFlow: TypeScript function/component
 * - highlightTimersRef: TypeScript function/component
 * - initialViewportRef: TypeScript function/component
 * - unsub: TypeScript function/component
 * - nodeType: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
