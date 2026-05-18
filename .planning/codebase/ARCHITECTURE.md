# Architecture

Last mapped: 2026-04-19

## High-Level Shape

- The app is a monolithic Flask server in `app.py`
- Presentation, request handling, and part of the business logic live in the same module
- Persistence is isolated into ORM models in `models.py`
- Templates under `templates/` render all user-facing pages
- Static assets under `static/` provide CSS, JavaScript, uploaded files, and the public resume PDF

## Request Flow

- Browser requests a Flask route defined in `app.py`
- Route handler tries to read relational data through SQLAlchemy models from `models.py`
- If database access fails with `OperationalError`, the handler falls back to JSON data from `data/resume_data.json`
- Handler renders a Jinja template from `templates/`
- Static assets referenced through `url_for('static', ...)` are served from `static/`

## Data Flow Patterns

- Read path for public pages:
  - `load_resume_data()` in `app.py` reads `data/resume_data.json`
  - Page handlers query tables like `Education`, `Experience`, `Project`, `Certification`, and `Skill`
  - Templates consume either ORM rows or JSON dictionaries/lists
- Write path for admin pages:
  - `templates/admin_dashboard.html` renders hidden forms
  - `static/js/admin.js` submits JSON or multipart data to admin routes
  - `app.py` validates request data, persists via `db.session`, and returns JSON responses

## Main Architectural Components

- App bootstrap: `app.py`
- Configuration: `config.py`
- Persistence layer: `models.py`
- Migration layer: `migrations/`
- Resume ingestion utilities: `scripts/parse_resume.py` and `scripts/populate_db.py`
- Admin credential management: `scripts/create_admin.py`

## Entry Points

- Web runtime starts from `app.py`
- Dev execution uses `if __name__ == '__main__': app.run(debug=True)` in `app.py`
- Production execution likely uses `Procfile` and Gunicorn
- Data preparation starts from `scripts/parse_resume.py`
- Database seeding starts from `scripts/populate_db.py`

## Architectural Style

- Pattern is closest to "single-module MVC-ish Flask app"
- Views and controllers are not separated; route handlers directly orchestrate ORM and fallback logic
- There is no dedicated service layer, repository layer, or blueprint segmentation
- The app intentionally supports degraded operation without a live database by falling back to JSON

## Cross-Cutting Concerns

- Security: CSRF is enabled, but admin authorization is a simple session flag in `app.py`
- Error handling: most public data routes only catch `OperationalError`
- File handling: uploaded certificates and resume files are written to local disk under `static/`
- Rendering: all page composition flows through `templates/base.html`

## Architectural Gaps

- `models.py` defines `bcrypt = Bcrypt()` but `app.py` never calls `bcrypt.init_app(app)`
- `config.py` contains two configuration styles, but `Config` does not reflect the module-level MySQL fallback
- Admin routes for adding experience and projects do not enforce login, unlike other admin routes in `app.py`
