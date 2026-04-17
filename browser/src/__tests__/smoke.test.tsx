/**
 * smoke.test
 *
 * * Browser smoke tests — integration tests for major flows
 *
 * These tests verify real component wiring and integration paths.
 * We mock the hivenode API (fetch calls) but let everything else run real:
 * - Relay bus
 * - State management
 * - Adapters
 * - Markdown serialization/parsing
 *
 * Dependencies:
 * - import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
 * - import { render, screen, waitFor } from '@testing-library/react';
 * - import userEvent from '@testing-library/user-event';
 * - import type { ConversationWithMessages } from '../services/terminal/types';
 * - import { serializeConversation, parseConversation } from '../services/terminal/chatMarkdown';
 * - import { parseInput } from '../services/terminal/shellParser';
 * - import { MessageBus } from '../infrastructure/relay_bus/messageBus';
 *
 * Components/Functions:
 * - mockFetch: TypeScript function/component
 * - conversation: TypeScript function/component
 * - markdown: TypeScript function/component
 * - conversation: TypeScript function/component
 * - parsed: TypeScript function/component
 * - writeCalls: TypeScript function/component
 * - body: TypeScript function/component
 * - conversation: TypeScript function/component
 * - markdown: TypeScript function/component
 * - homeUri: TypeScript function/component
 * - cloudUri: TypeScript function/component
 * - body: TypeScript function/component
 * - parsed: TypeScript function/component
 * - response: TypeScript function/component
 * - result: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
