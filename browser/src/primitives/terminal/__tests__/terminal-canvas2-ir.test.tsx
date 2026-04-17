/**
 * terminal-canvas2-ir.test
 *
 * * terminal-canvas2-ir.test.tsx
 *
 * Integration test for canvas2 EGG IR routing pipeline.
 * Tests the complete flow: LLM returns envelope with to_ir mutations →
 * routeEnvelope extracts and sends bus message → FlowDesigner receives and applies mutations.
 *
 * Task: TASK-CANVAS2-IR-ROUTING
 *
 * Dependencies:
 * - import { describe, it, expect, vi, beforeEach } from 'vitest';
 * - import type { MessageBus } from '../../../infrastructure/relay_bus/messageBus';
 * - import type { MessageEnvelope } from '../../../infrastructure/relay_bus/types/messages';
 * - import { routeEnvelope } from '../../../services/terminal/terminalResponseRouter';
 * - import { processMutations, isMutationArray } from '../../../apps/sim/components/flow-designer/irMutationProcessor';
 * - import type { Node, Edge } from '@xyflow/react';
 *
 * Components/Functions:
 * - llmResponse: TypeScript function/component
 * - paneRegistry: TypeScript function/component
 * - result: TypeScript function/component
 * - irMessage: TypeScript function/component
 * - mutations: TypeScript function/component
 * - currentNodes: TypeScript function/component
 * - currentEdges: TypeScript function/component
 * - result: TypeScript function/component
 * - node1: TypeScript function/component
 * - node2: TypeScript function/component
 * - llmResponse: TypeScript function/component
 * - paneRegistry: TypeScript function/component
 * - routeResult: TypeScript function/component
 * - irMessage: TypeScript function/component
 * - mutations: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
