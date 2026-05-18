---
plan_id: "02"
phase: "02"
phase_name: "Ship SPA Navigation Shell"
title: "Refine Certifications View and Align Admin Pages with SPA Theme"
wave: 2
depends_on:
  - "01"
requirements_addressed:
  - "SPA-01"
autonomous: true
files_modified:
  - "templates/public_shell.html"
  - "static/js/spa.js"
  - "static/css/spa.css"
  - "templates/base.html"
  - "templates/admin_login.html"
  - "templates/admin_dashboard.html"
  - "static/css/admin_dashboard.css"
---

# Plan 02: Refine Certifications View and Align Admin Pages with SPA Theme

## Objective

Improve the most visible route-specific usability gap in the SPA by turning certifications into a browse-and-preview layout, then restyle the separate admin pages so they visually belong to the same portfolio system without changing their server-rendered operational behavior.

## Must Haves

- Certifications route uses a scrollable list with a sticky/fixed preview panel on desktop
- Certificate preview sizing respects the actual image shape rather than stretching a large generic container
- Certifications layout collapses to a normal stacked mobile flow
- Admin login and dashboard remain separate server-rendered pages
- Admin visual language matches the public site more closely through shared background, typography, and panel treatment
- Admin forms, warnings, and JS behaviors remain intact after the visual update

## Tasks

<task id="02-1" type="route-layout">
  <goal>Rework the certifications route in `static/js/spa.js` and `static/css/spa.css` into a scan-and-preview desktop layout.</goal>
  <details>
    Keep the current `activeCertIndex` interaction model.
    Make the certificate list scrollable when content exceeds the viewport.
    Keep the preview visible on desktop with sticky/fixed behavior inside the route layout.
  </details>
</task>

<task id="02-2" type="responsive-design">
  <goal>Make certification preview sizing image-led instead of panel-led.</goal>
  <details>
    Use containment sizing so preview height and width align naturally with the selected certificate image.
    On narrow viewports, collapse the layout to a stacked flow with no sticky side preview.
  </details>
</task>

<task id="02-3" type="admin-theming">
  <goal>Restyle `templates/admin_login.html`, `templates/admin_dashboard.html`, and shared admin layout surfaces to match the SPA design language.</goal>
  <details>
    Reuse the public background direction and typography where practical.
    Keep admin warnings, actions, and form clarity operationally strong.
    Do not turn admin into part of the client-side SPA.
  </details>
</task>

<task id="02-4" type="compatibility">
  <goal>Ensure restyling does not break existing admin behavior or phase-1 safeguards.</goal>
  <details>
    Preserve CSRF fields, flash rendering, existing form IDs, and JS hooks used by `static/js/admin.js`.
    Keep database warning and storage-note surfaces readable after the restyle.
  </details>
</task>

## Verification

- On desktop, certifications shows a scrollable list with a persistent visible preview pane
- Preview image sizing feels aligned to the certificate rather than to an oversized empty frame
- On mobile, the certifications route becomes a normal stacked layout
- `/admin/login` and `/admin/dashboard` look visually related to the public site
- Admin login, warnings, and form submissions still work after the restyle

## Exit Criteria

- The SPA shell includes the key route-level layout behavior the user explicitly requested
- Admin pages feel intentionally integrated with the rest of the product without changing their architectural boundary
