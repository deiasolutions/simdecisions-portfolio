/**
 * ApiClientContext
 *
 * * ApiClientContext — Shared React context for the PhaseAPIClient.
 *
 * WB-B01: Wire adapters to flow-designer.
 *
 * Provides a single PhaseAPIClient instance to the entire component tree,
 * eliminating the need for each hook/component to instantiate its own client.
 *
 * Usage:
 *   // In a top-level component:
 *   <ApiClientProvider>
 *     <FlowDesigner />
 *   </ApiClientProvider>
 *
 *   // In any hook or component that needs API access:
 *   const client = useApiClient();
 *   await client.saveFlow(flow);
 *
 * Dependencies:
 * - import { createContext, useContext, useMemo, type ReactNode } from "react";
 * - import { createClient, type PhaseAPIClient } from "./api-client";
 *
 * Components/Functions:
 * - client: TypeScript function/component
 * - ApiClientContext: TypeScript function/component
 * - ApiClientProvider: TypeScript function/component
 * - resolvedClient: TypeScript function/component
 * - useApiClient: TypeScript function/component
 * - client: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
