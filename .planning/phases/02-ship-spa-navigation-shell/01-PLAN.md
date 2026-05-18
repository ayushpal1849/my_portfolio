---
plan_id: "01"
phase: "02"
phase_name: "Ship SPA Navigation Shell"
title: "Lock Route Navigation, Mobile Shell, and Client-Side View Swaps"
wave: 1
depends_on: []
requirements_addressed:
  - "SPA-01"
  - "SPA-02"
  - "SPA-03"
autonomous: true
files_modified:
  - "app.py"
  - "templates/public_shell.html"
  - "static/js/spa.js"
  - "static/css/spa.css"
---

# Plan 01: Lock Route Navigation, Mobile Shell, and Client-Side View Swaps

## Objective

Make the existing public SPA shell behave like the intended production navigation experience: persistent shell, route-based URL changes, no-refresh view swaps, direct-link resilience, subtle transitions, and a responsive mobile nav that still feels like the same product.

## Must Haves

- Public pages continue to render inside one persistent shell
- Clicking nav links updates the browser URL without a full page refresh
- Browser back/forward and direct URL entry continue to render the correct route
- The SPA fetches site data once on startup and reuses it for route changes
- A responsive mobile menu replaces the current wrapped desktop-nav behavior
- Loading feedback remains lightweight and does not dominate the interaction

## Tasks

<task id="01-1" type="shell-navigation">
  <goal>Refine the public shell markup in `templates/public_shell.html` for a persistent desktop/mobile navigation model.</goal>
  <details>
    Introduce a mobile navigation toggle pattern that works inside the existing fixed topbar.
    Keep route links declarative and compatible with History API interception.
    Preserve the public/admin separation in shell structure.
  </details>
</task>

<task id="01-2" type="client-routing">
  <goal>Harden route changes in `static/js/spa.js` so SPA navigation remains instant and predictable.</goal>
  <details>
    Keep route-only paths as the public state model.
    Preserve direct route entry, browser back/forward behavior, and route fallback to `/`.
    Ensure route changes do not trigger full reloads for internal public links.
  </details>
</task>

<task id="01-3" type="data-loading">
  <goal>Keep the startup data-fetch model explicit and route-safe.</goal>
  <details>
    Continue bootstrapping the SPA from a single `/api/site-data` fetch.
    Add only lightweight loading feedback for startup or delayed render states.
    Avoid per-route fetch complexity in this phase.
  </details>
</task>

<task id="01-4" type="interaction-design">
  <goal>Tune `static/css/spa.css` for subtle route transitions and a reliable fixed-shell layout.</goal>
  <details>
    Retain understated fade/slide transitions.
    Ensure the fixed topbar, content container, and mobile navigation state work on desktop and mobile.
    Do not let motion or layout changes fight the particle background.
  </details>
</task>

## Verification

- Opening `/`, `/about`, `/projects`, and `/contact` directly still renders the correct SPA route
- Clicking route links updates the URL and swaps content without a full refresh
- Browser back/forward navigation behaves correctly
- Mobile navigation can open, navigate, and close cleanly
- The public SPA still fetches content only once on startup

## Exit Criteria

- Phase 2 route-shell requirements are fully covered by one stable public navigation model
- The shell is strong enough that later Phase 3 design work can focus on content presentation rather than routing repair
