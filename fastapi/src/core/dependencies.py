from typing import Type

from src.core.database.session_manager import db_manager
from src.utils.repository.crud.base_crud_repository import SqlAlchemyRepository, ModelType


async def valid_id(model_id: int, model: Type[ModelType], model_name: str):
    """Returns object of given model with given id if exists."""

    instance: model = await SqlAlchemyRepository(db_manager.get_session,
                                                 model=model).get_single(id=model_id)

    if not instance:
        raise Exception(f"{model_name} with this data does not exist.")

    return instance
