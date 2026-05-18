---
plan_id: "01"
phase: "03"
phase_name: "Redesign Public Experience"
title: "Rebuild the Homepage and Shared Visual System"
wave: 1
depends_on: []
requirements_addressed:
  - "UX-01"
  - "UX-02"
  - "UX-03"
  - "UX-04"
autonomous: true
files_modified:
  - "templates/public_shell.html"
  - "static/js/spa.js"
  - "static/css/spa.css"
---

# Plan 01: Rebuild the Homepage and Shared Visual System

## Objective

Replace the current generic glassmorphism-heavy homepage and base styling with a stronger editorial + futuristic premium visual system, while preserving the Phase 2 SPA shell behavior and keeping the experience readable, mobile-safe, and recruiter-oriented.

## Must Haves

- Public visual direction clearly shifts away from template-like layout and styling
- Dark overall mood is preserved
- Cyan + gold becomes the controlled accent palette
- Particle background remains atmospheric and does not overpower content
- Typography uses a premium editorial hierarchy with serif-led headings and clean sans UI/body copy
- The homepage becomes a recruiter-focused landing with a stronger proof-first structure
- Resume download and contact remain obvious and accessible

## Tasks

<task id="01-1" type="visual-system">
  <goal>Redesign the shared public visual system in `static/css/spa.css` around the locked Phase 3 art direction.</goal>
  <details>
    Rework tokens, section spacing, panel treatment, type hierarchy, accent usage, and visual layering.
    Keep the design restrained and technical rather than neon-heavy or playful.
    Preserve mobile readability and route-level usability established in Phase 2.
  </details>
</task>

<task id="01-2" type="homepage">
  <goal>Rebuild `renderHome()` in `static/js/spa.js` into the recruiter-focused landing structure decided in context.</goal>
  <details>
    The home route should prioritize engineering credibility first, then proof, then supporting story.
    Include hero, proof strip, featured projects teaser, supporting credibility section, and contact CTA.
    Keep the hero text-and-work focused with no portrait/avatar.
  </details>
</task>

<task id="01-3" type="shell-polish">
  <goal>Adjust `templates/public_shell.html` only as needed to support the redesigned public presentation.</goal>
  <details>
    Preserve the single-shell SPA architecture and route wiring.
    Only change shell markup where the redesign requires stronger framing or semantics.
  </details>
</task>

<task id="01-4" type="cta-hierarchy">
  <goal>Make action priority explicit throughout the redesigned public experience.</goal>
  <details>
    Keep `Explore Projects` as the dominant action.
    Keep `Download Resume` clearly visible as the secondary action.
    Keep contact available as a tertiary path without overpowering proof sections.
  </details>
</task>

## Verification

- The homepage feels materially different from the current template-like presentation
- The visual system reads as dark, premium, and technical rather than generic
- Hero, proof strip, and CTA hierarchy align with recruiter-first scanning behavior
- Particle background remains supportive rather than distracting
- Mobile layout still feels intentional rather than merely compressed

## Exit Criteria

- The public experience has a coherent visual language that satisfies `UX-01` and `UX-02`
- The homepage becomes a strong landing surface that supports `UX-03` and `UX-04`
