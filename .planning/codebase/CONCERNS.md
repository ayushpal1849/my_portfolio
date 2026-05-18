# Concerns

Last mapped: 2026-04-19

## Highest-Risk Issues

- `/admin/add_experience` and `/admin/add_project` in `app.py` accept POST writes without checking `session['admin_logged_in']`
- `Config.SQLALCHEMY_DATABASE_URI` in `config.py` only reads `DATABASE_URL`, so the intended local MySQL fallback declared earlier in the file is effectively bypassed
- `models.py` defines `bcrypt = Bcrypt()`, but the app bootstrap in `app.py` never initializes it with `bcrypt.init_app(app)`

## Security Concerns

- Admin authentication is a simple session boolean rather than a role-checked user identity model
- Uploaded files are stored under `static/uploads/`, making them immediately web-servable if linked or guessed
- File validation for certifications is extension-based only; MIME/content validation is absent
- The default secret key fallback in `config.py` and `Config` is development-friendly and unsafe for production if env vars are missing

## Data Integrity Concerns

- Public pages mix ORM rows and JSON dictionaries depending on database availability, which can hide shape mismatches until runtime
- `scripts/populate_db.py` imports data without idempotency guards beyond a final commit error path
- Experience responsibilities are stored as JSON text rather than normalized rows or a typed JSON column
- There is no transaction-level validation around uploaded certificate metadata or resume replacement

## Maintainability Concerns

- `app.py` is the single controller module for all routes, admin behavior, config overrides, and helpers
- There is no blueprint or service-layer separation, so growth will increase coupling quickly
- `README.md` says personal data is managed in `app.py`, but the live app now depends on `data/resume_data.json` and database tables
- `scripts/parse_resume.py` uses brittle heuristics and contains mojibake-like bullet characters, which suggests encoding issues in parsing assumptions

## Performance and Operations Concerns

- Every public request may hit the database first and only then fall back to JSON on `OperationalError`, which can create noisy failures when the DB is down
- Local-disk uploads and resume storage are fragile on ephemeral hosting platforms
- CDN-only frontend dependencies mean the site’s look and interactions depend on third-party availability

## Missing Engineering Safeguards

- No automated tests exist
- No CI workflow exists
- No linting or formatting configuration is present
- No environment example file or deployment validation script is present

## Refactor Pressure Points

- Split `app.py` into blueprints or route modules first
- Normalize auth checks across every `/admin/*` mutating endpoint
- Consolidate configuration so the deployed and local database behavior matches the documented intent
- Add a basic test harness before expanding admin functionality further
