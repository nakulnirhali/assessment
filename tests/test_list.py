import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_list_endpoint_exists():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/list")
        # endpoint should exist; allow 200 or 401 depending on auth config
        assert r.status_code in (200, 401)
