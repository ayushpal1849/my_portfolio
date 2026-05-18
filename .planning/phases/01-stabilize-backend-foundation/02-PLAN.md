---
plan_id: "02"
phase: "01"
phase_name: "Stabilize Backend Foundation"
title: "Harden Admin Boundaries and Route Compatibility"
wave: 2
depends_on:
  - "01"
requirements_addressed:
  - "ADMN-01"
  - "ADMN-02"
  - "ADMN-03"
  - "PLAT-03"
autonomous: true
files_modified:
  - "app.py"
  - "templates/base.html"
  - "templates/admin_login.html"
  - "templates/admin_dashboard.html"
  - "static/js/admin.js"
---

# Plan 02: Harden Admin Boundaries and Route Compatibility

## Objective

Make the admin utility consistently protected, keep its fetch-driven behavior aligned with JSON `401` responses, surface degraded-mode state to the owner only, and ensure shared template routing works correctly now that the public site is SPA-first.

## Must Haves

- Every admin write endpoint requires an authenticated admin session
- Admin login continues to work with initialized bcrypt password verification
- Unauthorized admin fetch requests return JSON `401` rather than redirect HTML
- Admin remains a separate server-rendered flow outside the public SPA
- Shared template navigation does not depend on removed legacy public route names

## Tasks

<task id="02-1" type="security">
  <goal>Audit all admin routes in `app.py` for consistent access control and response behavior.</goal>
  <details>
    Confirm write endpoints use `admin_session_required(json_response=True)`.
    Confirm page routes use redirect-based session enforcement where appropriate.
    Keep the auth model session-based; do not expand into roles or broader auth features.
  </details>
</task>

<task id="02-2" type="frontend-backend-contract">
  <goal>Align `static/js/admin.js` with JSON `401` behavior and degraded-mode handling.</goal>
  <details>
    Make unauthorized responses fail cleanly for fetch-based forms.
    Ensure the admin UI can surface useful feedback instead of failing silently.
    If DB degradation warnings are added, keep them visible only in the admin flow.
  </details>
</task>

<task id="02-3" type="templates">
  <goal>Make shared admin templates route-safe in the SPA-first architecture.</goal>
  <details>
    Confirm `templates/base.html`, `templates/admin_login.html`, and `templates/admin_dashboard.html` do not rely on removed public route function names.
    Preserve admin usability while treating the SPA shell plus API as the supported public path.
  </details>
</task>

<task id="02-4" type="operational-safety">
  <goal>Document or encode the accepted local-file behavior for resume and certificate uploads in the current architecture.</goal>
  <details>
    Keep local disk storage in place for Phase 1.
    Capture the AWS persistence risk clearly enough that deployment planning in Phase 4 has an explicit starting point.
  </details>
</task>

## Verification

- Unauthenticated POSTs to admin write routes yield JSON `401`
- Admin login still succeeds when valid credentials exist
- Admin dashboard still loads and form actions remain wired correctly
- Shared base/admin templates render without stale public route references
- Public SPA path and admin path coexist without cross-dependencies

## Exit Criteria

- Admin behavior is consistent, understandable, and safe for a personal maintenance utility
- Public/admin route boundaries are stable enough to proceed to frontend-focused phases
