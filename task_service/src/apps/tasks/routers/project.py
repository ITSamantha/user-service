from typing import List

from fastapi import APIRouter, Depends

from src.apps.tasks import models
from src.apps.tasks.dependencies import valid_project_id, existing_project
from src.apps.tasks.schemas.project import Project, CreateProject, UpdateProject
from src.apps.tasks.transformers.project import ProjectTransformer
from src.core.database.session_manager import db_manager
from src.core.schemas.base import BaseDeleteSchema
from src.utils.handlers import api_handler
from src.utils.repository.crud.base_crud_repository import SqlAlchemyRepository
from src.utils.transformer import transform

router: APIRouter = APIRouter(
    prefix="/projects",
    tags=["projects"],
)

"""PROJECT"""


@router.get(path="", response_model=List[Project], tags=["projects"])
@api_handler
async def get_projects():
    """Returns the list of all projects."""

    projects: List[models.Project] = await SqlAlchemyRepository(db_manager.get_session,
                                                                model=models.Project).get_multi()
    return transform(projects, ProjectTransformer().include(["tasks"]))


@router.get(path="/{project_id}", response_model=Project, tags=["projects"])
@api_handler
async def get_project_by_id(project: models.Project = Depends(valid_project_id)):
    """Returns project with id=project_id."""

    return transform(project, ProjectTransformer().include(["tasks"]))


@router.post(path="", response_model=Project, tags=["projects"])
@api_handler
async def create_project(data: CreateProject):
    """Returns created with the given data project."""

    project: models.Project = await SqlAlchemyRepository(db_manager.get_session,
                                                         model=models.Project).create(data=data)
    return transform(project, ProjectTransformer())


@router.patch(path="/{project_id}", response_model=Project, tags=["projects"])
@api_handler
async def update_project_by_id(project_id: int, data: UpdateProject) -> Project:
    """Returns updated with given data project."""

    project: models.Project = await SqlAlchemyRepository(db_manager.get_session,
                                                         model=models.Project).update(
        data=data,
        id=project_id)
    return transform(project, ProjectTransformer())


@router.delete(path="/{project_id}", response_model=Project, tags=["projects"])
@api_handler
async def delete_project(project: models.Project = Depends(existing_project)) -> Project:
    """Returns deleted project."""

    project: models.Project = await SqlAlchemyRepository(db_manager.get_session,
                                                         model=models.Project).update(
        data=BaseDeleteSchema(),
        id=project.id)
    return transform(project, ProjectTransformer())
