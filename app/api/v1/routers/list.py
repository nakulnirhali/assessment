from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, and_
from app.db.models import symbols
from app.schemas.list import ListResponse, SymbolOut
from app.db.session import get_session
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/list", response_model=ListResponse)
async def list_symbols(
    asset_type: str | None = Query(None),
    sector: str | None = Query(None),
    industry: str | None = Query(None),
    is_active: bool | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    db = Depends(get_session),
    user = Depends(get_current_user),
):
    offset = (page - 1) * limit
    conditions = []
    if asset_type:
        conditions.append(symbols.c.asset_type == asset_type)
    if sector:
        conditions.append(symbols.c.sector == sector)
    if industry:
        conditions.append(symbols.c.industry == industry)
    if is_active is not None:
        conditions.append(symbols.c.is_active == is_active)

    stmt = select(symbols).where(and_(*conditions)) if conditions else select(symbols)
    stmt = stmt.limit(limit).offset(offset)

    res = await db.execute(stmt)
    rows = res.fetchall()

    items = []
    for r in rows:
        # access via Row._mapping to get column-name keyed mapping (works across SQLAlchemy versions)
        m = r._mapping
        items.append(
            SymbolOut(
                symbol = m.get("symbol"),
                name = m.get("name"),
                is_active = m.get("is_active"),
                sector = m.get("sector"),
                industry = m.get("industry"),
                asset_type = m.get("asset_type"),
            )
        )

    # For demo keep total = count of returned rows (real impl should count all matches)
    return ListResponse(items=items, page=page, limit=limit, total=len(items))

