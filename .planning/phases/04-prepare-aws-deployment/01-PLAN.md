---
plan_id: "01"
phase: "04"
phase_name: "Prepare AWS Deployment"
title: "Containerize the Flask App and Lock the Production Runtime Contract"
wave: 1
depends_on: []
requirements_addressed:
  - "PLAT-02"
autonomous: true
files_modified:
  - "Dockerfile"
  - ".dockerignore"
  - "app.py"
  - "config.py"
  - "requirements.txt"
  - "docker-compose.yml"
  - ".env.example"
---

# Plan 01: Containerize the Flask App and Lock the Production Runtime Contract

## Objective

Make the existing Flask portfolio runnable in a production-oriented Docker container while preserving the locked architecture: one Flask app container, host-installed MySQL, mounted local upload storage, and environment-driven runtime configuration.

## Must Haves

- Flask app can run in Docker with `gunicorn app:app`
- Docker runtime works with the existing DB-first plus JSON-fallback behavior
- Resume and certificate paths remain compatible with host-mounted persistence
- Production configuration is explicit and driven by environment variables
- Container setup does not assume MySQL runs inside Docker

## Tasks

<task id="01-1" type="containerization">
  <goal>Create a production-ready Docker image for the Flask app.</goal>
  <details>
    Add a `Dockerfile` that installs Python dependencies, copies the app, and runs Gunicorn.
    Add `.dockerignore` so local virtualenvs, caches, git data, and planning artifacts do not bloat the image.
    Keep the image simple and reproducible rather than over-optimizing layers.
  </details>
</task>

<task id="01-2" type="runtime-contract">
  <goal>Make the runtime configuration explicit for Docker and EC2 deployment.</goal>
  <details>
    Audit `config.py` and any related runtime assumptions so the app can cleanly use production env vars.
    Prefer one clear production contract using `DATABASE_URL` for server deployment while keeping local MySQL fallback intact for development.
    Add a safe `.env.example` that documents required variables without leaking secrets.
  </details>
</task>

<task id="01-3" type="persistence">
  <goal>Preserve upload and resume behavior under a containerized deployment.</goal>
  <details>
    Verify the existing `static/uploads` and `static/resume` paths can be mounted from host directories.
    Adjust path handling only if needed to keep current app behavior compatible with host-mounted volumes.
    Do not move uploads to S3 or redesign file handling in this phase.
  </details>
</task>

<task id="01-4" type="local-ops">
  <goal>Provide a lightweight local/prod-like orchestration path for the app container.</goal>
  <details>
    Add a minimal Docker orchestration file only if it materially helps repeatable deployment.
    Keep MySQL outside Docker per the locked Phase 4 decision.
    Do not introduce unnecessary multi-container complexity.
  </details>
</task>

## Verification

- Docker image builds successfully
- App container can boot with env-driven configuration
- Mounted resume and upload directories remain readable/writable by the app
- Production runtime does not depend on local Windows-only paths or dev-only assumptions

## Exit Criteria

- The codebase has a clear, reproducible container runtime for the Flask app
- The production env contract is explicit enough for host deployment planning in Wave 2

