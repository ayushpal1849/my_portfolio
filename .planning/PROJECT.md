# Ayush Pal Portfolio SPA

## What This Is

This is a personal portfolio platform for Ayush Pal that showcases AI engineering, Python development, projects, certifications, skills, and experience through a polished single-shell SPA. It is built for recruiters, hiring managers, and professional contacts who need a fast, modern, no-refresh browsing experience, while still giving the owner a separate admin utility to update portfolio data.

## Core Value

A visitor should be able to understand Ayush Pal's profile, credibility, and key work quickly through a fast, polished SPA experience that feels modern and professional.

## Requirements

### Validated

- Existing Flask backend serves portfolio content and admin flows - existing codebase
- Existing SQLAlchemy models and Alembic migrations support core content entities - existing codebase
- Existing JSON fallback allows the public portfolio to render without a working database - existing codebase
- Existing admin utility can add projects, experience, certifications, and resume assets - existing codebase
- Backend content delivery is stabilized for SPA consumption with a single aggregated API and JSON fallback - validated in Phase 1
- Admin write endpoints are consistently protected and admin runtime behavior is stabilized - validated in Phase 1
- Local development resolves to MySQL correctly without requiring `DATABASE_URL` - validated in Phase 1
- Public portfolio now runs as a single-shell SPA with no-refresh navigation and direct-link support - validated in Phase 2
- Public experience is redesigned into the locked dark editorial + futuristic premium direction and verified across desktop/mobile flows - validated in Phase 3

### Active

- [ ] Prepare the application for AWS free-tier deployment with Flask app hosting and MySQL database hosting

### Out of Scope

- Native mobile app - web-first portfolio is the priority
- Public user accounts or multi-user admin roles - admin is a personal maintenance utility only
- Real-time chat, messaging, or social features - not part of the portfolio core value
- Rebuilding resume parsing into a robust ingestion product - current parser is one-time bootstrap only
- README refresh during current execution - defer documentation rewrite until implementation stabilizes

## Context

This is a brownfield Flask portfolio project with existing server-rendered templates, a small admin interface, SQLAlchemy models, Alembic migrations, static asset handling, and fallback JSON content in `data/resume_data.json`. The product direction is now clear:

- Public experience becomes a single-shell SPA
- Admin remains a separate server-rendered utility
- Content remains dual-mode: database plus JSON fallback
- Local development should support MySQL
- Deployment target is AWS free tier for both app and database

The current codebase already contains the structural pieces needed to evolve into this target, and the first two phases have now stabilized the backend plus shipped the SPA navigation shell:

- `bcrypt` is initialized and admin write routes are protected
- local MySQL fallback is configured consistently
- public navigation is SPA-driven with direct-link support
- certifications browsing and admin visual alignment are improved

## Constraints

- **Tech stack**: Preserve Flask backend and MySQL local development - current codebase already uses this foundation
- **Architecture**: Public site must become a JavaScript-driven SPA with History API navigation - explicitly requested
- **Admin boundary**: Admin must remain separate from the public SPA - explicitly requested
- **Content model**: Database and JSON fallback both remain supported - explicitly requested
- **Design direction**: Visual redesign should feel creative and modern while keeping the particle background - explicitly requested
- **Deployment**: Must be feasible on AWS free tier - hosting and infrastructure decisions should stay lightweight

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Keep Flask as the backend | Existing project already uses Flask, models, admin routes, and migrations | Good |
| Use single-shell SPA for public site | Matches requirement for no-refresh navigation and URL changes | Good |
| Keep admin server-rendered and separate | Admin is a personal maintenance utility, not part of public UX | Good |
| Preserve dual-mode content (DB + JSON fallback) | Existing data strategy is intentional and useful for resilience | Good |
| Standardize local development on MySQL | Matches current user preference and deployment direction | Good |
| Defer README updates until after implementation | Documentation should reflect final stabilized behavior, not transitional state | Good |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `$gsd-transition`):
1. Requirements invalidated? -> Move to Out of Scope with reason
2. Requirements validated? -> Move to Validated with phase reference
3. New requirements emerged? -> Add to Active
4. Decisions to log? -> Add to Key Decisions
5. "What This Is" still accurate? -> Update if drifted

**After each milestone** (via `$gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check -> still the right priority?
3. Audit Out of Scope -> reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-13 after Phase 3 verification*
