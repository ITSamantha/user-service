import pytest
from httpx import AsyncClient

from src.apps.employees.schemas.employee import CreateEmployee, CreateEmployeePosition, UpdateEmployeePosition, \
    UpdateEmployee
from tests.conftest import app, async_client, event_loop, setup_and_teardown_db

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


"""EMPLOYEE"""


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_employees(anyio_backend, async_client: AsyncClient):
    response = await async_client.get("/employees/")
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_work_employees(anyio_backend, async_client: AsyncClient):
    instance: dict = CreateEmployee(last_name="Попов",
                                    first_name="Поп",
                                    patronymic=None,
                                    login="popovpop",
                                    password="qwerty222222",
                                    email="popovpop@gmail.com",
                                    unit_id=1,
                                    position_id=2).model_dump()
    response = await async_client.post("/employees/", json=instance)
    assert response.status_code == 200

    response = await async_client.get("/employees/")
    assert response.status_code == 200
    assert len(response.json()) == 1

    instance: dict = CreateEmployee(last_name="Иванов",
                                    first_name="Иван",
                                    patronymic=None,
                                    login="popovpop11",
                                    email="popovpop@gmail.com",
                                    password="qw5jsjy222222",
                                    unit_id=1,
                                    position_id=2).model_dump()

    response = await async_client.post("/employees/", json=instance)
    assert response.status_code == 500

    response = await async_client.get("/employees/")
    assert response.status_code == 200
    assert len(response.json()) == 1

    instance: dict = UpdateEmployee(last_name="Поляков",
                                    first_name="Алексей",
                                    patronymic=None,
                                    login="popovpop",
                                    password="qwerty222222",
                                    email="popovpop@gmail.com",
                                    unit_id=1,
                                    position_id=2).model_dump()
    response = await async_client.patch("/employees/1", json=instance)
    assert response.status_code == 200
    assert response.json()["last_name"] == "Поляков"
