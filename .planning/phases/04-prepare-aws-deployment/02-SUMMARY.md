# Plan 02 Summary

**Plan:** 02 - Define EC2 Host Setup, HTTPS Routing, Persistence, and Backup Runbook
**Completed:** 2026-05-17
**Status:** Complete

## Outcome

The repository now includes the deployment assets and operational runbook needed to launch the app on a temporary-free AWS EC2 Ubuntu host using Docker for Flask, host-installed MySQL, Nginx, HTTPS, and scheduled backups.

## Changes Made

- Added `deploy/README.md` with a full EC2 deployment runbook
- Added sample Nginx reverse-proxy config in `deploy/nginx/portfolio.conf`
- Added systemd service definition in `deploy/systemd/portfolio.service`
- Added deploy helper scripts for:
  - host bootstrap
  - app deployment
  - MySQL backup
- Documented host-mounted persistence model for:
  - `static/uploads`
  - `static/resume`
- Captured the temporary-free AWS constraint and same-server MySQL tradeoff in the runbook

## Files Touched

- `deploy/README.md`
- `deploy/nginx/portfolio.conf`
- `deploy/systemd/portfolio.service`
- `deploy/scripts/bootstrap-ubuntu.sh`
- `deploy/scripts/deploy-app.sh`
- `deploy/scripts/backup-mysql.sh`

## Notes

- This plan stops at deployment readiness and runbook quality
- Live EC2, Docker, Nginx, MySQL, domain, and certbot validation still need to happen on a real server
