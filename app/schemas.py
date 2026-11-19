from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class MetricRecordIn(BaseModel):
    source_id: str = Field(..., min_length=2, max_length=64, examples=["gateway-01"])
    metric_name: str = Field(..., min_length=1, max_length=128, examples=["cpu_temp_c"])
    value: float = Field(..., examples=[64.5])
    recorded_at: datetime


class BatchIngestResponse(BaseModel):
    status: str
    records_inserted: int


class MetricSummaryOut(BaseModel):
    source_id: str
    total_records: int
    avg_value: float
    latest_recorded_at: datetime
