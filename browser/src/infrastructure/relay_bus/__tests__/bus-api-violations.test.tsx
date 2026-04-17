/**
 * bus-api-violations.test
 *
 * * bus-api-violations.test.tsx
 * Tests to verify correct MessageBus API usage patterns
 *
 * This test suite ensures that:
 * - bus.emit() is NOT used (should use bus.send())
 * - bus.on() is NOT used (should use bus.subscribe())
 * - bus.off() is NOT used (unsubscribe function pattern)
 * - Correct send() and subscribe() patterns work as expected
 *
 * Dependencies:
 * - import { describe, it, expect, vi, beforeEach } from 'vitest'
 * - import { MessageBus } from '../messageBus'
 * - import type { MessageEnvelope } from '../types/messages'
 *
 * Components/Functions:
 * - pattern: TypeScript function/component
 * - handler: TypeScript function/component
 * - nonce: TypeScript function/component
 * - envelope: TypeScript function/component
 * - handler1: TypeScript function/component
 * - handler2: TypeScript function/component
 * - handler3: TypeScript function/component
 * - that: TypeScript function/component
 * - handler: TypeScript function/component
 * - unsubscribe: TypeScript function/component
 * - handler1: TypeScript function/component
 * - handler2: TypeScript function/component
 * - unsub1: TypeScript function/component
 * - unsub2: TypeScript function/component
 * - handler1: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
