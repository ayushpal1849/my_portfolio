---
phase: "04-prepare-aws-deployment"
status: "human_needed"
updated: "2026-05-17"
research: "completed"
verification_mode: "static-checks-plus-host-verification-needed"
---

# Phase 4 Verification

## Result

Implementation is complete locally, but host-level deployment verification is still required.

## Research Summary

Research confirmed the locked Phase 4 choices are coherent:

- EC2 is the cleanest AWS target once Docker is required
- same-server MySQL is the lowest-cost path consistent with the temporary-free constraint
- Nginx + Dockerized Flask app + systemd is the right host topology
- host-mounted local storage is required to preserve resume/certificate uploads across container replacement
- AWS free use is temporary and should be treated as such in the deployment runbook

See `04-RESEARCH.md`.

## Coverage Check

| Requirement | Covered By | Notes |
|-------------|------------|-------|
| `PLAT-02` | `01-PLAN.md`, `02-PLAN.md` | Wave 1 covers container/runtime contract; Wave 2 covers EC2 host setup, HTTPS, persistence, and backup runbook |

## Static Checks Completed

- Flask app import succeeded with the updated runtime config
- `config.py` resolved upload and resume folders correctly through the Flask app config
- deployment artifacts were written for:
  - Docker
  - Docker Compose
  - `.env` contract
  - Nginx
  - systemd
  - deployment scripts

## Manual Host Verification Still Required

1. Build the Docker image on a Linux host.
2. Start the app container with a real `.env`.
3. Confirm the app serves:
   - `/`
   - `/about`
   - `/projects`
   - `/admin/login`
   - `/healthz`
4. Confirm host-mounted resume and certificate uploads survive container replacement.
5. Install MySQL on the host and verify the app connects through `DATABASE_URL`.
6. Put Nginx in front of the container and verify SPA direct-link routes still work.
7. Run certbot on the domain and verify HTTPS works.
8. Run the backup script on the host and confirm a real SQL dump file is created.

## Execution Risks Already Captured

1. AWS temporary-free eligibility may expire by account age or credit usage.
2. Same-server MySQL creates a single-host failure domain.
3. Local uploads remain instance-bound even with host-mounted persistence.
4. Nginx must preserve direct SPA route behavior.

## Conclusion

Phase 4 is ready for server-side verification on the target EC2 host.
