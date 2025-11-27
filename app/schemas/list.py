from pydantic import BaseModel
from typing import Optional, List

class SymbolOut(BaseModel):
    symbol: str
    name: Optional[str]
    is_active: Optional[bool]
    sector: Optional[str]
    industry: Optional[str]
    asset_type: Optional[str]

class ListResponse(BaseModel):
    items: List[SymbolOut]
    page: int
    limit: int
    total: int
