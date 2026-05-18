# Phase 4: Prepare AWS Deployment - Research

**Date:** 2026-05-17
**Phase:** 04-prepare-aws-deployment
**Status:** Complete

## Goal

Research the lowest-complexity AWS deployment path that still fits the locked Phase 4 decisions:

- temporary-free AWS deployment
- Dockerized Flask app
- same-server MySQL
- no RDS
- Nginx in front
- manual SSH deploy
- custom domain + HTTPS
- scheduled `mysqldump`

## Findings

### 1. AWS free-tier reality

- AWS no longer guarantees a permanently free production setup for new accounts.
- Current EC2 guidance states free usage is time-limited for newer accounts and tied to free-plan/credit rules.
- This confirms the Phase 4 decision to optimize for a temporary-free launch, not a forever-free AWS architecture.

**Primary references**
- [EC2 Free Tier usage](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-free-tier-usage.html)
- [AWS Free Tier overview](https://aws.amazon.com/free/)

### 2. App host choice

- A plain EC2 Linux instance is the cleanest target once Docker is a hard requirement.
- It gives direct control over Docker, Nginx, certbot, systemd, and local MySQL without the extra abstraction of Elastic Beanstalk.
- Lightsail is simpler for some cases, but the user locked Docker-first deployment and same-server MySQL, which fits EC2 better.

### 3. Docker packaging direction

- The current app already has a production command shape via `Procfile`: `gunicorn app:app`.
- The codebase uses a single Flask app process, so one app container is sufficient.
- The container should stay stateless except for mounted persistent paths:
  - `static/uploads`
  - `static/resume`
- This avoids losing uploaded assets when the container is rebuilt or replaced.

### 4. MySQL strategy

- Same-server MySQL is the cheapest locked option.
- Running MySQL outside Docker reduces persistence complexity on a small single-host setup.
- The app can connect to it using either:
  - `DATABASE_URL`
  - or the existing `LOCAL_DB_*` variables already supported by `config.py`

### 5. Reverse proxy and process management

- `Nginx + Gunicorn + systemd` remains the most standard operational shape for this Flask app.
- With Docker added, the clean host model is:
  - Nginx on host
  - Flask app in Docker
  - MySQL on host
  - systemd managing the container lifecycle or a wrapper service

### 6. HTTPS and domain

- Let’s Encrypt remains the correct zero-cost TLS path.
- Certbot with Nginx is a standard documented setup and fits the chosen host topology.

**Primary references**
- [Let’s Encrypt documentation](https://letsencrypt.org/docs/)
- [NGINX / Certbot TLS guide](https://docs.nginx.com/nginx-unit/howto/certbot/)

### 7. Server OS and install path

- Ubuntu remains the most practical host choice because:
  - Docker installation is well documented
  - Nginx and Certbot support is straightforward
  - MySQL package setup is well understood

**Primary references**
- [Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

## Recommended implementation shape

### Host topology

- EC2 Ubuntu instance
- host-installed MySQL
- host-installed Nginx
- Dockerized Flask app
- host-mounted persistent directories for resume and certificate uploads

### Environment contract

The deployment plan should explicitly define:

- `SECRET_KEY`
- `DATABASE_URL` or `LOCAL_DB_*`
- `COOKIE_SECURE=true`
- any Flask runtime variables needed for production behavior

### Persistence rules

- Container image should not be treated as durable storage
- Resume and certificate directories must live on host disk and be mounted into the container
- Backup scope must cover:
  - MySQL dumps
  - uploaded files
  - server `.env`
  - Nginx config

## Risks to plan around

1. Same-server MySQL creates a single-host failure domain.
2. Local uploads are still instance-bound even with host mounts.
3. EC2 free eligibility may expire or vary by account age and credit usage.
4. SPA direct-link routing can break if Nginx is not configured to hand public routes back to Flask correctly.
5. Manual deploy is simple, but only if the runbook is explicit and reproducible.

## Planning implications

The phase should split into two implementation waves:

1. **Application packaging and runtime preparation**
   - Dockerfile
   - `.dockerignore`
   - production env contract
   - mounted upload path compatibility

2. **Host operations and deployment runbook**
   - Nginx reverse proxy
   - HTTPS/domain setup
   - EC2 setup steps
   - MySQL install/config notes
   - backup/runbook documentation

## Conclusion

The best plan for this codebase is not “full cloud architecture.” It is a cost-minimized, single-host EC2 deployment with:

- Dockerized Flask app
- host-installed MySQL
- host-installed Nginx
- HTTPS via Let’s Encrypt
- explicit host-mounted storage for uploads
- repeatable manual deploy documentation

That is the lowest-complexity path consistent with the locked Phase 4 decisions.
