/**
 * GovernanceProxy
 *
 * * GovernanceProxy.tsx — Governance wrapper for applets
 * Ported from simdecisions-2/src/components/shell/GovernanceProxy.tsx
 *
 * GovernanceProxy wraps every applet and enforces capability ceilings.
 *
 * Intercepts:
 * 1. MessageBus.send() — blocks messages not in bus_emit list
 * 2. MessageBus.subscribe() — filters incoming messages not in bus_receive list
 * 3. Tool adapter calls — blocks tools not in tools list (future — stub for now)
 * 4. Autonomous action gates — enforces REQUIRE_HUMAN (Wave 4-3)
 *
 * The applet does not know it is wrapped.
 *
 * Dependencies:
 * - import React, { useMemo, useCallback, useState } from 'react'
 * - import { ShellCtx, useShell, MessageBus } from './messageBus'
 * - import type { ResolvedPermissions } from './types/permissions'
 * - import type { MessageEnvelope } from './types/messages'
 * - import { BrowserGateEnforcer } from '../gate_enforcer/enforcer'
 * - import type { AgentEthics, CheckResult } from '../gate_enforcer/types'
 * - import { Disposition } from '../gate_enforcer/types'
 * - import { GovernanceApprovalModal } from './GovernanceApprovalModal'
 *
 * Components/Functions:
 * - matchesPermissionPattern: TypeScript function/component
 * - prefix: TypeScript function/component
 * - isMessageAllowed: TypeScript function/component
 * - GovernanceProxy: TypeScript function/component
 * - shell: TypeScript function/component
 * - enforcer: TypeScript function/component
 * - handleApprove: TypeScript function/component
 * - handleReject: TypeScript function/component
 * - governedSend: TypeScript function/component
 * - messageType: TypeScript function/component
 * - platformInvariants: TypeScript function/component
 * - allowed: TypeScript function/component
 * - checkResult: TypeScript function/component
 * - governedSubscribe: TypeScript function/component
 * - wrappedHandler: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
