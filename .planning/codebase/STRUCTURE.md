# Structure

Last mapped: 2026-04-19

## Top-Level Layout

- `app.py`: central Flask application, route definitions, upload config, and admin handlers
- `config.py`: environment-driven configuration
- `models.py`: SQLAlchemy models and password helpers
- `requirements.txt`: Python dependency manifest
- `README.md`: setup notes and a high-level architecture description
- `Procfile`: deployment process declaration

## Data and Migration Directories

- `data/resume_data.json`: fallback portfolio content extracted from a resume
- `migrations/env.py`: Alembic runtime configuration
- `migrations/alembic.ini`: migration settings
- `migrations/versions/3c82fbdcce8f_initial.py`: first tracked migration
- `migrations/versions/64ed07a75625_add_image_file_to_certification_model.py`: certification image field migration

## Script Directory

- `scripts/parse_resume.py`: heuristic resume PDF parsing
- `scripts/populate_db.py`: JSON-to-database importer
- `scripts/create_admin.py`: admin user bootstrap/update utility

## Template Directory

- `templates/base.html`: shared layout, navbar, CDN assets, flash messages, particle background
- `templates/index.html`: hero and contact landing page
- `templates/about.html`: summary and personal details page
- `templates/educational.html`: education listing page
- `templates/technical_skills.html`: skills page
- `templates/professional_experience.html`: experience page
- `templates/projects.html`: project listing page
- `templates/certifications.html`: certifications page
- `templates/admin_login.html`: admin login screen
- `templates/admin_dashboard.html`: admin forms and CSRF token source

## Static Directory

- `static/css/`: page-specific and shared styles like `style.css`, `home.css`, and `admin_dashboard.css`
- `static/js/admin.js`: admin dashboard interaction logic
- `static/js/skills-animation.js`: skills page interaction
- `static/resume/resume.pdf`: downloadable public resume artifact
- `static/uploads/certs/`: uploaded certification images

## Naming and Organization Patterns

- Routing names in `app.py` largely match template names and URL intent
- Template filenames use descriptive snake_case
- CSS files are mostly per-page and mirror template concerns
- Model classes in `models.py` are singular nouns with simple fields

## Missing or Unusual Structure Signals

- There is no package directory such as `src/` or an app package; everything server-side is flat at repo root
- There are no `tests/`, `.github/`, or CI workflow directories
- Public portfolio content is split across database rows and `data/resume_data.json`, creating two content sources
- Uploaded user-managed content lives inside the same tree as versioned static assets under `static/`
