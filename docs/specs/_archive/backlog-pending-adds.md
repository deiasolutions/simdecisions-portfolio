# Backlog — Pending Adds

> These 5 items were requested by Dave to be added to the backlog on 2026-03-13.
> Add was halted before execution. These need to be added manually or via CLI.

| # | ID (suggested) | Title | Priority | Type | Category | Source Spec | T-Shirt | Notes |
|---|----------------|-------|----------|------|----------|-------------|---------|-------|
| 1 | — | ADR-GC-APPLET-001: Draw.io / maxGraph as GC third-party applet | P2 | work | frontend | `docs/specs/ADR-GC-APPLET-001-drawio-third-party-applet.md` | XL | First GC third-party applet. Wraps maxGraph (Apache-2.0) in AppletShell. Reference implementation for Monaco, Quill, vis.js, p5.js pattern. Trust Tier 1. |
| 2 | — | SPEC-CANVAS-SURFACE-001: Infinite canvas surface primitive | P2 | work | frontend | `docs/specs/SPEC-CANVAS-SURFACE-001-infinite-canvas.md` | XL | CSS transform-based infinite 2D world. Two z-layers (World + Glass). Pan/zoom/minimap. Backdrop applet support. DOM-based, not `<canvas>`. |
| 3 | — | SPEC-SCAFFOLD-001: Scaffold and float layout service | P2 | work | frontend | `docs/specs/SPEC-SCAFFOLD-001-scaffold-float-layout.md` | L | Named scaffold regions, floater panes, nav_joystick. Breakpoint-driven responsive morphing (fixed/shrink/hide/float/drawer/tab/sheet). Architect-defined, not auto. |
| 4 | — | SPEC-SIM-CHAT-001: Simulation chat channel | P2 | work | frontend | `docs/specs/SPEC-SIM-CHAT-001-simulation-chat-channel.md` | M | Unified message stream: human + IR node execution + system + bot. MCP-exposed. Y.js synced. Mobile bridge via STT/TTS. Meeting summary on session end. |
| 5 | — | SPEC-IR-PRESENCE-TRIGGER-001: Presence events as IR triggers | P2 | work | backend | `docs/specs/SPEC-IR-PRESENCE-TRIGGER-001-ir-presence-triggers.md` | S | Adds `trigger: presence` to PHASE-IR v2.0. Host drop, quorum, mobile bridge as IR conditions. CEL expressions. Reuses bus_event evaluation pipeline. |

## Dependencies Between These Items

- SPEC-SCAFFOLD-001 depends on SPEC-CANVAS-SURFACE-001
- SPEC-SIM-CHAT-001 depends on SPEC-IR-PRESENCE-TRIGGER-001 (for presence-driven bot messages)
- ADR-GC-APPLET-001 depends on SPEC-CANVAS-SURFACE-001 (draw.io as backdrop applet)
- SPEC-IR-PRESENCE-TRIGGER-001 is standalone (only depends on existing relay_bus + SPEC-PRESENCE-001)

## Suggested Build Order

1. SPEC-IR-PRESENCE-TRIGGER-001 (S — smallest, no new primitives)
2. SPEC-SIM-CHAT-001 (M — new pane adapter, bus wiring)
3. SPEC-CANVAS-SURFACE-001 (XL — new platform primitive)
4. SPEC-SCAFFOLD-001 (L — depends on canvas surface)
5. ADR-GC-APPLET-001 (XL — depends on canvas surface + AppletShell contract)
