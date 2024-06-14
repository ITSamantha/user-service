import pytest
from httpx import AsyncClient

from src.apps.employees.schemas.employee import CreateEmployee
from tests.conftest import app, async_client, event_loop, setup_db, setup_and_teardown_db


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_employee_positions(anyio_backend, async_client: AsyncClient):
    response = await async_client.get("/employees/positions")
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_employees(anyio_backend, async_client: AsyncClient):
    response = await async_client.get("/employees/")
    assert response.status_code == 200
    assert len(response.json()) == 0

    # employee: CreateEmployee = CreateEmployee()
    # response = await async_client.post("/employees/", data={})
