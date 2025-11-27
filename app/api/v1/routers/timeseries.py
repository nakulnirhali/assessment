from fastapi import APIRouter, Query, Depends, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import json
import uuid

from sqlalchemy import select, asc, desc
from app.db.session import get_session
from app.models.mv import timeseries_mv
from app.api.v1.schemas.timeseries import Point, TimeseriesOut, IntervalEnum
from app.cache.redis_client import get_cached, set_cached
from app.core import config

router = APIRouter()

# inside the file: replace the timeseries handler with this
@router.get("/timeseries", response_model=TimeseriesOut)
async def timeseries(
    request: Request,
    response: Response,
    symbol: str | None = Query(None),
    figi: str | None = Query(None),
    interval: IntervalEnum = Query(...),
    fields: str | None = Query(None),
    start_date: str | None = Query(None),
    end_date: str | None = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    page: int = Query(1, ge=1),
    order: str = Query("desc"),
    db = Depends(get_session),
):
    # basic validation
    if not symbol and not figi:
        return JSONResponse(status_code=400, content={"detail": "symbol or figi required"})

    query_symbol = symbol or figi

    # Build a deterministic cache key from query params
    cache_key = f"timeseries:symbol={query_symbol}|interval={interval}|fields={fields or ''}|start={start_date or ''}|end={end_date or ''}|limit={limit}|page={page}|order={order}"

    # Try cache
    cached = await get_cached(cache_key)
    if cached:
        # cached is JSON string
        response.headers["X-Cache"] = "HIT"
        # cached content already matches TimeseriesOut shape
        return JSONResponse(content=json.loads(cached))

    # Not cached -> query DB
    stmt = select(timeseries_mv).where(timeseries_mv.c.symbol == query_symbol)

    if order.lower() == "desc":
        stmt = stmt.order_by(desc(timeseries_mv.c.timestamp))
    else:
        stmt = stmt.order_by(asc(timeseries_mv.c.timestamp))

    offset = (page - 1) * limit
    stmt = stmt.limit(limit).offset(offset)

    res = await db.execute(stmt)
    rows = res.mappings().all()

    points = [
        Point(
            timestamp=r.get("timestamp"),
            net=r.get("net"),
            buy=r.get("buy"),
            sell=r.get("sell"),
            total=r.get("total"),
        )
        for r in rows
    ]

    payload = {
    "symbol": query_symbol,
    "interval": interval,
    # convert Pydantic models to dicts first
    "data": [p.dict() for p in points],
    "request_id": request.state.request_id if hasattr(request.state, "request_id") else str(uuid.uuid4()),
    }

    # Encode to JSON-friendly types (handles datetime -> isoformat automatically)
    content = jsonable_encoder(payload)

    # Store in cache (store JSON string)
    ttl = getattr(config.settings, "CACHE_TTL_SECONDS", None)
    try:
        # json.dumps on content is safe because jsonable_encoder replaced datetimes
        await set_cached(cache_key, json.dumps(content), ttl=ttl)
    except Exception:
        pass

    response.headers["X-Cache"] = "MISS"
    return JSONResponse(content=content)