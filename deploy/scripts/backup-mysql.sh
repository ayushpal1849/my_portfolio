#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/ayush-portfolio}"
ENV_FILE="${ENV_FILE:-$APP_DIR/.env}"
BACKUP_DIR="${BACKUP_DIR:-$APP_DIR/deploy/backups}"

if [ ! -f "$ENV_FILE" ]; then
  echo "Missing env file: $ENV_FILE" >&2
  exit 1
fi

mkdir -p "$BACKUP_DIR"

DATABASE_URL="$(grep '^DATABASE_URL=' "$ENV_FILE" | cut -d '=' -f 2-)"
if [ -z "$DATABASE_URL" ]; then
  echo "DATABASE_URL is required in $ENV_FILE" >&2
  exit 1
fi

mapfile -t DB_PARTS < <(python3 - "$DATABASE_URL" "$BACKUP_DIR" <<'PY'
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

database_url = sys.argv[1]
backup_dir = Path(sys.argv[2])
parsed = urlparse(database_url)

username = parsed.username or ""
password = parsed.password or ""
host = parsed.hostname or "127.0.0.1"
port = str(parsed.port or 3306)
database = parsed.path.lstrip("/")

print(username)
print(password)
print(host)
print(port)
print(database)
timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
target = backup_dir / f"{database}-{timestamp}.sql"
print(target)
PY
)

DB_USER="${DB_PARTS[0]}"
DB_PASS="${DB_PARTS[1]}"
DB_HOST="${DB_PARTS[2]}"
DB_PORT="${DB_PARTS[3]}"
DB_NAME="${DB_PARTS[4]}"
TARGET_FILE="${DB_PARTS[5]}"

MYSQL_PWD="$DB_PASS" mysqldump \
  -h "$DB_HOST" \
  -P "$DB_PORT" \
  -u "$DB_USER" \
  --single-transaction \
  --quick \
  --lock-tables=false \
  "$DB_NAME" > "$TARGET_FILE"

echo "Backup written to $TARGET_FILE"
