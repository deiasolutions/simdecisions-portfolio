/**
 * conversationNavigator.test
 *
 * * conversationNavigator.test.ts — Tests for conversation navigator pane
 *
 * Coverage:
 * - Selection handler (3 tests)
 * - Tree refresh (3 tests)
 * - Volume badges (4 tests)
 * - Conversation actions (2 tests)
 *
 * Total: 12 tests
 *
 * Dependencies:
 * - import { describe, it, expect, vi, beforeEach } from 'vitest';
 * - import { render, screen, waitFor } from '@testing-library/react';
 * - import userEvent from '@testing-library/user-event';
 * - import React from 'react';
 * - import { ChatNavigatorPane } from '../ChatNavigatorPane';
 * - import type { Conversation, ConversationWithMessages } from '../../../services/terminal/types';
 * - import type { MessageEnvelope } from '../../../infrastructure/relay_bus/types/messages';
 * - import { listConversations, getConversation, createConversation, deleteConversation } from '../../../services/terminal/chatApi';
 * - import { getVolumeStatus } from '../../../services/volumes/volumeStatus';
 *
 * Components/Functions:
 * - mockListConversations: TypeScript function/component
 * - mockGetConversation: TypeScript function/component
 * - mockCreateConversation: TypeScript function/component
 * - mockDeleteConversation: TypeScript function/component
 * - mockGetVolumeStatus: TypeScript function/component
 * - makeConversation: TypeScript function/component
 * - now: TypeScript function/component
 * - conv: TypeScript function/component
 * - mockSend: TypeScript function/component
 * - mockBus: TypeScript function/component
 * - convNode: TypeScript function/component
 * - conv: TypeScript function/component
 * - mockSend: TypeScript function/component
 * - mockBus: TypeScript function/component
 * - callArg: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
