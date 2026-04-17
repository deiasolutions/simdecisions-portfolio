/**
 * useCheckpoints
 *
 * * useCheckpoints - React hook for checkpoint operations
 *
 * Based on ADR-019 Decision 10: Checkpoint system for flow designer.
 * Manages checkpoint creation, retrieval, listing, and restoration.
 *
 * WB-B01: Refactored to use auth headers from the adapter layer and
 * to validate we're inside the ApiClientProvider tree.  The checkpoint
 * endpoints (/api/checkpoints/*) are not part of the core PhaseAPIClient
 * interface — they will be added in a future sprint.  For now, fetch()
 * calls include proper auth headers via getAuthHeaders() (the same
 * source the CloudAPIClient uses internally).
 *
 * Dependencies:
 * - import { useState, useCallback, useRef, useEffect } from 'react';
 * - import { getAuthHeaders } from "../../../lib/auth";
 * - import { useApiClient } from "../../../adapters";
 *
 * Components/Functions:
 * - checkpointFetch: TypeScript function/component
 * - useCheckpoints: TypeScript function/component
 * - autoSaveTimerRef: TypeScript function/component
 * - createCheckpoint: TypeScript function/component
 * - response: TypeScript function/component
 * - checkpoint: TypeScript function/component
 * - errorMsg: TypeScript function/component
 * - getCheckpoint: TypeScript function/component
 * - response: TypeScript function/component
 * - snapshot: TypeScript function/component
 * - errorMsg: TypeScript function/component
 * - listCheckpoints: TypeScript function/component
 * - response: TypeScript function/component
 * - checkpoints: TypeScript function/component
 * - errorMsg: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
