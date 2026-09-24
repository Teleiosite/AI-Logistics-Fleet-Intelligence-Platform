#!/usr/bin/env bash
set -Eeuo pipefail

: "${DATABASE_URL:?DATABASE_URL is required}"
: "${BACKUP_DIR:=/var/backups/fleetiq}"
mkdir -p "$BACKUP_DIR"

timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
output="$BACKUP_DIR/fleetiq-$timestamp.dump"
pg_dump "$DATABASE_URL" --format=custom --no-owner --file="$output"
sha256sum "$output" > "$output.sha256"
find "$BACKUP_DIR" -type f -mtime +"${BACKUP_RETENTION_DAYS:-30}" -delete
echo "Created $output"
