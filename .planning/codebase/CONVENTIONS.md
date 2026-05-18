# Conventions

Last mapped: 2026-04-19

## Backend Style

- Route handlers in `app.py` are function-based and directly decorated with `@app.route(...)`
- Imports are mostly grouped at the top, though some local imports exist inside handlers such as `import json as _json`
- Most handlers return either rendered templates or `jsonify(...)` payloads
- Validation style is lightweight and inline, using explicit `if not ...` guards

## Data Handling Conventions

- JSON fallback loading is centralized in `load_resume_data()` in `app.py`
- Several handlers use the same pattern:
  - try a model query
  - catch `OperationalError`
  - flash a warning
  - fall back to `data/resume_data.json`
- Experience responsibilities are stored as JSON text in `Experience.responsibilities`
- Templates expect mixed data shapes: ORM objects in some paths and plain dictionaries in fallback paths

## Security and Auth Conventions

- Login state is represented by `session['admin_logged_in']`
- Some protected routes check for that flag explicitly and return `401` or redirect
- CSRF tokens are embedded in `templates/admin_dashboard.html` and attached in `static/js/admin.js`
- File upload filtering uses a simple extension allowlist in `allowed_file()` in `app.py`

## Frontend Conventions

- All templates extend `templates/base.html`
- Page-specific styles are included with a `{% block styles %}` override
- UI styling mixes Bootstrap utility classes with custom CSS files under `static/css/`
- Client-side behavior is kept in vanilla JavaScript with DOMContentLoaded handlers

## Database and Model Conventions

- Model definitions are flat and minimal in `models.py`
- No explicit relationships or foreign keys are defined
- Helper behavior is added directly on models, for example `User.set_password()` and `Skill.get_skills_by_category()`
- Migrations are auto-generated Alembic revisions stored under `migrations/versions/`

## Documentation Conventions

- `README.md` describes the app at a high level, but some details are outdated relative to the current code
- Inline comments are used sparingly and usually explain intent around uploads or parsing

## Inconsistencies to Note

- Auth protection is inconsistent: `/admin/add_experience` and `/admin/add_project` lack the session check used by `/admin/add_certification` and `/admin/upload_resume`
- Configuration is inconsistent between module-level variables in `config.py` and the `Config` class actually used by `app.py`
- `models.py` comments imply bcrypt must be initialized, but there is no matching initialization in `app.py`
