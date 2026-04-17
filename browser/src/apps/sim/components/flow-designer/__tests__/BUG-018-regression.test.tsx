/**
 * BUG-018-regression.test
 *
 * * BUG-018-regression.test.tsx
 * Regression test for BUG-018: Canvas IR generation shows error, response appears in Code egg instead
 *
 * This test verifies that terminal IR deposits are correctly received by the canvas pane,
 * not mistakenly routed to other panes (like code eggs).
 *
 * Root cause: terminal:ir-deposit bus routing was not wired to canvas
 * Fix: TASK-CANVAS-001 added irConverter.ts + bus subscription in FlowDesigner.tsx
 *
 * Dependencies:
 * - import { describe, it, expect, vi, beforeEach } from 'vitest';
 * - import { render, waitFor } from '@testing-library/react';
 * - import '@testing-library/jest-dom';
 * - import FlowDesigner from '../FlowDesigner';
 * - import type { MessageBus } from '../../../../../infrastructure/relay_bus/messageBus';
 * - import type { MessageEnvelope } from '../../../../../infrastructure/relay_bus/types/messages';
 *
 * Components/Functions:
 * - actual: TypeScript function/component
 * - mockBus: TypeScript function/component
 * - calls: TypeScript function/component
 * - subscriptionHandler: TypeScript function/component
 * - testMsg: TypeScript function/component
 * - calls: TypeScript function/component
 * - handler: TypeScript function/component
 * - wrongTargetMsg: TypeScript function/component
 * - calls: TypeScript function/component
 * - handler: TypeScript function/component
 * - validIR: TypeScript function/component
 * - calls: TypeScript function/component
 * - handler: TypeScript function/component
 * - emptyIR: TypeScript function/component
 * - malformedIR: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
