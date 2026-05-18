# Phase 1: Stabilize Backend Foundation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves the alternatives considered.

**Date:** 2026-04-19
**Phase:** 01-stabilize-backend-foundation
**Areas discussed:** API contract, Fallback behavior, Admin security, File handling, Route compatibility

---

## API contract

| Option | Description | Selected |
|--------|-------------|----------|
| Single aggregated endpoint only | Use `/api/site-data` as the only public content endpoint in this phase | ✓ |
| Aggregated endpoint plus section endpoints later | Keep one now and add more only if needed later | |
| Separate section endpoints immediately | Split public data by section from the start | |

**User's choice:** Accepted recommendation to keep one aggregated endpoint for now.
**Notes:** Also locked `meta.source` as API-visible but UI-hidden, and stable keys with empty arrays/strings for missing data.

---

## Fallback behavior

| Option | Description | Selected |
|--------|-------------|----------|
| Silent public fallback | Visitors keep seeing portfolio content through JSON fallback | ✓ |
| Public banner in fallback mode | Public UI indicates degraded mode | |
| Public outage on DB failure | Do not render if DB is unavailable | |

**User's choice:** Accepted recommended fallback strategy.
**Notes:** Admin should receive a clear warning if DB is down. API shape remains identical in fallback mode, with only `meta.source` signaling the mode.

---

## Admin security

| Option | Description | Selected |
|--------|-------------|----------|
| Session auth only | Keep current simple session model | |
| Session auth plus basic hardening | Keep simple auth model but strengthen it for correctness and safety | ✓ |
| Full auth overhaul | Expand scope into broader auth/security features | |

**User's choice:** Accepted recommendation for basic hardening only.
**Notes:** Unauthorized admin API writes should return JSON `401`, and single-session behavior is sufficient for this phase.

---

## File handling

| Option | Description | Selected |
|--------|-------------|----------|
| Local disk for now | Keep current upload model and document AWS risk | ✓ |
| Abstract storage now | Introduce indirection layer before it is needed | |
| Move toward S3 now | Pull storage migration into Phase 1 | |

**User's choice:** Accepted recommendation to keep local disk in Phase 1.
**Notes:** Resume overwrites fixed `resume.pdf`, and certificate preview URLs remain normalized through the API.

---

## Route compatibility

| Option | Description | Selected |
|--------|-------------|----------|
| SPA shell is the supported public path immediately | Public traffic should use the SPA route model now | ✓ |
| Run old and new public paths in parallel | Keep both active temporarily | |
| Keep old templates as hidden fallback | Preserve runtime fallback to old templates | |

**User's choice:** Accepted recommendation to support SPA shell plus API immediately.
**Notes:** Old public templates may remain in the repo temporarily, but admin templates must not rely on removed public route names.

---

## the agent's Discretion

- Internal Flask helper organization
- Admin warning presentation details
- Documentation location for local upload persistence risk

## Deferred Ideas

- Section-specific APIs
- Stronger admin session controls and broader auth hardening
- S3 or abstracted upload storage
- Cleanup removal of old public templates after SPA path stability
