from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional, List

class Interval(str, Enum):
    ten_min = "10min"
    one_hour = "1h"
    one_day = "1d"
    one_week = "1w"

class Field(str, Enum):
    net = "net"
    buy = "buy"
    sell = "sell"
    total = "total"

class Point(BaseModel):
    timestamp: datetime
    net: Optional[float]
    buy: Optional[float]
    sell: Optional[float]
    total: Optional[float]

class TSResponse(BaseModel):
    symbol: str
    interval: Interval
    data: List[Point]
    request_id: str
