# FastAPI + PostgreSQL ETL Ingestion Service

Modular backend service for batch telemetry/data ingestion, Pydantic v2 schema validation, bulk SQLAlchemy PostgreSQL writes, and SQL aggregation endpoints.

Built as a sanitized reference architecture demonstrating the modular FastAPI, Pydantic v2, and SQLAlchemy bulk-ingestion patterns I use in production ETL and telemetry pipelines (where client code is NDA-protected)

### Architecture
- `app/database.py` — Pooled SQLAlchemy engine (`pool_pre_ping=True`) and request-scoped DB sessions.
- `app/models.py` — PostgreSQL schema with composite indexing (`source_id`, `recorded_at`) for time-range queries.
- `app/schemas.py` — Strict Pydantic v2 input/output validation models.
- `app/main.py` — `/health` DB probe, `/api/v1/ingest` bulk insert pipeline, and `/api/v1/metrics/{source_id}/summary` aggregation query.

### Run Full Stack with Docker Compose
    docker compose up --build

Interactive API docs will be live at `http://localhost:8000/docs`.
