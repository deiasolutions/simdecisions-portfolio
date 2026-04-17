/**
 * useTerminal.chatPersist.test
 *
 * * Tests for useTerminal chat persistence integration
 * TDD: Tests written first
 *
 * Scenarios:
 * 1. First message: createConversation called, addMessage called for user + assistant
 * 2. Subsequent messages: only addMessage called (no duplicate createConversation)
 * 3. chatApi failure: error logged, terminal still functional
 * 4. Volume preference: reads from settings, defaults to 'both'
 * 5. No conversationId: creates conversation before calling addMessage
 *
 * Dependencies:
 * - import { describe, it, expect, vi, beforeEach } from 'vitest';
 * - import { renderHook, act, waitFor } from '@testing-library/react';
 * - import { useTerminal } from '../useTerminal';
 * - import * as chatApi from '../../../services/terminal/chatApi';
 * - import * as settingsStore from '../../../primitives/settings/settingsStore';
 *
 * Components/Functions:
 * - mockConv: TypeScript function/component
 * - mockConv: TypeScript function/component
 * - mockConv: TypeScript function/component
 * - mockConv: TypeScript function/component
 * - consoleSpy: TypeScript function/component
 * - mockConv: TypeScript function/component
 * - mockConv: TypeScript function/component
 * - mockLoadedConv: TypeScript function/component
 * - mockBus: TypeScript function/component
 * - mockLoadedConv: TypeScript function/component
 * - mockBus: TypeScript function/component
 * - mockLoadedConv: TypeScript function/component
 * - mockBus: TypeScript function/component
 * - consoleSpy: TypeScript function/component
 * - mockBus: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
