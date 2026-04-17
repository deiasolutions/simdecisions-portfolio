/**
 * messageBus.crossWindow.test
 *
 * * messageBus.crossWindow.test.ts — Cross-window message isolation tests
 *
 * This test suite verifies that MessageBus instances in different tabs/windows
 * cannot leak messages to each other. Each Shell creates its own MessageBus
 * instance (line 31 in Shell.tsx), so messages in one bus should never appear
 * in another bus.
 *
 * IMPORTANT: This tests in-memory isolation ONLY. There is no BroadcastChannel
 * or localStorage sync mechanism, so message isolation is guaranteed by virtue
 * of separate MessageBus instances with independent _subs maps.
 *
 * Dependencies:
 * - import { describe, it, expect, vi, beforeEach } from 'vitest'
 * - import { MessageBus } from '../messageBus'
 * - import type { MessageEnvelope } from '../types/messages'
 *
 * Components/Functions:
 * - handler1: TypeScript function/component
 * - handler2: TypeScript function/component
 * - handler1: TypeScript function/component
 * - handler2: TypeScript function/component
 * - handler1: TypeScript function/component
 * - handler2: TypeScript function/component
 * - collisionId: TypeScript function/component
 * - handler1a: TypeScript function/component
 * - handler1b: TypeScript function/component
 * - handler2a: TypeScript function/component
 * - handler2b: TypeScript function/component
 * - handler1: TypeScript function/component
 * - handler2: TypeScript function/component
 * - bus1Handlers: TypeScript function/component
 * - bus2Handlers: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
