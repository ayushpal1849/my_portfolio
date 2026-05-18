# Phase 2: Ship SPA Navigation Shell - Context

**Gathered:** 2026-04-20
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase turns the already-functional public SPA shell into the intended navigation experience for the portfolio: one persistent shell, route-based URL updates, no full page refresh, subtle page transitions, and responsive navigation behavior. It also includes two targeted UI refinements the user explicitly requested during Phase 2 discussion: a better certifications viewing layout and admin pages that visually align with the public portfolio style while remaining separate server-rendered pages.

</domain>

<decisions>
## Implementation Decisions

### SPA navigation behavior
- **D-01:** Public navigation should update the route immediately and swap views without a full page refresh.
- **D-02:** Use lightweight loading feedback only when bootstrap or route rendering is meaningfully delayed; do not add heavy loading choreography.
- **D-03:** Use route-only URL paths such as `/`, `/about`, `/projects`, and `/contact`. Do not add deeper URL state in this phase.
- **D-04:** Fetch the full portfolio payload once on app startup and render route views from in-memory state rather than refetching on every route change.
- **D-05:** Keep browser back/forward support and direct URL entry working through the same SPA shell.

### Motion and shell structure
- **D-06:** Use subtle fade/slide transitions between views. Avoid stronger animations that compete with the particle background.
- **D-07:** Keep one persistent fixed top navigation bar across public routes.
- **D-08:** Add a responsive mobile navigation pattern rather than relying on the current wrapped desktop links.

### Certifications view
- **D-09:** On desktop, the certifications route should use a two-panel layout with a scrollable certificate list and a fixed/sticky preview area.
- **D-10:** The certificate preview panel should size itself around the certificate image using containment rules rather than stretching to an arbitrary large box.
- **D-11:** On mobile, the certifications layout should collapse to a normal stacked flow instead of trying to preserve a fixed side preview.

### Admin visual alignment
- **D-12:** `/admin/login` and `/admin/dashboard` remain separate server-rendered pages; they do not join the public SPA shell.
- **D-13:** Admin pages should visually align with the public site through shared background direction, typography, color system, and panel treatment.
- **D-14:** Admin usability takes priority over decorative parity; forms and warnings must remain clear and operational.

### the agent's Discretion
- Exact implementation of loading-state timing thresholds
- Whether shell transitions are handled via CSS classes, keyed containers, or small JS hooks
- How the mobile navigation toggle is structured as long as it stays accessible and route-safe
- Whether admin theme alignment is done through shared CSS tokens, a new admin stylesheet, or selective template-level reuse

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project scope and roadmap
- `.planning/PROJECT.md` - Current product direction and validated Phase 1 state
- `.planning/REQUIREMENTS.md` - Phase-mapped requirement list, especially `SPA-01`, `SPA-02`, and `SPA-03`
- `.planning/ROADMAP.md` - Phase 2 goal, success criteria, and sequencing
- `.planning/STATE.md` - Current active phase and execution handoff

### Prior phase outputs
- `.planning/phases/01-stabilize-backend-foundation/01-CONTEXT.md` - Locked backend/content decisions that Phase 2 must preserve
- `.planning/phases/01-stabilize-backend-foundation/01-SUMMARY.md` - Public API and config work already completed
- `.planning/phases/01-stabilize-backend-foundation/02-SUMMARY.md` - Admin boundary decisions and current server-rendered admin constraints

### Current implementation files
- `app.py` - Public shell routes and SPA shell serving behavior
- `templates/public_shell.html` - Current public shell markup and navigation structure
- `static/js/spa.js` - Current route handling, rendering, and certification interactions
- `static/css/spa.css` - Current public SPA styling, transitions, and certifications layout
- `templates/base.html` - Shared admin base and global page structure
- `templates/admin_login.html` - Admin login markup that needs visual alignment
- `templates/admin_dashboard.html` - Admin dashboard structure that needs visual alignment
- `static/js/admin.js` - Admin interaction behavior that must remain functional after restyling

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `static/js/spa.js:navigateTo()` - Current History API path update and route rendering path
- `static/js/spa.js:renderRoute()` - Single render entry point for route changes
- `static/js/spa.js:fetchSiteData()` - Current one-time startup fetch
- `static/js/spa.js:renderCertifications()` - Existing certification interaction surface to refine
- `static/css/spa.css:@keyframes fade-slide` - Existing subtle transition baseline that can be retained or tuned

### Established Patterns
- Public shell already uses a fixed `#tsparticles` background plus glassmorphism panels
- The SPA already fetches all site data once on boot and renders from local state
- Public navigation is route-based today, but mobile behavior and route transition polish are still thin
- Admin pages still rely on Bootstrap-heavy server-rendered templates with a different visual language

### Integration Points
- Route behavior should stay compatible with Flask shell serving for direct URL access
- Admin restyling must not break CSRF inputs, flash messages, or existing form IDs used by `static/js/admin.js`
- Certifications layout needs to work with the existing `activeCertIndex` state model and uploaded image URLs from the API

</code_context>

<specifics>
## Specific Ideas

- The SPA should feel instant first and animated second.
- The certifications page should behave like a browsing workspace: scan list, keep preview visible.
- Admin pages should look like part of the same product family, not like a separate template dropped into the repo.

</specifics>

<deferred>
## Deferred Ideas

- Deep-linking to specific projects or certifications via route params or query state
- Refetch-on-route or stale-while-revalidate client data strategies
- Full public visual redesign across every route beyond what is required to support the shell and requested layout changes
- Moving admin into a separate design system or SPA architecture

</deferred>

---

*Phase: 02-ship-spa-navigation-shell*
*Context gathered: 2026-04-20*
