# Roadmap: Ayush Pal Portfolio SPA

**Created:** 2026-04-19
**Phases:** 4
**Mapped v1 requirements:** 17/17

## Overview

| # | Phase | Goal | Requirements |
|---|-------|------|--------------|
| 1 | Stabilize Backend Foundation | Normalize backend behavior for secure, API-driven SPA delivery | SPA-04, CONT-01, CONT-02, CONT-03, ADMN-01, ADMN-02, ADMN-03, PLAT-01, PLAT-03 |
| 2 | Ship SPA Navigation Shell | Replace multi-page public rendering with a single-shell SPA that updates URLs without refresh | SPA-01, SPA-02, SPA-03 |
| 3 | Redesign Public Experience | Deliver a creative, mobile-safe portfolio interface around the SPA shell | UX-01, UX-02, UX-03, UX-04 |
| 4 | Prepare AWS Deployment | Make the application operationally ready for AWS free-tier hosting and database deployment | PLAT-02 |

## Phase Details

### Phase 1: Stabilize Backend Foundation

**Goal:** Make the existing Flask backend safe, consistent, and suitable as the API/content source for the SPA.

**Requirements:** SPA-04, CONT-01, CONT-02, CONT-03, ADMN-01, ADMN-02, ADMN-03, PLAT-01, PLAT-03

**Success criteria:**
1. Public content is available through stable JSON API responses built from DB-first reads with JSON fallback.
2. All admin write routes reject unauthenticated access consistently.
3. `bcrypt` is initialized correctly and admin login remains functional.
4. Local config resolves to MySQL when `DATABASE_URL` is absent.
5. Public and admin route structure is coherent enough to support SPA rollout without breaking the admin utility.

**Execution notes:**
- This phase should land before any frontend redesign work.
- Regression checks should focus on login, admin actions, content loading, and route handling.

### Phase 2: Ship SPA Navigation Shell

**Goal:** Convert the public site from template-per-page rendering into a single-shell SPA with no-refresh navigation.

**Requirements:** SPA-01, SPA-02, SPA-03

**Success criteria:**
1. Public routes load one shell and render views client-side.
2. Clicking navigation updates the URL and swaps views without a full refresh.
3. Directly opening `/about`, `/projects`, or similar public URLs still renders the correct SPA view.
4. Client-side navigation is resilient to reloads and browser back/forward navigation.

**Execution notes:**
- Keep admin out of the SPA scope.
- Avoid introducing a second frontend framework unless the architecture clearly justifies it.

### Phase 3: Redesign Public Experience

**Goal:** Redesign the visitor-facing portfolio experience so it feels creative, modern, and intentional.

**Requirements:** UX-01, UX-02, UX-03, UX-04

**Success criteria:**
1. Public UI has a coherent visual direction that is meaningfully better than the current Bootstrap-template look.
2. Particle background remains integrated without harming readability or responsiveness.
3. Mobile and desktop layouts both feel complete, not merely functional.
4. Resume and contact actions are obvious and accessible from the redesigned SPA.

**Execution notes:**
- Treat this as product-facing design work, not just CSS cleanup.
- The final layout should support content hierarchy for recruiters scanning quickly.

### Phase 4: Prepare AWS Deployment

**Goal:** Make the app deployment-ready for AWS free-tier infrastructure decisions and rollout.

**Requirements:** PLAT-02

**Success criteria:**
1. Deployment topology is defined for Flask app hosting and MySQL-compatible database hosting on AWS free tier.
2. Environment variable strategy is explicit for secrets, DB connections, and runtime config.
3. File upload handling risks are documented with an agreed short-term and long-term plan.
4. The app can be deployed without architecture surprises introduced by the SPA conversion.

**Execution notes:**
- Decide whether uploads remain local short-term or move to S3-compatible storage later.
- Keep hosting approach lightweight enough for free-tier constraints.

## Execution Order

1. Finish backend stabilization and auth/config correctness.
2. Lock the public shell and History API behavior.
3. Redesign the public UX on top of the stable SPA architecture.
4. Finalize deployment preparation once the app behavior and structure are stable.

## Risks

- SPA conversion can create broken direct-link or back-button behavior if route handling is incomplete.
- Dual-mode content adds edge cases if API normalization differs between DB and JSON payloads.
- AWS free-tier constraints may clash with local-file uploads if persistence expectations are not explicit.
- Frontend redesign can drift into cosmetic work unless tied to visitor outcomes and scanning behavior.

---
*Roadmap created: 2026-04-19 after initialization*
