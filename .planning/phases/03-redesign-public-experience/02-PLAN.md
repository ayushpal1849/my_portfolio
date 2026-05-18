---
plan_id: "02"
phase: "03"
phase_name: "Redesign Public Experience"
title: "Restructure Route-Level Content and Elevate Projects Presentation"
wave: 2
depends_on:
  - "01"
requirements_addressed:
  - "UX-01"
  - "UX-03"
  - "UX-04"
autonomous: true
files_modified:
  - "static/js/spa.js"
  - "static/css/spa.css"
---

# Plan 02: Restructure Route-Level Content and Elevate Projects Presentation

## Objective

Apply the new design system across the public routes so the site feels cohesive beyond the homepage, and upgrade the projects route into a featured-project-plus-supporting-grid presentation that better communicates capability and proof.

## Must Haves

- Projects no longer all carry equal visual weight
- One project is visually featured with deeper narrative support
- Remaining projects are presented in a supporting grid or scan-friendly structure
- About, skills, experience, certifications, and contact routes all align with the redesigned system
- Route-level layouts feel intentional on both desktop and mobile
- Contact and resume paths remain easy to find throughout the public experience

## Tasks

<task id="02-1" type="projects-presentation">
  <goal>Rework the projects route in `static/js/spa.js` and `static/css/spa.css` into one featured project plus supporting project grid.</goal>
  <details>
    Give the featured project deeper storytelling space than the other projects.
    Preserve outward project links where they exist.
    Keep the route scan-friendly for recruiters while making the strongest project more memorable.
  </details>
</task>

<task id="02-2" type="route-design">
  <goal>Bring route-level sections into the new editorial premium system without breaking the current SPA behavior.</goal>
  <details>
    Rework section headers, tile arrangements, density, and rhythm across About, Skills, Experience, Certifications, and Contact.
    Preserve working interactions such as certifications preview behavior.
    Keep the information hierarchy consistent with the homepage.
  </details>
</task>

<task id="02-3" type="mobile-quality">
  <goal>Audit the redesigned route layouts for mobile completeness, not just responsiveness.</goal>
  <details>
    Ensure spacing, reading order, action placement, and route composition still feel deliberate on smaller screens.
    Do not allow the featured-project design or asymmetrical layout choices to collapse awkwardly on mobile.
  </details>
</task>

## Verification

- Projects route clearly highlights one featured project
- Supporting projects remain easy to scan
- Public routes feel part of one coherent design system
- Certifications interaction still works after route redesign
- Mobile layouts remain intentional, readable, and complete

## Exit Criteria

- The redesign extends beyond the homepage into a consistent visitor-facing product experience
- Projects presentation better communicates capability and supports recruiter decision-making
