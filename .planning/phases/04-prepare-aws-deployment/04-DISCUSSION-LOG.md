# Phase 4: Prepare AWS Deployment - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in `04-CONTEXT.md`.

**Date:** 2026-05-14
**Phase:** 04-prepare-aws-deployment
**Areas discussed:** app hosting, database hosting, file uploads, runtime topology, secrets/config, deploy workflow, domain/HTTPS, backups, Docker packaging

---

## App hosting

| Option | Description | Selected |
|--------|-------------|----------|
| Amazon Lightsail | Simple VM-style hosting with predictable pricing | |
| Elastic Beanstalk | Managed AWS app deployment | |
| AWS temporary-free VM path | Cost-minimized AWS-first deployment path | ✓ |

**User's choice:** AWS temporary-free deployment
**Notes:** User wants AWS, but accepted that the plan is temporary-free rather than permanently free.

---

## Database hosting

| Option | Description | Selected |
|--------|-------------|----------|
| RDS MySQL | Managed AWS database | |
| Same-server MySQL | Database runs on the same machine as the app | ✓ |
| Non-AWS free database | Move away from AWS for permanent free hosting | |

**User's choice:** Same-server MySQL, no RDS
**Notes:** Decision is driven by cost minimization.

---

## Deployment packaging

| Option | Description | Selected |
|--------|-------------|----------|
| Traditional VM install | Python app directly on the server | |
| Dockerized app | Flask app packaged and deployed in Docker | ✓ |

**User's choice:** First deploy on Docker
**Notes:** This became a hard requirement for the phase.

---

## Runtime topology

| Option | Description | Selected |
|--------|-------------|----------|
| Gunicorn only | Minimal app process setup | |
| Nginx + Dockerized Flask app + systemd | Reverse proxy in front of containerized app | ✓ |
| Full container stack including DB | App and DB both in containers | |

**User's choice:** Agreed with `Nginx + Dockerized Flask app + systemd`
**Notes:** MySQL remains outside Docker.

---

## MySQL placement

| Option | Description | Selected |
|--------|-------------|----------|
| MySQL in Docker | Database container on same host | |
| MySQL installed directly on server | Native DB install on the same host | ✓ |

**User's choice:** MySQL installed directly on the server
**Notes:** Chosen to reduce persistence and recovery complexity.

---

## File uploads

| Option | Description | Selected |
|--------|-------------|----------|
| Local disk in container only | Keep uploads only inside container filesystem | |
| Local disk with host-mounted persistent directories | Persist uploads outside container | ✓ |
| S3 now | Move to object storage immediately | |

**User's choice:** Agreed with local disk plus persistent host mounts
**Notes:** S3 deferred.

---

## Secrets/config

| Option | Description | Selected |
|--------|-------------|----------|
| Server-side `.env` | Keep secrets in server environment file | ✓ |
| AWS Secrets Manager | Managed secret storage | |

**User's choice:** Agreed with server-side `.env`
**Notes:** Keeps first deploy simple.

---

## Deploy workflow

| Option | Description | Selected |
|--------|-------------|----------|
| Manual SSH deploy | Repeatable manual deployment steps over SSH | ✓ |
| CI/CD pipeline now | Automated pipeline in this phase | |

**User's choice:** Agreed with manual SSH deploy
**Notes:** CI/CD deferred.

---

## Domain and HTTPS

| Option | Description | Selected |
|--------|-------------|----------|
| Raw IP only | No domain/HTTPS in first deploy | |
| Custom domain + HTTPS | Production-ready public access | ✓ |

**User's choice:** Agreed with custom domain + HTTPS in this phase
**Notes:** Required for portfolio credibility.

---

## Backups

| Option | Description | Selected |
|--------|-------------|----------|
| No explicit backup plan | Minimal setup | |
| Scheduled `mysqldump` on same server | Cheapest first backup path | ✓ |
| Managed backup service | More robust but higher cost/complexity | |

**User's choice:** Agreed with scheduled `mysqldump`
**Notes:** Fits same-server MySQL and cost constraints.

---

## the agent's Discretion

- Exact Docker workflow shape
- Exact Nginx config structure
- Exact host volume layout
- Exact HTTPS automation details

## Deferred Ideas

- RDS migration
- S3 migration
- CI/CD
- IaC
- Permanent zero-cost non-AWS hosting
