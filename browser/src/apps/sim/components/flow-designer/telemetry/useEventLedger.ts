/**
 * useEventLedger
 *
 * * useEventLedger — React hook that logs flow designer events to the backend.
 *
 * ADR-019 Event Ledger section + ADR-001 Event Ledger Foundation.
 *
 * Provides a type-safe `emit()` function that sends events to the
 * /api/flow-events endpoint. Events are buffered in a small queue and
 * flushed periodically (or immediately for critical events) to avoid
 * flooding the backend on rapid user interactions.
 *
 * WB-B01: Refactored to route through PhaseAPIClient.logEvent() via
 * the shared ApiClientContext.  The hook retains its own batching logic —
 * individual events are still queued locally and flushed in a batch.
 * Each event in the batch is sent through client.logEvent() which the
 * CloudAPIClient/LocalAPIClient implementations POST as a single-item
 * batch.  This preserves the original batching behavior while routing
 * all network I/O through the adapter layer.
 *
 * Dependencies:
 * - import { useCallback, useRef, useEffect } from "react";
 * - import { getUser } from "../../../lib/auth";
 * - import { useApiClient } from "../../../adapters";
 * - import type {
 *
 * Components/Functions:
 * - that: TypeScript function/component
 * - CRITICAL_EVENTS: TypeScript function/component
 * - useEventLedger: TypeScript function/component
 * - client: TypeScript function/component
 * - queueRef: TypeScript function/component
 * - flushTimerRef: TypeScript function/component
 * - inflightRef: TypeScript function/component
 * - optionsRef: TypeScript function/component
 * - clientRef: TypeScript function/component
 * - doFlush: TypeScript function/component
 * - batch: TypeScript function/component
 * - event: TypeScript function/component
 * - emit: TypeScript function/component
 * - user: TypeScript function/component
 * - event: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
