---
plan_id: "01"
phase: "01"
phase_name: "Stabilize Backend Foundation"
title: "Stabilize Public Content API and Local Config"
wave: 1
depends_on: []
requirements_addressed:
  - "SPA-04"
  - "CONT-01"
  - "CONT-02"
  - "CONT-03"
  - "PLAT-01"
autonomous: true
files_modified:
  - "app.py"
  - "config.py"
  - "models.py"
---

# Plan 01: Stabilize Public Content API and Local Config

## Objective

Make the Flask backend expose a predictable SPA-ready content contract, preserve DB-plus-JSON fallback behavior without changing the public payload shape, and ensure local MySQL configuration resolves correctly when `DATABASE_URL` is absent.

## Must Haves

- `/api/site-data` remains the single aggregated public content endpoint
- API payload keeps stable keys with empty arrays or empty strings for missing values
- Fallback mode preserves the same payload shape and only changes `meta.source`
- Certification preview URLs are normalized consistently for DB-backed entries
- Local configuration resolves to MySQL automatically when `DATABASE_URL` is missing

## Tasks

<task id="01-1" type="backend">
  <goal>Audit and normalize the response contract returned by `get_public_content()` in `app.py`.</goal>
  <details>
    Ensure every public section returns stable keys and predictable scalar defaults.
    Confirm fallback JSON content and DB-backed content are normalized to the same shape.
    Remove any branch that would cause the SPA to receive structurally different payloads in fallback mode.
  </details>
</task>

<task id="01-2" type="backend">
  <goal>Harden fallback behavior without exposing degraded-mode noise in the public UX.</goal>
  <details>
    Keep `meta.source` in the API response for diagnostics.
    Do not introduce public warning banners or alternate payload formats.
    Make sure empty DB results and DB outage fallback are handled intentionally rather than accidentally.
  </details>
</task>

<task id="01-3" type="backend">
  <goal>Verify local configuration behavior in `config.py` is aligned with the Phase 1 decision.</goal>
  <details>
    Confirm `Config.SQLALCHEMY_DATABASE_URI` resolves to `DATABASE_URL` when present and otherwise uses local MySQL.
    Keep the configuration minimal and avoid adding deployment-specific complexity in this phase.
  </details>
</task>

<task id="01-4" type="consistency">
  <goal>Check model and serializer assumptions in `models.py` against the normalized API contract.</goal>
  <details>
    Verify `User`, `Experience`, `Project`, `Education`, `Certification`, `Skill`, and `Achievement` fields align with the API shape.
    Avoid introducing schema changes unless a concrete contract bug forces one.
  </details>
</task>

## Verification

- `GET /api/site-data` returns one aggregated payload with stable top-level keys
- Response shape does not change between DB-backed and fallback-backed execution paths
- Missing or empty content produces empty values, not missing keys
- Local development config does not require `DATABASE_URL` to resolve a valid MySQL URI

## Exit Criteria

- Public SPA can rely on a stable API contract without fallback-specific frontend branching
- Phase 1 API and configuration requirements are satisfied for downstream admin and routing work
