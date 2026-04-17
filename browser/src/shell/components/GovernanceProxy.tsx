/**
 * GovernanceProxy
 *
 * * GovernanceProxy.tsx — Re-export from infrastructure/relay_bus
 *
 * GovernanceProxy wraps every applet and enforces capability ceilings.
 * The implementation lives in infrastructure/relay_bus where it belongs (core infrastructure).
 * This file exists for convenience so shell components can import from a consistent location.
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
 * - (see source)
 *
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
