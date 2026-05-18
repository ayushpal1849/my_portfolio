# Testing

Last mapped: 2026-04-19

## Current State

- No `tests/` directory exists in the repository
- No unit, integration, or end-to-end test files were found by the codebase scan
- No CI workflow or automated verification pipeline is checked into the repo

## What Can Be Verified Manually Today

- Public route rendering from `app.py` can be checked by running the Flask app and browsing pages
- Admin login and dashboard flows can be exercised through `templates/admin_login.html`, `templates/admin_dashboard.html`, and `static/js/admin.js`
- Migration health can be checked with Flask-Migrate/Alembic commands against the configured database
- Resume parsing can be tested by running `scripts/parse_resume.py` against `assets/resume.pdf`
- Seeding can be tested by running `scripts/populate_db.py` after parsing

## Implicit Test Boundaries

- Fallback behavior when the database is unavailable is encoded in handlers like `/educational`, `/projects`, and `/technical-skills` in `app.py`
- Password hashing behavior is encapsulated in `User.set_password()` and `User.check_password()` in `models.py`
- Upload validation behavior exists in `allowed_file()` and the `/admin/upload_resume` and `/admin/add_certification` routes

## Recommended Initial Test Coverage

- Route smoke tests for all public GET endpoints in `app.py`
- Auth and redirect tests for `/admin/login`, `/admin/dashboard`, and `/admin/logout`
- Authorization regression tests for `/admin/add_experience` and `/admin/add_project`
- Model tests for password hashing in `models.py`
- Fallback-data tests that simulate `OperationalError` and verify template rendering still succeeds
- Upload tests for accepted and rejected file types

## Likely Tooling Fit

- `pytest` is the most natural fit given the current Flask application structure
- Flask’s test client would cover most route-level behavior without major refactors
- Temporary SQLite or dedicated test database config would make migration and ORM testing easier

## Gaps and Risks

- No automated checks currently protect admin authorization paths
- No regression coverage exists for the split JSON-versus-database content model
- No tests validate that migrations remain compatible with the current models
- No frontend automation covers the fetch-based admin dashboard flows
