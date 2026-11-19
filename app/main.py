from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import TelemetryMetric
from app.schemas import BatchIngestResponse, MetricRecordIn, MetricSummaryOut

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI + PostgreSQL ETL Ingestion Service",
    version="1.0.0",
)


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Database unreachable: {exc}")


@app.post("/api/v1/ingest", response_model=BatchIngestResponse, status_code=201)
def ingest_batch(records: list[MetricRecordIn], db: Session = Depends(get_db)):
    if not records:
        raise HTTPException(status_code=400, detail="Batch payload cannot be empty")

    orm_objects = [
        TelemetryMetric(
            source_id=item.source_id,
            metric_name=item.metric_name,
            value=item.value,
            recorded_at=item.recorded_at,
        )
        for item in records
    ]
    db.bulk_save_objects(orm_objects)
    db.commit()

    return BatchIngestResponse(status="ingested", records_inserted=len(orm_objects))


@app.get("/api/v1/metrics/{source_id}/summary", response_model=MetricSummaryOut)
def get_source_summary(source_id: str, db: Session = Depends(get_db)):
    row = (
        db.query(
            TelemetryMetric.source_id,
            func.count(TelemetryMetric.id).label("total_records"),
            func.avg(TelemetryMetric.value).label("avg_value"),
            func.max(TelemetryMetric.recorded_at).label("latest_recorded_at"),
        )
        .filter(TelemetryMetric.source_id == source_id)
        .group_by(TelemetryMetric.source_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail=f"No records found for {source_id}")

    return MetricSummaryOut(
        source_id=row.source_id,
        total_records=row.total_records,
        avg_value=round(float(row.avg_value), 4),
        latest_recorded_at=row.latest_recorded_at,
    )
