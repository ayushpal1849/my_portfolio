#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/ayush-portfolio}"
cd "$APP_DIR"

mkdir -p runtime-data/uploads/certs runtime-data/resume deploy/backups

docker compose build
docker compose up -d
docker compose run --rm app flask db upgrade

echo "Deployment complete."
