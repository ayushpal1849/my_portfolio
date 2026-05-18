# Stack

Last mapped: 2026-04-19

## Overview

- Primary language: Python
- Web stack: Flask with Jinja templates
- ORM and migrations: Flask-SQLAlchemy and Flask-Migrate/Alembic
- Frontend stack: server-rendered HTML, Bootstrap 5, custom CSS, vanilla JavaScript
- Data sources: relational database plus JSON fallback from `data/resume_data.json`

## Runtime

- Application entry point is `app.py`
- Configuration lives in `config.py`
- Production process hint is `Procfile`
- Python dependencies are pinned loosely in `requirements.txt`

## Python Dependencies

- `Flask>=2.2` for routing, request handling, templating, and flashing
- `Flask-SQLAlchemy>=3.0` for ORM access in `models.py`
- `Flask-Migrate>=4.0` for Alembic-driven schema changes under `migrations/`
- `python-dotenv>=1.0` for `.env` loading in `config.py`
- `pymysql>=1.0` for local MySQL development
- `psycopg2-binary>=2.9` for PostgreSQL-style `DATABASE_URL` deployments
- `Flask-WTF>=1.1` and `Werkzeug>=3.0` for CSRF and request helpers
- `Flask-Bcrypt>=1.0.1` and `bcrypt>=4.0.1` for password hashing in `models.py`
- `gunicorn>=21.2` for production serving

## Frontend Dependencies

- Bootstrap CSS/JS is loaded from CDN in `templates/base.html`
- Bootstrap Icons is loaded from CDN in `templates/base.html`
- Google Fonts (`Poppins`, `Roboto`) are loaded from CDN in `templates/base.html`
- `tsparticles-slim` is loaded from CDN in `templates/base.html` for animated background effects

## Configuration Model

- `config.py` reads `SECRET_KEY`, `FLASK_SECRET_KEY`, `DATABASE_URL`, and local MySQL fallback variables
- The module defines top-level `SQLALCHEMY_DATABASE_URI`, but the active `Config` class only uses `os.getenv('DATABASE_URL')`
- In practice `app.py` loads `Config`, so local MySQL fallback logic is currently not applied unless `Config` is updated
- Upload behavior is configured directly in `app.py` via `UPLOAD_FOLDER` and `ALLOWED_EXTENSIONS`

## Persistence

- ORM models are in `models.py`
- Migration environment is in `migrations/env.py`
- Schema revisions exist in `migrations/versions/3c82fbdcce8f_initial.py` and `migrations/versions/64ed07a75625_add_image_file_to_certification_model.py`
- Resume fallback data is stored in `data/resume_data.json`
- Resume assets live in `assets/resume.pdf` and `static/resume/resume.pdf`

## Supporting Scripts

- `scripts/parse_resume.py` extracts text from `assets/resume.pdf` into `data/resume_data.json`
- `scripts/populate_db.py` imports JSON data into the database
- `scripts/create_admin.py` creates or updates an admin user from env vars or prompts

## Deployment Notes

- `Procfile` suggests a Gunicorn-style deployment target
- README mentions multiple hosting options, but no container or CI config is present
- Static uploads are stored on local disk under `static/uploads/`, which implies ephemeral-file risk on many hosted platforms
