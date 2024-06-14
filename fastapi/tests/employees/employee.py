import pytest
from httpx import AsyncClient

from src.apps.employees.schemas.employee import CreateEmployee, CreateEmployeePosition, UpdateEmployeePosition
from tests.conftest import app, async_client, event_loop, setup_db, setup_and_teardown_db

"""EMPLOYEE POSITIONS"""


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_employee_positions(anyio_backend, async_client: AsyncClient):
    response = await async_client.get("/employees/positions")
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_work_employee_positions(anyio_backend, async_client: AsyncClient):
    instance: dict = CreateEmployeePosition(title="Главный программист 1").model_dump()
    response = await async_client.post("/employees/positions", json=instance)
    assert response.status_code == 200
    assert response.json()["title"] == "Главный программист 1"

    response = await async_client.get("/employees/positions")
    assert response.status_code == 200
    assert len(response.json()) == 1

    instance: dict = CreateEmployeePosition(title="Руководитель").model_dump()
    response = await async_client.post("/employees/positions", json=instance)
    assert response.status_code == 200
    assert response.json()["title"] == "Руководитель"

    response = await async_client.get("/employees/positions")
    assert response.status_code == 200
    assert len(response.json()) == 2

    instance: dict = CreateEmployeePosition(title="Главный программист 1").model_dump()
    response = await async_client.post("/employees/positions", json=instance)
    assert response.status_code == 500

    response = await async_client.get("/employees/positions")
    assert response.status_code == 200
    assert len(response.json()) == 2

    instance: dict = UpdateEmployeePosition(title="Главный программист").model_dump()
    response = await async_client.patch("/employees/positions/1", json=instance)
    assert response.status_code == 200
    assert response.json()["title"] == "Главный программист"


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_delete_employee_positions(anyio_backend, async_client: AsyncClient):
    response = await async_client.delete("/employees/positions/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Главный программист"

    response = await async_client.get("/employees/positions")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_employees(anyio_backend, async_client: AsyncClient):
    response = await async_client.get("/employees/")
    assert response.status_code == 200
    assert len(response.json()) == 0

    # employee: CreateEmployee = CreateEmployee()
    # response = await async_client.post("/employees/", data={})
