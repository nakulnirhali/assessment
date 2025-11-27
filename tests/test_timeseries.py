import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_timeseries_endpoint_exists():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/timeseries?symbol=AAPL")
        # accepts 200/400/401 depending on environment and presence of seeded data
        assert r.status_code in (200, 400, 401)
