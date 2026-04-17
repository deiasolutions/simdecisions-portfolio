/**
 * useCollaboration
 *
 * * useCollaboration — WebSocket hook for live design-flight synchronisation.
 *
 * ADR-019 Decision 9: Lock-based collaboration.
 *
 * Manages:
 * - Design flight start/end (lock acquisition)
 * - Live cursor broadcasting and receiving
 * - Node-level comment sync
 * - Flow state change propagation to viewers
 * - Connection lifecycle with reconnect
 *
 * Dependencies:
 * - import { useState, useCallback, useEffect, useRef } from "react";
 * - import { getToken, getUser } from "../../../lib/auth";
 * - import { WS_URL } from "../../../lib/config";
 *
 * Components/Functions:
 * - CURSOR_COLORS: TypeScript function/component
 * - assignColor: TypeScript function/component
 * - useCollaboration: TypeScript function/component
 * - wsRef: TypeScript function/component
 * - reconnectTimerRef: TypeScript function/component
 * - cursorThrottleRef: TypeScript function/component
 * - intentionalCloseRef: TypeScript function/component
 * - retryCountRef: TypeScript function/component
 * - viewerColorMapRef: TypeScript function/component
 * - user: TypeScript function/component
 * - userId: TypeScript function/component
 * - displayName: TypeScript function/component
 * - interval: TypeScript function/component
 * - now: TypeScript function/component
 * - send: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
