from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Float, Index, Integer, String
from app.database import Base


class TelemetryMetric(Base):
    __tablename__ = "telemetry_metrics"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(String(64), nullable=False, index=True)
    metric_name = Column(String(128), nullable=False)
    value = Column(Float, nullable=False)
    recorded_at = Column(DateTime(timezone=True), nullable=False)
    ingested_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        Index("ix_source_recorded", "source_id", "recorded_at"),
    )
