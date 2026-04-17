/**
 * ir-deposit-integration.test
 *
 * * ir-deposit-integration.test.tsx — Integration test for terminal → IR → canvas pipeline
 *
 * Verifies end-to-end flow:
 * 1. Terminal with routeTarget: 'ir'
 * 2. Mock LLM response with IR JSON
 * 3. terminalResponseRouter sends terminal:ir-deposit event
 * 4. Canvas receives event and adds nodes
 *
 * Dependencies:
 * - import React from 'react';
 * - import { describe, it, expect, vi, beforeEach } from 'vitest';
 * - import { render, waitFor } from '@testing-library/react';
 * - import '@testing-library/jest-dom';
 * - import FlowDesigner from '../FlowDesigner';
 * - import { MessageBus } from '../../../../../infrastructure/relay_bus/messageBus';
 * - import { routeEnvelope } from '../../../../../services/terminal/terminalResponseRouter';
 *
 * Components/Functions:
 * - actual: TypeScript function/component
 * - paneRegistry: TypeScript function/component
 * - llmResponse: TypeScript function/component
 * - routeResult: TypeScript function/component
 * - irData: TypeScript function/component
 * - paneRegistry: TypeScript function/component
 * - llmResponse: TypeScript function/component
 * - routeResult: TypeScript function/component
 * - irData: TypeScript function/component
 * - paneRegistry: TypeScript function/component
 * - llmResponse: TypeScript function/component
 * - routeResult: TypeScript function/component
 * - paneRegistry: TypeScript function/component
 * - llmResponse: TypeScript function/component
 * - routeResult: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
