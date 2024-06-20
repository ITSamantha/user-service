from typing import Type, TypeVar

from src.apps.employees.utils.utils import check_business_trips_valid_dates, check_vacations_valid_dates
from src.core.database.session_manager import db_manager
from src.core.schemas.base import BaseSchemaModel
from src.utils.repository.crud.base_crud_repository import SqlAlchemyRepository, ModelType

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseSchemaModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseSchemaModel)


async def valid_id(model_id: int, model: Type[ModelType], model_name: str = "The model"):
    """Returns object of given model with given id if exists."""

    instance: model = await SqlAlchemyRepository(db_manager.get_session,
                                                 model=model).get_single(id=model_id)

    if not instance:
        raise Exception(f"{model_name} with this data does not exist.")

    return instance


async def valid_dates(data: CreateSchemaType | UpdateSchemaType, object_id: int = None):
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
