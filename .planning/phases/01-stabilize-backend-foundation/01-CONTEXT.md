# Phase 1: Stabilize Backend Foundation - Context

**Gathered:** 2026-04-19
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase stabilizes the existing Flask backend so it can safely and consistently serve the public SPA and separate admin utility. It covers API delivery shape, fallback behavior, admin authentication consistency, local file-handling policy for the current architecture, and route compatibility decisions needed before deeper frontend redesign or AWS deployment work.

</domain>

<decisions>
## Implementation Decisions

### API contract
- **D-01:** Use one aggregated public endpoint at `/api/site-data` for this phase. Do not split into section-specific endpoints yet.
- **D-02:** Keep `meta.source` in the API response for debugging and operational visibility, but do not surface it in the public UI.
- **D-03:** Maintain a stable API shape at all times by returning consistent keys with empty arrays and empty strings for missing data instead of omitting keys.

### Fallback behavior
- **D-04:** If MySQL is unavailable, public visitors should be served JSON fallback content silently rather than seeing an outage banner or broken page.
- **D-05:** Admin views should surface a clear warning when the database is unavailable so the site owner can detect the degraded mode.
- **D-06:** Fallback mode must preserve the exact same API response structure as normal mode, with `meta.source` as the only behavioral signal.

### Admin security
- **D-07:** Keep session-based admin authentication, but harden it with basic security improvements rather than expanding scope into a full auth system.
- **D-08:** All fetch-driven admin write endpoints must return JSON `401` responses for unauthorized requests.
- **D-09:** Single active admin session behavior is sufficient for this phase; no session management UI or multi-device controls are required.

### File handling
- **D-10:** Keep local-disk storage for resume and certificate uploads in this phase, but isolate path usage clearly and document the AWS persistence risk.
- **D-11:** Resume replacement continues to overwrite a fixed `resume.pdf` file rather than versioning uploads.
- **D-12:** Certificate image handling remains local and public-preview capable, with preview URLs normalized through the API.

### Route compatibility
- **D-13:** Treat SPA shell plus API delivery as the supported public path immediately; do not keep legacy server-rendered public routes as active production paths.
- **D-14:** Old public templates may remain in the repository temporarily for reference, but no traffic should be routed through them.
- **D-15:** Admin remains on Flask templates, and shared layout dependencies must not rely on removed public route names.

### the agent's Discretion
- Exact JSON helper organization and normalization function layout inside the Flask app
- How admin warning messages are surfaced visually as long as they are clear to the owner
- Whether local file-path documentation lives in code comments, planning docs, or deployment notes, provided the operational risk is captured

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project scope and locked requirements
- `.planning/PROJECT.md` - Product direction, constraints, and locked project-level decisions
- `.planning/REQUIREMENTS.md` - Phase-mapped requirements including Phase 1 backend scope
- `.planning/ROADMAP.md` - Phase 1 goal, success criteria, and sequencing expectations
- `.planning/STATE.md` - Current project status and active phase

### Existing codebase map
- `.planning/codebase/STACK.md` - Runtime stack, dependencies, and configuration expectations
- `.planning/codebase/ARCHITECTURE.md` - Current Flask architecture and boundary issues already identified
- `.planning/codebase/STRUCTURE.md` - File layout and key entry points
- `.planning/codebase/CONVENTIONS.md` - Established coding patterns and current inconsistencies
- `.planning/codebase/CONCERNS.md` - Known backend risks relevant to this phase

### Backend implementation files
- `app.py` - Public routing, API delivery, admin endpoints, fallback logic, and file handling
- `config.py` - Runtime configuration and local MySQL fallback behavior
- `models.py` - ORM models and bcrypt integration
- `templates/base.html` - Shared admin/public layout dependencies that must remain route-safe
- `templates/admin_login.html` - Admin login form behavior
- `templates/admin_dashboard.html` - Admin utility interface and fetch-driven forms
- `static/js/admin.js` - Admin-side fetch behavior and unauthorized-response expectations

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `app.py:get_public_content()` - Existing normalized content aggregation path for SPA consumption
- `app.py:admin_session_required()` - Reusable authorization decorator for admin routes
- `app.py:normalize_*` helpers - Existing normalization layer for DB and JSON fallback content
- `config.py:build_local_mysql_uri()` - Current MySQL fallback builder for local development
- `models.py:User.set_password()` and `models.py:User.check_password()` - Existing password hashing and verification behavior

### Established Patterns
- Public content is loaded DB-first and falls back to `data/resume_data.json` on `OperationalError`
- Admin write flows use fetch-based JSON or multipart requests from `static/js/admin.js`
- Resume and certificate assets are stored under `static/`, making them directly web-servable in the current design
- The public SPA is already wired to a single-shell route model and `/api/site-data`

### Integration Points
- Phase 1 changes concentrate in `app.py`, `config.py`, shared admin templates, and possibly `static/js/admin.js`
- Any admin warning behavior should integrate cleanly with Flask flash messaging or existing dashboard rendering
- Route compatibility work must preserve admin login/dashboard flows while retiring public dependence on old template routes

</code_context>

<specifics>
## Specific Ideas

- The public portfolio should behave as if the backend is stable even when it is running on JSON fallback.
- The admin side is allowed to expose operational state because it is a private maintenance utility.
- The backend should stay simple in Phase 1: stabilize what exists, do not expand into broader infrastructure or auth scope.

</specifics>

<deferred>
## Deferred Ideas

- Section-specific public API endpoints - revisit only if the SPA grows enough to justify endpoint splitting
- Richer admin security features such as rate limiting, remember-me, or multi-session controls - future security hardening phase
- Upload abstraction or S3-backed media handling - deployment/infrastructure phase
- Full removal of old public templates - cleanup phase after the SPA path is fully stable

</deferred>

---

*Phase: 01-stabilize-backend-foundation*
*Context gathered: 2026-04-19*
