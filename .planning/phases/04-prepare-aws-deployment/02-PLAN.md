---
plan_id: "02"
phase: "04"
phase_name: "Prepare AWS Deployment"
title: "Define EC2 Host Setup, HTTPS Routing, Persistence, and Backup Runbook"
wave: 2
depends_on:
  - "01"
requirements_addressed:
  - "PLAT-02"
autonomous: true
files_modified:
  - "deploy/README.md"
  - "deploy/nginx/portfolio.conf"
  - "deploy/systemd/portfolio.service"
  - "scripts/deploy/*.sh"
---

# Plan 02: Define EC2 Host Setup, HTTPS Routing, Persistence, and Backup Runbook

## Objective

Turn the containerized Flask runtime into a concrete EC2 deployment plan: Ubuntu host setup, host-installed MySQL, Nginx reverse proxy, HTTPS, domain routing, mounted persistence, and a manual deploy/backup runbook that can actually be executed on a temporary-free AWS server.

## Must Haves

- Deployment target is an EC2 Ubuntu host, not Lightsail or Elastic Beanstalk
- MySQL is installed directly on the host, not in Docker
- Nginx reverse-proxies traffic to the Flask container
- Public deployment includes custom domain and HTTPS
- Upload directories and resume file are persisted on the host outside the container
- Backup procedure covers MySQL dumps and file uploads

## Tasks

<task id="02-1" type="host-setup">
  <goal>Document the EC2 host preparation steps for Docker, Nginx, MySQL, and runtime directories.</goal>
  <details>
    Capture the exact packages, services, directories, and ownership model needed on an Ubuntu host.
    Include the host paths used for mounted uploads, resume storage, and deployment artifacts.
    Keep the setup optimized for one small server rather than future cluster scaling.
  </details>
</task>

<task id="02-2" type="reverse-proxy-and-https">
  <goal>Provide Nginx and HTTPS configuration that works with the SPA and the Flask container.</goal>
  <details>
    Ensure `/about`, `/projects`, and other public SPA routes remain compatible behind the reverse proxy.
    Include a concrete Nginx site config and the certbot/HTTPS steps needed for deployment.
    Preserve admin and public routing within the same Flask service.
  </details>
</task>

<task id="02-3" type="service-management">
  <goal>Define how the Dockerized app is started and kept alive on reboot.</goal>
  <details>
    Use a systemd-managed service or equivalent reproducible host mechanism.
    Make the restart path explicit for manual deploys and crash recovery.
    Avoid adding a full CI/CD system in this phase.
  </details>
</task>

<task id="02-4" type="deploy-runbook">
  <goal>Create a repeatable manual deployment and backup runbook.</goal>
  <details>
    Document the SSH-based deployment sequence: code update, image build, container restart, migration/db checks, and health checks.
    Add a backup routine using scheduled `mysqldump`.
    Include operational warnings for free-tier expiry, same-server DB risk, and local-disk upload limitations.
  </details>
</task>

## Verification

- A new EC2 host can be prepared from the runbook without inventing missing steps
- Nginx config supports direct SPA URLs and admin routes through the Flask container
- The app uses host-mounted directories for uploads/resume instead of container-only storage
- Backup instructions are concrete enough to schedule and test

## Exit Criteria

- The project has a realistic first-production EC2 deployment path that matches all locked Phase 4 decisions
- Deployment execution can proceed without unresolved architectural ambiguity

