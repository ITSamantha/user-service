from typing import Type, Union

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.employees.schemas.business_trip import CreateBusinessTrip
from src.apps.employees.schemas.vacation import CreateVacation
from src.apps.employees.utils.utils import check_business_trips_valid_dates, check_vacations_valid_dates
from src.core.database.session_manager import db_manager
from src.utils.repository.crud.base_crud_repository import SqlAlchemyRepository, ModelType


async def valid_id(model_id: int, model: Type[ModelType], model_name: str = "The model"):
    """Returns object of given model with given id if exists."""

    instance: model = await SqlAlchemyRepository(db_manager.get_session,
                                                 model=model).get_single(id=model_id)

    if not instance:
        raise Exception(f"{model_name} with this data does not exist.")

    return instance


async def valid_dates(data: Union[CreateBusinessTrip, CreateVacation]):
    """Returns schema with validated dates."""

    try:
        await check_vacations_valid_dates(data)
        await check_business_trips_valid_dates(data)
    except Exception as e:
        raise Exception(str(e))

    return data


async def is_deleted_model(model_id: int, model: Type[ModelType], model_name: str = "The model"):
    """Returns object of given model with given id if exists and not deleted."""

    instance: model = await valid_id(model_id, model, model_name)

    if instance.deleted_at:
        raise Exception(f"{model_name} with this data has already been deleted.")

    return instance
