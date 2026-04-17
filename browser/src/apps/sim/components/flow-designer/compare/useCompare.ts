/**
 * useCompare
 *
 * * useCompare — React hook for diffing two PHASE-IR flow branches.
 *
 * ADR-019 Decision 6: Alterverse Comparison View.
 *
 * Accepts two branch IDs, fetches their snapshots from the API,
 * runs the diff algorithm, and exposes the result plus loading/error state.
 *
 * WB-B01: Refactored to route snapshot fetches through PhaseAPIClient
 * via the shared ApiClientContext.  The branch snapshot endpoint
 * (/flow-designer/branches/{id}/snapshot) is not part of the core
 * PhaseAPIClient interface (which covers /api/phase/* routes), so we
 * use the client's internal request pattern via a thin wrapper that
 * calls fetch with the same auth headers the client would use.
 *
 * NOTE: The compare endpoint lives outside the standard PhaseAPIClient
 * surface area.  Rather than polluting the adapter interface with a
 * one-off method, we continue to use fetch() but obtain auth headers
 * from getAuthHeaders() — the same source the CloudAPIClient uses.
 * When a dedicated compare method is added to PhaseAPIClient in a
 * future sprint, this hook will be updated to call it directly.
 * For now the key refactoring value is: useCompare no longer hard-codes
 * an API base URL — it reads it from the adapter context.
 *
 * Dependencies:
 * - import { useState, useCallback, useEffect, useRef } from "react";
 * - import {
 * - import { getAuthHeaders } from "../../../lib/auth";
 * - import { useApiClient } from "../../../adapters";
 *
 * Components/Functions:
 * - useCompare: TypeScript function/component
 * - abortRef: TypeScript function/component
 * - fetchSnapshot: TypeScript function/component
 * - response: TypeScript function/component
 * - raw: TypeScript function/component
 * - snapshot: TypeScript function/component
 * - compare: TypeScript function/component
 * - controller: TypeScript function/component
 * - diffResponse: TypeScript function/component
 * - result: TypeScript function/component
 * - ids: TypeScript function/component
 * - message: TypeScript function/component
 * - setFilter: TypeScript function/component
 * - reset: TypeScript function/component
 * - filteredNodeDiffs: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
