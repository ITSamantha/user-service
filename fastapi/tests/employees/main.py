import pytest
from httpx import AsyncClient
from tests.conftest import app, async_client, event_loop


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_root(anyio_backend, async_client: AsyncClient):
    response = await async_client.get("/employees/")
    assert response.status_code == 200
