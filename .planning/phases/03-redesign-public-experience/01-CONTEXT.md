# Phase 3: Redesign Public Experience - Context

**Gathered:** 2026-04-26
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase redesigns the public-facing portfolio experience on top of the already-working SPA shell. It focuses on visual direction, content hierarchy, homepage composition, project presentation, typography, action emphasis, and mobile-safe presentation quality. It does not change the backend content model, the admin architecture, or the single-shell SPA routing model established in earlier phases.

</domain>

<decisions>
## Implementation Decisions

### Visual direction
- **D-01:** The public site should use a restrained editorial + futuristic premium visual direction.
- **D-02:** The overall mood should stay dark rather than switching to a light theme.
- **D-03:** The particle background remains, but it should act as atmosphere behind the content rather than as the dominant visual.
- **D-04:** Layouts should feel intentional and composed, like a modern technical product story page rather than a standard Bootstrap portfolio.

### Typography and tone
- **D-05:** Use serious technical tone with premium editorial styling.
- **D-06:** Major headings should use an expressive serif treatment, while body copy and interface text should use a clean sans-serif.
- **D-07:** Copy should stay concise, high-contrast, and confident rather than playful or overly corporate.

### Content hierarchy
- **D-08:** The visitor should first see engineering credibility.
- **D-09:** Projects should come second as proof of capability.
- **D-10:** Personal story comes after credibility and project proof.
- **D-11:** Contact or hire-path should remain visible, but not outrank proof sections.

### Homepage composition
- **D-12:** The homepage should use a recruiter-focused landing structure.
- **D-13:** The homepage should include:
  - a hero section explaining who Ayush is and what he builds
  - a proof strip showing high-signal credibility metrics
  - one featured projects section
  - a selected experience / credibility section
  - a contact CTA
- **D-14:** The homepage should prioritize proof quickly instead of starting with a generic biography-first flow.

### Projects presentation
- **D-15:** Projects should not all be presented with equal visual weight.
- **D-16:** The public projects section should feature one highlighted project plus a supporting project grid.
- **D-17:** The featured project should allow deeper narrative depth than the supporting project cards.

### Action emphasis
- **D-18:** The primary CTA should be `Explore Projects`.
- **D-19:** The secondary CTA should be `Download Resume`.
- **D-20:** Contact should remain accessible as a tertiary action.

### Personal imagery and palette
- **D-21:** Do not include a personal photo/avatar in the hero.
- **D-22:** Lock the accent palette to `cyan + gold`.

### the agent's Discretion
- Exact component layout details for each section
- Whether asymmetry appears through grid offsets, panel sizing, or sectional composition
- Exact motion treatment, as long as it remains subtle and does not fight readability
- Exact copy polish for headings and CTA labels, provided it stays aligned with the hierarchy above

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project and roadmap context
- `.planning/PROJECT.md` - active product direction, validated phases, and remaining work
- `.planning/REQUIREMENTS.md` - Phase 3 requirement mapping for `UX-01`, `UX-02`, `UX-03`, and `UX-04`
- `.planning/ROADMAP.md` - Phase 3 goal, success criteria, and execution notes
- `.planning/STATE.md` - current project status and next phase handoff

### Prior phase context
- `.planning/phases/02-ship-spa-navigation-shell/01-CONTEXT.md` - locked SPA shell and route behavior decisions
- `.planning/phases/02-ship-spa-navigation-shell/02-UAT.md` - verified runtime behavior that the redesign must preserve
- `.planning/phases/01-stabilize-backend-foundation/01-CONTEXT.md` - backend and admin boundary constraints that remain in force

### Current implementation files
- `templates/public_shell.html` - public SPA shell structure
- `static/js/spa.js` - route rendering and section presentation logic
- `static/css/spa.css` - current visual system and layout rules that will be redesigned
- `templates/base.html` - current shared admin base, relevant to preserving boundary separation
- `static/css/admin_dashboard.css` - evidence of the visual language already used for admin alignment

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `static/js/spa.js:renderHome()` - current homepage composition to replace or refine
- `static/js/spa.js:renderProjects()` - current project rendering surface where featured/supporting hierarchy can be introduced
- `static/js/spa.js:renderAbout()` and `static/js/spa.js:renderExperience()` - existing credibility and story sections that can be reordered or visually reframed
- `static/css/spa.css` color tokens and panel primitives - base styling system available for redesign rather than full rebuild from zero

### Established Patterns
- The app already uses a single-shell SPA with direct route entry and no-refresh navigation
- The public site already uses a dark atmosphere and particle background
- The certifications route already has a stronger layout pattern than some other public routes
- The admin side is intentionally separate and should not be pulled into public redesign scope

### Integration Points
- Phase 3 work will primarily concentrate in `static/css/spa.css`, `static/js/spa.js`, and possibly `templates/public_shell.html`
- CTA hierarchy changes must remain compatible with existing route names and `meta.resume_url`
- Public redesign must preserve mobile usability and all runtime behavior verified in Phase 2

</code_context>

<specifics>
## Specific Ideas

- The site should feel like a serious technical founder or engineer portfolio, not like a generic student template.
- The hero should be text-and-work focused, not portrait-driven.
- Accent usage should stay restrained: cyan as the primary cool signal, gold as the premium contrast signal.
- The redesign should make recruiters understand capability quickly without overwhelming them with too many equal-weight sections.

</specifics>

<deferred>
## Deferred Ideas

- Adding a personal photo/avatar to the public site
- Expanding projects into full case-study subpages with their own deep-link states
- Any deployment, storage, or infra presentation work beyond what the public UI needs

</deferred>

---

*Phase: 03-redesign-public-experience*
*Context gathered: 2026-04-26*
