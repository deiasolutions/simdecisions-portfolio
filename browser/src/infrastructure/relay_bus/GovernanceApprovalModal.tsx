/**
 * GovernanceApprovalModal
 *
 * * GovernanceApprovalModal.tsx — Modal for governance approval decisions
 *
 * Shows when gate_enforcer returns ESCALATE, HOLD, or REQUIRE_HUMAN dispositions.
 * User can approve or reject the action (reject blocked for REQUIRE_HUMAN).
 *
 * Features:
 * - Portal-based rendering to .hhp-root
 * - Semi-transparent backdrop (non-dismissible for REQUIRE_HUMAN)
 * - Shows disposition type, reason, and matched rule
 * - Escape key and backdrop click handling
 * - CSS variables only (var(--sd-*))
 *
 * Dependencies:
 * - import { useEffect, useRef } from 'react'
 * - import { createPortal } from 'react-dom'
 * - import { Disposition } from '../gate_enforcer/types'
 * - import './GovernanceApprovalModal.css'
 *
 * Components/Functions:
 * - getDispositionLabel: TypeScript function/component
 * - GovernanceApprovalModal: TypeScript function/component
 * - backdropRef: TypeScript function/component
 * - isRequireHuman: TypeScript function/component
 * - handleEscape: TypeScript function/component
 * - handleBackdropClick: TypeScript function/component
 * - handleModalClick: TypeScript function/component
 * - modalContent: TypeScript function/component
 * - portalTarget: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
