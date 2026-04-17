/**
 * terminal-canvas-e2e.test
 *
 * * terminal-canvas-e2e.test.tsx
 *
 * End-to-end integration tests for the terminal → LLM → canvas chatbot flow.
 * Tests the complete pipeline: user types NL in terminal → backend converts to PHASE-IR
 * → canvas receives and renders nodes via bus events.
 *
 * Dependencies: TASK-165 (backend /api/phase/nl-to-ir) + TASK-166 (frontend routing)
 *
 * Dependencies:
 * - import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
 * - import { renderHook, act, waitFor } from '@testing-library/react';
 * - import { useTerminal } from '../useTerminal';
 * - import type { MessageBus as MessageBusType, BusMessage } from '../../../infrastructure/relay_bus';
 * - import { createMessageBus, createMockFlowResponse } from './terminal-canvas-e2e.helpers';
 *
 * Components/Functions:
 * - mockResponse: TypeScript function/component
 * - initialLength: TypeScript function/component
 * - sendCalls: TypeScript function/component
 * - irDepositCall: TypeScript function/component
 * - msg: TypeScript function/component
 * - msg: TypeScript function/component
 * - lastEntry: TypeScript function/component
 * - complexFlow: TypeScript function/component
 * - initialLength: TypeScript function/component
 * - sendCalls: TypeScript function/component
 * - irDepositCall: TypeScript function/component
 * - msg: TypeScript function/component
 * - msg: TypeScript function/component
 * - lastEntry: TypeScript function/component
 * - invalidFlow: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
