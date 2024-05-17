from typing import List

from fastapi import APIRouter

from src.apps.employees import models
from src.core.database.session_manager import db_manager
from src.utils.repository.crud.base_crud_repository import SqlAlchemyRepository

router: APIRouter = APIRouter(
    prefix="/employees",
    tags=["employees"],
)


@router.get(path="")
async def get_employees():
    """Returns the list of user projects."""

    employees: List[models.Employee] = await SqlAlchemyRepository(db_manager.get_session,
                                                                  model=models.Employee).get_multi(deleted_at=None)
    return employees
