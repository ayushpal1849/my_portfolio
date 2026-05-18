# Requirements: Ayush Pal Portfolio SPA

**Defined:** 2026-04-19
**Core Value:** A visitor should be able to understand Ayush Pal's profile, credibility, and key work quickly through a fast, polished SPA experience that feels modern and professional.

## v1 Requirements

### Public SPA

- [ ] **SPA-01**: Visitor can navigate between Home, About, Education, Skills, Experience, Projects, Certifications, and Contact without a full page refresh
- [ ] **SPA-02**: Browser URL updates correctly for each public view using History API navigation
- [ ] **SPA-03**: Direct navigation to a public URL loads the SPA shell and renders the correct view
- [ ] **SPA-04**: Public SPA consumes portfolio content from API-style JSON endpoints instead of server-rendered page-specific templates

### Design and UX

- [x] **UX-01**: Public site uses a redesigned creative visual system that feels distinct from the current template-based layout
- [x] **UX-02**: Particle background is preserved and integrated into the redesigned experience
- [x] **UX-03**: Public site remains readable and responsive on desktop and mobile layouts
- [x] **UX-04**: Key visitor actions include resume download and contact navigation from the SPA

### Content Delivery

- [ ] **CONT-01**: Public API returns normalized portfolio content for summary, contact details, education, skills, experience, projects, certifications, and achievements
- [ ] **CONT-02**: Public site continues to support dual-mode content delivery using database-first reads with JSON fallback
- [ ] **CONT-03**: Certification entries can include image preview data when uploaded certificate files exist

### Admin and Security

- [ ] **ADMN-01**: All admin write endpoints require authenticated admin session access
- [ ] **ADMN-02**: Admin login continues to work with bcrypt-backed password verification
- [ ] **ADMN-03**: Admin dashboard remains a separate server-rendered maintenance page outside the public SPA

### Configuration and Platform

- [ ] **PLAT-01**: Local development configuration supports MySQL when `DATABASE_URL` is not provided
- [ ] **PLAT-02**: Project structure supports AWS free-tier deployment planning for Flask app hosting and MySQL-compatible database hosting
- [ ] **PLAT-03**: Public and admin flows remain compatible with the current Flask application structure and migration setup

## v2 Requirements

### Admin Enhancements

- **ADMN-04**: Admin can edit and delete existing portfolio entities from the dashboard
- **ADMN-05**: Admin can preview public content changes before publishing

### Content and Analytics

- **CONT-04**: Public site includes richer project storytelling, featured work ordering, and curated spotlight sections
- **CONT-05**: Public site captures lightweight visitor analytics or engagement signals

### Deployment and Ops

- **PLAT-04**: Infrastructure is automated through repeatable AWS deployment scripts or IaC
- **PLAT-05**: Uploaded files move from local disk to managed object storage

## Out of Scope

| Feature | Reason |
|---------|--------|
| Native mobile application | Portfolio value is best delivered on the web first |
| Public user authentication | Site is a personal portfolio, not a user platform |
| Real-time chat or messaging | Adds complexity without serving the core portfolio goal |
| Multi-admin roles and permission system | Admin is a private maintenance utility for one owner |
| Converting resume parser into robust ETL workflow | Parser is only needed as one-time bootstrap support |
| README rewrite during current build cycle | Documentation should be updated after the implementation settles |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| SPA-01 | Phase 2 | Complete |
| SPA-02 | Phase 2 | Complete |
| SPA-03 | Phase 2 | Complete |
| SPA-04 | Phase 1 | Complete |
| UX-01 | Phase 3 | Complete |
| UX-02 | Phase 3 | Complete |
| UX-03 | Phase 3 | Complete |
| UX-04 | Phase 3 | Complete |
| CONT-01 | Phase 1 | Complete |
| CONT-02 | Phase 1 | Complete |
| CONT-03 | Phase 1 | Complete |
| ADMN-01 | Phase 1 | Complete |
| ADMN-02 | Phase 1 | Complete |
| ADMN-03 | Phase 1 | Complete |
| PLAT-01 | Phase 1 | Complete |
| PLAT-02 | Phase 4 | Pending |
| PLAT-03 | Phase 1 | Complete |

**Coverage:**
- v1 requirements: 17 total
- Mapped to phases: 17
- Unmapped: 0

---
*Requirements defined: 2026-04-19*
*Last updated: 2026-05-13 after Phase 3 verification*
