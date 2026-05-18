# Phase 4: Prepare AWS Deployment - Context

**Gathered:** 2026-05-14
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase makes the portfolio operationally ready for an initial AWS deployment. It covers deployment packaging, host topology, same-server MySQL strategy, runtime process layout, persistence handling for uploads, environment-variable handling, HTTPS/domain setup, and backup expectations. It does not redesign the app, change the DB-first content model, or move uploads to managed cloud storage yet.

</domain>

<decisions>
## Implementation Decisions

### AWS deployment model
- **D-01:** Use a temporary-free AWS deployment path rather than designing for permanent zero-cost hosting on AWS.
- **D-02:** Do not use RDS in this phase.
- **D-03:** Keep the database on the same server as the app for the first deployment.

### Packaging and runtime
- **D-04:** The first deployment must use Docker for the Flask application.
- **D-05:** The target runtime topology is `Nginx + Dockerized Flask app + systemd`.
- **D-06:** Nginx should terminate HTTP/HTTPS and reverse-proxy requests into the Flask container.

### Database strategy
- **D-07:** MySQL should be installed directly on the server, not run in Docker.
- **D-08:** The app container should connect to the host MySQL instance through environment-driven configuration.
- **D-09:** Same-server MySQL is accepted as a cost-control tradeoff for the first AWS deployment.

### File persistence
- **D-10:** Keep resume and certificate uploads on local disk in this phase.
- **D-11:** Upload paths must be mounted into the container from persistent host directories so uploads survive container replacement.
- **D-12:** This phase should explicitly document that local-disk uploads are still instance-bound and not yet durable like object storage.

### Secrets and deployment workflow
- **D-13:** Runtime secrets and configuration should be stored in a server-side `.env` file, not committed to git.
- **D-14:** The first deployment workflow should be manual SSH deployment with repeatable Docker commands.
- **D-15:** The deployment plan must include the exact environment variables required by Flask, MySQL, cookies, and production runtime.

### Public access and recovery
- **D-16:** Production deployment should use a custom domain and HTTPS in this phase.
- **D-17:** Database backup should use scheduled `mysqldump` on the same server.
- **D-18:** Backup guidance should be treated as part of deployment readiness, not deferred entirely.

### the agent's Discretion
- Exact Dockerfile and image layering strategy
- Whether Docker Compose, plain `docker run`, or another lightweight Docker workflow is the cleanest first implementation
- Exact host directory layout for mounted uploads, logs, and app deployment files
- Exact certbot/Nginx integration details as long as HTTPS setup is reproducible

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project scope and validated constraints
- `.planning/PROJECT.md` - locked product direction, architecture constraints, and current active deployment goal
- `.planning/REQUIREMENTS.md` - requirement mapping, especially `PLAT-02`
- `.planning/ROADMAP.md` - Phase 4 goal, success criteria, and deployment risk framing
- `.planning/STATE.md` - current handoff state entering deployment preparation

### Prior phase decisions that remain binding
- `.planning/phases/01-stabilize-backend-foundation/01-CONTEXT.md` - DB-first fallback model, local file-storage policy, and admin/runtime constraints
- `.planning/phases/02-ship-spa-navigation-shell/01-CONTEXT.md` - SPA shell/public routing behavior that deployment must preserve
- `.planning/phases/03-redesign-public-experience/01-CONTEXT.md` - public UX direction and public/admin separation that production deployment must not break

### Current application files
- `app.py` - Flask entrypoint, upload paths, download route, CSRF behavior, and current runtime assumptions
- `config.py` - environment-variable contract, MySQL URI construction, cookie settings, and runtime config behavior
- `models.py` - DB model surface that same-server MySQL must support
- `Procfile` - current production command expectation
- `requirements.txt` - Python package/runtime dependencies, including `gunicorn`, `pymysql`, and `psycopg2-binary`
- `data/resume_data.json` - fallback content file that must remain available in production
- `static/uploads/` - upload target pattern implied by the app
- `static/resume/` - resume file path used by `download_resume`

### AWS and hosting references
- [EC2 Free Tier usage](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-free-tier-usage.html) - current AWS free-tier limits and temporary-free constraints
- [AWS Free Tier overview](https://aws.amazon.com/free/) - account-level free-plan/credit model context
- [Amazon RDS Free Tier](https://aws.amazon.com/rds/free/) - confirms RDS is free-plan/trial bound rather than permanently free
- [Amazon Lightsail pricing](https://aws.amazon.com/lightsail/pricing/?loc=ft) - pricing/trial context used to reject Lightsail as the locked first path

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `config.py:build_local_mysql_uri()` - existing env-driven MySQL connection builder that can be reused in production with different variables
- `Procfile` - existing `gunicorn app:app` production process hint
- `app.py:download_resume()` - current production path for serving the uploaded resume
- `app.py` upload handlers - existing certificate and resume persistence assumptions that need host-volume support

### Established Patterns
- The app already uses environment-variable driven config via `.env` and `python-dotenv`
- The portfolio is DB-first with JSON fallback, so production deployment must preserve DB access and fallback file access
- Uploads currently live under `static/`, which makes them simple to serve but ties persistence to host storage
- Admin and public flows share one Flask app process, so deployment should not split them into separate services

### Integration Points
- Docker packaging should center around `app.py`, `requirements.txt`, and the existing Flask/Gunicorn runtime
- Host-mounted directories must connect cleanly to `static/uploads` and `static/resume`
- Nginx and HTTPS setup must preserve SPA direct-link behavior for `/about`, `/projects`, and the other public shell routes
- MySQL server installation and env vars must line up with the existing `LOCAL_DB_*` / `DATABASE_URL` config contract

</code_context>

<specifics>
## Specific Ideas

- The deployment target is explicitly cost-minimized, not “best-practice cloud architecture.”
- Docker is a hard requirement for the first deploy, but MySQL should stay outside Docker to reduce persistence complexity.
- The first deployment is allowed to be manual as long as the exact steps are documented and repeatable.
- AWS is being used for temporary-free hosting only; long-term zero-cost hosting is not assumed.

</specifics>

<deferred>
## Deferred Ideas

- Moving MySQL to RDS
- Moving uploads to S3 or another managed object store
- Full CI/CD pipeline for automated deploys
- Infrastructure as Code for AWS provisioning
- Migrating to a permanently free non-AWS hosting stack

</deferred>

---

*Phase: 04-prepare-aws-deployment*
*Context gathered: 2026-05-14*
