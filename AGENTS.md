# Project Guidance

This repository uses `.planning/` as the source of execution context.

## Read First

1. `.planning/PROJECT.md`
2. `.planning/REQUIREMENTS.md`
3. `.planning/ROADMAP.md`
4. `.planning/STATE.md`
5. `.planning/codebase/`

## Current Direction

- Public site is a JavaScript-driven single-shell SPA
- Admin stays separate and server-rendered
- Content remains dual-mode: DB first, JSON fallback
- Local development targets MySQL
- Deployment target is AWS free tier

## Execution Priority

Work phases in roadmap order unless the user explicitly overrides:

1. Stabilize backend foundation
2. Ship SPA navigation shell
3. Redesign public experience
4. Prepare AWS deployment

## Guardrails

- Do not remove the JSON fallback model without explicit approval
- Do not merge admin into the public SPA
- Do not rewrite README until implementation stabilizes
- Prefer incremental verification after each phase
