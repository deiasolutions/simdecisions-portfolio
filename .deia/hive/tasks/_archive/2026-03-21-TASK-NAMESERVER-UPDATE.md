# TASK-NAMESERVER-UPDATE: Point All Hodeia Domains to Cloudflare

**Priority:** P0 — IMMEDIATE
**Assigned to:** Q88N (manual — no API available)
**Date:** 2026-03-21
**Model:** N/A — human task

---

## Status

All Cloudflare zones created. All A records set (76.76.21.21 → Vercel). All domains added to Vercel project. All EGG mappings configured in eggResolver.ts.

**The only remaining step is updating nameservers at the registrar.**

## Already Done (hodeia.guru)

hodeia.guru is LIVE — resolving to Vercel, HTTP 200, DNS propagated.

## Google Domains Dashboard (2 domains)

| Domain | New NS 1 | New NS 2 |
|--------|----------|----------|
| hodeia.me | kallie.ns.cloudflare.com | noel.ns.cloudflare.com |
| hodeia.de | kallie.ns.cloudflare.com | noel.ns.cloudflare.com |

## Squarespace Dashboard (11 domains)

| Domain | New NS 1 | New NS 2 | Current NS |
|--------|----------|----------|------------|
| hodeia.one | kallie.ns.cloudflare.com | noel.ns.cloudflare.com | (none) |
| hodeia.ai | kallie.ns.cloudflare.com | noel.ns.cloudflare.com | (none) |
| hodeia.dev | chip.ns.cloudflare.com | veda.ns.cloudflare.com | (none) |
| hodeia.app | chip.ns.cloudflare.com | veda.ns.cloudflare.com | (none) |
| hodeia.cloud | chip.ns.cloudflare.com | veda.ns.cloudflare.com | dns1-5.name-services.com |
| hodeia.run | chip.ns.cloudflare.com | veda.ns.cloudflare.com | (none) |
| hodeia.org | chip.ns.cloudflare.com | veda.ns.cloudflare.com | brodie/kara (old CF zone) |
| hodeia.io | chip.ns.cloudflare.com | veda.ns.cloudflare.com | (none) |
| hodeia.network | chip.ns.cloudflare.com | veda.ns.cloudflare.com | (none) |
| hodeia.studio | chip.ns.cloudflare.com | veda.ns.cloudflare.com | (none) |
| hodeia.win | kallie.ns.cloudflare.com | noel.ns.cloudflare.com | (none) |

## Verification

After updating, run:
```bash
nslookup hodeia.one 8.8.8.8
# Should return 76.76.21.21 (or Cloudflare proxy IP)
```

Or check Cloudflare dashboard — zone status should change from "Pending" to "Active".

## Recommended Order

1. hodeia.me (Google Domains) — auth gateway, critical path
2. hodeia.one (Squarespace) — flagship
3. hodeia.ai (Squarespace) — investor surface
4. hodeia.de (Google Domains) — your ops console
5. Rest in any order

---

*hodeia gara*
