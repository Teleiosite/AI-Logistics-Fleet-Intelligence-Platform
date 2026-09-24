# Disaster recovery runbook

## Targets

- RPO: 1 hour when the backup job is scheduled hourly.
- RTO: 4 hours.
- Backups must be encrypted at rest and copied to a separate storage account.

## Backup

Run `tools/backup_postgres.sh` from a restricted operations runner with
`DATABASE_URL` and an off-host `BACKUP_DIR`. Upload both the dump and its
`.sha256` manifest to immutable object storage.

## Restore drill

1. Provision an isolated PostgreSQL instance.
2. Verify the checksum before importing.
3. Run `pg_restore --clean --if-exists --no-owner`.
4. Run `alembic upgrade head`.
5. Start the API and verify `/api/v1/health`, `/api/v1/ready`, authentication,
   and one tenant-isolation smoke test.
6. Record elapsed recovery time and corrective actions quarterly.

Never restore production data into a developer or shared staging database.
