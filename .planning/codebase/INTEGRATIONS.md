# Integrations

Last mapped: 2026-04-19

## Overview

- The application has no third-party business API integrations
- External dependencies are infrastructure-oriented: database drivers, CDN frontend assets, and PDF parsing tooling
- Authentication is local username/password against the `user` table in `models.py`

## Databases

- Production-style connection is expected through `DATABASE_URL` in `config.py`
- `requirements.txt` includes `psycopg2-binary`, indicating PostgreSQL support for hosted deployments
- Local development fallback is intended to use MySQL through `pymysql` and variables like `LOCAL_DB_USER`, `LOCAL_DB_PASS`, and `LOCAL_DB_NAME`
- Alembic migrations under `migrations/` manage schema evolution

## Local File Integrations

- Resume source PDF is read from `assets/resume.pdf` by `scripts/parse_resume.py`
- Parsed structured fallback data is written to `data/resume_data.json`
- Public downloadable resume is served from `static/resume/resume.pdf` by `/download_resume` in `app.py`
- Certification images are uploaded into `static/uploads/certs/` via `/admin/add_certification`

## Authentication and Session Handling

- Admin login posts to `/admin/login` in `app.py`
- Password verification uses `User.check_password()` in `models.py`
- Session state is tracked with `session['admin_logged_in']`
- CSRF protection is enabled globally with `CSRFProtect(app)` in `app.py`
- JavaScript admin requests pass the CSRF token from `templates/admin_dashboard.html` into `static/js/admin.js`

## Frontend Network Dependencies

- `templates/base.html` loads Bootstrap CSS from `https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css`
- `templates/base.html` loads Bootstrap Icons from `https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css`
- `templates/base.html` loads `tsparticles-slim` from `https://cdn.jsdelivr.net/npm/tsparticles-slim@2.12.0/tsparticles.slim.bundle.min.js`
- `templates/base.html` loads Google Fonts from `https://fonts.googleapis.com` and `https://fonts.gstatic.com`

## Client to Server Interfaces

- HTML pages are served by GET routes like `/`, `/about`, `/projects`, and `/technical-skills` in `app.py`
- JSON admin POST endpoints include `/admin/add_experience` and `/admin/add_project`
- Multipart admin POST endpoints include `/admin/add_certification` and `/admin/upload_resume`
- `static/js/admin.js` is the only client-side file making `fetch()` requests to the Flask backend

## Missing Integrations

- No email service, contact form backend, analytics, or OAuth provider is wired in
- No object storage integration exists for uploaded files
- No webhook or background job integration appears in the repo
- No payment, CMS, or search provider integration is present
