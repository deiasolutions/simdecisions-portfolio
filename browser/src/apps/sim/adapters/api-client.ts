/**
 * api-client
 *
 * * api-client.ts — PhaseAPIClient interface + CloudAPIClient implementation
 *
 * WB-003: API adapter interface definition.
 *
 * Defines the PhaseAPIClient interface that abstracts all backend communication
 * for the flow designer. CloudAPIClient is the canonical HTTP implementation
 * using the standard fetch() API.
 *
 * LocalAPIClient (browser-local / offline) is deferred to WB-A02.
 *
 * Dependencies:
 * - import type { PhaseFlow, PhaseNode, PhaseEdge } from "../components/flow-designer/file-ops/serialization";
 * - import type { BaseFlowEvent } from "../components/flow-designer/telemetry/eventTypes";
 * - import { getAuthHeaders } from "../lib/auth";
 *
 * Components/Functions:
 * - APIError: TypeScript class
 * - CloudAPIClient: TypeScript class
 * - LocalAPIClient: TypeScript class
 * - url: TypeScript function/component
 * - init: TypeScript function/component
 * - response: TypeScript function/component
 * - json: TypeScript function/component
 * - result: TypeScript function/component
 * - url: TypeScript function/component
 * - response: TypeScript function/component
 * - json: TypeScript function/component
 * - response: TypeScript function/component
 * - url: TypeScript function/component
 * - init: TypeScript function/component
 * - response: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
