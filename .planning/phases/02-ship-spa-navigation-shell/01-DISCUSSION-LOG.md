# Phase 2 Discussion Log

**Date:** 2026-04-20
**Phase:** 2 - Ship SPA Navigation Shell

## User Decisions

- Navigation should change pages without refresh in a JavaScript-driven SPA shell.
- Browser URLs should update with History API route paths.
- Public HTML should be replaced by SPA shell plus API-style content delivery.
- Visual direction should be creative.
- Keep the particle background.
- Navigation behavior: immediate route change with lightweight loading feedback.
- View transitions: subtle fade/slide.
- Data model: fetch once on startup.
- URL behavior: route-only paths.
- Shell structure: fixed navbar plus responsive mobile menu.
- Certifications page:
  - certificate list should be scrollable
  - certificate image preview should stay fixed/sticky on desktop
  - preview sizing should align to the image instead of stretching awkwardly
- Admin pages:
  - keep separate from the public SPA
  - make login and dashboard visually match the rest of the site

## Planning Notes

- These decisions are sufficient to plan Phase 2 without additional research.
- The certificate and admin visual changes are accepted as explicit user-directed scope inside Phase 2.
- Full creative redesign of the public experience remains Phase 3, but Phase 2 is allowed to refine shell-level presentation where it supports navigation and requested route layouts.
