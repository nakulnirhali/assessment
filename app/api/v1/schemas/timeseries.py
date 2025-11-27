# app/api/v1/schemas/timeseries.py
from __future__ import annotations
from enum import Enum
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class IntervalEnum(str, Enum):
    TEN_MIN = "10min"
    HOUR = "1h"
    DAY = "1d"
    WEEK = "1w"

class Point(BaseModel):
    timestamp: datetime
    net: Optional[float] = Field(None, description="net value")
    buy: Optional[float] = Field(None, description="buy value")
    sell: Optional[float] = Field(None, description="sell value")
    total: Optional[float] = Field(None, description="total value")

class TimeseriesOut(BaseModel):
    symbol: str
    interval: IntervalEnum
    data: List[Point]
    request_id: Optional[str] = None

# keep module export names explicit
__all__ = ["IntervalEnum", "Point", "TimeseriesOut"]
