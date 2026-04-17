/**
 * useLLMRouter
 *
 * * useLLMRouter.ts — LLM routing hook with streaming support
 *
 * Routes messages to appropriate LLM endpoints:
 * - command → local command-interpreter (fast)
 * - question → Claude API (slow, streaming)
 * - code → code-specialized model (streaming)
 *
 * Features:
 * - Server-Sent Events (SSE) for streaming responses
 * - Exponential backoff retry logic
 * - Error handling with retry UI
 * - Message history management
 *
 * Dependencies:
 * - import { useState, useCallback, useRef } from 'react'
 * - import type { Message, AssistantTextMessage, LoadingMessage, ErrorMessage } from './types'
 * - import { discoverHivenodeUrl } from '../../services/hivenodeDiscovery'
 *
 * Components/Functions:
 * - DEFAULT_OPTIONS: TypeScript function/component
 * - useLLMRouter: TypeScript function/component
 * - opts: TypeScript function/component
 * - pendingRequestRef: TypeScript function/component
 * - eventSourceRef: TypeScript function/component
 * - loadingMessageIdRef: TypeScript function/component
 * - generateId: TypeScript function/component
 * - addUserMessage: TypeScript function/component
 * - userMsg: TypeScript function/component
 * - addLoadingMessage: TypeScript function/component
 * - loadingMsg: TypeScript function/component
 * - replaceLoadingWithResponse: TypeScript function/component
 * - loadingId: TypeScript function/component
 * - assistantMsg: TypeScript function/component
 * - updateStreamingMessage: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
