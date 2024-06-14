import datetime

import pytest
from httpx import AsyncClient

from src.apps.employees.schemas.vacation import CreateVacationType, UpdateVacationType, UpdateVacationReason, \
    CreateVacationReason, CreateVacation, UpdateVacation
from tests.conftest import app, async_client, event_loop, setup_db, setup_and_teardown_db

"""VACATION TYPES"""


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_vacation_types(anyio_backend, async_client: AsyncClient):
    response = await async_client.get("/employees/vacations/types")
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_work_vacation_types(anyio_backend, async_client: AsyncClient):
    instance: dict = CreateVacationType(title="Официальный").model_dump()
    response = await async_client.post("/employees/vacations/types", json=instance)
    assert response.status_code == 200
    assert response.json()["title"] == "Официальный"

    response = await async_client.get("/employees/vacations/types")
    assert response.status_code == 200
    assert len(response.json()) == 1

    instance: dict = CreateVacationType(title="Внеплановый").model_dump()
    response = await async_client.post("/employees/vacations/types", json=instance)
    assert response.status_code == 200

    response = await async_client.get("/employees/vacations/types")
    assert response.status_code == 200
    assert len(response.json()) == 2

    instance: dict = UpdateVacationType(title="Внеплановый").model_dump()
    response = await async_client.patch("/employees/vacations/types/1", json=instance)
    assert response.status_code == 500


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_delete_vacation_types(anyio_backend, async_client: AsyncClient):
    response = await async_client.delete("/employees/vacations/types/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Официальный"

    response = await async_client.get("/employees/vacations/types")
    assert response.status_code == 200
    assert len(response.json()) == 1


"""VACATION REASONS"""


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_vacation_reasons(anyio_backend, async_client: AsyncClient):
    response = await async_client.get("/employees/vacations/reasons")
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_work_vacation_reasons(anyio_backend, async_client: AsyncClient):
    instance: dict = CreateVacationReason(title="По семейным обстоятельствам").model_dump()
    response = await async_client.post("/employees/vacations/reasons", json=instance)
    assert response.status_code == 200
    assert response.json()["title"] == "По семейным обстоятельствам"

    response = await async_client.get("/employees/vacations/reasons")
    assert response.status_code == 200
    assert len(response.json()) == 1

    instance: dict = CreateVacationReason(title="Официальный").model_dump()
    response = await async_client.post("/employees/vacations/reasons", json=instance)
    assert response.status_code == 200

    response = await async_client.get("/employees/vacations/reasons")
    assert response.status_code == 200
    assert len(response.json()) == 2

    instance: dict = UpdateVacationReason(title="Официальный (месяц в год)").model_dump()
    response = await async_client.patch("/employees/vacations/reasons/2", json=instance)
    assert response.status_code == 200


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_delete_vacation_reasons(anyio_backend, async_client: AsyncClient):
    response = await async_client.delete("/employees/vacations/reasons/2")
    assert response.status_code == 200
    assert response.json()["title"] == "Официальный (месяц в год)"

    response = await async_client.get("/employees/vacations/reasons")
    assert response.status_code == 200
    assert len(response.json()) == 1


"""VACATION"""


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_vacations(anyio_backend, async_client: AsyncClient):
    response = await async_client.get("/employees/vacations")
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_work_vacations(anyio_backend, async_client: AsyncClient):
    instance: dict = CreateVacation(vacation_type_id=2,
                                    vacation_reason_id=1,
                                    comment=None,
                                    employee_id=2,
                                    start_date=datetime.date(2024, 12, 5),
                                    end_date=datetime.date(2024, 12, 3)).model_dump()
    response = await async_client.post("/employees/vacations", json=instance)
    assert response.status_code == 422

    response = await async_client.get("/employees/vacations")
    assert response.status_code == 200
    assert len(response.json()) == 0

    instance: dict = CreateVacation(vacation_type_id=2,
                                    vacation_reason_id=1,
                                    comment=None,
                                    employee_id=2,
                                    start_date=datetime.date(2024, 12, 3),
                                    end_date=datetime.date(2024, 12, 5)).model_dump()
    response = await async_client.post("/employees/vacations", json=instance)
    assert response.status_code == 200

    instance: dict = CreateVacation(vacation_type_id=2,
                                    vacation_reason_id=1,
                                    comment=None,
                                    employee_id=2,
                                    start_date=datetime.date(2024, 12, 4),
                                    end_date=datetime.date(2024, 12, 12)).model_dump()
    response = await async_client.post("/employees/vacations", json=instance)
    assert response.status_code == 422

    response = await async_client.get("/employees/vacations")
    assert response.status_code == 200
    assert len(response.json()) == 1

    instance: dict = UpdateVacation(vacation_type_id=2,
                                    vacation_reason_id=1,
                                    comment="Всё-таки в отпуск!",
                                    start_date=datetime.date(2024, 12, 3),
                                    end_date=datetime.date(2024, 12, 5)).model_dump()
    response = await async_client.patch("/employees/vacations/1", json=instance)
    assert response.status_code == 200
    assert response.json()["comment"] == "Всё-таки в отпуск!"
