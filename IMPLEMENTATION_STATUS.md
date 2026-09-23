# FleetIQ Implementation Status

This repository now contains a cross-stack production baseline aligned to the FleetIQ product documentation.

## Completed

### Backend platform
- FastAPI app with versioned APIs, CORS, and tenant-aware JWT auth.
- Endpoint-level RBAC policy checks using resource/action permissions.
- Core logistics domains implemented: companies, fleet, shipments, fuel, DVR, invoices, analytics, notifications, AI.
- Shipment workflow guardrails:
  - explicit transition matrix
  - assignment required before dispatch
  - POD required before delivery completion
  - timeline logging
- Fuel anomaly detection rules:
  - excessive fill (>110% tank capacity)
  - frequent fill anomaly (>=2 fills in 24h)
- Invoice workflow additions:
  - text-based OCR extraction pipeline
  - invoice line-item generation
  - auto-match endpoint
  - dispute memo generation
- Production baseline additions:
  - PDF/text invoice document ingestion
  - trained delay-model loading with deterministic fallback
  - readiness and request metrics endpoints
  - tenant-scoped vehicle location telemetry API
  - persistent geofence event history and tenant-scoped SSE event stream
  - constrained tenant-scoped analytics copilot with input limits and SQL rejection
  - automated backend/frontend CI workflow

### Infrastructure and ops
- PostgreSQL-first defaults in config and docker-compose.
- Redis and Celery worker integration for async notifications.
- Alembic migration framework with baseline initial migration.

### AI/ML
- Delay prediction endpoint loads a trained model artifact when available.
- Training pipeline accepts validated historical shipment CSV data.

### Frontend and mobile
- Next.js dashboard skeleton in `frontend/`.
- Flutter driver app skeleton in `mobile/`.

### Testing
- Expanded tests for health, authorization policy, and invoice text extraction.

## Remaining for a production launch
1. Configure and contract-test a real image OCR provider, LLM provider, and model registry.
2. Add managed map rendering, route/traffic providers, and horizontally scalable event streaming.
3. Replace the mobile preference queue with SQLite/Drift, background GPS, push delivery, and offline POD/fuel sync.
4. Add ERP/payment/GPS provider adapters, distributed tracing, centralized logs, alerting, backups, and restore drills.
5. Add Kubernetes/ECS promotion, migrations, smoke tests, approvals, rollback, and staging-to-production controls.
6. Reach measured >80% backend coverage plus frontend/mobile/load/security/UAT/DR suites and remediate frontend advisories.
