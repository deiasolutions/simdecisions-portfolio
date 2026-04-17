/**
 * hivenodeDiscovery
 *
 * * hivenodeDiscovery.ts — Auto-discover which port hivenode is running on.
 *
 * Probes /hivenode/health (not generic /health) to avoid false positives
 * from other services. Checks the default port range (8420-8429, matching
 * the hivenode port-fallback logic) plus common manual override ports.
 *
 * If VITE_HIVENODE_URL env var is set, uses that directly (no probing).
 *
 * Dependencies:
 * - (see source)
 *
 * Components/Functions:
 * - BASE_PORT: TypeScript function/component
 * - PORT_RANGE: TypeScript function/component
 * - EXTRA_PORTS: TypeScript function/component
 * - buildCandidatePorts: TypeScript function/component
 * - ports: TypeScript function/component
 * - p: TypeScript function/component
 * - CANDIDATE_PORTS: TypeScript function/component
 * - DEFAULT_URL: TypeScript function/component
 * - PROBE_TIMEOUT_MS: TypeScript function/component
 * - HEALTH_PATH: TypeScript function/component
 * - discoverHivenodeUrl: TypeScript function/component
 * - envUrl: TypeScript function/component
 * - hostname: TypeScript function/component
 * - result: TypeScript function/component
 * - resetDiscovery: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
