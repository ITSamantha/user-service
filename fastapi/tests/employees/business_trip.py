import pytest
from httpx import AsyncClient

from src.apps.employees.schemas.business_trip import UpdateBusinessTrip, CreateBusinessTrip
from tests.conftest import app, async_client, event_loop, setup_and_teardown_db

"""BusinessTrip"""


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_business_trips(anyio_backend, async_client: AsyncClient):
    response = await async_client.get("/employees/business_trips")
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_work_business_trips(anyio_backend, async_client: AsyncClient):
    instance: dict = CreateBusinessTrip(purpose="Отдыхать",
                                        destination="Анапа",
                                        comment=None,
                                        employee_id=2,
                                        start_date="2024-12-05",
                                        end_date="2024-12-03").model_dump()

    instance["start_date"] = "2024-12-05"
    instance["end_date"] = "2024-12-03"

    response = await async_client.post("/employees/business_trips", json=instance)
    assert response.status_code == 500

    response = await async_client.get("/employees/business_trips")
    assert response.status_code == 200
    assert len(response.json()) == 0

    instance: dict = CreateBusinessTrip(purpose="Отдыхать",
                                        destination="Анапа",
                                        comment=None,
                                        employee_id=2,
                                        start_date="2024-12-14",
                                        end_date="2024-12-19").model_dump()

    instance["start_date"] = "2024-12-14"
    instance["end_date"] = "2024-12-19"

    response = await async_client.post("/employees/business_trips", json=instance)
    assert response.status_code == 200

    instance: dict = CreateBusinessTrip(purpose="Отдыхать",
                                        destination="Анапа",
                                        comment=None,
                                        employee_id=2,
                                        start_date="2024-12-16",
                                        end_date="2024-12-17").model_dump()

    instance["start_date"] = "2024-12-16"
    instance["end_date"] = "2024-12-17"

    response = await async_client.post("/employees/business_trips", json=instance)
    assert response.status_code == 400

    response = await async_client.get("/employees/business_trips")
    assert response.status_code == 200
    assert len(response.json()) == 1

    instance: dict = UpdateBusinessTrip(purpose="Отдыхать",
                                        destination="Анапа",
                                        comment="УРА, АНАПА!",
                                        start_date="2024-12-14",
                                        end_date="2024-12-19").model_dump()

    instance["start_date"] = "2024-12-14"
    instance["end_date"] = "2024-12-19"

    response = await async_client.patch("/employees/business_trips/1", json=instance)
    assert response.status_code == 200
    print(response.json())
    assert response.json()["comment"] == "УРА, АНАПА!"
